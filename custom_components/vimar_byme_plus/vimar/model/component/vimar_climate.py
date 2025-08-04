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
    OFF = "off"
    HEAT = "heat"
    COOL = "cool"
    HEAT_COOL = "heat_cool"
    AUTO = "auto"
    DRY = "dry"
    FAN_ONLY = "fan_only"

    @staticmethod
    def get_hvac_mode(
        hvac_mode: str | None, out_status: str | None, change_over_mode: str | None
    ) -> Optional["HVACMode"]:
        mode = _HVACMode.get_mode(hvac_mode)
        change_mode = ChangeOverMode.get_change_over_mode(change_over_mode)
        status = OutStatus.get_out_status(out_status)

        if mode.is_off():
            return HVACMode.OFF
        if status.is_heat() or change_mode == ChangeOverMode.HEAT:
            return HVACMode.HEAT
        if status.is_cool() or change_mode == ChangeOverMode.COOL:
            return HVACMode.COOL
        return None


class _HVACMode(Enum):
    AUTO = "Auto"
    MANUAL = "Manual"
    REDUCTION = "Reduction"
    ABSENCE = "Absence"
    PROTECTION = "Protection"
    OFF = "Off"
    TIMED_MANUAL = "Timed manual"

    def is_off(self) -> bool:
        return self in [_HVACMode.OFF, _HVACMode.ABSENCE, _HVACMode.PROTECTION]

    @staticmethod
    def get_mode(value: str | None) -> Optional["_HVACMode"]:
        if not value:
            return None
        for elem in _HVACMode:
            if elem.value == value:
                return elem
        return None


class HVACAction(Enum):
    COOLING = "cooling"
    DEFROSTING = "defrosting"
    DRYING = "drying"
    FAN = "fan"
    HEATING = "heating"
    IDLE = "idle"
    OFF = "off"
    PREHEATING = "preheating"

    @staticmethod
    def get_hvac_action(
        hvac_mode: str | None, out_status: str | None, change_over_mode: str | None
    ) -> Optional["HVACAction"]:
        mode = HVACMode.get_hvac_mode(hvac_mode, out_status, change_over_mode)
        status = OutStatus.get_out_status(out_status)

        if mode == HVACMode.OFF:
            return HVACAction.OFF
        if status.is_heat():
            return HVACAction.HEATING
        if status.is_cool():
            return HVACAction.COOLING
        return HVACAction.IDLE


class OutStatus(Enum):
    OFF = "Off"
    HEAT = "Heat"
    HEAT_BOOST = "Heat + Boost"
    COOL = "Cool"
    COOL_BOOST = "Cool + Boost"

    def is_heat(self) -> bool:
        return self in [OutStatus.HEAT, OutStatus.HEAT_BOOST]

    def is_cool(self) -> bool:
        return self in [OutStatus.COOL, OutStatus.COOL_BOOST]

    @staticmethod
    def get_out_status(value: str | None) -> Optional["OutStatus"]:
        if not value:
            return None
        for elem in OutStatus:
            if elem.value == value:
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
    can_change_mode: bool
    permission_granted: bool

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
