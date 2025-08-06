from ...model.component.vimar_climate import (
    ChangeOverMode,
    ClimateEntityFeature,
    FanMode,
    HVACAction,
    HVACMode,
    PresetMode,
    VimarClimate,
)
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsClimaZoneMapper:
    SSTYPE = SsType.CLIMA_ZONE.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarClimate]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarClimate:
        return VimarClimate(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="climate",
            area=component.ambient.name,
            current_temperature=self.current_temperature(component),
            min_temp=self.min_temp(component),
            max_temp=self.max_temp(component),
            target_temperature=self.target_temperature(component),
            target_temperature_step=self.target_temperature_step(component),
            target_temperature_high=self.target_temperature_high(component),
            target_temperature_low=self.target_temperature_low(component),
            hvac_mode=self.hvac_mode(component),
            hvac_modes=self.hvac_modes(component),
            hvac_action=self.hvac_action(component),
            preset_mode=self.preset_mode(component),
            preset_modes=self.preset_modes(component),
            fan_mode=self.fan_mode(component),
            fan_modes=self.fan_modes(component),
            swing_mode=self.swing_mode(component),
            swing_modes=self.swing_modes(component),
            supported_features=self.supported_features(component),
            current_humidity=self.current_humidity(component),
            target_humidity=self.target_humidity(component),
            min_humidity=self.min_humidity(component),
            max_humidity=self.max_humidity(component),
            on_behaviour=self.on_behaviour(component),
            off_behaviour=self.off_behaviour(component),
            can_change_mode=self.can_change_mode(component),
            permission_granted=self.permission_granted(component),
        )

    def current_temperature(self, component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_AMBIENT_TEMPERATURE)
        return float(value) if value else None

    def target_temperature(self, component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_AMBIENT_SETPOINT)
        return float(value) if value else None

    def hvac_modes(self, component: UserComponent) -> list[HVACMode]:
        if self._is_change_mode_enabled(component):
            return [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
        if self.get_change_over_mode(component) == ChangeOverMode.HEAT:
            return [HVACMode.OFF, HVACMode.HEAT]
        if self.get_change_over_mode(component) == ChangeOverMode.COOL:
            return [HVACMode.OFF, HVACMode.COOL]
        return [HVACMode.OFF]

    def hvac_mode(self, component: UserComponent) -> HVACMode | None:
        hvac = self._get_hvac(component)
        return hvac[0]

    def hvac_action(self, component: UserComponent) -> HVACAction | None:
        hvac = self._get_hvac(component)
        return hvac[1]

    def preset_mode(self, component: UserComponent) -> str | None:
        value = component.get_value(SfeType.STATE_HVAC_MODE)
        mode = PresetMode.get_preset_mode(value)
        return mode.vimar_value if mode else None

    def preset_modes(self, component: UserComponent) -> list[str] | None:
        mode = self.preset_mode(component)
        return PresetMode.get_group_values(mode)

    def fan_mode(self, component: UserComponent) -> FanMode | None:
        mode = self.hvac_mode(component)
        fan_mode = component.get_value(SfeType.STATE_FAN_MODE)
        fan_speed = component.get_value(SfeType.STATE_FAN_SPEED_3V)
        mode = FanMode.get_fan_mode(fan_mode)
        speed = FanMode.get_fan_mode(fan_speed)
        return mode if mode else speed

    def fan_modes(self, component: UserComponent) -> list[FanMode] | None:
        return list(FanMode)

    def supported_features(
        self, component: UserComponent
    ) -> list[ClimateEntityFeature]:
        features = [
            ClimateEntityFeature.TARGET_TEMPERATURE,
            ClimateEntityFeature.TURN_OFF,
            ClimateEntityFeature.PRESET_MODE,
        ]

        if self._is_fan_enabled(component):
            features.append(ClimateEntityFeature.FAN_MODE)
        return features

    def current_humidity(self, component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_HUMIDITY)
        return float(value) if value else None

    def target_humidity(self, component: UserComponent) -> float | None:
        value = component.get_value(SfeType.STATE_HUMIDITY_SETPOINT)
        return float(value) if value else None

    def on_behaviour(self, component: UserComponent) -> PresetMode | None:
        value = component.get_value(SfeType.STATE_ON_BEHAVIOUR)
        return PresetMode.get_preset_mode(value)

    def off_behaviour(self, component: UserComponent) -> PresetMode | None:
        value = component.get_value(SfeType.STATE_OFF_BEHAVIOUR)
        return PresetMode.get_preset_mode(value)

    def min_temp(self, component: UserComponent) -> float:
        return 4.0

    def max_temp(self, component: UserComponent) -> float:
        return 40.0

    def target_temperature_step(self, component: UserComponent) -> float | None:
        return 0.1

    def target_temperature_low(self, component: UserComponent) -> float | None:
        return self.min_temp(component)

    def target_temperature_high(self, component: UserComponent) -> float | None:
        return self.max_temp(component)

    def swing_mode(self, component: UserComponent) -> str | None:
        return None

    def swing_modes(self, component: UserComponent) -> list[str] | None:
        return None

    def min_humidity(self, component: UserComponent) -> float:
        return 20.0

    def max_humidity(self, component: UserComponent) -> float:
        return 99.0

    def _get_hvac(self, component: UserComponent) -> tuple[HVACMode, HVACAction]:
        mode = self._get_hvac_mode(component)
        change_over_mode = self._get_change_over_mode(component)
        status = self._get_out_status(component)
        hvac_mode = HVACMode.get_hvac_mode(mode, status, change_over_mode)
        hvac_action = HVACAction.get_hvac_action(mode, status, change_over_mode)
        return (hvac_mode, hvac_action)

    def get_change_over_mode(self, component: UserComponent) -> ChangeOverMode | None:
        change_over_mode = self._get_change_over_mode(component)
        return ChangeOverMode.get_change_over_mode(change_over_mode)

    def _get_change_over_mode(self, component: UserComponent) -> str | None:
        return component.get_value(SfeType.STATE_CHANGE_OVER_MODE)

    def _get_out_status(self, component: UserComponent) -> str | None:
        return component.get_value(SfeType.STATE_OUT_STATUS)

    def _get_hvac_mode(self, component: UserComponent) -> str | None:
        return component.get_value(SfeType.STATE_HVAC_MODE)

    def _is_fan_enabled(self, component: UserComponent) -> str | None:
        return component.is_enabled(SfeType.STATE_FAN_SPEED_3V)

    def can_change_mode(self, component: UserComponent) -> bool:
        return self._is_change_mode_enabled(component)

    def permission_granted(self, component: UserComponent) -> bool:
        mode = SfeType.CMD_CHANGE_OVER_MODE
        return component.get_value(mode) is not None  # empty is ok

    def _is_change_mode_enabled(self, component: UserComponent) -> bool:
        return component.is_enabled(SfeType.CMD_CHANGE_OVER_MODE)
