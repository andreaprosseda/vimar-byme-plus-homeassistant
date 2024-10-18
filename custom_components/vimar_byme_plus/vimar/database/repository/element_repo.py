from .base_repo import BaseRepo
from ...model.repository.user_component import UserComponent
from ...model.repository.user_element import UserElement
from sqlite3 import Connection


class ElementRepo(BaseRepo):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idcomponent INTEGER NOT NULL,
                enable BOOLEAN NOT NULL,
                sfetype TEXT NOT NULL,
                value TEXT,
                FOREIGN KEY (idcomponent) REFERENCES components (idsf)
            );
        """
        self.execute(query)

    def get_value_by_id(self, idcomponent: str, type: str) -> str:
        elements_data = (idcomponent, type)
        query = """
            SELECT value
            FROM elements
            WHERE idcomponent = ? AND sfetype = ?;
        """
        self.execute(query, elements_data)
        cursor = self.cursor().execute(query, elements_data)
        result = cursor.fetchone()
        return result[0] if result else None


    def delete_all(self):
        query = "DELETE FROM elements;"
        self.execute(query)

    def insert_all(self, components: list[UserComponent]):
        elements = self._get_all_elements(components)
        self._insert_all(elements)

    def update_all(self, components: list[UserComponent]):
        elements = self._get_all_elements(components)
        self._update_all(elements)

    def _insert_all(self, elements: list[UserElement]):
        elements_data = [element.to_tuple() for element in elements]
        query = """
            INSERT INTO elements
                (enable, idcomponent, sfetype, value)
            VALUES
                (?, ?, ?, ?);
        """
        self.execute(query, elements_data)

    def _update_all(self, elements: list[UserElement]):
        elements_data = [element.to_tuple_for_update() for element in elements]
        query = """
            UPDATE elements
            SET enable = ?, value = ?
            WHERE idcomponent = ? AND sfetype = ?;
        """
        self.execute(query, elements_data)

    def _get_all_elements(self, components: list[UserComponent]) -> list[UserElement]:
        elements = []
        all_elements = [component.elements for component in components]
        for elems in all_elements:
            elements.extend(elems)
        return elements
