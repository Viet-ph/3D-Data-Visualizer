import enum

class OperationMode(enum.Flag):
    Normal = 0
    Pan = 1
    Remove = 2

operationMode = OperationMode.Remove

def isOperatingWith(mode: OperationMode) -> bool:
    return (operationMode == mode) 

def isOperatingWith(modeStr:str) -> bool:
    switcher = {
            "normal": OperationMode.Normal,
            "pan": OperationMode.Pan,
            "remove": OperationMode.Remove
    }
    return (operationMode == switcher.get(modeStr.lower()))