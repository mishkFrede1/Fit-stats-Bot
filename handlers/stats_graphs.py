from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from data import keyboards, texts
from db_manager import Manager
from utils import graphs_functions


router = Router()
manager = Manager()

@router.message(F.text == "Качество сна 🛌")
async def sleep_quality_stats(message: Message, bot: Bot):
    if manager.user_exists(message.from_user.id):
        await graphs_functions.sleep_quality_graph(message.from_user.id, bot, message.from_user.id)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(F.text == "Калории 🥪")
async def calories_stats(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ <b>Выберите тип графика</b>:", parse_mode="html", reply_markup=keyboards.calories_stats_types)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data.startswith("stats_"))
async def calories_types_stats(callback_query: CallbackQuery, bot: Bot):
    type = callback_query.data.split("_")[1]
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if type == "gained":
        await graphs_functions.calories_gained_graph(callback_query.from_user.id, bot, callback_query.from_user.id)
    else:
        await graphs_functions.calories_burned_graph(callback_query.from_user.id, bot, callback_query.from_user.id)

#Измерения 📏
@router.message(F.text == "Измерения 📏")
async def measurements_stats(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ <b>Выберите тип измерения</b>:", parse_mode="html", reply_markup=keyboards.measurement_stats_types)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data.startswith("measure_stat_"))
async def measurements_types_stats(callback_query: CallbackQuery, bot: Bot):
    type = callback_query.data.split("_")[2]
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await graphs_functions.measurement_graph(callback_query.from_user.id, bot, callback_query.from_user.id, type)