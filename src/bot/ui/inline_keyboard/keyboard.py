from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.bot.ui.inline_keyboard import callbacks
from src.bot.ui.inline_keyboard.callbacks import answer_support_msg_callback


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

def cancel() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Отмена", callback_data=callbacks.CANCEL)
    return builder

def stats_has_not_active_subscription_kb() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Продлить подписку", callback_data=callbacks.GET_VPN)
    builder.button(text="Посмотреть ключи подключений", callback_data=callbacks.CHECK_ACTIVE_CONNECTION_LINKS)
    return builder

def answer_support_msg(user_id: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить по обращению", callback_data=answer_support_msg_callback(user_id))
    return builder
