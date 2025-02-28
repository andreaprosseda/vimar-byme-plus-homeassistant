from enum import Enum


class SsType(Enum):
    LIGHT_SWITCH = "SS_Light_Switch"
    LIGHT_DIMMER = "SS_Light_Dimmer"
    LIGHT_DIMMER_RGB = "SS_Light_DimmerRGB"

    ACCESS_GATE = "SS_Access_Gate"
    ACCESS_DOOR_WINDOW = "SS_Access_DoorWindow"

    SHUTTER_POSITION = "SS_Shutter_Position"
    SHUTTER_SLAT_POSITION = "SS_Shutter_SlatPosition"
    SHUTTER_WITHOUT_POSITION = "SS_Shutter_WithoutPosition"
    SHUTTER_SLAT_WITHOUT_POSITION = "SS_Shutter_SlatWithoutPosition"
    CURTAIN_POSITION = "SS_Curtain_Position"
    CURTAIN_WITHOUT_POSITION = "SS_Curtain_WithoutPosition"

    AUDIO_RADIO_FM = "SS_Audio_RadioFM"
    AUDIO_ZONE = "SS_Audio_Zone"
    AUDIO_RCA = "SS_Audio_RCA"
    AUDIO_BLUETOOTH = "SS_Audio_Bluetooth"

    ENERGY_LOAD = "SS_Energy_Load"
    ENERGY_LOAD_CONTROL_1P = "SS_Energy_LoadControl1P"
    ENERGY_LOAD_CONTROL_3P = "SS_Energy_LoadControl3P"
    ENERGY_LOAD_CONTROL_1P_PRODUCTION = "SS_Energy_LoadControl1PProduction"
    ENERGY_LOAD_CONTROL_3P_PRODUCTION = "SS_Energy_LoadControl3PProduction"
    ENERGY_MEASURE_1P = "SS_Energy_Measure1P"
    ENERGY_MEASURE_3P = "SS_Energy_Measure3P"

    IRRIGATION_MULTI_ZONES = "SS_Irrigation_MultiZones"
    AUTOMATION_ON_OFF = "SS_Automation_OnOff"
    AUTOMATION_TIMER_ASTRONOMIC = "SS_Automation_TimerAstronomic"
    AUTOMATION_TECHNICAL_ALARM = "SS_Automation_TechnicalAlarm"
    AUTOMATION_TIMER_WEEKLY = "SS_Automation_TimerWeekly"
    SENSOR_INTERFACE_CONTACT = "SS_Sensor_InterfaceContact"
    SENSOR_AIR_QUALITY_GRADIENT = "SS_Sensor_AirQualityGradient"
    SENSOR_HUMIDITY = "SS_Sensor_Humidity"
    SENSOR_WEATHER_STATION = "SS_Sensor_WeatherStation"
    SCENE_EXECUTOR = "SS_Scene_Executor"
