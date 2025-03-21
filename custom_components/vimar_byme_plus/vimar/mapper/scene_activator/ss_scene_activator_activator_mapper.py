from ...model.component.vimar_button import VimarButton
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneActivatorActivatorMapper:
    SSTYPE = SsType.SCENE_ACTIVATOR_ACTIVATOR.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarButton:
        return VimarButton(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=None,
            executed=False,
        )
