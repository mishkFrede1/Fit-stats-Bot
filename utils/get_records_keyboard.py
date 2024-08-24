from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date
# import psycopg2

def get_records_list_keyboard(
        records: list, 
        id=0, 
        buttons_on=True, 
        mode="records_info",
        user_id_in_mode="False",
        type="not-filtered", 
        arrow_buttons_text="records_list", 
        id_in_arrow_buttons="False",
        back_button=False, 
        back_button_data="backto_records",
        id_in_back_button_data="False",
        finder_data="records_find_list"
    ) -> InlineKeyboardMarkup: 

    inline_keyboard = []

    if type == "not-filtered":
        for record in records:
            record_id = record[3]
            record_date = record[4]

            day = record_date.day
            month = record_date.month
            year = record_date.year

            if len(str(month)) < 2: month = f"0{month}"
            if len(str(day)) < 2: day = f"0{day}"

            if user_id_in_mode == "False":
                button = InlineKeyboardButton(text=f"{day}.{month}.{year}", callback_data=f"{mode}_{record_id}")
            else:
                button = InlineKeyboardButton(text=f"{day}.{month}.{year}", callback_data=f"{mode}_{record_id}_{user_id_in_mode}")

            inline_keyboard.append([button])

    elif type == "filtered" or type == "filtered-str":
        if type == "filtered-str": 
            array = records
        else: 
            array = records[0]

        for record in array:
            data = record.split(",")
            filtered_record_id = data[3]
            filtered_record_date = data[4].split("-")
            filtered_record_date = date(int(filtered_record_date[0]), int(filtered_record_date[1]), int(filtered_record_date[2]))

            day = filtered_record_date.day
            month = filtered_record_date.month
            year = filtered_record_date.year

            if len(str(month)) < 2: month = f"0{month}"
            if len(str(day)) < 2: day = f"0{day}"

            if user_id_in_mode == "False":
                button = InlineKeyboardButton(text=f"{day}.{month}.{year}", callback_data=f"{mode}_{filtered_record_id}")
            else:
                button = InlineKeyboardButton(text=f"{day}.{month}.{year}", callback_data=f"{mode}_{filtered_record_id}_{user_id_in_mode}")
            inline_keyboard.append([button])

    
    if buttons_on and id_in_arrow_buttons == "False":
        inline_keyboard.append([InlineKeyboardButton(text="⬅️", callback_data=f"{arrow_buttons_text}_left_{id}"), InlineKeyboardButton(text="Поиск 🔍", callback_data=f"{finder_data}"), InlineKeyboardButton(text="➡️", callback_data=f"{arrow_buttons_text}_right_{id}")])
    elif buttons_on:
        inline_keyboard.append([InlineKeyboardButton(text="⬅️", callback_data=f"{arrow_buttons_text}_left_{id}_{id_in_arrow_buttons}"), InlineKeyboardButton(text="Поиск 🔍", callback_data=f"{finder_data}"), InlineKeyboardButton(text="➡️", callback_data=f"{arrow_buttons_text}_right_{id}_{id_in_arrow_buttons}")])

    if back_button and id_in_back_button_data != "False":
        inline_keyboard.append([InlineKeyboardButton(text="Назад ↩️", callback_data=f"{back_button_data}_{id_in_back_button_data}")])
    elif back_button:
        inline_keyboard.append([InlineKeyboardButton(text="Назад ↩️", callback_data=f"{back_button_data}")])

    list_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return list_keyboard



# def get_records(user_id: int):
#     try:
#         conn = psycopg2.connect(user='postgres', password='1707', database='accounts', host='127.0.0.1')
#         conn.autocommit = True

#         with conn.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT * FROM records WHERE user_id = %s
#                 """, 
#                 (user_id,)
#             )
#             data = cursor.fetchall()
#             return(data)

#     except Exception as _ex:
#         print("[INFO]", _ex)

#     finally:
#         conn.close()

# def get_records_keyboard(user_id: int, mode="records_info") -> InlineKeyboardMarkup: 
#     records = get_records(user_id)

#     inline_keyboard = []

#     for record in records:
#         record_id = record[3]
#         date = record[4]

#     for _, record in enumerate(records):
#         record_id = record[3]
#         date = record[4]

#         day = date.day
#         month = date.month
#         year = date.year

#         if len(str(month)) < 2: month = f"0{month}"
#         if len(str(day)) < 2: day = f"0{day}"

#         button = InlineKeyboardButton(text=f"{day}.{month}.{year}", callback_data=f"{mode}_{record_id}")
#         inline_keyboard.append([button])

#     keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

#     return keyboard
