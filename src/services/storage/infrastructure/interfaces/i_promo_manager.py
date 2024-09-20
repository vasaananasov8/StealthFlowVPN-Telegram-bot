import uuid
from abc import ABC, abstractmethod

from src.core.models.promo import Promo
from src.services.storage.repository.interfaces.i_promo_repository import IPromoRepository


class IPromoManager(ABC):
    def __init__(self, promo_repository: IPromoRepository) -> None:
        self.promo_repository = promo_repository

    @staticmethod
    def is_valid_uuid(string: str) -> bool:
        try:
            uuid_obj = uuid.UUID(string, version=4)
        except ValueError:
            return False
        return str(uuid_obj) == string

    @abstractmethod
    async def get_promo(self, _id: str) -> Promo:
        ...

    @abstractmethod
    async def create_promos(self, promo_nums: int) -> list[str]:
        ...