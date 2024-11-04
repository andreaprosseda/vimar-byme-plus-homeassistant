from typing import Optional
from enum import Enum
from dataclasses import dataclass
from .vimar_component import VimarComponent


class PresetMode(Enum):
    AUTO = "Auto", "none"
    COMFORT = "Comfort", "comfort"
    ECONOMY = "Economy", "eco"
    OFF = "Off", "none"

    def __init__(self, vimar_value, ha_value):
        self.vimar_value = vimar_value
        self.ha_value = ha_value

    @staticmethod
    def get_preset_mode_value(vimar_value: str | None) -> str:
        for elem in PresetMode:
            if elem.vimar_value == vimar_value:
                return elem.ha_value
        return PresetMode.OFF.ha_value


class HVACMode(Enum):
    # AUTO = "Auto", "auto"
    # MANUAL = "Manual", "TO_BE_DEFINED_PROGRAMMATICALLY"
    # REDUCTION = "Reduction"
    # ABSENCE = "Absence"
    # PROTECTION = "Protection"
    # TIMED_MANUAL = "Timed manual"
    # COMFORT = "Comfort"
    # ECONOMY = "Economy"
    OFF = "Off", "off"
    HEAT = "Heat", "heat"
    COOL = "Cool", "cool"
    # FAN = "Fan", "fan_only"
    # DRY = "Dry", "dry"

    def __init__(self, vimar_value, ha_value):
        self.vimar_value = vimar_value
        self.ha_value = ha_value

    @staticmethod
    def get_hvac_mode(vimar_value: str | None) -> Optional["HVACMode"]:
        for elem in HVACMode:
            if elem.vimar_value == vimar_value:
                return elem
        return None


class HVACAction(Enum):
    HEAT = "Heat", "heating"
    COOL = "Cool", "cooling"
    HEAT_BOOST = "Heat + Boost", "heating"
    COOL_BOOST = "Cool + Boost", "heating"
    OFF = "Off", "off"
    IDLE = "TO_BE_DEFINED_PROGRAMMATICALLY", "idle"

    def __init__(self, vimar_value, ha_value):
        self.vimar_value = vimar_value
        self.ha_value = ha_value

    @staticmethod
    def get_hvac_action(vimar_value: str | None) -> Optional["HVACAction"]:
        for elem in HVACAction:
            if elem.vimar_value == vimar_value:
                return elem
        return None


class ChangeOverMode(Enum):
    HEAT = "Heating"
    COOL = "Cooling"

    @staticmethod
    def get_change_over_mode(vimar_value: str | None) -> Optional["ChangeOverMode"]:
        for elem in ChangeOverMode:
            if elem.value == vimar_value:
                return elem
        return None


class FanModeV3(Enum):
    FAN_OFF = "Off", "off"
    FAN_LOW = "V1", "low"
    FAN_MEDIUM = "V2", "medium"
    FAN_HIGH = "V3", "high"

    def __init__(self, vimar_value, ha_value):
        self.vimar_value = vimar_value
        self.ha_value = ha_value

    @staticmethod
    def get_fan_mode_value(vimar_value: str | None) -> str | None:
        for elem in FanModeV3:
            if elem.vimar_value == vimar_value:
                return elem.ha_value
        return None


class ClimateEntityFeature(Enum):
    """Supported features of the climate entity."""

    TARGET_TEMPERATURE = 1
    TARGET_TEMPERATURE_RANGE = 2
    TARGET_HUMIDITY = 4
    FAN_MODE = 8
    PRESET_MODE = 16
    SWING_MODE = 32
    AUX_HEAT = 64
    TURN_OFF = 128
    TURN_ON = 256


@dataclass
class VimarClimate(VimarComponent):
    current_humidity: float | None
    target_humidity: float | None
    hvac_mode: HVACMode | None
    hvac_modes: list[HVACMode]
    hvac_action: HVACAction | None
    current_temperature: float | None
    target_temperature: float | None
    target_temperature_step: float | None
    target_temperature_high: float | None
    target_temperature_low: float | None
    preset_mode: str | None
    preset_modes: list[str] | None
    fan_mode: str | None
    fan_modes: list[str] | None
    swing_mode: str | None
    swing_modes: list[str] | None
    supported_features: list[ClimateEntityFeature]
    min_temp: float
    max_temp: float
    min_humidity: float
    max_humidity: float

    @staticmethod
    def get_table_header() -> list:
        return [
            "Area",
            "Name",
            "Type",
            "Temp",
            "Target",
            "HVACMode",
            "HVACAction",
            "Preset",
            "Fan",
        ]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.current_temperature,
            self.target_temperature,
            self.hvac_mode,
            self.hvac_action,
            self.preset_mode,
            self.fan_mode,
        ]
