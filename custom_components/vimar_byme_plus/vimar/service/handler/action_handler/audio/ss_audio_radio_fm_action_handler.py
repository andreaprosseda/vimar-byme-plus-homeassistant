from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_media_player import VimarMediaPlayer
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .....utils.json import json_dumps
from ..base_action_handler import BaseActionHandler

STATION = SfeType.CMD_SKIP_STATION
FREQUENCY = SfeType.CMD_MEM_FREQUENCY_CONTROL


class SsAudioRadioFmActionHandler(BaseActionHandler):
    SSTYPE = SsType.AUDIO_RADIO_FM.value

    def get_actions(
        self, component: VimarMediaPlayer, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.SET_SOURCE:
            return self.get_select_frequency_actions(component, args[0])
        if action_type == ActionType.PREVIOUS:
            return self.get_previous_fm_actions(component.id)
        if action_type == ActionType.NEXT:
            return self.get_next_fm_actions(component.id)
        raise NotImplementedError

    def get_select_frequency_actions(
        self, component: VimarMediaPlayer, source: str
    ) -> list[VimarAction]:
        """Select input source."""
        position = self._get_position(component, source)
        if not position or int(position) < 0:
            return []
        value = self._get_frequency_control_json(position)
        return [self._action(component.id, FREQUENCY, value)]

    def get_previous_fm_actions(self, id: str) -> list[VimarAction]:
        """Turn the media player on."""
        return [self._action(id, STATION, "Scan prev")]

    def get_next_fm_actions(self, id: str) -> list[VimarAction]:
        """Turn the media player off."""
        return [self._action(id, STATION, "Scan next")]

    def _get_position(self, component: VimarMediaPlayer, source: str) -> str | None:
        for component_source in component.source_list:
            if component_source.name == source:
                return component_source.id
        return None

    def _get_frequency_control_json(self, position: str) -> str:
        json = {"action": "select", "position": int(position)}
        return json_dumps(json)
