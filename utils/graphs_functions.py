from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import os
from numpy import isnan

from data import keyboards
from db_manager import Manager
from utils.get_time_ending import getTimeEndingHour
from data.graphs_text import sleep_texts, cal_gained_texts, cal_burned_texts

router = Router()
manager = Manager()

def sleep_category(age: int) -> int:
    if age <= 13:
        return 11
    elif 14 <= age <= 17:
        return 10
    elif 18 <= age <= 25:
        return 9
    elif age >= 65:
        return 8
    
def date_num_in_text(num: int) -> str:
    if num < 10:
        return f"0{num}"
    else: return str(num)

def std(array: list, mean: int) -> int:
    std = 0
    for i in array:
        std += (i - mean)**2
    std = (std/(len(array)-1))**0.5

    return round(std, 2)

def get_last_measure(df: pd.DataFrame, option: str) -> int:
    new_df = df
    for _ in new_df:
        el = new_df.tail(1)["measurements"].item()
        if el != None:
            for j in el:
                if j[0] == f"{option}":
                    return int(j[1])
            new_df = new_df.head(new_df.shape[0]-1)
        else:
            new_df = new_df.head(new_df.shape[0]-1)

def mifflin_coef(gender_female: bool, weight: int, height: int, age: int, coef: float) -> float:
    if gender_female:
        return round((10*weight + 6.25*height - 5*age - 161) * coef)
    else:
        return round((10*weight + 6.25*height - 5*age + 5) * coef)

