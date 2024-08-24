from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from data import texts, keyboards
from db_manager import Manager
from utils.get_records_keyboard import get_records_list_keyboard
from utils.get_time_ending import getTimeEndingMinute, getTimeEndingSeconds, getTimeEndingHour
from utils.get_record_ending import getRecordCountEnding

router = Router()
manager = Manager()

names_table = {
    "weight": "Вес",
    "height": "Рост",
    "neck": "Шея",
    "chest": "Грудь",
    "weist": "Талия",
    "hips": "Бедра",
    "biceps": "Бицепс",
    "calf": "Икры"
}

# Кнопка для вывода списка записей
@router.message(F.text == "Все записи 📝")
async def get_records_info(message: Message):
    if manager.user_exists(message.from_user.id):
        records = manager.get_records(message.from_user.id)
        if len(records) == 0:
            await message.answer("⚙️ <b>У вас нет ни одной записи. Вам следует создать её.</b>", reply_markup=keyboards.records_settings, parse_mode="html")
        else:
            if len(records) > 5:
                keyboard = get_records_list_keyboard(records[0:5])
            else:
                keyboard = get_records_list_keyboard(records, buttons_on=False)
            await message.answer("📑 <b>Выберите запись</b>:", reply_markup=keyboard, parse_mode="html")
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

# Вывод записи
@router.callback_query(F.data.startswith('records_info') | F.data.startswith('records_back_'))
async def records_info(callback_query: CallbackQuery, bot: Bot):
    record_id = int(callback_query.data.split('_')[2])
    user_id = callback_query.from_user.id

    record = manager.get_record(record_id)
    date = record[4]
    training_type = record[5]
    exercises = record[6]
    time_spent = record[7]
    state_of_health = record[8]
    note = record[9]
    burned_cal = record[10]
    gained_cal = record[11]
    measurements = record[12]
    sleep = record[13]

    day = date.day
    month = date.month
    year = date.year

    if len(str(month)) < 2: 
        month = f"0{month}"

    text = texts.record_info_text.format(day=day, month=month, year=year)

    if training_type != None:
        text += f"<b>Тип тренировки</b>: {training_type} \n"

    if time_spent != None:
        if time_spent > 59:
            hour = time_spent // 60
            minute = time_spent % 60
            minute_ending = getTimeEndingMinute(minute)
            hour_ending = getTimeEndingHour(hour)
            if minute != 0:
                text += f"<b>Времени потрачено</b>: {hour} {hour_ending}, {minute} {minute_ending} \n"
            else:
                text += f"<b>Времени потрачено</b>: {hour} {hour_ending}\n"
        else:
            ending = getTimeEndingMinute(time_spent)
            text += f"<b>Времени потрачено</b>: {time_spent} {ending} \n"

    if gained_cal != None:
        text += f"<b>Набранно</b>: {gained_cal} килокалорий \n"

    if burned_cal != None:
        text += f"<b>Соженно</b>: {burned_cal} килокалорий \n"

    if state_of_health != None:
        text += f"<b>Самочувствие</b>: {state_of_health} \n"

    if sleep != None:
        sleep_ending = getTimeEndingHour(int(sleep))
        text += f"<b>Сон</b>: {sleep} {sleep_ending} \n"

    if measurements != None:
        measures = ""
        for i in measurements:
            ending = "см."
            if i[0] == "weight":
                ending = "кг."
            measures += f"  <b><i>{names_table[i[0]]}</i></b>: {i[1]} {ending}\n"
        text += f"\n<b>Измерения</b>:\n{measures}"

    if note != None:
        text += f"\n<b>Комменнтарий</b>: {note} \n"

    inline_keyboard = []
    if exercises != None:
        inline_keyboard.append([InlineKeyboardButton(text="Показать упражнения 📋", callback_data=f"records_show_ex_{record_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Удалить запись ❌", callback_data=f"record_delete_{record_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_records")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    await bot.edit_message_text(text, user_id, callback_query.message.message_id, parse_mode="html", reply_markup=keyboard)

# Кнопка для возвращения обратно к списку записей
@router.callback_query(F.data == 'backto_records')
async def records_info_back(callback_query: CallbackQuery, bot: Bot):
    records = manager.get_records(callback_query.from_user.id)
    if len(records) > 5:
        keyboard = get_records_list_keyboard(records[0:5])
    else:
        keyboard = get_records_list_keyboard(records, buttons_on=False)

    await bot.edit_message_text(
        "📑 <b>Выберите запись</b>:", 
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        parse_mode="html", 
        reply_markup=keyboard
    )

# Удаление записи
@router.callback_query(F.data.startswith("record_delete_"))
async def record_delete(callback_query: CallbackQuery, bot: Bot):
    record_id = callback_query.data.split("_")[2]
    manager.delete_record(record_id)

    records = manager.get_records(callback_query.from_user.id)
    if len(records) > 5:
        keyboard = get_records_list_keyboard(records[0:5])
    else:
        keyboard = get_records_list_keyboard(records, buttons_on=False)

    if len(manager.get_records(callback_query.from_user.id)) == 0:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, "✔️ <b>Запись удалена</b>.", parse_mode="html", reply_markup=keyboards.records_settings)
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, "✔️ <b>Запись удалена</b>.", parse_mode="html")
        await bot.send_message(callback_query.from_user.id, "📑 <b>Выберите запись</b>: ", parse_mode="html", reply_markup=keyboard)

