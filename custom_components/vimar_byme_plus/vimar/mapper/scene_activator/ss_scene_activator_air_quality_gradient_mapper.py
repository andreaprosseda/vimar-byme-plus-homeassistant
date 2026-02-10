from ...model.component.vimar_button import VimarButton
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneActivatorAirQualityGradientMapper:
    SSTYPE = SsType.SCENE_ACTIVATOR_AIR_QUALITY_GRADIENT.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [
            self._get_descending_button_from_obj(component),
            self._get_stabilization_button_from_obj(component)
        ]

    def _get_descending_button_from_obj(self, component: UserComponent) -> VimarButton:
        return self._button_from_obj(component, "descending", "Gradiente discendente")

    def _get_stabilization_button_from_obj(self, component: UserComponent) -> VimarButton:
        return self._button_from_obj(component, "stabilization", "Stabilizzazione")

    def _button_from_obj(self, component: UserComponent, suffix: str, label: str) -> VimarButton:
        return VimarButton(
            id=str(component.idsf) + "_" + suffix,
            name=component.name + " - " + label,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            executed=False,
        )