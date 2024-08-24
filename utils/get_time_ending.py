def getTimeEndingMinute(minute: int) -> str:
    if minute == 1 or minute != 11 and minute % 10 == 1:
        return "минута"
    elif minute % 10 != 1 and 0 != minute % 10 < 5 and minute > 20 or minute < 5 and minute > 1:
        return "минуты"
    else:
        return "минут"
    
def getTimeEndingSeconds(seconds: int) -> str:
    if seconds == 1 or seconds != 11 and seconds % 10 == 1:
        return "секунда"
    elif seconds % 10 != 1 and 0 != seconds % 10 < 5 and seconds > 20 or seconds < 5 and seconds > 1:
        return "секунды"
    else:
        return "секунд"

def getTimeEndingHour(hour: int) -> str:
    if hour == 1 or hour != 11 and hour % 10 == 1:
        return "час"
    elif hour % 10 != 1 and 0 != hour % 10 < 5 and hour > 20 or hour < 5 and hour > 1:
        return "часа"
    else:
        return "часов"