import sqlite3
from sqlite3 import Connection, Error
from typing import Optional

from ..utils.file import get_file_path
from ..utils.logger import log_error, log_info
from .repository.ambient_repo import AmbientRepo
from .repository.component_repo import ComponentRepo
from .repository.element_repo import ElementRepo
from .repository.user_repo import UserRepo

DATABASE_NAME = "home.db"


class Database:
    ambient_repo: AmbientRepo
    component_repo: ComponentRepo
    element_repo: ElementRepo
    user_repo: UserRepo

    _instance: Optional["Database"] = None
    _connection: Connection = None

    def __new__(cls):
        raise NotImplementedError("Use Database.instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        conn = self.create_connection()
        self.element_repo = ElementRepo(conn)
        self.ambient_repo = AmbientRepo(conn)
        self.user_repo = UserRepo(conn)
        self.component_repo = ComponentRepo(conn, self.element_repo)

    def create_connection(self) -> Connection:
        try:
            file_path = get_file_path(DATABASE_NAME)
            self._connection = sqlite3.connect(file_path, check_same_thread=False)
            log_info(__name__, "Connection to SQLite DB successful")
            return self._connection
        except Error as e:
            log_error(__name__, f"Error occurred: {e}")
