from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager
from utils.get_trainings_keyboard import get_trainings_keyboard

router = Router()
manager = Manager()

class training(StatesGroup):
    training = State()

class weight(StatesGroup):
    weight = State()

@router.message(F.text == "Тренировка 🏋️")
async def get_note_training(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(training.training)
        await message.answer("⚙️ <b>Выберите вашу тренировку</b>:", reply_markup=get_trainings_keyboard(message.from_user.id, "note_training"), parse_mode="html")
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.callback_query(F.data.startswith("note_training"))
async def save_note_training(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    training_id = callback_query.data.split("_")[2]
    training = manager.get_training(training_id)

    training_type = training[5]
    with open(f"note_training_type_{callback_query.from_user.id}.txt", "w") as file:
        file.write(training_type)

    text = ""
    training_exercises = training[7]
    if training_exercises != []:
        for i in training_exercises:
            text += f"{i[0]}, {i[1]}, {i[2]};"

    with open(f"note_training_exercises_{callback_query.from_user.id}.txt", "w") as file:
        file.write(text)

    await state.clear()
    await bot.send_message(callback_query.from_user.id, "✔️ <b>Тренировка выбрана</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)




# @router.callback_query(F.data.startswith("note_training"))
# async def get_exercises_weights(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
#     training_id = callback_query.data.split("_")[2]
#     training = manager.get_training(training_id)

#     training_type = training[5]
#     with open(f"note_training_type_{callback_query.from_user.id}.txt", "w") as file:
#         file.write(training_type)

#     inline_keyboard = []
#     training_exercises = training[7]
#     for i, el in enumerate(training_exercises):
#         if i[1] == "Силовое упражнение ":
#             inline_keyboard.append([InlineKeyboardButton(text=f"{el[0]}", callback_query=f"exercise_weight_{i}_")])
#     inline_keyboard.append([InlineKeyboardButton(text=f"Подтвердить", callback_query=f"exercise_weight_done")])
#     keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

#     await bot.send_message(callback_query.from_user.id, "⚙️ <b>Введите максимальный вес на каждом упражнении</b>:", parse_mode="html", reply_markup=keyboard)


# @router.callback_query(F.data.startswith("exercise_weight_"))
# async def save_exercise_weight(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
#     await state.set_state(weight.weight)
#     await bot.send_message(callback_query.from_user.id, "⚙️ Введите максимальный вес:")
#     with open(f"exercise_{callback_query.from_user.id}.txt", "w") as file:
#         file.write(text)

# @router.callback_query(weight.weight)
# async def get_exercises_weights(message: Message, state: FSMContext, bot: Bot):
#     data = F.data.split("_")

#     with open(f"exercises_weights_{message.from_user.id}.txt", "w") as file:
#         file.write(f"{data[2]}, {}")

#     await state.clear()




    # text = ""
    # if training_exercises != []:
    #     for i in training_exercises:
    #         text += f"{i[0]}, {i[1]}, {i[2]};"

    # with open(f"note_training_exercises_{callback_query.from_user.id}.txt", "w") as file:
    #     file.write(text)

    #else:
    #    await state.clear()
    #    await bot.send_message(callback_query.from_user.id, "✔️ <b>Тренировка выбрана</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)


# @router.callback_query(F.data.startswith("note_training"))
# async def save_note_training(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
#     training_id = callback_query.data.split("_")[2]
#     training = manager.get_training(training_id)

#     training_type = training[5]
#     with open(f"note_training_type_{callback_query.from_user.id}.txt", "w") as file:
#         file.write(training_type)

#     text = ""
#     training_exercises = training[7]
#     if training_exercises != []:
#         for i in training_exercises:
#             text += f"{i[0]}, {i[1]}, {i[2]};"

#     with open(f"note_training_exercises_{callback_query.from_user.id}.txt", "w") as file:
#         file.write(text)

#     await state.clear()
#     await bot.send_message(callback_query.from_user.id, "✔️ <b>Тренировка выбрана</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)