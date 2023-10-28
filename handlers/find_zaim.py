from aiogram import types
from aiogram.dispatcher.filters import Text

import tg_analytic
from config import dp
from keyboards.client import *


@dp.message_handler(Text("🔍Подбор займа"))
async def loan_selection(message: types.Message):
    tg_analytic.statistics(message.chat.id, message.text)
    country = await base.get_user_country(message.from_user.id)

    if country == "Россия":
        markup = russia_sum_choose_kb

    await message.answer("Вы воспользовались <b>Мастером подбора займов</b>\n\n<b>Выберите СУММУ займа</b>", reply_markup=markup)

@dp.callback_query_handler(Text("russia_date_choose"))
async def russia_date_choose(call: types.CallbackQuery):
    await call.message.answer("<b>Выбери СРОК займа</b>", reply_markup=russia_date_choose_kb)
    await call.answer()

@dp.callback_query_handler(Text("russia_procent_choose"))
async def russia_date_choose(call: types.CallbackQuery):
    await call.message.answer("<b>Выбери ПРОЦЕНТ займа</b>", reply_markup=russia_procent_choose_kb)
    await call.answer()

@dp.callback_query_handler(Text(startswith="russia_"))
async def russia_payment_choose(call: types.CallbackQuery):
    procent = call.data.split("_")[1]
    await call.message.answer("<b>Выбери СПОСОБ ПОЛУЧЕНИЯ займа</b>", reply_markup=await get_russia_way_choose_kb(procent))
    await call.answer()


@dp.callback_query_handler(Text(startswith="services_russia_"))
async def get_popular_by_param(call: types.CallbackQuery):
    try:
        param = call.data.split("_")[3]
        procent = call.data.split("_")[2]
        country = await base.get_user_country(call.from_user.id)
        start_service_info = (await base.get_popular_services_by_param(param, country))[0]
        if country == "Россия":
            valute = "руб."
        elif country == "Казахстан":
            valute = "тенге"
        elif country == "Украина":
            valute = "гр."
        free_procent_if = "" if start_service_info[7] is None else start_service_info[7]
        msg = (f"<b>Займ:</b> от {start_service_info[2]} до {start_service_info[3]} {valute}\n"
               f"<b>Срок:</b>  от {start_service_info[4]} до {start_service_info[5]} дней\n"
               f"<b>Процент:</b> {start_service_info[6]}%\n")
        if bool(len(free_procent_if)):
            msg += (f"\n<b>Условия займа под 0%</b>\n"
                    f"{free_procent_if}")
        await call.message.answer_photo(photo=start_service_info[8],
                                        caption=msg, reply_markup=await get_popular_service_kb(start_service_info[-1], param, country))
    except IndexError:
        await call.message.answer("Пока что в данной категории нет займов!")
