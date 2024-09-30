from ..model.user.user_credentials import UserCredentials
from ..database.database import Database
from ..database.repository.user_repo import UserRepo

class CredentialManager:
    
    username = 'xm7r1'
    
    _user_repo: UserRepo
    
    def __init__(self):
        self._user_repo = Database.instance.user_repo
    
    def save_user_credentials(self, response: dict):
        credentials = self.get_credentials_from_response(response)
        self._user_repo.update(credentials)
    
    def get_user_credentials(self) -> UserCredentials:
        credentials = self._user_repo.get_current_user()
        if credentials:
            return credentials
        else:
            code = input('Enter setup code obtained from Vimar PRO:\n')
            credentials = UserCredentials(username = self.username, setup_code = code)
            self._user_repo.insert(credentials)
        
    def get_credentials_from_response(self, response: dict) -> UserCredentials:
        useruid = response['result'][0]['useruid']
        password = response['result'][0]['password']
        token = response['result'][0]['token']
        return UserCredentials(
            username = self.username,
            useruid = useruid, 
            password = password, 
            token = token
        )