from enum import Enum


class SsType(Enum):
    LIGHT_SWITCH = "SS_Light_Switch"
    LIGHT_DIMMER = "SS_Light_Dimmer"

    ACCESS_GATE = "SS_Access_Gate"
    ACCESS_DOOR_WINDOW = "SS_Access_DoorWindow"

    SHUTTER_POSITION = "SS_Shutter_Position"
    SHUTTER_WITHOUT_POSITION = "SS_Shutter_WithoutPosition"

    AUDIO_RADIO_FM = "SS_Audio_RadioFM"
    AUDIO_ZONE = "SS_Audio_Zone"
    AUDIO_RCA = "SS_Audio_RCA"
    AUDIO_BLUETOOTH = "SS_Audio_Bluetooth"
