import uuid
from typing import Any

from src.services.storage.repository.interfaces.i_promo_repository import IPostgresPromoRepository
from src.services.storage.schemas.promo import Promo


class PostgresPromoRepository(IPostgresPromoRepository):
    async def get_promo(self, _id: uuid.UUID) -> dict[str, Any]:
        ...

    async def get_all_active_promo(self) -> list[dict[str, Any]]:
        ...

    async def create_promos(self, promos: list[Promo]) -> None:
        ...

    async def change_promo_activity(self, _id: str, new_value: bool) -> None:
        ...
