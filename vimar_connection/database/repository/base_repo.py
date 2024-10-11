from sqlite3 import Error, Connection, Cursor

class BaseRepo:
    
    _connection: Connection
    
    def __init__(self, connection: Connection):
        self._connection = connection
        
    def cursor(self) -> Cursor: 
        return self._connection.cursor()
    
    def execute(self, query, params: tuple = ()):
        cursor = self.cursor()
        try:
            print(f"Executing query: {query} with params: {params}")
            if params and isinstance(params, (tuple)):
                cursor.execute(query, params)
            elif params and isinstance(params, list):
                cursor.executemany(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
    
    