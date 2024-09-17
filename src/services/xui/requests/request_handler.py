from src.services.xui.requests.i_request_handler import IRequestHandler, ResponseModel


class RequestHandler(IRequestHandler):
    session_id: str

    async def login(self) -> ResponseModel:
        pass

    async def get(self, url: str) -> ResponseModel:
        pass

    async def post(self, url: str, body: dict) -> ResponseModel:
        pass

    async def patch(self, url: str, body: dict) -> ResponseModel:
        pass

    async def delete(self, url: str, body: dict) -> ResponseModel:
        pass