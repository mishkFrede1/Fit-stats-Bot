from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from data import keyboards, texts
from db_manager import Manager
from utils.get_trainings_keyboard import get_trainings_keyboard

router = Router()
manager = Manager()

@router.message(F.text == "Тренировки 🏋️")
async def delete_training(message: Message):
    if manager.user_exists(message.from_user.id):
        keyboard = get_trainings_keyboard(message.from_user.id)

        if keyboard.inline_keyboard == []:
            await message.answer("⚙️ <b>У вас нет ни одной тренировки, вам следует создать её</b>.", parse_mode="html", reply_markup=keyboards.schedule_settings)
        else:
            await message.answer("📑 <b>Ваши тренировки</b>:", parse_mode="html", reply_markup=keyboard)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
