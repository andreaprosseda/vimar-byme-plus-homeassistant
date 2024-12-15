from ...model.component.vimar_binary_sensor import VimarBinarySensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSensorInterfaceContactMapper:
    SSTYPE = SsType.SENSOR_INTERFACE_CONTACT.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarBinarySensor]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarBinarySensor:
        return VimarBinarySensor(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="switch",
            area=component.ambient.name,
            is_on=self.get_is_on(component),
        )

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_OUTPUT)
        return value == "On" if value else False
