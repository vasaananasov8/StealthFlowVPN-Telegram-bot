import logging

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError
from sqlalchemy.future import select

from src.services.storage.repository.exceptions import (RepositoryUserNotFound, RepositoryException, \
    RepositoryUserCreationError, handle_db_exception
    RepositoryUserCreationError, RepositoryAlreadyExist)
from src.services.storage.repository.interfaces.i_user_repository import IPostgresUserRepository
from src.services.storage.schemas.user import User

logger = logging.getLogger(__name__)


class PostgresUserRepository(IPostgresUserRepository):
    @handle_db_exception(exception_mapping={'user': RepositoryUserNotFound})
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

    @handle_db_exception(exception_mapping={'user': RepositoryUserCreationError})
    async def create_user(self, user: User) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add(user)
