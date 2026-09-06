"""Genera `fixtures/master.db`: un solo home.db con OGNI caso d'uso testabile.

PERCHE' UN DATABASE SOLO
------------------------
I 19 home.db di installazioni reali coprono 42 mapper su 60, ma sono privati
(la tabella `users` contiene setup code e password di gateway altrui) e
ridondanti: diciassette contengono la stessa luce accesa. Questo script li
distilla in un unico database anonimo in cui ogni componente e' UN CASO D'USO,
col nome che lo dice: `luce_spenta`, `cover_aperta_50_percento`,
`clima_freddo_senza_permessi`.

Il vantaggio non e' la dimensione: e' che un test che fallisce nomina da solo
lo scenario rotto, senza che nessuno debba aprire il SQLite per capirlo.

ANONIMO PER COSTRUZIONE
-----------------------
Nessun dato reale viene copiato. Lo script parte da `element_templates.json`,
che contiene solo la FORMA dei componenti (quali SFE esistono per ogni SsType,
il loro `enable` e un valore di esempio) estratta dal corpus, e ricostruisce
tutto da zero: ambienti generici, nomi di caso d'uso, tabella `users` vuota.
I 19 database originali non servono per rigenerarlo.

COSA COPRE
----------
1. i 42 SsType presenti nel corpus, con le loro varianti di stato;
2. i 18 SsType che hanno un mapper ma che nessuna installazione del campione
   usava — sono la meta' scoperta, quella dove i bug passano inosservati;
3. i 13 SsType che NON hanno ancora un mapper (le varianti clima Daikin, LG,
   Mitsubishi, VRV...). Oggi devono produrre zero entita' senza far crashare
   il mapping; il giorno che qualcuno scrive il mapper, la fixture c'e' gia'.

Uso:  python3 tests/build_master_db.py
"""

from __future__ import annotations

import json
import os
import sqlite3

QUI = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(QUI, "fixtures", "element_templates.json")
USCITA = os.path.join(QUI, "fixtures", "master.db")

# ── Ambienti ────────────────────────────────────────────────────────────────
# Generici e tematici: raggruppano per famiglia invece che per stanza, cosi'
# un test puo' isolare "tutte le coperture" senza sapere nomi di casa altrui.
AMBIENTI = [
    "Luci",
    "Coperture",
    "Clima",
    "Energia",
    "Accessi",
    "Sensori",
    "Audio",
    "Scene",
    "Automazioni",
    "Irrigazione",
    "Non mappati",
]

