from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config import dp, base, admins
from keyboards.admin import get_services_kb, choose_kb, edit_countires_kb, cancel_kb, get_service_edit_kb
from states.admin_states import AddService


@dp.message_handler(Text("📄Редактирование сервисов"), user_id=admins)
async def services_menu(message: types.Message):
    await message.answer("⚙Выберите страну:", reply_markup=edit_countires_kb)

@dp.callback_query_handler(Text("country_menu"))
async def call_services_menu(call: types.CallbackQuery):
    await call.message.edit_text("⚙Выберите страну:", reply_markup=edit_countires_kb)

@dp.callback_query_handler(Text(startswith="editservices_"))
async def edit_service(call: types.CallbackQuery):
    country = call.data.split("_")[1]
    await call.message.edit_text("📄Выберите сервис:", reply_markup=await get_services_kb(country))

@dp.callback_query_handler(Text(startswith="add_new_service_"))
async def add_new_service(call: types.CallbackQuery, state: FSMContext):
    await AddService.get_link.set()
    country = call.data.split("_")[3]
    async with state.proxy() as data:
        data['country'] = country
    await call.message.answer("Введите ссылку:", reply_markup=cancel_kb)
    await call.message.delete()

@dp.message_handler(state=AddService.get_link)
async def get_service_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await AddService.next()
    await message.answer("Введите нижнюю границу размера займа:", reply_markup=cancel_kb)

