from ....model.repository.user_component import UserComponent
from ....model.component.vimar_media_player import (
    VimarMediaPlayer,
    MediaType,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from ....model.enum.sfetype_enum import SfeType
from ....model.enum.sstype_enum import SsType


class SsAudioRcaMapper:
    SSTYPE = SsType.AUDIO_RCA.value

    def from_obj(self, component: UserComponent, *args) -> VimarMediaPlayer:
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            area=component.ambient.name,
            is_on=True,
            state=self.get_state(component),
            media_content_type=self.get_media_content_type(component),
            source_id=self.get_source_id(component),
            current_source=self.get_current_source(component),
            supported_features=self.get_supported_features(component),
        )

    def get_state(self, component: UserComponent) -> MediaPlayerState | None:
        """State of the player."""
        return MediaPlayerState.STANDBY

    def get_media_content_type(
        self, component: UserComponent
    ) -> MediaType | str | None:
        """Content type of current playing media."""
        return MediaType.MUSIC

    def get_source_id(self, component: UserComponent) -> str | None:
        """Name of the current input source."""
        return component.get_value(SfeType.STATE_SOURCE_ID)

    def get_current_source(self, component: UserComponent) -> str | None:
        """Name of the current input source."""
        return None

    def get_supported_features(
        self, component: UserComponent
    ) -> list[MediaPlayerEntityFeature]:
        """Flag media player features that are supported."""
        return []
