from abc import ABC, abstractmethod
from typing import Any

from src.services.storage.repository.interfaces.i_postrgres_init import IPostgresInit
from src.services.storage.schemas.subscription import Subscription


class ISubscriptionRepository(ABC):
    """Interface to interact with user subscriptions database"""
    @abstractmethod
    async def get_user_subscription(self, user_id: int) -> dict[str, Any]:
        """
        Get user subscription from db
        :param:  user telegram id
        :return: dict
        :raise: RepositorySubscriptionNotFound, RepositoryException
        """
        ...

    @abstractmethod
    async def create_subscription(self, subscription: Subscription) -> None:
        """
        Create subscription in db
        :param: Subscription
        :return: None
        :raise: RepositorySubscriptionCreationError, RepositoryException
        """
        ...


class IPostgresSubscriptionRepository(IPostgresInit, ISubscriptionRepository, ABC):
    """
    Interface to interact with postgres payment table
    """
