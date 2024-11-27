from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_cover import VimarCover, CoverEntityFeature
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType


class SsShutterWithoutPositionMapper(BaseMapper):
    SFTYPE = SfType.SHUTTER.value
    SSTYPE = SsType.SHUTTER_WITHOUT_POSITION.value

    def from_obj(self, component: UserComponent, *args) -> VimarCover:
        return VimarCover(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="shutter",
            area=component.ambient.name,
            current_cover_position=self.current_position(component),
            is_closed=self.is_closed(component),
            is_closing=self.is_closing(component),
            is_opening=self.is_opening(component),
            supported_features=self.get_supported_features(component),
        )

    def current_position(self, component: UserComponent) -> int | None:
        return None

    def is_closed(self, component: UserComponent) -> bool | None:
        return None

    def is_closing(self, component: UserComponent) -> bool:
        return None
        # is_changing = self._is_changing(component)
        # return is_changing

    def is_opening(self, component: UserComponent) -> bool:
        return None
        # is_changing = self._is_changing(component)
        # return is_changing

    def get_supported_features(self, component: UserComponent) -> list[CoverEntityFeature]:
        """Flag media player features that are supported."""
        return [
            CoverEntityFeature.CLOSE,
            CoverEntityFeature.OPEN,
            CoverEntityFeature.STOP,
        ]

    def _is_changing(self, component: UserComponent) -> bool | None:
        value = component.get_value(SfeType.STATE_SHUTTER_WITHOUT_POSITION)
        if value:
            return value == "Moving"
        return None
