from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager
from utils.is_number import isNumber

router = Router()
manager = Manager()

class spent_time(StatesGroup):
    time = State()

@router.message(F.text == "Затраченное время ⌛️")
async def get_note_spent_time(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(spent_time.time)
        await message.answer("⚙️ <b>Введите затраченное время на тренировку в минутах</b>:", parse_mode="html")
    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

@router.message(spent_time.time)
async def send_note_spent_time(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
    else:
        with open(f"note_spent_time_{message.from_user.id}.txt", "w") as file:
            file.write(message.text)

        await state.clear()
        await message.answer("✔️ <b>Время обновлено</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)