def getAgeEnding(age: int):
    text = ""
    
    if 11 != age and age % 10 == 1 or age == 1:
        text = "год"
    elif age % 10 != 1 and 0 != age % 10 < 5 and age > 20 or age < 5 and age > 1:
        text = "года"
    else:
        text = "лет"

    return text