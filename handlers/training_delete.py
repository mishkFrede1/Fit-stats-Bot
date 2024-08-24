from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from data import keyboards
from db_manager import Manager
from utils.get_trainings_keyboard import get_trainings_keyboard

router = Router()
manager = Manager()

@router.callback_query(lambda c: c.data and c.data.startswith('delete_'))
async def delete_training_from_db(callback_query: CallbackQuery, bot: Bot):
    training_id = int(callback_query.data.split('_')[1])
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        manager.delete_training(training_id)

        await bot.send_message(callback_query.from_user.id, "✔️ <b>Тренировка удалена</b>.", parse_mode="html", reply_markup=keyboards.schedule_settings)
        keyboard = get_trainings_keyboard(callback_query.from_user.id)
        if len(keyboard.inline_keyboard) == 0:
            await bot.send_message(callback_query.from_user.id, "⚙️ Выберите интересующие вас настройки расписания:", reply_markup=keyboards.schedule_settings)
        else:
            await bot.send_message(
                callback_query.from_user.id,
                "📑 <b>Ваши тренировки</b>:", 
                parse_mode="html", 
                reply_markup=keyboard
            )
    
    except Exception as _ex:
        print("[INFO]", _ex)