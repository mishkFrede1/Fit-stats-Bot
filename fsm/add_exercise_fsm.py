from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import keyboards, texts
from db_manager import Manager
from utils.is_number import isNumber

class add_exercise(StatesGroup):
    name = State()
    type = State()
    counts_or_time = State()

router = Router()
manager = Manager()

@router.message(F.text == "Добавить упражнение ➕")
async def get_exercise_name(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(add_exercise.name)
        await message.answer("⚙️ Введите название упражнения:")
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(add_exercise.name)
async def get_exercise_type(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(add_exercise.type)

    await message.answer("⚙️ Выберите тип упражнения:", reply_markup=keyboards.exercise_types)

@router.message(add_exercise.type)
async def get_exercise_counts_or_time(message: Message, state: FSMContext):
    if message.text in ["Силовое упражнение 🏋️", "Кардио упражнение 🏃", "Для растяжки 🤸"]:    
        await state.update_data(type = message.text[0:len(message.text) - 2])
        await state.set_state(add_exercise.counts_or_time)

        if message.text == "Силовое упражнение 🏋️":
            await message.answer("⚙️ Введите количество подходов для этого упражнения:", reply_markup=ReplyKeyboardRemove())
        elif message.text == "Кардио упражнение 🏃":
            await message.answer("⚙️ Введите продолжительность упражнения в минутах:", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("⚙️ Введите продолжительность упражнения в секундах:", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.new_training)
        await state.clear()

@router.message(add_exercise.counts_or_time)
async def set_all_data(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.new_training)
        await state.clear()
    else:
        await state.update_data(counts_or_time = isNumberResult)
        data = await state.get_data()
        exercise = f"{data['name']}, {data['type']}, {data['counts_or_time']}; "

        try:
            with open(f'exercises_{message.from_user.id}.txt', 'a') as file:
                file.write(f"{exercise}")

        except FileNotFoundError:
            with open(f'exercises_{message.from_user.id}.txt', 'w') as file:
                file.write(f"{exercise}")

        await message.answer("✔️ <b>Упражнение добавлено в тренировку</b>.", parse_mode="html", reply_markup=keyboards.new_training)
        await state.clear()