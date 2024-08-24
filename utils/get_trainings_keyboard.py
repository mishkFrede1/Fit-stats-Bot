from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db_manager import Manager

manager = Manager()

def get_trainings_keyboard(user_id: int, mode="info", return_array=False, user_id_in_callback=False) -> InlineKeyboardMarkup: 
    trainings = manager.get_trainings(user_id)

    inline_keyboard = []

    if user_id_in_callback:
        for _, training in enumerate(trainings):
            t_time = training[4]
            hour = t_time.hour
            minute = t_time.minute
            if len(str(minute)) < 2: minute = f"0{minute}"

            button = InlineKeyboardButton(text=f"{training[8]} {hour}:{minute}", callback_data=f"{mode}_{training[6]}_{user_id}")
            inline_keyboard.append([button])
    else:
        for _, training in enumerate(trainings):
            t_time = training[4]
            hour = t_time.hour
            minute = t_time.minute
            if len(str(minute)) < 2: minute = f"0{minute}"

            button = InlineKeyboardButton(text=f"{training[8]} {hour}:{minute}", callback_data=f"{mode}_{training[6]}")
            inline_keyboard.append([button])

    if return_array:
        return inline_keyboard

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return keyboard
