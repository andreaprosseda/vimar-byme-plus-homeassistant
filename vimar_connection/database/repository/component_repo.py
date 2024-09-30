from .base_repo import BaseRepo
from sqlite3 import Connection

class ComponentRepo(BaseRepo):
    
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()
        
    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idambient INTEGER NOT NULL,
                dictKey INTEGER NOT NULL,
                idsf INTEGER NOT NULL,
                name TEXT NOT NULL,
                sftype TEXT NOT NULL,
                sstype TEXT NOT NULL,
                FOREIGN KEY (idambient) REFERENCES ambients (idambient)
            );
            """
        self.execute(query)