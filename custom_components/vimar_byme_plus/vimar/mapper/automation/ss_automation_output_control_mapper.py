from ...model.component.vimar_switch import VimarSwitch
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAutomationOutputControlMapper:
    SSTYPE = SsType.AUTOMATION_OUTPUT_CONTROL.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarSwitch]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarSwitch:
        raise NotImplementedError
