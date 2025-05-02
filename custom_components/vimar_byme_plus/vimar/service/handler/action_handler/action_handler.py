from ....model.component.vimar_action import VimarAction
from ....model.component.vimar_component import VimarComponent
from ....model.enum.action_type import ActionType
from ....model.enum.sftype_enum import SfType
from .access.access_action_handler import AccessActionHandler
from .audio.audio_action_handler import AudioActionHandler
from .automation.automation_action_handler import AutomationActionHandler
from .base_action_handler import BaseActionHandler
from .clima.clima_action_handler import ClimaActionHandler
from .irrigation.irrigation_action_handler import IrrigationActionHandler
from .light.light_action_handler import LightActionHandler
from .scene.scene_action_handler import SceneActionHandler
from .scene_activator.scene_activator_action_handler import SceneActivatorActionHandler
from .sensor.sensor_action_handler import SensorActionHandler
from .shutter.shutter_action_handler import ShutterActionHandler


class ActionHandler:
    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = ActionHandler._get_handler(component.device_group)
        return handler.get_actions(component, action_type, *args)

    @staticmethod
    def _get_handler(device_group: str) -> BaseActionHandler:
        group = SfType(device_group)
        match group:
            case SfType.ACCESS:
                return AccessActionHandler()
            case SfType.AUDIO:
                return AudioActionHandler()
            case SfType.AUTOMATION:
                return AutomationActionHandler()
            case SfType.CLIMA:
                return ClimaActionHandler()
            case SfType.IRRIGATION:
                return IrrigationActionHandler()
            case SfType.LIGHT:
                return LightActionHandler()
            case SfType.SCENE:
                return SceneActionHandler()
            case SfType.SCENE_ACTIVATOR:
                return SceneActivatorActionHandler()
            case SfType.SENSOR:
                return SensorActionHandler()
            case SfType.SHUTTER:
                return ShutterActionHandler()
            case _:
                raise NotImplementedError
