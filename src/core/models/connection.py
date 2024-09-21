import uuid

from pydantic import BaseModel
from src.services.storage.schemas.connection import Connection as DbConnection

class Connection(BaseModel):
    id: uuid.UUID
    user_id: int

    def get_db_connection_model(self) -> DbConnection:
        return DbConnection(
            id=self.id,
            user_id=self.user_id
        )
