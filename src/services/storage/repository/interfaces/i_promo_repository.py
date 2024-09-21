import uuid
from abc import ABC, abstractmethod
from typing import Any

from src.services.storage.repository.interfaces.i_postrgres_init import IPostgresInit
from src.services.storage.schemas.promo import Promo


class IPromoRepository(ABC):
    @abstractmethod
    async def get_promo(self, _id: uuid.UUID) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_all_active_promo(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def create_promos(self, promo: Promo) -> None:
        ...

    @abstractmethod
    async def change_promo_activity(self, _id: str, new_value: bool) -> None:
        ...

    @abstractmethod
    async def delete_promo(self, _id: str) -> None:
        ...

class IPostgresPromoRepository(IPostgresInit, IPromoRepository, ABC):
    """
    Interface to interact with postgres promos table
    """