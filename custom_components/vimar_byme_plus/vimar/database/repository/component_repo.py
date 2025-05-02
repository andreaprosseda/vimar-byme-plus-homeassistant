from sqlite3 import Connection
from typing import Any

from ...model.repository.user_ambient import UserAmbient
from ...model.repository.user_component import UserComponent
from ...model.repository.user_element import UserElement
from .base_repo import BaseRepo
from .element_repo import ElementRepo


class ComponentRepo(BaseRepo):
    element_repo: ElementRepo

    def __init__(self, connection: Connection, element_repo: ElementRepo):
        super().__init__(connection)
        self.create_table()
        self.element_repo = element_repo

    def create_table(self):
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
        self.execute(query)

    def replace_all(self, components: list[UserComponent]):
        self.delete_all()
        self.insert_all(components)

    def delete_all(self):
        self.element_repo.delete_all()
        self._delete_all()

    def _delete_all(self):
        query = "DELETE FROM components;"
        self.execute(query)

    def insert_all(self, components: list[UserComponent]):
        self._insert_all(components)
        self.element_repo.insert_all(components)

    def _insert_all(self, components: list[UserComponent]):
        components_data = [component.to_tuple() for component in components]
        query = """
            INSERT INTO components
                (dictKey, idambient, idsf, name, sftype, sstype)
            VALUES
                (?, ?, ?, ?, ?, ?);
        """
        self.execute(query, components_data)

    def get_all(self) -> list[UserComponent]:
        query = """
            SELECT
                c.dictKey, c.idambient, c.idsf, c.name, c.sftype, c.sstype,
                e.id, e.enable, e.sfetype, e.value, e.updated,
                a.dictKey, a.hash, a.idambient, a.idparent, a.name
            FROM
                components c
            JOIN
                elements e ON c.idsf = e.idcomponent
            JOIN
                ambients a ON c.idambient = a.idambient;

        """
        cursor = self.cursor().execute(query)
        rows = cursor.fetchall()
        return self._get_all(rows)

    def get_component_of_type(self, sftype: str) -> list[UserComponent]:
        query = """
            SELECT dictKey, idambient, idsf, name, sftype, sstype
            FROM components
            WHERE sftype = ?;
        """

        cursor = self.cursor().execute(query, (sftype,))
        rows = cursor.fetchall()
        return [self._get_values(row) for row in rows]

    def _get_all(self, rows: list[Any]) -> list[UserComponent]:
        result: dict[int, UserComponent] = {}
        for row in rows:
            component, element, ambient = self._get_all_values(row)
            if component.idsf not in result:
                result[component.idsf] = component
            result[component.idsf].ambient = ambient
            result[component.idsf].elements.append(element)
        return list(result.values())

    def _get_values(self, row: list[Any]) -> UserComponent:
        (
            dictKey,
            idambient,
            idsf,
            name,
            sftype,
            sstype,
        ) = row
        return UserComponent(dictKey, idambient, idsf, name, sftype, sstype)

    def _get_all_values(
        self, row: list[Any]
    ) -> tuple[UserComponent, UserElement, UserAmbient]:
        (
            c_dictKey,
            c_idambient,
            c_idsf,
            c_name,
            c_sftype,
            c_sstype,
            e_element_id,
            e_enable,
            e_sfetype,
            e_value,
            e_updated,
            a_dictKey,
            a_hash,
            a_idambient,
            a_idparent,
            a_name,
        ) = row
        ambient = UserAmbient(a_dictKey, a_hash, a_idambient, a_idparent, a_name)
        element = UserElement(e_enable, e_element_id, e_sfetype, e_value, e_updated)
        component = UserComponent(
            c_dictKey, c_idambient, c_idsf, c_name, c_sftype, c_sstype
        )
        return component, element, ambient
