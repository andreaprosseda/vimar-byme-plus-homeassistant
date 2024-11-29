from .ss_audio_rca_mapper import SsAudioRcaMapper
from .ss_audio_radio_fm_mapper import SsAudioRadioFmMapper
from .ss_audio_zone_mapper import SsAudioZoneMapper
from .ss_audio_bluetooth_mapper import SsAudioBluetoothMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_media_player import VimarMediaPlayer
from ...model.enum.sftype_enum import SfType
from ...utils.logger import not_implemented
from ...utils.filtering import filter_none


class AudioMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarMediaPlayer]:
        sftype = SfType.AUDIO.value
        audios = [component for component in components if component.sftype == sftype]
        sources = AudioMapper.remove_sources(audios)
        components = AudioMapper.get_components(audios, sources)
        return filter_none(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarMediaPlayer:
        try:
            mapper = AudioMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return None

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsAudioRadioFmMapper.SSTYPE:
            return SsAudioRadioFmMapper()
        if sstype == SsAudioRcaMapper.SSTYPE:
            return SsAudioRcaMapper()
        if sstype == SsAudioZoneMapper.SSTYPE:
            return SsAudioZoneMapper()
        if sstype == SsAudioBluetoothMapper.SSTYPE:
            return SsAudioBluetoothMapper()
        raise NotImplementedError

    @staticmethod
    def get_components(
        audio_list: list[UserComponent], source_list: list[UserComponent]
    ) -> list[VimarMediaPlayer]:
        sources = [AudioMapper.from_obj(source) for source in source_list]
        audios = [AudioMapper.from_obj(audio, sources) for audio in audio_list]
        return sources + audios

    @staticmethod
    def remove_sources(components: list[UserComponent]) -> list[UserComponent]:
        sources = [
            SsAudioRcaMapper.SSTYPE,
            SsAudioRadioFmMapper.SSTYPE,
            SsAudioBluetoothMapper.SSTYPE,
        ]
        result = []
        for component in components:
            if component.sstype in sources:
                result.append(component)
                components.remove(component)
        return result
