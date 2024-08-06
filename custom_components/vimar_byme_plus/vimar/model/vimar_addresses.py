from dataclasses import dataclass


@dataclass
class VimarAddresses:
    hvac_mode: str
    hvac_mode_info: str
    change_over_mode: str
    change_over_mode_info: str
    ambient_temperature: str
    temperature_setpoint: str
    temperature_setpoint_info: str
