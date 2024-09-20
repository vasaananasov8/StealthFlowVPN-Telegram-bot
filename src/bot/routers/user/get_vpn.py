import uuid
from logging import getLogger
from aiogram import Router, types
from aiogram.filters import Command
from dependency_injector.wiring import inject, Provide
from win32ctypes.pywin32.pywintypes import datetime

from src.bot.ui import commands
from src.bot.ui.inline_keyboard import callbacks
from src.bot.ui.inline_keyboard.keyboard import get_vpm_meny
from src.bot.ui.scripts import Scripts
from src.container import AppContainer
from src.core.models.subscription import Subscription
from src.services.storage.infrastructure.interfaces.i_subscription_manager import ISubscriptionStorageManager
from src.services.storage.infrastructure.interfaces.i_user_storage_manager import IUserStorageManager
from src.services.vpn.i_vpn_manager import IVpnManager

logger = getLogger(__name__)
router = Router(name=__name__)


@router.message(Command(commands.GET_VPN))
@router.callback_query(lambda x: x == callbacks.GET_VPN)
# @handel_unexpected_exception
@inject
async def get_vpn(
        msg: types.Message | None = None,
        callback: types.CallbackQuery | None = None,
        subscription_storage_manager: ISubscriptionStorageManager = Provide[AppContainer.subscription_storage_manager],
        vpn_manager: IVpnManager = Provide[AppContainer.vpn_handler],
        scripts_handler: Scripts = Provide[AppContainer.handler_scripts]
) -> None:
    kb = get_vpm_meny()
    if msg is not None:
        await msg.answer(text="stub", reply_markup=kb.as_markup())
    else:
        await callback.message.answer(text="stub", reply_markup=kb.as_markup())

@router.callback_query(lambda x: x == callbacks.USER_PROMO)
@inject
async def user_promo(
        callback: types.CallbackQuery,
) -> None:
    ...
    # TODO: Слой бизнес логики для впн

    # user_id = msg.from_user.id if msg is not None else callback.from_user.id
    # username = msg.from_user.username if msg is not None else callback.from_user.username


    # user_subscription = await subscription_storage_manager.get_user_subscription(user_id)
    # if not user_subscription:
    #     user_subscription = Subscription(
    #         id=None,
    #         user_id=user_id,
    #         last_payment=None,
    #         sale=100,  # TODO
    #         until=datetime.now(),
    #         active_links=0,
    #         is_active=False
    #     )
    #     await subscription_storage_manager.create_subscription(user_subscription)
    # else:
    #     # TODO: logic for new subscription
    #     ...
    #
    # # TODO: Payment, calculate user sale etc
    #
    # connection_link = await vpn_manager.add_client_with_connection_string(
    #     user_email=f"{username}_{user_id}_{user_subscription.active_links + 1}",
    #     connection_id=uuid.uuid4()
    # )
    #
    # if connection_link is not None:
    #     script = scripts_handler.connection_link(connection_link)
    # else:
    #     raise Exception
    #
    # if msg is not None:
    #     await msg.answer(
    #         text=script
    #     )
    #     await msg.delete()
    # else:
    #     await callback.answer(
    #         text=script
    #     )
