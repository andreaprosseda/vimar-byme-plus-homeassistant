from ....model.repository.user_component import UserComponent
from ....model.component.vimar_cover import VimarCover
from ....model.enum.sftype_enum import SfType
from ....model.enum.sfetype_enum import SfeType
from ....model.enum.sstype_enum import SsType
from ..base_mapper import BaseMapper


class SsShutterPositionMapper(BaseMapper):
    SFTYPE = SfType.SHUTTER.value
    SSTYPE = SsType.SHUTTER_POSITION.value
    
    def from_obj(self, component: UserComponent, *args)-> VimarCover:
        return VimarCover(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sftype,
            area=component.ambient.name,
            current_cover_position=self.current_position(component),
            is_closed=self.is_closed(component),
            is_closing=self.is_closing(component),
            is_opening=self.is_opening(component),
        )

    def current_position(self, component: UserComponent) -> int | None:
        return self._get_position(component)

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

    def _get_position(self, component: UserComponent) -> int | None:
        value = component.get_value(SfeType.STATE_SHUTTER)
        try:
            clean_value = value.replace("Change to ", "")
            return int(clean_value)
        except Exception:
            return None

    def _is_changing(self, component: UserComponent) -> bool | None:
        value = component.get_value(SfeType.STATE_SHUTTER)
        if value:
            return "Change to " in value
        return None