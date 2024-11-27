from ...model.repository.user_credentials import UserCredentials
from .base_repo import BaseRepo
from sqlite3 import Connection


class UserRepo(BaseRepo):

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                setup_code TEXT,
                useruid TEXT,
                password TEXT
            );
        """
        self.execute(query)

    def get_current_user(self) -> UserCredentials:
        query = """
            SELECT
                username, setup_code, useruid, password
            FROM users
            LIMIT 1
        """
        cursor = self.cursor().execute(query)
        record = cursor.fetchone()
        if not record:
            return None
        username, setup_code, useruid, password = record
        return UserCredentials(
            username=username,
            useruid=useruid,
            password=password,
            setup_code=setup_code
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
            SET useruid = ?, password = ?, setup_code = ?
            WHERE username = ?;
        """
        values = (credentials.useruid, credentials.password, None, credentials.username,)
        self.execute(query, values,)
