from abc import ABC, abstractmethod
from typing import Any

from src.services.storage.repository.interfaces.i_postrgres_init import IPostgresInit
from src.services.storage.schemas.user import User


class IUserRepository(ABC):
    """Interface to interact with users database"""

    @abstractmethod
    async def get_user(self, _id: int) -> dict[str, Any]:
        """
        Get user from db
        :param _id: telegram user id
        :return dict: user
        :raise: RepositoryUserNotFound, RepositoryException
        """
        ...

    @abstractmethod
    async def create_user(self, user: User) -> None:
        """
        Create user in database
        :param user: User
        :return None:
        :raise: RepositoryUserCreationError, RepositoryException
        """
        ...


class IPostgresUserRepository(IPostgresInit, IUserRepository, ABC):
    """
    Interface to interact with postgres users database
    """
