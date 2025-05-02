from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_button import VimarButton
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType

REAL_TIME = SfeType.CMD_TIMED_DYNAMIC_MODE


class SensorActionHandler:
    # def get_actions(
    #     self, component: VimarComponent, action_type: ActionType, *args
    # ) -> list[VimarAction]:
    #     handler = self.get_handler(component)
    #     return handler.get_actions(component, action_type, *args)

    # @staticmethod
    # def get_handler(component: VimarComponent) -> HandlerInterface:
    #     sstype = component.device_name
    #     if sstype == SsSensorPowerActionHandler.SSTYPE:
    #         return SsSensorPowerActionHandler()
    #     raise NotImplementedError

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.PRESS:
            return self.get_press_actions(component)
        raise NotImplementedError

    def get_press_actions(self, component: VimarButton) -> list[VimarAction]:
        if "real_time" in component.id:
            return [
                VimarAction(
                    idsf=component.main_id, sfetype=REAL_TIME.value, value="Start"
                )
            ]
        raise NotImplementedError
