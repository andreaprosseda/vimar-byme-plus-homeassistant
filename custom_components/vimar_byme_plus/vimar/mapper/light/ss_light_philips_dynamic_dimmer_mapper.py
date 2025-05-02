from ...model.enum.sstype_enum import SsType
from .ss_light_dynamic_dimmer_mapper import SsLightDynamicDimmerMapper


class SsLightPhilipsDynamicDimmerMapper(SsLightDynamicDimmerMapper):
    SSTYPE = SsType.LIGHT_PHILIPS_DYNAMIC_DIMMER.value
