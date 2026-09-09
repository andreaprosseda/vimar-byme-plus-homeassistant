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

# What newer gateways declare in SFE_State_MeasureType. The vocabulary follows
# the Telemetry family of the Vimar spec (SS_TelemetryWaterHot/Cold,
# SS_TelemetryGas, SS_Telemetry_EnergyMeasure_*); confirmed on a real
# installation, where a water meter reports 'WaterCold' with unit 'L'.
# Matched lowercase and by substring, so WaterCold/WaterHot/Water all land on
# water and any EnergyMeasure variant lands on electricity.
_DECLARED_MEDIA = (
    ("water", _WATER_PROFILE),
    ("gas", _GAS_PROFILE),
    ("energy", _ELECTRICITY_PROFILE),
    ("electric", _ELECTRICITY_PROFILE),
)

# SFE_State_UnitOfMeasure is a free string in the spec, so it is matched, not
# parsed. Only the units the model can express are honoured; anything else
# leaves the medium profile's own unit in place.
_DECLARED_UNITS = {
    "l": SensorMeasurementUnit.LITRE,
    "litre": SensorMeasurementUnit.LITRE,
    "litri": SensorMeasurementUnit.LITRE,
    "m3": SensorMeasurementUnit.CUBIC_METERS,
    "m³": SensorMeasurementUnit.CUBIC_METERS,
    "kwh": SensorMeasurementUnit.KILO_WATT_HOUR,
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
        profile = self._profile(component, counter_type)
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

    def _profile(self, component: UserComponent, counter_type: str | None) -> dict:
        """Which medium this counter measures, most trustworthy source first.

        1. what the user picked in the options - an explicit choice always wins;
        2. what the gateway declares, on firmwares that say it;
        3. the historical default, so installations that declare nothing keep
           behaving exactly as before (electricity, raw pulses divided by 1000).
        """
        if counter_type:
            return _PROFILES.get(counter_type, _ELECTRICITY_PROFILE)
        declared = self._declared_profile(component)
        return declared or _ELECTRICITY_PROFILE

    def _declared_profile(self, component: UserComponent) -> dict | None:
        """Build a profile out of what the gateway says it is metering.

        The divisor is 1: when the gateway states both the counter and its
        unit, the raw value is already expressed in that unit - a water meter
        reading 1316978 with unit 'L' is 1316978 litres, not 1316.978.
        """
        measure_type = (component.get_value(SfeType.STATE_MEASURE_TYPE) or "").lower()
        if not measure_type:
            return None
        base = next(
            (p for key, p in _DECLARED_MEDIA if key in measure_type),
            None,
        )
        if base is None:
            return None
        profile = dict(base)
        profile["divisor"] = 1
        unit = (
            (component.get_value(SfeType.STATE_UNIT_OF_MEASURE) or "").strip().lower()
        )
        if unit in _DECLARED_UNITS:
            profile["unit"] = _DECLARED_UNITS[unit]
        return profile

    def native_value(self, component: UserComponent, divisor: int) -> Decimal | None:
        value = component.get_value(SfeType.STATE_PARTIAL_COUNTER)
        if not value:
            return None
        decimal_value = Decimal(value) / divisor
        if divisor == 1:
            return decimal_value
        return decimal_value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
