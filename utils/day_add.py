from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from data import texts, keyboards

async def day_add(state: FSMContext, callback_query: CallbackQuery, bot: Bot):
    day = callback_query.data
    await state.update_data(day=day)
    text = texts.day_add_text

    if day == "alldays": 
        text = texts.days_add_text
        day = "monday, tuesday, wednesday, thursday, friday, saturday, sunday"

    try:
        with open(f'training_{callback_query.from_user.id}.txt', 'a') as file:
            file.write(f"{day}, ")

    except FileNotFoundError:
        with open(f'training_{callback_query.from_user.id}.txt', 'w') as file:
            file.write(f"{day}, ")
    

    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, text, parse_mode="html", reply_markup=keyboards.new_training)
    await state.clear()