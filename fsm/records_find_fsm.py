from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import keyboards, texts
from db_manager import Manager
from utils import months, is_number
from utils.get_records_keyboard import get_records_list_keyboard
from utils.get_record_ending import getRecordCountEnding
from datetime import date

router = Router()
manager = Manager()

class date_find(StatesGroup):
    type = State()
    date = State()

class friend_date_find(StatesGroup):
    friend_id = State()
    type = State()
    date = State()

async def send_filtered_records(records: list, bot: Bot, user_id: int):
    if len(records) > 5:
        keyboard = get_records_list_keyboard(records[0:5], mode="records_filtered_info", arrow_buttons_text="filtered_records_list", back_button=True)
    else:
        keyboard = get_records_list_keyboard(records, buttons_on=False, mode="records_filtered_info", arrow_buttons_text="filtered_records_list", back_button=True)
    manager.update_filter_data(user_id, records)

    length = len(records)
    ending = getRecordCountEnding(length)

    await bot.send_message(
        user_id,
        f"📑 <b>Найдено {length} {ending}</b>:",   
        parse_mode="html", 
        reply_markup=keyboard
    )

# Поиск записей по дате
@router.callback_query(F.data.startswith('find_type_'))
async def records_find_get_type(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    find_type = callback_query.data.split("_")[2]
    await state.set_state(date_find.type)
    await state.update_data(type=find_type)
    await state.set_state(date_find.date)
    if find_type == "date":
        await bot.edit_message_text(f"🔍 <b>Введите дату записи через точку</b>: 12.7.2024 ...", callback_query.from_user.id, callback_query.message.message_id, parse_mode="html")
    elif find_type == "day":
        await bot.edit_message_text(f"🔍 <b>Введите день</b>:", callback_query.from_user.id, callback_query.message.message_id, parse_mode="html")
    elif find_type == "month":
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f"🔍 <b>Выберите месяц</b>:", parse_mode="html", reply_markup=keyboards.months)
    else:
        await bot.edit_message_text(f"🔍 <b>Введите год</b>:", callback_query.from_user.id, callback_query.message.message_id, parse_mode="html")

@router.message(date_find.date)
async def records_find_send_type(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    type = data["type"]
    if type == "day":
        isNumberResult = is_number.isNumber(message.text)
        if isNumberResult != -1:
            records = manager.get_records(message.from_user.id, "day", isNumberResult)
            await send_filtered_records(records, bot, message.from_user.id)
            await state.clear()
        else:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()

    elif type == "month":
        if message.text in months.months_list:
            records = manager.get_records(message.from_user.id, "month", months.days_in_int[message.text])
            await send_filtered_records(records, bot, message.from_user.id)
            await state.clear()
        else:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()

    elif type == "year":
        isNumberResult = is_number.isNumber(message.text)
        if isNumberResult != -1:
            records = manager.get_records(message.from_user.id, "year", isNumberResult)
            await send_filtered_records(records, bot, message.from_user.id)
            await state.clear()
        else:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()

    else:
        splitted_date = message.text.split(".")
        try:
            day = int(splitted_date[0])
            month = int(splitted_date[1])
            year = int(splitted_date[2])

            records = manager.get_records(message.from_user.id, "date", date(year, month, day))
            await send_filtered_records(records, bot, message.from_user.id)
            await state.clear()
        except:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()



async def send_filtered_friend_records(records: list, bot: Bot, user_id: int, friend_id: int):
    if len(records) > 5:
        keyboard = get_records_list_keyboard(
            records[0:5], 
            mode="friend_record_filtered_info", 
            arrow_buttons_text="filtered_records_friend_list", 
            back_button=True,
            back_button_data="backto_friend_records",
            user_id_in_mode=f"{friend_id}",
            id_in_arrow_buttons=f"{friend_id}",
            id_in_back_button_data=f"{friend_id}"
        )
    else:
        keyboard = get_records_list_keyboard(
            records, 
            buttons_on=False, 
            mode="friend_record_filtered_info", 
            user_id_in_mode=f"{friend_id}",
            back_button=True,
            back_button_data="backto_friend_records",
            id_in_back_button_data=f"{friend_id}"
        )
    
    manager.update_filter_data(user_id, records)

    length = len(records)
    ending = getRecordCountEnding(length)

    await bot.send_message(
        user_id,
        f"📑 <b>Найдено {length} {ending}</b>:",   
        parse_mode="html", 
        reply_markup=keyboard
    )

# Поиск записей по дате
@router.callback_query(F.data.startswith('friend_find_type_'))
async def friend_records_find_get_type(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    splited = callback_query.data.split("_")
    find_type = splited[3]
    friend_id = splited[4]
    await state.set_state(friend_date_find.friend_id)
    await state.update_data(friend_id=friend_id)

    await state.set_state(friend_date_find.type)
    await state.update_data(type=find_type)

    await state.set_state(friend_date_find.date)
    if find_type == "date":
        await bot.edit_message_text(f"🔍 <b>Введите дату записи через точку</b>: 12.7.2024 ...", callback_query.from_user.id, callback_query.message.message_id, parse_mode="html")
    elif find_type == "day":
        await bot.edit_message_text(f"🔍 <b>Введите день</b>:", callback_query.from_user.id, callback_query.message.message_id, parse_mode="html")
    elif find_type == "month":
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, f"🔍 <b>Выберите месяц</b>:", parse_mode="html", reply_markup=keyboards.months)
    else:
        await bot.edit_message_text(f"🔍 <b>Введите год</b>:", callback_query.from_user.id, callback_query.message.message_id, parse_mode="html")

@router.message(friend_date_find.date)
async def friend_records_find_send_type(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    type = data["type"]
    friend_id = data["friend_id"]
    if type == "day":
        isNumberResult = is_number.isNumber(message.text)
        if isNumberResult != -1:
            records = manager.get_records(friend_id, "day", isNumberResult)
            await send_filtered_friend_records(records, bot, message.from_user.id, friend_id)
            await state.clear()
        else:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()

    elif type == "month":
        if message.text in months.months_list:
            records = manager.get_records(friend_id, "month", months.days_in_int[message.text])
            await send_filtered_friend_records(records, bot, message.from_user.id, friend_id)
            await state.clear()
        else:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()

    elif type == "year":
        isNumberResult = is_number.isNumber(message.text)
        if isNumberResult != -1:
            records = manager.get_records(friend_id, "year", isNumberResult)
            await send_filtered_friend_records(records, bot, message.from_user.id, friend_id)
            await state.clear()
        else:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()

    else:
        splitted_date = message.text.split(".")
        try:
            day = int(splitted_date[0])
            month = int(splitted_date[1])
            year = int(splitted_date[2])

            records = manager.get_records(friend_id, "date", date(year, month, day))
            await send_filtered_friend_records(records, bot, message.from_user.id, friend_id)
            await state.clear()
        except:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.records_settings)
            await state.clear()