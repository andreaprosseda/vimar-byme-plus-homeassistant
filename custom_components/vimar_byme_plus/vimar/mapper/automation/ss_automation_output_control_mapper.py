from .ss_automation_on_off_mapper import SsAutomationOnOffMapper
from ...model.enum.sstype_enum import SsType


class SsAutomationOutputControlMapper(SsAutomationOnOffMapper):
    SSTYPE = SsType.AUTOMATION_OUTPUT_CONTROL.value