# ── I casi d'uso ────────────────────────────────────────────────────────────
# (sstype, ambiente, [(slug_caso, {sfetype: valore, ...}), ...])
#
# Gli override toccano SOLO gli SFE che definiscono il caso: tutto il resto
# viene dal template, cosi' i componenti restano realistici. Un valore None
# rimuove l'elemento (serve a simulare un gateway che non lo espone).
CASI: list[tuple[str, str, list[tuple[str, dict]]]] = [
    # ── Luci ────────────────────────────────────────────────────────────────
    (
        "SS_Light_Switch",
        "Luci",
        [
            ("luce_spenta", {"SFE_State_OnOff": "Off"}),
            ("luce_accesa", {"SFE_State_OnOff": "On"}),
        ],
    ),
    (
        "SS_Light_Dimmer",
        "Luci",
        [
            ("dimmer_spento", {"SFE_State_OnOff": "Off", "SFE_State_Brightness": "0"}),
            (
                "dimmer_acceso_1_percento",
                {"SFE_State_OnOff": "On", "SFE_State_Brightness": "1"},
            ),
            (
                "dimmer_acceso_50_percento",
                {"SFE_State_OnOff": "On", "SFE_State_Brightness": "50"},
            ),
            (
                "dimmer_acceso_100_percento",
                {"SFE_State_OnOff": "On", "SFE_State_Brightness": "100"},
            ),
        ],
    ),
    (
        "SS_Light_DimmerRGB",
        "Luci",
        [
            ("dimmer_rgb_spento", {"SFE_State_OnOff": "Off"}),
            (
                "dimmer_rgb_acceso",
                {"SFE_State_OnOff": "On", "SFE_State_Brightness": "80"},
            ),
        ],
    ),
    (
        "SS_Light_PhilipsDimmer",
        "Luci",
        [
            (
                "philips_dimmer_acceso",
                {"SFE_State_OnOff": "On", "SFE_State_Brightness": "70"},
            ),
        ],
    ),
    (
        "SS_Light_PhilipsDynamicDimmer",
        "Luci",
        [
            ("philips_dinamico_acceso", {"SFE_State_OnOff": "On"}),
        ],
    ),
    (
        "SS_Light_PhilipsDynamicDimmerRGB",
        "Luci",
        [
            ("philips_dinamico_rgb_acceso", {"SFE_State_OnOff": "On"}),
        ],
    ),
    # Non nel corpus: ereditano dai mapper sopra, quindi stesso template.
    (
        "SS_Light_PhilipsSwitch",
        "Luci",
        [
            ("philips_interruttore_spento", {"SFE_State_OnOff": "Off"}),
        ],
        "SS_Light_Switch",
    ),
    (
        "SS_Light_PhilipsDimmerRGB",
        "Luci",
        [
            ("philips_dimmer_rgb_acceso", {"SFE_State_OnOff": "On"}),
        ],
        "SS_Light_DimmerRGB",
    ),
    (
        "SS_Light_DynamicDimmer",
        "Luci",
        [
            (
                "dimmer_dinamico_bianco_caldo",
                {"SFE_State_OnOff": "On", "SFE_State_MixingWhiteValue": "30"},
            ),
        ],
        "SS_Light_Dimmer",
    ),
    (
        "SS_Light_ConstantControl",
        "Luci",
        [
            ("luce_costante_attiva", {"SFE_State_OnOff": "On"}),
        ],
        "SS_Light_Switch",
    ),
    # ── Coperture ───────────────────────────────────────────────────────────
    # ATTENZIONE alla scala: nel gateway 100 = CHIUSA e 0 = APERTA, l'opposto
    # della convenzione di Home Assistant. A invertirla e' l'entita'
    # (`cover.py` fa `100 - position`), non il mapper — quindi qui i valori
    # sono quelli veri di Vimar e i nomi descrivono il mondo reale.
    (
        "SS_Shutter_Position",
        "Coperture",
        [
            ("cover_chiusa", {"SFE_State_Shutter": "100"}),
            ("cover_aperta_50_percento", {"SFE_State_Shutter": "50"}),
            ("cover_aperta", {"SFE_State_Shutter": "0"}),
            ("cover_in_movimento", {"SFE_State_Shutter": "Change to 75"}),
        ],
    ),
    (
        "SS_Shutter_WithoutPosition",
        "Coperture",
        [
            ("tapparella_ferma", {"SFE_State_ShutterWithoutPosition": "Stopped"}),
            ("tapparella_in_movimento", {"SFE_State_ShutterWithoutPosition": "Moving"}),
        ],
    ),
    (
        "SS_Shutter_SlatPosition",
        "Coperture",
        [
            # Su un frangisole il registro di POSIZIONE comprende anche la
            # rotazione delle lamelle agli estremi della corsa: gli ultimi
            # punti percentuali sono l'inclinazione, non il movimento. I
            # quattro casi sotto sono stati reali, presi dai database di
            # installazioni con le veneziane (issue #90) e dal corpus:
            #   100/100  giu', lamelle chiuse   <- dove deve arrivare un CLOSE
            #    97/23   giu', lamelle aperte   <- il sintomo della issue
            #     0/0    su,   lamelle aperte
            #     3/100  su,   lamelle chiuse
            ("veneziana_chiusa", {"SFE_State_Shutter": "100", "SFE_State_Slat": "100"}),
            (
                "veneziana_giu_lamelle_aperte",
                {"SFE_State_Shutter": "97", "SFE_State_Slat": "23"},
            ),
            (
                "veneziana_aperta_lamelle_meta",
                {"SFE_State_Shutter": "0", "SFE_State_Slat": "50"},
            ),
            (
                "veneziana_su_lamelle_chiuse",
                {"SFE_State_Shutter": "3", "SFE_State_Slat": "100"},
            ),
        ],
    ),
    (
        "SS_Shutter_SlatWithoutPosition",
        "Coperture",
        [
            ("veneziana_senza_posizione", {}),
        ],
    ),
    (
        "SS_Curtain_Position",
        "Coperture",
        [
            ("tenda_chiusa", {"SFE_State_Shutter": "100"}),
            ("tenda_aperta", {"SFE_State_Shutter": "0"}),
        ],
    ),
    (
        "SS_Curtain_WithoutPosition",
        "Coperture",
        [
            ("tenda_senza_posizione", {"SFE_State_ShutterWithoutPosition": "Stopped"}),
        ],
        "SS_Shutter_WithoutPosition",
    ),
    # ── Clima ───────────────────────────────────────────────────────────────
    # ATTENZIONE al vocabolario: `SFE_State_ChangeOverMode` vuole "Heating"/
    # "Cooling" (vedi ChangeOverMode in vimar_climate.py — NON in
    # vimar_climate_old.py, che nonostante il nome e' ancora vivo ed e'
    # un'altra classe con lo stesso nome). "Heat"/"Cool" (i valori HA, minuscoli
    # e diversi) qui vengono silenziosamente ignorati: get_change_over_mode()
    # non li riconosce, ritorna None, e hvac_modes cade sul ramo finale
    # `[OFF]` — verificato di persona, un test scriveva "Heat" e i mode
    # offerti erano SOLO "off", senza errori a dirlo.
    #
    # `SFE_Cmd_ChangeOverMode` assente e' il caso della issue #85: il gateway
    # non concede il permesso di cambiare caldo/freddo.
    #
    # "clima_caldo" e "clima_freddo" sono i casi COL permesso: scrivono
    # esplicitamente `SFE_Cmd_ChangeOverMode` (valore vuoto, e' un comando non
    # uno stato — solo l'enable conta, vedi permission_granted) cosi' finiscono
    # con enable=1 (la regola generale sugli override, sopra) invece di
    # ereditare l'enable=0 del template — che li avrebbe resi indistinguibili
    # dal caso senza permessi. Portano anche `SFE_State_FanSpeed3V`: senza,
    # ClimateEntityFeature.FAN_MODE non viene esposta e action_set_fan_mode
    # fallisce con "service_not_supported" ancora prima di arrivare al gate.
    #
    # "clima_senza_permessi_cambio_modo" e' costruito apposta per riprodurre
    # la #85 nella sua forma vera: hvac_modes offre GIA' "cool" (perche' lo
    # stato ChangeOverMode e' Cool), eppure il comando va bloccato lo stesso.
    # Se rimuovessimo anche lo stato, il test scambierebbe "cool non e' fra le
    # modalita' offerte" (validazione di HA, ServiceValidationError) per "il
    # gate ha bloccato" (HomeAssistantError, il bug della issue) — due errori
    # diversi che si assomigliano solo nel far fallire la chiamata.
    (
        "SS_Clima_Zone",
        "Clima",
        [
            ("clima_spento", {"SFE_State_OnOffMode": "Off"}),
            (
                "clima_caldo",
                {
                    "SFE_State_OnOffMode": "On",
                    "SFE_State_ChangeOverMode": "Heating",
                    "SFE_Cmd_ChangeOverMode": "",
                    "SFE_State_FanSpeed3V": "V1",
                },
            ),
            (
                "clima_freddo",
                {
                    "SFE_State_OnOffMode": "On",
                    "SFE_State_ChangeOverMode": "Cooling",
                    "SFE_Cmd_ChangeOverMode": "",
                },
            ),
            (
                "clima_senza_permessi_cambio_modo",
                {
                    "SFE_State_OnOffMode": "On",
                    "SFE_State_ChangeOverMode": "Cooling",
                    "SFE_Cmd_ChangeOverMode": None,
                },
            ),
        ],
    ),
    # ── Energia ─────────────────────────────────────────────────────────────
    (
        "SS_Energy_Measure1P",
        "Energia",
        [
            (
                "energia_monofase_carico_stabile",
                {"SFE_State_GlobalActivePowerConsumption": "207"},
            ),
            ("energia_monofase_zero", {"SFE_State_GlobalActivePowerConsumption": "0"}),
        ],
    ),
    ("SS_Energy_Measure3P", "Energia", [("energia_trifase", {})]),
    (
        "SS_Energy_MeasureCounter",
        "Energia",
        [
            ("contatore_impulsi", {"SFE_State_PartialCounter": "1234"}),
        ],
    ),
    ("SS_Energy_Load", "Energia", [("carico_elettrico", {})]),
    ("SS_Energy_LoadControl1P", "Energia", [("controllo_carichi_1f", {})]),
    ("SS_Energy_LoadControl3P", "Energia", [("controllo_carichi_3f", {})]),
    ("SS_Energy_LoadControl1PProduction", "Energia", [("produzione_1f", {})]),
    ("SS_Energy_LoadControl3PProduction", "Energia", [("produzione_3f", {})]),
    # ── Accessi ─────────────────────────────────────────────────────────────
    # "Closed" e "Close" convivono davvero nel corpus: due varianti, non un refuso.
    (
        "SS_Access_Gate",
        "Accessi",
        [
            ("cancello_chiuso", {"SFE_State_OnOff": "Off"}),
            ("cancello_aperto", {"SFE_State_OnOff": "On"}),
        ],
    ),
    (
        "SS_Access_DoorWindow",
        "Accessi",
        [
            ("porta_chiusa", {"SFE_State_OnOff": "Off"}),
            ("porta_aperta", {"SFE_State_OnOff": "On"}),
        ],
    ),
    (
        "SS_Access_InterfaceContact",
        "Accessi",
        [
            ("contatto_chiuso", {"SFE_State_Access": "Closed"}),
            ("contatto_chiuso_dizione_breve", {"SFE_State_Access": "Close"}),
            ("contatto_aperto", {"SFE_State_Access": "Open"}),
        ],
    ),
    # ── Sensori ─────────────────────────────────────────────────────────────
    ("SS_Sensor_Humidity", "Sensori", [("umidita", {"SFE_State_Humidity": "55"})]),
    ("SS_Sensor_InterfaceContact", "Sensori", [("contatto_sensore", {})]),
    ("SS_Sensor_AirQualityGradient", "Sensori", [("gradiente_qualita_aria", {})]),
    ("SS_Sensor_WeatherStation", "Sensori", [("stazione_meteo", {})]),
    # I sensori sotto hanno un mapper ma non compaiono in nessuna installazione
    # del campione: sono il gruppo piu' esposto a regressioni silenziose.
    (
        "SS_Sensor_Temperature",
        "Sensori",
        [("temperatura", {"SFE_State_SensorTemperature": "21.5"})],
    ),
    (
        "SS_Sensor_Luminosity",
        "Sensori",
        [("luminosita", {"SFE_State_Luminosity": "450"})],
    ),
    ("SS_Sensor_Power", "Sensori", [("potenza", {"SFE_State_Power": "1200"})]),
    ("SS_Sensor_Current", "Sensori", [("corrente", {"SFE_State_Current": "5.2"})]),
    ("SS_Sensor_Tension", "Sensori", [("tensione", {"SFE_State_Tension": "230"})]),
    ("SS_Sensor_Pressure", "Sensori", [("pressione", {"SFE_State_Pressure": "1013"})]),
    (
        "SS_Sensor_AirQuality",
        "Sensori",
        [("qualita_aria", {"SFE_State_AirQuality": "42"})],
    ),
    ("SS_Sensor_RainAmount", "Sensori", [("pioggia", {"SFE_State_RainAmount": "12"})]),
    (
        "SS_Sensor_WindSpeed",
        "Sensori",
        [("velocita_vento", {"SFE_State_WindSpeed": "18"})],
    ),
    ("SS_Sensor_VolumeFlow", "Sensori", [("portata", {"SFE_State_VolumeFlow": "3.4"})]),
    (
        "SS_Sensor_Generic",
        "Sensori",
        [("sensore_generico", {"SFE_State_Generic": "7"})],
    ),
    # ── Audio ───────────────────────────────────────────────────────────────
    ("SS_Audio_Zone", "Audio", [("zona_audio", {})]),
    ("SS_Audio_RadioFM", "Audio", [("radio_fm", {})]),
    ("SS_Audio_Bluetooth", "Audio", [("bluetooth", {})]),
    ("SS_Audio_RCA", "Audio", [("ingresso_rca", {})]),
    # ── Scene e attivatori ──────────────────────────────────────────────────
    # `SFE_State_Executed` = "Executed" e' lo stato che in sfdiscovery generava
    # i falsi eventi della issue #83.
    (
        "SS_Scene_Executor",
        "Scene",
        [
            ("scena_a_riposo", {"SFE_State_Executed": "NotExecuted"}),
            ("scena_appena_eseguita", {"SFE_State_Executed": "Executed"}),
        ],
    ),
    ("SS_SceneActivator_Activator", "Scene", [("attivatore_scena", {})]),
    ("SS_SceneActivator_Sai", "Scene", [("attivatore_sai", {})]),
    ("SS_SceneActivator_Videoentry", "Scene", [("attivatore_videocitofono", {})]),
    (
        "SS_SceneActivator_AirQualityGradient",
        "Scene",
        [("attivatore_qualita_aria", {})],
    ),
    (
        "SS_SceneActivator_Saig2",
        "Scene",
        [("attivatore_sai_g2", {})],
        "SS_SceneActivator_Sai",
    ),
    # ── Automazioni ─────────────────────────────────────────────────────────
    (
        "SS_Automation_OnOff",
        "Automazioni",
        [
            ("automazione_spenta", {"SFE_State_OnOff": "Off"}),
            ("automazione_accesa", {"SFE_State_OnOff": "On"}),
        ],
    ),
    (
        "SS_Automation_OutputControl",
        "Automazioni",
        [
            ("controllo_uscita", {"SFE_State_OnOff": "On"}),
        ],
        "SS_Automation_OnOff",
    ),
    ("SS_Automation_TechnicalAlarm", "Automazioni", [("allarme_tecnico", {})]),
    ("SS_Automation_TimerAstronomic", "Automazioni", [("timer_astronomico", {})]),
    ("SS_Automation_TimerPeriodic", "Automazioni", [("timer_periodico", {})]),
    ("SS_Automation_TimerWeekly", "Automazioni", [("timer_settimanale", {})]),
    ("SS_Synoptic", "Automazioni", [("sinottico", {})]),
    # ── Irrigazione ─────────────────────────────────────────────────────────
    ("SS_Irrigation_MultiZones", "Irrigazione", [("irrigazione_multizona", {})]),
]

