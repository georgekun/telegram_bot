from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config import dp, base, admins, bot
from keyboards.admin import countries_kb, cancel_kb
from states.admin_states import Mailing


@dp.message_handler(Text("📩Рассылка"), user_id=admins)
async def get_mailing_message(message: types.Message):
    await message.answer("<b>🇪🇺Выберите регион для рассылки:</b>", reply_markup=countries_kb)


@dp.callback_query_handler(Text(startswith="choose_"), user_id=admins)
async def wait_for_upper_message(call: types.CallbackQuery, state: FSMContext):
    await Mailing.get_upper_message.set()
    async with state.proxy() as data:
        data['message_id'] = (await call.message.edit_text("Введите текст сообщения:", reply_markup=cancel_kb)).message_id
        data['country'] = call.data.split("_")[1]


@dp.message_handler(state=Mailing.get_upper_message)
async def wait_for_button_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.edit_message_reply_markup(message.from_user.id, data['message_id'])
        data['message_id'] = (await message.answer("Введите текст на кнопке", reply_markup=cancel_kb)).message_id
        data['message_text'] = message.parse_entities()
    await Mailing.next()


@dp.message_handler(state=Mailing.get_button_text)
async def wait_for_button_link(message: types.Message, state: FSMContext):
    await Mailing.next()
    async with state.proxy() as data:
        await bot.edit_message_reply_markup(message.from_user.id, data['message_id'])
        data['message_id'] = (await message.answer("Введите ссылку в кнопке", reply_markup=cancel_kb)).message_id
        data['button_text'] = message.text


@dp.message_handler(state=Mailing.get_button_link)
async def wait_for_button_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.edit_message_reply_markup(message.from_user.id, data['message_id'])
        data['message_id'] = (await message.answer("⏳ <strong>Рассылка началась ...</strong>")).message_id
        data['button_link'] = message.text
        users = await base.get_users_by_country(data['country'])
        normal_users, problem_users = 0, 0
        for user in users:
            try:
                await bot.send_message(user[0], data['message_text'], reply_markup=types.InlineKeyboardMarkup(row_width=1).
                                       add(types.InlineKeyboardButton(text=data['button_text'], url=data['button_link'])))
                normal_users += 1
            except:
                problem_users += 1
        await bot.edit_message_text(f"✉ <b>Рассылка окончена</b>\n\n"
                                    f"<strong>📊 Результат</strong>:\n"
                                    f"Сообщение успешно доставлено <code>{normal_users}</code> пользователям ✔️\n"
                                    f"Сообщение не было доставлено <code>{problem_users}</code> пользователям ❌",
                                    chat_id=message.from_user.id, message_id=data['message_id'])
    await state.finish()
