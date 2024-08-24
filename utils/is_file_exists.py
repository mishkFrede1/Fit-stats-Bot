from os.path import isfile

def isFileExists(filename: str) -> bool:
    if isfile(filename):
        return True
    else: return False