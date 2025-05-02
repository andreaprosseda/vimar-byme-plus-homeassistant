from ...model.component.vimar_cover import CoverEntityFeature, VimarCover
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent
from ..base_mapper import BaseMapper


class SsShutterWithoutPositionMapper(BaseMapper):
    SSTYPE = SsType.SHUTTER_WITHOUT_POSITION.value

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
            current_cover_position=None,
            current_tilt_position=None,
            is_closed=None,
            is_closing=None,
            is_opening=None,
            supported_features=self.get_supported_features(component),
        )

    def get_supported_features(
        self, component: UserComponent
    ) -> list[CoverEntityFeature]:
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
