from ...model.repository.user_component import UserComponent
from ...model.component.vimar_cover import VimarCover
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType

SFTYPE = SfType.SHUTTER.value


class ShutterMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarCover]:
        data = []
        for component in components:
            if component.sftype == SFTYPE:
                data.append(ShutterMapper.from_obj(component))
        return data

    @staticmethod
    def from_obj(component: UserComponent) -> VimarCover:
        return VimarCover(
            id=component.idsf,
            name=component.name,
            device_name=component.sftype,
            area=component.ambient.name,
            current_cover_position=ShutterMapper.current_position(component),
            is_closed=ShutterMapper.is_closed(component),
            is_closing=ShutterMapper.is_closing(component),
            is_opening=ShutterMapper.is_opening(component),
        )

    @staticmethod
    def current_position(component: UserComponent) -> int | None:
        return ShutterMapper._get_position(component)

    @staticmethod
    def is_closed(component: UserComponent) -> bool | None:
        position = ShutterMapper._get_position(component)
        return position == 100 if position else None

    @staticmethod
    def is_closing(component: UserComponent) -> bool:
        is_changing = ShutterMapper._is_changing(component)
        value = component.get_value(SfeType.STATE_SHUTTER)
        return is_changing and value > 50

    @staticmethod
    def is_opening(component: UserComponent) -> bool:
        is_changing = ShutterMapper._is_changing(component)
        value = component.get_value(SfeType.STATE_SHUTTER)
        return is_changing and value <= 50

    @staticmethod
    def _get_position(component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_SHUTTER)
        try:
            clean_value = value.replace("Change to ", "")
            return int(clean_value)
        except Exception:
            return None

    @staticmethod
    def _is_changing(component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_SHUTTER)
        return "Change to " in value
