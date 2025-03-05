from datetime import datetime
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
from .ss_energy_load_control_1p_mapper import SsEnergyLoadControl1pMapper

MODES = {
    "Exchange": SfeType.STATE_GLOBAL_ACTIVE_POWER_EXCHANGE,
    "Production": SfeType.STATE_GLOBAL_ACTIVE_POWER_PRODUCT,
    "Consumption": SfeType.STATE_GLOBAL_ACTIVE_POWER_CONSUMPTION,
}

EXCHANGE = SfeType.STATE_GLOBAL_ACTIVE_POWER_EXCHANGE
PRODUCT = SfeType.STATE_GLOBAL_ACTIVE_POWER_PRODUCT
CONSUMPTION = SfeType.STATE_GLOBAL_ACTIVE_POWER_CONSUMPTION


class SsEnergyLoadControl1pProductionMapper(SsEnergyLoadControl1pMapper):
    SSTYPE = SsType.ENERGY_LOAD_CONTROL_1P_PRODUCTION.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [
            self.power_from_obj(component, "Exchange"),
            self.energy_from_obj(component, "Exchange"),
            self.power_from_obj(component, "Production"),
            self.energy_from_obj(component, "Production"),
            self.power_from_obj(component, "Consumption"),
            self.energy_from_obj(component, "Consumption"),
        ]

    def power_from_obj(self, component: UserComponent, mode: str) -> VimarSensor:
        return VimarSensor(
            id=str(component.idsf) + "_power_" + mode.lower(),
            name=component.name + " - " + mode,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.POWER,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component, MODES.get(mode)),
            last_update=self.last_update(component, MODES.get(mode)),
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILO_WATT,
            state_class=SensorStateClass.MEASUREMENT,
            options=None,
        )

    def energy_from_obj(self, component: UserComponent, mode: str) -> VimarSensor:
        return VimarSensor(
            id=str(component.idsf) + "_energy_" + mode.lower(),
            name=component.name + " - " + mode,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ENERGY,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component, MODES.get(mode)),
            last_update=self.last_update(component, MODES.get(mode)),
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=SensorMeasurementUnit.KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL_INCREASING,
            options=None,
        )

    def native_value(
        self, component: UserComponent, sfetype: SfeType
    ) -> Decimal | None:
        value = component.get_value(sfetype)
        if not value:
            return None
        decimal_value = Decimal(value) / 1000
        return decimal_value.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)

    def last_update(
        self, component: UserComponent, sfetype: SfeType
    ) -> datetime | None:
        value = component.get_last_update(sfetype)
        if not value:
            return None
        return datetime.fromisoformat(value)

    def decimal_precision(self, component: UserComponent) -> int:
        return 3
