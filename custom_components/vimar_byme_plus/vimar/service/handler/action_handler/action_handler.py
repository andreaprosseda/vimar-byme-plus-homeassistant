from ....model.component.vimar_action import VimarAction
from ....model.component.vimar_component import VimarComponent
from ....model.enum.action_type import ActionType
from ....model.enum.sftype_enum import SfType
from .access.access_action_handler import AccessActionHandler
from .audio.audio_action_handler import AudioActionHandler
from .automation.automation_action_handler import AutomationActionHandler
from .base_action_handler import BaseActionHandler
from .clima.clima_action_handler import ClimaActionHandler
from .energy.energy_action_handler import EnergyActionHandler
from .irrigation.irrigation_action_handler import IrrigationActionHandler
from .light.light_action_handler import LightActionHandler
from .scene.scene_action_handler import SceneActionHandler
from .scene_activator.scene_activator_action_handler import SceneActivatorActionHandler
from .sensor.sensor_action_handler import SensorActionHandler
from .shutter.shutter_action_handler import ShutterActionHandler


class ActionHandler:
    def __init__(self, gateway_id: str) -> None:
        self._gateway_id = gateway_id

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        handler = self._get_handler(component.device_group)
        return handler.get_actions(component, action_type, *args)

    def _get_handler(self, device_group: str) -> BaseActionHandler:
        gw = self._gateway_id
        group = SfType(device_group)
        match group:
            case SfType.ACCESS:
                return AccessActionHandler(gw)
            case SfType.AUDIO:
                return AudioActionHandler(gw)
            case SfType.AUTOMATION:
                return AutomationActionHandler(gw)
            case SfType.CLIMA:
                return ClimaActionHandler(gw)
            case SfType.ENERGY:
                return EnergyActionHandler(gw)
            case SfType.IRRIGATION:
                return IrrigationActionHandler(gw)
            case SfType.LIGHT:
                return LightActionHandler(gw)
            case SfType.SCENE:
                return SceneActionHandler(gw)
            case SfType.SCENE_ACTIVATOR:
                return SceneActivatorActionHandler(gw)
            case SfType.SENSOR:
                return SensorActionHandler(gw)
            case SfType.SHUTTER:
                return ShutterActionHandler(gw)
            case _:
                raise NotImplementedError
