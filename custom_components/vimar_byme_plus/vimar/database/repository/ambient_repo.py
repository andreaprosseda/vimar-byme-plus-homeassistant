from sqlite3 import Connection

from ...model.repository.user_ambient import UserAmbient
from .base_repo import BaseRepo


class AmbientRepo(BaseRepo):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS ambients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dictKey TEXT NOT NULL,
                hash TEXT NOT NULL,
                idambient INTEGER NOT NULL,
                idparent INTEGER,
                name TEXT NOT NULL
            );
            """
        self.execute(query)

    def get_ids(self) -> list[int]:
        query = "SELECT idambient FROM ambients;"
        cursor = self.cursor().execute(query)
        record = cursor.fetchall()
        return record if record else []

    def replace_all(self, ambients: list[UserAmbient]):
        self.delete_all()
        self.insert_all(ambients)

    def delete_all(self):
        query = "DELETE FROM ambients;"
        self.execute(query)

    def insert_all(self, ambients: list[UserAmbient]):
        ambients_data = [ambient.to_tuple() for ambient in ambients]
        query = """
            INSERT INTO ambients
                (dictKey, hash, idambient, idparent, name)
            VALUES
                (?, ?, ?, ?, ?);
        """
        self.execute(query, ambients_data)

    def get_name_by_id(self, idambient: int) -> str:
        query = "SELECT name FROM ambients WHERE idambient = ?;"
        cursor = self.cursor().execute(query, (idambient,))
        result = cursor.fetchone()
        return result[0] if result else None
