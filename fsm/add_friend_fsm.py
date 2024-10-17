from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import keyboards, texts
from db_manager import Manager
from utils.is_number import isNumber

class new_friend(StatesGroup):
    type_of_find = State()
    friend_id = State()

router = Router()
manager = Manager()

@router.message(F.text == "Добавить друга ➕")
async def get_friend_find_type(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(new_friend.type_of_find)
        await message.answer("⚙️ <b>Выберите тип поиска</b>:", parse_mode="html", reply_markup=keyboards.friend_find_types)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.callback_query(F.data.startswith("friend_find_"))
async def get_friend_id(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(new_friend.friend_id)
    if callback_query.data.split("_")[2] == "id":
        await state.update_data(type = "id")
        await bot.send_message(callback_query.from_user.id, "⚙️ <b>Введите ID друга</b>:", parse_mode="html")
    else:
        await state.update_data(type = "nick")
        await bot.send_message(callback_query.from_user.id, "⚙️ <b>Введите никнейм друга</b>:", parse_mode="html")

@router.message(new_friend.friend_id)
async def send_friend(message: Message, state: FSMContext):
    data = await state.get_data()
    type = data["type"]
    friend_list = manager.get_user_data(message.from_user.id)[11]
    if friend_list == None: friend_list = []

    isNumberResult = isNumber(message.text)
    if type == "id" and isNumberResult != -1:
        if isNumberResult == message.from_user.id:
            await message.answer(texts.self_add_friend_list, parse_mode="html", reply_markup=keyboards.friends)

        elif not manager.user_exists(isNumberResult):
            await message.answer(texts.user_is_not_exist, parse_mode="html", reply_markup=keyboards.friends)

        else:
            friend_list.append(isNumberResult)
            manager.upload_friend_list(message.from_user.id, list(set(friend_list)))

            for id in friend_list:
                f_list = manager.get_user_data(id)[11]
                if f_list == None: f_list = []

                f_list.append(message.from_user.id)
                manager.upload_friend_list(id, list(set(f_list)))

            await message.answer("✔️ <b>Друг успешно добавлен</b>.", parse_mode="html", reply_markup=keyboards.friends)

    elif type == "nick":
        username = message.text
        if '@' == message.text[0]:
            username = message.text[1:]

        friend = manager.get_user_data_by_username(username)

        if friend == None:
            await message.answer(texts.user_is_not_exist, parse_mode="html", reply_markup=keyboards.friends)
        else: 
            friend_id = friend[0]

            if message.from_user.id == friend_id:
                await message.answer(texts.self_add_friend_list, parse_mode="html", reply_markup=keyboards.friends)
            else:
                friend_list.append(friend_id)
                manager.upload_friend_list(message.from_user.id, list(set(friend_list)))

                for id in friend_list:
                    f_list = manager.get_user_data(id)[11]
                    if f_list == None: f_list = []

                    f_list.append(message.from_user.id)
                    manager.upload_friend_list(id, list(set(f_list)))

                await message.answer("✔️ <b>Друг успешно добавлен</b>.", parse_mode="html", reply_markup=keyboards.friends)
    else:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html", reply_markup=keyboards.friends)

    await state.clear()