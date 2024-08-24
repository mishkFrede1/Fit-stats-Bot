def isNumber(var: str):
    """
    Checks the string for the presence of numbers in it.\n 
    Returns the string itself in `int` format if it contains only integers. Otherwise returns `-1`.

    """
    try:
        intVar = int(var)
        return intVar
    except: 
        return -1