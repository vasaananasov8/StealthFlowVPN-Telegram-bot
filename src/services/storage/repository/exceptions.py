import logging
import uuid
from functools import wraps

from sqlalchemy.exc import NoResultFound, SQLAlchemyError


class RepositoryException(Exception):
    ...


class RepositoryUserNotFound(RepositoryException):
    """An exception that occurs when the user is not found."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f'User with ID {self.user_id} not found.')


class RepositoryUserCreationError(RepositoryException):
    """Exception for errors when creating a user"""
    ...


class RepositorySubscriptionCreationError(RepositoryException):
    """Exception for errors when creating a subscription"""
    ...


class RepositorySubscriptionNotFound(RepositoryException):
    """An exception that occurs when a subscription is not found."""

    def __init__(self, subscription_id: int):
        self.subscription_id = subscription_id
        super().__init__(f'Subscription with ID {self.subscription_id} not found.')


class RepositoryConnectionCreationError(RepositoryException):
    """Exception for errors when creating a connection"""
    ...


class RepositoryConnectionNotFound(RepositoryException):
    """An exception that occurs when the connection is not found."""

    def __init__(self, connection_id: int):
        self.connection_id = connection_id
        super().__init__(f'Connection with ID {self.connection_id} not found.')


class RepositoryPromoCreationError(RepositoryException):
    """Exception for errors when creating a promo"""
    ...


class RepositoryPromoNotFound(RepositoryException):
    """An exception that occurs when the promo is not found."""

    def __init__(self, promo_id: uuid.UUID):
        self.promo_id = promo_id
        super().__init__(f'Promo with ID {self.promo_id} not found.')


logger = logging.getLogger(__name__)


def handle_db_exception(exception_mapping):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except NoResultFound:
                exception_key = func.__name__.split('_')[-1]
                custom_exception = exception_mapping.get(exception_key, RepositoryException)

                entity_id = kwargs.get('_id') or kwargs.get('user_id') or kwargs.get('subscription_id') or args[1]

                logger.info(f'No result found for {exception_key} with ID: {entity_id}.')
                raise custom_exception(entity_id)
            except SQLAlchemyError as e:
                logger.error(f'SQLAlchemy error in {func.__name__}: {e}')
                if 'create' in func.__name__:
                    custom_exception = exception_mapping.get('create', RepositoryException)
                    entity = kwargs.get('user') or kwargs.get('subscription') or args[1]
                    raise custom_exception(f'Error occurred while creating entity with ID {entity.id}: {e}')
                elif 'update' in func.__name__:
                    custom_exception = exception_mapping.get('update', RepositoryException)
                    entity_id = kwargs.get('subscription_id') or kwargs.get('user_id') or args[1]
                    raise custom_exception(f'Error occurred while updating entity with ID {entity_id}: {e}')
                else:
                    raise RepositoryException(f'SQLAlchemy error in {func.__name__}: {e}')
        return wrapper
    return decorator
