from ...model.enum.sstype_enum import SsType
from .ss_light_switch_mapper import SsLightSwitchMapper


class SsLightPhilipsSwitchMapper(SsLightSwitchMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_SWITCH.value
