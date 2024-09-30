from .base_repo import BaseRepo
from sqlite3 import Connection

class AmbientRepo(BaseRepo):
    
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()
        
    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS ambients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictKey TEXT NOT NULL,
                hash TEXT NOT NULL,
                idambient INTEGER NOT NULL,
                idparent INTEGER,
                name TEXT NOT NULL
            );
            """
        self.execute(query)