from db_manager import Manager
from datetime import date
from random import randint
manager = Manager()

def fake_accs(count):
    for i in range(0, count):
        manager.upload_registration_data(143873259, date(2024, 8, 15+i), f"Fake{i}", f"fakeuser{i}", False, 15+i, 73+i, 165+i, "Набор веса")

def fake_sleep_records(count, user_id: int, name: str, username: str):
    for i in range(0, count):
        manager.upload_record(
            user_id,
            name,
            username,
            date(2024, 8, i+14),
            None,
            None,
            None,
            None,
            None,
            randint(100, 500),
            randint(2000, 3500),
            [["weight", str(randint(75, 79))], ["height", str(randint(169, 171))], ["biceps", str(randint(39, 42))], ["hips", str(randint(80, 84))]],
            randint(7, 12)
        )

#fake_sleep_records([9, 8, 10, 8, 10, 8, 8, 10, 12, 9, 9, 12], 863400079)
#fake_sleep_records(1, 863400079, "Дамир", "whitePower1")
fake_sleep_records(1, 917823627, "Дио", "gaffrin")
# manager.upload_record(
#                 863400079,
#                 "Дамир",
#                 "whitePower1",
#                 date(2024, 8, 11),
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 None,
#                 randint(2000, 4000),
#                 [["height", "170"]],
#                 randint(8, 12)
#             )