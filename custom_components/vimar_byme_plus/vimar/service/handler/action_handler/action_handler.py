from .base_action_handler import BaseActionHandler
from .access.access_action_handler import AccessActionHandler
from .audio.audio_action_handler import AudioActionHandler
from .clima.clima_action_handler import ClimaActionHandler
from .light.light_action_handler import LightActionHandler
from .shutter.shutter_action_handler import ShutterActionHandler
from ....model.enum.action_type import ActionType
from ....model.component.vimar_action import VimarAction
from ....model.component.vimar_component import VimarComponent
from ....model.enum.sftype_enum import SfType


class ActionHandler:
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = ActionHandler._get_handler(component.device_group)
        actions = handler.get_actions(component, action_type, *args)
        # self.save(actions)
        return actions

    @staticmethod
    def _get_handler(device_group: str) -> BaseActionHandler:
        group = SfType(device_group)
        match group:
            case SfType.ACCESS:
                return AccessActionHandler()
            case SfType.AUDIO:
                return AudioActionHandler()
            case SfType.CLIMA:
                return ClimaActionHandler()
            case SfType.LIGHT:
                return LightActionHandler()
            case SfType.SHUTTER:
                return ShutterActionHandler()
            case _:
                raise NotImplementedError
