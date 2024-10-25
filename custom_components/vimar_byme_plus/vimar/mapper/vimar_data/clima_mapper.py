from ...model.repository.user_component import UserComponent
from ...model.component.vimar_climate import (
    VimarClimate,
    HVACMode,
    HVACAction,
    PresetMode,
    ChangeOverMode,
)
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType
from ...utils.logger import log_info

SFTYPE = SfType.CLIMA.value


class ClimaMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarClimate]:
        return [ClimaMapper.from_obj(c) for c in components if c.sftype == SFTYPE]

    @staticmethod
    def from_obj(component: UserComponent) -> VimarClimate:
        return VimarClimate(
            id=component.idsf,
            name=component.name,
            device_name=component.sftype,
            area=component.ambient.name,
            current_temperature=ClimaMapper.current_temperature(component),
            min_temp=ClimaMapper.min_temp(component),
            max_temp=ClimaMapper.max_temp(component),
            target_temperature=ClimaMapper.target_temperature(component),
            target_temperature_step=ClimaMapper.target_temperature_step(component),
            target_temperature_high=ClimaMapper.target_temperature_high(component),
            target_temperature_low=ClimaMapper.target_temperature_low(component),
            hvac_mode=ClimaMapper.hvac_mode(component),
            hvac_modes=ClimaMapper.hvac_modes(component),
            hvac_action=ClimaMapper.hvac_action(component),
            preset_mode=ClimaMapper.preset_mode(component),
            preset_modes=ClimaMapper.preset_modes(component),
            fan_mode=ClimaMapper.fan_mode(component),
            fan_modes=ClimaMapper.fan_modes(component),
            swing_mode=ClimaMapper.swing_mode(component),
            swing_modes=ClimaMapper.swing_modes(component),
            # supported_features=ClimaMapper.supported_features(component),
            current_humidity=ClimaMapper.current_humidity(component),
            target_humidity=ClimaMapper.target_humidity(component),
            min_humidity=ClimaMapper.min_humidity(component),
            max_humidity=ClimaMapper.max_humidity(component),
        )

    @staticmethod
    def current_temperature(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_AMBIENT_TEMPERATURE)
        return float(value) if value else None

    @staticmethod
    def min_temp(component: UserComponent) -> float:
        return 4.0

    @staticmethod
    def max_temp(component: UserComponent) -> float:
        return 40.0

    @staticmethod
    def target_temperature(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_AMBIENT_SETPOINT)
        return float(value) if value else None

    @staticmethod
    def target_temperature_step(component: UserComponent) -> float | None:
        return 0.1

    @staticmethod
    def target_temperature_low(component: UserComponent) -> float | None:
        return ClimaMapper.min_temp(component)

    @staticmethod
    def target_temperature_high(component: UserComponent) -> float | None:
        return ClimaMapper.max_temp(component)

    @staticmethod
    def hvac_mode(component: UserComponent) -> HVACMode | None:
        value = component.get_value(SfeType.STATE_HVAC_MODE)
        hvac_mode = HVACMode.get_hvac_mode(value)
        if hvac_mode:
            return hvac_mode

        value = component.get_value(SfeType.STATE_CHANGE_OVER_MODE)
        change_over_mode = ChangeOverMode.get_change_over_mode(value)
        if not change_over_mode:
            return None
        if change_over_mode == ChangeOverMode.HEAT:
            return HVACMode.HEAT
        if change_over_mode == ChangeOverMode.COOL:
            return HVACMode.COOL
        return None

    @staticmethod
    def hvac_modes(component: UserComponent) -> list[HVACMode]:
        return list(HVACMode)

    @staticmethod
    def hvac_action(component: UserComponent) -> HVACAction | None:
        value = component.get_value(SfeType.STATE_OUT_STATUS)
        hvac_action = HVACAction.get_hvac_action(value)
        hvac_mode = component.get_value(SfeType.STATE_HVAC_MODE)
        if hvac_mode != "Off" and hvac_action == HVACAction.OFF:
            log_info(__name__, "Climate IDLE")
            return HVACAction.IDLE
        log_info(__name__, f"Climate {hvac_action}")
        return hvac_action

    @staticmethod
    def preset_mode(component: UserComponent) -> PresetMode | None:
        # return None
        value = component.get_value(SfeType.STATE_HVAC_MODE)
        return PresetMode.get_preset_mode(value)

    @staticmethod
    def preset_modes(component: UserComponent) -> list[PresetMode] | None:
        # return None
        return list(PresetMode)

    @staticmethod
    def fan_mode(component: UserComponent) -> str | None:
        fan_mode = component.get_value(SfeType.STATE_FAN_MODE)
        if not fan_mode:
            return None
        if fan_mode == "Automatic":
            return "auto"
        fan_speed = component.get_value(SfeType.STATE_FAN_SPEED_3V)
        if fan_speed == "V1":
            return "low"
        if fan_speed == "V2":
            return "medium"
        if fan_speed == "V3":
            return "high"
        return None

    @staticmethod
    def fan_modes(component: UserComponent) -> list[str] | None:
        return ["low", "medium", "high", "auto"]

    @staticmethod
    def swing_mode(component: UserComponent) -> str | None:
        return None

    @staticmethod
    def swing_modes(component: UserComponent) -> list[str] | None:
        return None

    # @staticmethod
    # def supported_features(component: UserComponent) -> ClimateEntityFeature:
    #     pass

    @staticmethod
    def current_humidity(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_HUMIDITY)
        return float(value) if value else None

    @staticmethod
    def target_humidity(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_HUMIDITY_SETPOINT)
        return float(value) if value else None
        return None

    @staticmethod
    def min_humidity(component: UserComponent) -> float:
        return 20.0

    @staticmethod
    def max_humidity(component: UserComponent) -> float:
        return 99.0
