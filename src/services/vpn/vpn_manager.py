import logging
import uuid
from datetime import datetime
from typing import Any

from src.core.models.connection import Connection
from src.core.models.promo import Promo
from src.core.models.subscription import Subscription
from src.services.storage.infrastructure.interfaces.i_promo_manager import IPromoManager
from src.services.vpn.exceptions import ApplyPromoException
from src.services.vpn.i_vpn_manager import IVpnManager, ApplyPromoResult, ApplyPromoResultValues
from src.utils import dt_utils

logger = logging.getLogger(__name__)


class VpnManager(IVpnManager):
    async def create_connection(self) -> str:
        pass

    async def update_subscription(self, sub_id: int, new_data: dict[str, Any]) -> bool:
        pass

    async def create_new_subscription(
            self, subscription: Subscription,
            user_id: int, username: str, connection_number: int
    ) -> str:
        connection_id = uuid.uuid4()
        await self._subscription_manager.create_subscription(subscription)
        connection_link = await self._vpn_repository.add_client_with_connection_string(
            connection_id=connection_id,
            user_email=self.create_user_email_for_vpn(user_id, username, connection_number)
        )
        await self._connection_manager.add_new_connection(
            Connection(
                id=connection_id,
                user_id=user_id,
                link=connection_link
            )
        )
        return connection_link

    async def extend_subscription(self) -> bool:
        pass

    async def apply_promo(
            self, promo: Promo,
            user_id: int,
            username: str,
            promo_manager: IPromoManager
    ) -> ApplyPromoResult:
        user_sub = await self._subscription_manager.get_user_subscription(user_id)
        if user_sub is None:
            # if first user sub
            new_until = dt_utils.add_mount(datetime.now(), promo.duration)
            user_sub = Subscription(
                id=None,
                user_id=user_id,
                last_payment=None,
                sale=100,
                until=new_until,
                active_links=1,
                is_active=True,
            )
            connection_link = await self.create_new_subscription(
                subscription=user_sub,
                user_id=user_id,
                username=username,
                connection_number=1
            )
            result = ApplyPromoResult(
                result=ApplyPromoResultValues.CREATE_NEW,
                connection_link=connection_link,
                new_until=new_until
            )
        elif user_sub.is_active:
            # If user already has active sub
            old_until = user_sub.until
            new_until = dt_utils.add_mount(old_until, promo.duration)
            if await self.extend_subscription():  # TODO in STEAL-17
                result = ApplyPromoResult(
                    result=ApplyPromoResultValues.EXTEND_ACTIVE,
                    new_until=new_until,
                    old_until=old_until
                )
            else:
                raise ApplyPromoException(f"Can't apply promo")  # TODO need more details message
        else:
            # if user already has sub, but it not activ
            new_until = dt_utils.add_mount(datetime.now(), promo.duration)
            if await self.update_subscription(
                    user_sub.id,
                    {
                        "last_payment": None,
                        "until": new_until,
                        "is_active": True,
                        "active_links": 1
                    }
            ):
                connection_link = await self.create_connection()
                result = ApplyPromoResult(
                    result=ApplyPromoResultValues.EXTEND_NON_ACTIVE,
                    connection_link=connection_link,
                    new_until=new_until
                )
            else:
                logger.error("Can't apply promo: update subscription failed")
                raise ApplyPromoException("Can't apply promo: update subscription failed")

        if await promo_manager.delete_promo(promo.id):
            return result
        else:
            logger.error("Failed changer promo activity")
