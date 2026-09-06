"""Il banco per i test che caricano l'integrazione con Home Assistant vero.

Condiviso da test_setup.py, test_actions.py e test_snapshot.py: tutti e tre
hanno bisogno della STESSA config entry caricata sullo STESSO master.db, la
differenza e' solo cosa verificano dopo. Prima viveva duplicato dentro
test_setup.py; spostato qui quando e' servito un secondo file.
"""

from __future__ import annotations

import importlib

from const import ADDRESS, CODE, GATEWAY_ID, GATEWAY_NAME, HOST, PORT, PROTOCOL


def action_type_prefissato():
    """`ActionType`, ma dal modulo che HA ha DAVVERO caricato (prefisso
    `custom_components.vimar_byme_plus.*`), non dal `vimar` nudo che
    conftest.py mette sul path per test_mapping.py.

    Stesso problema di `VimarDataMapper` in `retrieve_data` qui sotto, ma per
    un Enum: `Enum` confronta i membri per IDENTITA', non per valore — due
    classi `ActionType` caricate da due moduli diversi (stesso codice sorgente)
    producono membri che `is` e persino `==` considerano diversi. Chi in un
    test scrive `ActionType.ON` deve prenderlo da qui, non da un
    `import` statico in testa al file.
    """
    return importlib.import_module(
        "custom_components.vimar_byme_plus.vimar.model.enum.action_type"
    ).ActionType


# Dati minimi che il costruttore di Coordinator (_get_gateway_info) legge da
# entry.data — nessuno di questi valori viene davvero usato per connettersi,
# dato che il client e' sostituito, ma le chiavi devono esserci o
# `_get_gateway_info` solleva KeyError prima ancora di arrivare al client.
DATI_ENTRY = {
    HOST: "banco-test.local",
    ADDRESS: "192.0.2.1",
    PORT: "20615",
    GATEWAY_ID: "TESTBENCH0000",
    GATEWAY_NAME: "Banco di prova",
    PROTOCOL: "3.0",
    CODE: "0000",
}


class FakeVimarClient:
    """Sostituisce VimarClient: stesso spazio dei nomi, nessuna rete.

    Ogni metodo che il Coordinator chiama sul client vero e' presente qui.
    `retrieve_data` e' l'unico che deve restituire qualcosa di vero perche' i
    test di lettura abbiano senso; `send` registra ogni chiamata invece di
    ignorarla, perche' i test sulle AZIONI (test_actions.py) devono poter
    verificare cosa l'integrazione avrebbe spedito al gateway.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._componenti = kwargs.pop("componenti", None)
        # (component_id, ActionType, args) — un elemento per ogni comando che
        # una entita' ha provato a mandare al gateway.
        self.chiamate: list[tuple] = []

    def set_setup_code(self, code) -> None: ...
    def has_credentials(self) -> bool:
        return True

    def association_phase(self) -> None: ...
    def operational_phase(self) -> None: ...
    def stop(self) -> None: ...
    def reconnect(self) -> None: ...

    def send(self, component, action_type, *args) -> None:
        self.chiamate.append((component.id, action_type, args))

    def is_thread_alive(self) -> bool:
        return True

    @property
    def seconds_since_last_message(self) -> int:
        return 0

    def retrieve_data(self, options=None):
        # Import DINAMICO, e con il prefisso `custom_components.vimar_byme_plus`
        # — lo stesso con cui il loader di HA ha gia' importato l'integrazione
        # per questo test. conftest.py mette ANCHE il pacchetto `vimar` nudo
        # sul sys.path (serve a test_mapping.py, che gira senza HA): se qui si
        # importasse `from vimar.mapper... import VimarDataMapper` in testa al
        # file, si otterrebbe un modulo caricato una SECONDA volta sotto un
        # nome diverso — stesso codice, classi diverse per identita'. La
        # VimarData risultante userebbe classi di quell'universo duplicato,
        # mentre climate.py/cover.py (importati da HA con il prefisso
        # `custom_components.`) si aspettano quelle del loro. Per liste e
        # attributi letti per duck typing non cambierebbe nulla, ma il mapper
        # energia fa un `isinstance` interno (energy_mapper.py) che con le
        # classi sbagliate direbbe sempre falso. Risolvendo qui, a runtime,
        # si prende sempre il modulo giusto.
        mapper_mod = importlib.import_module(
            "custom_components.vimar_byme_plus.vimar.mapper.vimar_data_mapper"
        )
        return mapper_mod.VimarDataMapper.from_list(self._componenti, options)
