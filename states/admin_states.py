from aiogram.dispatcher.filters.state import State, StatesGroup

class AddService(StatesGroup):
    get_link = State()
    get_bottom_sum = State()
    get_upper_sum = State()
    get_bottom_term = State()
    get_upper_term = State()
    get_procent = State()
    get_service_have_free_procent_if = State()
    get_free_procent_if = State()
    get_picture = State()
    get_is_badki = State()
    get_is_card = State()
    get_is_yandex = State()
    get_is_qiwi = State()
    get_is_contact = State()

class Mailing(StatesGroup):
    get_upper_message = State()
    get_button_text = State()
    get_button_link = State()
