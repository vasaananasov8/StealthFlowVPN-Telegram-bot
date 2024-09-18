import json
import aiohttp
import ssl

from http.cookies import SimpleCookie
from json import JSONDecodeError
from aiohttp import ClientResponse

from src.config.config import Config
from src.services.xui.requests.exceptions import BadResponseException, LoginRecursionException
from src.services.xui.requests.i_request_handler import IRequestHandler, ResponseModel
from src.services.xui.requests.statuses import SUCCESS_200


class RequestHandler(IRequestHandler):
    session_id: str | None = None

    def __init__(self, config: Config):
        self.config = config
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    @staticmethod
    async def parce_response(r: ClientResponse) -> ResponseModel:
        """Parce ClientResponse obj to ResponseModel obj"""
        status = r.status
        details: str = await r.text()
        cookies: dict = dict(r.cookies)
        return ResponseModel(body=details, status=status, cookies=cookies)

    @staticmethod
    async def check_response(r: ClientResponse) -> bool:
        r = await r.text()
        try:
            json.loads(r)
        except JSONDecodeError:
            # raise BadResponseException(f"Expected json instead: {body=}") # TODO: add to logging
            return False
        else:
            return True

    @staticmethod
    async def check_login_response(r: ClientResponse) -> bool:
        r = await r.text()
        try:
            body = json.loads(r)
        except JSONDecodeError:
            return False
        return not (body.get("msg", "").strip() == "Invalid username or password or secret")

    @property
    def _cookies(self) -> SimpleCookie:
        cookies = SimpleCookie()
        cookies["3x-ui"] = self.session_id
        return cookies

    async def _login(self) -> None:
        """
        Make login request to api and save session_id to future interact with api in self.session_id
        :return: None
        :exception: BadResponseException if login was not success
        """
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{self.config.xui_host}/login?"
                        f"username={self.config.xui_login}&password={self.config.xui_password}",
                    ssl=self.ssl_context
            ) as r:
                if await self.check_login_response(r):
                    cookies = r.cookies
                    cookies = cookies["3x-ui"]
                    self.session_id = cookies.value
                else:
                    body = await r.text()
                    raise BadResponseException(f"Fail login: {body=}")

    async def get(self, url: str, _counter: int = 0) -> ResponseModel:
        if not self.session_id:
            await self._login()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=f"{self.config.xui_host}/{url}",
                    ssl=self.ssl_context,
                    cookies=self._cookies
            ) as r:

                if r.status != SUCCESS_200:
                    return await self.parce_response(r)

                if await self.check_response(r):
                    return await self.parce_response(r)
                elif _counter < 2:
                    await self._login()
                    _counter += 1
                    return await self.get(url, _counter)
                else:
                    raise LoginRecursionException("To many bad login requests")

    async def post(self, url: str, body: dict | None = None, _counter: int = 0) -> ResponseModel:
        if not self.session_id:
            await self._login()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"{self.config.xui_host}/{url}",
                    data=body,
                    ssl=self.ssl_context,
                    cookies=self._cookies
            ) as r:

                if r.status != SUCCESS_200:
                    return await self.parce_response(r)

                if await self.check_response(r):
                    return await self.parce_response(r)
                elif _counter < 2:
                    await self._login()
                    _counter += 1
                    return await self.post(url, body, _counter)
                else:
                    raise LoginRecursionException("To many bad login requests")
