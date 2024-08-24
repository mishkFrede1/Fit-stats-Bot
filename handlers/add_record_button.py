from aiogram import Bot, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from datetime import datetime
from os import remove

from data import keyboards, texts
from db_manager import Manager


router = Router()
manager = Manager()

@router.message(F.text == "Добавить запись ✔️")
async def cancel(message: Message):
    if manager.user_exists(message.from_user.id):
        username = message.from_user.username
        if username == "": 
            username = None

        now = datetime.now()
        date_strftime = now.strftime("%d.%m.%Y")

        training_type = ""
        try:
            with open(f"note_training_type_{message.from_user.id}.txt") as file:
                training_type = file.read()
        except: training_type = None

        exercises = []
        try:
            with open(f"note_training_exercises_{message.from_user.id}.txt") as file:
                text = file.read()
                text = text.split(";")
                for i in text[0:len(text)-1]:
                    splited = i.split(", ")
                    exercises.append([splited[0], splited[1], splited[2]])
        except: exercises = None

        time_spent = 0
        try:
            with open(f"note_spent_time_{message.from_user.id}.txt") as file:
                time_spent = int(file.read())
        except: time_spent = None

        state_of_health = ""
        try:
            with open(f"note_health_{message.from_user.id}.txt") as file:
                state_of_health = file.read()
        except: state_of_health = None

        note = ""
        try:
            with open(f"note_comment_{message.from_user.id}.txt") as file:
                note = file.read()
        except: note = None

        burned_cal = ""
        try:
            with open(f"note_burned_calories_{message.from_user.id}.txt") as file:
                burned_cal = file.read()
        except: burned_cal = None

        gained_cal = ""
        try:
            with open(f"note_gained_calories_{message.from_user.id}.txt") as file:
                gained_cal = file.read()
        except: gained_cal = None

        sleep = 0
        try:
            with open(f"note_sleep_{message.from_user.id}.txt") as file:
                sleep = file.read()
        except: sleep = None

        measurements = []
        try:
            with open(f"note_measurement_{message.from_user.id}.txt") as file:
                text = file.read()
                text = text.split(";")
                text = set(text[0:len(text)-1])
                for i in text:
                    splited = i.split(", ")
                    measurements.append([splited[0], splited[1]])
        except: measurements = None

        if gained_cal == burned_cal == sleep == note == state_of_health == time_spent == exercises == training_type == measurements:
            await message.answer(texts.all_params_none_error_text, parse_mode="html", reply_markup=keyboards.records_settings)

        else:
            manager.upload_record(
                message.from_user.id,
                message.from_user.first_name,
                username,
                date_strftime,
                training_type,
                exercises,
                time_spent,
                state_of_health,
                note,
                burned_cal,
                gained_cal,
                measurements,
                sleep
            )

            names = ["training_type", "training_exercises", "spent_time", "health", "comment", "gained_calories", "burned_calories", "measurement", "sleep"]
            for name in names:
                try:
                    remove(f'note_{name}_{message.from_user.id}.txt')
                except: pass
        
            await message.answer("✔️ <b>Запись создана</b>.", reply_markup=keyboards.records_settings, parse_mode="html")
        
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())