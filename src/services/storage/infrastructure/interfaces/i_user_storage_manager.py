from abc import ABC, abstractmethod

from src.core.models.user import User
from src.services.storage.repository.interfaces.i_user_repository import IUserRepository


class IUserStorageManager(ABC):
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    @abstractmethod
    async def create_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> User:
        ...