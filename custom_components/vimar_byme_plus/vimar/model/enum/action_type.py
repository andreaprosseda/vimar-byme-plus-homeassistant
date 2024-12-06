from enum import Enum


class ActionType(Enum):
    ON = "ON"
    OFF = "OFF"

    OPEN = "OPEN"
    CLOSE = "CLOSE"
    STOP = "STOP"
    SET_POSITION = "SET_POSITION"

    OPEN_SLAT = "OPEN"
    CLOSE_SLAT = "CLOSE"
    STOP_SLAT = "STOP"
    SET_SLAT_POSITION = "SET_POSITION"

    PLAY = "PLAY"
    PAUSE = "PAUSE"
    PREVIOUS = "PREVIOUS"
    NEXT = "NEXT"

    SET_LEVEL = "SET_LEVEL"
    SET_SOURCE = "SET_SOURCE"

    SET_TEMP = "SET_TEMP"
    SET_HVAC_MODE = "SET_HVAC_MODE"
    SET_PRESET_MODE = "SET_PRESET_MODE"
