from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager
from utils.is_number import isNumber

router = Router()
manager = Manager()

class measurements(StatesGroup):
    type = State(),
    measurement = State()

@router.message(F.text == "Замеры 📏")
async def get_measure_type(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(measurements.type)
        await message.answer("⚙️ <b>Выберите тип измерения</b>:", parse_mode="html", reply_markup=keyboards.measurement_types)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.callback_query(F.data.startswith("measure_type_")) # | F.data.startswith("measure_type_")
async def get_measurement(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    measure_type = callback_query.data.split("_")[2]
    await state.update_data(type = measure_type)
    await state.set_state(measurements.measurement)

    if measure_type == "weight":
        text = "⚙️ <b>Введите ваш вес в килограммах</b>."
    elif measure_type == "height":
        text = "⚙️ <b>Введите ваш рост в сантиметрах</b>."
    else:
        text = "⚙️ <b>Введите ваши измерения в сантиметрах</b>."

    await bot.edit_message_text(text, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, parse_mode="html")

@router.message(measurements.measurement)
async def send_measurement(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    type = data["type"]
    
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.new_record_params)
        await state.clear()
    else:
        try:
            with open(f'note_measurement_{message.from_user.id}.txt', 'a') as file:
                file.write(f"{type}, {isNumberResult};")

        except FileNotFoundError:
            with open(f'note_measurement_{message.from_user.id}.txt', 'w') as file:
                file.write(f"{type}, {isNumberResult};")

        await state.clear()
        await bot.send_message(message.from_user.id, "✔️ <b>Измерения записаны</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)