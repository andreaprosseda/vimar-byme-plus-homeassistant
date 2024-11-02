from abc import ABC, abstractmethod
from ..model.repository.user_component import UserComponent
from ..model.component.vimar_component import VimarComponent


class BaseMapper(ABC):
    @abstractmethod
    def from_obj(component: UserComponent, *args) -> VimarComponent:
        pass
