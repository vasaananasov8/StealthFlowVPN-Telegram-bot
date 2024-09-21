import logging
import uuid
from typing import Any

from sqlalchemy.future import select

from src.services.storage.repository.exceptions import RepositoryPromoNotFound, handle_db_exception
from src.services.storage.repository.interfaces.i_promo_repository import IPostgresPromoRepository
from src.services.storage.schemas.promo import Promo


class PostgresPromoRepository(IPostgresPromoRepository):
    @handle_db_exception(exception_mapping={'promo': RepositoryPromoNotFound})
    async def get_promo(self, _id: uuid.UUID) -> dict[str, Any]:
        async with self.async_session() as session:
            result = await session.execute(
                select(Promo).filter(Promo.id == _id)
            )
            promo = result.scalar_one()

            if promo:
                return {
                    'id': promo.id,
                    'is_active': promo.is_active,
                    'duration': promo.duration
                }

    @handle_db_exception(exception_mapping={'promo': RepositoryPromoNotFound})
    async def get_all_active_promo(self) -> list[dict[str, Any]]:
        async with self.async_session() as session:
            result = await session.execute(
                select(Promo).filter(Promo.is_active == True)
            )
            promos = result.scalars().all()

            if promos:
                return [
                    {
                        promo.id: {
                            'is_active': promo.is_active,
                            'duration': promo.duration
                        }
                    }
                    for promo in promos
                ]

    @handle_db_exception(exception_mapping={'promo': RepositoryPromoNotFound})
    async def create_promos(self, promos: list[Promo]) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add_all(promos)
