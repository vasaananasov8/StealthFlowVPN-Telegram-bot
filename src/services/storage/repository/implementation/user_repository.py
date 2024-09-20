import logging

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.future import select

from src.services.storage.repository.exceptions import RepositoryUserNotFound, RepositoryException, \
    RepositoryUserCreationError
from src.services.storage.repository.interfaces.i_user_repository import IPostgresUserRepository
from src.services.storage.schemas.user import User

logger = logging.getLogger(__name__)


class PostgresUserRepository(IPostgresUserRepository):
    async def get_user(self, _id: int) -> dict:
        async with self.async_session() as session:
            try:
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
            except NoResultFound:
                logger.info(f'No result found for user with ID {_id}.')
                raise RepositoryUserNotFound(_id)
            except Exception as e:
                logger.error(f'Error occurred while fetching user with ID {_id}')
                raise RepositoryException(f'Error occurred while fetching user with ID {_id}')

    async def create_user(self, user: User) -> None:
        try:
            async with self.async_session() as session:
                async with session.begin():
                    session.add(user)
        except SQLAlchemyError as e:
            logger.info(f'Error occurred while creating user with ID {user.id}: {e}')
            raise RepositoryUserCreationError(f'Error occurred while creating user with ID {user.id}: {e}')
        except Exception as e:
            logger.error(f'Unexpected error occurred while creating user with ID {user.id}: {e}')
            raise RepositoryException(f'Unexpected error occurred while creating user with ID {user.id}')
