from db_manager import Manager
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

manager = Manager()

def get_friends_keyboard(friends_list: list[int]) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for i in friends_list:
        friend = manager.get_user_data(i)
        if friend != None:
            inline_keyboard.append([InlineKeyboardButton(text=f"{friend[2]}", callback_data=f"friend_info_{i}")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)