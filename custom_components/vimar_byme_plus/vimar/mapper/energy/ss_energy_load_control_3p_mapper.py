from .ss_energy_load_control_1p_mapper import SsEnergyLoadControl1pMapper
from ...model.enum.sstype_enum import SsType


class SsEnergyLoadControl3pMapper(SsEnergyLoadControl1pMapper):
    SSTYPE = SsType.ENERGY_LOAD_CONTROL_3P.value
