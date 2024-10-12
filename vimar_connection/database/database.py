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
        conn = self.create_connection(db_file)
        self.element_repo = ElementRepo(conn)
        self.ambient_repo = AmbientRepo(conn)
        self.user_repo = UserRepo(conn)
        self.component_repo = ComponentRepo(conn, self.element_repo)
        
    def create_connection(self, db_file: str) -> Connection:
        try:
            file_path = get_file_path(db_file)
            self._connection = sqlite3.connect(file_path, check_same_thread=False)
            print("Connection to SQLite DB successful")
            return self._connection
        except Error as e:
            print(f"The error '{e}' occurred")