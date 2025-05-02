from ...model.component.vimar_light import ColorMode, VimarLight
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsLightSwitchMapper:
    SSTYPE = SsType.LIGHT_SWITCH.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarLight]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarLight:
        return VimarLight(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="light",
            area=component.ambient.name,
            is_on=self.get_is_on(component),
            brightness=self.get_brightness(component),
            color_mode=self.get_color_mode(component),
            hsv_color=self.get_hsv_color(component),
            rgb_color=self.get_rgb_color(component),
            temp_color=self.get_temp_color(component),
            supported_color_modes=self.get_supported_color_modes(component),
        )

    def get_is_on(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_ON_OFF)
        return value == "On" if value else False

    def get_color_mode(self, component: UserComponent) -> ColorMode:
        return ColorMode.ONOFF

    def get_supported_color_modes(self, component: UserComponent) -> set[ColorMode]:
        return {ColorMode.ONOFF}

    def get_brightness(self, component: UserComponent) -> int | None:
        return None

    def get_hsv_color(self, component: UserComponent) -> tuple[int, int, int] | None:
        return None

    def get_rgb_color(self, component: UserComponent) -> tuple[int, int, int] | None:
        return None

    def get_temp_color(self, component: UserComponent) -> int | None:
        return None
