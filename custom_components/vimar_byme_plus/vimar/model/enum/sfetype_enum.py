from enum import Enum


class SfeType(Enum):
    CMD_AMBIENT_SETPOINT = "SFE_Cmd_AmbientSetpoint"
    CMD_FAN_MODE = "SFE_Cmd_FanMode"
    CMD_FAN_SPEED = "SFE_Cmd_FanSpeed"
    CMD_FAN_SPEED_3V = "SFE_Cmd_FanSpeed3V"
    CMD_FORCED_ONTIME = "SFE_Cmd_ForcedOnTime"
    CMD_HVAC_MODE = "SFE_Cmd_HVACMode"
    CMD_LOAD_TIMED = "SFE_Cmd_LoadTimed"
    CMD_ON_OFF = "SFE_Cmd_OnOff"
    CMD_VOLUME = "SFE_Cmd_Volume"
    CMD_CURRENT_SOURCE = "SFE_Cmd_CurrentSource"
    CMD_BRIGHTNESS = "SFE_Cmd_Brightness"
    CMD_HSV = "SFE_Cmd_HSV"
    CMD_RGB = "SFE_Cmd_RGB"
    CMD_SHUTTER = "SFE_Cmd_Shutter"
    CMD_SHUTTER_WITHOUT_POSITION = "SFE_Cmd_ShutterWithoutPosition"
    CMD_SLAT = "SFE_Cmd_Slat"
    CMD_SLAT_WITHOUT_POSITION = "SFE_Cmd_SlatWithoutPosition"
    CMD_TIMED_DYNAMIC_MODE = "SFE_Cmd_TimedDynamicMode"
    CMD_TIMED_MANUAL = "SFE_Cmd_TimedManual"
    CMD_SKIP_STATION = "SFE_Cmd_SkipStation"
    CMD_SKIP_TRACK = "SFE_Cmd_SkipTrack"
    CMD_PLAY_PAUSE = "SFE_Cmd_PlayPause"
    CMD_MEM_FREQUENCY_CONTROL = "SFE_Cmd_MemFrequencyControl"
    CMD_CHANGE_OVER_MODE = "SFE_Cmd_ChangeOverMode"
    CMD_OFF_BEHAVIOUR = "SFE_Cmd_OffBehaviour"
    CMD_ON_BEHAVIOUR = "SFE_Cmd_OnBehaviour"
    CMD_IMMEDIATE_START_STOP = "SFE_Cmd_ImmediateStartStop"
    CMD_SKIP_ZONE = "SFE_Cmd_SkipZone"
    CMD_EXECUTE = "SFE_Cmd_Execute"
    CMD_MIXING_WHITE_VALUE = "SFE_Cmd_MixingWhiteValue"
    CMD_DOWNKEY_ACTIVE_SCENE = "SFE_Cmd_DownKey_ActiveScene"
    CMD_START_ACTIVE_SCENE = "SFE_Cmd_CallStart_ActiveScene"
    CMD_END_ACTIVE_SCENE = "SFE_Cmd_CallEnd_ActiveScene"

    STATE_AMBIENT_SETPOINT = "SFE_State_AmbientSetpoint"
    STATE_AMBIENT_TEMPERATURE = "SFE_State_AmbientTemperature"
    STATE_CHANGE_OVER_MODE = "SFE_State_ChangeOverMode"
    STATE_FAN_MODE = "SFE_State_FanMode"
    STATE_FAN_SPEED = "SFE_State_FanSpeed"
    STATE_FAN_SPEED_3V = "SFE_State_FanSpeed3V"
    STATE_FORCED_ON_TIME = "SFE_State_ForcedOnTime"
    STATE_GLOBAL_ACTIVE_POWER_EXCHANGE = "SFE_State_GlobalActivePowerExchange"
    STATE_GLOBAL_ACTIVE_POWER_PRODUCT = "SFE_State_GlobalActivePowerProduct"
    STATE_GLOBAL_ACTIVE_POWER_CONSUMPTION = "SFE_State_GlobalActivePowerConsumption"
    STATE_GLOBAL_THRESHOLD = "SFE_State_GlobalThreshold"
    STATE_HVAC_MODE = "SFE_State_HVACMode"
    STATE_LINE1_THRESHOLD = "SFE_State_Line1Threshold"
    STATE_LINE2_THRESHOLD = "SFE_State_Line2Threshold"
    STATE_LINE3_THRESHOLD = "SFE_State_Line3Threshold"
    STATE_LOAD = "SFE_State_Load"
    STATE_LOADS_PRIORITY = "SFE_State_LoadsPriority"
    STATE_OFF_BEHAVIOUR = "SFE_State_OffBehaviour"
    STATE_ON_BEHAVIOUR = "SFE_State_OnBehaviour"
    STATE_ON_OFF = "SFE_State_OnOff"

    STATE_BRIGHTNESS = "SFE_State_Brightness"
    STATE_HSV = "SFE_State_HSV"
    STATE_RGB = "SFE_State_RGB"
    STATE_MINIMUM_DIMMING_VALUE = "SFE_State_MinimumDimmingValue"
    STATE_MIXING_WHITE_VALUE = "SFE_State_MixingWhiteValue"

    STATE_OUT_STATUS = "SFE_State_OutStatus"
    STATE_SHUTTER = "SFE_State_Shutter"
    STATE_SLAT = "SFE_State_Slat"
    STATE_TIMED_MANUAL = "SFE_State_TimedManual"
    STATE_GENERIC = "SFE_State_Generic"
    STATE_CURRENT = "SFE_State_Current"
    STATE_HUMIDITY = "SFE_State_Humidity"
    STATE_HUMIDITY_SETPOINT = "SFE_State_HumiditySetpoint"
    STATE_SHUTTER_WITHOUT_POSITION = "SFE_State_ShutterWithoutPosition"

    STATE_AUX = "SFE_State_Aux"
    STATE_CURRENT_ALBUM = "SFE_State_CurrentAlbum"
    STATE_CURRENT_ARTIST = "SFE_State_CurrentArtist"
    STATE_CURRENT_SOURCE = "SFE_State_CurrentSource"
    STATE_CURRENT_TRACK = "SFE_State_CurrentTrack"
    STATE_DEVICE_CONNECTED = "SFE_State_DeviceConnected"
    STATE_FM_FREQUENCY = "SFE_State_FMFrequency"
    STATE_MEM_FREQUENCY_ID = "SFE_State_MemFrequencyId"
    STATE_MEM_FREQUENCY_NAMES = "SFE_State_MemFrequencyNames"
    STATE_PLAY_PAUSE = "SFE_State_PlayPause"
    STATE_RDS = "SFE_State_RDS"
    STATE_RSSI = "SFE_State_RSSI"
    STATE_SLEEP = "SFE_State_Sleep"
    STATE_SLEEP_SETTING = "SFE_State_SleepSetting"
    STATE_SOURCE_ID = "SFE_State_SourceId"
    STATE_VOLUME = "SFE_State_Volume"
    STATE_ACCESS = "SFE_State_Access"

    STATE_ACTIVE_ZONE = "SFE_State_ActiveZone"
    STATE_PROGRAM_SETTINGS = "SFE_State_ProgramSettings"

    STATE_OUTPUT = "SFE_State_Output"
    STATE_ALARM = "SFE_State_Alarm"

    STATE_AIR_QUALITY = "SFE_State_AirQuality"
    STATE_AIR_QUALITY_GRADIENT = "SFE_State_AirQualityGradient"
    STATE_ITS_NIGHT = "SFE_State_ItsNight"
    STATE_ITS_RAINING = "SFE_State_ItsRaining"
    STATE_LUMINOSITY = "SFE_State_Luminosity"
    STATE_PRESSURE = "SFE_State_Pressure"
    STATE_RAIN_AMOUNT = "SFE_State_RainAmount"
    STATE_POWER = "SFE_State_Power"
    STATE_TENSION = "SFE_State_Tension"
    STATE_VOLUME_FLOW = "SFE_State_VolumeFlow"
    STATE_SENSOR_TEMPERATURE = "SFE_State_SensorTemperature"
    STATE_WIND_SPEED = "SFE_State_WindSpeed"
    STATE_EXECUTED = "SFE_State_Executed"
