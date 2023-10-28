from aiogram.dispatcher.filters.state import State, StatesGroup

class GetUserSettings(StatesGroup):
    get_country = State()
    get_age = State()
