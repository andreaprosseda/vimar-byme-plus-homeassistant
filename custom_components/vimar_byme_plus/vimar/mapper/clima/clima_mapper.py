from ...model.repository.user_component import UserComponent
from ...model.component.vimar_component import VimarComponent
from ...model.component.vimar_climate import (
    VimarClimate,
    HVACMode,
    HVACAction,
    FanMode,
    ClimateEntityFeature,
    PresetMode,
)
from ...model.enum.sftype_enum import SfType
from ...model.enum.sfetype_enum import SfeType


class ClimaMapper:
    @staticmethod
    def from_list(components: list[UserComponent]) -> list[VimarComponent]:
        SFTYPE = SfType.CLIMA.value
        return [ClimaMapper.from_obj(c) for c in components if c.sftype == SFTYPE]

    @staticmethod
    def from_obj(component: UserComponent, *args) -> VimarClimate:
        return VimarClimate(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="climate",
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
            supported_features=ClimaMapper.supported_features(component),
            current_humidity=ClimaMapper.current_humidity(component),
            target_humidity=ClimaMapper.target_humidity(component),
            min_humidity=ClimaMapper.min_humidity(component),
            max_humidity=ClimaMapper.max_humidity(component),
            on_behaviour=ClimaMapper.on_behaviour(component),
            off_behaviour=ClimaMapper.off_behaviour(component),
        )

    @staticmethod
    def current_temperature(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_AMBIENT_TEMPERATURE)
        return float(value) if value else None

    @staticmethod
    def target_temperature(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_AMBIENT_SETPOINT)
        return float(value) if value else None

    @staticmethod
    def hvac_mode(component: UserComponent) -> HVACMode | None:
        value = component.get_value(SfeType.STATE_HVAC_MODE)
        return HVACMode.get_hvac_mode(value)

    @staticmethod
    def hvac_modes(component: UserComponent) -> list[HVACMode]:
        return [HVACMode.OFF, HVACMode.AUTO]

    @staticmethod
    def hvac_action(component: UserComponent) -> HVACAction | None:
        hvac_mode = component.get_value(SfeType.STATE_HVAC_MODE)
        hvac_action = ClimaMapper._get_hvac_action(component)
        if hvac_mode != "Off" and hvac_action == HVACAction.OFF:
            return HVACAction.IDLE
        return hvac_action

    @staticmethod
    def preset_mode(component: UserComponent) -> str | None:
        value = component.get_value(SfeType.STATE_HVAC_MODE)
        mode = PresetMode.get_preset_mode(value)
        return mode.vimar_value if mode else None

    @staticmethod
    def preset_modes(component: UserComponent) -> list[str] | None:
        mode = ClimaMapper.preset_mode(component)
        return PresetMode.get_group_values(mode)

    @staticmethod
    def fan_mode(component: UserComponent) -> FanMode | None:
        mode = ClimaMapper.hvac_mode(component)
        fan_mode = component.get_value(SfeType.STATE_FAN_MODE)
        fan_speed = component.get_value(SfeType.STATE_FAN_SPEED_3V)
        mode = FanMode.get_fan_mode(fan_mode)
        speed = FanMode.get_fan_mode(fan_speed)
        return mode if mode else speed

    @staticmethod
    def fan_modes(component: UserComponent) -> list[FanMode] | None:
        return list(FanMode)

    @staticmethod
    def supported_features(component: UserComponent) -> list[ClimateEntityFeature]:
        features = [
            ClimateEntityFeature.TARGET_TEMPERATURE,
            ClimateEntityFeature.TURN_OFF,
            ClimateEntityFeature.PRESET_MODE,
        ]
        hvac_action = ClimaMapper._get_hvac_action(component)
        if hvac_action and hvac_action == HVACAction.COOL:
            features.append(ClimateEntityFeature.FAN_MODE)
        return features

    @staticmethod
    def current_humidity(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_HUMIDITY)
        return float(value) if value else None

    @staticmethod
    def target_humidity(component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_HUMIDITY_SETPOINT)
        return float(value) if value else None

    @staticmethod
    def on_behaviour(component: UserComponent) -> PresetMode | None:
        value = component.get_value(SfeType.STATE_ON_BEHAVIOUR)
        return PresetMode.get_preset_mode(value)

    @staticmethod
    def off_behaviour(component: UserComponent) -> PresetMode | None:
        value = component.get_value(SfeType.STATE_OFF_BEHAVIOUR)
        return PresetMode.get_preset_mode(value)

    @staticmethod
    def min_temp(component: UserComponent) -> float:
        return 4.0

    @staticmethod
    def max_temp(component: UserComponent) -> float:
        return 40.0

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
    def swing_mode(component: UserComponent) -> str | None:
        return None

    @staticmethod
    def swing_modes(component: UserComponent) -> list[str] | None:
        return None

    @staticmethod
    def min_humidity(component: UserComponent) -> float:
        return 20.0

    @staticmethod
    def max_humidity(component: UserComponent) -> float:
        return 99.0

    @staticmethod
    def _get_hvac_action(component: UserComponent) -> HVACAction | None:
        value = component.get_value(SfeType.STATE_OUT_STATUS)
        return HVACAction.get_hvac_action(value)
