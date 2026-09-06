"""I messaggi che finiscono davvero sul filo, non solo l'intenzione di HA.

`test_actions.py` si ferma al confine dell'integrazione: verifica che
`cover.close_cover` produca un `ActionType.CLOSE` con gli argomenti giusti.
Quello che succede DOPO — quale `SFE_Cmd_*` e con quale valore finisce nel
messaggio `doaction` — non era coperto da nessun test, perche' il client
fittizio del banco intercetta la chiamata prima degli action handler.

Questo file copre quel pezzo: `ActionType` in ingresso, lista di `VimarAction`
in uscita.

Gli handler si istanziano con `__new__` e non con il costruttore: `__init__`
apre il database SQLite del gateway (`Database.instance`) per i metodi che
leggono componenti e credenziali, mentre la costruzione delle azioni non tocca
nulla di tutto cio'. Costruire l'oggetto senza il database tiene il test sul
punto che interessa e ne fa fallire la premessa nel momento in cui qualcuno
dovesse spostare la logica dentro `__init__`.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from vimar.model.enum.action_type import ActionType
from vimar.model.enum.sfetype_enum import SfeType
from vimar.service.handler.action_handler.shutter.ss_shutter_position_action_handler import (
    SsShutterPositionActionHandler,
)
from vimar.service.handler.action_handler.shutter.ss_shutter_slat_position_action_handler import (
    SsShutterSlatPositionActionHandler,
)
from vimar.service.handler.action_handler.shutter.ss_shutter_slat_without_position_action_handler import (
    SsShutterSlatWithoutPositionActionHandler,
)


@dataclass
class _Componente:
    """Il minimo che un action handler guarda: l'id e il tipo."""

    id: str = "1042"
    device_name: str = ""


def _handler(classe):
    return object.__new__(classe)


def _coppie(azioni) -> list[tuple[str, str]]:
    """Le azioni in forma leggibile: (sfetype, valore)."""
    return [(a.sfetype, a.value) for a in azioni]


# ── Tapparella semplice: nessuna lamella, nessun comando in piu' ─────────────


@pytest.mark.parametrize(
    ("azione", "atteso"),
    [
        (ActionType.OPEN, [(SfeType.CMD_SHUTTER.value, "0")]),
        (ActionType.CLOSE, [(SfeType.CMD_SHUTTER.value, "100")]),
        (ActionType.STOP, [(SfeType.CMD_SHUTTER.value, "Stop")]),
    ],
)
def test_tapparella_semplice_manda_un_solo_comando(azione, atteso):
    """Contro-prova della correzione della #90: le tapparelle senza lamelle
    non devono aver preso comandi in piu' per effetto collaterale."""
    handler = _handler(SsShutterPositionActionHandler)
    assert _coppie(handler.get_actions(_Componente(), azione)) == atteso


# ── Frangisole (issue #90) ───────────────────────────────────────────────────
#
# Su una veneziana la corsa e l'inclinazione sono un gesto solo: Vimar apre le
# lamelle mentre la tapparella sale e le chiude mentre scende. Mandando solo il
# comando di corsa, una tapparella abbassata da Home Assistant restava chiusa
# ma con le lamelle aperte — cosa che dall'app Vimar non succede.


def test_frangisole_chiudendo_chiude_anche_le_lamelle():
    handler = _handler(SsShutterSlatPositionActionHandler)
    azioni = handler.get_actions(_Componente(), ActionType.CLOSE)
    assert _coppie(azioni) == [
        (SfeType.CMD_SHUTTER.value, "100"),
        (SfeType.CMD_SLAT.value, "100"),
    ]


def test_frangisole_aprendo_apre_anche_le_lamelle():
    handler = _handler(SsShutterSlatPositionActionHandler)
    azioni = handler.get_actions(_Componente(), ActionType.OPEN)
    assert _coppie(azioni) == [
        (SfeType.CMD_SHUTTER.value, "0"),
        (SfeType.CMD_SLAT.value, "0"),
    ]


def test_frangisole_senza_posizione_accoppia_corsa_e_lamelle():
    handler = _handler(SsShutterSlatWithoutPositionActionHandler)
    giu = handler.get_actions(_Componente(), ActionType.CLOSE)
    su = handler.get_actions(_Componente(), ActionType.OPEN)
    assert _coppie(giu) == [
        (SfeType.CMD_SHUTTER_WITHOUT_POSITION.value, "Down"),
        (SfeType.CMD_SLAT_WITHOUT_POSITION.value, "Close"),
    ]
    assert _coppie(su) == [
        (SfeType.CMD_SHUTTER_WITHOUT_POSITION.value, "Up"),
        (SfeType.CMD_SLAT_WITHOUT_POSITION.value, "Open"),
    ]


def test_frangisole_la_sola_inclinazione_resta_isolata():
    """Muovere le lamelle non deve muovere la tapparella: l'accoppiamento
    vale in un verso solo."""
    handler = _handler(SsShutterSlatPositionActionHandler)
    azioni = handler.get_actions(_Componente(), ActionType.SET_SLAT_POSITION, "70")
    assert _coppie(azioni) == [(SfeType.CMD_SLAT.value, "70")]


def test_frangisole_stop_non_tocca_le_lamelle():
    """Uno stop a meta' corsa e' una richiesta di fermarsi, non di inclinare."""
    handler = _handler(SsShutterSlatPositionActionHandler)
    azioni = handler.get_actions(_Componente(), ActionType.STOP)
    assert _coppie(azioni) == [(SfeType.CMD_SHUTTER.value, "Stop")]


def test_frangisole_set_position_non_tocca_le_lamelle():
    """Portare la tapparella a una quota intermedia lascia decidere
    l'inclinazione a chi l'ha chiesta."""
    handler = _handler(SsShutterSlatPositionActionHandler)
    azioni = handler.get_actions(_Componente(), ActionType.SET_POSITION, "30")
    assert _coppie(azioni) == [(SfeType.CMD_SHUTTER.value, "30")]
