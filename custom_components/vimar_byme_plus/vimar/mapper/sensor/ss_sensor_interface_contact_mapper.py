from ...model.component.vimar_binary_sensor import VimarBinarySensor
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_sensor_generic_mapper import SsSensorGenericMapper


class SsSensorInterfaceContactMapper(SsSensorGenericMapper):
    SSTYPE = SsType.SENSOR_INTERFACE_CONTACT.value

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

    def _button_real_time(self, component: UserComponent, *args):
        return None  # Not implemented by Vimar

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_OUTPUT)
        return value == "On" if value else False
