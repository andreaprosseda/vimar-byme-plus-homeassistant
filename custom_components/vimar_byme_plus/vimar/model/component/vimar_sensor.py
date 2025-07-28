from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from .vimar_component import VimarComponent


class SensorStateClass(StrEnum):
    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


class SensorDeviceClass(StrEnum):
    AQI = "aqi"
    CURRENT = "current"
    GAS = "gas"
    ENERGY = "energy"
    ENERGY_STORAGE = "energy_storage"
    ENUM = "enum"
    HUMIDITY = "humidity"
    ILLUMINANCE = "illuminance"
    POWER = "power"
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    VOLTAGE = "voltage"
    VOLUME_FLOW_RATE = "volume_flow_rate"
    WIND_SPEED = "wind_speed"


class SensorMeasurementUnit(StrEnum):
    CELSIUS = "°C"
    CUBIC_METERS = "m³"
    CUBIC_METERS_PER_HOUR = "m³/h"
    KILO_WATT = "kW"
    KILO_WATT_HOUR = "kWh"
    LITRE_PER_SQUARE_METER = "l/m²"
    LUX = "lx"
    METERS_PER_SECOND = "m/s"
    KILOMETERS_PER_HOUR = "km/h"
    MILLIAMPERE = "mA"
    MILLIVOLTS = "mV"
    PASCAL = "Pa"
    PERCENTAGE = "%"


@dataclass
class VimarSensor(VimarComponent):
    main_id: str | None
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
