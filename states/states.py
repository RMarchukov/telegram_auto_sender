from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    password = State()
    date = State()
    message_text = State()
    agreement = State()
