from aiogram import Bot, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from os import remove

from data import keyboards, texts
from db_manager import Manager

router = Router()
manager = Manager()

@router.message(F.text == "Удалить запись ❌")
async def cancel_note(message: Message, bot: Bot):
    if manager.user_exists(message.from_user.id):
        await message.answer("❌ <b>Запись удалена</b>", parse_mode="html")

        names = ["note_training_type_", "note_training_exercises_", "note_spent_time_", "note_health_", "note_comment_", "note_gained_calories_", "note_burned_calories_"]
        for name in names:
            try:
                remove(f'{name}{message.from_user.id}.txt')
            except: pass
        
        await message.answer("⚙️ Меню записей:", reply_markup=keyboards.records_settings)
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())