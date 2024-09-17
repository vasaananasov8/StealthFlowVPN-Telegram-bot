import os
from typing import Any, Final

import dotenv

from src.config.exceptions import EnvDependNotFound


class Config:
    def __init__(self):
        dotenv.load_dotenv()
        self.BOT_TOKEN: Final[str] = self.get_env_var("BOT_TOKEN")
        self.DB_HOST: Final[str] = self.get_env_var("DB_HOST")
        self.DB_PORT: Final[int] = self.get_env_var("DB_PORT")
        self.DB_USER: Final[str] = self.get_env_var("DB_USER")
        self.DB_PASSWORD: Final[str] = self.get_env_var("DB_PASSWORD")
        self.DB_NAME: Final[str] = self.get_env_var("DB_NAME")

    @staticmethod
    def get_env_var(var_name: str, default_value: Any = None) -> Any:
        value: str | None = os.getenv(var_name)
        if value is None:
            raise EnvDependNotFound(f"Env var: {var_name} is None")
        else:
            return value

    @property
    def bot_token(self) -> str:
        return self.BOT_TOKEN

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
