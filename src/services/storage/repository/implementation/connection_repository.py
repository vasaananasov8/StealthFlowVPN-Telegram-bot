import logging
from typing import Any

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.services.storage.repository.exceptions import RepositoryConnectionCreationError, RepositoryException, \
    RepositoryUserNotFound, handle_db_exception, RepositoryConnectionNotFound
from src.services.storage.repository.interfaces.i_connection_repository import IPostgresConnectionRepository
from src.services.storage.schemas.connection import Connection

logger = logging.getLogger(__name__)


class PostgresConnectionRepository(IPostgresConnectionRepository):
    @handle_db_exception(exception_mapping={'connection': RepositoryUserNotFound})
    async def get_all_user_connections(self, user_id: int) -> list[dict[str, Any]]:
        async with self.async_session() as session:
            query = select(Connection).filter(Connection.user_id == user_id)
            result = await session.execute(query)
            connections = result.scalars().all()

            connections_list = [
                connection.id
                for connection in connections
            ]

            return connections_list

    @handle_db_exception(exception_mapping={'connection': RepositoryConnectionCreationError})
    async def create_connection(self, connection: Connection) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add(connection)

    @handle_db_exception(exception_mapping={'connection': RepositoryConnectionNotFound})
    async def delete_connection(self, connection_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                await session.execute(
                    delete(Connection).where(Connection.id == connection_id)
                )
