import uuid

from logging import Logger
from functools import wraps
from typing import Callable, Any
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


def async_method_arguments_logger(logger: Logger) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            logger.info(f"Statr handler: {method.__name__} | With arguments: {args}, {kwargs}")
            result = await method(*args, **kwargs)
            logger.info(f"Finish handler: {method.__name__} | With result: {result}")
            return result

        return wrapper

    return decorator
