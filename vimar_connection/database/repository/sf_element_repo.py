class SfElementRepo:
    
    create_sf_elements_table = """
        CREATE TABLE IF NOT EXISTS sf_elements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component_id INTEGER NOT NULL,
            enable BOOLEAN NOT NULL,
            sfetype TEXT NOT NULL,
            value TEXT,
            FOREIGN KEY (component_id) REFERENCES components (id)
        );
    """