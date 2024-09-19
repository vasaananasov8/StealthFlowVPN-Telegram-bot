import os
from typing import Any, Final

import dotenv

from src.config.exceptions import EnvDependNotFound


class Config:
    def __init__(self):
        dotenv.load_dotenv()

        # Telegram
        self._BOT_TOKEN: Final[str] = self.get_env_var("BOT_TOKEN")

        # Database
        self._DB_HOST: Final[str] = self.get_env_var("DB_HOST")
        self._DB_PORT: Final[int] = self.get_env_var("DB_PORT")
        self._DB_USER: Final[str] = self.get_env_var("DB_USER")
        self._DB_PASSWORD: Final[str] = self.get_env_var("DB_PASSWORD")
        self._DB_NAME: Final[str] = self.get_env_var("DB_NAME")

        # Vpn service
        self._VPN_LOGIN: Final[str] = self.get_env_var("VPN_LOGIN")
        self._VPN_PASSWORD: Final[str] = self.get_env_var("VPN_PASSWORD")
        self._VPN_HOST: Final[str] = self.get_env_var("VPN_HOST")
        self._VPN_PORT: Final[str] = self.get_env_var("VPN_PORT")
        self._VPN_SECRET: Final[str] = self.get_env_var("VPN_SECRET")
        self._VPN_PBK: Final[str] = self.get_env_var("VPN_PBK")
        self._VPN_SID: Final[str] = self.get_env_var("VPN_SID")

    @staticmethod
    def get_env_var(var_name: str, default_value: Any = None) -> Any:
        value: str | None = os.getenv(var_name)
        if value is None:
            raise EnvDependNotFound(f"Env var: {var_name} is None")
        else:
            return value

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self._DB_USER}:{self._DB_PASSWORD}@{self._DB_HOST}:{self._DB_PORT}/{self._DB_NAME}"

    @property
    def bot_token(self) -> str:
        return self._BOT_TOKEN

    @property
    def vpn_login(self) -> str:
        return self._VPN_LOGIN

    @property
    def vpn_password(self) -> str:
        return self._VPN_PASSWORD

    @property
    def vpn_host_with_secret_str(self) -> str:
        return f"https://{self._VPN_HOST}:{self._VPN_PORT}/{self._VPN_SECRET}"

    @property
    def vpn_host(self) -> str:
        return self._VPN_HOST

    @property
    def vpn_pbk(self) -> str:
        return self._VPN_PBK

    @property
    def vpn_sid(self) -> str:
        return self._VPN_SID
