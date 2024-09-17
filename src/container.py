from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dependency_injector import containers, providers

from src.bot.bot import TgBot
from src.config.config import Config
from src.services.storage.repository.Implementation.payment_repository import PostgresPaymentRepository
from src.services.storage.repository.Implementation.subscription_repository import PostgresSubscriptionRepository
from src.services.storage.repository.Implementation.user_repository import PostgresUserRepository
from src.services.storage.repository.engine import get_engine


class AppContainer(containers.DeclarativeContainer):
    app_config = providers.Singleton(Config)

    bot = providers.Singleton(
        TgBot,
        config=app_config,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    bot_dispatcher = providers.Singleton(Dispatcher)

    # engine to repositories
    engine = providers.Singleton(
        get_engine,
        app_config
    )

    user_repository = providers.Singleton(
        PostgresUserRepository,
        engine=engine
    )

    payment_repository = providers.Singleton(
        PostgresPaymentRepository,
        engine=engine
    )

    subscription_repository = providers.Singleton(
        PostgresSubscriptionRepository,
        engine=engine
    )

















