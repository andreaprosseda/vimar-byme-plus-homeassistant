import json
from ....model.repository.user_component import UserComponent
from ....model.component.vimar_media_player import (
    VimarMediaPlayer,
    MediaPlayerState,
    MediaType,
    MediaPlayerEntityFeature,
)
from ....model.enum.sfetype_enum import SfeType
from ....model.enum.sstype_enum import SsType


class SsAudioZoneMapper:
    SSTYPE = SsType.AUDIO_ZONE.value

    # TBD:
    # STATE_DEVICE_CONNECTED = 'SFE_State_DeviceConnected'
    # STATE_AUX = 'SFE_State_Aux'

    def from_obj(self, component: UserComponent, *args) -> VimarMediaPlayer:
        sources = args[0]
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            area=component.ambient.name,
            is_on=self.get_is_on(component),
            state=self.get_state(component),
            volume_level=self.get_volume_level(component),
            volume_step=self.get_volume_step(component),
            is_volume_muted=self.get_is_volume_muted(component),
            media_content_type=self.get_media_content_type(component),
            source=self.get_source(component, sources),
            source_list=self.get_source_list(component, sources),
            supported_features=self.get_supported_features(component),
        )

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "On" if value else False

    def get_state(self, component: UserComponent) -> MediaPlayerState | None:
        """State of the player."""
        play_pause = component.get_value(SfeType.STATE_PLAY_PAUSE)
        is_on = self.get_is_on(component)
        if not is_on:
            return MediaPlayerState.OFF
        if play_pause == "Play":
            return MediaPlayerState.PLAYING
        if play_pause == "Pause":
            return MediaPlayerState.PAUSED
        return MediaPlayerState.ON

    def get_volume_level(self, component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_VOLUME)
        if not value:
            return None
        return int(value) / 100

    def get_volume_step(self, component: UserComponent) -> float:
        return 1 / 100

    def get_is_volume_muted(self, component: UserComponent) -> bool | None:
        return self.get_volume_level(component) == 0

    def get_media_content_type(
        self, component: UserComponent
    ) -> MediaType | str | None:
        """Content type of current playing media."""
        return MediaType.MUSIC

    def get_media_title(self, component: UserComponent) -> str | None:
        """Title of current playing media."""
        return "prova"

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

    def get_source(
        self, component: UserComponent, sources: list[VimarMediaPlayer]
    ) -> list[str] | None:
        value = component.get_value(SfeType.STATE_CURRENT_SOURCE)
        return self._get_source_name(value, sources)

    def get_source_list(
        self, component: UserComponent, sources: list[VimarMediaPlayer]
    ) -> list[str] | None:
        return [source.name for source in sources]

    def get_supported_features(
        self, component: UserComponent
    ) -> list[MediaPlayerEntityFeature]:
        """Flag media player features that are supported."""
        return [
            MediaPlayerEntityFeature.VOLUME_SET,
            MediaPlayerEntityFeature.VOLUME_MUTE,
            MediaPlayerEntityFeature.SELECT_SOURCE,
            MediaPlayerEntityFeature.TURN_OFF,
            MediaPlayerEntityFeature.TURN_ON,
        ]

    def _get_source_name(
        self, value: str | None, sources: list[VimarMediaPlayer]
    ) -> str | None:
        if not value:
            return None
        for source in sources:
            if source.source == value:
                return source.name
