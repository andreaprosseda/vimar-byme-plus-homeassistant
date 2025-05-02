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


class SsAudioBluetoothMapper:
    SSTYPE = SsType.AUDIO_BLUETOOTH.value

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
            media_title=None,
            media_artist=None,
            media_album_name=None,
            media_album_artist=None,
            media_track=None,
            source_id=self.get_source_id(component),
            current_source=self.get_current_source(component),
            source_list=None,
            source_flavor=self.get_source_flavor(component),
            supported_features=self.get_supported_features(component),
        )

    def get_is_connected(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_DEVICE_CONNECTED)
        return value == "Connected" if value else False

    def get_state(self, component: UserComponent) -> MediaPlayerState | None:
        """State of the player."""
        connected = self.get_is_connected(component)
        play_pause = component.get_value(SfeType.STATE_PLAY_PAUSE)
        if not connected:
            return MediaPlayerState.STANDBY
        if play_pause == "Play":
            return MediaPlayerState.PLAYING
        if play_pause == "Pause":
            return MediaPlayerState.PAUSED
        return MediaPlayerState.ON

    def get_media_content_type(
        self, component: UserComponent
    ) -> MediaType | str | None:
        """Content type of current playing media."""
        return MediaType.MUSIC

    def get_media_title(self, component: UserComponent) -> str | None:
        """Title of current playing media."""
        return self.get_media_track(component)

    def get_media_artist(self, component: UserComponent) -> str | None:
        """Artist of current playing media, music track only."""
        return component.get_value(SfeType.STATE_CURRENT_ARTIST)

    def get_media_album_name(self, component: UserComponent) -> str | None:
        """Album name of current playing media, music track only."""
        return component.get_value(SfeType.STATE_CURRENT_ALBUM)

    def get_media_album_artist(self, component: UserComponent) -> str | None:
        """Album artist of current playing media, music track only."""
        return self.get_media_artist(component)

    def get_media_track(self, component: UserComponent) -> int | None:
        """Track number of current playing media, music track only."""
        return component.get_value(SfeType.STATE_CURRENT_TRACK)

    def get_source_id(self, component: UserComponent) -> str | None:
        """Name of the current input source."""
        return component.get_value(SfeType.STATE_SOURCE_ID)

    def get_current_source(self, component: UserComponent) -> str | None:
        """Name of the current input source."""
        return None

    def get_source_flavor(self, component: UserComponent) -> Source | None:
        """Name of the current input source."""
        return Source(
            id=self.get_source_id(component),
            name=component.name,
            component_id=component.idsf,
            media_class="music",
            media_content_type="music",
            children_list=[],
        )

    def get_supported_features(
        self, component: UserComponent
    ) -> list[MediaPlayerEntityFeature]:
        """Flag media player features that are supported."""
        return [
            MediaPlayerEntityFeature.PLAY,
            MediaPlayerEntityFeature.PAUSE,
            MediaPlayerEntityFeature.PREVIOUS_TRACK,
            MediaPlayerEntityFeature.NEXT_TRACK,
        ]
