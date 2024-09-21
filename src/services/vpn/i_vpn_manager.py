from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, NamedTuple

from src.core.models.promo import Promo
from src.core.models.subscription import Subscription
from src.services.storage.infrastructure.interfaces.i_connection_manager import IConnectionManager
from src.services.storage.infrastructure.interfaces.i_promo_manager import IPromoManager
from src.services.storage.infrastructure.interfaces.i_subscription_manager import ISubscriptionStorageManager
from src.services.vpn.i_vpn_repository import IVpnRepository


class ApplyPromoResultValues(Enum):
    CREATE_NEW = 1
    EXTEND_ACTIVE = 2
    EXTEND_NON_ACTIVE = 3

class ApplyPromoResult(NamedTuple):
    result: ApplyPromoResultValues
    connection_link: str | None = None
    old_until: datetime | None = None
    new_until: datetime | None = None


class IVpnManager(ABC):
    def __init__(
            self, vpn_repository: IVpnRepository,
            subscription_manager: ISubscriptionStorageManager,
            connection_manager: IConnectionManager
    ) -> None:
        self._vpn_repository = vpn_repository
        self._subscription_manager = subscription_manager
        self._connection_manager = connection_manager

    @staticmethod
    def create_user_email_for_vpn(user_id: int, username: str, connection_number: int) -> str:
        return f"{username}_{user_id}_{connection_number}"

    @abstractmethod
    async def create_connection(self) -> str:
        ...

    @abstractmethod
    async def create_new_subscription(
            self, subscription: Subscription,
            user_id: str, username: str, connection_number: int
    ) -> str:
        ...

    @abstractmethod
    async def extend_subscription(self) -> bool:
        ...

    @abstractmethod
    async def update_subscription(self, sub_id: int, new_data: dict[str, Any]) -> bool:
        ...

    @abstractmethod
    async def apply_promo(
            self, promo: Promo,
            user_id: int, username: str,
            promo_manager: IPromoManager
    ) -> ApplyPromoResult:
        ...
