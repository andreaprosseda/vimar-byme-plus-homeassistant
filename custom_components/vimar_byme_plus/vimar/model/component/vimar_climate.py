from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .vimar_component import VimarComponent


class PresetMode(Enum):
    OFF = "Off", False
    ECONOMY = "Absence", False
    PROTECTION = "Protection", False
    AUTO = "Auto", True
    MANUAL = "Manual", True
    REDUCTION = "Reduction", True
    TIMED_MANUAL = "Timed manual", True

    def __init__(self, vimar_value: str, on: bool):
        self.vimar_value = vimar_value
        self.on = on

    @staticmethod
    def get_group_values(preset_mode: str) -> list[str] | None:
        mode = PresetMode.get_preset_mode(preset_mode)
        if not mode:
            return None
        return [preset.vimar_value for preset in PresetMode if preset.on == mode.on]

    @staticmethod
    def get_preset_mode(vimar_value: str | None) -> Optional["PresetMode"]:
        for elem in PresetMode:
            if elem.vimar_value == vimar_value:
                return elem
        return None


class HVACMode(Enum):
    OFF = "Off", "off"
    ABSENCE = "Absence", "off"
    PROTECTION = "Protection", "off"
    AUTO = "Auto", "heat_cool"
    MANUAL = "Manual", "heat_cool"
    REDUCTION = "Reduction", "heat_cool"
    TIMED_MANUAL = "Timed manual", "heat_cool"

    def __init__(self, vimar_value, ha_value):
        self.vimar_value = vimar_value
        self.ha_value = ha_value

    @staticmethod
    def get_ha_hvac_mode(ha_value: str | None) -> Optional["HVACMode"]:
        for elem in HVACMode:
            if elem.ha_value == ha_value:
                return elem
        return None

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


class FanMode(Enum):
    AUTOMATIC = "Automatic", "auto"
    # FAN_OFF = "Off", "off"
    FAN_LOW = "V1", "low"
    FAN_MEDIUM = "V2", "medium"
    FAN_HIGH = "V3", "high"

    def __init__(self, vimar_value, ha_value):
        self.vimar_value = vimar_value
        self.ha_value = ha_value

    @staticmethod
    def get_fan_mode(vimar_value: str | None) -> Optional["FanMode"]:
        for elem in FanMode:
            if elem.vimar_value == vimar_value:
                return elem
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
    fan_mode: FanMode | None
    fan_modes: list[FanMode] | None
    swing_mode: str | None
    swing_modes: list[str] | None
    supported_features: list[ClimateEntityFeature]
    min_temp: float
    max_temp: float
    min_humidity: float
    max_humidity: float
    on_behaviour: PresetMode | None
    off_behaviour: PresetMode | None

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
