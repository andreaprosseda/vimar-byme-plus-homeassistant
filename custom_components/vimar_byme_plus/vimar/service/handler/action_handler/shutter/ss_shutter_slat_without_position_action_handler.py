from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_shutter_without_position_action_handler import (
    SsShutterWithoutPositionActionHandler,
)

SLAT = SfeType.CMD_SLAT_WITHOUT_POSITION


class SsShutterSlatWithoutPositionActionHandler(SsShutterWithoutPositionActionHandler):
    SSTYPE = SsType.SHUTTER_SLAT_WITHOUT_POSITION.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.OPEN_SLAT:
            return self.get_open_slat_actions(component.id)
        if action_type == ActionType.CLOSE_SLAT:
            return self.get_close_slat_actions(component.id)
        return super().get_actions(component, action_type, *args)

    # NOTE: do not bundle the slat command with the movement command (see #91).
    # On SS_Shutter_SlatWithoutPosition actuators that do not expect the slat
    # action while travelling, the second action is interpreted as a stop: the
    # motor does a short step and the cover never reaches the end position
    # (regression in 3.3.1, see #98). Movement and tilt are sent separately;
    # the tilt is still available through OPEN_TILT / CLOSE_TILT.

    def get_open_slat_actions(self, id: str) -> list[VimarAction]:
        """Open the cover slat."""
        return [self._action(id, SLAT, "Open")]

    def get_close_slat_actions(self, id: str) -> list[VimarAction]:
        """Close cover slat."""
        return [self._action(id, SLAT, "Close")]
