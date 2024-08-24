from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from os import remove
from datetime import time
from utils.scheduler import scheduler

from data import keyboards, texts
from db_manager import Manager
from utils.send_reminder import send_reminder
from utils.get_days_str import get_days_str


router = Router()
manager = Manager()

@router.message(F.text == "Подтвердить ✔️")
async def accept(message: Message, bot: Bot):
    if manager.user_exists(message.from_user.id):
        try:
            with open(f'training_{message.from_user.id}.txt', 'r') as file:
                days = file.read()
                
                days = days.split(", ")
                days = list(set(days[0:len(days)-1]))

            with open(f't_time_{message.from_user.id}.txt', 'r') as file:
                t_time = file.read()
                
                t_time = t_time.split(":")
                hour = int(t_time[0])
                minute = int(t_time[1])

                t_time = time(int(t_time[0]), int(t_time[1]))

            with open(f'training_type_{message.from_user.id}.txt', 'r') as file:
                training_type = file.read()
            with open(f'training_name_{message.from_user.id}.txt', 'r') as file:
                training_name = file.read()
            
            exercises = []
            try:
                with open(f'exercises_{message.from_user.id}.txt', 'r') as file: #жим 1, Силовое упражнение , 3; жим2, Силовое упражнение , 5; жим3, Силовое упражнение , 6; 
                    string = file.read().split("; ")
                    for i in string[0: len(string) - 1]:
                        exercises.append(i.split(", "))

                remove(f"exercises_{message.from_user.id}.txt")
            except: pass

            remove(f'training_{message.from_user.id}.txt')
            remove(f't_time_{message.from_user.id}.txt')
            remove(f'training_type_{message.from_user.id}.txt')
            remove(f'training_name_{message.from_user.id}.txt')

            training_id = manager.upload_training(
                message.from_user.id, 
                message.from_user.first_name, 
                message.from_user.username, 
                days,
                t_time, 
                training_type, 
                exercises,
                training_name
            )

            notice_time = manager.get_notice_time(message.from_user.id)
            if notice_time != 0:
                all_minutes = (hour * 60 + minute) - notice_time
                hour = all_minutes // 60
                all_minutes = all_minutes % 60
                minute = all_minutes

            day_of_week = get_days_str(days)

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Показать тренировку", callback_data=f"info_{training_id}")]
            ])

            notice_args = [
                message.from_user.id,
                bot,
                notice_time,
                hour,
                minute,
                training_type,
                keyboard
            ]
            scheduler.add_job(send_reminder, 'cron', day_of_week=day_of_week, hour=hour, minute=minute, args=notice_args, id=f"job_id_{training_id}")
            
            if not manager.get_user_notice(message.from_user.id):
                scheduler.pause_job(f"job_id_{training_id}")

            await message.answer("✔️ <b>Тренировка создана</b>", parse_mode="html", reply_markup=keyboards.schedule_settings)

        except Exception as _ex: 
           print("[INFO]", _ex)
           await message.answer(texts.incorrect_training_params, parse_mode="html", reply_markup=keyboards.schedule_settings)

    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())