from ...model.enum.sstype_enum import SsType
from .ss_shutter_without_position_mapper import SsShutterWithoutPositionMapper


class SsCurtainWithoutPositionMapper(SsShutterWithoutPositionMapper):
    SSTYPE = SsType.CURTAIN_WITHOUT_POSITION.value
