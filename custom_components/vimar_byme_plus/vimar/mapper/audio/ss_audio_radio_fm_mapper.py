import json
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_media_player import (
    VimarMediaPlayer,
    MediaType,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    Source,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType


class SsAudioRadioFmMapper:
    SSTYPE = SsType.AUDIO_RADIO_FM.value

    def from_obj(self, component: UserComponent, *args) -> VimarMediaPlayer:
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="receiver",
            area=component.ambient.name,
            is_on=True,
            state=self.get_state(component),
            media_content_type=self.get_media_content_type(component),
            media_title=self.get_media_title(component),
            source_id=self.get_source_id(component),
            current_source=self.get_current_source(component),
            source_list=self.get_source_list(component),
            supported_features=self.get_supported_features(component),
        )

    def get_state(self, component: UserComponent) -> MediaPlayerState | None:
        """State of the player."""
        return MediaPlayerState.PLAYING

    def get_media_content_type(self, component: UserComponent) -> MediaType | str | None:
        """Content type of current playing media."""
        return MediaType.CHANNEL

    def get_media_title(self, component: UserComponent) -> str | None:
        """Title of current playing media."""
        return self._get_radio_title(component)

    def get_source_id(self, component: UserComponent) -> str | None:
        """Name of the current input source."""
        return component.get_value(SfeType.STATE_SOURCE_ID)

    def get_current_source(self, component: UserComponent) -> str | None:
        """Name of the current input source."""
        return self._get_frequency_name(component)

    def get_source_list(self, component: UserComponent) -> list[str] | None:
        """List of available input sources."""
        return self._get_frequency_names(component)

    def get_supported_features(self, component: UserComponent) -> list[MediaPlayerEntityFeature]:
        """Flag media player features that are supported."""
        return [
            MediaPlayerEntityFeature.PREVIOUS_TRACK,
            MediaPlayerEntityFeature.NEXT_TRACK,
            MediaPlayerEntityFeature.SELECT_SOURCE,
        ]

    def _get_radio_title(self, component: UserComponent) -> str:
        result = self._get_frequency_description(component)
        rds = component.get_value(SfeType.STATE_RDS)
        return result + rds

    def _get_frequency_description(self, component: UserComponent) -> str:
        frequency = component.get_value(SfeType.STATE_FM_FREQUENCY)
        freq_name = self._get_frequency_name(component)
        if freq_name and frequency:
            return f"[{freq_name} | FM {frequency}] "
        if frequency:
            return f"[FM {frequency}] "
        return ""

    def _get_frequency_name(self, component: UserComponent) -> str | None:
        frequency_id = self._get_frequency_id(component)
        return self._get_frequency_name_by_id(frequency_id, component)

    def _get_frequency_id(self, component: UserComponent) -> int:
        try:
            frequency_id = component.get_value(SfeType.STATE_MEM_FREQUENCY_ID)
            frequency_id_json = json.loads(frequency_id)
            if frequency_id_json["found"]:
                return int(frequency_id_json["position"])
        except Exception:
            return 0

    def _get_frequency_name_by_id(self, frequency_id: int, component: UserComponent) -> str | None:
        try:
            frequencies = component.get_value(SfeType.STATE_MEM_FREQUENCY_NAMES)
            frequencies_json = json.loads(frequencies)
            return frequencies_json[f"freq{frequency_id}_name"]
        except Exception:
            return "Manual"

    def _get_frequency_names(self, component: UserComponent) -> list[Source] | None:
        try:
            frequencies = component.get_value(SfeType.STATE_MEM_FREQUENCY_NAMES)
            frequencies_json = json.loads(frequencies)
            sources = []
            for i in range(8):
                name = frequencies_json[f"freq{i+1}_name"]
                source = self._get_source(i + 1, name)
                sources.append(source)
            sources.append(self._get_source(-1, "Manual"))
            return sources
        except Exception:
            return None

    def _get_source(self, id: int, name: str) -> Source:
        return Source(id=str(id), name=name)
