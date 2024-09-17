from aiogram import Bot

from src.config.config import Config


class TgBot(Bot):
    """Aiogram telegram bot"""
    def __init__(self, config: Config, *args, **kwargs) -> None:
        super().__init__(
            token=config.bot_token,
            *args, **kwargs
        )
