from datetime import datetime, timedelta

from ...model.component.vimar_button import VimarButton
from ...model.enum.sfetype_enum import SfeType
from ...model.enum.sstype_enum import SsType
from ...model.repository.user_component import UserComponent


class SsSceneExecutorMapper:
    SSTYPE = SsType.SCENE_EXECUTOR.value

    def from_obj(self, component: UserComponent, *args) -> list[VimarButton]:
        return [
            self._button_from_obj(component, *args),
            # self._sensor_from_obj(component, *args),
        ]

    def _button_from_obj(self, component: UserComponent, *args) -> VimarButton:
        return VimarButton(
            id=component.idsf,
            name=component.name,
            device_group=component.sftype,
            device_name=component.sstype,
            device_class=None,
            area=component.ambient.name,
            main_id=None,
            executed=self._executed(component),
        )

    def _executed(self, component: UserComponent) -> bool:
        value = component.get_value(SfeType.STATE_EXECUTED)
        if value != "Executed":
            return False
        last_update = self._last_update(component)
        return (datetime.now() - last_update) <= timedelta(seconds=2)

    def _last_update(self, component: UserComponent) -> datetime | None:
        value = component.get_last_update(SfeType.STATE_EXECUTED)
        if not value:
            return None
        return datetime.fromisoformat(value)
