from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_access_door_window_mapper import SsAccessDoorWindowMapper
from .ss_access_gate_mapper import SsAccessGateMapper
from .ss_access_interface_contact_mapper import SsAccessInterfaceContactMapper


class AccessMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        sftype = SfType.ACCESS.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [AccessMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarComponent]:
        try:
            mapper = AccessMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(__name__, component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsAccessInterfaceContactMapper.SSTYPE:
            return SsAccessInterfaceContactMapper()
        if sstype == SsAccessGateMapper.SSTYPE:
            return SsAccessGateMapper()
        if sstype == SsAccessDoorWindowMapper.SSTYPE:
            return SsAccessDoorWindowMapper()
        raise NotImplementedError
