from decimal import Decimal
import json

from ...model.component.vimar_button import VimarButton
from ...model.component.vimar_component import VimarComponent
from ...model.component.vimar_sensor import SensorDeviceClass, VimarSensor
from ...model.component.vimar_switch import VimarSwitch
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsIrrigationMultiZonesMapper:
    SSTYPE = SsType.IRRIGATION_MULTI_ZONES.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarComponent]:
        return [
            self.button_start_stop_from_obj(component, *args),
            self.button_skip_from_obj(component, *args),
            self.switch_auto_from_obj(component, *args),
            self.sensor_from_obj(component, *args),
        ]

    def button_start_stop_from_obj(
        self, component: UserComponent, *args
    ) -> VimarButton:
        return VimarButton(
            id=str(component.idsf) + "_start_stop",
            name=component.name + " - " + "Avvio/Stop immediato",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            executed=False,
        )

    def button_skip_from_obj(self, component: UserComponent, *args) -> VimarButton:
        if self._get_number_of_zones(component) < 2:
            return None
        return VimarButton(
            id=str(component.idsf) + "_skip",
            name=component.name + " - " + "Uscita successiva",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            executed=False,
        )

    def switch_auto_from_obj(self, component: UserComponent, *args) -> VimarSwitch:
        return VimarSwitch(
            id=str(component.idsf) + "_auto",
            name=component.name + " - " + "Avvio automatico",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class="switch",
            area=component.ambient.name,
            main_id=component.idsf,
            is_on=True,
        )

    def sensor_from_obj(self, component: UserComponent, *args) -> VimarSensor:
        return VimarSensor(
            id=str(component.idsf) + "_sensor",
            name=component.name + " - " + "Zona corrente",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=SensorDeviceClass.ENUM,
            area=component.ambient.name,
            main_id=component.idsf,
            native_value=self.native_value(component),
            last_update=None,
            decimal_precision=None,
            unit_of_measurement=None,
            state_class=None,
            options=self.get_values(component),
        )

    def native_value(self, component: UserComponent) -> str | Decimal | None:
        zone = self._get_current_zone(component)
        if not zone:
            return "Spento"
        return zone

    def get_values(self, component: UserComponent) -> list[str]:
        zones = self._get_number_of_zones(component)
        return ["Spento"] + [str(zone) for zone in range(1, zones + 1)]

    def _get_number_of_zones(self, component: UserComponent) -> int:
        try:
            settings = component.get_value(SfeType.STATE_PROGRAM_SETTINGS)
            settings_json = json.loads(settings)
            periods: list = settings_json["OutputsActivationPeriod"]
            return len(periods)
        except Exception:
            return 0

    def _get_current_zone(self, component: UserComponent) -> str:
        zone = component.get_value(SfeType.STATE_ACTIVE_ZONE)
        if zone and zone.isdigit() and int(zone):
            return zone
        return None
