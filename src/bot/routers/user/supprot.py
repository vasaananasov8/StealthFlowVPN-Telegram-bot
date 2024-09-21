from logging import getLogger

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide
from pyexpat.errors import messages

from src.bot.routers.fsm import Support, SupportAnswerAppeal
from src.bot.ui.inline_keyboard import callbacks, keyboard
from src.bot.ui.scripts.i_scripts import IScripts
from src.config.config import Config
from src.container import AppContainer

logger = getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(lambda x: x.data == callbacks.SUPPORT)
@inject
async def support(
        callback: types.CallbackQuery,
        state: FSMContext,
        script_handler: IScripts = Provide[AppContainer.handler_scripts]
) -> None:
    """"""
    script_handler.set_language(callback.from_user.language_code)
    await callback.message.answer(
        text=script_handler.support(),
        reply_markup=keyboard.cancel().as_markup()
    )
    await state.set_state(Support.add_message)
    return


@router.message(Support.add_message)
@inject
async def support_register_appeal(
        msg: types.Message,
        state: FSMContext,
        script_handler: IScripts = Provide[AppContainer.handler_scripts],
        config: Config = Provide[AppContainer.app_config]
) -> None:
    """"""
    script_handler.set_language(lang_code=msg.from_user.language_code)
    user = msg.from_user

    if msg.photo is None:
        await msg.bot.send_message(
            chat_id=config.support_chanel_id,
            reply_markup=keyboard.answer_support_msg(msg.from_user.id).as_markup(),
            text=script_handler.support_problem(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                lang_code=user.language_code,
                text=msg.text,
            )
        )
    else:
        msg_photo_id = msg.photo[-1].file_id
        await msg.bot.send_photo(
            chat_id=config.support_chanel_id,
            reply_markup=keyboard.answer_support_msg(msg.from_user.id).as_markup(),
            photo=msg_photo_id,
            caption=script_handler.support_problem(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                lang_code=user.language_code,
                text=msg.caption,
            )
        )

    await msg.answer(
        text=script_handler.support_register_appeal(),
    )
    await state.clear()
    return


@router.callback_query(lambda x: x.data.startswith(callbacks.ANSWER_SUPPORT_MSG))
async def answer_appeal(
        callback: types.CallbackQuery,
        state: FSMContext
) -> None:
    user_id = callbacks.get_user_id_from_callback_data(callback.data)
    await state.set_state(SupportAnswerAppeal.add_message)
    await state.update_data(user_id=user_id)
    await callback.message.answer(text="Введите текст ответа", reply_markup=keyboard.cancel().as_markup())
    return


@router.message(SupportAnswerAppeal.add_message)
async def answer_appeal_send_message(
        msg: types.Message,
        state: FSMContext
) -> None:
    state_data = await state.get_data()
    user_id = state_data["user_id"]
    await msg.bot.send_message(
        chat_id=user_id,
        text=f"Ответ по вашему обращению:\n{msg.text}"
    )
    await msg.answer(
        text="Ответ по обращению успешно отправлен"
    )
    await state.clear()
    return
