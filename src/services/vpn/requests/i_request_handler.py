from abc import ABC, abstractmethod
from http.cookies import SimpleCookie

from pydantic import BaseModel


class ResponseModel(BaseModel):
    body: str
    status: int
    cookies: dict


class IRequestHandler(ABC):

    @abstractmethod
    async def get(self, url: str) -> ResponseModel:
        """GET request"""
        ...

    @abstractmethod
    async def post(self, url: str, body: dict) -> ResponseModel:
        """POST request"""
        ...
