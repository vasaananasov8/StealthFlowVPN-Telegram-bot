from abc import ABC, abstractmethod
from datetime import datetime

from src.core.models.subscription import Subscription
from src.services.storage.repository.interfaces.i_subscription_repository import ISubscriptionRepository


class ISubscriptionStorageManager(ABC):
    def __init__(self, subscription_repository: ISubscriptionRepository) -> None:
        self.subscription_repository = subscription_repository

    @abstractmethod
    async def get_user_subscription(self, user_id: int) -> Subscription | None:
        ...

    @abstractmethod
    async def create_subscription(self, subscription: Subscription) -> None:
        ...

    @abstractmethod
    async def update_subscription(self, new_subscription: Subscription) -> None:
        ...

    @abstractmethod
    async def extend_subscription(self, _id: int, new_until: datetime) -> bool:
        ...