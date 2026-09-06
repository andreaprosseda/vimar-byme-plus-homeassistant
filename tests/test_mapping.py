"""Il mapping del master.db: nessun crash, e ogni caso d'uso produce il suo.

Questo file e' la rete che avrebbe fermato la 3.2.0. Il bug era
`VimarCover.__init__() got an unexpected keyword argument 'is_closing'`: un
TypeError sollevato durante il mapping, che mandava l'INTERA integrazione in
`setup_retry`. `test_mapping_non_solleva_eccezioni` fallisce su quel commit.
"""

from __future__ import annotations

import pytest
from vimar.mapper.vimar_data_mapper import VimarDataMapper
from vimar.model.component.vimar_climate import VimarClimate
from vimar.model.component.vimar_cover import VimarCover
from vimar.model.component.vimar_light import VimarLight
from vimar.model.component.vimar_sensor import VimarSensor
from vimar.model.enum.sstype_enum import SsType

# Gli SsType che l'integrazione non implementa ancora. Stanno nel master.db
# APPOSTA: devono essere ignorati in silenzio, non far cadere il mapping. Il
# giorno che uno di questi riceve un mapper, va tolto da qui e il test
# `test_i_non_mappati_non_producono_entita` fallisce ricordandolo.
NON_MAPPATI = {
    SsType.CLIMA_CONTROL.value,
    SsType.CLIMA_DAIKIN.value,
    SsType.CLIMA_DAIKIN_VRV.value,
    SsType.CLIMA_HUMIDITY.value,
    SsType.CLIMA_INTERFACE_CONTACT.value,
    SsType.CLIMA_LG.value,
    SsType.CLIMA_MITSUBISHI.value,
    SsType.CLIMA_MITSUBISHI_NO_FAN.value,
    SsType.CLIMA_PRESSURE.value,
    SsType.CLIMA_RAIN_AMOUNT.value,
    SsType.CLIMA_TEMPERATURE.value,
    SsType.CLIMA_WIND_SPEED.value,
    SsType.CLIMA_ZONE_VRV.value,
    # Ha un mapper, ma il suo `_from_obj` e' uno stub che solleva
    # NotImplementedError di proposito.
    SsType.LIGHT_CONSTANT_CONTROL.value,
}

# Hanno un mapper, ma restituisce una lista vuota DI PROPOSITO: sono
# funzioni del gateway che non hanno un corrispettivo in Home Assistant
# (i timer li programma l'app Vimar, il sinottico e' una vista). Non vanno
# confusi con i NON_MAPPATI: qui il mapper c'e' e la scelta e' deliberata.
SENZA_ENTITA = {
    SsType.AUTOMATION_TIMER_ASTRONOMIC.value,
    SsType.AUTOMATION_TIMER_PERIODIC.value,
    SsType.AUTOMATION_TIMER_WEEKLY.value,
    "SS_Synoptic",  # nemmeno presente nell'enum SsType: filtrato a monte
}


def test_mapping_non_solleva_eccezioni(componenti):
    """Il guasto della 3.2.0: un mapper che esplode ferma tutta l'integrazione."""
    entita = VimarDataMapper.from_list(componenti).get_all()
    assert entita, "il mapping non ha prodotto nessuna entita'"


def test_ogni_componente_mappato_produce_entita(componenti, per_caso):
    """Un caso d'uso che smette di produrre entita' e' una regressione muta.

    Non conta QUANTE: conta che il componente non sparisca. E' il modo in cui
    si accorge di un `sftype` sbagliato, che non solleva errori — semplicemente
    fa cadere il componente fuori dal dispatcher (successo davvero: le tende
    stavano sotto SF_Shutter, non SF_Curtain).
    """
    per_nome = {c.name: c for c in componenti}
    vuoti = [
        nome
        for nome, ents in per_caso.items()
        if not ents and per_nome[nome].sstype not in (NON_MAPPATI | SENZA_ENTITA)
    ]
    assert not vuoti, f"casi d'uso senza entita': {sorted(vuoti)}"


def test_i_non_mappati_non_producono_entita(componenti, per_caso):
    """Gli SsType non implementati vanno ignorati, non mappati per sbaglio."""
    per_nome = {c.name: c for c in componenti}
    inattesi = [
        nome
        for nome, ents in per_caso.items()
        if ents and per_nome[nome].sstype in NON_MAPPATI
    ]
    assert not inattesi, (
        f"questi SsType risultano mappati ma sono elencati fra i NON_MAPPATI: "
        f"{sorted(inattesi)} — se ora hanno un mapper, aggiorna la costante"
    )


