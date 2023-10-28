from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hide_link

import tg_analytic
from config import dp
from keyboards.client import help_kb, help_back_kb


@dp.message_handler(Text("⁉Помощь"))
async def get_help_menu(message: types.Message):
    tg_analytic.statistics(message.chat.id, message.text)
    await message.answer("С чем вам необходима помощь", reply_markup=help_kb)


@dp.callback_query_handler(Text(startswith="help_"))
async def get_help_message(call: types.CallbackQuery):
    variant = int(call.data.split("_")[1])
    if variant == 1:
        msg = (hide_link('https://www.youtube.com/watch?v=g8BXfbyrRsg') + "<b>Как подобрать выгодный займ. Пошаговая и видео инструкции.</b>\n\n"
               "1. Нажмите кнопку <b>Подбор займа</b>\n"
               "2. Выберите <b>СУММУ</b> займа\n"
               "3. Выбери <b>СРОК</b> займа\n"
               "4. Выберите тип займа. <b>Бесплатный</b> (под ноль процентов) или <b>Все варианты</b> возможных займов.\n"
               "5. Выберете куда бы вы хотели получить займ?\n"
               "6. Далее выбирайте МФО с помощью кнопок Назад и Еще варианты. Чтобы получить займ нажмите <b>Получить деньги</b> и заполните заявку.\n\n"
               "⚠<b>Важно!</b>! Чтобы получить займ под ноль процентов, выбирайте новое МФО, то есть там где ва еще не брали займ, а чтобы точно получить деньги отправляйте заявки сразу во все МФО.")
    elif variant == 2:
        msg = (hide_link('https://www.youtube.com/watch?v=NSr29KAhEpU') + "<b>Как выбрать займ в популярных предложениях. Пошаговая и видео инструкции.</b>\n\n"
               "1. Нажмите кнопку <b>Популярные предложения</b>\n"
               "2. Выберите более подходящую для вас подборку нажатием кнопки\n"
               "3. Далее выбирайте МФО с помощью кнопок <b>Назад</b> и <b>Еще варианты</b>. Чтобы получить займ нажмите <b>Получить деньги</b> и заполните заявку.\n\n"
               "⚠<b>Важно</b>! Чтобы получить займ под ноль процентов, выбирайте новое МФО, то есть там где ва еще не брали займ, а чтобы точно получить деньги отправляйте заявки сразу во все МФО.")
    else:
        msg = (hide_link('https://www.youtube.com/watch?v=DXTM6vudoeA') +
               "<b>Как сменить страну или возраст. Пошаговая и видео инструкции.</b>\n\n"
               "1. Нажмите кнопку <b>Мои настройки</b> и вы увидите страну и возраст которые вы выбрали ранее.\n"
               "2. Если вы хотите изменить страну или возраст нажмите кнопку <b>Изменить</b>. \n3. Выберете страну\n"
               "4. Укажите свой возраст числом (Пример — 21)")
    await call.message.edit_text(msg, reply_markup=help_back_kb)

@dp.callback_query_handler(Text("helpmenu"))
async def get_help_menu(call: types.CallbackQuery):
    await call.message.edit_text("С чем вам необходима помощь", reply_markup=help_kb)
