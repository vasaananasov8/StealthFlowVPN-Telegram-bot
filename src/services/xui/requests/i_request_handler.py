from abc import ABC, abstractmethod


from pydantic import BaseModel


class ResponseModel(BaseModel):
    body: str
    status: int


class IRequestHandler(ABC):

    @abstractmethod
    async def get(self, url: str) -> ResponseModel:
        """GET request"""
        ...

    @abstractmethod
    async def post(self, url: str, body: dict) -> ResponseModel:
        """POST request"""
        ...

    @abstractmethod
    async def patch(self, url: str, body: dict) -> ResponseModel:
        """PATCH request"""
        ...

    @abstractmethod
    async def delete(self, url: str, body: dict) -> ResponseModel:
        """DELETE request"""
        ...
