from ....model.repository.user_component import UserComponent
from ....model.component.vimar_media_player import VimarMediaPlayer, MediaType, MediaPlayerEntityFeature
from ....model.enum.sfetype_enum import SfeType
from ....model.enum.sstype_enum import SsType


class SsAudioRcaMapper:
    SSTYPE = SsType.AUDIO_RCA.value
    
    def from_obj(self, component: UserComponent, *args)-> VimarMediaPlayer:
        return VimarMediaPlayer(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            area=component.ambient.name,
            is_on = True,
            media_content_type = self.get_media_content_type(component),
            source = self.get_source(component),
            supported_features=self.get_supported_features(component)
        )
  
    def get_media_content_type(self, component: UserComponent) -> MediaType | str | None:    
        """Content type of current playing media."""
        return MediaType.MUSIC
    
    def get_source(self, component: UserComponent) -> str | None:
        value = component.get_value(SfeType.STATE_SOURCE_ID)
        return value
    
    def get_supported_features(self, component: UserComponent) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported."""
        return ()