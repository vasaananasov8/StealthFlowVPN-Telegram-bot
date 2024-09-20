from aiogram.fsm.state import StatesGroup, State


#  Themes FSM
class UsePromo(StatesGroup):
    set_promo: State = State()
