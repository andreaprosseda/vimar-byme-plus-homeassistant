from sqlite3 import Connection, Cursor, Error

from ...utils.logger import log_debug, log_error


class BaseRepo:
    _connection: Connection

    def __init__(self, connection: Connection):
        self._connection = connection

    def cursor(self) -> Cursor:
        return self._connection.cursor()

    def execute(self, query, params: tuple = ()):
        cursor = self.cursor()
        try:
            log_debug(__name__, f"Executing query: {query} with params: {params}")
            if params and isinstance(params, (tuple)):
                cursor.execute(query, params)
            elif params and isinstance(params, list):
                cursor.executemany(query, params)
            else:
                cursor.execute(query)
            self._connection.commit()
            log_debug(__name__, "Query executed successfully")
        except Error as e:
            log_error(__name__, f"The error '{e}' occurred")
