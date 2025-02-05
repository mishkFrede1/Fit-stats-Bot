from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command

from data import keyboards, texts
from db_manager import Manager
from utils.get_age_ending import getAgeEnding

router = Router()
manager = Manager()

@router.message(F.text == "Изменить персональные данные ⚙️")
async def account_delete(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите необходимые настройки для изменения:", parse_mode="html", reply_markup=keyboards.change_account)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("change"))
async def account_delete_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите необходимые настройки для изменения:", parse_mode="html", reply_markup=keyboards.change_account)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())




@router.message(F.text == "Удалить аккаунт ❌")
async def account_delete(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Вы уверены что хотите удалить ваш текущий аккаунт? <b>Все ваши данные будут утерянны.</b>", parse_mode="html", reply_markup=keyboards.delete_account)
    else:
        await message.answer(texts.unregistered_acces_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("del"))
async def account_delete_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Вы уверены что хотите удалить ваш текущий аккаунт? <b>Все ваши данные будут утерянны.</b>", parse_mode="html", reply_markup=keyboards.delete_account)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())




@router.callback_query(F.data == "YesDeleteAcc")
async def delete_confirmation_yes(callback_query: CallbackQuery, bot: Bot):
    if callback_query.data == "YesDeleteAcc" and manager.user_exists(callback_query.from_user.id):
        manager.delete_user(callback_query.from_user.id)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, "✔️ <b>Аккаунт удален</b>.", parse_mode="html", reply_markup=ReplyKeyboardRemove())

    else:
        await bot.send_message(callback_query.from_user.id, texts.delete_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data == "NoDeleteAcc")
async def delete_confirmation_no(callback_query: CallbackQuery, bot: Bot):
    if callback_query.data == "NoDeleteAcc":
        await bot.edit_message_text("❌ <b>Удаление отменено</b>.", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, parse_mode="html")

    else:
        await bot.send_message(callback_query.from_user.id, texts.delete_error_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())




@router.message(F.text == "Мои данные 📋")
async def account_info(message: Message):
    if manager.user_exists(message.from_user.id):
        data = manager.get_user_data(message.from_user.id) 
        
        day, month, year = data[1].day, data[1].month, data[1].year
        if len(str(month)) < 2: month = f"0{month}"

        date = f"{day}.{month}.{year}"
        gender_female = data[4]
        age = data[5]
        height = data[6]
        weight = data[7]
        goal = data[8]
        
        gender = "Мужской"
        if gender_female: gender = "Женский"

        ending = getAgeEnding(age)
        age_str = str(age) + " " + ending

        await message.answer(texts.user_info_text.format(
            id=message.from_user.id, 
            date=date, 
            gender=gender, 
            age=age_str, 
            weight=weight, 
            height=height, 
            goal=goal
        ), parse_mode="html")
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("info"))
async def account_info(message: Message):
    if manager.user_exists(message.from_user.id):
        data = manager.get_user_data(message.from_user.id) 
        day, month, year = data[1].day, data[1].month, data[1].year

        date = f"{day}.{month}.{year}"
        gender_female = data[4]
        age = data[5]
        height = data[6]
        weight = data[7]
        goal = data[8]
        
        gender = "Мужской"
        if gender_female: gender = "Женский"

        ending = getAgeEnding(age)
        age_str = str(age) + " " + ending

        await message.answer(texts.user_info_text.format(
            id=message.from_user.id, 
            date=date, 
            gender=gender, 
            age=age_str, 
            weight=weight, 
            height=height, 
            goal=goal
        ), parse_mode="html")
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())