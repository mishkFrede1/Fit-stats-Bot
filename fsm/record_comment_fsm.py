from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data import texts, keyboards
from db_manager import Manager

router = Router()
manager = Manager()

class comment(StatesGroup):
    comment = State()

@router.message(F.text == "Комментарий/Заметка ✍️")
async def get_note_comment(message: Message, state: FSMContext):
    if manager.user_exists(message.from_user.id):
        await state.set_state(comment.comment)
        await message.answer("⚙️ <b>Введите коментарий на счет сегодняшнего дня</b>:", parse_mode="html")
    else:
        await message.answer(texts.unregistered_access_text, parse_mode="html")
        await state.clear()

@router.message(comment.comment)
async def save_note_comment(message: Message, state: FSMContext, bot: Bot):
    with open(f"note_comment_{message.from_user.id}.txt", "w") as file:
        file.write(message.text)

    await state.clear()
    await bot.send_message(message.from_user.id, "✔️ <b>Комментарий записан</b>.", parse_mode="html", reply_markup=keyboards.new_record_params)