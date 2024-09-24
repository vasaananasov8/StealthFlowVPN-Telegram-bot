import logging
import uuid
from typing import Any

from sqlalchemy import delete
from sqlalchemy.future import select

from src.services.storage.repository.exceptions import async_method_arguments_logger
from src.services.storage.repository.interfaces.i_promo_repository import IPostgresPromoRepository
from src.services.storage.schemas.promo import Promo

logger = logging.getLogger(__name__)


class PostgresPromoRepository(IPostgresPromoRepository):
    @async_method_arguments_logger(logger)
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

    @async_method_arguments_logger(logger)
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

    @async_method_arguments_logger(logger)
    async def create_promos(self, promos: list[Promo]) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add_all(promos)

        ...

    async def change_promo_activity(self, _id: str, new_value: bool) -> None:
        ...


    @async_method_arguments_logger(logger)
    async def delete_promo(self, _id: str) -> None:
        async with self.async_session() as session:
            async with session.begin():
                await session.execute(
                    delete(Promo).where(Promo.id == _id)
                )

