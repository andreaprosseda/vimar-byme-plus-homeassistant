from decimal import Decimal

from ...model.component.vimar_button import VimarButton
from ...model.component.vimar_sensor import VimarSensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSensorGenericMapper:
    SSTYPE = SsType.SENSOR_GENERIC.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSensor]:
        components = []
        main = self._from_obj(component, *args)
        if main:
            components.append(main)

        real_time = self._button_real_time(component, *args)
        if real_time:
            components.append(real_time)

        return components

    def _from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=self.decimal_precision(component),
            unit_of_measurement=None,
            state_class=None,
            options=None,
        )

    def _button_real_time(self, component: UserComponent, *args) -> VimarButton:
        return VimarButton(
            id=str(component.idsf) + "_real_time_updates",
            name=component.name + " - " + "Aggiornamenti RealTime",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            executed=False,
        )

    def native_value(self, component: UserComponent) -> str | Decimal | None:
        value = component.get_value(SfeType.STATE_GENERIC)
        if value:
            return Decimal(value)
        return None

    def decimal_precision(self, component: UserComponent) -> int:
        return 1
