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
    def get_preset_mode(vimar_value: str | None) -> Optional["PresetMode"]:
        for elem in PresetMode:
            if elem.vimar_value == vimar_value:
                return elem
        return PresetMode.OFF


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
    preset_mode: PresetMode | None
    preset_modes: list[PresetMode] | None
    fan_mode: str | None
    fan_modes: list[str] | None
    swing_mode: str | None
    swing_modes: list[str] | None
    # supported_features: ClimateEntityFeature
    min_temp: float
    max_temp: float
    min_humidity: float
    max_humidity: float

    @staticmethod
    def get_table_header() -> list:
        return ['Area', 'Name', 'Temp', 'Target', 'HVACMode', 'HVACAction', 'Preset', 'Fan']
    
    def to_table(self) -> list:
        return [self.area, self.name, self.current_temperature, self.target_temperature, self.hvac_mode, self.hvac_action, self.preset_mode, self.fan_mode]