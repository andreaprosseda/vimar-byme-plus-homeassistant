from .ss_access_door_window_mapper import SsAccessDoorWindowMapper
from .ss_access_gate_mapper import SsAccessGateMapper
from ..base_mapper import BaseMapper
from ...model.repository.user_component import UserComponent
from ...model.component.vimar_cover import VimarCover
from ...model.enum.sftype_enum import SfType


class AccessMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarCover]:
        sftype = SfType.ACCESS.value
        shutters = [component for component in components if component.sftype == sftype]
        return [AccessMapper.from_obj(shutter) for shutter in shutters]

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarCover:
        mapper = AccessMapper.get_mapper(component)
        return mapper.from_obj(component, *args)

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsAccessGateMapper.SSTYPE:
            return SsAccessGateMapper()
        if sstype == SsAccessDoorWindowMapper.SSTYPE:
            return SsAccessDoorWindowMapper()
        raise NotImplementedError
