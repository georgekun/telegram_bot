from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from config import base

main_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin_kb.add("📄Редактирование сервисов")
main_admin_kb.add("📩Рассылка")
main_admin_kb.add("↩Вернуться в режим пользователя")

edit_countires_kb = InlineKeyboardMarkup(row_width=1)
edit_countires_kb.add(InlineKeyboardButton(text="Россия", callback_data="editservices_Россия"))
edit_countires_kb.add(InlineKeyboardButton(text="Закрыть", callback_data="adm_close"))

async def get_services_kb(country):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for service in await base.get_services(country):
        keyboard.add(InlineKeyboardButton(text=service[0], callback_data=f"editservice_{service[-1]}"))
    keyboard.add(InlineKeyboardButton(text="🈹Добавить новый сервис", callback_data=f"add_new_service_{country}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"country_menu"))
    return keyboard

async def get_service_edit_kb(link):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="❌Удалить сервис", callback_data=f"deleteservice_{link}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"country_back_{link}"))
    return keyboard

cancel_kb = InlineKeyboardMarkup(row_width=1)
cancel_kb.add(InlineKeyboardButton(text="Отменить", callback_data="adm_cancel"))

choose_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
choose_kb.row("✅Да", "❌Нет")

countries_kb = InlineKeyboardMarkup(row_width=1)
countries_kb.add(InlineKeyboardButton(text="Россия", callback_data="choose_Россия"))

