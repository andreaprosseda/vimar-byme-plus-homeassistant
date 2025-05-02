from ...model.component.vimar_cover import CoverEntityFeature, VimarCover
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ..base_mapper import BaseMapper


class SsShutterPositionMapper(BaseMapper):
    SSTYPE = SsType.SHUTTER_POSITION.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarCover]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarCover:
        return VimarCover(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="shutter",
            area=component.ambient.name,
            current_cover_position=self.current_position(component),
            current_tilt_position=self.current_tilt_position(component),
            is_closed=self.is_closed(component),
            is_closing=self.is_closing(component),
            is_opening=self.is_opening(component),
            supported_features=self.get_supported_features(component),
        )

    def current_position(self, component: UserComponent) -> int | None:
        is_changing = self._is_changing(component)
        return self._get_position(component) if not is_changing else None

    def current_tilt_position(self, component: UserComponent) -> int | None:
        return None

    def is_closed(self, component: UserComponent) -> bool | None:
        position = self._get_position(component)
        return position == 100

    def is_closing(self, component: UserComponent) -> bool:
        is_changing = self._is_changing(component)
        position = self._get_position(component)
        return is_changing and position > 50

    def is_opening(self, component: UserComponent) -> bool:
        is_changing = self._is_changing(component)
        position = self._get_position(component)
        return is_changing and position <= 50

    def get_supported_features(
        self, component: UserComponent
    ) -> list[CoverEntityFeature]:
        """Flag media player features that are supported."""
        return [
            CoverEntityFeature.CLOSE,
            CoverEntityFeature.OPEN,
            CoverEntityFeature.SET_POSITION,
            CoverEntityFeature.STOP,
        ]

    def _get_position(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_SHUTTER)
        if not value:
            return None
        if not value.isdigit():
            value = value.replace("Change to ", "")
        return int(value)

    def _is_changing(self, component: UserComponent) -> bool | None:
        value = component.get_value(SfeType.STATE_SHUTTER)
        if value:
            return "Change to " in value
        return None
