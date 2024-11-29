from .....model.enum.sstype_enum import SsType
from .ss_shutter_position_action_handler import SsShutterPositionActionHandler


class SsCurtainPositionActionHandler(SsShutterPositionActionHandler):
    SSTYPE = SsType.CURTAIN_POSITION.value
