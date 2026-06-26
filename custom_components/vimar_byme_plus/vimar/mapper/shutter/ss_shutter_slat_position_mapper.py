from ...model.component.vimar_cover import CoverEntityFeature
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from .ss_shutter_position_mapper import SsShutterPositionMapper


class SsShutterSlatPositionMapper(SsShutterPositionMapper):
    SSTYPE = SsType.SHUTTER_SLAT_POSITION.value

    def get_supported_features(
        self, component: UserComponent
    ) -> list[CoverEntityFeature]:
        """Flag media player features that are supported."""
        features: list = super().get_supported_features(component)
        features.extend(
            [
                CoverEntityFeature.CLOSE_TILT,
                CoverEntityFeature.OPEN_TILT,
                CoverEntityFeature.SET_TILT_POSITION,
            ]
        )
        return features

    def current_position(self, component: UserComponent, *args) -> int | None:
        position = super().current_position(component, *args)
        return self._normalize_closed_position(component, position, *args)

    def current_tilt_position(self, component: UserComponent, *args) -> int | None:
        is_tilt_changing = self._is_tilt_changing(component)
        return self._get_tilt_position(component) if not is_tilt_changing else None

    def is_closed(self, component: UserComponent, *args) -> bool | None:
        position = self._get_position(component)
        if not self._is_changing(component):
            position = self._normalize_closed_position(component, position, *args)
        return position == 100

    def _normalize_closed_position(
        self, component: UserComponent, position: int | None, *args
    ) -> int | None:
        if position is None or not component.get_value(SfeType.STATE_SLAT):
            return position
        tolerance = int(getattr(args[0], "tilt_tolerance", 0)) if args else 0
        if tolerance >= 0 and position >= 100 - tolerance:
            return 100
        return position

    def _get_tilt_position(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_SLAT)
        if not value:
            return None
        if not value.isdigit():
            value = value.replace("Change to ", "")
        return int(value)

    def _is_tilt_changing(self, component: UserComponent) -> bool | None:
        value = component.get_value(SfeType.STATE_SLAT)
        if value:
            return "Change to " in value
        return None
