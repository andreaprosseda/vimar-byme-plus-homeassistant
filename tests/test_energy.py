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

# Il caso d'uso del master.db e' modellato sul "Rack" della issue: 207 W
# costanti. `..._2` e' l'entita' kWh, quella senza suffisso e' i kW.
STABILE_KWH = "sensor.energia_monofase_carico_stabile_2"
ZERO_KWH = "sensor.energia_monofase_zero_2"


def _entita(hass, entity_id: str):
    componente = hass.data["entity_components"][entity_id.split(".")[0]]
    entita = componente.get_entity(entity_id)
    assert entita is not None, f"{entity_id} non risulta caricata"
    return entita


def _totale(hass, entity_id: str) -> Decimal:
    entita = _entita(hass, entity_id)
    return Decimal(entita._running_total or 0)


async def test_lettura_a_zero_non_viene_scartata(hass, entry_caricata):
    """La meta' "sovrastima" della #79, presa alla radice.

    Non serve simulare la pausa: basta verificare che una potenza di zero
    produca comunque un'ancora. Finche' tornava `{}`, l'ancora restava
    indietro e il tempo a carico spento veniva fatturato alla potenza di
    prima.
    """
    entita = _entita(hass, ZERO_KWH)
    assert entita._component.native_value == Decimal("0.000")
    misura = entita._create_measure(entita._component)
    assert misura, "una lettura di 0 W e' un dato valido, non un dato mancante"
    assert misura["value"] == Decimal("0.000")


async def test_energia_accumula_a_carico_costante(hass, entry_caricata, freezer):
    """La meta' "niente accumulo": il gateway tace, il contatore deve salire.

    Nessun `changestatus` viene simulato di proposito — e' esattamente la
    condizione in cui l'utente ha misurato 0,00000 kWh in dieci minuti.
    """
    prima = _totale(hass, STABILE_KWH)

    freezer.tick(timedelta(hours=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    dopo = _totale(hass, STABILE_KWH)
    assert dopo > prima, "un'ora a 207 W deve valere piu' di zero"
    # 0,207 kW per un'ora = 0,207 kWh. Tolleranza larga: quello che conta e'
    # l'ordine di grandezza, non il millesimo.
    assert Decimal("0.19") < (dopo - prima) < Decimal("0.22")


async def test_un_ancora_inservibile_non_congela_il_contatore(
    hass, entry_caricata, freezer
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
    entita = _entita(hass, STABILE_KWH)
    entita.previous_measure = {"value": Decimal("0.207"), "date": None}

    entita._accumulate_energy()
    assert entita.previous_measure.get("date") is not None, (
        "l'ancora inservibile e' rimasta al suo posto: il contatore e' congelato"
    )

    prima = _totale(hass, STABILE_KWH)
    freezer.tick(timedelta(hours=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()
    assert _totale(hass, STABILE_KWH) > prima


async def test_energia_a_zero_non_accumula(hass, entry_caricata, freezer):
    """Contro-prova: contare il tempo non deve voler dire inventare energia."""
    prima = _totale(hass, ZERO_KWH)

    freezer.tick(timedelta(hours=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert _totale(hass, ZERO_KWH) == prima
