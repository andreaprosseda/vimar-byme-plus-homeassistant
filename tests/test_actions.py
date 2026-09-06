"""Test sulle AZIONI: quando HA comanda qualcosa, il gateway riceve il comando giusto.

Tutto quello scritto finora (test_mapping.py, test_setup.py) verifica una sola
direzione: gateway → HA, cioe' "leggere" uno stato. Zero di quei test tocca
l'altra direzione, HA → gateway, cioe' i 45 metodi `set_*`/`turn_on`/`press`
sparsi in climate.py, cover.py, light.py, switch.py, button.py.

Non e' un buco astratto: le DUE issue vere lavorate in questa sessione erano
entrambe qui. La #87 (la temperatura impostata da HA non arrivava al
termostato) e la #85 (il gate sui permessi bloccava anche `turn_on`/`turn_off`,
non solo lo switch caldo/freddo) sono bug nel percorso di INVIO — un percorso
che, prima di questo file, non aveva un solo assert sopra.

Il banco (`entry_caricata`, `client`) e' condiviso con test_setup.py — vive in
conftest.py e in helpers/ha_harness.py. `ActionType` va importato con
`helpers.ha_harness.action_type_prefissato()`, non con uno statico in testa al
file: vedi il motivo li' dentro, e' lo stesso dei due universi di moduli
risolto per VimarDataMapper.
"""

from __future__ import annotations

import pytest
from helpers.ha_harness import action_type_prefissato
from homeassistant.components.climate import HVACMode
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError


def _entita(hass: HomeAssistant, entity_id: str):
    """L'oggetto entita' vero e proprio, non solo il suo stato.

    Serve per i controlli che vivono dentro i metodi dell'entita' e che la
    validazione dei servizi di HA intercetterebbe prima.
    """
    dominio = entity_id.split(".")[0]
    componente = hass.data["entity_components"][dominio]
    entita = componente.get_entity(entity_id)
    assert entita is not None, f"{entity_id} non risulta caricata"
    return entita


async def _comanda(
    hass: HomeAssistant, domain: str, service: str, entity_id: str, **dati
) -> None:
    await hass.services.async_call(
        domain, service, {ATTR_ENTITY_ID: entity_id, **dati}, blocking=True
    )
    await hass.async_block_till_done()


def _ultima(client, action_type=None):
    """L'ultima chiamata registrata (id, ActionType, args), o quella di un
    ActionType preciso se piu' di un comando e' partito per lo stesso tap."""
    chiamate = client.chiamate
    assert chiamate, "nessuna chiamata verso il gateway: il comando non e' partito"
    if action_type is None:
        return chiamate[-1]
    per_tipo = [c for c in chiamate if c[1] == action_type]
    assert per_tipo, f"nessuna chiamata {action_type} fra {chiamate}"
    return per_tipo[-1]


# ── Luci ─────────────────────────────────────────────────────────────────────


