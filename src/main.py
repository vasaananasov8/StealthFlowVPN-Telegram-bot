import asyncio
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command

from src.container import AppContainer
from src.services.storage.schemas.payment import Payment
from src.services.storage.schemas.subscription import Subscription
from src.services.storage.schemas.user import User


async def main():

    container = AppContainer()
    container.wire(modules=[__name__])

    # sub_repo = container.subscription_repository()
    # await sub_repo.create_subscription(
    #     Subscription(
    #     user_id=1,
    #     last_payment=1,
    #     sale=0,
    #     until=datetime.now(),
    #     active_links=1,
    #     is_active=True
    #     )
    # )

    # payment_repo = container.payment_repository()
    # await payment_repo.create_payment(
    #     Payment(
    #         user_id=1,
    #         amount=123.1,
    #         currency="rub",
    #         dt=datetime.now()
    #     )
    # )
    # await payment_repo.create_payment(
    #     Payment(
    #         user_id=1,
    #         amount=2500,
    #         currency="rub",
    #         dt=datetime.now()
    #     )
    # )

    # user_sub = await sub_repo.get_user_subscription(1)
    # user_payments = await payment_repo.get_all_user_payment(1)

    # print(f"{user_sub=}")
    # print(f"{user_payments=}")

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


