# ── SsType ancora senza mapper ──────────────────────────────────────────────
# Devono stare nel database proprio perche' NON sono gestiti: il test che li
# usa verifica che il mapping li ignori senza sollevare eccezioni. Sono tutte
# varianti clima di terze parti (split Daikin/LG/Mitsubishi, VRV) piu' i
# sensori clima dedicati.
NON_MAPPATI = [
    ("SS_Clima_Control", "clima_control_non_mappato"),
    ("SS_Clima_Daikin", "clima_daikin_non_mappato"),
    ("SS_Clima_DaikinVRV", "clima_daikin_vrv_non_mappato"),
    ("SS_Clima_Humidity", "clima_umidita_non_mappato"),
    ("SS_Clima_InterfaceContact", "clima_contatto_non_mappato"),
    ("SS_Clima_LG", "clima_lg_non_mappato"),
    ("SS_Clima_Mitsubishi", "clima_mitsubishi_non_mappato"),
    ("SS_Clima_MitsubishiNoFan", "clima_mitsubishi_senza_ventola_non_mappato"),
    ("SS_Clima_Pressure", "clima_pressione_non_mappato"),
    ("SS_Clima_RainAmount", "clima_pioggia_non_mappato"),
    ("SS_Clima_Temperature", "clima_temperatura_non_mappato"),
    ("SS_Clima_WindSpeed", "clima_vento_non_mappato"),
    ("SS_Clima_ZoneVRV", "clima_zona_vrv_non_mappato"),
]

