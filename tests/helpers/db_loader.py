"""Carica un `home.db` e restituisce i `UserComponent` pronti per i mapper.

PERCHE' NON SI USA `Database`
-----------------------------
La classe `Database` dell'integrazione e' un registry per-gateway: sceglie il
file in base al `gateway_id`, migra il vecchio `home.db`, tiene una
connessione condivisa e un lock. Tutto giusto in produzione, tutto rumore in
un test — e soprattutto vincolerebbe le fixture a chiamarsi
`home_<gateway_id>.db` e a passare per la migrazione.

Qui il SQLite si legge e basta. Le tre tabelle che servono (`ambients`,
`components`, `elements`) hanno lo stesso schema da sempre, quindi un database
salvato prima del supporto multi-gateway si carica esattamente come uno di
oggi.

DERIVA DI SCHEMA
----------------
La colonna `elements.updated` non esiste nei database piu' vecchi. Invece di
rifiutarli, qui si guarda cosa c'e' davvero e si passa `None`: un componente
senza timestamp e' un caso legittimo (e' anche quello che la sfdiscovery
produce oggi, vedi issue #83).
"""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from pathlib import Path

from vimar.model.repository.user_ambient import UserAmbient
from vimar.model.repository.user_component import UserComponent
from vimar.model.repository.user_element import UserElement


def carica_componenti(percorso: str | Path) -> list[UserComponent]:
    """I componenti di un home.db, con ambiente ed elementi gia' agganciati."""
    con = sqlite3.connect(f"file:{Path(percorso)}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        colonne = {r[1] for r in con.execute("PRAGMA table_info(elements)")}
        ha_updated = "updated" in colonne

        ambienti = {
            # `.keys()` non e' ridondante: iterare una sqlite3.Row da' i
            # VALORI, non i nomi delle colonne.
            r["idambient"]: UserAmbient(**{k: r[k] for k in r.keys() if k != "id"})  # noqa: SIM118
            for r in con.execute("SELECT * FROM ambients")
        }

        elementi: dict[int, list[UserElement]] = defaultdict(list)
        for r in con.execute("SELECT * FROM elements"):
            elementi[r["idcomponent"]].append(
                UserElement(
                    idcomponent=r["idcomponent"],
                    enable=r["enable"],
                    sfetype=r["sfetype"],
                    value=r["value"],
                    last_update=r["updated"] if ha_updated else None,
                )
            )

        return [
            UserComponent(
                idambient=r["idambient"],
                dictKey=r["dictKey"],
                idsf=r["idsf"],
                name=r["name"],
                sftype=r["sftype"],
                sstype=r["sstype"],
                ambient=ambienti.get(r["idambient"]),
                elements=elementi.get(r["idsf"], []),
            )
            for r in con.execute("SELECT * FROM components ORDER BY idsf")
        ]
    finally:
        con.close()
