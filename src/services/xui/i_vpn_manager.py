import uuid
from abc import ABC, abstractmethod

from src.config.config import Config
from src.services.xui.requests.request_handler import RequestHandler


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
    ) -> bool:
        """
        Create new client connection in 3x service
        :param user_email:
        :param connection_id:
        :param inbound_id:
        :param total_gb:
        :param duration_mouth:
        :return:
        """
        ...

    # @abstractmethod
    # def generate_client_qr(self) -> bytes:
    #     ...
