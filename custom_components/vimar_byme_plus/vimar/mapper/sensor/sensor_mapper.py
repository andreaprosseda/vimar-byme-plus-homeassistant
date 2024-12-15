from ...model.component.vimar_switch import VimarSwitch
from ...model.enum.sftype_enum import SfType
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_sensor_interface_contact_mapper import SsSensorInterfaceContactMapper


class SensorMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarSwitch]:
        sftype = SfType.SENSOR.value
        shutters = [component for component in components if component.sftype == sftype]
        components = [SensorMapper.from_obj(shutter) for shutter in shutters]
        return flat(components)

    @staticmethod
    def from_obj(component: UserComponent, *args) -> list[VimarSwitch]:
        try:
            mapper = SensorMapper.get_mapper(component)
            return mapper.from_obj(component, *args)
        except NotImplementedError:
            not_implemented(component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsSensorInterfaceContactMapper.SSTYPE:
            return SsSensorInterfaceContactMapper()
        raise NotImplementedError
