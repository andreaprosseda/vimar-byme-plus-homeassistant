import sqlite3
from sqlite3 import Error, Connection
from ..utils.file import get_file_path

class Database:

    _connection: Connection = None
    
    def __init__(self, db_file: str):
        try:
            file_path = get_file_path(db_file)
            self._connection = sqlite3.connect(file_path)
            # self.create_tables()
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
    
    
    def execute_query(self, query):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
    
