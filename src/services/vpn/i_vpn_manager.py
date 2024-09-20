import uuid
from abc import ABC, abstractmethod

from src.config.config import Config
from src.services.vpn.requests.request_handler import RequestHandler


class IVpnManager(ABC):
    def __init__(self, request_handler: RequestHandler, config: Config) -> None:
        self.request_handler = request_handler
        self.config = config

    @abstractmethod
    async def add_client(
            self,
            user_email: str,
            connection_id: uuid.UUID,
            inbound_id: int = 1,
            total_gb: int = 0,
            duration_mouth: int = 1
    ) -> None:
        """
        Create new client connection in 3x service
        :param user_email: some unic str to indelicate client connection
        :param connection_id: uuid of current connection
        :param inbound_id:
        :param total_gb: gb limit of connection
        :param duration_mouth:
        :raise: CreateVpnClientException if client not created
        """
        ...

    @abstractmethod
    async def add_client_with_connection_string(
            self,
            connection_id: uuid.UUID,
            user_email: str,
            inbound_id: int = 1,
            total_gb: int = 0,
            duration_mouth: int = 1
    ) -> str | None:
        ...
