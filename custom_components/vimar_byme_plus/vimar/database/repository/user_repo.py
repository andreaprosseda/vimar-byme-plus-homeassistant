from sqlite3 import Connection
from typing import Optional

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
                plant_name TEXT,
                gateway_uid TEXT
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
        if "gateway_uid" not in columns:
            alter = "ALTER TABLE users ADD COLUMN gateway_uid TEXT;"
            cursor.execute(alter)

    def get_current_user(self, gateway_uid: Optional[str] = None) -> UserCredentials:
        """Return credentials for the given gateway, or any if gateway_uid is None.

        Backward-compatible: rows that pre-date the multi-gateway scoping
        have gateway_uid = NULL and are still returned (until the
        operational coordinator claims them at startup).
        """
        if gateway_uid:
            # Prefer the row tagged for this gateway; fall back to a NULL row
            # left over from the pre-scoped schema.
            query = """
                SELECT username, setup_code, useruid, password, plant_name
                FROM users
                WHERE gateway_uid = ? OR gateway_uid IS NULL
                ORDER BY (gateway_uid IS NULL) ASC
                LIMIT 1
            """
            cursor = self.cursor().execute(query, (gateway_uid,))
        else:
            query = """
                SELECT username, setup_code, useruid, password, plant_name
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

    def insert(self, credentials: UserCredentials, gateway_uid: Optional[str] = None):
        query = """
            INSERT INTO users
                (setup_code, username, gateway_uid)
            VALUES
                (?, ?, ?);
        """
        self.execute(query, (credentials.setup_code, credentials.username, gateway_uid))

    def insert_setup_code(
        self, username: str, setup_code: str, gateway_uid: Optional[str] = None
    ):
        credentials = UserCredentials(username=username, setup_code=setup_code)
        # Only delete the row(s) for this specific gateway, so other paired
        # gateways keep their credentials. Without scoping, the second pair
        # in a multi-gateway setup would wipe the first one (issue #34, BUG#3).
        self.delete_all(gateway_uid=gateway_uid)
        self.insert(credentials, gateway_uid=gateway_uid)

    def delete_all(self, gateway_uid: Optional[str] = None):
        if gateway_uid:
            query = "DELETE FROM users WHERE gateway_uid = ? OR gateway_uid IS NULL;"
            self.execute(query, (gateway_uid,))
        else:
            query = "DELETE FROM users;"
            self.execute(query)

    def update(
        self, credentials: UserCredentials, gateway_uid: Optional[str] = None
    ):
        if gateway_uid:
            query = """
                UPDATE users
                SET useruid = ?, password = ?, setup_code = ?, plant_name = ?
                WHERE username = ? AND (gateway_uid = ? OR gateway_uid IS NULL);
            """
            values = (
                credentials.useruid,
                credentials.password,
                None,
                credentials.plant_name,
                credentials.username,
                gateway_uid,
            )
        else:
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
        self.execute(query, values)
