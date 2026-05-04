import threading
from sqlite3 import Connection, Cursor, Error

from ...utils.logger import log_debug, log_error


class BaseRepo:
    _connection: Connection

    # Class-level lock guarding the shared sqlite3 Connection.
    #
    # Every repo instance receives the same `Database.instance()` connection,
    # which is opened with `check_same_thread=False` so it can be used from
    # the WS callback threads of multiple OperationalService coordinators.
    # Without serialisation, two coordinators starting up at the same time
    # (e.g. right after an HA restart with two paired gateways) interleave
    # `cursor.execute() + connection.commit()` calls on the same Connection,
    # which sqlite3 surfaces as `cannot start a transaction within a
    # transaction` / `bad parameter or other API misuse`. The integration
    # then loses some of the schema/state writes (visible symptom: doubled
    # `components` rows after sfdiscovery, entities stuck `unavailable`
    # until the user manually reloads the config entries from the UI).
    #
    # Holding the lock around the entire execute → commit pair is the
    # smallest correct fix; the operations are short and not on the hot
    # path so the contention is negligible.
    _lock = threading.Lock()

    def __init__(self, connection: Connection):
        self._connection = connection

    def cursor(self) -> Cursor:
        return self._connection.cursor()

    def execute(self, query, params: tuple = ()):
        with self._lock:
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
