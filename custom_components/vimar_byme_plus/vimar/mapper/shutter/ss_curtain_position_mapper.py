from ...model.enum.sstype_enum import SsType
from .ss_shutter_position_mapper import SsShutterPositionMapper


class SsCurtainPositionMapper(SsShutterPositionMapper):
    SSTYPE = SsType.CURTAIN_POSITION.value
