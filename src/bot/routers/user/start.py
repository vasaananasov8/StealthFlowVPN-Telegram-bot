from logging import getLogger
from aiogram import Router, types
from aiogram.filters import CommandStart
from dependency_injector.wiring import inject, Provide
from sqlalchemy.exc import IntegrityError

from src.bot.ui.inline_keyboard import callbacks
from src.bot.ui.inline_keyboard.keyboard import main_menu_kb
from src.bot.ui.scripts import Scripts
from src.container import AppContainer
from src.core.models.user import User
from src.services.storage.infrastructure.interfaces.i_user_storage_manager import IUserStorageManager

logger = getLogger(__name__)
router = Router(name=__name__)

@router.message(CommandStart())
@router.callback_query(lambda x: x == callbacks.MAIN_MENU)
# @handel_unexpected_exception
@inject
async def start(
        msg: types.Message,
        user_storage_manager: IUserStorageManager = Provide[AppContainer.user_storage_manager],
        handler_scripts: Scripts = Provide[AppContainer.handler_scripts]
) -> None:
    try:
        await user_storage_manager.create_user(
            User(
                id=msg.from_user.id,
                username=msg.from_user.username,
                first_name=msg.from_user.first_name,
                second_name=msg.from_user.last_name,
                language_code=msg.from_user.language_code,
                timezone=0  # TODO: need logic to get user tz
            )
        )
    except IntegrityError:
        ...
    finally:
        await msg.answer(
            text=handler_scripts.start_script,
            reply_markup=main_menu_kb().as_markup()
        )
        await msg.delete()

















