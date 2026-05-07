import os
import sqlite3
import threading
from sqlite3 import Connection, Error
from typing import Optional

from ..utils.file import get_file_path
from ..utils.logger import log_error, log_info
from .repository.ambient_repo import AmbientRepo
from .repository.component_repo import ComponentRepo
from .repository.element_repo import ElementRepo
from .repository.user_repo import UserRepo

DATABASE_NAME = "home.db"

# Thread-local gateway scope. Each coordinator runs in its own thread; the
# coordinator sets its gateway uid here on connect so repos and message
# handlers can filter rows belonging to *this* gateway without every method
# having to forward an extra argument. Without scoping, the second gateway's
# pair wipes the first one's users/components/elements rows from the shared
# singleton DB (issue #34, Bug #3).
_thread_local = threading.local()


def set_current_gateway_uid(gateway_uid: Optional[str]) -> None:
    """Set the active gateway_uid for this thread (None clears it)."""
    _thread_local.gateway_uid = gateway_uid


def current_gateway_uid() -> Optional[str]:
    """Return the active gateway_uid for this thread, or None if not set."""
    return getattr(_thread_local, "gateway_uid", None)


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
        # Defensive: explicitly commit the CREATE TABLE statements run by each
        # repo's __init__. Without this, an exception later in setup may leave
        # the SQLite file as 0 bytes (no schema flushed to disk), and every
        # subsequent reconnect re-opens an empty file. See discussion in #34.
        try:
            conn.commit()
        except Error as e:
            log_error(__name__, f"Could not commit schema: {e}")

    def create_connection(self) -> Connection:
        try:
            file_path = get_file_path(DATABASE_NAME)
            # Self-heal: if a previous failed init left a 0-byte file,
            # remove it so SQLite can write a fresh schema. Otherwise we
            # would keep reopening the empty file forever and the integration
            # would never reach the operational phase.
            try:
                if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
                    os.remove(file_path)
                    log_info(
                        __name__,
                        f"Removed empty {DATABASE_NAME} left by a previous failed init",
                    )
            except OSError as e:
                log_error(__name__, f"Could not remove empty db file: {e}")
            self._connection = sqlite3.connect(file_path, check_same_thread=False)
            log_info(__name__, "Connection to SQLite DB successful")
            return self._connection
        except Error as e:
            log_error(__name__, f"Error occurred: {e}")
