import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMediaPhoto

import tg_analytic
from config import dp, base
from keyboards.client import change_settings_kb, main_client_kb, popular_offers_kb, get_popular_service_kb
from states.client_states import GetUserSettings


@dp.message_handler(commands="start", state="*")
async def greeting_message(message: types.Message, state: FSMContext):
    tg_analytic.statistics(message.chat.id, message.text)
    await state.finish()
    user_settings = await base.get_user_settigns(message.from_user.id)
    if user_settings is None:
        if not await base.user_exists(message.from_user.id):
            await base.add_user(message.from_user.id, message.from_user.username)
        if (await base.get_user_settigns(message.from_user.id))[0] is None:
            await GetUserSettings.get_country.set()
            await message.answer("Выберите ваше гражданство пожалуйста.\n\n"
                                 "⚠Внимание. Получить займ могу только граждане 🇷🇺 России.",
                                 reply_markup=change_settings_kb)
    else:
        if (await base.get_user_settigns(message.from_user.id))[0] is None:
            await GetUserSettings.get_country.set()
            await message.answer("Выберите ваше гражданство пожалуйста.\n\n"
                                 "⚠Внимание. Получить займ могу только граждане 🇷🇺 России.",
                                 reply_markup=change_settings_kb)
        else:
            await message.answer(f"<b>Страна:</b> {user_settings[0]}\n"
                                 f"<b>Возраст:</b> {user_settings[1]}\n",
                                 reply_markup=main_client_kb)


@dp.callback_query_handler(Text(startswith="settings_"), state=GetUserSettings.get_country)
async def get_country(call: types.CallbackQuery, state: FSMContext):
    country = call.data.split("_")[1]
    async with state.proxy() as data:
        data['country'] = country
    await GetUserSettings.next()
    await call.message.answer(f"<strong>{call.from_user.username}</strong>, "
                              f"напиши свой возраст числом (Пример — 21)")
    await call.message.delete()


@dp.message_handler(state=GetUserSettings.get_age)
async def get_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if 17 < age < 86:
            async with state.proxy() as data:
                data['age'] = age
                await base.update_user_settings(message.from_user.id, data['country'], data['age'])
                await message.answer(f"<b>Новые данные</b>\n"
                                     f"<b>Страна:</b> {data['country']}\n"
                                     f"<b>Возраст:</b> {data['age']}\n",
                                     reply_markup=main_client_kb)
            await state.finish()
        else:
            await message.answer("Для получения займа вам должно быть не менее 18 и не более 85 лет")
    except ValueError:
        await message.answer("<b>Вы ввели информацию некорректно.\n"
                             "Введите число.</b>")


@dp.message_handler(Text("⭐Популярные предложения"))
async def get_popular_offers(message: types.Message):
    tg_analytic.statistics(message.chat.id, message.text)
    await message.answer("Выберите подходящее предложение", reply_markup=popular_offers_kb)


@dp.callback_query_handler(Text(startswith="popular_"))
async def get_popular_by_param(call: types.CallbackQuery):
    try:
        param = call.data.split("_")[1]
        country = await base.get_user_country(call.from_user.id)
        print((await base.get_popular_services_by_param(param, country))[0])
        start_service_info = (await base.get_popular_services_by_param(param, country))[0]
        await call.message.delete()
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
                                        caption=msg,
                                        reply_markup=await get_popular_service_kb(start_service_info[-1], param,
                                                                                  country))
    except IndexError:
        await call.message.delete()
        await call.message.answer("Пока что в данной категории нет займов!")


@dp.callback_query_handler(Text(startswith="getservice_"))
async def get_service_info(call: types.CallbackQuery):
    param = call.data.split("_")[1]
    callback = call.data.split("_")[2]
    country = await base.get_user_country(call.from_user.id)
    ind = await base.get_index_by_callback(callback, param, country)
    service_info = (await base.get_popular_services_by_param(param, country))[ind]
    if country == "Россия":
        valute = "руб."
 
    free_procent_if = "" if service_info[7] is None else service_info[7]
    msg = (f"<b>Займ:</b> от {service_info[2]} до {service_info[3]} {valute}\n"
           f"<b>Срок:</b>  от {service_info[4]} до {service_info[5]} дней\n"
           f"<b>Процент:</b> {service_info[6]}%\n")
    if bool(len(free_procent_if)):
        msg += (f"\n<b>Условия займа под 0%</b>\n"
                f"{free_procent_if}")
    try:
        await call.message.edit_media(InputMediaPhoto(media=service_info[8], caption=msg),
                                      reply_markup=await get_popular_service_kb(service_info[-1], param, country))
    except aiogram.utils.exceptions.MessageNotModified:
        await call.answer()
