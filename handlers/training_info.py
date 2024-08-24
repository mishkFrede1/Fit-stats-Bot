from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from data import texts
from db_manager import Manager
from utils.sort_week_days import sort_week_days
from utils.get_trainings_keyboard import get_trainings_keyboard

router = Router()
manager = Manager()

@router.callback_query(F.data.startswith('info_') | F.data.startswith('back_'))
async def training_info(callback_query: CallbackQuery, bot: Bot):
    training_id = int(callback_query.data.split('_')[1])
    user_id = callback_query.from_user.id

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
        inline_keyboard.append([InlineKeyboardButton(text="Показать упражнения 📋", callback_data=f"show_ex_{training_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Удалить тренировку ❌", callback_data=f"delete_{training_id}")])
    inline_keyboard.append([InlineKeyboardButton(text="Назад ⬅️", callback_data=f"backto_sched")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )

    await bot.edit_message_text(texts.training_info_text.format(t_time=t_time, t_type=t_type, t_days=t_days), user_id, callback_query.message.message_id, parse_mode="html", reply_markup=keyboard)


@router.callback_query(F.data == 'backto_sched')
async def training_info(callback_query: CallbackQuery, bot: Bot):
    keyboard = get_trainings_keyboard(callback_query.from_user.id)

    await bot.edit_message_text(
        "📑 <b>Ваши тренировки</b>:", 
        callback_query.from_user.id, 
        callback_query.message.message_id, 
        parse_mode="html", 
        reply_markup=keyboard
    )