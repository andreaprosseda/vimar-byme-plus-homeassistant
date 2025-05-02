from decimal import Decimal

from ...model.component.vimar_sensor import SensorDeviceClass, VimarSensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ..base_mapper import BaseMapper


class SsEnergyLoadMapper(BaseMapper):
    SSTYPE = SsType.ENERGY_LOAD.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ENUM,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=None,
            unit_of_measurement=None,
            state_class=None,
            options=self.get_values(component),
        )

    def native_value(self, component: UserComponent) -> str | Decimal | None:
        value = component.get_value(SfeType.STATE_LOAD)
        if value:
            return value
        return "Unknown"

    def get_values(self, component: UserComponent) -> list[str]:
        return ["Auto on", "Auto off", "Forced on", "Forced off", "Unknown"]
