import logging
from typing import Any

from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from src.services.storage.repository.exceptions import RepositoryConnectionCreationError, RepositoryException, \
    RepositoryUserNotFound
from src.services.storage.repository.interfaces.i_connection_repository import IPostgresConnectionRepository
from src.services.storage.schemas.connection import Connection
from src.services.storage.schemas.payment import Payment

logger = logging.getLogger(__name__)


class PostgresConnectionRepository(IPostgresConnectionRepository):

    async def get_all_user_connections(self, user_id: int) -> list[dict[str, Any]]:
        async with self.async_session() as session:
            try:
                query = select(Connection).filter(Connection.user_id == user_id)
                result = await session.execute(query)
                connections = result.scalars().all()

                if not connections:
                    logger.warning(f'No connections found for user with ID {user_id}')
                    raise RepositoryUserNotFound(user_id)

                connections_list = [
                    {
                        'id': connection.id,
                        'user_id': connection.user_id,
                    }
                    for connection in connections
                ]

                return connections_list
            except SQLAlchemyError as e:
                logger.error(f'Error occurred while fetching connections for user with ID {user_id}: {e}')
                raise RepositoryException(f'Error occurred while fetching connections for user with ID {user_id}: {e}')
            except Exception as e:
                logger.error(f'Unexpected error occurred while fetching connections for user with ID {user_id}: {e}')
                raise RepositoryException(
                    f'Unexpected error occurred while fetching connections for user with ID {user_id}')

    async def create_connection(self, connection: Connection) -> None:
        async with self.async_session() as session:
            try:
                async with session.begin():
                    session.add(connection)
            except SQLAlchemyError as e:
                logger.error(f'Error occurred while creating connection with ID {connection.id}: {e}')
                raise RepositoryConnectionCreationError(
                    f'Error occurred while creating connection with ID {connection.id}: {e}')
            except Exception as e:
                logger.error(f'Unexpected error occurred while creating connection with ID {connection.id}: {e}')
                raise RepositoryException(
                    f'Unexpected error occurred while creating connection with ID {connection.id}')
