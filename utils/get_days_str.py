def get_days_str(days: list[str]) -> str:
    result = ""
    reduced_days = {
        "monday":"mon",
        "tuesday":"tue",
        "wednesday":"wed",
        "thursday":"thu",
        "friday":"fri",
        "saturday":"sat",
        "sunday":"sun"
    }

    for day in days:
        if day != days[len(days)-1]:
            result += f"{reduced_days[day]},"
        else:
            result += reduced_days[day]

    return result