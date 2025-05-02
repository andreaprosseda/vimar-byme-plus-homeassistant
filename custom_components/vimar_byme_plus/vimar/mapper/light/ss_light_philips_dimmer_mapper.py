from ...model.enum.sstype_enum import SsType
from .ss_light_dimmer_mapper import SsLightDimmerMapper


class SsLightPhilipsDimmerMapper(SsLightDimmerMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_DIMMER.value
