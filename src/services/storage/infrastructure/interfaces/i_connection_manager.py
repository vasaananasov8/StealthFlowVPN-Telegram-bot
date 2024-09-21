from abc import ABC, abstractmethod

from src.core.models.connection import Connection
from src.services.storage.repository.interfaces.i_connection_repository import IConnectionRepository


class IConnectionManager(ABC):
    def __init__(self, connection_repository: IConnectionRepository):
        self.connection_repository = connection_repository

    @abstractmethod
    async def get_all_user_connections(self, user_id: int) -> list[Connection]:
        ...

    @abstractmethod
    async def add_new_connection(self, connection: Connection) -> None:
        ...

    @abstractmethod
    async def get_all_user_active_connection_links(self, user_id: int) -> list[str] | None:
        ...
