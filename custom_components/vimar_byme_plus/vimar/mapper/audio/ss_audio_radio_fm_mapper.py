import json

from ...model.component.vimar_media_player import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
    Source,
    VimarMediaPlayer,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ...utils.logger import log_error


class SsAudioRadioFmMapper:
    SSTYPE = SsType.AUDIO_RADIO_FM.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarMediaPlayer]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarMediaPlayer:
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="receiver",
            area=component.ambient.name,
            is_on=True,
            state=self.get_state(component),
            volume_level=None,
            volume_step=None,
            is_volume_muted=None,
            media_content_type=self.get_media_content_type(component),
            media_title=self.get_media_title(component),
            media_artist=None,
            media_album_name=None,
            media_album_artist=None,
            media_track=None,
            source_id=self.get_source_id(component),
            current_source=self.get_current_source(component),
            source_list=self.get_source_list(component),
            source_flavor=self.get_source_flavor(component),
            supported_features=self.get_supported_features(component),
        )

    def get_state(self, component: UserComponent) -> MediaPlayerState | None:
        """State of the player."""
        return MediaPlayerState.PLAYING

    def get_media_content_type(
        self, component: UserComponent
    ) -> MediaType | str | None:
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

    def get_source_list(self, component: UserComponent) -> list[Source] | None:
        """List of available input sources."""
        return self._get_frequency_sources(component)

    def get_source_flavor(self, component: UserComponent) -> Source | None:
        """Name of the current input source."""
        return Source(
            id=self.get_source_id(component),
            name=component.name,
            component_id=component.idsf,
            media_class="channel",
            media_content_type="channel",
            children_list=self._get_frequency_names(component),
        )

    def get_supported_features(
        self, component: UserComponent
    ) -> list[MediaPlayerEntityFeature]:
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

    def _get_frequency_name_by_id(
        self, frequency_id: int, component: UserComponent
    ) -> str | None:
        try:
            frequencies = component.get_value(SfeType.STATE_MEM_FREQUENCY_NAMES)
            frequencies_json = json.loads(frequencies)
            return frequencies_json[f"freq{frequency_id}_name"]
        except Exception:
            return "Manual"

    def _get_frequency_sources(self, component: UserComponent) -> list[Source] | None:
        try:
            frequencies = component.get_value(SfeType.STATE_MEM_FREQUENCY_NAMES)
            frequencies_json = json.loads(frequencies)
            sources = []
            for i in range(8):
                name = frequencies_json[f"freq{i + 1}_name"]
                source = self._get_source(component, i + 1, name)
                sources.append(source)
            sources.append(self._get_source(component, -1, "Manual"))
            return sources
        except Exception as e:
            log_error(__name__, f"Exception occurred: {e}")
            return None

    def _get_frequency_names(self, component: UserComponent) -> list[str] | None:
        try:
            frequencies = component.get_value(SfeType.STATE_MEM_FREQUENCY_NAMES)
            frequencies_json = json.loads(frequencies)
            sources = []
            for i in range(8):
                name = frequencies_json[f"freq{i + 1}_name"]
                sources.append(name)
            return sources
        except Exception as e:
            log_error(__name__, f"An exception occurred: {e}")
            return None

    def _get_source(self, component: UserComponent, id: int, name: str) -> Source:
        return Source(
            id=str(id),
            name=name,
            component_id=component.idsf,
            media_class="channel",
            media_content_type="channel",
            children_list=[],
        )
