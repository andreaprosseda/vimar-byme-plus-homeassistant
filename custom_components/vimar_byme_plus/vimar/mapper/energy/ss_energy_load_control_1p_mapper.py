from ...model.enum.sstype_enum import SsType
from .ss_energy_measure_1p_mapper import SsEnergyMeasure1pMapper


class SsEnergyLoadControl1pMapper(SsEnergyMeasure1pMapper):
    SSTYPE = SsType.ENERGY_LOAD_CONTROL_1P.value
