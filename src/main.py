import asyncio
import logging

from src.container import AppContainer
from src.bot.routers.main_router import get_main_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    container = AppContainer()
    container.wire(packages=["src.bot"])

    dp = container.bot_dispatcher()
    dp.include_router(get_main_router())
    await dp.start_polling(container.bot())


if __name__ == '__main__':
    asyncio.run(main())
