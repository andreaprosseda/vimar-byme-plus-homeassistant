from .handler_interface import HandlerInterface
from ...database.database import Database
from ...model.repository.user_ambient import UserAmbient
from ...model.repository.user_component import UserComponent
from ...model.repository.user_credentials import UserCredentials
from ...model.enum.component_type import ComponentType

class BaseMessageHandler(HandlerInterface):
    
    _user_repo = Database.instance().user_repo
    _ambient_repo = Database.instance().ambient_repo
    _component_repo = Database.instance().component_repo
    _element_repo = Database.instance().element_repo

    def save_user_credentials(self, response: dict):
        credentials = UserCredentials.obj_from_dict(response)
        self._user_repo.update(credentials)
    
    def save_ambients(self, response: dict):
        ambients = UserAmbient.list_from_dict(response)
        self._ambient_repo.replace_all(ambients)

    def save_components(self, response: dict):
        components = UserComponent.list_from_response(response)
        self._component_repo.replace_all(components)

    def save_component_changes(self, request: dict):
        components = UserComponent.list_from_request(request)
        self._element_repo.update_all(components)
        
    def get_user_credentials(self) -> UserCredentials:
        return self._user_repo.get_current_user()
    
    def get_all_ambient_ids(self) -> list[int]:
        return self._ambient_repo.get_ids()

    def get_all_components(self) -> list[UserComponent]:
        return self._component_repo.get_all()

    def get_components(self, type: ComponentType) -> list[UserComponent]:
        return self._component_repo.get_component_of_type(type.value)