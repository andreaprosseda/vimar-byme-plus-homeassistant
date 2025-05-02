from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler


class SsAudioRcaActionHandler(BaseActionHandler):
    SSTYPE = SsType.AUDIO_RCA.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        raise NotImplementedError