@dp.message_handler(state=AddService.get_bottom_sum)
async def get_service_link(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['bottom_sum'] = int(message.text)
        await AddService.next()
        await message.answer("Введите верхнюю границу размера займа:", reply_markup=cancel_kb)
    except ValueError:
        await message.answer("Неверный ввод! Вы должны ввести число")

@dp.message_handler(state=AddService.get_upper_sum)
async def get_service_link(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['upper_sum'] = int(message.text)
        await AddService.next()
        await message.answer("Введите нижнюю границу срока займа:", reply_markup=cancel_kb)
    except ValueError:
        await message.answer("Неверный ввод! Вы должны ввести число")

@dp.message_handler(state=AddService.get_bottom_term)
async def get_service_link(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['bottom_term'] = int(message.text)
        await AddService.next()
        await message.answer("Введите верхнюю границу срока займа:", reply_markup=cancel_kb)
    except ValueError:
        await message.answer("Неверный ввод! Вы должны ввести число")

@dp.message_handler(state=AddService.get_upper_term)
async def get_service_link(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['upper_term'] = int(message.text)
        await AddService.next()
        await message.answer("Введите процент займа:", reply_markup=cancel_kb)
    except ValueError:
        await message.answer("Неверный ввод! Вы должны ввести число")

@dp.message_handler(state=AddService.get_procent)
async def get_service_link(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['procent'] = int(message.text)
        await AddService.get_service_have_free_procent_if.set()
        await message.answer("Есть ли условие займа под 0% ?", reply_markup=choose_kb)
    except ValueError:
        await message.answer("Неверный ввод! Вы должны ввести число")

@dp.message_handler(state=AddService.get_service_have_free_procent_if)
async def get_is_badki(message: types.Message, state: FSMContext):
    ans = message.text
    if ans in ["✅Да", "❌Нет"]:
        if ans == "✅Да":
            await message.answer("Введите условие займа под 0%:")
            await AddService.get_free_procent_if.set()
        else:
            async with state.proxy() as data:
                data['free_procent_if'] = None
            await message.answer("Отправьте картинку, которая будет отображаться пользователю", reply_markup=cancel_kb)
            await AddService.get_picture.set()
    else:
        await message.answer("Неверный ответ!\n\n Нажмите на одну из кнопкок ниже", reply_markup=choose_kb)

@dp.message_handler(state=AddService.get_free_procent_if)
async def get_service_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['free_procent_if'] = message.text
    await AddService.get_picture.set()
    await message.answer("Отправьте картинку, которая будет отображаться пользователю", reply_markup=cancel_kb)

@dp.message_handler(state=AddService.get_picture, content_types=['photo'])
async def get_picture(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['picture'] = message.photo[0].file_id
    await AddService.next()
    await message.answer("Займ с плохой кредитной историей?", reply_markup=choose_kb)

@dp.message_handler(state=AddService.get_is_badki)
async def get_is_badki(message: types.Message, state: FSMContext):
    ans = message.text
    if ans in ["✅Да", "❌Нет"]:
        async with state.proxy() as data:
            data['is_badki'] = 1 if ans == "✅Да" else 0
        await AddService.next()
        await message.answer("Банковская карта? (Способ получения займа)", reply_markup=choose_kb)
    else:
        await message.answer("Неверный ответ!\n\n Нажмите на одну из кнопкок ниже", reply_markup=choose_kb)

@dp.message_handler(state=AddService.get_is_card)
async def get_is_badki(message: types.Message, state: FSMContext):
    ans = message.text
    if ans in ["✅Да", "❌Нет"]:
        async with state.proxy() as data:
            data['is_card'] = 1 if ans == "✅Да" else 0
        await AddService.next()
        await message.answer("Яндекс деньги? (Способ получения займа)", reply_markup=choose_kb)
    else:
        await message.answer("Неверный ответ!\n\n Нажмите на одну из кнопкок ниже", reply_markup=choose_kb)

@dp.message_handler(state=AddService.get_is_yandex)
async def get_is_badki(message: types.Message, state: FSMContext):
    ans = message.text
    if ans in ["✅Да", "❌Нет"]:
        async with state.proxy() as data:
            data['is_yandex'] = 1 if ans == "✅Да" else 0
        await AddService.next()
        await message.answer("QIWI? (Способ получения займа)", reply_markup=choose_kb)
    else:
        await message.answer("Неверный ответ!\n\n Нажмите на одну из кнопкок ниже", reply_markup=choose_kb)

@dp.message_handler(state=AddService.get_is_qiwi)
async def get_is_badki(message: types.Message, state: FSMContext):
    ans = message.text
    if ans in ["✅Да", "❌Нет"]:
        async with state.proxy() as data:
            data['is_qiwi'] = 1 if ans == "✅Да" else 0
        await AddService.next()
        await message.answer("Через Систему Контакт? (Способ получения займа)", reply_markup=choose_kb)
    else:
        await message.answer("Неверный ответ!\n\n Нажмите на одну из кнопкок ниже", reply_markup=choose_kb)

@dp.message_handler(state=AddService.get_is_contact)
async def get_is_contact(message: types.Message, state: FSMContext):
    ans = message.text
    if ans in ["✅Да", "❌Нет"]:
        async with state.proxy() as data:
            data['is_contact'] = 1 if ans == "✅Да" else 0
            await base.add_service(data['link'], data['country'], data['bottom_sum'], data['upper_sum'], data['bottom_term'], data['upper_term'],
                                   data['procent'], data['picture'], data['is_badki'], data['is_card'], data['is_yandex'], data['is_qiwi'], data['is_contact'], data['free_procent_if'])
            await message.answer("<b>✅Сервис добавлен!</b>\n\n📄Выберите сервис", reply_markup=await get_services_kb(data['country']))
        await state.finish()
    else:
        await message.answer("Неверный ответ!\n\n Нажмите на одну из кнопкок ниже", reply_markup=choose_kb)

@dp.callback_query_handler(Text(startswith="editservice_"), user_id=admins)
async def edit_service(call: types.CallbackQuery):
    service = call.data.split("_")[1]
    service_info = await base.get_service_info(service)
    country = service_info[1]
    if country == "Россия":
        valute = "руб."
    elif country == "Казахстан":
        valute = "тенге"
    elif country == "Украина":
        valute = "гр."
    free_procent_if = "Нет" if service_info[7] is None else service_info[7]
    is_badki = "Нет" if bool(service_info[9]) else "Да"
    is_card = "Нет" if bool(service_info[10]) else "Да"
    is_yandex = "Нет" if bool(service_info[11]) else "Да"
    is_qiwi = "Нет" if bool(service_info[12]) else "Да"
    is_contact = "Нет" if bool(service_info[13]) else "Да"
    msg = "<b>🈯Информация о сервисе</b>\n\n"
    msg += (f"<b>Ссылка</b>: {service_info[0]}\n"
            f"<b>Сумма</b>: от {service_info[2]} {valute} до {service_info[3]} {valute}\n"
            f"<b>Срок</b>: от {service_info[4]} до {service_info[5]} дней\n"
            f"<b>Процент займа</b>: {service_info[6]}%\n"
            f"<b>Условие займа под 0%</b>: {free_procent_if}\n"
            f"<b>С плохой кредитной историей</b>: {is_badki}\n"
            f"<b>Карта</b>: {is_card}\n"
            f"<b>Яндекс.Деньги</b>: {is_yandex}\n"
            f"<b>QIWI</b>: {is_qiwi}\n"
            f"<b>Система Контакт</b>: {is_contact}\n")
    await call.message.answer_photo(photo=service_info[8], caption=msg, reply_markup=await get_service_edit_kb(service))
    await call.message.delete()

@dp.callback_query_handler(Text(startswith="deleteservice_"))
async def delete_service(call: types.CallbackQuery):
    country = await base.get_country_by_link(call.data.split("_")[1])
    await base.delete_service(call.data.split("_")[1])
    await call.message.answer("<b>✅Сервис удалён</b>\n\n📄Выберите сервис:", reply_markup=await get_services_kb(country))
    await call.message.delete()

@dp.callback_query_handler(Text(startswith="country_back_"))
async def get_back_to_country_menu(call: types.CallbackQuery):
    country = await base.get_country_by_link(call.data.split("_")[2])
    await call.message.answer("📄Выберите сервис:", reply_markup=await get_services_kb(country))
    await call.message.delete()




