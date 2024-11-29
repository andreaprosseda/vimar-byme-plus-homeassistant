from .....model.enum.sstype_enum import SsType
from .ss_shutter_without_position_action_handler import (
    SsShutterWithoutPositionActionHandler,
)


class SsCurtainWithoutPositionActionHandler(SsShutterWithoutPositionActionHandler):
    SSTYPE = SsType.CURTAIN_WITHOUT_POSITION.value
