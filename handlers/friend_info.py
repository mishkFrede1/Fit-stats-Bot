from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove

from data import texts, keyboards
from db_manager import Manager
from utils.sort_week_days import sort_week_days
from utils.get_friends_keyboard import get_friends_keyboard
from utils.get_trainings_keyboard import get_trainings_keyboard
from utils.get_records_keyboard import get_records_list_keyboard
from utils.get_time_ending import getTimeEndingMinute, getTimeEndingHour
from utils.get_record_ending import getRecordCountEnding
from utils.get_age_ending import getAgeEnding
from utils import get_time_ending
from utils import graphs_functions

router = Router()
manager = Manager()

def get_privacy_keyboard(user_id: int, trainings: str, trainings_data: str, records: str, records_data: str, stats: str, stats_data: str) -> InlineKeyboardMarkup:
    privacy_settings = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Мои тренировки: {trainings}", callback_data=f"privacy_trainings_{trainings_data}_{user_id}")],
            [InlineKeyboardButton(text=f"Просмотр записей: {records}", callback_data=f"privacy_records_{records_data}_{user_id}")],
            [InlineKeyboardButton(text=f"Статистика: {stats}", callback_data=f"privacy_stats_{stats_data}_{user_id}")]
        ]
    )
    return privacy_settings

async def send_privacy_text(user_id: int, sender, is_message=True, message_id=None):
    user = manager.get_user_data(user_id)

    trainings_text = "Все 👥"
    trainings_data = "on"
    if user[12] == False: 
        trainings_text = "Только Я 👤"
        trainings_data = "off"

    records_text = "Все 👥"
    records_data = "on"
    if user[13] == False: 
        records_text = "Только Я 👤"
        records_data = "off"

    stats_text = "Все 👥"
    stats_data = "on"
    if user[14] == False: 
        stats_text = "Только Я 👤"
        stats_data = "off"

    keyboard = get_privacy_keyboard(user_id, trainings_text, trainings_data, records_text, records_data, stats_text, stats_data)

    if is_message:
        await sender.answer("🔒 <b>Кто может просматривать</b>:", parse_mode="html", reply_markup=keyboard)

    else:
        await sender.edit_message_text("🔒 <b>Кто может просматривать</b>:", user_id, message_id, parse_mode="html", reply_markup=keyboard)

@router.message(F.text == "Настройки приватности 🔐")
async def privacy_settings(message: Message):
    if manager.user_exists(message.from_user.id):
        await send_privacy_text(message.from_user.id, message)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data.startswith('privacy_'))
