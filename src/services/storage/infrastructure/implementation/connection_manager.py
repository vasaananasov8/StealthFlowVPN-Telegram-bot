from logging import getLogger
from typing import List

from pydantic import TypeAdapter, ValidationError

from src.core.models.connection import Connection
from src.services.storage.infrastructure.exceptions import DbDataValidationError
from src.services.storage.infrastructure.interfaces.i_connection_manager import IConnectionManager

logger = getLogger(__name__)


class ConnectionManager(IConnectionManager):
    async def get_all_user_connections(self, user_id: int) -> list[Connection]:
        connections = await self.connection_repository.get_all_user_connections(user_id)
        ta = TypeAdapter(List[Connection])
        try:
            return ta.validate_python(connections)
        except ValidationError as err:
            err_text = f"Error while try validate list of connections: {err}"
            logger.error(err_text)
            raise DbDataValidationError(err_text)

    async def add_new_connection(self, connection: Connection) -> None:
        await self.connection_repository.create_connection(
            connection.get_db_connection_model()
        )
        return

    async def get_all_user_active_connection_links(self, user_id: int) -> list[str] | None:
        pass
