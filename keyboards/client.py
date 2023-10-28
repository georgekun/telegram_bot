from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import base

change_settings_kb = InlineKeyboardMarkup(row_width=1)
change_settings_kb.add(InlineKeyboardButton(text="Россия", callback_data="settings_Россия"))

main_client_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_client_kb.row("🔍Подбор займа", "⭐Популярные предложения")
main_client_kb.add("📝Мои настройки")
main_client_kb.add("⁉Помощь")

async def get_settings_change_kb(userid):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Изменить", callback_data=f"changesettings_{userid}"))
    return keyboard

popular_offers_kb = InlineKeyboardMarkup(row_width=1)
popular_offers_kb.add(InlineKeyboardButton(text="Под 0%", callback_data="popular_0"))
popular_offers_kb.add(InlineKeyboardButton(text="С плохой кредитной историей", callback_data="popular_badki"))
popular_offers_kb.add(InlineKeyboardButton(text="На QIWI", callback_data="popular_qiwi"))
popular_offers_kb.add(InlineKeyboardButton(text="На Yandex.Деньги", callback_data="popular_yandex"))
popular_offers_kb.add(InlineKeyboardButton(text="Наличными через контакт", callback_data="popular_contact"))
popular_offers_kb.add(InlineKeyboardButton(text="Все варианты", callback_data="popular_all"))

async def get_popular_service_kb(callback, param, country):
    keyboard = InlineKeyboardMarkup(row_width=2)
    prev_next = await base.get_popular_prev_and_next(callback, param, country)
    link = await base.get_link_by_callback(callback)
    keyboard.add(InlineKeyboardButton(text="Получить деньги", url=link))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"getservice_{param}_{prev_next[0]}"))
    keyboard.insert(InlineKeyboardButton(text="Ещё варианты", callback_data=f"getservice_{param}_{prev_next[1]}"))
    return keyboard

help_kb = InlineKeyboardMarkup(row_width=1)
help_kb.add(InlineKeyboardButton(text="Как подобрать выгодный займ", callback_data="help_1"))
help_kb.add(InlineKeyboardButton(text="Как выбрать займ в популярных предложениях", callback_data="help_2"))
help_kb.add(InlineKeyboardButton(text="Как сменить страну или возраст", callback_data="help_3"))

help_back_kb = InlineKeyboardMarkup(row_width=1)
help_back_kb.add(InlineKeyboardButton(text="Назад", callback_data="helpmenu"))

russia_sum_choose_kb = InlineKeyboardMarkup(row_width=1)
russia_sum_choose_kb.add(InlineKeyboardButton(text="До 10 000 руб.", callback_data="russia_date_choose"))
russia_sum_choose_kb.add(InlineKeyboardButton(text="от 10 000 руб. до 20 000 руб", callback_data="russia_date_choose"))
russia_sum_choose_kb.add(InlineKeyboardButton(text="от 20 000 руб. до 30 000 руб", callback_data="russia_date_choose"))
russia_sum_choose_kb.add(InlineKeyboardButton(text="Более 30 000 руб", callback_data="russia_date_choose"))

russia_date_choose_kb = InlineKeyboardMarkup(row_width=1)
russia_date_choose_kb.add(InlineKeyboardButton(text="До 10 дней", callback_data="russia_procent_choose"))
russia_date_choose_kb.add(InlineKeyboardButton(text="От 11 до 20 дней", callback_data="russia_procent_choose"))
russia_date_choose_kb.add(InlineKeyboardButton(text="До 21 до 30 дней", callback_data="russia_procent_choose"))
russia_date_choose_kb.add(InlineKeyboardButton(text="Больше 30 дней", callback_data="russia_procent_choose"))

russia_procent_choose_kb = InlineKeyboardMarkup(row_width=1)
russia_procent_choose_kb.add(InlineKeyboardButton(text="Только 0%", callback_data="russia_0"))
russia_procent_choose_kb.add(InlineKeyboardButton(text="Показать все варианты", callback_data="russia_all"))

async def get_russia_way_choose_kb(procent):
    russia_way_choose_kb = InlineKeyboardMarkup(row_width=1)
    russia_way_choose_kb.add(InlineKeyboardButton(text="Карта банка", callback_data=f"services_russia_{procent}_card"))
    russia_way_choose_kb.add(InlineKeyboardButton(text="Яндекс.Деньги", callback_data=f"services_russia_{procent}_yandex"))
    russia_way_choose_kb.add(InlineKeyboardButton(text="QIWI", callback_data=f"services_russia_{procent}_qiwi"))
    russia_way_choose_kb.add(InlineKeyboardButton(text="Через Систему Контакт", callback_data=f"services_russia_{procent}_contact"))
    return russia_way_choose_kb



