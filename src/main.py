import asyncio

from aiogram import Router, types
from aiogram.filters import Command

from src.container import AppContainer


async def main():

    container = AppContainer()
    container.wire(modules=[__name__])

    # Test tg router
    router = Router(name=__name__)

    @router.message(Command("statr"))
    async def create_account(
            message: types.Message,
    ) -> None:
        """"""
        await message.answer(text="hello")
        print(
            message.from_user
        )

    dp = container.bot_dispatcher()
    dp.include_router(router)
    await dp.start_polling(container.bot())


if __name__ == '__main__':
    asyncio.run(main())


























