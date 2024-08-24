from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from data import keyboards, texts
from db_manager import Manager

router = Router()
manager = Manager()

@router.message(F.text == "Настройки тренировки ⚙️")
async def training_params(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас параметры:", reply_markup=keyboards.training_params)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())