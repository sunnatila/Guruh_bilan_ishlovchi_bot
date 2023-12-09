from aiogram.dispatcher.filters.state import State, StatesGroup


class GameStates(StatesGroup):
    start = State()
    stop = State()


