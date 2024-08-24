from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from data import keyboards, texts
from db_manager import Manager

router = Router()
manager = Manager()

@router.message(F.text == "Настройки оповещений 🔔")
async def notifications(message: Message):
    if manager.user_exists(message.from_user.id):
        notices = manager.get_user_notice(message.from_user.id)
        keyboard = keyboards.notifications_params_disabled

        if notices: 
            keyboard = keyboards.notifications_params_enabled
            
        await message.answer("⚙️ Выберите настройки для уведомлений:", parse_mode="html", reply_markup=keyboard)

    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())