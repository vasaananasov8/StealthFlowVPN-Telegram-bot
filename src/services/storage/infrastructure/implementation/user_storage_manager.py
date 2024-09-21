from charset_normalizer.md import getLogger
from pydantic import ValidationError

from src.core.models.user import User
from src.services.storage.exception import StorageManagerValidationError
from src.services.storage.infrastructure.interfaces.i_user_storage_manager import IUserStorageManager
from src.services.storage.repository.exceptions import RepositoryException

logger = getLogger(__name__)


class UserStorageManager(IUserStorageManager):

    async def create_user(self, user: User) -> None:
        try:
            await self.user_repository.create_user(user.get_db_user_model())
        except RepositoryException:  # TODO: need more specific exception if user already exist
            ...

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repository.get_user(user_id)
        try:
            return User.model_validate(user)
        except ValidationError as err:
            err_text = f"ValidationError while try validate dict to User pydantic model. details: {err}"
            logger.error(err_text)
            raise StorageManagerValidationError(err_text)
