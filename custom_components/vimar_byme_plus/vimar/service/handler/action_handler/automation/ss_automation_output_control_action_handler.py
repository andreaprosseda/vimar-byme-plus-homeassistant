from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_automation_on_off_action_handler import SsAutomationOnOffActionHandler

ON_OFF = SfeType.CMD_ON_OFF


class SsAutomationOutputControlActionHandler(SsAutomationOnOffActionHandler):
    SSTYPE = SsType.AUTOMATION_OUTPUT_CONTROL.value
