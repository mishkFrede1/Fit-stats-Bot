from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager

router = Router()
manager = Manager()

class training_type(StatesGroup):
    type = State()

class training_time(StatesGroup):
    t_time = State()

class training_name(StatesGroup):
    name = State()

@router.callback_query(F.data == "training_type")
async def get_training_type(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await state.set_state(training_type.type)
        await bot.send_message(callback_query.from_user.id, "⚙️ <b>Выберите тип тренировки</b>:", parse_mode="html", reply_markup=keyboards.training_types)
    else:
        await bot.send_message(callback_query.from_user.id, texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.message(training_type.type)
async def save_training_type(message: Message, state: FSMContext):
    if message.text in ["Силовая тренировка 🏋️", "Кардио тренировка 🏃", "Гибкость и растяжка 🤸"]:
        with open(f"training_type_{message.from_user.id}.txt", "w") as file:
            index = 2
            if message.text == "Кардио тренировка 🏃": index = 1

            file.write(message.text[0:len(message.text) - index])

        await state.clear()
        await message.answer("✔️ <b>Тип тренировки обновлен</b>.", parse_mode="html", reply_markup=keyboards.new_training)

    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")



@router.callback_query(F.data == "training_time")
async def get_training_time(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await state.set_state(training_time.t_time)
        await bot.send_message(callback_query.from_user.id, "⚙️ <b>Введите время вашей тренировки</b>. Для примера: 9:00, 14:30 и т.д.", parse_mode="html")
    else:
        await bot.send_message(callback_query.from_user.id, texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.message(training_time.t_time)
async def save_training_time(message: Message, state: FSMContext):
    if ":" in message.text:
        try:
            time = message.text.split(":")
            hour = int(time[0])
            minute = int(time[1])

            if hour < 24 and minute < 60:
                with open(f"t_time_{message.from_user.id}.txt", "w") as file:
                   file.write(message.text)

                await state.clear()
                await message.answer("✔️ <b>Время тренировки обновлено</b>.", parse_mode="html", reply_markup=keyboards.new_training)

            else:
                await message.answer(texts.incorrect_format_error_text, parse_mode="html")
                await state.clear()
        except:
            await message.answer(texts.incorrect_format_error_text, parse_mode="html")
            await state.clear()
    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()



@router.callback_query(F.data == "training_name")
async def get_training_name(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await state.set_state(training_name.name)
        await bot.send_message(callback_query.from_user.id, "⚙️ <b>Введите имя тренировки</b>:", parse_mode="html")
    else:
        await bot.send_message(callback_query.from_user.id, texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.message(training_name.name)
async def save_training_name(message: Message, state: FSMContext):
    with open(f"training_name_{message.from_user.id}.txt", "w") as file:
        file.write(message.text)

    await state.clear()
    await message.answer("✔️ <b>Название тренировки обновлен</b>.", parse_mode="html", reply_markup=keyboards.new_training)