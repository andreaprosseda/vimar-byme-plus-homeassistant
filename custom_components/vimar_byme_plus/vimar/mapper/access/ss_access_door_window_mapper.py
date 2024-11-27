from ...model.repository.user_component import UserComponent
from ...model.component.vimar_cover import VimarCover, CoverEntityFeature
from ...model.enum.sstype_enum import SsType
from ...model.enum.sfetype_enum import SfeType


class SsAccessDoorWindowMapper:
    SSTYPE = SsType.ACCESS_DOOR_WINDOW.value

    def from_obj(self, component: UserComponent, *args) -> VimarCover:
        return VimarCover(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            area=component.ambient.name,
            current_cover_position=self.current_position(component),
            is_closed=self.is_closed(component),
            is_closing=False,
            is_opening=False,
            supported_features=self.get_supported_features(component),
        )

    def current_position(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return 100 if value == "Off" else 0

    def is_closed(self, component: UserComponent) -> bool | None:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "Off" if value else None

    def get_supported_features(self, component: UserComponent) -> list[CoverEntityFeature]:
        return [CoverEntityFeature.OPEN]
