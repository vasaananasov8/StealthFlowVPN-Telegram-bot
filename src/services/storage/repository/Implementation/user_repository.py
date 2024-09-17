from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from src.services.storage.repository.interfaces.i_user_repository import IPostgresUserRepository
from src.services.storage.schemas.user import User


class PostgresUserRepository(IPostgresUserRepository):

    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine)

    async def get_user(self, _id: int) -> dict:
        async with self.session() as s:
            query = text(f"SELECT * FROM users WHERE id = {_id}")  # TODO: orm query + need fetch one
            res = await s.execute(query)
            res = res.mappings().all()
            return res[0] if len(res) == 1 else {}

    async def create_user(self, user: User) -> None:
        async with self.session() as s:
            s.add(user)
            await s.commit()
