from abc import ABC, abstractmethod
from typing import Any

from src.services.storage.repository.interfaces.i_postrgres_init import IPostgresInit
from src.services.storage.schemas.connection import Connection


class IConnectionRepository(ABC):
    """Interface to interact with connectin database"""
    @abstractmethod
    async def get_all_user_connections(self, user_id: int) -> list[dict[str, Any]]:

        ...

    @abstractmethod
    async def create_connection(self, connection: Connection) -> None:
        ...


class IPostgresConnectionRepository(IPostgresInit, IConnectionRepository, ABC):
    """
    Interface to interact with postgres payment table
    """
