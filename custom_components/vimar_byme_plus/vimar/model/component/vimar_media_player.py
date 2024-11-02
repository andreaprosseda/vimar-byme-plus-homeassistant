from enum import Enum
from dataclasses import dataclass
from .vimar_component import VimarComponent


class MediaType(Enum):
    CHANNEL = "channel"
    MUSIC = "music"


class MediaPlayerState(Enum):
    OFF = "off"
    ON = "on"
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    STANDBY = "standby"
    BUFFERING = "buffering"


class MediaPlayerEntityFeature(Enum):
    PAUSE = 1
    SEEK = 2
    VOLUME_SET = 4
    VOLUME_MUTE = 8
    PREVIOUS_TRACK = 16
    NEXT_TRACK = 32

    TURN_ON = 128
    TURN_OFF = 256
    PLAY_MEDIA = 512
    VOLUME_STEP = 1024
    SELECT_SOURCE = 2048
    STOP = 4096
    CLEAR_PLAYLIST = 8192
    PLAY = 16384
    SHUFFLE_SET = 32768
    SELECT_SOUND_MODE = 65536
    BROWSE_MEDIA = 131072
    REPEAT_SET = 262144
    GROUPING = 524288
    MEDIA_ANNOUNCE = 1048576
    MEDIA_ENQUEUE = 2097152

@dataclass
class Source:
    id: str
    name: str

@dataclass
class VimarMediaPlayer(VimarComponent):
    is_on: bool | None
    state: MediaPlayerState | None
    volume_level: float | None
    volume_step: float
    is_volume_muted: bool | None
    media_content_type: MediaType | str | None
    media_title: str | None
    media_artist: str | None
    media_album_name: str | None
    media_album_artist: str | None
    media_track: int | None
    source_id: str | None
    current_source: str | None
    source_list: list[Source] | None
    supported_features: list[MediaPlayerEntityFeature]

    def __init__(
        self,
        id: str,
        name: str,
        device_group: str,
        device_name: str,
        area: str,
        is_on: bool | None = None,
        state: MediaPlayerState | None = None,
        volume_level: float | None = None,
        volume_step: float = None,
        is_volume_muted: bool | None = None,
        media_content_type: MediaType | str | None = None,
        media_title: str | None = None,
        media_artist: str | None = None,
        media_album_name: str | None = None,
        media_album_artist: str | None = None,
        media_track: int | None = None,
        source_id: str | None = None,
        current_source: str | None = None,
        source_list: list[Source] | None = None,
        supported_features: MediaPlayerEntityFeature = None,
    ) -> None:
        super().__init__(id, name, device_group, device_name, area)
        self.is_on = is_on
        self.state = state
        self.volume_level = volume_level
        self.volume_step = volume_step
        self.is_volume_muted = is_volume_muted
        self.media_content_type = media_content_type
        self.media_title = media_title
        self.media_artist = media_artist
        self.media_album_name = media_album_name
        self.media_album_artist = media_album_artist
        self.media_track = media_track
        self.source_id = source_id
        self.current_source = current_source
        self.source_list = source_list
        self.supported_features = supported_features

    @staticmethod
    def get_table_header() -> list:
        return ["Area", "Name", "Type", "isOn", "Source", "Volume"]

    def to_table(self) -> list:
        return [
            self.area,
            self.name,
            self.device_name,
            self.is_on,
            self.current_source,
            int(self.volume_level * 100) if self.volume_level else None,
        ]