async def friends_privacy_on_off(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split("_")
    user_id = splited[3]
    type = splited[1]
    value = splited[2]

    option = "friends_records_visible"
    if type == "trainings":
        option = "friends_trainings_visible"
    elif type == "stats":
        option = "friends_stats_visible"

    new_value = True
    if value == "on":
        new_value = False

    manager.update_privacy_param(user_id, option, new_value)
    await send_privacy_text(user_id, bot, False, callback_query.message.message_id)

@router.callback_query(F.data.startswith('friend_info_') | F.data.startswith('friend_back_'))
async def friends_info(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split('_')
    new_message = False
    if len(splited) > 3:
        new_message = True
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id-1)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

    friend_id = int(splited[2])
    friend = manager.get_user_data(friend_id)
    friend_trainings = manager.get_trainings(friend_id)
    friend_records = manager.get_records(friend_id)
    is_trainings_acceptance = friend[12]
    is_records_acceptance = friend[13]
    is_stats_acceptance = friend[14]

    inline_keyboard = []
    if len(friend_trainings) != 0 and is_trainings_acceptance:
        inline_keyboard.append([InlineKeyboardButton(text="Показать тренировки 🏋️", callback_data=f"friend_trainings_{friend_id}")])
    if len(friend_records) != 0 and is_records_acceptance:
        inline_keyboard.append([InlineKeyboardButton(text="Показать записи 📑", callback_data=f"friend_records_{friend_id}")])
    if is_stats_acceptance:
        inline_keyboard.append([InlineKeyboardButton(text="Статистика 📈", callback_data=f"friend_stats_{friend_id}")])

    inline_keyboard.append([InlineKeyboardButton(text="Удалить из друзей ❌", callback_data=f"friend_delete_{friend_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_friend_list")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    gender = friend[4]
    if gender: 
        gender = "Женский"
    else: gender = "Мужской"

    if new_message:
        await bot.send_message(
            callback_query.from_user.id,
            texts.friend_info_text.format(
                username=friend[2],
                id=f"<a href='https://t.me/{friend[3]}'>{friend[0]}</a>", 
                date=friend[1],
                gender=gender,
                age=friend[5],
                age_ending=getAgeEnding(friend[5]),
                weight=friend[7],
                height=friend[6],
                goal=friend[8]
            ), 
            parse_mode="html", 
            reply_markup=keyboard)
    else:
        await bot.edit_message_text(
            texts.friend_info_text.format(
                username=friend[2],
                id=f"<a href='https://t.me/{friend[3]}'>{friend[0]}</a>", 
                date=friend[1],
                gender=gender,
                age=friend[5],
                age_ending=getAgeEnding(friend[5]),
                weight=friend[7],
                height=friend[6],
                goal=friend[8]
            ), 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html", 
            reply_markup=keyboard
        )

@router.callback_query(F.data == 'backto_friend_list')
async def friends_info_back(callback_query: CallbackQuery, bot: Bot):
    friends = manager.get_user_data(callback_query.from_user.id)[11]

    await bot.edit_message_text(
        "📑 <b>Список друзей</b>:", 
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        parse_mode="html", 
        reply_markup=get_friends_keyboard(friends)
    )

@router.callback_query(F.data.startswith('friend_stats_'))
async def friends_stats_type_select(callback_query: CallbackQuery, bot: Bot):
    friend_id = callback_query.data.split("_")[2]
    stats = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Качество сна 🛌", callback_data=f"friend_sleep_stats_{friend_id}")],
            [InlineKeyboardButton(text="Измерения 📏", callback_data=f"friend_measure_stats_{friend_id}")],
            [InlineKeyboardButton(text="Калории 🥪", callback_data=f"friend_calories_stats_{friend_id}")],
            [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_back_{friend_id}")]
        ]
    )
    await bot.edit_message_text(
        "⚙️ <b>Выберите тип графика</b>:", 
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        parse_mode="html", 
        reply_markup=stats
    )

@router.callback_query(F.data.startswith('friend_sleep_stats_'))
async def friends_stats_sleep(callback_query: CallbackQuery, bot: Bot):
    friend_id = callback_query.data.split("_")[3]
    await graphs_functions.sleep_quality_graph(callback_query.from_user.id, bot, friend_id, False, True, callback_query.message.message_id, "friend", True)

@router.callback_query(F.data.startswith('friend_calories_stats_'))
async def friends_stats_calories_types(callback_query: CallbackQuery, bot: Bot):
    friend_id = callback_query.data.split("_")[3]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Набранные 📈", callback_data=f"friend_cal_gained_{friend_id}"), InlineKeyboardButton(text="Сожженные 📉", callback_data=f"friend_cal_burned_{friend_id}")]
        ]
    )
    await bot.edit_message_text(
        "⚙️ <b>Выберите тип графика</b>:", 
        callback_query.from_user.id,
        callback_query.message.message_id,
        parse_mode="html", 
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith('friend_cal_'))
async def friends_stats_measurements_types(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split("_")
    type = splited[2]
    friend_id = splited[3]
    if type == "gained":
        await graphs_functions.calories_gained_graph(callback_query.from_user.id, bot, friend_id, False, True, callback_query.message.message_id, "friend", True)
    else:
        await graphs_functions.calories_burned_graph(callback_query.from_user.id, bot, friend_id, False, True, callback_query.message.message_id, "friend", True)

@router.callback_query(F.data.startswith('friend_measure_stats_'))
async def friends_stats_measurements_types(callback_query: CallbackQuery, bot: Bot):
    friend_id = callback_query.data.split("_")[3]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вес", callback_data=f"measure_friend_weight_{friend_id}"), InlineKeyboardButton(text="Рост", callback_data=f"measure_friend_height_{friend_id}")],
            [InlineKeyboardButton(text="Шея", callback_data=f"measure_friend_neck_{friend_id}"), InlineKeyboardButton(text="Грудь", callback_data=f"measure_friend_chest_{friend_id}")],
            [InlineKeyboardButton(text="Талия", callback_data=f"measure_friend_weist_{friend_id}"), InlineKeyboardButton(text="Бедра", callback_data=f"measure_friend_hips_{friend_id}")],
            [InlineKeyboardButton(text="Бицепс", callback_data=f"measure_friend_biceps_{friend_id}"), InlineKeyboardButton(text="Икры", callback_data=f"measure_friend_calf_{friend_id}")],
        ]
    )
    await bot.edit_message_text(
        "⚙️ <b>Выберите тип графика</b>:", 
        callback_query.from_user.id,
        callback_query.message.message_id,
        parse_mode="html", 
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith('measure_friend_'))
async def friends_stats_measurements(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split("_")
    type = splited[2]
    friend_id = splited[3]
    await graphs_functions.measurement_graph(callback_query.from_user.id, bot, friend_id, type, False, True, callback_query.message.message_id, True)

@router.callback_query(F.data.startswith('friend_delete_'))
async def friend_delete(callback_query: CallbackQuery, bot: Bot):
    friends = manager.get_user_data(callback_query.from_user.id)[11]
    friend_id = int(callback_query.data.split("_")[2])
    friend_list = manager.get_user_data(friend_id)[11]

    friend_list.remove(callback_query.from_user.id)
    friends.remove(friend_id)

    if friend_list == []: friend_list = None
    manager.upload_friend_list(friend_id, friend_list)

    if friends == []:
        friends = None
        await bot.edit_message_text(
            "✔️ <b>Успешное удаление</b>", 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html"
        )
        manager.upload_friend_list(callback_query.from_user.id, friends)

    else:
        manager.upload_friend_list(callback_query.from_user.id, friends)
        await bot.send_message(callback_query.from_user.id, "✔️ <b>Успешное удаление</b>", parse_mode="html")
        await bot.edit_message_text(
            "📑 <b>Список друзей</b>:", 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html", 
            reply_markup=get_friends_keyboard(friends)
        )

@router.callback_query(F.data.startswith("friend_trainings_") | F.data.startswith("backto_friend_trainings_"))
async def friend_trainings_list(callback_query: CallbackQuery, bot: Bot):
    split_index = 2
    if callback_query.data.startswith("backto_friend_trainings_"): split_index = 3

    friend_id = int(callback_query.data.split("_")[split_index])

    inline_keyboard = get_trainings_keyboard(friend_id, mode="friend_training_info", return_array=True, user_id_in_callback=True)
    inline_keyboard.append([InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_back_{friend_id}")])

    await bot.edit_message_text(
        "📑 <b>Тренировки</b>:", 
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        parse_mode="html", 
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    )

@router.callback_query(F.data.startswith("friend_training_info_") | F.data.startswith("friend_backto_train_"))
async def friend_training_info(callback_query: CallbackQuery, bot: Bot):
    splitted = callback_query.data.split('_')
    training_id = int(splitted[3])
    friend_id = splitted[4]

    training = manager.get_training(training_id)
    t_days = sort_week_days(training[3])
    t_time = training[4]
    t_type = training[5]
    exercises = training[7]

    hour = t_time.hour
    minute = t_time.minute

    if len(str(minute)) < 2: 
        minute = f"0{minute}"

    t_time = f"{hour}:{minute}"

    inline_keyboard = []
    if len(exercises) != 0:
        inline_keyboard.append([InlineKeyboardButton(text="Показать упражнения 📋", callback_data=f"friend_show_ex_{training_id}_{friend_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_friend_trainings_{friend_id}")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    await bot.edit_message_text(texts.training_info_text.format(t_time=t_time, t_type=t_type, t_days=t_days), callback_query.from_user.id, callback_query.message.message_id, parse_mode="html", reply_markup=keyboard)

async def send_exercise_text(user_id: int, message_id: int, id: int, exercises: list, keyboard: InlineKeyboardMarkup, bot: Bot):
    name=exercises[id][0]
    type=exercises[id][1]
    counts=exercises[id][2]

    text = texts.power_exercise_info_text.format(id=id+1, name=name, type=type, counts=counts)
    if type == "Кардио упражнение":
        measure = get_time_ending.getTimeEndingMinute(int(counts))
        text = texts.stretch_cardio_exercise_info_text.format(id=id+1, name=name, type=type, time=counts, measure=measure)
        
    elif type == "Для растяжки":
        measure = get_time_ending.getTimeEndingSeconds(int(counts))
        text = texts.stretch_cardio_exercise_info_text.format(id=id+1, name=name, type=type, time=counts, measure=measure)

    await bot.edit_message_text(
        text, 
        user_id, 
        message_id,
        parse_mode="html",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith('friend_show_ex_'))
async def friend_show_training_exercises(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split('_')
    friend_id = int(splited[4])
    training_id = int(splited[3])
    training = manager.get_training(training_id)
    exercises = training[7]
    id = 0

    inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_backto_train_{training_id}_{friend_id}"), 
                       InlineKeyboardButton(text="➡️", callback_data=f"friend_next_right_{id}_{training_id}_{friend_id}")]
    if len(exercises) == 1:
        inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_backto_train_{training_id}_{friend_id}")]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

    await send_exercise_text(
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        id,
        exercises, 
        keyboard, 
        bot
    )

@router.callback_query(F.data.startswith('friend_next_'))
async def friend_show_right(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    friend_id = splited_data[5]
    command = splited_data[2]

    id = int(splited_data[3])
    if command == "right": 
        id += 1
    else: id -= 1

    training_id = splited_data[4]
    exercises = manager.get_training(training_id)[7]
    lenght = len(exercises)

    is_possible = False

    if id <= lenght-1 and command == "right" or id >= 0 and command == "left": 
        is_possible = True

    if is_possible:
        if id == lenght-1:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"friend_next_left_{id}_{training_id}_{friend_id}"),
                               InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_backto_train_{training_id}_{friend_id}")]]
        elif id == 0:
            inline_keyboard = [[InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_backto_train_{training_id}_{friend_id}"), 
                               InlineKeyboardButton(text="➡️", callback_data=f"friend_next_right_{id}_{training_id}_{friend_id}")]]
        else:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"friend_next_left_{id}_{training_id}_{friend_id}"),
                                InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_backto_train_{training_id}_{friend_id}"),
                                InlineKeyboardButton(text="➡️", callback_data=f"friend_next_right_{id}_{training_id}_{friend_id}")]]

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




######################################################################




@router.callback_query(F.data.startswith("friend_records_") | F.data.startswith("backto_friend_records_"))
async def friend_records_list(callback_query: CallbackQuery, bot: Bot):
    split_index = 2
    if callback_query.data.startswith("backto_friend_records_"): split_index = 3

    friend_id = int(callback_query.data.split("_")[split_index])

    records = manager.get_records(friend_id)
    if len(records) > 5:
        keyboard = get_records_list_keyboard(
            records[0:5], 
            mode="friend_record_info", 
            user_id_in_mode=f"{friend_id}",
            arrow_buttons_text="friend_record_list", 
            back_button=True, 
            back_button_data="friend_info",
            id_in_back_button_data=f"{friend_id}",
            finder_data=f"friend_record_find_list_{friend_id}",
            id_in_arrow_buttons=f"{friend_id}"
        )
    else:
        keyboard = get_records_list_keyboard(
            records, 
            buttons_on=False, 
            mode="friend_record_info", 
            user_id_in_mode=f"{friend_id}",
            back_button=True, 
            back_button_data="friend_info",
            id_in_back_button_data=f"{friend_id}" 
        )
    await bot.edit_message_text("📑 <b>Выберите запись</b>:", callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard, parse_mode="html")



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

@router.callback_query(F.data.startswith('friend_record_info') | F.data.startswith('friend_record_back_'))
async def friend_record_info(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split('_')
    record_id = int(splited[3])
    friend_id = int(splited[4])

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
        inline_keyboard.append([InlineKeyboardButton(text="Показать упражнения 📋", callback_data=f"friend_record_show_ex_{record_id}_{friend_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_friend_records_{friend_id}")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    await bot.edit_message_text(text, callback_query.from_user.id, callback_query.message.message_id, parse_mode="html", reply_markup=keyboard)

@router.callback_query(F.data.startswith('friend_record_show_ex_'))
async def records_exercises_info(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split("_")
    record_id = splited[4]
    friend_id = splited[5]
    exercises = manager.get_record(record_id)[6]
    id = 0

    inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_back_{record_id}_{friend_id}"), 
                       InlineKeyboardButton(text="➡️", callback_data=f"friend_record_next_right_{id}_{record_id}_{friend_id}")]
    if len(exercises) == 1:
        inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_back_{record_id}_{friend_id}")]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

    await send_exercise_text(
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        id,
        exercises, 
        keyboard, 
        bot
    )

@router.callback_query(F.data.startswith('friend_record_next_'))
async def friend_record_show_ex_right_left(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[3]

    id = int(splited_data[4])
    if command == "right": 
        id += 1
    else: id -= 1

    record_id = splited_data[5]
    friend_id = splited_data[6]
    exercises = manager.get_record(record_id)[6]
    lenght = len(exercises)

    is_possible = False

    if id <= lenght-1 and command == "right" or id >= 0 and command == "left": 
        is_possible = True

    if is_possible:
        if id == lenght-1:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"friend_record_next_left_{id}_{record_id}_{friend_id}"),
                               InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_back_{record_id}_{friend_id}")]]
        elif id == 0:
            inline_keyboard = [[InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_records_back_{record_id}_{friend_id}"), 
                               InlineKeyboardButton(text="➡️", callback_data=f"friend_ecord_next_right_{id}_{record_id}_{friend_id}")]]
        else:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"friend_record_next_left_{id}_{record_id}_{friend_id}"),
                                InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_back_{record_id}_{friend_id}"),
                                InlineKeyboardButton(text="➡️", callback_data=f"friend_record_next_right_{id}_{record_id}_{friend_id}")]]

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


##############################################################################














# Листание записей
@router.callback_query(F.data.startswith('friend_record_list_'))
async def friend_records_list_show_right_left(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[3]

    id = int(splited_data[4])
    if command == "right": 
        id += 1
    else: id -= 1

    friend_id = splited_data[5]
    records = manager.get_records(friend_id)
    length = len(records) // 5 + 1
    list_left = 0 + id * 5
    list_right = 5 + id * 5

    records_list = records[list_left: list_right]

    is_possible = False
    if len(records_list) > 0:
        if id <= length-1 and command == "right" or id >= 0 and command == "left": 
            is_possible = True

    if is_possible:
        keyboard = get_records_list_keyboard(
            records_list, 
            id=id,
            mode="friend_record_info", 
            user_id_in_mode=f"{friend_id}",
            arrow_buttons_text="friend_record_list", 
            back_button=True, 
            back_button_data="friend_info",
            id_in_back_button_data=f"{friend_id}",
            id_in_arrow_buttons=f"{friend_id}",
            finder_data=f"friend_record_find_list_{friend_id}"
        )

        await bot.edit_message_text(
            "📑 <b>Выберите запись</b>:", 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html", 
            reply_markup=keyboard
        )

# Поиск записей по дате
@router.callback_query(F.data.startswith('friend_record_find_list'))
async def friend_records_list_finder(callback_query: CallbackQuery, bot: Bot):
    friend_id = int(callback_query.data.split("_")[4])
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="По дню", callback_data=f"friend_find_type_day_{friend_id}"), InlineKeyboardButton(text="По месяцу", callback_data=f"friend_find_type_month_{friend_id}"), InlineKeyboardButton(text="По году", callback_data=f"friend_find_type_year_{friend_id}")],
            [InlineKeyboardButton(text="Поиск по дате", callback_data=f"friend_find_type_date_{friend_id}")]
        ]
    )

    await bot.edit_message_text("🔍 <b>Выберите тип поиска: </b>", callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard, parse_mode="html")



