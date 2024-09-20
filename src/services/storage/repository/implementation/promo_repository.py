import uuid
from typing import Any

from src.services.storage.repository.interfaces.i_promo_repository import IPostgresPromoRepository
from src.services.storage.schemas.promo import Promo


class PostgresPromoRepository(IPostgresPromoRepository):
    async def get_promo(self, _id: uuid.UUID) -> dict[str, Any]:
        ...

    async def get_all_active_promo(self) -> list[dict[str, Any]]:
        ...

    async def create(self, promo: Promo) -> None:
        ...
