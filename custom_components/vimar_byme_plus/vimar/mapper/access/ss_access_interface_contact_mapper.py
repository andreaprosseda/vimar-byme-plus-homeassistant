from ...model.component.vimar_cover import VimarCover
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsAccessInterfaceContactMapper:
    SSTYPE = SsType.ACCESS_INTERFACE_CONTACT.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarCover]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarCover:
        raise NotImplementedError
