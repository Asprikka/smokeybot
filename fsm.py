from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    vapes_str = State()
    order = State()
