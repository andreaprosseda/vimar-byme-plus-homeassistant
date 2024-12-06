from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from .vimar_component import VimarComponent
from enum import StrEnum


class SensorStateClass(StrEnum):
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


class SensorDeviceClass(StrEnum):
    ENERGY = "energy"
    ENERGY_STORAGE = "energy_storage"
    POWER = "power"
    ENUM = "enum"


class SensorMeasurementUnit(StrEnum):
    KILO_WATT = "kW"
    KILO_WATT_HOUR = "kWh"


@dataclass
class VimarSensor(VimarComponent):
    native_value: str | Decimal | None
    last_update: datetime
    decimal_precision: int | None
    unit_of_measurement: SensorMeasurementUnit | None
    state_class: SensorStateClass | None
    options: list[str] | None

    @staticmethod
    def get_table_header() -> list:
        return [
            "Area",
            "Name",
            "Type",
            "Value",
        ]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.native_value,
        ]
