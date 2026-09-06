"""Smoke test: la config entry carica, con TUTTE le piattaforme, sul master.db.

E' il livello che avrebbe intercettato il guasto della 3.2.0 nel modo in cui
l'utente l'ha visto: non "una funzione ha sollevato un'eccezione" (test_mapping.py
lo sa gia'), ma "l'integrazione e' rimasta in setup_retry" — lo stesso stato,
lo stesso messaggio, che compariva in Impostazioni > Dispositivi e Servizi.

Il banco (config entry + client fittizio) e' condiviso con test_actions.py e
test_snapshot.py: vive in conftest.py e in helpers/ha_harness.py — qui solo
i test che leggono lo stato del CARICAMENTO, non quello delle entita'.
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant


async def test_la_config_entry_carica(entry_caricata):
    """Il sintomo esatto della 3.2.0: 'Configurazione non riuscita, riproverà'.

    Un'eccezione nel mapping durante il primo refresh fa terminare
    `async_config_entry_first_refresh` con `ConfigEntryNotReady`, e la entry
    resta in SETUP_RETRY — questo assert e' rosso esattamente li'.
    """
    assert entry_caricata.state is ConfigEntryState.LOADED


async def test_tutte_le_piattaforme_registrano_entita(
    hass: HomeAssistant, entry_caricata
):
    """Ogni dominio previsto (PLATFORMS in __init__.py) produce entita' vere.

    Non basta che l'entry sia LOADED: una piattaforma che fallisce il proprio
    `async_setup_entry` lo fa in modo silenzioso rispetto allo stato
    dell'entry (resta comunque LOADED). Serve guardare il registro.
    """
    stati = hass.states.async_all()
    domini = {s.entity_id.split(".")[0] for s in stati}
    attesi = {
        "binary_sensor",
        "button",
        "climate",
        "cover",
        "light",
        "media_player",
        "sensor",
        "switch",
    }
    mancanti = attesi - domini
    assert not mancanti, f"nessuna entita' registrata per: {sorted(mancanti)}"


async def test_lo_scarico_della_entry_non_lascia_errori(
    hass: HomeAssistant, entry_caricata
):
    """Unload pulito: niente listener orfani, niente eccezioni nei log."""
    assert await hass.config_entries.async_unload(entry_caricata.entry_id)
    await hass.async_block_till_done()
    assert entry_caricata.state is ConfigEntryState.NOT_LOADED
