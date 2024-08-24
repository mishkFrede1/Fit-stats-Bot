from aiogram import Router, Bot
from aiogram.types import CallbackQuery

from data import keyboards
from utils.scheduler import scheduler_off, scheduler_on
from db_manager import Manager

router = Router()
manager = Manager()

@router.callback_query(lambda c: c.data and c.data.startswith("notice_o"))
async def change_notice_time(callback_query: CallbackQuery, bot: Bot):
    data = callback_query.data
    if data == "notice_off":
        manager.update_notice_on_off(callback_query.from_user.id, False)
        scheduler_off(callback_query.from_user.id)
        
        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboards.notifications_params_disabled)
        
    elif data == "notice_on":
        manager.update_notice_on_off(callback_query.from_user.id, True)
        scheduler_on(callback_query.from_user.id)

        await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboards.notifications_params_enabled)