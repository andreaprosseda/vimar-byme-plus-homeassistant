from ...model.component.vimar_component import VimarComponent
from ...model.enum.sftype_enum import SfType
from ...model.integration_options import IntegrationOptions
from ...model.repository.user_component import UserComponent
from ...utils.filtering import flat
from ...utils.logger import not_implemented
from ..base_mapper import BaseMapper
from .ss_energy_load_control_1p_mapper import SsEnergyLoadControl1pMapper
from .ss_energy_load_control_1p_production_mapper import (
    SsEnergyLoadControl1pProductionMapper,
)
from .ss_energy_load_control_3p_mapper import SsEnergyLoadControl3pMapper
from .ss_energy_load_control_3p_production_mapper import (
    SsEnergyLoadControl3pProductionMapper,
)
from .ss_energy_load_mapper import SsEnergyLoadMapper
from .ss_energy_measure_1p_mapper import SsEnergyMeasure1pMapper
from .ss_energy_measure_3p_mapper import SsEnergyMeasure3pMapper
from .ss_energy_measure_counter_mapper import SsEnergyMeasureCounterMapper


class EnergyMapper:
    @staticmethod
    def from_list(
        components: list[UserComponent],
        options: IntegrationOptions | None = None,
    ) -> list[VimarComponent]:
        opts = options or IntegrationOptions()
        sftype = SfType.ENERGY.value
        energies = [component for component in components if component.sftype == sftype]
        components_out = [EnergyMapper.from_obj(energy, opts) for energy in energies]
        return flat(components_out)

    @staticmethod
    def from_obj(
        component: UserComponent, options: IntegrationOptions | None = None
    ) -> list[VimarComponent]:
        opts = options or IntegrationOptions()
        try:
            mapper = EnergyMapper.get_mapper(component)
            if isinstance(mapper, SsEnergyMeasureCounterMapper):
                counter_type = opts.counter_types.get(str(component.idsf))
                return mapper.from_obj(component, counter_type)
            return mapper.from_obj(component)
        except NotImplementedError:
            not_implemented(__name__, component)
            return []

    @staticmethod
    def get_mapper(component: UserComponent) -> BaseMapper:
        sstype = component.sstype
        if sstype == SsEnergyLoadMapper.SSTYPE:
            return SsEnergyLoadMapper()
        if sstype == SsEnergyLoadControl1pMapper.SSTYPE:
            return SsEnergyLoadControl1pMapper()
        if sstype == SsEnergyLoadControl1pProductionMapper.SSTYPE:
            return SsEnergyLoadControl1pProductionMapper()
        if sstype == SsEnergyLoadControl3pMapper.SSTYPE:
            return SsEnergyLoadControl3pMapper()
        if sstype == SsEnergyLoadControl3pProductionMapper.SSTYPE:
            return SsEnergyLoadControl3pProductionMapper()
        if sstype == SsEnergyMeasure1pMapper.SSTYPE:
            return SsEnergyMeasure1pMapper()
        if sstype == SsEnergyMeasure3pMapper.SSTYPE:
            return SsEnergyMeasure3pMapper()
        if sstype == SsEnergyMeasureCounterMapper.SSTYPE:
            return SsEnergyMeasureCounterMapper()
        raise NotImplementedError
