from aiogram import Router, Bot, F
from aiogram.filters import Command 
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime

from data import keyboards, texts
from utils.is_number import isNumber
from db_manager import Manager

router = Router()
manager = Manager()

class user_reg(StatesGroup):
    gender = State()
    age = State()
    weight = State()
    height = State()
    goal = State()

#Запрос пола (через команду)
@router.message(Command("reg"))
async def genderCommand(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await message.answer(texts.repeated_registration_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.set_state(user_reg.gender)
        await message.answer("⚙️ Выберите пожалуйста ваш пол:", reply_markup=keyboards.gender_choice)

#Запрос пола (через inline кнопку)
@router.callback_query(F.data == "reg")
async def genderInline(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    if callback_query.data == "reg" and not manager.user_exists(callback_query.from_user.id):
        await state.set_state(user_reg.gender)
        await bot.send_message(callback_query.from_user.id, "⚙️ Выберите пожалуйста ваш пол:", reply_markup=keyboards.gender_choice)
    else:
        await bot.send_message(callback_query.from_user.id, texts.repeated_registration_error_text, parse_mode="html")
        await state.clear()

#Запрос возраста и запись пола в FSM
@router.message(user_reg.gender)
async def age(message: Message, state: FSMContext):
    gender_female = True
    if message.text == "Мужской" or message.text == "Женский": 
        if message.text == "Мужской": gender_female = False

        await state.update_data(gender = gender_female)
        await state.set_state(user_reg.age)
        await message.answer("⚙️ Сколько вам лет? Отправьте ответ ввиде одного <b>целого числа</b>.", parse_mode="html", reply_markup=ReplyKeyboardRemove())
        
    else:
        await message.answer(texts.registration_error_text, parse_mode="html")
        await state.clear()

#Запрос массы и запись возраста в FSM
@router.message(user_reg.age)
async def weight(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.registration_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.update_data(age = isNumberResult)

        await message.answer("⚙️ Какая ваша масса тела? Отправьте ответ в <b>килограммах</b>.", parse_mode="html")
        await state.set_state(user_reg.weight)

#Запрос роста и запись массы тела в FSM
@router.message(user_reg.weight)
async def height(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.registration_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.update_data(weight = isNumberResult)

        await state.set_state(user_reg.height)
        await message.answer("⚙️ Какой у вас полный рост? Отправьте ответ в <b>сантиметрах</b>.", parse_mode="html")

#Запись роста тела в FSM и отправка данных в БД
@router.message(user_reg.height)
async def goal(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)
    if isNumberResult == -1:
        await message.answer(texts.registration_error_text, parse_mode="html")
        await state.clear()
    else:
        await state.update_data(height = isNumberResult)

        await state.set_state(user_reg.goal)
        await message.answer("⚙️ Выберите направление:", parse_mode="html", reply_markup=keyboards.goal_set)

@router.message(user_reg.goal)
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
        await message.answer(texts.registration_error_text, parse_mode="html")
        await state.clear()

    if isRight:
        data = await state.get_data()

        now = datetime.now()
        date_strftime = now.strftime("%d.%m.%Y")

        manager.upload_registration_data(
            message.from_user.id, 
            date_strftime,
            message.from_user.first_name,
            message.from_user.username, 
            data["gender"], 
            data["age"], 
            data["weight"], 
            data["height"], 
            data["goal"]
        )

        await state.clear()
        await message.answer("⚙️ <b>Регистрация успешно завершена</b>.", parse_mode="html", reply_markup=keyboards.main_menu)