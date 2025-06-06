from enum import Enum


class Intent(Enum):
    UNKNOWN = 0
    NOTHING = 1
    EXIT = 2
    FILE_SYSTEM = 3
    RANDOM = 4
    KNOWLEDGE = 5
