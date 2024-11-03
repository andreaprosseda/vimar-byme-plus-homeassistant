from .....model.enum.action_type import ActionType
from .....model.enum.sftype_enum import SfType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_media_player import VimarMediaPlayer
from ..base_action_handler import BaseActionHandler

ON_OFF = SfeType.CMD_ON_OFF
VOLUME = SfeType.CMD_VOLUME
SOURCE = SfeType.CMD_CURRENT_SOURCE


class SsAudioZoneActionHandler(BaseActionHandler):
    SFTYPE = SfType.AUDIO.value
    SSTYPE = SsType.AUDIO_ZONE.value

    def get_actions(self, component: VimarMediaPlayer, action_type: ActionType, *args) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component.id)
        if action_type == ActionType.OFF:
            return self.get_turn_off_actions(component.id)
        if action_type == ActionType.TOGGLE:
            return self.get_toggle_actions(component.id, component.is_on)
        if action_type == ActionType.SET_SOURCE:
            return self.get_select_source_actions(component, args[0])
        if action_type == ActionType.SET_LEVEL:
            return self.get_select_volume_level_actions(component.id, args[0])
        raise NotImplementedError
    
    def get_turn_on_actions(self, id: str) -> list[VimarAction]:
        """Turn the media player on."""
        return [self._action(id, ON_OFF, "On")]

    def get_turn_off_actions(self, id: str) -> list[VimarAction]:
        """Turn the media player off."""
        return [self._action(id, ON_OFF, "Off")]

    def get_toggle_actions(self, id: str, is_on: bool) -> list[VimarAction]:
        """Toggle the power on the media player."""
        if is_on:
            return self.get_turn_off_actions(id)
        return self.get_turn_on_actions(id)

    def get_select_volume_level_actions(self, id: str, volume: float) -> list[VimarAction]:
        """Set volume level, range 0..1."""
        return [self._action(id, VOLUME, int(volume * 100))]
        
    def get_select_source_actions(self, component: VimarMediaPlayer, source: str) -> list[VimarAction]:
        """Select input source."""
        source_id = self._get_source_id(component, source)
        if source_id:
            return [self._action(component.id, SOURCE, source_id)]
        return []
    
    def _get_source_id(self, component: VimarMediaPlayer, source: str) -> str | None:
        for component_source in component.source_list:
            if component_source.name == source:
                return component_source.id
        return None