SCHEMA = """
CREATE TABLE ambients (
    id INTEGER PRIMARY KEY AUTOINCREMENT, dictKey INTEGER NOT NULL,
    hash TEXT, idambient INTEGER NOT NULL, idparent INTEGER, name TEXT NOT NULL);
CREATE TABLE components (
    id INTEGER PRIMARY KEY AUTOINCREMENT, idambient INTEGER NOT NULL,
    dictKey INTEGER NOT NULL, idsf INTEGER NOT NULL, name TEXT NOT NULL,
    sftype TEXT NOT NULL, sstype TEXT NOT NULL);
CREATE TABLE elements (
    id INTEGER PRIMARY KEY AUTOINCREMENT, idcomponent INTEGER NOT NULL,
    enable INTEGER, sfetype TEXT NOT NULL, value TEXT, updated TEXT);
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, setup_code TEXT,
    useruid TEXT, password TEXT, plant_name TEXT);
"""

# Un istante fisso: un `updated` che si muove renderebbe il database diverso a
# ogni rigenerazione, e gli snapshot dei test diventerebbero rumore in git.
ISTANTE = "2026-01-01 12:00:00.000000"

# Il gruppo (sftype) NON si deduce dal nome, e questa e' una trappola: le tende
# `SS_Curtain_*` viaggiano sotto `SF_Shutter` e il sinottico sotto `SF_Clima`.
# I dispatcher filtrano per sftype PRIMA di guardare l'sstype, quindi un gruppo
# sbagliato non produce un errore: produce silenzio, e il componente sparisce.
# Le eccezioni qui sotto vengono dai dati reali, non da un'intuizione.
GRUPPO_SPECIALE = {
    "SS_Curtain_Position": "SF_Shutter",
    "SS_Curtain_WithoutPosition": "SF_Shutter",
    "SS_Synoptic": "SF_Clima",
}


