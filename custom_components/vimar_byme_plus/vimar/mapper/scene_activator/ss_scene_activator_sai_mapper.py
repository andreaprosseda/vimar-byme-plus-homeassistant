from ...model.component.vimar_button import VimarButton
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent

_BUTTONS: list[tuple[str, str]] = [
    ("dis", "Disinserimento"),
    ("on", "Inserimento totale"),
    ("int", "Inserimento intermedio"),
    ("par", "Inserimento parziale"),
    ("alarm", "Allarme"),
    ("alarm_memory", "Memoria allarme"),
    ("alarm_memory_reset", "Reset memoria allarme"),
    ("alarm_reset", "Reset allarme"),
]


class SsSceneActivatorSaiMapper:
    SSTYPE = SsType.SCENE_ACTIVATOR_SAI.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [
            self._button_from_obj(component, suffix, label)
            for suffix, label in _BUTTONS
        ]

    def _button_from_obj(
        self, component: UserComponent, suffix: str, label: str
    ) -> VimarButton:
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
