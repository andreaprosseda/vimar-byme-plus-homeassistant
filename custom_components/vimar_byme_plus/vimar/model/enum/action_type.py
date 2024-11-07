from enum import Enum


class ActionType(Enum):
    ON = "ON"
    OFF = "OFF"

    OPEN = "OPEN"
    CLOSE = "CLOSE"
    STOP = "STOP"

    PLAY = "PLAY"
    PAUSE = "PAUSE"
    PREVIOUS = "PREVIOUS"
    NEXT = "NEXT"

    SET_LEVEL = "SET_LEVEL"
    SET_SOURCE = "SET_SOURCE"

    SET_TEMP = "SET_TEMP"
    SET_HVAC_MODE = "SET_HVAC_MODE"
    SET_PRESET_MODE = "SET_PRESET_MODE"
