from decimal import ROUND_HALF_UP, Decimal

from ...model.component.vimar_sensor import (
    SensorDeviceClass,
    SensorMeasurementUnit,
    SensorStateClass,
    VimarSensor,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ..base_mapper import BaseMapper

# Per-type sensor configuration. Electricity preserves the historical
# behaviour (kWh, /1000, no state_class) for users upgrading without
# touching the new OptionsFlow. Water/Gas use TOTAL_INCREASING so they
# show up in HA Energy/Statistics dashboards and the unit override sticks
# (HA has unit converters for water/gas but not for energy<->litres).
_ELECTRICITY_PROFILE = {
    "device_class": SensorDeviceClass.ENERGY,
    "unit": SensorMeasurementUnit.KILO_WATT_HOUR,
    "divisor": 1000,
    "state_class": None,
    "decimal_precision": None,
}

_WATER_PROFILE = {
    "device_class": SensorDeviceClass.WATER,
    "unit": SensorMeasurementUnit.LITRE,
    "divisor": 1,
    "state_class": SensorStateClass.TOTAL_INCREASING,
    "decimal_precision": 0,
}

_GAS_PROFILE = {
    "device_class": SensorDeviceClass.GAS,
    "unit": SensorMeasurementUnit.CUBIC_METERS,
    "divisor": 1,
    "state_class": SensorStateClass.TOTAL_INCREASING,
    "decimal_precision": 0,
}

_PROFILES = {
    "electricity": _ELECTRICITY_PROFILE,
    "water": _WATER_PROFILE,
    "gas": _GAS_PROFILE,
}


class SsEnergyMeasureCounterMapper(BaseMapper):
    SSTYPE = SsType.ENERGY_MEASURE_COUNTER.value

    def from_obj(
        self, component: UserComponent, counter_type: str | None = None, *args
    ) -> list[VimarSensor]:
        return [self._from_obj(component, counter_type)]

    def _from_obj(
        self, component: UserComponent, counter_type: str | None
    ) -> VimarSensor:
        profile = _PROFILES.get(counter_type or "electricity", _ELECTRICITY_PROFILE)
        return VimarSensor(
            id=str(component.idsf),
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=profile["device_class"],
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component, profile["divisor"]),
            last_update=None,
            decimal_precision=profile["decimal_precision"],
            unit_of_measurement=profile["unit"],
            state_class=profile["state_class"],
            options=None,
        )

    def native_value(self, component: UserComponent, divisor: int) -> Decimal | None:
        value = component.get_value(SfeType.STATE_PARTIAL_COUNTER)
        if not value:
            return None
        decimal_value = Decimal(value) / divisor
        if divisor == 1:
            return decimal_value
        return decimal_value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
