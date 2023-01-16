from enum import Enum


class LogLevels(int, Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __int__(self) -> int:
        return int.__int__(self)
