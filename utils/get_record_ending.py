def getRecordCountEnding(count: int) -> str:
    if count == 1 or count != 11 and count % 10 == 1:
        return "запись"
    elif count % 10 != 1 and 0 != count % 10 < 5 and count > 20 or count < 5 and count > 1:
        return "записи"
    else:
        return "записей"