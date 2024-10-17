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

def fake_records(user_id: int, name: str, username: str, day, burned, gained, weight, height, biceps, sleep):
    manager.upload_record(
            user_id,
            name,
            username,
            date(2024, 10, day),
            None,
            None,
            None,
            None,
            None,
            burned,
            gained,
            [["weight", str(weight)], ["height", str(height)], ["biceps", str(biceps)]],
            sleep
    )


burned=[300, 500, 100, 700, 200, 500, 250, 200, 800, 300, 670, 210, 500, 150, 300, 800, 300, 190, 200, 750]
gained=[3000, 3300, 3400, 4000, 4000, 4100, 3500, 3500, 3400, 3700, 3400, 4000, 4300, 3200, 3500, 3500, 3550, 3800, 3900, 3700]
weight=[77, 77, 77, 77, 76, 77, 79, 79, 79, 81, 81, 80, 80, 80, 82, 82, 83, 83, 82, 82]
height=[169, 169, 169, 169, 169, 169, 169, 169, 169, 169, 169, 169, 170, 170, 170, 170, 170, 170, 170, 170]
biceps=[39, 39, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
sleep=[8, 8, 7, 8, 8, 10, 11, 6, 7, 6, 8, 10, 7, 8, 6, 6, 9, 10, 11, 7]
for i in range(20):
    fake_records(863400079, "Дамир", "whitePower1", i+1, burned[i], gained[i], weight[i], height[i], biceps[i], sleep[i])

#fake_sleep_records([9, 8, 10, 8, 10, 8, 8, 10, 12, 9, 9, 12], 863400079)
#fake_sleep_records(1, 863400079, "Дамир", "whitePower1")
#fake_sleep_records(1, 917823627, "Дио", "gaffrin")
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