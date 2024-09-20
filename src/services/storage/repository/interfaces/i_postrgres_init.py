from abc import ABC

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine


class IPostgresInit(ABC):
    def __init__(self, engine: AsyncEngine) -> None:
        self.async_session = async_sessionmaker(engine)
