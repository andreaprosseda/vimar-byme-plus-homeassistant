from .ss_energy_load_control_1p_mapper import SsEnergyLoadControl1pMapper
from ...model.enum.sstype_enum import SsType


class SsEnergyLoadControl1pProductionMapper(SsEnergyLoadControl1pMapper):
    SSTYPE = SsType.ENERGY_LOAD_CONTROL_1P_PRODUCTION.value

    # SFE_State_GlobalActivePowerExchange
    # SFE_State_GlobalActivePowerProduct
    # SFE_State_GlobalActivePowerConsumption
