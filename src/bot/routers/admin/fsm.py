from aiogram.fsm.state import StatesGroup, State


class AddPromo(StatesGroup):
    choose_num: State = State()
    chose_duration: State = State()
    accept: State = State()
