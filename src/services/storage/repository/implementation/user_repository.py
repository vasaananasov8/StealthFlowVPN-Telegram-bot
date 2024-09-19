from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.services.storage.repository.interfaces.i_user_repository import IPostgresUserRepository
from src.services.storage.schemas.user import User


class PostgresUserRepository(IPostgresUserRepository):

    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine)

    async def get_user(self, _id: int) -> dict:
        async with self.async_session() as session:
            try:
                result = await session.execute(
                    select(User).filter(User.id == _id)
                )
                user = result.scalar_one_or_none()

                if user:
                    return {
                        'id': user.id,
                        'username': user.username,
                        'first_name': user.first_name,
                        'second_name': user.second_name,
                        'language_code': user.language_code,
                        'timezone': user.timezone
                    }
                else:
                    return {}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {}

    async def create_user(self, user: User) -> None:
        try:
            async with self.async_session() as session:
                async with session.begin():
                    session.add(user)
        except SQLAlchemyError as e:
            print(f'Error occurred: {e}')
