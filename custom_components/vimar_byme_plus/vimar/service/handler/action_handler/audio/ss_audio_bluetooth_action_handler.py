from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from ..base_action_handler import BaseActionHandler

PLAY_PAUSE = SfeType.CMD_PLAY_PAUSE
TRACK = SfeType.CMD_SKIP_TRACK


class SsAudioBluetoothActionHandler(BaseActionHandler):
    SSTYPE = SsType.AUDIO_BLUETOOTH.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.PLAY:
            return self.get_play_actions(component.id)
        if action_type == ActionType.PAUSE:
            return self.get_pause_actions(component.id)
        if action_type == ActionType.PREVIOUS:
            return self.get_previous_actions(component.id)
        if action_type == ActionType.NEXT:
            return self.get_next_actions(component.id)
        raise NotImplementedError

    def get_play_actions(self, id: str) -> list[VimarAction]:
        """Send previous track command."""
        return [self._action(id, PLAY_PAUSE, "Play")]

    def get_pause_actions(self, id: str) -> list[VimarAction]:
        """Send previous track command."""
        return [self._action(id, PLAY_PAUSE, "Pause")]

    def get_previous_actions(self, id: str) -> list[VimarAction]:
        """Send previous track command."""
        return [self._action(id, TRACK, "Down")]

    def get_next_actions(self) -> list[VimarAction]:
        """Send next track command."""
        return [self._action(id, TRACK, "Up")]