# Вывод текста упражнения 
async def send_exercise_text(user_id: int, message_id: int, id: int, exercises: list, keyboard: InlineKeyboardMarkup, bot: Bot):
    name=exercises[id][0]
    type=exercises[id][1]
    counts=exercises[id][2]

    text = texts.power_exercise_info_text.format(id=id+1, name=name, type=type, counts=counts)
    if type == "Кардио упражнение":
        measure = getTimeEndingMinute(int(counts))
        text = texts.stretch_cardio_exercise_info_text.format(id=id+1, name=name, type=type, time=counts, measure=measure)
        
    elif type == "Для растяжки":
        measure = getTimeEndingSeconds(int(counts))
        text = texts.stretch_cardio_exercise_info_text.format(id=id+1, name=name, type=type, time=counts, measure=measure)

    await bot.edit_message_text(
        text, 
        user_id, 
        message_id,
        parse_mode="html",
        reply_markup=keyboard
    )

# Кнопка для показа упражнений в записи
@router.callback_query(F.data.startswith('records_show_ex_'))
async def records_exercises_info(callback_query: CallbackQuery, bot: Bot):
    record_id = callback_query.data.split("_")[3]
    exercises = manager.get_record(record_id)[6]
    id = 0

    inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_back_{record_id}"), 
                       InlineKeyboardButton(text="➡️", callback_data=f"record_next_right_{id}_{record_id}")]
    if len(exercises) == 1:
        inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_back_{record_id}")]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

    await send_exercise_text(
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        id,
        exercises, 
        keyboard, 
        bot
    )

# Листание упражнений в записи
@router.callback_query(F.data.startswith('record_next_'))
async def records_show_right(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[2]

    id = int(splited_data[3])
    if command == "right": 
        id += 1
    else: id -= 1

    record_id = splited_data[4]
    exercises = manager.get_record(record_id)[6]
    lenght = len(exercises)

    is_possible = False

    if id <= lenght-1 and command == "right" or id >= 0 and command == "left": 
        is_possible = True

    if is_possible:
        if id == lenght-1:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"record_next_left_{id}_{record_id}"),
                               InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_back_{record_id}")]]
        elif id == 0:
            inline_keyboard = [[InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_back_{record_id}"), 
                               InlineKeyboardButton(text="➡️", callback_data=f"record_next_right_{id}_{record_id}")]]
        else:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"record_next_left_{id}_{record_id}"),
                                InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_back_{record_id}"),
                                InlineKeyboardButton(text="➡️", callback_data=f"record_next_right_{id}_{record_id}")]]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

        await send_exercise_text(
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            id,
            exercises, 
            keyboard, 
            bot
        )

