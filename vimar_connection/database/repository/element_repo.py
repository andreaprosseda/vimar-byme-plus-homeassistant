from .base_repo import BaseRepo
from sqlite3 import Connection

class ElementRepo(BaseRepo):
    
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()
        
    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS sf_elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                component_id INTEGER NOT NULL,
                enable BOOLEAN NOT NULL,
                sfetype TEXT NOT NULL,
                value TEXT,
                FOREIGN KEY (component_id) REFERENCES components (id)
            );
        """
        self.execute(query)