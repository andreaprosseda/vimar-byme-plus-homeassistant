from ...model.component.vimar_button import VimarButton
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneActivatorVideoEntryMapper:
    SSTYPE = SsType.SCENE_ACTIVATOR_VIDEO_ENTRY.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [
            self.button_start_call_from_obj(component, *args),
            self.button_end_call_from_obj(component, *args),
        ]

    def button_start_call_from_obj(
        self, component: UserComponent, *args
    ) -> VimarButton:
        return VimarButton(
            id=str(component.idsf) + "_start_call",
            name=component.name + " - " + "Avvio Chiamata",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            executed=False,
        )

    def button_end_call_from_obj(self, component: UserComponent, *args) -> VimarButton:
        return VimarButton(
            id=str(component.idsf) + "_end_call",
            name=component.name + " - " + "Fine Chiamata",
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=component.idsf,
            executed=False,
        )
