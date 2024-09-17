from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from src.config.config import Config


def get_engine(config: Config) -> AsyncEngine:
    """Create async engine for database"""
    return create_async_engine(
        url=config.db_url,
        echo=True
    )
