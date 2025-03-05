from .ss_light_dimmer_mapper import SsLightDimmerMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_light import VimarLight
from ...model.enum.sstype_enum import SsType


class SsLightDynamicDimmerMapper(SsLightDimmerMapper):
    SSTYPE = SsType.LIGHT_DYNAMIC_DIMMER.value
