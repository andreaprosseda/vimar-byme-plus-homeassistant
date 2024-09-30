from sqlite3 import Error, Connection

class BaseRepo:
    
    _connection: Connection
    
    def __init__(self, connection: Connection):
        self._connection = connection

    def execute(self, query, params: tuple = ()):
        cursor = self._connection.cursor()
        try:
            print(f"Executing query: {query} with params: {params}")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
    
    