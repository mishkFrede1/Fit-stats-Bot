from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import keyboards, texts
from utils.is_number import isNumber
from db_manager import Manager

router = Router()
manager = Manager()

class notice_time(StatesGroup):
    notice_time = State()

@router.callback_query(F.data == "notice_time")
async def change_notice_time(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(notice_time.notice_time)
    await bot.send_message(callback_query.from_user.id, "⚙️ Введите время, за сколько минут до начала тренировки отправлять напоминание:", parse_mode="html", reply_markup=ReplyKeyboardRemove())

@router.message(notice_time.notice_time)
async def send_new_notice_time(message: Message, state: FSMContext):
    isNumberResult = isNumber(message.text)

    if isNumberResult == -1:
        await message.answer(texts.incorrect_format_error_text, parse_mode="html")
        await state.clear()
    else:
        manager.update_notice_time(message.from_user.id, isNumberResult)

        await message.answer("✔️ <b>Время уведомлений обновлено</b>", parse_mode="html", reply_markup=keyboards.schedule_settings)
        await state.clear()