from .ss_light_dimmer_rgb_mapper import SsLightDimmerRgbMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sstype_enum import SsType


class SsLightPhilipsDimmerRgbMapper(SsLightDimmerRgbMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_DIMMER_RGB.value


#   Missing
#   SFE_Cmd_FadingShow
#   SFE_State_FadingShow
