from .ss_automation_on_off_mapper import SsAutomationOnOffMapper
from .ss_automation_timer_astronomic_mapper import SsAutomationTimerAstronomicMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_switch import VimarSwitch
from ...model.enum.sftype_enum import SfType
from ...utils.logger import not_implemented
from ...utils.filtering import flat


class AutomationMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarSwitch]:
        sftype = SfType.AUTOMATION.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [AutomationMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarSwitch]:
        try:
            mapper = AutomationMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsAutomationOnOffMapper.SSTYPE:
            return SsAutomationOnOffMapper()
        if sstype == SsAutomationTimerAstronomicMapper.SSTYPE:
            return SsAutomationTimerAstronomicMapper()
        raise NotImplementedError