def test_tutti_i_sstype_dell_enum_sono_nel_fixture(componenti):
    """Il master.db deve restare completo quando l'enum cresce."""
    presenti = {c.sstype for c in componenti}
    mancanti = {e.value for e in SsType} - presenti
    assert not mancanti, (
        f"SsType senza un caso d'uso nel master.db: {sorted(mancanti)} — "
        f"aggiungilo in tests/build_master_db.py e rigenera"
    )


# ── Contratti per famiglia ─────────────────────────────────────────────────
# Non ripetono la logica dei mapper: fissano il patto che le entita' devono
# rispettare, quello su cui Home Assistant fa affidamento.


@pytest.mark.parametrize(
    ("caso", "posizione_vimar"),
    [
        ("cover_chiusa", 100),
        ("cover_aperta_50_percento", 50),
        ("cover_aperta", 0),
    ],
)
def test_posizione_delle_coperture(per_caso, caso, posizione_vimar):
    """Il MODELLO porta la scala Vimar (100 = chiusa), non quella di HA.

    L'inversione la fa l'entita' (`cover.py`: `100 - position`). Fissarla qui
    e' voluto: se qualcuno spostasse l'inversione nel mapper senza togliere
    quella dell'entita', le tapparelle si ribalterebbero e questo test lo
    direbbe subito.
    """
    assert _unica(per_caso, caso, VimarCover).current_cover_position == posizione_vimar


def test_cover_chiusa_si_dichiara_chiusa(per_caso):
    assert _unica(per_caso, "cover_chiusa", VimarCover).is_closed is True


def test_cover_aperta_non_si_dichiara_chiusa(per_caso):
    assert _unica(per_caso, "cover_aperta", VimarCover).is_closed is False


def test_cover_in_movimento(per_caso):
    """`Change to 75` e' come il gateway annuncia una corsa in atto."""
    assert _unica(per_caso, "cover_in_movimento", VimarCover).is_moving is True


@pytest.mark.parametrize(
    ("caso", "accesa"),
    [("luce_spenta", False), ("luce_accesa", True)],
)
def test_stato_delle_luci(per_caso, caso, accesa):
    assert _unica(per_caso, caso, VimarLight).is_on is accesa


@pytest.mark.parametrize(
    ("caso", "luminosita"),
    [
        ("dimmer_acceso_1_percento", 1),
        ("dimmer_acceso_50_percento", 50),
        ("dimmer_acceso_100_percento", 100),
    ],
)
def test_luminosita_dei_dimmer(per_caso, caso, luminosita):
    assert _unica(per_caso, caso, VimarLight).brightness == luminosita


def test_clima_spento(per_caso):
    clima = _unica(per_caso, "clima_spento", VimarClimate)
    assert clima.hvac_mode is not None


def test_clima_senza_permessi_non_offre_il_cambio_modo(per_caso):
    """Issue #85: senza `SFE_Cmd_ChangeOverMode` niente switch caldo/freddo.

    Il termostato resta comandabile (acceso/spento sulla modalita' che ha),
    ma le modalita' offerte non possono includerle entrambe.
    """
    clima = _unica(per_caso, "clima_senza_permessi_cambio_modo", VimarClimate)
    modi = {str(m.value) for m in (clima.hvac_modes or [])}
    assert not {"heat", "cool"}.issubset(modi), (
        f"senza permessi non deve offrire sia heat che cool: {modi}"
    )


def test_sensore_temperatura_ha_unita(per_caso):
    """Uno dei 18 mapper che nessuna installazione del campione esercitava."""
    sensori = [e for e in per_caso["temperatura"] if isinstance(e, VimarSensor)]
    assert sensori, "il sensore temperatura non produce entita'"
    assert sensori[0].unit_of_measurement


def _unica(per_caso, caso: str, tipo):
    """L'entita' di quel tipo prodotta dal caso d'uso, con errore parlante."""
    assert caso in per_caso, f"caso d'uso assente dal master.db: {caso}"
    trovate = [e for e in per_caso[caso] if isinstance(e, tipo)]
    assert trovate, (
        f"il caso '{caso}' non ha prodotto nessuna {tipo.__name__}: "
        f"ha prodotto {[type(e).__name__ for e in per_caso[caso]]}"
    )
    return trovate[0]
