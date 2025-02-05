from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from data import texts
from db_manager import Manager
from utils.get_time_ending import getTimeEndingMinute, getTimeEndingSeconds

router = Router()
manager = Manager()

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
        chat_id=user_id, 
        message_id=message_id,
        parse_mode="html",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith('show_ex_'))
async def show_training_exercises(callback_query: CallbackQuery, bot: Bot):
    training_id = int(callback_query.data.split('_')[2])
    training = manager.get_training(training_id)
    exercises = training[7]
    id = 0

    inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"back_{training_id}"), 
                       InlineKeyboardButton(text="➡️", callback_data=f"next_right_{id}_{training_id}")]
    if len(exercises) == 1:
        inline_keyboard = [InlineKeyboardButton(text="Назад ↩️", callback_data=f"back_{training_id}")]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_keyboard])

    await send_exercise_text(
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        id,
        exercises, 
        keyboard, 
        bot
    )

@router.callback_query(F.data.startswith('next_'))
async def show_right(callback_query: CallbackQuery, bot: Bot):
    splited_data = callback_query.data.split('_')
    command = splited_data[1]

    id = int(splited_data[2])
    if command == "right": 
        id += 1
    else: id -= 1

    training_id = splited_data[3]
    exercises = manager.get_training(training_id)[7]
    lenght = len(exercises)

    is_possible = False

    if id <= lenght-1 and command == "right" or id >= 0 and command == "left": 
        is_possible = True

    if is_possible:
        if id == lenght-1:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"next_left_{id}_{training_id}"),
                               InlineKeyboardButton(text="Назад ↩️", callback_data=f"back_{training_id}")]]
        elif id == 0:
            inline_keyboard = [[InlineKeyboardButton(text="Назад ↩️", callback_data=f"back_{training_id}"), 
                               InlineKeyboardButton(text="➡️", callback_data=f"next_right_{id}_{training_id}")]]
        else:
            inline_keyboard = [[InlineKeyboardButton(text="⬅️", callback_data=f"next_left_{id}_{training_id}"),
                                InlineKeyboardButton(text="Назад ↩️", callback_data=f"back_{training_id}"),
                                InlineKeyboardButton(text="➡️", callback_data=f"next_right_{id}_{training_id}")]]

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