from enum import Enum
from dataclasses import dataclass
from .vimar_component import VimarComponent

class HVACMode(Enum):
    AUTO = 'Auto'
    MANUAL = 'Manual'
    REDUCTION = 'Reduction'
    ABSENCE = 'Absence'
    PROTECTION = 'Protection'
    TIMED_MANUAL = 'Timed manual'
    COMFORT = 'Comfort'
    ECONOMY = 'Economy'
    OFF = 'Off'
    HEAT = 'Heat'
    COOL = 'Cool'
    FAN = 'Fan'
    DRY = 'Dry'

class HVACAction(Enum):
    HEATING = 'Heating'
    COOLING = 'Cooling'


@dataclass
class VimarClimate(VimarComponent):
    is_on: bool
    current_humidity: float | None
    target_humidity: float | None
    hvac_mode: HVACMode | None
    hvac_modes: list[HVACMode]
    # hvac_action: HVACAction | None
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
    # supported_features: ClimateEntityFeature
    min_temp: float
    max_temp: float
    min_humidity: float
    max_humidity: float
