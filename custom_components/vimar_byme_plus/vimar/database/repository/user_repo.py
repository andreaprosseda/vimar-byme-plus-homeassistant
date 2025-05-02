from sqlite3 import Connection

from ...model.repository.user_credentials import UserCredentials
from .base_repo import BaseRepo


class UserRepo(BaseRepo):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()
        self.alter_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                setup_code TEXT,
                useruid TEXT,
                password TEXT,
                plant_name TEXT
            );
        """
        self.execute(query)

    def alter_table(self):
        query = "PRAGMA table_info(users);"
        cursor = self.cursor().execute(query)
        columns = [column[1] for column in cursor.fetchall()]
        if "plant_name" not in columns:
            alter = "ALTER TABLE users ADD COLUMN plant_name TEXT;"
            cursor.execute(alter)

    def get_current_user(self) -> UserCredentials:
        query = """
            SELECT
                username, setup_code, useruid, password, plant_name
            FROM users
            LIMIT 1
        """
        cursor = self.cursor().execute(query)
        record = cursor.fetchone()
        if not record:
            return None
        username, setup_code, useruid, password, plant_name = record
        return UserCredentials(
            username=username,
            useruid=useruid,
            password=password,
            setup_code=setup_code,
            plant_name=plant_name,
        )

    def insert(self, credentials: UserCredentials):
        query = """
            INSERT INTO users
                (setup_code, username)
            VALUES
                (?, ?);
        """
        self.execute(query, (credentials.setup_code, credentials.username))

    def insert_setup_code(self, username: str, setup_code: str):
        credentials = UserCredentials(username=username, setup_code=setup_code)
        self.delete_all()
        self.insert(credentials)

    def delete_all(self):
        query = "DELETE FROM users;"
        self.execute(query)

    def update(self, credentials: UserCredentials):
        query = """
            UPDATE users
            SET useruid = ?, password = ?, setup_code = ?, plant_name = ?
            WHERE username = ?;
        """
        values = (
            credentials.useruid,
            credentials.password,
            None,
            credentials.plant_name,
            credentials.username,
        )
        self.execute(
            query,
            values,
        )
