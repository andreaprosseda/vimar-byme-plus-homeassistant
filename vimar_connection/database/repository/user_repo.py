from ...model.user.user_credentials import UserCredentials
from .base_repo import BaseRepo
from sqlite3 import Connection

class UserRepo(BaseRepo):
  
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()
        
    def create_table(self):
        print("Creating table")
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                setup_code TEXT NOT NULL,
                useruid TEXT,
                password TEXT,
                token TEXT
            );
        """
        self.execute(query)
    
    def get_current_user(self) -> UserCredentials:
        query = """
            SELECT 
                username, setup_code, useruid, password, token 
            FROM users
            LIMIT 1
        """
        cursor = self._connection.cursor()
        cursor.execute(query)
        record = cursor.fetchone()
        if not record:
            return None
        username, setup_code, useruid, password, token = record
        return UserCredentials(
            username = username,
            useruid = useruid,
            password = password,
            setup_code = setup_code,
            token = token
        )
    
    def insert(self, credentials: UserCredentials):
        self.delete_all()
        query = """
            INSERT INTO users
                (setup_code, username)
            VALUES
                (?, ?);
        """
        self.execute(query, (credentials.setup_code, credentials.username))
    
    def delete_all(self):
        query = "DELETE FROM users;"
        self.execute(query)
        
    def update(self, credentials: UserCredentials):
        query = """
            UPDATE users
            SET useruid = ?, password = ?, token = ?
            WHERE username = ?;
        """
        self.execute(query, (credentials.useruid, credentials.password, credentials.token, credentials.username))