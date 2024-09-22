from logging import getLogger

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from alembic.ddl.mssql import mssql_add_column
from dependency_injector.wiring import Provide, inject
from pyexpat.errors import messages

from src.bot.routers.admin.fsm import AddPromo
from src.bot.ui import commands
from src.bot.ui.commands import ADD_PROMOS
from src.bot.ui.inline_keyboard import callbacks, keyboard
from src.config.config import Config
from src.container import AppContainer
from src.services.storage.infrastructure.interfaces.i_promo_manager import IPromoManager

logger = getLogger(__name__)
router = Router(name=__name__)


@router.message(Command(commands.ADD_PROMOS))
@inject
async def add_promo(
        msg: types.Message,
        state: FSMContext,
        config: Config = Provide[AppContainer.app_config]
) -> None:
    if msg.chat.id != config.support_chanel_id:
        return

    await state.set_state(AddPromo.choose_num)
    await msg.answer(
        text="Введите сколько промокодов надо сгенерировать",
        reply_markup=keyboard.cancel().as_markup()
    )
    return


@router.message(AddPromo.choose_num)
async def choose_promo_num(
        msg: types.Message,
        state: FSMContext
) -> None:
    try:
        num = int(msg.text)
    except ValueError:
        await msg.answer(
            text="Введите целое число",
            reply_markup=keyboard.cancel().as_markup()
        )
    else:
        await state.update_data(num=num)
        await msg.answer(
            text="Теперь введите продолжительность действия этих промокодов в месяцах",
            reply_markup=keyboard.cancel().as_markup()
        )
        await state.set_state(AddPromo.chose_duration)


@router.message(AddPromo.chose_duration)
async def chose_promo_duration(
        msg: types.message,
        state: FSMContext
) -> None:
    try:
        duration = int(msg.text)
    except ValueError:
        await msg.answer(
            text="Введите целое число",
            reply_markup=keyboard.cancel().as_markup()
        )
    else:
        kb = keyboard.accept_kb().attach(keyboard.cancel())
        user_data = await state.get_data()
        await state.update_data(duration=duration)
        await msg.answer(
            text=f"Создать {user_data.get("num", "err")} промокодов с продолжительностью {duration} месяцев?",
            reply_markup=kb.as_markup()
        )
        await state.set_state(AddPromo.accept)


@router.callback_query(AddPromo.accept, lambda x: x.data == callbacks.ACCEPT)
@inject
async def accept(
        callback: types.CallbackQuery,
        state: FSMContext,
        promo_manager: IPromoManager = Provide[AppContainer.promo_manager]
) -> None:
    user_data = await state.get_data()
    num = user_data["num"]
    duration = user_data["duration"]

    promos = await promo_manager.create_promos(num, duration)

    await callback.message.answer(
        text="\n".join(promos)
    )
