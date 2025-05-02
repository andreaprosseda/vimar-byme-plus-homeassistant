from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from ..base_action_handler import HandlerInterface
from .ss_audio_bluetooth_action_handler import SsAudioBluetoothActionHandler
from .ss_audio_radio_fm_action_handler import SsAudioRadioFmActionHandler
from .ss_audio_rca_action_handler import SsAudioRcaActionHandler
from .ss_audio_zone_action_handler import SsAudioZoneActionHandler


class AudioActionHandler:
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = self.get_handler(component)
        return handler.get_actions(component, action_type, *args)

    @staticmethod
    def get_handler(component: VimarComponent) -> HandlerInterface:
        sstype = component.device_name
        if sstype == SsAudioBluetoothActionHandler.SSTYPE:
            return SsAudioBluetoothActionHandler()
        if sstype == SsAudioRadioFmActionHandler.SSTYPE:
            return SsAudioRadioFmActionHandler()
        if sstype == SsAudioRcaActionHandler.SSTYPE:
            return SsAudioRcaActionHandler()
        if sstype == SsAudioZoneActionHandler.SSTYPE:
            return SsAudioZoneActionHandler()
        raise NotImplementedError
