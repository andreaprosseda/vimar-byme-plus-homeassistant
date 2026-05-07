from sqlite3 import Connection
from typing import Optional

from ...model.repository.user_ambient import UserAmbient
from .base_repo import BaseRepo


class AmbientRepo(BaseRepo):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()
        self.alter_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS ambients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictKey TEXT NOT NULL,
                hash TEXT NOT NULL,
                idambient INTEGER NOT NULL,
                idparent INTEGER,
                name TEXT NOT NULL,
                gateway_uid TEXT
            );
            """
        self.execute(query)

    def alter_table(self):
        query = "PRAGMA table_info(ambients);"
        cursor = self.cursor().execute(query)
        columns = [column[1] for column in cursor.fetchall()]
        if "gateway_uid" not in columns:
            cursor.execute("ALTER TABLE ambients ADD COLUMN gateway_uid TEXT;")

    def get_ids(self, gateway_uid: Optional[str] = None) -> list[int]:
        if gateway_uid:
            query = "SELECT idambient FROM ambients WHERE gateway_uid = ? OR gateway_uid IS NULL;"
            cursor = self.cursor().execute(query, (gateway_uid,))
        else:
            query = "SELECT idambient FROM ambients;"
            cursor = self.cursor().execute(query)
        record = cursor.fetchall()
        return record if record else []

    def replace_all(
        self, ambients: list[UserAmbient], gateway_uid: Optional[str] = None
    ):
        # Only wipe rows for *this* gateway, otherwise the second gateway's
        # ambient discovery would erase the first gateway's ambients and
        # break the components<->ambients JOIN in component_repo.get_all
        # (issue #34, BUG#3 — ambients-scoping completion).
        self.delete_all(gateway_uid=gateway_uid)
        self.insert_all(ambients, gateway_uid=gateway_uid)

    def delete_all(self, gateway_uid: Optional[str] = None):
        if gateway_uid:
            query = "DELETE FROM ambients WHERE gateway_uid = ? OR gateway_uid IS NULL;"
            self.execute(query, (gateway_uid,))
        else:
            query = "DELETE FROM ambients;"
            self.execute(query)

    def insert_all(
        self, ambients: list[UserAmbient], gateway_uid: Optional[str] = None
    ):
        ambients_data = [(*ambient.to_tuple(), gateway_uid) for ambient in ambients]
        query = """
            INSERT INTO ambients
                (dictKey, hash, idambient, idparent, name, gateway_uid)
            VALUES
                (?, ?, ?, ?, ?, ?);
        """
        self.execute(query, ambients_data)

    def get_name_by_id(
        self, idambient: int, gateway_uid: Optional[str] = None
    ) -> str:
        if gateway_uid:
            query = "SELECT name FROM ambients WHERE idambient = ? AND (gateway_uid = ? OR gateway_uid IS NULL);"
            cursor = self.cursor().execute(query, (idambient, gateway_uid))
        else:
            query = "SELECT name FROM ambients WHERE idambient = ?;"
            cursor = self.cursor().execute(query, (idambient,))
        result = cursor.fetchone()
        return result[0] if result else None
