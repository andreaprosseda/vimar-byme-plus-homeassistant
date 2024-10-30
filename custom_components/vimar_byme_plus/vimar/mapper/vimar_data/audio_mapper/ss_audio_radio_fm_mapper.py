import json
from ....model.repository.user_component import UserComponent
from ....model.component.vimar_media_player import (
    VimarMediaPlayer,
    MediaType,
    MediaPlayerEntityFeature,
)
from ....model.enum.sfetype_enum import SfeType
from ....model.enum.sstype_enum import SsType


class SsAudioRadioFmMapper:
    SSTYPE = SsType.AUDIO_RADIO_FM.value

    # TBD:
    # STATE_DEVICE_CONNECTED = 'SFE_State_DeviceConnected'
    # STATE_AUX = 'SFE_State_Aux'

    def from_obj(self, component: UserComponent, *args) -> VimarMediaPlayer:
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            area=component.ambient.name,
            is_on=True,
            media_content_type=self.get_media_content_type(component),
            media_title=self.get_media_title(component),
            source=self.get_source(component),
            supported_features=self.get_supported_features(component),
        )

    def get_media_content_type(
        self, component: UserComponent
    ) -> MediaType | str | None:
        """Content type of current playing media."""
        return MediaType.CHANNEL

    def get_media_title(self, component: UserComponent) -> str | None:
        """Title of current playing media."""
        return self._get_radio_title(component)

    def get_source(self, component: UserComponent) -> str | None:
        value = component.get_value(SfeType.STATE_SOURCE_ID)
        return value

    def get_supported_features(
        self, component: UserComponent
    ) -> list[MediaPlayerEntityFeature]:
        """Flag media player features that are supported."""
        return [
            MediaPlayerEntityFeature.PREVIOUS_TRACK,
            MediaPlayerEntityFeature.NEXT_TRACK,
            MediaPlayerEntityFeature.MEDIA_ANNOUNCE,
            MediaPlayerEntityFeature.SELECT_SOURCE,
        ]

    def _get_radio_title(self, component: UserComponent) -> str:
        result = self._get_frequency_description(component)
        rds = component.get_value(SfeType.STATE_RDS)
        return result + " " + rds

    def _get_frequency_description(self, component: UserComponent) -> str:
        frequency = component.get_value(SfeType.STATE_FM_FREQUENCY)
        freq_name = self._get_frequency_name(component)
        if freq_name and frequency:
            return f"[{freq_name} | FM {frequency}]"
        if frequency:
            return f"[FM {frequency}]"
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
        if frequency_id <= 0 or frequency_id > 8:
            return None
        try:
            frequencies = component.get_value(SfeType.STATE_MEM_FREQUENCY_NAMES)
            frequencies_json = json.loads(frequencies)
            return frequencies_json[f"freq{frequency_id}_name"]
        except Exception:
            return None
