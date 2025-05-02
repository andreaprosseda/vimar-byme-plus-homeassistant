from ...model.enum.sstype_enum import SsType
from .ss_energy_load_control_1p_production_mapper import (
    SsEnergyLoadControl1pProductionMapper,
)


class SsEnergyLoadControl3pProductionMapper(SsEnergyLoadControl1pProductionMapper):
    SSTYPE = SsType.ENERGY_LOAD_CONTROL_3P_PRODUCTION.value
