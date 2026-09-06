"""Snapshot: OGNI attributo di OGNI entita' prodotta dal master.db, in un colpo.

test_mapping.py verifica un pugno di campi scelti a mano, per quattro domini
su otto (Cover, Climate, Light, Sensor) — Switch, BinarySensor, MediaPlayer,
Button non hanno un solo assert sul CONTENUTO delle loro entita', solo "non
sono sparite" (test_ogni_componente_mappato_produce_entita).

Scrivere quei contratti a mano per gli altri quattro domini costerebbe
parecchio per un ritorno modesto (sono in gran parte pass-through: on/off).
Uno snapshot fa lo stesso lavoro all'incontrario: cattura TUTTO cio' che le
134 entita' del master.db espongono — entity_registry (unique_id, device_class,
...) e stato live (state + attributes) — per OGNI dominio insieme, e fa
fallire il test se qualcosa cambia rispetto all'ultima approvazione. Non dice
"perche'" un valore e' quello giusto (per quello servono i contratti mirati
di test_mapping.py/test_actions.py): dice "e' cambiato qualcosa, guardalo".

COME SI AGGIORNA
-----------------
Un cambiamento voluto (nuovo mapper, campo in piu', nome diverso) fa fallire
questo test finche' non si rigenera lo snapshot:

    python3 -m pytest tests/test_snapshot.py --snapshot-update

Rivedi il diff in tests/__snapshots__/ prima di committarlo — e' li' che si
vede a colpo d'occhio SE il cambiamento era davvero quello voluto.
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from syrupy.assertion import SnapshotAssertion


async def test_ogni_entita_del_master_db(
    hass: HomeAssistant, entry_caricata, snapshot: SnapshotAssertion
):
    """Variante di `pytest_homeassistant_custom_component.common.snapshot_platform`
    senza il suo vincolo "un solo dominio per chiamata" — qui la config entry
    carica le otto piattaforme insieme, ed e' proprio quell'insieme che
    interessa fotografare in un unico file invece che con otto chiamate."""
    registro = er.async_get(hass)
    entries = er.async_entries_for_config_entry(registro, entry_caricata.entry_id)
    assert entries, "nessuna entita' registrata: il setup non ha prodotto nulla"

    # Ordine stabile: altrimenti il file di snapshot cambierebbe riga per
    # riga ad ogni rigenerazione anche senza nessuna modifica vera, solo
    # perche' l'ordine di scoperta dei componenti non e' garantito.
    for entry in sorted(entries, key=lambda e: e.entity_id):
        assert entry == snapshot(name=f"{entry.entity_id}-registry")
        assert entry.disabled_by is None, f"{entry.entity_id} risulta disabilitata"
        stato = hass.states.get(entry.entity_id)
        assert stato, f"nessuno stato live per {entry.entity_id}"
        assert stato == snapshot(name=f"{entry.entity_id}-state")