async def sleep_quality_graph(sender_id: int, bot: Bot, user_id: int, keyboard=True, edit_message=False, message_id=None, texts_type="user", show_back=False):
    user = manager.get_user_data(user_id)
    age = user[5]

    conn = manager.get_connection_from_pool()
    df = pd.read_sql_query(f"SELECT date, sleep FROM records WHERE user_id = {user_id}", conn)
    manager.release_db_connection(conn)

    if df['date'].nunique(dropna=True) < 2:
        back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
        if edit_message:
            await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
        else:
            if show_back:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
            else:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")

    else:
        df['date'] = pd.to_datetime(df['date'])

        mean_sleep_hours = round(df['sleep'].aggregate(['mean']).iloc[0], 1)
        if isnan(mean_sleep_hours):
            back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
            if edit_message:
                await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
            else:
                if show_back:
                    await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
                else:
                    await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")
        else:
            if isinstance(mean_sleep_hours, float):
                mean_sleep_hours_ending = getTimeEndingHour(int(str(mean_sleep_hours)[len(str(mean_sleep_hours))-1]))
            else: mean_sleep_hours_ending = getTimeEndingHour(mean_sleep_hours)

            recommended_sleep = sleep_category(age)
            recommended_sleep_ending = getTimeEndingHour(recommended_sleep)

            first_date = df['date'].agg(["min"]).iloc[0]
            first_date = f"{date_num_in_text(first_date.day)}.{date_num_in_text(first_date.month)}.{first_date.year}"
            last_date = df['date'].agg(["max"]).iloc[0]
            last_date = f"{date_num_in_text(last_date.day)}.{date_num_in_text(last_date.month)}.{last_date.year}"

            df = df.tail(30)
            df = df.sort_values(by="date")
            rec_std = std(list(df.sleep), recommended_sleep)

            text = ""
            avg_hour_text = sleep_texts[texts_type]["avg_hour_text"].format(first_date=first_date, last_date=last_date, mean_sleep_hours=mean_sleep_hours, mean_sleep_hours_ending=mean_sleep_hours_ending)
            rec_std_text = sleep_texts[texts_type]["rec_std_text"].format(rec_std=rec_std)

            if recommended_sleep-1 <= mean_sleep_hours and rec_std < 1:
                text += sleep_texts[texts_type]["good_sleep_quality"]
                text += avg_hour_text
                text += sleep_texts[texts_type]["good_std"].format(rec_std=rec_std)
                text += sleep_texts[texts_type]["good_indicator"]
                mean_line_color = "#00D907"

            elif mean_sleep_hours <= recommended_sleep-3:
                text += sleep_texts[texts_type]["bad_sleep_quality"]
                text += avg_hour_text
                text += sleep_texts[texts_type]["bad_value"].format(recommended_sleep=recommended_sleep, recommended_sleep_ending=recommended_sleep_ending)
                if rec_std > 1: 
                    text += rec_std_text
                text += sleep_texts[texts_type]["bad_problems"]
                mean_line_color = "#DC143C"

            else:
                text += sleep_texts[texts_type]["med_sleep_problems"]
                text += avg_hour_text
                if mean_sleep_hours < recommended_sleep-2:
                    text += sleep_texts[texts_type]["med_value"].format(recommended_sleep=recommended_sleep, recommended_sleep_ending=recommended_sleep_ending)
                if rec_std > 1: 
                    text += rec_std_text
                    text += sleep_texts[texts_type]["med_problem_stable"]
                else:
                    text += sleep_texts[texts_type]["med_problem_more"]
                mean_line_color = "#ECDB0C"


            plt.figure(figsize=(10, 6))
            plt.plot(df['date'], df['sleep'], marker='o', label='Продолжительность сна в часах')
            plt.axhline(mean_sleep_hours, linestyle='--', label=f"Среднее количество сна: {mean_sleep_hours} {mean_sleep_hours_ending}", linewidth=2, color=mean_line_color)
            plt.axhline(recommended_sleep, linestyle="--", label=f"Необходимое количество сна: {recommended_sleep} {recommended_sleep_ending}", linewidth=2, color="g")

            plt.gca().yaxis.set_major_locator(MultipleLocator(1))
            #plt.xticks(rotation=-45, ha='left')
            plt.title('Анализ качества сна')
            plt.xlabel('Дни')
            plt.ylabel('Продолжительность сна (часы)')
            plt.legend(loc='lower left')
            plt.tight_layout()
            plt.grid(True)
            plt.savefig(f'sleep_stats_{sender_id}.png')
            if edit_message:
                await bot.edit_message_text(sleep_texts[texts_type]["graph_message_text"], sender_id, message_id, parse_mode="html")
            else:
                await bot.send_message(sender_id, sleep_texts[texts_type]["graph_message_text"], parse_mode="html")

            if keyboard:
                await bot.send_photo(sender_id, FSInputFile(f'sleep_stats_{sender_id}.png'), caption=text, parse_mode="html", reply_markup=keyboards.stats)
            else:
                back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}_delete")]])
                await bot.send_photo(sender_id, FSInputFile(f'sleep_stats_{sender_id}.png'), caption=text, parse_mode="html", reply_markup=back_button)

            os.remove(f'sleep_stats_{sender_id}.png')

