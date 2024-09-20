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
    async def create(self, promo: Promo) -> None:
        ...


class IPostgresPromoRepository(IPostgresInit, IPromoRepository, ABC):
    """
    Interface to interact with postgres promos table
    """