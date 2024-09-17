from typing import Any

from sqlalchemy import text

from src.services.storage.repository.interfaces.i_connection_repository import IPostgresConnectionRepository
from src.services.storage.schemas.payment import Payment


class PostgresConnectionRepository(IPostgresConnectionRepository):

    async def get_all_user_connections(self, user_id: int) -> list[dict[str, Any]]:
        async with self.session() as s:
            query = text(f"SELECT * FROM connections WHERE user_id = {user_id}")  # TODO: orm query
            res = await s.execute(query)
            res = res.mappings().all()
            return res

    async def create_connection(self, payment: Payment) -> None:
        async with self.session() as s:
            s.add(payment)
            await s.commit()
