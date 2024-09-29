from ..model.user.user_credentials import UserCredentials
from ..utils.file import save_file, file_exists
from ..utils.json import read_json

class CredentialManager:
    
    FILE_NAME = 'credentials.json'
    
    _user_credentials: UserCredentials
    
    def __init__(self):
        self.retrieve_user_credentials()
    
    def save_user_credentials(self, response: dict):
        useruid = response['result'][0]['useruid']
        password = response['result'][0]['password']
        credentials = UserCredentials(useruid = useruid, password = password)
        save_file(credentials.to_json(), self.FILE_NAME)
    
    def get_user_credentials(self) -> UserCredentials:
        if not self._user_credentials:
            self.retrieve_user_credentials()
        return self._user_credentials
        
    def retrieve_user_credentials(self):
        if file_exists(self.FILE_NAME):
            credentials = read_json(self.FILE_NAME)
            self._user_credentials = UserCredentials(**credentials)
        else:
            code = input('Enter setup code obtained from Vimar PRO:\n')
            self._user_credentials = UserCredentials(setup_code=code)