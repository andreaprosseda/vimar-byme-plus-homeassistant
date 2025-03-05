from .ss_light_switch_mapper import SsLightSwitchMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sstype_enum import SsType


class SsLightPhilipsSwitchMapper(SsLightSwitchMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_SWITCH.value
