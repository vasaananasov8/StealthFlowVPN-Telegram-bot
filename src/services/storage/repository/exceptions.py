from logging import Logger
from typing import Callable, Any
from functools import wraps

from sqlalchemy.exc import NoResultFound, SQLAlchemyError


class RepositoryException(Exception):
    ...


class RepositoryNotFound(RepositoryException):
    ...


def async_method_arguments_logger(logger: Logger) -> Callable:
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
            logger.debug(f"Statr handler: {method.__name__} | With arguments: {args}, {kwargs}")
            try:
                result = await method(*args, **kwargs)
            except NoResultFound as err:
                logger.info(f"Error: {err}")
                raise RepositoryNotFound(err)
            except SQLAlchemyError as err:
                logger.info(f"Error: {err}")
                raise RepositoryException(err)
            except BaseException as err:
                logger.error(f"Error: {err}")
                raise err
            else:
                logger.debug(f"Finish handler: {method.__name__} | With result: {result}")
                return result

        return wrapper

    return decorator