def gruppo(sstype: str) -> str:
    if sstype in GRUPPO_SPECIALE:
        return GRUPPO_SPECIALE[sstype]
    return "SF_" + sstype.split("_")[1]


def costruisci() -> None:
    with open(TEMPLATES, encoding="utf-8") as f:
        templates = json.load(f)

    if os.path.exists(USCITA):
        os.remove(USCITA)
    con = sqlite3.connect(USCITA)
    con.executescript(SCHEMA)

    id_ambiente = {nome: i + 1 for i, nome in enumerate(AMBIENTI)}
    for nome, idamb in id_ambiente.items():
        con.execute(
            "INSERT INTO ambients (dictKey, hash, idambient, idparent, name) VALUES (?,?,?,?,?)",
            (idamb, f"hash{idamb:03d}", idamb, 0, nome),
        )

    idsf = 1000
    righe_comp: list[tuple] = []
    righe_elem: list[tuple] = []

    def aggiungi(
        sstype: str, ambiente: str, slug: str, override: dict, tpl_da: str
    ) -> None:
        nonlocal idsf
        idsf += 1
        righe_comp.append(
            (id_ambiente[ambiente], idsf, idsf, slug, gruppo(sstype), sstype)
        )
        base = dict(templates.get(tpl_da, {}))
        for sfe, val in override.items():
            if val is None:
                base.pop(sfe, None)  # elemento assente dal gateway
            else:
                # enable=1 SEMPRE quando un caso d'uso scrive un valore, anche
                # se nel template quell'sfe era enable=0 (e' il caso di
                # SFE_Cmd_ChangeOverMode: nel corpus e' disabilitato piu'
                # spesso che no, e senza questo "clima_caldo" ereditava
                # enable=0 dal template ed era INDISTINGUIBILE dal caso
                # apposta senza permessi — un override e' una dichiarazione
                # d'intento, "questo campo c'e' ed e' attivo", non "eredita
                # quel che capita". L'unico modo di ottenere enable=0 resta
                # rimuovere l'sfe con `None`.
                base[sfe] = {"v": val, "e": 1}
        for sfe, dati in base.items():
            righe_elem.append((idsf, dati["e"], sfe, dati["v"], ISTANTE))

    for voce in CASI:
        sstype, ambiente, casi = voce[0], voce[1], voce[2]
        tpl_da = voce[3] if len(voce) > 3 else sstype
        for slug, override in casi:
            aggiungi(sstype, ambiente, slug, override, tpl_da)

    for sstype, slug in NON_MAPPATI:
        # Nessun template disponibile: un solo stato generico basta a provare
        # che il mapping non esploda su un tipo che non conosce.
        idsf += 1
        righe_comp.append(
            (id_ambiente["Non mappati"], idsf, idsf, slug, gruppo(sstype), sstype)
        )
        righe_elem.append((idsf, 1, "SFE_State_OnOff", "Off", ISTANTE))

    con.executemany(
        "INSERT INTO components (idambient, dictKey, idsf, name, sftype, sstype) VALUES (?,?,?,?,?,?)",
        righe_comp,
    )
    con.executemany(
        "INSERT INTO elements (idcomponent, enable, sfetype, value, updated) VALUES (?,?,?,?,?)",
        righe_elem,
    )
    con.commit()

    n_ss = len({r[5] for r in righe_comp})
    print(f"scritto {os.path.relpath(USCITA, os.path.dirname(QUI))}")
    print(f"  ambienti:   {len(AMBIENTI)}")
    print(f"  componenti: {len(righe_comp)}  (casi d'uso)")
    print(f"  elementi:   {len(righe_elem)}")
    print(f"  SsType:     {n_ss}")
    print("  utenti:     0  (tabella vuota: nessun dato personale)")
    con.close()


if __name__ == "__main__":
    costruisci()
