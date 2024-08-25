from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager
from utils.is_number import isNumber

router = Router()
manager = Manager()

class calories_burned(StatesGroup):
    calories = State()

class calories_gained(StatesGroup):
    calories = State()

@router.message(F.text == "Калории 🍽")
async def get_note_calories_type(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите тип:", reply_markup=keyboards.calories_types)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html")

@router.callback_query(F.data.startswith("cal_burned"))
async def get_note_calories_burned(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(calories_burned.calories)
    await bot.send_message(callback_query.from_user.id, f"🍽 <b>Введите количество соженных ккал.</b>:", parse_mode="html")
    
@router.message(calories_burned.calories)
async def save_note_calories_burned(message: Message, state: FSMContext, bot: Bot):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

    else:
        with open(f"note_burned_calories_{message.from_user.id}.txt", "w") as file:
            file.write(f"{message.text}")

        await state.clear()
        await bot.send_message(message.from_user.id, "✔️ <b>Калории записаны</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)


@router.callback_query(F.data.startswith("cal_gained"))
async def get_note_calories_gained(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(calories_gained.calories)
    await bot.send_message(callback_query.from_user.id, f"🍽 <b>Введите количество набранных ккал.</b>:", parse_mode="html")
    
@router.message(calories_gained.calories)
async def save_note_calories_gained(message: Message, state: FSMContext, bot: Bot):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

    else:
        with open(f"note_gained_calories_{message.from_user.id}.txt", "w") as file:
            file.write(f"{message.text}")

        await state.clear()
        await bot.send_message(message.from_user.id, "✔️ <b>Калории записаны</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)