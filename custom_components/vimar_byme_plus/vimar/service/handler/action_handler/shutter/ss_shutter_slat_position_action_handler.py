from .....model.component.vimar_action import VimarAction
from .....model.component.vimar_component import VimarComponent
from .....model.enum.action_type import ActionType
from .....model.enum.sfetype_enum import SfeType
from .....model.enum.sstype_enum import SsType
from .ss_shutter_position_action_handler import SsShutterPositionActionHandler

SLAT = SfeType.CMD_SLAT


class SsShutterSlatPositionActionHandler(SsShutterPositionActionHandler):
    SSTYPE = SsType.SHUTTER_SLAT_POSITION.value

    def get_actions(
        self, component: VimarComponent, action_type: ActionType, *args
    ) -> list[VimarAction]:
        if action_type == ActionType.OPEN_SLAT:
            return self.get_open_slat_actions(component.id)
        if action_type == ActionType.CLOSE_SLAT:
            return self.get_close_slat_actions(component.id)
        if action_type == ActionType.SET_SLAT_POSITION:
            return self.get_set_slat_position_actions(component.id, args[0])
        return super().get_actions(component, action_type, *args)

    def get_open_cover_actions(self, id: str) -> list[VimarAction]:
        """Raise the blind AND tilt the slats open, in one message.

        Issue #90: on a venetian blind the two are one gesture. Vimar opens
        the slats while the blind rises and closes them while it comes down;
        sending only the travel command left the slats wherever they were, so
        a blind lowered from Home Assistant ended up shut but with the light
        still coming through — something the Vimar app never does.

        One `doaction` carries both, the same way the dimmer already sends
        on + brightness together.
        """
        return [*super().get_open_cover_actions(id), *self.get_open_slat_actions(id)]

    def get_close_cover_actions(self, id: str) -> list[VimarAction]:
        """Lower the blind AND tilt the slats closed. See get_open_cover_actions."""
        return [*super().get_close_cover_actions(id), *self.get_close_slat_actions(id)]

    def get_open_slat_actions(self, id: str) -> list[VimarAction]:
        """Open the cover slat."""
        return [self._action(id, SLAT, "0")]

    def get_close_slat_actions(self, id: str) -> list[VimarAction]:
        """Close cover slat."""
        return [self._action(id, SLAT, "100")]

    def get_set_slat_position_actions(
        self, id: str, position: int
    ) -> list[VimarAction]:
        """Move the cover slat to a specific position."""
        return [self._action(id, SLAT, str(position))]
