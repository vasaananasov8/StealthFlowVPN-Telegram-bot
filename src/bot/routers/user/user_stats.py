from logging import getLogger

from aiogram import Router, types
from dependency_injector.wiring import inject, Provide

from src.bot.ui.inline_keyboard import callbacks
from src.bot.ui.inline_keyboard import keyboard
from src.bot.ui.scripts.i_scripts import IScripts
from src.container import AppContainer
from src.services.storage.infrastructure.interfaces.i_connection_manager import IConnectionManager
from src.services.storage.infrastructure.interfaces.i_subscription_manager import ISubscriptionStorageManager

logger = getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(lambda x: x.data == callbacks.GET_USER_STATS)
@inject
async def user_stats(
        callback: types.CallbackQuery,
        subscription_manager: ISubscriptionStorageManager = Provide[AppContainer.subscription_storage_manager],
        script_manager: IScripts = Provide[AppContainer.handler_scripts]
) -> None:
    user_sub = await subscription_manager.get_user_subscription(callback.from_user.id)
    script_manager.set_language(callback.from_user.language_code)
    if (user_sub is None) or (not user_sub.is_active):
        await callback.message.answer(
            text=script_manager.stats_has_not_active_subscription(),
            reply_markup=keyboard.get_vpm_meny().as_markup()
        )
    else:
        await callback.message.answer(
            text=script_manager.stats(user_sub),
            reply_markup=keyboard.stats_has_not_active_subscription_kb().as_markup()
        )
    return


@router.callback_query(lambda x: x.data == callbacks.CHECK_ACTIVE_CONNECTION_LINKS)
@inject
async def user_stats_check_active_links(
        callback: types.CallbackQuery,
        connection_manager: IConnectionManager = Provide[AppContainer.connection_manager],
        script_manager: IScripts = Provide[AppContainer.handler_scripts]
) -> None:
    """"""
    user_id = callback.from_user.id
    user_links = await connection_manager.get_all_user_active_connection_links(user_id)
    script_manager.set_language(callback.from_user.language_code)
    await callback.message.answer(
        text=script_manager.stats_active_connection_links(user_links)
    )
