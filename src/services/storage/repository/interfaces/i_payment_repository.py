from abc import ABC, abstractmethod
from typing import Any

from src.services.storage.repository.interfaces.i_postrgres_init import IPostgresInit
from src.services.storage.schemas.payment import Payment


class IPaymentRepository(ABC):
    """Interface to interact with payment database"""
    @abstractmethod
    async def get_all_user_payment(self, user_id: int) -> list[dict[str, Any]]:
        """
        Get all user payment from db
        :param user_id:  user telegram id
        """
        ...

    @abstractmethod
    async def create_payment(self, payment: Payment) -> None:
        ...


class IPostgresPaymentRepository(IPostgresInit, IPaymentRepository, ABC):
    """
    Interface to interact with postgres payment table
    """
