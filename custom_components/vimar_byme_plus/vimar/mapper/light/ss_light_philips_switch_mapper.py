from .ss_light_switch_mapper import SsLightSwitchMapper
from ...model.enum.sstype_enum import SsType


class SsLightPhilipsSwitchMapper(SsLightSwitchMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_SWITCH.value
