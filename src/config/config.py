import os
from typing import Any, Final

import dotenv

from src.config.exceptions import EnvDependNotFound


class Config:
    def __init__(self):
        dotenv.load_dotenv()

        # Telegram
        self.BOT_TOKEN: Final[str] = self.get_env_var("BOT_TOKEN")

        # Database
        self.DB_HOST: Final[str] = self.get_env_var("DB_HOST")
        self.DB_PORT: Final[int] = self.get_env_var("DB_PORT")
        self.DB_USER: Final[str] = self.get_env_var("DB_USER")
        self.DB_PASSWORD: Final[str] = self.get_env_var("DB_PASSWORD")
        self.DB_NAME: Final[str] = self.get_env_var("DB_NAME")

        # Xui service
        self.XUI_LOGIN: Final[str] = self.get_env_var("XUI_LOGIN")
        self.XUI_PASSWORD: Final[str] = self.get_env_var("XUI_PASSWORD")
        self.XUI_HOST: Final[str] = self.get_env_var("XUI_HOST")
        self.XUI_PORT: Final[str] = self.get_env_var("XUI_PORT")
        self.XUI_SECRET: Final[str] = self.get_env_var("XUI_SECRET")

    @staticmethod
    def get_env_var(var_name: str, default_value: Any = None) -> Any:
        value: str | None = os.getenv(var_name)
        if value is None:
            raise EnvDependNotFound(f"Env var: {var_name} is None")
        else:
            return value

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def bot_token(self) -> str:
        return self.BOT_TOKEN

    @property
    def xui_login(self) -> str:
        return self.XUI_LOGIN

    @property
    def xui_password(self) -> str:
        return self.XUI_PASSWORD

    @property
    def xui_host(self) -> str:
        return f"https://{self.XUI_HOST}:{self.XUI_PORT}/{self.XUI_SECRET}"
