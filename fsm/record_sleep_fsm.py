from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager
from utils.is_number import isNumber

router = Router()
manager = Manager()

class sleep(StatesGroup):
    sleep = State()

@router.message(F.text == "Сон 🛌")
async def get_note_sleep(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(sleep.sleep)
        await message.answer("⚙️ <b>Введите сколько часов вы спали этой ночью</b>:", parse_mode="html")
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.message(sleep.sleep)
async def save_note_sleep(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult != -1:
        with open(f"note_sleep_{message.from_user.id}.txt", "w") as file:
            file.write(message.text)

        await state.clear()
        await message.answer("✔️ <b>Комментарий записан</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html")
        await state.clear()