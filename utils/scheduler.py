from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_manager import Manager
from utils.get_days_str import get_days_str
from utils.send_reminder import send_reminder

scheduler = AsyncIOScheduler()
manager = Manager()

def start_scheduler():
    scheduler.start()

def scheduler_off(user_id):
    """
    Stops all scheduled tasks for a specific user.

    :param user_id: User's telegram id .
    """

    trainings = manager.get_trainings(user_id)

    for i in trainings:
        scheduler.pause_job(job_id=f"job_id_{i[6]}")

def scheduler_on(user_id):
    """
    Starts all scheduled tasks for a specific user.

    :param user_id: User's telegram id .
    """
    
    trainings = manager.get_trainings(user_id)

    for i in trainings:
        scheduler.resume_job(f"job_id_{i[6]}")

def start_all_notices(bot: Bot):
    """
    Create and starts notices for all trainings.

    :param bot: aiogram Bot object.
    """
    ids = manager.get_all_user_id()

    for id in ids:
        user_notice = manager.get_user_notice(id)

        trainings = manager.get_trainings(id)
        for train in trainings:
            days = train[3]
            training_type = train[5]
            training_id = train[6]

            training_time = manager.get_training_time(training_id)[0]
            hour = training_time.hour
            minute = training_time.minute

            notice_time = manager.get_notice_time(id)
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
                id,
                bot,
                notice_time,
                hour,
                minute,
                training_type,
                keyboard
            ]
            scheduler.add_job(send_reminder, 'cron', day_of_week=day_of_week, hour=hour, minute=minute, args=notice_args, id=f"job_id_{training_id}")

            if not user_notice:
                scheduler.pause_job(f"job_id_{training_id}")