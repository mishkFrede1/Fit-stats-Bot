from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import keyboards, texts
from db_manager import Manager
from utils.is_number import isNumber

router = Router()
manager = Manager()

class user_data_update(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()
    goal = State()

class new_gender(StatesGroup):
    gender = State()

class new_age(StatesGroup):
    age = State()

class new_weight(StatesGroup):
   weight = State()

class new_height(StatesGroup):
    height = State()

class new_goal(StatesGroup):
    goal = State()


#
# Changing all user data:
#

#Gender query 
@router.callback_query(F.data == "allChange")
async def genderInline(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        
        await state.set_state(user_data_update.gender)
        await bot.send_message(callback_query.from_user.id, "⚙️ Выберите пожалуйста ваш пол:", reply_markup=keyboards.gender_choice)
    else:
        await bot.send_message(callback_query.from_user.id, texts.unregistered_access_text, parse_mode="html")

#Age query and Gender recording
@router.message(user_data_update.gender)
async def age(message: Message, state: FSMContext):
    user_gender = True
    if message.text == "Мужской": user_gender = False

    await state.update_data(gender = user_gender)
    await state.set_state(user_data_update.age)

    await message.answer("⚙️ Введите ваш возраст:", parse_mode="html", reply_markup=ReplyKeyboardRemove())

#Weight query and Age recording
@router.message(user_data_update.age)
async def weight(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.update_data(age = isNumberResult)

        await message.answer("⚙️ Введите ваш вес:", parse_mode="html")
        await state.set_state(user_data_update.weight)

#Height query and Weight recording
@router.message(user_data_update.weight)
async def height(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.update_data(weight = isNumberResult)

        await state.set_state(user_data_update.height)
        await message.answer("⚙️ Введите ваш рост:", parse_mode="html")

#Goal query and Height recording
@router.message(user_data_update.height)
async def db_send_data(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.update_data(height = isNumberResult)

        await state.set_state(user_data_update.goal)
        await message.answer("⚙️ Выберите направление:", parse_mode="html", reply_markup=keyboards.goal_set)

#Goal recording and save data in DB
@router.message(user_data_update.goal)
async def db_send_data(message: Message, state: FSMContext):
    isRight = False
    if message.text == "Снижение веса":
        await state.update_data(goal = "Снижение веса")
        isRight = True
    elif message.text == "Набор веса":
        await state.update_data(goal = "Набор веса")
        isRight = True
    elif message.text == "Удержание веса":
        await state.update_data(goal = "Удержание веса")
        isRight = True

    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

    if isRight:
        data = await state.get_data()

        manager.update_all(message.from_user.id, data["gender"], data["age"], data["weight"], data["height"], data["goal"])

        await state.clear()
        await message.answer(texts.updated_data_text, parse_mode="html", reply_markup=keyboards.main_menu)


#
# Changing user Gender:
#

@router.callback_query(F.data == "genderChange")
async def change_gender(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        
        await state.set_state(new_gender.gender)
        await bot.send_message(callback_query.from_user.id, "⚙️ Выберите пожалуйста ваш пол:", reply_markup=keyboards.gender_choice)
    else:
        await bot.send_message(callback_query.from_user.id, texts.incorrect_format_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router.message(new_gender.gender)
async def send_new_gender(message: Message, state: FSMContext):
    gender_female = True
    if message.text == "Мужской": gender_female = False

    await state.update_data(gender = gender_female)
    manager.update_option(message.from_user.id, "gender_female", gender_female)

    await message.answer(texts.updated_data_text, parse_mode="html", reply_markup=keyboards.main_menu)
    await state.clear()


#
# Changing user Age:
#

@router.callback_query(F.data == "ageChange")
async def change_age(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        
        await state.set_state(new_age.age)
        await bot.send_message(callback_query.from_user.id, "⚙️ Введите ваш возраст:", reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, texts.incorrect_format_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        
@router.message(new_age.age)
async def send_new_age(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)

    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

    else:
        await state.update_data(age = message.text)
        manager.update_option(message.from_user.id, "age", isNumberResult)

        await message.answer(texts.updated_data_text, parse_mode="html", reply_markup=keyboards.main_menu)
        await state.clear()


#
# Changing user Weight:
#

@router.callback_query(F.data == "weightChange")
async def change_weight(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        
        await state.set_state(new_weight.weight)
        await bot.send_message(callback_query.from_user.id, "⚙️ Введите ваш вес:", reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, texts.incorrect_format_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(new_weight.weight)
async def send_new_weight(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)

    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

    else:
        await state.update_data(weight = message.text)
        manager.update_option(message.from_user.id, "weight", isNumberResult)

        await message.answer(texts.updated_data_text, parse_mode="html", reply_markup=keyboards.main_menu)
        await state.clear()


#
# Changing user Height:
#

@router.callback_query(F.data == "heightChange")
async def change_height(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        
        await state.set_state(new_height.height)
        await bot.send_message(callback_query.from_user.id, "⚙️ Введите ваш рост:", reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, texts.incorrect_format_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router.message(new_height.height)
async def send_new_height(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)

    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()

    else:
        await state.update_data(height = message.text)
        manager.update_option(message.from_user.id, "height", isNumberResult)

        await message.answer(texts.updated_data_text, parse_mode="html", reply_markup=keyboards.main_menu)
        await state.clear()
        

#
# Changing user Height:
#

@router.callback_query(F.data == "goalChange")
async def change_goal(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if manager.user_exists(callback_query.from_user.id):
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        
        await state.set_state(new_goal.goal)
        await bot.send_message(callback_query.from_user.id, "⚙️ Выберите новую цель:", reply_markup=keyboards.goal_set)
    else:
        await bot.send_message(callback_query.from_user.id, texts.incorrect_format_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
        await state.clear()

@router.message(new_goal.goal)
async def send_new_goal(message: Message, state: FSMContext):
    if message.text == "Снижение веса" or message.text == "Набор веса" or message.text == "Удержание веса":
        await state.update_data(goal = message.text)
        manager.update_option(message.from_user.id, "goal", message.text)

        await message.answer(texts.updated_data_text, parse_mode="html", reply_markup=keyboards.main_menu)
        await state.clear()

    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())
        await state.clear()