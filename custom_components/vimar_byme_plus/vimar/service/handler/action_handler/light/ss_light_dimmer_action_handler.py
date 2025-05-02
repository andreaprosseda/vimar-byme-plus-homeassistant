from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_light_switch_action_handler import SsLightSwitchActionHandler

ON_OFF = SfeType.CMD_ON_OFF
BRIGHTNESS = SfeType.CMD_BRIGHTNESS


class SsLightDimmerActionHandler(SsLightSwitchActionHandler):
    SSTYPE = SsType.LIGHT_DIMMER.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.ON:
            return self.get_turn_on_actions(component.id, args[0])
        return super().get_actions(component, action_type, *args)

    def get_turn_on_actions(self, id: str, brightness: int) -> list[VimarAction]:
        return [
            self._action(id, ON_OFF, "On"),
            self._action(id, BRIGHTNESS, brightness),
        ]
