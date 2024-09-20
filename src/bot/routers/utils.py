import functools
from typing import Callable, Any

from aiogram import types
from aiogram.fsm.context import FSMContext


async def send_error_message(
        message: types.Message | types.CallbackQuery,
        state: FSMContext | None = None,
        text: str = "Что-то пошло не так, попробуйте позже :("
) -> types.Message:
    """
    Send error message to user. Stop fsmContext if it was
    :param message: aiogram user message or callback to reply
    :param state: Current state of Fsm
    :param text: Error message text
    :return:
    """

    if state is not None:
        await state.clear()

    if isinstance(message, types.Message):
        message_out = await message.answer(text)
    else:
        message_out = await message.bot.send_message(
            chat_id=message.from_user.id,
            text=text
        )

    return message_out


# TODO: Need loging
def handel_unexpected_exception(
        method: Callable,
        err_text: str = "Что-то пошло не так, попробуйте позже :("
) -> Callable:
    """Handle unexpected exception in aiogram router in callback or message handlers"""

    @functools.wraps(method)
    async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        try:
            return await method(*args, **kwargs)
        except Exception as e:
            for i in args:
                if isinstance(i, types.CallbackQuery):
                    await i.bot.send_message(
                        text=err_text,
                        chat_id=i.from_user.id
                    )
                    await i.message.delete()
                    return wrapper
                if isinstance(i, types.Message):
                    await i.answer(text=err_text)
                    await i.message.delete()
                    return wrapper

    return wrapper