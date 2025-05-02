from abc import ABC, abstractmethod

from ....database.database import Database
from ....model.enum.component_type import ComponentType
from ....model.repository.user_ambient import UserAmbient
from ....model.repository.user_component import UserComponent
from ....model.repository.user_credentials import UserCredentials
from ....model.web_socket.base_request import BaseRequest
from ....model.web_socket.base_request_response import BaseRequestResponse
from ....model.web_socket.supporting_models.message_supporting_values import (
    MessageSupportingValues,
)
from ....utils.logger import log_debug, log_info


class HandlerInterface(ABC):
    @abstractmethod
    def handle_message(
        self, message: BaseRequestResponse, config: MessageSupportingValues
    ) -> BaseRequestResponse:
        pass

    def _idle(self) -> BaseRequestResponse:
        log_debug(__name__, "Entering idle state: no action required for this phase...")
        return None

    def requires_response(self, message: BaseRequest) -> bool:
        return message.params[0]["requiredresp"]


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
        log_info(__name__, f"Ambients retrieved: {len(ambients)}")
        self._ambient_repo.replace_all(ambients)

    def save_components(self, response: dict):
        components = UserComponent.list_from_response(response)
        log_info(__name__, f"Components retrieved: {len(components)}")
        self._component_repo.replace_all(components)

    def save_component_changes(self, request: dict):
        components = UserComponent.list_from_request(request)
        log_info(__name__, f"Changes retrieved: {len(components)}")
        self._element_repo.update_all(components)

    def get_user_credentials(self) -> UserCredentials:
        return self._user_repo.get_current_user()

    def get_all_ambient_ids(self) -> list[int]:
        return self._ambient_repo.get_ids()

    def get_all_components(self) -> list[UserComponent]:
        return self._component_repo.get_all()

    def get_components(self, type: ComponentType) -> list[UserComponent]:
        return self._component_repo.get_component_of_type(type.value)
