day_ids = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5,
    "saturday": 6,
    "sunday": 7
}
rus_day_ids = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"      
}
def sort_week_days(days: list):
    int_days = []
    for day in days:
        int_days.append(day_ids[day])
    
    int_days = sorted(int_days)

    result = []
    for day in int_days:
        result.append(rus_day_ids[day])
    
    return ", ".join(result)

#print(sort_week_days(["tuesday", "sunday", "saturday", "wednesday"]))
