from aiogram import Router
from aiogram.filters import Command 
from aiogram.types import Message, ReplyKeyboardRemove

from data import texts, keyboards
from db_manager import Manager

router = Router()
manager = Manager()

@router.message(Command("help"))
async def start(message: Message):
    await message.answer(texts.help_text, parse_mode="html")

@router.message(Command("menu"))
async def main_menu_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Главное меню:", reply_markup=keyboards.main_menu)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("start"))
async def start(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer(texts.welcome_text.format(username=message.from_user.first_name), reply_markup=keyboards.main_menu)
    else:
        await message.answer(texts.registration_text.format(username=message.from_user.first_name), reply_markup=keyboards.registration_start)