class ComponentRepo:
    
    def create_table():
        query = """
        CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idambient INTEGER NOT NULL,
            dictKey INTEGER NOT NULL,
            idsf INTEGER NOT NULL,
            name TEXT NOT NULL,
            sftype TEXT NOT NULL,
            sstype TEXT NOT NULL,
            FOREIGN KEY (idambient) REFERENCES ambients (idambient)
        );
        """