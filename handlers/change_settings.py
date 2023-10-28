from aiogram import types

import tg_analytic
from config import dp, base

from keyboards.client import change_settings_kb, get_settings_change_kb

from aiogram.dispatcher.filters import Text

from states.client_states import GetUserSettings

@dp.message_handler(Text("📝Мои настройки"))
async def user_settings_menu(message: types.Message):
    tg_analytic.statistics(message.chat.id, message.text)
    user_settings = await base.get_user_settigns(message.from_user.id)
    await message.answer(f"<b>Установлено сейчас</b>\n\n"
                         f"<b>Страна:</b> {user_settings[0]}\n"
                         f"<b>Возраст:</b> {user_settings[1]}\n",
                         reply_markup=await get_settings_change_kb(message.from_user.id))

@dp.callback_query_handler(Text(startswith="changesettings_"))
async def change_settings(call: types.CallbackQuery):
    await GetUserSettings.get_country.set()
    await call.message.edit_text("Выберите ваше гражданство пожалуйста.\n\n"
                                 "⚠Внимание. Получить займ могу только граждане 🇷🇺 России.",
                                 reply_markup=change_settings_kb)
