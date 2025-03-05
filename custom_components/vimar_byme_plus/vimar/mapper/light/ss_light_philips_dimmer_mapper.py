from .ss_light_dimmer_mapper import SsLightDimmerMapper
from ...model.enum.sstype_enum import SsType


class SsLightPhilipsDimmerMapper(SsLightDimmerMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_DIMMER.value
