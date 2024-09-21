import logging

from sqlalchemy.future import select

from src.services.storage.repository.exceptions import async_method_arguments_logger
from src.services.storage.repository.interfaces.i_user_repository import IPostgresUserRepository
from src.services.storage.schemas.user import User

logger = logging.getLogger(__name__)


class PostgresUserRepository(IPostgresUserRepository):
    @async_method_arguments_logger(logger)
    async def get_user(self, _id: int) -> dict:
        async with self.async_session() as session:
            result = await session.execute(
                select(User).filter(User.id == _id)
            )
            user = result.scalar_one()

            if user:
                return {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'second_name': user.second_name,
                    'language_code': user.language_code,
                    'timezone': user.timezone
                }

    @async_method_arguments_logger(logger)
    async def create_user(self, user: User) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add(user)