# Листание записей
@router.callback_query(F.data.startswith('records_list_'))
async def records_list_show_right_left(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[2]

    id = int(splited_data[3])
    if command == "right": 
        id += 1
    else: id -= 1

    records = manager.get_records(callback_query.from_user.id)
    length = len(records) // 5 + 1
    list_left = 0 + id * 5
    list_right = 5 + id * 5

    records_list = records[list_left: list_right]

    is_possible = False
    if len(records_list) > 0:
        if id <= length-1 and command == "right" or id >= 0 and command == "left": 
            is_possible = True

    if is_possible:
        keyboard = get_records_list_keyboard(records_list, id=id)

        await bot.edit_message_text(
            "📑 <b>Выберите запись</b>:", 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html", 
            reply_markup=keyboard
        )

# Поиск записей по дате
@router.callback_query(F.data == 'records_find_list')
async def records_list_show_right_left(callback_query: CallbackQuery, bot: Bot):
    await bot.edit_message_text("🔍 <b>Выберите тип поиска: </b>", callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboards.record_find_types, parse_mode="html")



# Вывод записи в поиске (filtered)
@router.callback_query(F.data.startswith('records_filtered_info_') | F.data.startswith('records_filtered_back_'))
async def filtered_records_info(callback_query: CallbackQuery, bot: Bot):
    record_id = int(callback_query.data.split('_')[3])
    user_id = callback_query.from_user.id

    record = manager.get_record(record_id)
    date = record[4]
    training_type = record[5]
    exercises = record[6]
    time_spent = record[7]
    state_of_health = record[8]
    note = record[9]
    burned_cal = record[10]
    gained_cal = record[11]
    measurements = record[12]
    sleep = record[13]

    day = date.day
    month = date.month
    year = date.year

    if len(str(month)) < 2: 
        month = f"0{month}"

    text = texts.record_info_text.format(day=day, month=month, year=year)

    if training_type != None:
        text += f"<b>Тип тренировки</b>: {training_type} \n"

    if time_spent != None:
        if time_spent > 59:
            hour = time_spent // 60
            minute = time_spent % 60
            minute_ending = getTimeEndingMinute(minute)
            hour_ending = getTimeEndingHour(hour)
            if minute != 0:
                text += f"<b>Времени потрачено</b>: {hour} {hour_ending}, {minute} {minute_ending} \n"
            else:
                text += f"<b>Времени потрачено</b>: {hour} {hour_ending}\n"
        else:
            ending = getTimeEndingMinute(time_spent)
            text += f"<b>Времени потрачено</b>: {time_spent} {ending} \n"

    if gained_cal != None:
        text += f"<b>Набранно</b>: {gained_cal} килокалорий \n"

    if burned_cal != None:
        text += f"<b>Соженно</b>: {burned_cal} килокалорий \n"

    if state_of_health != None:
        text += f"<b>Самочувствие</b>: {state_of_health} \n"

    if sleep != None:
        sleep_ending = getTimeEndingHour(int(sleep))
        text += f"<b>Сон</b>: {sleep} {sleep_ending} \n"

    if measurements != None:
        measures = ""
        for i in measurements:
            ending = "см."
            if i[0] == "weight":
                ending = "кг."
            measures += f"  <b><i>{names_table[i[0]]}</i></b>: {i[1]} {ending}\n"
        text += f"\n<b>Измерения</b>:\n{measures}"

    if note != None:
        text += f"\n<b>Комменнтарий</b>: {note} \n"

    inline_keyboard = []
    if exercises != None:
        inline_keyboard.append([InlineKeyboardButton(text="Показать упражнения 📋", callback_data=f"filtered_records_show_ex_{record_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Удалить запись ❌", callback_data=f"record_delete_{record_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_filtered_records")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    await bot.edit_message_text(text, user_id, callback_query.message.message_id, parse_mode="html", reply_markup=keyboard)

# Возвращение к списку записей в поиске 
@router.callback_query(F.data == 'backto_filtered_records')
async def filtered_records_info_back(callback_query: CallbackQuery, bot: Bot):
    records = manager.get_filter_data(callback_query.from_user.id)
    if len(records) > 5:
        keyboard = get_records_list_keyboard(records[0:5], mode="records_filtered_info", type="filtered", arrow_buttons_text="filtered_records_list", back_button=True)
    else:
        keyboard = get_records_list_keyboard(records, buttons_on=False, mode="records_filtered_info", type="filtered", arrow_buttons_text="filtered_records_list", back_button=True)

    length = len(records[0])
    ending = getRecordCountEnding(length)

    await bot.edit_message_text(
        f"📑 <b>Найдено {length} {ending}</b>:", 
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        parse_mode="html", 
        reply_markup=keyboard
    )

# Листание записей в поиске
@router.callback_query(F.data.startswith('filtered_records_list_'))
async def filtered_records_list_show_right_left(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[3]

    id = int(splited_data[4])
    if command == "right": 
        id += 1
    else: id -= 1

    records = manager.get_filter_data(callback_query.from_user.id)
    list_length = len(records[0])
    length = list_length // 5 + 1
    list_left = 0 + id * 5
    list_right = 5 + id * 5

    records_list = records[0][list_left: list_right]

    is_possible = False
    if len(records_list) > 0:
        if id <= length-1 and command == "right" or id >= 0 and command == "left": 
            is_possible = True

    if is_possible:
        keyboard = get_records_list_keyboard(records_list, id=id, type="filtered-str", arrow_buttons_text="filtered_records_list", back_button=True)

        ending = getRecordCountEnding(list_length)
        await bot.edit_message_text(
            f"📑 <b>Найдено {list_length} {ending}</b>:", 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html", 
            reply_markup=keyboard
        )

# Кнопка для показа упражнений в записи в поиске
@router.callback_query(F.data.startswith('filtered_records_show_ex_'))
async def filtered_records_exercises_info(callback_query: CallbackQuery, bot: Bot):
    record_id = callback_query.data.split("_")[4]
    exercises = manager.get_record(record_id)[6]
    id = 0

    inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_filtered_back_{record_id}"), 
                       InlineKeyboardButton(text="➡️", callback_data=f"record_filtered_next_right_{id}_{record_id}")]
    if len(exercises) == 1:
        inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_filtered_back_{record_id}")]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])
    await send_exercise_text(
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        id,
        exercises, 
        keyboard, 
        bot
    )

# Листание упражнений в записи
@router.callback_query(F.data.startswith('record_filtered_next_'))
async def records_show_right(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[3]

    id = int(splited_data[4])
    if command == "right": 
        id += 1
    else: id -= 1

    record_id = splited_data[5]
    exercises = manager.get_record(record_id)[6]
    lenght = len(exercises)

    is_possible = False

    if id <= lenght-1 and command == "right" or id >= 0 and command == "left": 
        is_possible = True

    if is_possible:
        if id == lenght-1:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"record_filtered_next_left_{id}_{record_id}"),
                               InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_filtered_back_{record_id}")]]
        elif id == 0:
            inline_keyboard = [[InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_filtered_back_{record_id}"), 
                               InlineKeyboardButton(text="➡️", callback_data=f"record_filtered_next_right_{id}_{record_id}")]]
        else:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"record_filtered_next_left_{id}_{record_id}"),
                                InlineKeyboardButton(text="Назад ↩️", callback_data=f"records_filtered_back_{record_id}"),
                                InlineKeyboardButton(text="➡️", callback_data=f"record_filtered_next_right_{id}_{record_id}")]]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

        await send_exercise_text(
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            id,
            exercises, 
            keyboard, 
            bot
        )