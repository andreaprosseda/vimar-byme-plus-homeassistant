class AmbientRepo:
    create_ambients_table = """
        CREATE TABLE IF NOT EXISTS ambients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dictKey TEXT NOT NULL,
            hash TEXT NOT NULL,
            idambient INTEGER NOT NULL,
            idparent INTEGER,
            name TEXT NOT NULL
        );
        """