import logging
from typing import Any

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.future import select

from src.services.storage.repository.exceptions import RepositorySubscriptionCreationError, RepositoryException, \
    RepositorySubscriptionNotFound
from src.services.storage.repository.interfaces.i_subscription_repository import IPostgresSubscriptionRepository
from src.services.storage.schemas.subscription import Subscription

logger = logging.getLogger(__name__)


class PostgresSubscriptionRepository(IPostgresSubscriptionRepository):
    async def get_user_subscription(self, user_id: int) -> dict[str, Any]:
        async with self.async_session() as session:
            try:
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
            except NoResultFound:
                logger.info(f'No result found for subscription with ID {user_id}.')
                raise RepositorySubscriptionNotFound(user_id)
            except Exception as e:
                logger.error(f'Error occurred while fetching subscription with ID {user_id}')
                raise RepositoryException(f'Error occurred while fetching subscription with ID {user_id}')

    async def create_subscription(self, subscription: Subscription) -> None:
        try:
            async with self.async_session() as session:
                async with session.begin():
                    session.add(subscription)
        except SQLAlchemyError as e:
            logger.error(f'Error occurred while creating subscription with ID {subscription.id}: {e}')
            raise RepositorySubscriptionCreationError(
                f'Error occurred while creating subscription with ID {subscription.id}: {e}')
        except Exception as e:
            logger.error(f'Unexpected error occurred while creating subscription with ID {subscription.id}: {e}')
            raise RepositoryException(
                f'Unexpected error occurred while creating subscription with ID {subscription.id}')

    async def update_subscription(self, subscription_id: int, update_fields: dict) -> dict:
        async with self.async_session() as session:  # Используйте async_sessionmaker() для получения сессии
            async with session.begin():
                try:
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
                except NoResultFound:
                    logger.info(f'No result found for subscription with ID {subscription_id}.')
                    raise RepositorySubscriptionNotFound(subscription_id)
                except Exception as e:
                    raise RepositoryException(
                        f'Error occurred while updating subscription with ID {subscription_id}: {e}')
