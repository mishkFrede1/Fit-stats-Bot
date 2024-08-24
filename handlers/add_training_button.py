from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from data import keyboards, texts
from db_manager import Manager

router = Router()
manager = Manager()

@router.message(F.text == "Добавить тренировку ➕")
async def new_training(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Меню создания тренировки:", parse_mode="html", reply_markup=keyboards.new_training)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
