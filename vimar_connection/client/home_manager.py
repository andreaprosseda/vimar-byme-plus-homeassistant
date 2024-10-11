from ..model.repository.user_ambient import UserAmbient
from ..model.repository.user_component import UserComponent
from ..database.database import Database
from ..database.repository.ambient_repo import AmbientRepo
from ..database.repository.component_repo import ComponentRepo

class HomeManager:
    
    _ambient_repo: AmbientRepo
    _component_repo: ComponentRepo
    
    def __init__(self):
        self._ambient_repo = Database.instance.ambient_repo
        self._component_repo = Database.instance.component_repo
    
    def save_ambients(self, response: dict):
        ambients = UserAmbient.list_from_dict(response)
        self._ambient_repo.replace_all(ambients)
    
    def save_components(self, response: dict):
        components = UserComponent.list_from_dict(response)
        self._component_repo.replace_all(components)
    
    def get_all_ambient_ids(self) -> list[int]:
        return self._ambient_repo.get_ids()
    
    def get_all_components(self) -> list[UserComponent]:
        return self._component_repo.get_all()
    
    def save_component_changes(self, request: dict):
        pass