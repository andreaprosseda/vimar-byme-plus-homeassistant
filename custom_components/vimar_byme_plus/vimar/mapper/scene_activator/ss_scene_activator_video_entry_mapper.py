from ...model.component.vimar_button import VimarButton
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneActivatorVideoEntryMapper:
    SSTYPE = SsType.SCENE_ACTIVATOR_VIDEO_ENTRY.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [self._from_obj(component, *args)]

    def _from_obj(self, component: UserComponent, *args) -> VimarButton:
        raise NotImplementedError
