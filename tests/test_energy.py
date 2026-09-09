"""Test sui sensori di energia: il contatore kWh derivato dalla potenza.

L'integrazione non riceve kWh dal gateway: riceve una potenza istantanea e la
integra nel tempo. Tutta la issue #79 vive dentro `Sensor._accumulate_energy`,
e i due sintomi opposti che gli utenti hanno riportato hanno la stessa radice —
l'ancora dell'integrazione non veniva spostata quando doveva:

* SOVRASTIMA (il segnalatore originale, 8,92 kWh contro 1,89 attesi):
  `_create_measure` scartava una lettura di potenza esattamente zero, perche'
  `Decimal("0.000")` e' falsy. Un carico che si spegne non spostava l'ancora, e
  la prima lettura dopo la pausa fatturava TUTTA la pausa alla potenza che il
  carico aveva prima di spegnersi.

* NIENTE ACCUMULO (la verifica successiva dello stesso utente, 0,00000 kWh in
  10 minuti su un carico stabile): l'ancora usava il timestamp dell'elemento
  del gateway, che sta fermo finche' il valore non cambia. Un carico
  perfettamente stabile non produce `changestatus`, quindi non produceva
  energia.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from pytest_homeassistant_custom_component.common import async_fire_time_changed

# I casi d'uso del master.db: "carico_stabile" e' modellato sul "Rack" della
# issue (207 W costanti), "zero" e' un misuratore a 0 W. Ogni misuratore
# produce due sensori (kW e kWh); qui interessa sempre quello di ENERGIA, che
# nel modello ha id `<idsf>_energy` — da cui il suffisso passato a `eid`.
# Gli entity_id NON si scrivono a mano (da HA 2026.9 il core cambia lo schema):
# si risolvono dal registro via `eid`, vedi conftest.py.
CASO_STABILE = "energia_monofase_carico_stabile"
CASO_ZERO = "energia_monofase_zero"


def _entita(hass, entity_id: str):
    componente = hass.data["entity_components"][entity_id.split(".")[0]]
    entita = componente.get_entity(entity_id)
    assert entita is not None, f"{entity_id} non risulta caricata"
    return entita


def _totale(hass, entity_id: str) -> Decimal:
    entita = _entita(hass, entity_id)
    return Decimal(entita._running_total or 0)


async def _esercizio(hass, freezer, minuti: int) -> None:
    """Fa passare `minuti` alla CADENZA VERA dell'integratore: un tick al
    minuto, non un salto unico.

    Saltare in avanti di un'ora in un colpo solo non simula un'ora di
    esercizio: simula un BUCO di un'ora, e l'integratore lo scarta di
    proposito (vedi `_MAX_INTEGRATION_GAP` in sensor.py) invece di fatturarlo
    tutto all'ultima potenza nota — che era la sovrastima della #79.
    """
    for _ in range(minuti):
        freezer.tick(timedelta(seconds=60))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()


async def test_lettura_a_zero_non_viene_scartata(hass, entry_caricata, eid):
    """La meta' "sovrastima" della #79, presa alla radice.

    Non serve simulare la pausa: basta verificare che una potenza di zero
    produca comunque un'ancora. Finche' tornava `{}`, l'ancora restava
    indietro e il tempo a carico spento veniva fatturato alla potenza di
    prima.
    """
    entita = _entita(hass, eid(CASO_ZERO, "sensor", "energy"))
    assert entita._component.native_value == Decimal("0.000")
    misura = entita._create_measure(entita._component)
    assert misura, "una lettura di 0 W e' un dato valido, non un dato mancante"
    assert misura["value"] == Decimal("0.000")


async def test_energia_accumula_a_carico_costante(hass, entry_caricata, freezer, eid):
    """La meta' "niente accumulo": il gateway tace, il contatore deve salire.

    Nessun `changestatus` viene simulato di proposito — e' esattamente la
    condizione in cui l'utente ha misurato 0,00000 kWh in dieci minuti.
    """
    stabile = eid(CASO_STABILE, "sensor", "energy")
    prima = _totale(hass, stabile)

    await _esercizio(hass, freezer, minuti=60)

    dopo = _totale(hass, stabile)
    assert dopo > prima, "un'ora a 207 W deve valere piu' di zero"
    # 0,207 kW per un'ora = 0,207 kWh. Tolleranza larga: quello che conta e'
    # l'ordine di grandezza, non il millesimo.
    assert Decimal("0.19") < (dopo - prima) < Decimal("0.22")


async def test_un_ancora_inservibile_non_congela_il_contatore(
    hass, entry_caricata, freezer, eid
):
    """La causa vera della #79, quella misurata sull'impianto: un solo punto
    di partenza inservibile bloccava il contatore per sempre.

    All'avvio il componente arriva da `sfdiscovery`, che non porta timestamp,
    quindi l'ancora nasceva con `date=None`. Ogni lettura successiva usciva
    sul ramo `interval is None` PRIMA di sostituirla, e l'ancora restava
    `None` per il resto della sessione: i sensori kWh si fermavano sul valore
    ripristinato al boot e non si muovevano piu'.

    Qui l'ancora rotta viene rimessa a mano e si verifica che il contatore
    riesca comunque a ripartire.
    """
    stabile = eid(CASO_STABILE, "sensor", "energy")
    entita = _entita(hass, stabile)
    entita.previous_measure = {"value": Decimal("0.207"), "date": None}

    entita._accumulate_energy()
    assert entita.previous_measure.get("date") is not None, (
        "l'ancora inservibile e' rimasta al suo posto: il contatore e' congelato"
    )

    prima = _totale(hass, stabile)
    await _esercizio(hass, freezer, minuti=10)
    assert _totale(hass, stabile) > prima


async def test_energia_a_zero_non_accumula(hass, entry_caricata, freezer, eid):
    """Contro-prova: contare il tempo non deve voler dire inventare energia."""
    zero = eid(CASO_ZERO, "sensor", "energy")
    prima = _totale(hass, zero)

    await _esercizio(hass, freezer, minuti=60)

    assert _totale(hass, zero) == prima


# ── Il contaimpulsi non e' una potenza (la regressione della 3.3.x) ──────────
#
# `SS_Energy_MeasureCounter` conta gia' da solo: il suo valore e' un TOTALE,
# non una potenza istantanea. Finche' l'entita' decideva se integrare in base
# a `device_class == ENERGY`, il profilo di default del contaimpulsi
# (electricity -> ENERGY) lo faceva finire nell'integratore: il valore
# pubblicato non era piu' la lettura del contatore ma il suo integrale, che
# saliva da solo anche senza un solo aggiornamento dal gateway.
#
# Ora la scelta la dichiara il mapper (`integrate_power`) e il contatore usa
# una classe che quel codice non ce l'ha proprio.


async def test_il_contaimpulsi_non_viene_integrato(hass, entry_caricata, eid):
    """Il contatore pubblica la sua lettura, non un totale calcolato."""
    entita = _entita(hass, eid("contatore_impulsi", "sensor"))
    assert type(entita).__name__ == "Sensor", (
        "il contaimpulsi non deve usare la classe che integra"
    )
    assert entita.native_value == entita._component.native_value


async def test_il_contaimpulsi_non_deriva_da_solo(hass, entry_caricata, freezer, eid):
    """La regressione vera, come l'ha vista l'utente: letture divergenti.

    Il gateway non manda nulla per un'ora; un contatore deve restare dov'e'.
    Prima di questa correzione saliva a ogni tick.
    """
    contatore = _entita(hass, eid("contatore_impulsi", "sensor"))
    prima = contatore.native_value

    await _esercizio(hass, freezer, minuti=60)

    assert contatore.native_value == prima, (
        "il contaimpulsi si e' mosso da solo: sta venendo integrato"
    )


async def test_un_buco_lungo_non_viene_fatturato(hass, entry_caricata, freezer, eid):
    """Resilienza: un'interruzione non si paga all'ultima potenza nota.

    Se HA resta fermo (riavvio, sospensione, gateway irraggiungibile) e poi
    riprende, l'intervallo fra i due punti di integrazione vale ore. Fatturarlo
    per intero all'ultima potenza vista e' esattamente la sovrastima da cui e'
    partita la #79 (8,92 kWh contro 1,89 attesi). Si scarta e si riparte.
    """
    stabile = eid(CASO_STABILE, "sensor", "energy")
    await _esercizio(hass, freezer, minuti=5)
    prima = _totale(hass, stabile)

    freezer.tick(timedelta(hours=3))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert _totale(hass, stabile) == prima, (
        "tre ore di buco sono state fatturate all'ultima potenza nota"
    )


# ── Il tipo dichiarato dal gateway (auto-rilevamento) ────────────────────────
#
# I firmware recenti dicono cosa sta contando l'impulso: un contatore acqua
# reale espone `SFE_State_MeasureType = "WaterCold"` e
# `SFE_State_UnitOfMeasure = "L"`. Prima l'integrazione li ignorava e ripiegava
# sempre su "electricity", cioe' device_class ENERGY e kWh: un contatore
# d'acqua finiva classificato come energia.


async def test_contatore_con_tipo_dichiarato_diventa_acqua(hass, entry_caricata, eid):
    """Il gateway dichiara acqua e litri: HA deve dire acqua e litri."""
    entita = _entita(hass, eid("contatore_acqua_dichiarato", "sensor"))
    assert str(entita.device_class) == "water"
    assert str(entita.native_unit_of_measurement) == "L"
    # Quando il gateway dichiara anche l'unita', il grezzo e' gia' in
    # quell'unita': 1316978 litri, non 1316.978.
    assert entita.native_value == Decimal(1316978)


async def test_contatore_senza_dichiarazione_resta_come_prima(
    hass, entry_caricata, eid
):
    """Firmware che non dichiara nulla: comportamento storico, invariato.

    E' la meta' che protegge gli impianti esistenti dall'auto-rilevamento:
    senza dichiarazione si resta su electricity/kWh con il divisore storico.
    """
    entita = _entita(hass, eid("contatore_impulsi", "sensor"))
    assert str(entita.device_class) == "energy"
    assert entita.native_value == Decimal("1.234")
