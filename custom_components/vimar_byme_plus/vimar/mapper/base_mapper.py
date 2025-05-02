from abc import ABC, abstractmethod

from ..model.component.vimar_component import VimarComponent
from ..model.repository.user_component import UserComponent


class BaseMapper(ABC):
    @abstractmethod
    def from_obj(component: UserComponent, *args) -> VimarComponent:
        pass