# Вывод записи в поиске (filtered)
@router.callback_query(F.data.startswith('friend_record_filtered_info_') | F.data.startswith('friend_record_filtered_back_'))
async def friend_filtered_records_info(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split('_')
    record_id = int(splited[4])
    friend_id = int(splited[5])
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
        inline_keyboard.append([InlineKeyboardButton(text="Показать упражнения 📋", callback_data=f"friend_filtered_records_show_ex_{record_id}_{friend_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_friend_filtered_records_{friend_id}")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    await bot.edit_message_text(text, user_id, callback_query.message.message_id, parse_mode="html", reply_markup=keyboard)

# Возвращение к списку записей в поиске 
@router.callback_query(F.data.startswith('backto_friend_filtered_records_'))
async def friend_filtered_records_info_back(callback_query: CallbackQuery, bot: Bot):
    friend_id = callback_query.data.split("_")[4]
    records = manager.get_filter_data(callback_query.from_user.id)
    if len(records) > 5:
        keyboard = get_records_list_keyboard(
            records[0:5], 
            mode="friend_record_filtered_info", 
            type="filtered", 
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
            type="filtered", 
            back_button=True,
            back_button_data="backto_friend_records",
            id_in_back_button_data=f"{friend_id}"
        )

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
@router.callback_query(F.data.startswith('filtered_records_friend_list_'))
async def friend_filtered_records_list_show_right_left(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[4]
    friend_id = splited_data[6]

    id = int(splited_data[5])
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
        keyboard = get_records_list_keyboard(
            records_list, 
            id=id, 
            type="filtered-str", 
            arrow_buttons_text="filtered_records_friend_list", 
            back_button=True,
            back_button_data="backto_friend_records",
            user_id_in_mode=f"{friend_id}",
            id_in_arrow_buttons=f"{friend_id}",
            id_in_back_button_data=f"{friend_id}"
        )

        ending = getRecordCountEnding(list_length)
        await bot.edit_message_text(
            f"📑 <b>Найдено {list_length} {ending}</b>:", 
            callback_query.from_user.id, 
            callback_query.message.message_id, 
            parse_mode="html", 
            reply_markup=keyboard
        )

# Кнопка для показа упражнений в записи в поиске
@router.callback_query(F.data.startswith('friend_filtered_records_show_ex_'))
async def friend_filtered_records_exercises_info(callback_query: CallbackQuery, bot: Bot):
    splited = callback_query.data.split("_")
    record_id = splited[5]
    friend_id = splited[6]
    exercises = manager.get_record(record_id)[6]
    id = 0

    inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_filtered_back_{record_id}_{friend_id}"), 
                       InlineKeyboardButton(text="➡️", callback_data=f"friend_record_filtered_next_right_{id}_{record_id}_{friend_id}")]
    if len(exercises) == 1:
        inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_filtered_back_{record_id}_{friend_id}")]

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
@router.callback_query(F.data.startswith('friend_record_filtered_next_'))
async def friend_records_show_pag(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[4]

    id = int(splited_data[5])
    if command == "right": 
        id += 1
    else: id -= 1

    record_id = splited_data[6]
    friend_id = splited_data[7]
    exercises = manager.get_record(record_id)[6]
    lenght = len(exercises)

    is_possible = False

    if id <= lenght-1 and command == "right" or id >= 0 and command == "left": 
        is_possible = True

    if is_possible:
        if id == lenght-1:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"friend_record_filtered_next_left_{id}_{record_id}_{friend_id}"),
                               InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_filtered_back_{record_id}_{friend_id}")]]
        elif id == 0:
            inline_keyboard = [[InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_filtered_back_{record_id}_{friend_id}"), 
                               InlineKeyboardButton(text="➡️", callback_data=f"friend_record_filtered_next_right_{id}_{record_id}_{friend_id}")]]
        else:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"friend_record_filtered_next_left_{id}_{record_id}_{friend_id}"),
                                InlineKeyboardButton(text="Назад ↩️", callback_data=f"friend_record_filtered_back_{record_id}_{friend_id}"),
                                InlineKeyboardButton(text="➡️", callback_data=f"friend_record_filtered_next_right_{id}_{record_id}_{friend_id}")]]

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