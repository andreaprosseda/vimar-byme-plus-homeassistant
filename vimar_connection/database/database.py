import sqlite3
from sqlite3 import Error, Connection
from typing import Optional
from ..utils.file import get_file_path
from .repository.ambient_repo import AmbientRepo
from .repository.component_repo import ComponentRepo
from .repository.element_repo import ElementRepo
from .repository.user_repo import UserRepo

class Database:

    instance: Optional['Database'] = None
    
    ambient_repo: AmbientRepo
    component_repo: ComponentRepo
    element_repo: ElementRepo
    user_repo: UserRepo
    
    _connection: Connection = None
    
    def __new__(cls, db_file: str):
        if cls.instance is None:
            cls.instance = super(Database, cls).__new__(cls)
            cls.instance._initialize(db_file)
        return cls.instance

    def _initialize(self, db_file: str):
        self.create_connection(db_file)
        self.ambient_repo = AmbientRepo(self._connection)
        self.component_repo = ComponentRepo(self._connection)
        self.element_repo = ElementRepo(self._connection)
        self.user_repo = UserRepo(self._connection)
        
    def create_connection(self, db_file: str):
        try:
            file_path = get_file_path(db_file)
            self._connection = sqlite3.connect(file_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")