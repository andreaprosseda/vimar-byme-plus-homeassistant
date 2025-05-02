from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ..sensor.ss_sensor_interface_contact_mapper import SsSensorInterfaceContactMapper


class SsAccessInterfaceContactMapper(SsSensorInterfaceContactMapper):
    SSTYPE = SsType.ACCESS_INTERFACE_CONTACT.value

    def get_device_class(self) -> str:
        return "door"

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ACCESS)
        return value == "Open" if value else False
