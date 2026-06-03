"""Per-gateway SQLite registry.

The integration historically used a single global `home.db` and a
classic singleton `Database`. With multi-gateway support every gateway
gets its own file `home_<sanitized_deviceuid>.db` and `Database.instance`
becomes a registry keyed by `gateway_id`.

Migration: on first lookup for a gateway, if the legacy `home.db`
exists and no other `home_*.db` files are present, it is renamed to
`home_<gateway_id>.db` so existing single-gateway installs preserve
their data transparently.
"""

import os
import re
import sqlite3
import threading
from sqlite3 import Connection, Error

from ..utils.file import get_data_path, get_file_path
from ..utils.logger import log_error, log_info
from .repository.ambient_repo import AmbientRepo
from .repository.component_repo import ComponentRepo
from .repository.element_repo import ElementRepo
from .repository.user_repo import UserRepo

_LEGACY_DATABASE_NAME = "home.db"
_DATABASE_PREFIX = "home_"
_DATABASE_SUFFIX = ".db"

class Database:
    ambient_repo: AmbientRepo
    component_repo: ComponentRepo
    element_repo: ElementRepo
    user_repo: UserRepo

    _instances: dict[str, "Database"] = {}
    _instances_lock = threading.Lock()
    _connection: Connection | None = None

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("Use Database.instance(gateway_id) instead")


    @classmethod
    def instance(cls, gateway_id: str) -> "Database":
        key = cls._sanitize(gateway_id)
        with cls._instances_lock:
            if key not in cls._instances:
                inst = object.__new__(cls)
                inst._initialize(key)
                cls._instances[key] = inst
            return cls._instances[key]


    @classmethod
    def remove(cls, gateway_id: str | None, *, delete_file: bool = False) -> None:
        if not gateway_id:
            return
        key = cls._sanitize(gateway_id)
        with cls._instances_lock:
            inst = cls._instances.pop(key, None)
        if inst and inst._connection is not None:
            try:
                inst._connection.close()
            except Error as err:
                log_error(__name__, f"Error closing connection for {key}: {err}")
        if delete_file:
            cls._delete_file(key)


    @staticmethod
    def _delete_file(key: str) -> None:
        path = get_file_path(_DATABASE_PREFIX + key + _DATABASE_SUFFIX)
        try:
            if os.path.exists(path):
                os.remove(path)
                log_info(__name__, f"Removed database file {path}")
        except OSError as err:
            log_error(__name__, f"Could not remove {path}: {err}")
        for suffix in ("-wal", "-shm"):
            # WAL leaves `<file>-wal` and `<file>-shm` siblings; crashes leave them orphan. 
            sibling = path + suffix
            if not os.path.exists(sibling):
                continue
            try:
                os.remove(sibling)
                log_info(__name__, f"Removed orphan sibling {sibling}")
            except OSError as err:
                log_error(__name__, f"Could not remove {sibling}: {err}")


    @staticmethod
    def _sanitize(gateway_id: str) -> str:
        # Keep filenames safe by replacing unexpected characters in deviceuid
        return re.sub(r"[^A-Za-z0-9_-]", "_", str(gateway_id))


    def _initialize(self, key: str) -> None:
        target = get_file_path(_DATABASE_PREFIX + key + _DATABASE_SUFFIX)
        self._migrate_legacy_if_needed(target)
        self._heal_empty_files(target)
        conn = self._create_connection(target)
        self.element_repo = ElementRepo(conn)
        self.ambient_repo = AmbientRepo(conn)
        self.user_repo = UserRepo(conn)
        self.component_repo = ComponentRepo(conn, self.element_repo)
        conn.commit()


    @staticmethod
    def _migrate_legacy_if_needed(target: str) -> None:
        """Rename `home.db` > `home_<key>.db` for legacy single-gateway installs."""
        if os.path.exists(target):
            return
        legacy = get_file_path(_LEGACY_DATABASE_NAME)
        if not os.path.exists(legacy):
            return
        if Database._get_siblings():
            log_info(__name__, f"Legacy {_LEGACY_DATABASE_NAME} found but other gateway database files exist; leaving it untouched (manual cleanup may be needed).")
            return
        Database._migrate(legacy, target)
    
    
    @staticmethod
    def _migrate(legacy: str, target: str) -> None:
        try:
            os.rename(legacy, target)
            log_info(__name__, f"Migrated legacy {_LEGACY_DATABASE_NAME} -> {os.path.basename(target)}")
        except OSError as err:
            log_error(__name__, f"Failed to migrate legacy db: {err}")


    @staticmethod
    def _get_siblings() -> list[str]:
        try:
            data_dir = get_data_path()
            return [
                f
                for f in os.listdir(data_dir)
                if f.startswith(_DATABASE_PREFIX) and f.endswith(_DATABASE_SUFFIX)
            ]
        except OSError:
            return []


    @staticmethod
    def _heal_empty_files(target: str) -> None:
        """Delete 0-byte database files so SQLite can re-create the schema. Such files are produced by previous failed inits where DDL was never committed before the connection was closed."""
        for path in (target, get_file_path(_LEGACY_DATABASE_NAME)):
            try:
                if os.path.exists(path) and os.path.getsize(path) == 0:
                    os.remove(path)
                    log_info(__name__, f"Removed empty {os.path.basename(path)} left by a previous failed init")
            except OSError as err:
                log_error(__name__, f"Could not heal empty db {path}: {err}")


    def _create_connection(self, file_path: str) -> Connection:
        try:
            self._connection = sqlite3.connect(file_path, check_same_thread=False)
            # Enable WAL: writers don't block readers and vice versa. Fail silently if not supported
            row = self._connection.execute("PRAGMA journal_mode=WAL").fetchone()
            journal_mode = (row[0] if row else "").lower()
            log_info(__name__, f"Connection to SQLite DB successful ({file_path}, journal_mode={journal_mode})")
            return self._connection
        except Error as err:
            log_error(__name__, f"Error opening {file_path}: {err}")
            raise
