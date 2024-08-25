from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
import json

from data import keyboards, texts
from db_manager import Manager
from utils.get_friends_keyboard import get_friends_keyboard

router = Router()
manager = Manager()

@router.message(F.text == "Личный кабинет 👤")
async def account_settings(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас настройки аккаунта:", reply_markup=keyboards.account_settings)
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("acc"))
async def account_settings_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас настройки аккаунта:", reply_markup=keyboards.account_settings)
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Расписание тренировок 🗓")
async def schedule(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас настройки расписания:", reply_markup=keyboards.schedule_settings)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("sched"))
async def schedule_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас настройки расписания:", reply_markup=keyboards.schedule_settings)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())



@router.message(F.text == "Запись наблюдений ✏️")
async def recording_menu(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Меню записей:", reply_markup=keyboards.records_settings)
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("rec"))
async def recording_menu_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Меню записей:", reply_markup=keyboards.records_settings)
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())


@router.message(Command("about"))
async def about_command(message: Message):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

        bot_version = config["bot_version"]
        github = config["github"]

        telegram = config["creator"]["telegram_link"]
        vk = config["creator"]["vk_link"]
        await message.answer(texts.bot_info_text.format(bot_version=bot_version, github=github, telegram=telegram, vk=vk), parse_mode="html", disable_web_page_preview=True)

@router.message(F.text == "О боте ℹ️")
async def about(message: Message):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

        bot_version = config["bot_version"]
        github = config["github"]

        telegram = config["creator"]["telegram_link"]
        vk = config["creator"]["vk_link"]
        await message.answer(texts.bot_info_text.format(bot_version=bot_version, github=github, telegram=telegram, vk=vk), parse_mode="html", disable_web_page_preview=True)


async def friends_text_send(message: Message):
    if manager.user_exists(message.from_user.id):
        friends = manager.get_user_data(message.from_user.id)[11]
        if friends == None:
            await message.answer("⚙️ <b>У вас ещё нет друзей. Вам следует их добавить.</b>", parse_mode="html", reply_markup=keyboards.friends)
        else:
            await message.answer("👥 Выберите интересующие вас действия:", parse_mode="html", reply_markup=keyboards.friends)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("friends"))
async def friends_command(message: Message):
    await friends_text_send(message)

@router.message(F.text == "Друзья 👥")
async def friends(message: Message):
    await friends_text_send(message)

@router.message(F.text == "Список друзей 👥")
async def friends_list_button(message: Message):
    if manager.user_exists(message.from_user.id):
        friends = manager.get_user_data(message.from_user.id)[11]
        if friends == None:
            await message.answer("⚙️ <b>У вас ещё нет друзей. Вам следует их добавить.</b>", parse_mode="html")
        else:
            await message.answer("📑 <b>Список друзей</b>:", parse_mode="html", reply_markup=get_friends_keyboard(friends))
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Прогресс и Статистика 📈")
async def stats(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас настройки:", reply_markup=keyboards.stats)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(Command("stats"))
async def stats_command(message: Message):
    if manager.user_exists(message.from_user.id):
        await message.answer("⚙️ Выберите интересующие вас настройки:", reply_markup=keyboards.stats)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())