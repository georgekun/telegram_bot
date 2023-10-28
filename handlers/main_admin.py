from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import tg_analytic
from config import dp, admins, bot
from keyboards.admin import main_admin_kb
from keyboards.client import main_client_kb


@dp.message_handler(commands=["admin"], user_id=admins)
async def main_admin_menu(message: types.Message):
    await message.answer("Меню админ-панели", reply_markup=main_admin_kb)

@dp.message_handler(Text("↩Вернуться в режим пользователя"), user_id=admins)
async def get_back_to_user_mode(message: types.Message):
    await message.answer("Режим пользователя", reply_markup=main_client_kb)

@dp.message_handler(Text(contains="Статистика"), user_id=admins)
async def get_stats(message: types.Message):
    st = message.text.split(' ')
    if 'txt' in st or 'тхт' in st:
        tg_analytic.analysis(st, message.chat.id)
        with open('%s.txt' % message.chat.id, 'r', encoding='UTF-8') as file:
            await bot.send_document(message.chat.id, file)
        tg_analytic.remove(message.chat.id)
    else:
        messages = tg_analytic.analysis(st, message.chat.id)
        await bot.send_message(message.chat.id, messages)

@dp.callback_query_handler(Text("adm_cancel"), state="*")
async def adm_close(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Действие отменено")
    await call.message.delete()

@dp.callback_query_handler(Text("adm_close"))
async def adm_close(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()


