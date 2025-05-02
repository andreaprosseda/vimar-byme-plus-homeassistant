from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_media_player import Source, VimarMediaPlayer
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .....utils.json import json_dumps
from ..base_action_handler import BaseActionHandler

ON_OFF = SfeType.CMD_ON_OFF
VOLUME = SfeType.CMD_VOLUME
SOURCE = SfeType.CMD_CURRENT_SOURCE
FREQUENCY = SfeType.CMD_MEM_FREQUENCY_CONTROL


class SsAudioZoneActionHandler(BaseActionHandler):
    SSTYPE = SsType.AUDIO_ZONE.value

    def get_actions(
        self, component: VimarMediaPlayer, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component.id)
        if action_type == ActionType.OFF:
            return self.get_turn_off_actions(component.id)
        if action_type == ActionType.SET_SOURCE:
            return self.get_select_source_actions(component, *args)
        if action_type == ActionType.SET_LEVEL:
            return self.get_select_volume_level_actions(component.id, args[0])
        raise NotImplementedError

    def get_turn_on_actions(self, id: str) -> list[VimarAction]:
        """Turn the media player on."""
        return [self._action(id, ON_OFF, "On")]

    def get_turn_off_actions(self, id: str) -> list[VimarAction]:
        """Turn the media player off."""
        return [self._action(id, ON_OFF, "Off")]

    def get_select_volume_level_actions(
        self, id: str, volume: float
    ) -> list[VimarAction]:
        """Set volume level, range 0..1."""
        return [self._action(id, VOLUME, int(volume * 100))]

    def get_select_source_actions(
        self, component: VimarMediaPlayer, *args
    ) -> list[VimarAction]:
        """Select input source."""
        source = self._get_source(component, args[0])
        if source:
            actions = [self._action(component.id, SOURCE, source.id)]
            actions.extend(self._frequency_selection(component, source, *args))
            return actions
        return []

    def _frequency_selection(
        self, component: VimarMediaPlayer, source: Source, *args
    ) -> list[VimarAction]:
        if len(args) < 2:
            return []
        position = args[1]
        if not position or int(position) < 0:
            return []
        value = self._get_frequency_control_json(position)
        return [self._action(source.component_id, FREQUENCY, value)]

    def _get_source(self, component: VimarMediaPlayer, source: str) -> Source | None:
        for component_source in component.source_list:
            if component_source.id == source:
                return component_source
        return None

    def _get_frequency_control_json(self, position: str) -> str:
        json = {"action": "select", "position": int(position)}
        return json_dumps(json)
