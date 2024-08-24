from db_manager import Manager
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

manager = Manager()

def get_friends_keyboard(friends_list: list[int]) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in friends_list:
        inline_keyboard.append([InlineKeyboardButton(text=f"{manager.get_user_data(i)[2]}", callback_data=f"friend_info_{i}")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)