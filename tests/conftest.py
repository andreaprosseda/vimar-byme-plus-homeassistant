"""Configurazione pytest: mette il core `vimar` sul path e offre le fixture.

Il pacchetto `vimar` vive dentro `custom_components/vimar_byme_plus/` perche'
e' cosi' che HACS lo distribuisce. Per i test lo si importa direttamente da li'
— stesso espediente del symlink `standalone/vimar`, ma senza symlink: una riga
di sys.path, che funziona uguale su Windows e in CI.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# pytest-homeassistant-custom-component: abilita il caricamento dei componenti
# custom (di default HA in test rifiuta tutto cio' che non e' nel core), e
# fornisce automaticamente la fixture `hass`. Solo test_setup.py la usa
# davvero; test_mapping.py non la tocca e resta cosi' veloce com'era.
pytest_plugins = "pytest_homeassistant_custom_component"

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / "custom_components" / "vimar_byme_plus"))
sys.path.insert(0, str(RADICE))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# La fixture `hass` del plugin monta come "config dir" la cartella
# `testing_config/` DENTRO al pacchetto p-h-c-c installato, e importa
# `custom_components` da LI' (vedi homeassistant/loader.py
# `_async_mount_config_dir`, chiamata da `HomeAssistant.__init__` durante
# `async_test_home_assistant`). Il pacchetto p-h-c-c ne ha uno suo (usato dai
# LORO test interni), con un vero `__init__.py`: appena viene importato UNA
# volta come `custom_components` nudo, resta fissato in sys.modules per
# l'intera sessione di test — nessun sys.path.insert successivo lo sposta
# piu'. Patchando `get_test_config_dir` (che quella fixture chiama solo
# quando NON le viene passato un config_dir esplicito) il "config dir di
# test" diventa la radice DI QUESTO repo, che contiene la NOSTRA
# `custom_components/vimar_byme_plus` — cosi' e' quella che HA trova.
import pytest_homeassistant_custom_component.common as _phcc_common

_phcc_common.get_test_config_dir = lambda *aggiunta: (
    str(RADICE.joinpath(*aggiunta)) if aggiunta else str(RADICE)
)


FIXTURES = Path(__file__).resolve().parent / "fixtures"
MASTER_DB = FIXTURES / "master.db"


@pytest.fixture(scope="session")
def componenti():
    """I 95 casi d'uso del master.db, come `UserComponent`."""
    from helpers.db_loader import carica_componenti

    return carica_componenti(MASTER_DB)


@pytest.fixture(scope="session")
def entita(componenti):
    """Le entita' prodotte dal mapping completo del master.db."""
    from vimar.mapper.vimar_data_mapper import VimarDataMapper

    return VimarDataMapper.from_list(componenti).get_all()


@pytest.fixture(scope="session")
def per_caso(componenti, entita):
    """Entita' raggruppate per slug del caso d'uso che le ha generate.

    L'id di ogni entita' comincia con l'idsf del componente (a volte con un
    suffisso: `1042_power`, `1042_energy`), quindi il legame si ricostruisce
    dal prefisso numerico.
    """
    per_idsf = {str(c.idsf): c.name for c in componenti}
    gruppi: dict[str, list] = {c.name: [] for c in componenti}
    for e in entita:
        radice = str(e.id).split("_")[0]
        nome = per_idsf.get(radice)
        if nome:
            gruppi[nome].append(e)
    return gruppi


# ── Banco con Home Assistant vero (test_setup.py, test_actions.py,
#    test_snapshot.py) ─────────────────────────────────────────────────────
# Solo questi tre file chiedono `hass`/`enable_custom_integrations`: e' li'
# che pytest-homeassistant-custom-component avvia davvero un'istanza di HA,
# il pezzo lento (relativamente: ~0.1s) e superfluo per test_mapping.py.


@pytest.fixture
def client_fittizio(componenti):
    """Fabbrica di FakeVimarClient gia' agganciata ai componenti del master.db.

    VimarClient nel Coordinator viene istanziato come `VimarClient(gateway_info,
    callback)` — posizionale, senza il kwarg `componenti` che il fake usa
    internamente. Il lambda lo inietta senza toccare la firma che il
    Coordinator si aspetta.

    La fabbrica tiene anche un riferimento all'ULTIMA istanza creata
    (`fabbrica.istanza`): il Coordinator ne crea esattamente una per config
    entry, ed e' quella che i test sulle azioni devono poter ispezionare
    dopo il setup — vedi la fixture `client` sotto.
    """
    from helpers.ha_harness import FakeVimarClient

    def fabbrica(*args, **kwargs):
        fabbrica.istanza = FakeVimarClient(*args, componenti=componenti, **kwargs)
        return fabbrica.istanza

    return fabbrica


@pytest.fixture
async def entry_caricata(hass, enable_custom_integrations, client_fittizio):
    """La config entry Vimar, caricata per davvero, sul master.db."""
    from helpers.ha_harness import DATI_ENTRY
    from homeassistant.core import (
        HomeAssistant,  # noqa: F401  (per i type hint dei chiamanti)
    )
    from pytest_homeassistant_custom_component.common import MockConfigEntry

    entry = MockConfigEntry(
        domain="vimar_byme_plus", data=DATI_ENTRY, unique_id="TESTBENCH0000"
    )
    entry.add_to_hass(hass)
    with patch(
        "custom_components.vimar_byme_plus.coordinator.VimarClient",
        side_effect=client_fittizio,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    return entry


@pytest.fixture
def client(client_fittizio, entry_caricata):
    """Il FakeVimarClient che il Coordinator ha davvero istanziato.

    Dipende da `entry_caricata` non per il suo valore ma per il suo EFFETTO
    (il setup, che e' quello che popola `client_fittizio.istanza`): senza
    questa dipendenza esplicita, pytest potrebbe risolvere `client` prima
    che il setup sia mai avvenuto.
    """
    return client_fittizio.istanza
