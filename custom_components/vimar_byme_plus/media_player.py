"""Platform for media player integration."""

from __future__ import annotations
from functools import reduce

from homeassistant.components.media_player import (
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
from .vimar.model.component.vimar_media_player import VimarMediaPlayer
from .vimar.utils.logger import log_debug
from .vimar.model.enum.action_type import ActionType


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CoordinatorConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up component based on a config entry."""
    coordinator = entry.runtime_data
    components = coordinator.data.get_audios()
    entities = [MediaPlayer(coordinator, component) for component in components]
    log_debug(__name__, f"Media Players found: {len(entities)}")
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

    def toggle(self) -> None:
        """Toggle the power on the media player."""
        self.send(ActionType.TOGGLE)
