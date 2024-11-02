from .ss_audio_rca_mapper import SsAudioRcaMapper
from .ss_audio_radio_fm_mapper import SsAudioRadioFmMapper
from .ss_audio_zone_mapper import SsAudioZoneMapper
from .ss_audio_bluetooth_mapper import SsAudioBluetoothMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_media_player import VimarMediaPlayer
from ...model.enum.sftype_enum import SfType


class AudioMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarMediaPlayer]:
        sftype = SfType.AUDIO.value
        audios = [component for component in components if component.sftype == sftype]
        sources = AudioMapper.remove_sources(audios)
        source_components = [AudioMapper.from_obj(source) for source in sources]
        audio_components = [
            AudioMapper.from_obj(audio, source_components) for audio in audios
        ]
        return source_components + audio_components

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarMediaPlayer:
        mapper = AudioMapper.get_mapper(component)
        return mapper.from_obj(component, *args)

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
        return NotImplementedError()

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
