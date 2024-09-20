from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.bot.ui.inline_keyboard import callbacks

def main_menu_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить VPN", callback_data=callbacks.GET_VPN)
    builder.button(text="Личный кабинет", callback_data=callbacks.GET_USER_STATS)
    builder.button(text="Поддержка", callback_data=callbacks.SUPPORT)
    return builder


def get_vpm_meny() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    # builder.button(text="Оплатить", callback_data=callbacks.PAY)
    builder.button(text="Ввести промокод", callback_data=callbacks.USER_PROMO)
    return builder
