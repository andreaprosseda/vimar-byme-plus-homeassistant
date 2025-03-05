from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAutomationTimerPeriodicMapper:
    SSTYPE = SsType.AUTOMATION_TIMER_PERIODIC.value

    def from_obj(self, component: UserComponent, *args) -> list:
        return []
