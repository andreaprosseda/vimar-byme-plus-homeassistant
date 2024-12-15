from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAutomationTimerAstronomicMapper:
    SSTYPE = SsType.AUTOMATION_TIMER_ASTRONOMIC.value

    def from_obj(self, component: UserComponent, *args) -> list:
        return []
