from aiogram import Bot, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from os import remove

from data import keyboards, texts
from db_manager import Manager

router = Router()
manager = Manager()

@router.message(F.text == "Отмена ❌")
async def cancel(message: Message, bot: Bot):
    if manager.user_exists(message.from_user.id):
        await bot.delete_message(message.from_user.id, message.message_id-1)
        await bot.delete_message(message.from_user.id, message.message_id)
        await message.answer("❌ <b>Тренировка удалена</b>", parse_mode="html")

        names = ["training_", "t_time_", "training_type_", "training_name_", "exercises_"]
        for name in names:
            try:
                remove(f'{name}{message.from_user.id}.txt')
            except: pass
        
        await message.answer("⚙️ Выберите интересующие вас настройки расписания:", reply_markup=keyboards.schedule_settings)
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())