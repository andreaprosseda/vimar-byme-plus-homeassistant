"""Platform for media player integration."""

from __future__ import annotations

from functools import reduce
from typing import Any

from homeassistant.components.media_player import (
    BrowseMedia,
    MediaClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CoordinatorConfigEntry
from .base_entity import BaseEntity
from .coordinator import Coordinator
from .vimar.model.component.vimar_media_player import Source, VimarMediaPlayer
from .vimar.model.enum.action_type import ActionType
from .vimar.utils.logger import log_info


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_media_players()
    entities = [MediaPlayer(coordinator, component) for component in components]
    log_info(__name__, f"Media Players found: {len(entities)}")
    async_add_entities(entities, True)


class MediaPlayer(BaseEntity, MediaPlayerEntity):
    """Provides a Vimar Media Player."""

    _component: VimarMediaPlayer

    def __init__(self, coordinator: Coordinator, component: VimarMediaPlayer) -> None:
        """Initialize the media player."""
        self._component = component
        BaseEntity.__init__(self, coordinator, component)

    @property
    def state(self) -> MediaPlayerState | None:
        """State of the player."""
        value = self._component.state.value
        return MediaPlayerState(value) if value else None

    @property
    def volume_level(self) -> float | None:
        """Volume level of the media player (0..1)."""
        return self._component.volume_level

    @property
    def volume_step(self) -> float:
        """Volume step of the media player."""
        return self._component.volume_step

    @property
    def is_volume_muted(self) -> bool | None:
        """Boolean if volume is currently muted."""
        return self._component.is_volume_muted

    @property
    def media_content_type(self) -> MediaType | str | None:
        """Content type of current playing media."""
        return self._component.media_content_type

    @property
    def media_title(self) -> str | None:
        """Title of current playing media."""
        return self._component.media_title

    @property
    def media_artist(self) -> str | None:
        """Artist of current playing media, music track only."""
        return self._component.media_artist

    @property
    def media_album_name(self) -> str | None:
        """Album name of current playing media, music track only."""
        return self._component.media_album_name

    @property
    def media_album_artist(self) -> str | None:
        """Album artist of current playing media, music track only."""
        return self._component.media_album_artist

    @property
    def media_track(self) -> int | None:
        """Track number of current playing media, music track only."""
        return self._component.media_track

    @property
    def source(self) -> str | None:
        """Name of the current input source."""
        return self._component.current_source

    @property
    def source_list(self) -> list[str] | None:
        """List of available input sources."""
        if not self._component.source_list:
            return None
        return [source.name for source in self._component.source_list]

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported."""
        features = [f.value for f in self._component.supported_features]
        return reduce(lambda x, y: x | y, features, MediaPlayerEntityFeature(0))

    def turn_on(self) -> None:
        """Turn the media player on."""
        self.send(ActionType.ON)

    def turn_off(self) -> None:
        """Turn the media player off."""
        self.send(ActionType.OFF)

    def mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        self.send(ActionType.SET_LEVEL, 0)

    def set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        self.send(ActionType.SET_LEVEL, volume)

    def media_play(self) -> None:
        """Send play command."""
        self.send(ActionType.PLAY)

    def media_pause(self) -> None:
        """Send pause command."""
        self.send(ActionType.PAUSE)

    def media_stop(self) -> None:
        """Send stop command."""
        self.send(ActionType.STOP)

    def media_previous_track(self) -> None:
        """Send previous track command."""
        self.send(ActionType.PREVIOUS)

    def media_next_track(self) -> None:
        """Send next track command."""
        self.send(ActionType.NEXT)

    def select_source(self, source: str) -> None:
        """Select input source."""
        self.send(ActionType.SET_SOURCE, source)

    async def async_browse_media(
        self,
        media_content_type: MediaType | str | None = None,
        media_content_id: str | None = None,
    ) -> BrowseMedia:
        """Return a BrowseMedia instance."""
        if media_content_type == MediaType.CHANNEL and media_content_id:
            return self._browse_radio_fm(media_content_id)
        return self._browse_root()

    def play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs: Any
    ) -> None:
        """Play a piece of media."""
        if media_type == MediaType.MUSIC.value:
            self.send(ActionType.SET_SOURCE, media_id)
        if media_type == MediaType.CHANNEL.value:
            source = media_id.split("-")[0]
            frequency_index = media_id.split("-")[1]
            self.send(ActionType.SET_SOURCE, source, frequency_index)

    def _browse_root(self) -> BrowseMedia:
        sources = self._component.source_list
        media_list = [self._get_browse_media_from_source(source) for source in sources]
        return BrowseMedia(
            title="Sources",
            media_class=MediaClass.APP,
            media_content_id="apps",
            media_content_type=MediaType.APPS,
            can_play=False,
            can_expand=False,
            children=media_list,
        )

    def _browse_radio_fm(self, media_content_id: str) -> BrowseMedia:
        for source in self._component.source_list:
            if source.id == media_content_id:
                return self._browse_channel_from_source(source)
        return None

    def _browse_channel_from_source(self, source: Source) -> BrowseMedia:
        children = source.children_list
        media_list = [
            self._get_browse_media_fm(source, index, child)
            for index, child in enumerate(children, start=1)
        ]
        return BrowseMedia(
            title=source.name,
            media_class=MediaClass.CHANNEL,
            media_content_id=source.id,
            media_content_type=MediaType.CHANNELS,
            can_play=not media_list,
            can_expand=bool(media_list),
            children=media_list,
        )

    def _get_browse_media_fm(
        self, source: Source, index: int, name: str
    ) -> BrowseMedia:
        return BrowseMedia(
            media_class=MediaClass.CHANNEL,
            media_content_type=MediaClass.CHANNEL,
            media_content_id=source.id + "-" + str(index),
            title=name,
            can_play=True,
            can_expand=False,
        )

    def _get_browse_media_from_source(self, source: Source) -> BrowseMedia:
        return BrowseMedia(
            media_class=source.media_class,
            media_content_type=source.media_content_type,
            media_content_id=source.id,
            title=source.name,
            can_play=not source.children_list,
            can_expand=bool(source.children_list),
        )
