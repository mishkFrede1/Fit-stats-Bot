from db_manager import Manager
from datetime import date
manager = Manager()

for i in range(24, 27):
    manager.upload_record(863400079, "Дамир", "whitePower1", date(2022, 4, i), None, None, 20+i, None, None, None, None)

# print(len(manager.get_records(863400079, "day", 29)))