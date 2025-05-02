from ...model.enum.sstype_enum import SsType
from .ss_light_dimmer_rgb_mapper import SsLightDimmerRgbMapper


class SsLightPhilipsDimmerRgbMapper(SsLightDimmerRgbMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_DIMMER_RGB.value


#   Missing
#   SFE_Cmd_FadingShow
#   SFE_State_FadingShow
