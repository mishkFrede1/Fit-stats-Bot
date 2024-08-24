from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from utils.get_records_keyboard import get_records_list_keyboard
from db_manager import Manager

class test():
    def __init__(self, router: Router, manager: Manager, pag_data: str, mode: str, user_id_in_mode: str, id: int, type: str):
        self.router = router
        self.manager = manager,
        self.pag_data = pag_data

        self.router.callback_query.register(self.records_list_pagination, F.data.startswith(pag_data))

    async def records_list_pagination(self, callback_query: CallbackQuery, bot: Bot):
        splited_data = callback_query.data.split('_')
        command = splited_data[2]

        id = int(splited_data[3])
        if command == "right": 
            id += 1
        else: id -= 1

        records = self.manager.get_records(callback_query.from_user.id)
        length = len(records) // 5 + 1
        list_left = 0 + id * 5
        list_right = 5 + id * 5

        records_list = records[list_left: list_right]

        is_possible = False
        if len(records_list) > 0:
            if id <= length-1 and command == "right" or id >= 0 and command == "left": 
                is_possible = True

        if is_possible:
            keyboard = get_records_list_keyboard(records_list, id=id)

            await bot.edit_message_text(
                "📑 <b>Выберите запись</b>:", 
                callback_query.from_user.id, 
                callback_query.message.message_id, 
                parse_mode="html", 
                reply_markup=keyboard
            )