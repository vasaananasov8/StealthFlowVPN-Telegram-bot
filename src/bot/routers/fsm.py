from aiogram.fsm.state import StatesGroup, State


class UsePromo(StatesGroup):
    set_promo: State = State()

class Support(StatesGroup):
    add_message: State = State()

class SupportAnswerAppeal(StatesGroup):
    add_message: State = State()
