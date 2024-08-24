from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup

from data import texts
from utils.get_time_ending import getTimeEndingMinute

async def send_reminder(user_id: int, bot: Bot, notice_time: int, hour: int, minute: int, t_type: str, keyboard: InlineKeyboardMarkup):
    all_minute = (hour * 60 + minute) + notice_time
    hour = all_minute // 60
    all_minute = all_minute % 60
    minute = all_minute

    ending = getTimeEndingMinute(int(notice_time))

    if len(str(minute)) < 2:
        minute = f"0{minute}"

    if notice_time == 0:
        await bot.send_message(user_id, texts.notice_text_zero.format(t_type=t_type, hour=hour, minute=minute), parse_mode="html", reply_markup=keyboard)
    else:
        await bot.send_message(user_id, texts.notice_text.format(t_type=t_type, notice_time=notice_time, time_ending=ending, hour=hour, minute=minute), parse_mode="html", reply_markup=keyboard)