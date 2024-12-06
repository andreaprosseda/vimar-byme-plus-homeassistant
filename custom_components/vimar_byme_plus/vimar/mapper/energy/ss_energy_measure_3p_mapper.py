from .ss_energy_measure_1p_mapper import SsEnergyMeasure1pMapper
from ...model.enum.sstype_enum import SsType


class SsEnergyMeasure3pMapper(SsEnergyMeasure1pMapper):
    SSTYPE = SsType.ENERGY_MEASURE_3P.value
