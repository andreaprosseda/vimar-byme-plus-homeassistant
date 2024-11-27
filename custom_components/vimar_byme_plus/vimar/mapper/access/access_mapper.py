from ...model.repository.user_component import UserComponent
from ...model.component.vimar_cover import VimarCover, CoverEntityFeature
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType

SFTYPE = SfType.ACCESS.value


class AccessMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarCover]:
        return [AccessMapper.from_obj(c) for c in components if c.sftype == SFTYPE]

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarCover:
        return VimarCover(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=AccessMapper.device_class(component),
            area=component.ambient.name,
            current_cover_position=AccessMapper.current_position(component),
            is_closed=AccessMapper.is_closed(component),
            is_closing=False,
            is_opening=False,
            supported_features=AccessMapper.get_supported_features(component),
        )

    @staticmethod
    def device_class(component: UserComponent) -> str:
        if component.sstype == "SS_Access_Gate":
            return "gate"
        return "door"

    @staticmethod
    def current_position(component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return 100 if value == "Off" else 0

    @staticmethod
    def is_closed(component: UserComponent) -> bool | None:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "Off" if value else None

    @staticmethod
    def get_supported_features(component: UserComponent) -> list[CoverEntityFeature]:
        """Flag media player features that are supported."""
        return [CoverEntityFeature.OPEN]
