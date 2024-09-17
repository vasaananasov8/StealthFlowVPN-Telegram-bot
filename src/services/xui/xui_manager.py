from abc import ABC, abstractmethod

from src.services.xui.requests.request_handler import RequestHandler


class IVpnManager(ABC):
    def __init__(self, request_handler: RequestHandler) -> None:
        self.rh = request_handler

    @abstractmethod
    def add_client(self) -> str:
        ...

    # @abstractmethod
    # def generate_client_qr(self) -> bytes:
    #     ...


class VpnManager(IVpnManager):
    def generate_client_key(self) -> str:
        pass

    def add_client(self) -> str:
        pass
