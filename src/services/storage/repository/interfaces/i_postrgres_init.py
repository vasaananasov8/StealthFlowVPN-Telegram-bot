from abc import ABC

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine


class IPostgresInit(ABC):
    def __init__(self, engine: AsyncEngine) -> None:
        self.session = async_sessionmaker(engine)
