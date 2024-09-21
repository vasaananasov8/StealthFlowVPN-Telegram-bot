from logging import getLogger
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dependency_injector.wiring import inject, Provide

from src.bot.routers.fsm import UsePromo
from src.bot.routers.utils import send_error_message, handel_unexpected_exception
from src.bot.ui.inline_keyboard import callbacks
from src.bot.ui.inline_keyboard import keyboard
from src.bot.ui.scripts.scripts import Scripts
from src.container import AppContainer
from src.services.storage.infrastructure.interfaces.i_promo_manager import IPromoManager, PromoCheckValue
from src.services.vpn.i_vpn_manager import IVpnManager, ApplyPromoResultValues

logger = getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(lambda x: x.data == callbacks.GET_VPN)
@handel_unexpected_exception
@inject
async def get_vpn(
        callback: types.CallbackQuery | None = None,
) -> None:
    """Open menu to get vpn. Now 2 options: 'Pay for vpn', 'Use promo'"""
    kb = keyboard.get_vpm_meny()
    await callback.message.answer(text="stub", reply_markup=kb.as_markup())
    return


@router.callback_query(lambda x: x.data == callbacks.USER_PROMO)
async def use_promo(
        callback: types.CallbackQuery,
        state: FSMContext,
) -> None:
    """Start fsm to user promo"""
    await callback.message.answer(text="Введите промокод")
    await state.set_state(UsePromo.set_promo)
    return


@router.message(UsePromo.set_promo)
@inject
async def set_promo(
        msg: types.Message,
        state: FSMContext,
        promo_manager: IPromoManager = Provide[AppContainer.promo_manager],
        scripts_handler: Scripts = Provide[AppContainer.handler_scripts],
        vpn_manager: IVpnManager = Provide[AppContainer.vpn_manager]
) -> None:
    """Set promo to user"""
    promo_id = msg.text.strip()
    promo_check_result = await promo_manager.check_promo_is_valid(promo_id)
    match promo_check_result.result:
        case PromoCheckValue.INVALID_PROMO_CODE:
            await msg.answer(
                text="Неверный формат промокода",
                reply_markup=keyboard.cancel().as_markup()
            )
            return
        case PromoCheckValue.NO_PROMO:
            await msg.answer(
                text="Промокод не найден, попробуйте другой",
                reply_markup=keyboard.cancel().as_markup()
            )
            return
        case PromoCheckValue.PROMO_ALREADY_ACTIVE:
            await msg.answer(
                text="Промокод уже использован, попробуйте другой",
                reply_markup=keyboard.cancel().as_markup()
            )
            return
        case PromoCheckValue.VALID:
            promo = promo_check_result.promo
        case _:
            await send_error_message(msg, state)
            logger.error(f"Bad result after check promo: {promo_check_result}")
            return

    apply_promo_result = await vpn_manager.apply_promo(
        promo=promo,
        user_id=msg.from_user.id,
        promo_manager=promo_manager,
        username=msg.from_user.username
    )

    match apply_promo_result.result:
        case ApplyPromoResultValues.CREATE_NEW:
            script = scripts_handler.successful_new_connection(
                apply_promo_result.connection_link, apply_promo_result.new_until
            )
        case ApplyPromoResultValues.EXTEND_ACTIVE:
            script = scripts_handler.successful_extend_subscription(
                apply_promo_result.old_until,
                apply_promo_result.new_until
            )
        case ApplyPromoResultValues.EXTEND_NON_ACTIVE:
            script = scripts_handler.successful_new_connection(
                apply_promo_result.connection_link, until=apply_promo_result.new_until
            )
        case _:
            await send_error_message(msg, state)
            logger.error(f"Bad result after apply promo: {apply_promo_result}")
            return

    await msg.answer(
        text=script,
        reply_markup=InlineKeyboardBuilder()
            .button(text="Как подключить", callback_data=callbacks.CONNECTION_HELP)
            .as_markup()
    )
    await state.clear()
