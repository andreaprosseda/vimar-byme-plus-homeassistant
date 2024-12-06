from ...model.component.vimar_media_player import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
    VimarMediaPlayer,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAudioZoneMapper:
    SSTYPE = SsType.AUDIO_ZONE.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarMediaPlayer]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarMediaPlayer:
        sources = args[0]
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="speaker",
            area=component.ambient.name,
            is_on=self.get_is_on(component),
            state=self.get_state(component),
            volume_level=self.get_volume_level(component),
            volume_step=self.get_volume_step(component),
            is_volume_muted=self.get_is_volume_muted(component),
            media_content_type=self.get_media_content_type(component),
            media_title=self.get_media_title(component, sources),
            media_artist=None,
            media_album_name=None,
            media_album_artist=None,
            media_track=None,
            source_id=self.get_source_id(component),
            current_source=self.get_current_source(component, sources),
            source_list=self.get_source_list(component, sources),
            source_flavor=None,
            supported_features=self.get_supported_features(component),
        )

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "On" if value else False

    def get_state(self, component: UserComponent) -> MediaPlayerState | None:
        """State of the player."""
        sleep = component.get_value(SfeType.STATE_SLEEP)
        is_on = self.get_is_on(component)
        if not is_on:
            return MediaPlayerState.OFF
        if sleep == "Awake":
            return MediaPlayerState.PLAYING
        if sleep == "Sleep":
            return MediaPlayerState.IDLE
        return MediaPlayerState.ON

    def get_volume_level(self, component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_VOLUME)
        if not value:
            return None
        return int(value) / 100

    def get_volume_step(self, component: UserComponent) -> float:
        return 1 / 10

    def get_is_volume_muted(self, component: UserComponent) -> bool | None:
        return self.get_volume_level(component) == 0

    def get_media_content_type(
        self, component: UserComponent
    ) -> MediaType | str | None:
        """Content type of current playing media."""
        return MediaType.MUSIC

    def get_media_title(
        self, component: UserComponent, sources: list[VimarMediaPlayer]
    ) -> str | None:
        """Title of current playing media."""
        return self.get_current_source(component, sources)

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
        return None

    def get_current_source(
        self, component: UserComponent, sources: list[VimarMediaPlayer]
    ) -> str | None:
        """Name of the current input source."""
        value = component.get_value(SfeType.STATE_CURRENT_SOURCE)
        return self._get_source_name(value, sources)

    def get_source_list(
        self, component: UserComponent, sources: list[VimarMediaPlayer]
    ) -> list[str] | None:
        """Name of all input sources."""
        return [source.source_flavor for source in sources]

    def get_supported_features(
        self, component: UserComponent
    ) -> list[MediaPlayerEntityFeature]:
        """Flag media player features that are supported."""
        return [
            MediaPlayerEntityFeature.VOLUME_SET,
            MediaPlayerEntityFeature.VOLUME_MUTE,
            MediaPlayerEntityFeature.VOLUME_STEP,
            MediaPlayerEntityFeature.SELECT_SOURCE,
            MediaPlayerEntityFeature.BROWSE_MEDIA,
            MediaPlayerEntityFeature.PLAY_MEDIA,
            MediaPlayerEntityFeature.TURN_OFF,
            MediaPlayerEntityFeature.TURN_ON,
        ]

    def _get_source_name(
        self, value: str | None, sources: list[VimarMediaPlayer]
    ) -> str | None:
        if not value:
            return None
        for source in sources:
            if source.source_id == value:
                return source.name
        return None
