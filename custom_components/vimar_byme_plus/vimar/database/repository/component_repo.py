from sqlite3 import Connection
from typing import Any, Optional

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
        self.alter_table()
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
                gateway_uid TEXT,
                FOREIGN KEY (idambient) REFERENCES ambients (idambient)
            );
            """
        self.execute(query)

    def alter_table(self):
        query = "PRAGMA table_info(components);"
        cursor = self.cursor().execute(query)
        columns = [column[1] for column in cursor.fetchall()]
        if "gateway_uid" not in columns:
            cursor.execute("ALTER TABLE components ADD COLUMN gateway_uid TEXT;")

    def replace_all(
        self, components: list[UserComponent], gateway_uid: Optional[str] = None
    ):
        # Only wipe rows belonging to *this* gateway, so other paired gateways
        # keep their components in the shared DB (issue #34, BUG#3).
        self.delete_all(gateway_uid=gateway_uid)
        self.insert_all(components, gateway_uid=gateway_uid)

    def delete_all(self, gateway_uid: Optional[str] = None):
        self.element_repo.delete_all(gateway_uid=gateway_uid)
        self._delete_all(gateway_uid=gateway_uid)

    def _delete_all(self, gateway_uid: Optional[str] = None):
        if gateway_uid:
            query = "DELETE FROM components WHERE gateway_uid = ? OR gateway_uid IS NULL;"
            self.execute(query, (gateway_uid,))
        else:
            query = "DELETE FROM components;"
            self.execute(query)

    def insert_all(
        self, components: list[UserComponent], gateway_uid: Optional[str] = None
    ):
        self._insert_all(components, gateway_uid=gateway_uid)
        self.element_repo.insert_all(components, gateway_uid=gateway_uid)

    def _insert_all(
        self, components: list[UserComponent], gateway_uid: Optional[str] = None
    ):
        components_data = [
            (*component.to_tuple(), gateway_uid) for component in components
        ]
        query = """
            INSERT INTO components
                (dictKey, idambient, idsf, name, sftype, sstype, gateway_uid)
            VALUES
                (?, ?, ?, ?, ?, ?, ?);
        """
        self.execute(query, components_data)

    def get_all(self, gateway_uid: Optional[str] = None) -> list[UserComponent]:
        # Join elements/ambients also filtered by gateway_uid where applicable.
        # Same-idsf collisions across gateways are now safe because both
        # components and elements carry the gateway_uid scope.
        # LEFT JOIN on ambients so a missing/wiped ambient row never drops
        # the component (defensive: ambient discovery for a different gateway
        # used to wipe rows globally — see issue #34 BUG#3 ambients-scoping).
        if gateway_uid:
            query = """
                SELECT
                    c.dictKey, c.idambient, c.idsf, c.name, c.sftype, c.sstype,
                    e.id, e.enable, e.sfetype, e.value, e.updated,
                    a.dictKey, a.hash, a.idambient, a.idparent, a.name
                FROM
                    components c
                JOIN
                    elements e ON c.idsf = e.idcomponent
                    AND (e.gateway_uid = c.gateway_uid OR e.gateway_uid IS NULL)
                LEFT JOIN
                    ambients a ON c.idambient = a.idambient
                    AND (a.gateway_uid = c.gateway_uid OR a.gateway_uid IS NULL)
                WHERE
                    c.gateway_uid = ? OR c.gateway_uid IS NULL;
            """
            cursor = self.cursor().execute(query, (gateway_uid,))
        else:
            query = """
                SELECT
                    c.dictKey, c.idambient, c.idsf, c.name, c.sftype, c.sstype,
                    e.id, e.enable, e.sfetype, e.value, e.updated,
                    a.dictKey, a.hash, a.idambient, a.idparent, a.name
                FROM
                    components c
                JOIN
                    elements e ON c.idsf = e.idcomponent
                LEFT JOIN
                    ambients a ON c.idambient = a.idambient;
            """
            cursor = self.cursor().execute(query)
        rows = cursor.fetchall()
        return self._get_all(rows)

    def get_component_of_type(
        self, sftype: str, gateway_uid: Optional[str] = None
    ) -> list[UserComponent]:
        if gateway_uid:
            query = """
                SELECT dictKey, idambient, idsf, name, sftype, sstype
                FROM components
                WHERE sftype = ? AND (gateway_uid = ? OR gateway_uid IS NULL);
            """
            cursor = self.cursor().execute(query, (sftype, gateway_uid))
        else:
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
