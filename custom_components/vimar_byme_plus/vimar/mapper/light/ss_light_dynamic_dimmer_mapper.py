from .ss_light_dimmer_mapper import SsLightDimmerMapper
from ...model.enum.sstype_enum import SsType


class SsLightDynamicDimmerMapper(SsLightDimmerMapper):
    SSTYPE = SsType.LIGHT_DYNAMIC_DIMMER.value
