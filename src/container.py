from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dependency_injector import containers, providers

from src.bot.bot import TgBot
from src.config.config import Config
from src.services.storage.repository.implementation.connection_repository import PostgresConnectionRepository
from src.services.storage.repository.implementation.payment_repository import PostgresPaymentRepository
from src.services.storage.repository.implementation.subscription_repository import PostgresSubscriptionRepository
from src.services.storage.repository.implementation.user_repository import PostgresUserRepository
from src.services.storage.repository.engine import get_engine
from src.services.xui.requests.request_handler import RequestHandler
from src.services.xui.xui_manager import VpnManager


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

    connection_repository = providers.Singleton(
        PostgresConnectionRepository,
        engine=engine
    )

    # Handler to make api requests
    request_handler = providers.Singleton(
        RequestHandler,
        config=app_config
    )

    # Handler to interact with xui service
    vpn_handler = providers.Singleton(
        VpnManager,
        request_handler=request_handler
    )
