from datetime import datetime

from charset_normalizer.md import getLogger
from pydantic import ValidationError

from src.core.models.subscription import Subscription
from src.services.storage.exception import StorageManagerValidationError
from src.services.storage.infrastructure.interfaces.i_subscription_manager import ISubscriptionStorageManager
from src.services.storage.repository.exceptions import RepositorySubscriptionNotFound

logger = getLogger(__name__)

class SubscriptionStorageManager(ISubscriptionStorageManager):

    async def get_user_subscription(self, user_id: int) -> Subscription | None:
        try:
            subscription = await self.subscription_repository.get_user_subscription(user_id)
        except RepositorySubscriptionNotFound:
            return None

        try:
            return Subscription.model_validate(subscription) if subscription else None
        except ValidationError as err:
            err_text = f"ValidationError while try validate dict to Subscription pydantic model. details: {err}"
            logger.error(err_text)
            raise StorageManagerValidationError(err_text)

    async def create_subscription(self, subscription: Subscription) -> None:
        await self.subscription_repository.create_subscription(subscription.get_db_subscription_model())

    async def update_subscription(self, new_subscription: Subscription) -> None:
        ...

    async def extend_subscription(self, _id: int, new_until: datetime) -> bool:
        ...
