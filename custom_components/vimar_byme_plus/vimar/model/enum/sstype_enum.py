from enum import Enum


class SsType(Enum):
    # SF_ACCESS
    ACCESS_INTERFACE_CONTACT = "SS_Access_InterfaceContact"
    ACCESS_GATE = "SS_Access_Gate"
    ACCESS_DOOR_WINDOW = "SS_Access_DoorWindow"

    # SF_AUDIO
    AUDIO_BLUETOOTH = "SS_Audio_Bluetooth"
    AUDIO_RADIO_FM = "SS_Audio_RadioFM"
    AUDIO_RCA = "SS_Audio_RCA"
    AUDIO_ZONE = "SS_Audio_Zone"

    # SF_AUTOMATION
    AUTOMATION_TECHNICAL_ALARM = "SS_Automation_TechnicalAlarm"
    AUTOMATION_ON_OFF = "SS_Automation_OnOff"
    AUTOMATION_OUTPUT_CONTROL = "SS_Automation_OutputControl"
    AUTOMATION_TIMER_WEEKLY = "SS_Automation_TimerWeekly"
    AUTOMATION_TIMER_PERIODIC = "SS_Automation_TimerPeriodic"
    AUTOMATION_TIMER_ASTRONOMIC = "SS_Automation_TimerAstronomic"

    # SF_CLIMA
    CLIMA_CONTROL = "SS_Clima_Control"
    CLIMA_DAIKIN = "SS_Clima_Daikin"
    CLIMA_DAIKIN_VRV = "SS_Clima_DaikinVRV"
    CLIMA_HUMIDITY = "SS_Clima_Humidity"
    CLIMA_INTERFACE_CONTACT = "SS_Clima_InterfaceContact"
    CLIMA_LG = "SS_Clima_LG"
    CLIMA_MITSUBISHI = "SS_Clima_Mitsubishi"
    CLIMA_MITSUBISHI_NO_FAN = "SS_Clima_MitsubishiNoFan"
    CLIMA_PRESSURE = "SS_Clima_Pressure"
    CLIMA_RAIN_AMOUNT = "SS_Clima_RainAmount"
    CLIMA_TEMPERATURE = "SS_Clima_Temperature"
    CLIMA_WIND_SPEED = "SS_Clima_WindSpeed"
    CLIMA_ZONE = "SS_Clima_Zone"
    CLIMA_ZONE_VRV = "SS_Clima_ZoneVRV"

    # SF_ENERGY
    ENERGY_LOAD = "SS_Energy_Load"
    ENERGY_LOAD_CONTROL_1P = "SS_Energy_LoadControl1P"
    ENERGY_LOAD_CONTROL_1P_PRODUCTION = "SS_Energy_LoadControl1PProduction"
    ENERGY_LOAD_CONTROL_3P = "SS_Energy_LoadControl3P"
    ENERGY_LOAD_CONTROL_3P_PRODUCTION = "SS_Energy_LoadControl3PProduction"
    ENERGY_MEASURE_1P = "SS_Energy_Measure1P"
    ENERGY_MEASURE_3P = "SS_Energy_Measure3P"
    ENERGY_MEASURE_COUNTER = "SS_Energy_MeasureCounter"

    # SF_IRRIGATION
    IRRIGATION_MULTI_ZONES = "SS_Irrigation_MultiZones"

    # SF_LIGHT
    LIGHT_CONSTANT_CONTROL = "SS_Light_ConstantControl"
    LIGHT_DIMMER = "SS_Light_Dimmer"
    LIGHT_DIMMER_RGB = "SS_Light_DimmerRGB"
    LIGHT_DYNAMIC_DIMMER = "SS_Light_DynamicDimmer"
    LIGHT_PHILIPS_DIMMER = "SS_Light_PhilipsDimmer"
    LIGHT_PHILIPS_DIMMER_RGB = "SS_Light_PhilipsDimmerRGB"
    LIGHT_PHILIPS_DYNAMIC_DIMMER = "SS_Light_PhilipsDynamicDimmer"
    LIGHT_PHILIPS_DYNAMIC_DIMMER_RGB = "SS_Light_PhilipsDynamicDimmerRGB"
    LIGHT_PHILIPS_SWITCH = "SS_Light_PhilipsSwitch"
    LIGHT_SWITCH = "SS_Light_Switch"

    # SF_SCENE
    SCENE_EXECUTOR = "SS_Scene_Executor"

    # SF_SCENE_ACTIVATOR
    SCENE_ACTIVATOR_ACTIVATOR = "SS_SceneActivator_Activator"
    SCENE_ACTIVATOR_AIR_QUALITY_GRADIENT = "SS_SceneActivator_AirQualityGradient"
    SCENE_ACTIVATOR_SAI = "SS_SceneActivator_Sai"
    SCENE_ACTIVATOR_SAI_G2 = "SS_SceneActivator_Saig2"
    SCENE_ACTIVATOR_VIDEO_ENTRY = "SS_SceneActivator_Videoentry"

    # SF_SENSOR
    SENSOR_AIR_QUALITY = "SS_Sensor_AirQuality"
    SENSOR_AIR_QUALITY_GRADIENT = "SS_Sensor_AirQualityGradient"
    SENSOR_CURRENT = "SS_Sensor_Current"
    SENSOR_GENERIC = "SS_Sensor_Generic"
    SENSOR_HUMIDITY = "SS_Sensor_Humidity"
    SENSOR_INTERFACE_CONTACT = "SS_Sensor_InterfaceContact"
    SENSOR_LUMINOSITY = "SS_Sensor_Luminosity"
    SENSOR_POWER = "SS_Sensor_Power"
    SENSOR_PRESSURE = "SS_Sensor_Pressure"
    SENSOR_RAIN_AMOUNT = "SS_Sensor_RainAmount"
    SENSOR_TEMPERATURE = "SS_Sensor_Temperature"
    SENSOR_TENSION = "SS_Sensor_Tension"
    SENSOR_VOLUME_FLOW = "SS_Sensor_VolumeFlow"
    SENSOR_WEATHER_STATION = "SS_Sensor_WeatherStation"
    SENSOR_WIND_SPEED = "SS_Sensor_WindSpeed"

    # SF_SHUTTER
    CURTAIN_POSITION = "SS_Curtain_Position"
    CURTAIN_WITHOUT_POSITION = "SS_Curtain_WithoutPosition"
    SHUTTER_POSITION = "SS_Shutter_Position"
    SHUTTER_SLAT_POSITION = "SS_Shutter_SlatPosition"
    SHUTTER_SLAT_WITHOUT_POSITION = "SS_Shutter_SlatWithoutPosition"
    SHUTTER_WITHOUT_POSITION = "SS_Shutter_WithoutPosition"