async def test_luce_turn_on(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(hass, "light", "turn_on", "light.luce_spenta")
    _id, tipo, _args = _ultima(client)
    assert tipo is ActionType.ON


async def test_luce_turn_off(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(hass, "light", "turn_off", "light.luce_accesa")
    _id, tipo, _args = _ultima(client)
    assert tipo is ActionType.OFF


# ── Interruttori ─────────────────────────────────────────────────────────────


async def test_switch_turn_on(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(hass, "switch", "turn_on", "switch.automazione_spenta")
    _id, tipo, _args = _ultima(client)
    assert tipo is ActionType.ON


# ── Coperture ────────────────────────────────────────────────────────────────


async def test_cover_open(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(hass, "cover", "open_cover", "cover.cover_chiusa")
    _id, tipo, _args = _ultima(client)
    assert tipo is ActionType.OPEN


async def test_cover_close(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(hass, "cover", "close_cover", "cover.cover_aperta")
    _id, tipo, _args = _ultima(client)
    assert tipo is ActionType.CLOSE


@pytest.mark.parametrize(
    ("posizione_ha", "posizione_vimar_attesa"),
    [
        (100, "0"),  # tutta aperta per HA = 0 nella scala Vimar
        (0, "100"),  # tutta chiusa per HA = 100 nella scala Vimar
        (30, "70"),
    ],
)
async def test_cover_set_position_inverte_la_scala(
    hass, entry_caricata, client, posizione_ha, posizione_vimar_attesa
):
    """Il punto piu' delicato scoperto costruendo il master.db (test_mapping.py):
    nel MODELLO 100 = chiusa, ma HA usa la convenzione opposta. La lettura era
    gia' verificata; qui si verifica che anche la SCRITTURA converta nel verso
    giusto — non per caso, `cover.py` fa `str(100 - int(position))`.
    """
    ActionType = action_type_prefissato()
    await _comanda(
        hass,
        "cover",
        "set_cover_position",
        "cover.cover_aperta_50_percento",
        position=posizione_ha,
    )
    _id, _tipo, args = _ultima(client, ActionType.SET_POSITION)
    assert args == (posizione_vimar_attesa,)


# ── Clima ────────────────────────────────────────────────────────────────────


async def test_clima_set_temperature(hass, entry_caricata, client):
    """Issue #87: la temperatura impostata da HA non arrivava al termostato.
    Qui non si puo' verificare il gateway vero (non c'e'), ma si verifica che
    l'integrazione mandi DAVVERO il comando — cosa che, prima di questo file,
    nessun test faceva."""
    ActionType = action_type_prefissato()
    await _comanda(
        hass, "climate", "set_temperature", "climate.clima_caldo", temperature=21.5
    )
    _id, _tipo, args = _ultima(client, ActionType.SET_TEMP)
    assert args == (21.5,)


async def test_clima_set_hvac_mode_con_permessi(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(
        hass, "climate", "set_hvac_mode", "climate.clima_caldo", hvac_mode="cool"
    )
    _id, _tipo, args = _ultima(client, ActionType.SET_HVAC_MODE)
    assert args == ("cool",)


# ── Clima senza il grant sul change-over (issue #85) ─────────────────────────
#
# `clima_senza_permessi_cambio_modo` riproduce il caso piu' comune che si
# trova sugli impianti veri: il componente non porta affatto
# `SFE_Cmd_ChangeOverMode`. Sui 19 database reali sono 74 zone su 114 (64%).
#
# Prima della correzione TUTTE quelle zone erano completamente immobili da
# Home Assistant: `set_hvac_mode` alzava "Insufficient permissions" per
# qualsiasi modalita', OFF compreso, mentre `hvac_modes` continuava a offrire
# `off` e la stagione corrente come se funzionassero.

SENZA_PERMESSI = "climate.clima_senza_permessi_cambio_modo"


async def test_clima_senza_permessi_si_puo_spegnere(hass, entry_caricata, client):
    """Spegnere non tocca il change-over: il grant non c'entra."""
    ActionType = action_type_prefissato()
    await _comanda(hass, "climate", "turn_off", SENZA_PERMESSI)
    _id, _tipo, args = _ultima(client, ActionType.SET_HVAC_MODE)
    assert args == ("off",)


async def test_clima_senza_permessi_si_puo_riaccendere(hass, entry_caricata, client):
    """Riaccendere nella stagione gia' impostata dall'impianto neppure."""
    ActionType = action_type_prefissato()
    await _comanda(hass, "climate", "turn_on", SENZA_PERMESSI)
    _id, _tipo, args = _ultima(client, ActionType.SET_HVAC_MODE)
    assert args == ("cool",)  # lo stato ChangeOverMode del fixture e' Cooling


async def test_clima_senza_permessi_rifiuta_il_cambio_stagione(
    hass, entry_caricata, client
):
    """Il gate resta, ma solo su cio' che il grant copre davvero.

    Va chiamato sull'entita' e non via servizio: `hvac_modes` non offre
    `heat` per questa zona, quindi la validazione di HA rifiuterebbe la
    richiesta prima di arrivare al controllo dell'integrazione e il test
    passerebbe per il motivo sbagliato.
    """
    entita = _entita(hass, SENZA_PERMESSI)
    with pytest.raises(HomeAssistantError, match="[Pp]ermission"):
        entita.set_hvac_mode(HVACMode.HEAT)
    assert not client.chiamate, "il comando non doveva raggiungere il gateway"


async def test_clima_set_fan_mode(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(
        hass, "climate", "set_fan_mode", "climate.clima_caldo", fan_mode="high"
    )
    _id, _tipo, args = _ultima(client, ActionType.SET_LEVEL)
    assert args == ("high",)


# ── Pulsanti (scene) ─────────────────────────────────────────────────────────


async def test_button_press(hass, entry_caricata, client):
    ActionType = action_type_prefissato()
    await _comanda(hass, "button", "press", "button.scena_a_riposo")
    _id, tipo, _args = _ultima(client, ActionType.PRESS)
    assert tipo is ActionType.PRESS
