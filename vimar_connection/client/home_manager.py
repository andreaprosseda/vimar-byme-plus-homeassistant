from ..model.user.user_environment import UserEnvironment

class HomeManager:
    
    FILE_NAME = 'environments.json'
    
    _environments: list[UserEnvironment]
    
    def __init__(self):
        self._environments = []
    
    def save_environments(self, response: dict):
        result = response['result']
        self._environments = []
        for environment in result:
            self._environments.append(UserEnvironment(**environment))
    
    def get_environments(self) -> list[UserEnvironment]:
        return self._environments
        
    def get_ambient_ids(self) -> list[int]:
        ids = []
        for environment in self.get_environments():
            ids.append(environment.idambient)
        return ids