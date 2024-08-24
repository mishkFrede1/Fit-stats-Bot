from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from data import keyboards, texts
from db_manager import Manager
from utils.day_add import day_add

class add_day(StatesGroup):
    day = State()

router = Router()
manager = Manager()

@router.message(F.text == "Добавить день ➕")
async def select_day(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(add_day.day)
        await message.answer("⚙️ Выберите день недели для добавления:", reply_markup=keyboards.training_days)
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html", reply_markup=ReplyKeyboardRemove())



@router.callback_query(F.data.endswith("day"))
async def day_set(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await day_add(state, callback_query, bot)

@router.callback_query(F.data == "alldays")
async def day_set(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    await day_add(state, callback_query, bot)