import logging
from typing import Any

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.future import select

from src.services.storage.repository.exceptions import RepositorySubscriptionCreationError, RepositoryException, \
    RepositorySubscriptionNotFound, handle_db_exception
from src.services.storage.repository.interfaces.i_subscription_repository import IPostgresSubscriptionRepository
from src.services.storage.schemas.subscription import Subscription

logger = logging.getLogger(__name__)


class PostgresSubscriptionRepository(IPostgresSubscriptionRepository):
    @handle_db_exception(exception_mapping={'subscription': RepositorySubscriptionNotFound})
    # Возможно возращать он должен не дикт а лист
    async def get_user_subscription(self, user_id: int) -> dict[str, Any]:
        async with self.async_session() as session:
            result = await session.execute(
                select(Subscription).filter(Subscription.user_id == user_id)
            )
            subscription = result.scalar_one()

            if subscription:
                return {
                    'id': subscription.id,
                    'user_id': subscription.user_id,
                    'last_payment': subscription.last_payment,
                    'sale': subscription.sale,
                    'until': subscription.until,
                    'active_links': subscription.active_links,
                    'is_active': subscription.is_active
                }

    @handle_db_exception(exception_mapping={'subscription': RepositorySubscriptionCreationError})
    async def create_subscription(self, subscription: Subscription) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add(subscription)

    @handle_db_exception(exception_mapping={'subscription': RepositorySubscriptionNotFound})
    async def update_subscription(self, subscription_id: int, update_fields: dict) -> dict:
        async with self.async_session() as session:
            async with session.begin():
                stmt = (
                    update(Subscription)
                    .where(Subscription.id == subscription_id)
                    .values(update_fields)
                    .returning(Subscription)
                )

                result = await session.execute(stmt)
                updated_subscription = result.scalar_one()

                if updated_subscription:
                    return {
                        'id': updated_subscription.id,
                        'user_id': updated_subscription.user_id,
                        'last_payment': updated_subscription.last_payment,
                        'sale': updated_subscription.sale,
                        'until': updated_subscription.until,
                        'active_links': updated_subscription.active_links,
                        'is_active': updated_subscription.is_active
                    }
