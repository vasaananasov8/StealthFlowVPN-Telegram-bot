import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import NamedTuple

from src.core.models.promo import Promo
from src.services.storage.infrastructure.exceptions import PromoInvalidId
from src.services.storage.repository.interfaces.i_promo_repository import IPromoRepository


class PromoCheckValue(Enum):
    VALID = 1
    INVALID_PROMO_CODE = 2
    NO_PROMO = 3
    PROMO_ALREADY_ACTIVE = 4


class PromoCheckResult(NamedTuple):
    result: PromoCheckValue
    promo: Promo | None = None


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

    @staticmethod
    def convert_str_to_uuid(value: str) -> uuid.UUID:
        try:
            return uuid.UUID(value, version=4)
        except ValueError:
            raise PromoInvalidId(f"Failed convert {value=} to uuid") # TODO add exception

    @abstractmethod
    async def get_promo(self, _id: str) -> Promo | None:
        ...

    @abstractmethod
    async def get_all_active_promos(self) -> list[Promo]:
        ...

    @abstractmethod
    async def create_promos(self, promo_nums: int, promo_month_duration: int) -> list[str]:
        ...

    @abstractmethod
    async def change_promo_activity(self, _id: str, new_value: bool) -> bool:
        pass

    @abstractmethod
    async def check_promo_is_valid(self, promo_id) -> PromoCheckResult:
        ...

    @abstractmethod
    async def delete_promo(self, promo_id: uuid.UUID) -> None:
        ...