async def calories_gained_graph(sender_id: int, bot: Bot, user_id: int, keyboard=True, edit_message=False, message_id=None, texts_type="user", show_back=False):
    user = manager.get_user_data(user_id)
    trainings = manager.get_trainings(user_id)

    conn = manager.get_connection_from_pool()
    df = pd.read_sql_query(f"SELECT date, gained_cal, measurements FROM records WHERE user_id = {user_id}", conn)
    manager.release_db_connection(conn)

    if df['date'].nunique(dropna=True) < 2:
        back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
        if edit_message:
            await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
        else:
            if show_back:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
            else:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")
    else:
        df['date'] = pd.to_datetime(df['date'])

        first_date = df['date'].agg(["min"]).iloc[0]
        first_date = f"{date_num_in_text(first_date.day)}.{date_num_in_text(first_date.month)}.{first_date.year}"
        last_date = df['date'].agg(["max"]).iloc[0]
        last_date = f"{date_num_in_text(last_date.day)}.{date_num_in_text(last_date.month)}.{last_date.year}"

        df = df.tail(30)
        df = df.sort_values(by="date")

        mean_cal = round(df["gained_cal"].agg(["mean"]).item(), 1)
        if isnan(mean_cal):
            back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
            if edit_message:
                await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
            else:
                if show_back:
                    await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
                else:
                    await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")
        else:
            weight = get_last_measure(df, "weight")
            if weight == None:
                weight = user[7]

            height = get_last_measure(df, "height")
            if height == None:
                height = user[6]

            gender_female = user[4]
            age = user[5]
            goal = user[8]

            counts = {
                "Силовая тренировка ": 0,
                "Кардио тренировка ": 0,
                "Гибкость и растяжка": 0
            }
            for i in trainings:
                counts[i[5]] += 1
            type = max(counts)
            if type == "Силовая тренировка ":
                coef = 2
            elif type == "Кардио тренировка ":
                coef = 1.55
            else:
                coef = 1.375

            mifflin = mifflin_coef(gender_female, weight, height, age, coef)

            mean_line_color = "#00D907"
            text = ""
            if goal == "Набор веса":
                mifflin += 500
                if mean_cal >= mifflin-150:
                    text += cal_gained_texts[texts_type]["good_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_gained_texts[texts_type]["weight_up_good"] 
                else:
                    text += cal_gained_texts[texts_type]["bad_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal) 
                    text += cal_gained_texts[texts_type]["bad_weight_up"] 
                    text += cal_gained_texts[texts_type]["weight_up_recom"].format(mifflin=mifflin)
                    mean_line_color = "#DC143C"

            elif goal == "Снижение веса":
                mifflin -= 500
                if mean_cal <= mifflin-150:
                    text += cal_gained_texts[texts_type]["good_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal) 
                    text += cal_gained_texts[texts_type]["weight_loss_good"]
                else:
                    text += cal_gained_texts[texts_type]["more_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal) 
                    text += cal_gained_texts[texts_type]["bad_more_gained"]
                    text += cal_gained_texts[texts_type]["weight_loss_recom"].format(mifflin=mifflin)
                    mean_line_color = "#DC143C"

            else:
                if mifflin - 200  <= mean_cal <= mifflin + 200:
                    text += cal_gained_texts[texts_type]["good_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal) 
                    text += cal_gained_texts[texts_type]["weight_hold_good"]
                elif mean_cal >= mifflin + 200:
                    text += cal_gained_texts[texts_type]["more_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_gained_texts[texts_type]["bad_more_weight_hold"]
                    text += cal_gained_texts[texts_type]["weight_hold_loss_recom"].format(mifflin=mifflin)
                    mean_line_color = "#DC143C"
                elif mean_cal <= mifflin - 200:
                    text += cal_gained_texts[texts_type]["bad_cal_gained"]
                    text += cal_gained_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_gained_texts[texts_type]["bad_small_weight_hold"]
                    text += cal_gained_texts[texts_type]["weight_hold_more_recom"].format(mifflin=mifflin)
                    mean_line_color = "#DC143C"

            plt.figure(figsize=(10, 6))
            plt.plot(df['date'], df['gained_cal'], marker='o', label='Набранные калории')
            plt.axhline(mean_cal, linestyle='--', label=f"Среднее суточное потребление: {mean_cal} ккал", linewidth=2, color=mean_line_color)
            plt.axhline(mifflin, linestyle='--', label=f"Необходимое суточное потребление: {mifflin} ккал", linewidth=2, color="g")

            plt.title('Анализ набранных калорий')
            plt.xlabel('Дни')
            plt.ylabel('Килокалории')
            plt.legend(loc='lower left')
            plt.tight_layout()
            plt.grid(True)
            plt.savefig(f'gained_cal_stats_{sender_id}.png')

            if edit_message: 
                await bot.edit_message_text("📈 <b>График набранных калорий</b>:", sender_id, message_id, parse_mode="html")
            else:
                await bot.send_message(sender_id, "📈 <b>График набранных калорий</b>:", parse_mode="html")

            if keyboard:
                await bot.send_photo(sender_id, FSInputFile(f'gained_cal_stats_{sender_id}.png'), caption=text, parse_mode="html", reply_markup=keyboards.stats)
            else:
                back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}_delete")]])
                await bot.send_photo(sender_id, FSInputFile(f'gained_cal_stats_{sender_id}.png'), caption=text, parse_mode="html", reply_markup=back_button)

            os.remove(f'gained_cal_stats_{sender_id}.png')


async def calories_burned_graph(sender_id: int, bot: Bot, user_id: int, keyboard=True, edit_message = False, message_id = None, texts_type="user", show_back=False):
    user = manager.get_user_data(user_id)

    conn = manager.get_connection_from_pool()
    df = pd.read_sql_query(f"SELECT date, burned_cal, measurements FROM records WHERE user_id = {user_id}", conn)
    manager.release_db_connection(conn)

    if df['date'].nunique(dropna=True) < 2:
        back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
        if edit_message:
            await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
        else:
            if show_back:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
            else:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")
    else:
        df['date'] = pd.to_datetime(df['date'])

        first_date = df['date'].agg(["min"]).iloc[0]
        first_date = f"{date_num_in_text(first_date.day)}.{date_num_in_text(first_date.month)}.{first_date.year}"
        last_date = df['date'].agg(["max"]).iloc[0]
        last_date = f"{date_num_in_text(last_date.day)}.{date_num_in_text(last_date.month)}.{last_date.year}"

        df = df.tail(30)
        df = df.sort_values(by="date")

        mean_line_color = "#00D907"
        mean_cal = round(df["burned_cal"].agg(["mean"]).item(), 1)
        if isnan(mean_cal):
            back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
            if edit_message:
                await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
            else:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
        else:
            goal = user[8]
    
            text = ""
            if goal == "Набор веса":
                if mean_cal < 300:
                    text += cal_burned_texts[texts_type]["good_burned"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["good_val_weight_up"]
                else:
                    mean_line_color = "#DC143C"
                    text += cal_burned_texts[texts_type]["bad_weight_up_more"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["val_loss_weight_up"]

            elif goal == "Снижение веса":
                if mean_cal > 500:
                    text += cal_burned_texts[texts_type]["good_burned"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["good_val_weight_loss"]
                else:
                    mean_line_color = "#DC143C"
                    text += cal_burned_texts[texts_type]["bad_loss_weight_loss_"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["val_more_weight_loss"]
    
            else:
                if 300 <= mean_cal <= 500:
                    text += cal_burned_texts[texts_type]["good_burned"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["good_val_weight_hold"]
                elif mean_cal > 500:
                    mean_line_color = "#DC143C"
                    text += cal_burned_texts[texts_type]["more_weight_hold_burned"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["val_loss_weight_hold"]
                elif mean_cal < 300:
                    mean_line_color = "#DC143C"
                    text += cal_burned_texts[texts_type]["loss_weight_hold"]
                    text += cal_burned_texts[texts_type]["mean_cal"].format(mean_cal=mean_cal)
                    text += cal_burned_texts[texts_type]["val_more_weight_hold"]

            plt.figure(figsize=(10, 6))
            plt.plot(df['date'], df['burned_cal'], marker='o', label='Сожженные калории')
            plt.axhline(mean_cal, linestyle='--', label=f"Среднее суточное количество: {mean_cal} ккал", linewidth=2, color=mean_line_color)

            plt.title('Анализ сожженных калорий')
            plt.xlabel('Дни')
            plt.ylabel('Килокалории')
            plt.legend(loc='lower left')
            plt.tight_layout()
            plt.grid(True)
            plt.savefig(f'burned_cal_stats_{sender_id}.png')

            if edit_message:
                await bot.edit_message_text("📉 <b>График сожженных калорий</b>:", sender_id, message_id, parse_mode="html")
            else:
                await bot.send_message(sender_id, "📉 <b>График сожженных калорий</b>:", parse_mode="html")

            if keyboard:
                await bot.send_photo(sender_id, FSInputFile(f'burned_cal_stats_{sender_id}.png'), caption=text, parse_mode="html", reply_markup=keyboards.stats)
            else:
                back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}_delete")]])
                await bot.send_photo(sender_id, FSInputFile(f'burned_cal_stats_{sender_id}.png'), caption=text, parse_mode="html", reply_markup=back_button)

            os.remove(f'burned_cal_stats_{sender_id}.png')


def get_measure_records(df: pd.DataFrame, option: str) -> int:
    result = []
    for i, el in enumerate(df["measurements"]):
        if el != None:
            for j in el:
                if j[0] == f"{option}":
                    result.append(tuple([i, int(j[1])]))
    return result

measure_type_names = {
    "weight": ["Вес", "веса", "Вес (кг.)"],
    "height": ["Рост", "роста", "Рост (см.)"],
    "neck": ["Обхват шеи", "обхвата шеи", "Обхват шеи (см.)"],
    "chest": ["Обхват груди", "обхвата груди", "Обхват груди (см.)"],
    "weist": ["Обхват талии", "обхвата талии", "Обхват талии (см.)"],
    "hips": ["Обхват бедер", "обхвата бедер", "Обхват бедер (см.)"],
    "biceps": ["Обхват бицепса", "обхвата бицепса", "Обхват бицепса (см.)"],
    "calf": ["Обхват икр", "обхвата икр", "Обхват икр (см.)"]
}

async def measurement_graph(sender_id: int, bot: Bot, user_id: int, measure_type: str, keyboard=True, edit_message=False, message_id=None, show_back=False):
    conn = manager.get_connection_from_pool()
    df = pd.read_sql_query(f"SELECT date, measurements FROM records WHERE user_id = {user_id}", conn)
    manager.release_db_connection(conn)

    if df['date'].nunique() < 2:
        back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
        if edit_message:
            await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
        else:
            if show_back:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
            else:
                await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")
    else:
        df['date'] = pd.to_datetime(df['date'])

        first_date = df['date'].agg(["min"]).iloc[0]
        first_date = f"{date_num_in_text(first_date.day)}.{date_num_in_text(first_date.month)}.{first_date.year}"
        last_date = df['date'].agg(["max"]).iloc[0]
        last_date = f"{date_num_in_text(last_date.day)}.{date_num_in_text(last_date.month)}.{last_date.year}"

        df = df.tail(30)
        df = df.sort_values(by="date")

        weights = get_measure_records(df, f"{measure_type}")
        if len(weights) > 0:
            dates = []
            weight_nums = []
            for i in weights:
                dates.append(df["date"].iloc[i[0]])
                weight_nums.append(int(i[1]))

            mean = sum(weight_nums) / len(weight_nums)
            names = measure_type_names[measure_type]

            plt.figure(figsize=(10, 6))
            plt.plot(dates, weight_nums, marker='o', label=f'{names[0]}')
            plt.axhline(mean, linestyle='--', label=f"Среднее значение {names[1]}", linewidth=2, color="#0C88E4")

            plt.title(f'График {names[1]}')
            plt.xlabel('Дни')
            plt.ylabel(f'{names[2]}')
            plt.legend(loc='lower left')
            plt.tight_layout()
            plt.grid(True)
            plt.savefig(f'measure_{measure_type}_stats_{sender_id}.png')
            if edit_message:
                await bot.edit_message_text(f"📈 <b>График {names[1]}</b>:", sender_id, message_id, parse_mode="html")
            else:
                await bot.send_message(sender_id, f"📈 <b>График {names[1]}</b>:", parse_mode="html")
            if keyboard:
                await bot.send_photo(sender_id, FSInputFile(f'measure_{measure_type}_stats_{sender_id}.png'))
            else:
                back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}_delete")]])
                await bot.send_photo(sender_id, FSInputFile(f'measure_{measure_type}_stats_{sender_id}.png'), reply_markup=back_button)

            os.remove(f'measure_{measure_type}_stats_{sender_id}.png')

        else:
            back_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад ⬅️", callback_data=f"friend_back_{user_id}")]])
            if edit_message:
                await bot.edit_message_text("❌ <b>Недостаточно записей</b>.", sender_id, message_id, parse_mode="html", reply_markup=back_button)
            else:
                if show_back:
                    await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html", reply_markup=back_button)
                else:
                    await bot.send_message(sender_id, "❌ <b>Недостаточно записей</b>.", parse_mode="html")