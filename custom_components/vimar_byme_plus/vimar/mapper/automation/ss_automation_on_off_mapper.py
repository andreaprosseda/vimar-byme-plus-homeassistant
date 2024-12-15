from ...model.component.vimar_switch import VimarSwitch
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAutomationOnOffMapper:
    SSTYPE = SsType.AUTOMATION_ON_OFF.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSwitch]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarSwitch:
        return VimarSwitch(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="switch",
            area=component.ambient.name,
            main_id=None,
            is_on=self.get_is_on(component),
        )

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "On" if value else False
