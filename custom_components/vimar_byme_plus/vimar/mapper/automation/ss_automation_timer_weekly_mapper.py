from ...model.component.vimar_switch import VimarSwitch
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAutomationTimerWeeklyMapper:
    SSTYPE = SsType.AUTOMATION_TIMER_WEEKLY.value

    def from_obj(self, component: UserComponent, *args) -> list:
        return []
