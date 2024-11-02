from enum import Enum


class ActionType(Enum):
    ON = "ON"
    OFF = "OFF"
    TOGGLE = "TOGGLE"
    
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    STOP = "STOP"
    
    PLAY = "PLAY"
    PAUSE = "PAUSE"
    PREVIOUS = "PREVIOUS"
    NEXT = "NEXT"

    SET_LEVEL = "SET_LEVEL"
    SET_SOURCE = "SET_SOURCE"