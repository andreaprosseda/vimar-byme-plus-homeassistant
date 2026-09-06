# Suite di test

## Avviarli in locale

```bash
tests/run.sh
```

La prima volta crea un ambiente virtuale in `.venv/`, installa le dipendenze
di `requirements-test.txt`, rigenera `tests/fixtures/master.db` (e avvisa se
il file committato non corrisponde piu' al generatore) e fa girare pytest.
Le volte dopo riusa lo stesso `.venv/` — solo un giro di `pip install` in
piu', innocuo.

Passa argomenti a pytest cosi' come sono:

```bash
tests/run.sh -k mapping        # solo i nomi che contengono "mapping"
tests/run.sh tests/test_setup.py -v
tests/run.sh --durations=5
```

Senza lo script, a mano:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-test.txt
python3 -m pytest tests/
```

## Cosa c'e' dentro

| File | Cosa verifica | Quanto e' pesante |
|---|---|---|
| `test_mapping.py` | Ogni caso d'uso del `master.db` produce l'entita' giusta, con i campi giusti — tutto a livello di modello (`VimarCover`, `VimarClimate`, ...), senza Home Assistant. Direzione: gateway → HA. | ~0.1s: nessuna dipendenza da HA. |
| `test_setup.py` | La config entry carica DAVVERO, con tutte e otto le piattaforme, sul `master.db` — usando il codice vero di `custom_components/vimar_byme_plus` dentro un'istanza reale (ma isolata) di Home Assistant. | Qui e in giu' si paga l'avvio di HA (~35 test, ~1.3s in tutto). |
| `test_actions.py` | Quando HA COMANDA qualcosa (`climate.set_temperature`, `cover.set_cover_position`, `light.turn_on`, ...) il gateway riceve l'`ActionType` e gli argomenti giusti. Direzione: HA → gateway — l'opposto di `test_mapping.py`, e fino a questo file **zero** dei 45 metodi `set_*`/`turn_on`/`press` del progetto avevano un solo assert sopra. |  |
| `test_action_handlers.py` | Il pezzo DOPO `test_actions.py`: quale `SFE_Cmd_*` e con quale valore finisce nel messaggio `doaction`. Il banco di prova intercetta la chiamata prima degli action handler, quindi senza questo file quel livello non era coperto da niente. | ~0.1s: nessuna dipendenza da HA. |
| `test_energy.py` | Il contatore kWh derivato dalla potenza: che riparta, che non conti tempo a vuoto, e che una sola ancora inservibile non lo congeli per tutta la sessione. | Avvio di HA + orologio finto. |
| `test_snapshot.py` | Un unico snapshot con OGNI attributo di TUTTE le 134 entita' (registro + stato live). Chiude la copertura sui domini senza contratti mirati (Switch, BinarySensor, MediaPlayer, Button) per via strutturale, non campo per campo. |  |

`test_mapping.py` e' la rete piu' larga sui DATI (verifica ogni SsType
dell'enum, uno per uno) ed e' la piu' veloce — quella da tenere sott'occhio
mentre si scrive un mapper. `test_setup.py` e' quella che avrebbe fermato il
guasto della 3.2.0 esattamente come l'ha visto un utente: non "una funzione
ha sollevato un'eccezione", ma "l'integrazione e' rimasta in setup_retry".
`test_actions.py` e' quella che avrebbe preso le issue #87 e #85 (entrambe
bug nel percorso di invio, non di lettura) — verificato riproducendole di
proposito e vedendo il test rosso. `test_snapshot.py` e' la rete piu' ampia
in assoluto, e la piu' economica da scrivere: una manciata di righe copre
attributi che nessun contratto a mano coprirebbe mai tutti.

### Le tre issue che questa suite copre

Ogni correzione e' stata verificata rimettendo il bug e guardando quali test
diventavano rossi — non solo controllando che diventassero verdi:

| Issue | Test che diventano rossi senza la correzione |
|---|---|
| #85 clima bloccato senza il grant | `test_actions.py::test_clima_senza_permessi_si_puo_spegnere`, `..._si_puo_riaccendere` |
| #79 contatori di energia fermi | `test_energy.py`, 3 test su 4 (il quarto e' il controllo: a zero non si accumula) |
| #90 lamelle dei frangisole | `test_action_handlers.py::test_frangisole_*` |

### Aggiornare lo snapshot

Un cambiamento voluto (nuovo mapper, campo in piu', nome diverso) fa fallire
`test_snapshot.py` finche' non lo si rigenera:

```bash
tests/run.sh tests/test_snapshot.py --snapshot-update
```

Rivedi il diff in `tests/snapshots/test_snapshot.ambr` (testo semplice, si
legge in un editor qualsiasi) prima di committarlo — e' li' che si vede a
colpo d'occhio SE il cambiamento era davvero quello voluto o un effetto
collaterale non cercato.

## `tests/fixtures/master.db`

Un solo `home.db` sintetico in cui ogni componente e' un caso d'uso, con un
nome che lo dice (`luce_spenta`, `cover_aperta_50_percento`,
`clima_senza_permessi_cambio_modo`...). Copre tutti i 73 `SsType`
dell'enum, piu' `SS_Synoptic` (presente in installazioni reali ma non
nell'enum).

Anonimo per costruzione, non per ripulitura: `build_master_db.py` non legge
nessun database vero, parte da `fixtures/element_templates.json` (solo la
FORMA dei componenti, senza dati identificabili) e ricostruisce tutto da
zero. Tabella `users` vuota, ambienti generici.

Per rigenerarlo dopo aver aggiunto o modificato un caso d'uso:

```bash
python3 tests/build_master_db.py
```

Il file e' deterministico (stesso `.venv`, stesso Python → stesso md5): la
CI lo rigenera e confronta con quello committato, quindi un `master.db`
disallineato dal generatore fa fallire la pipeline prima ancora di arrivare
a pytest.

## Aggiungere un caso d'uso

1. In `build_master_db.py`, aggiungi una tupla `(slug, {sfetype: valore})`
   alla lista `CASI` del `SsType` giusto (o una nuova voce, se il tipo non
   c'e' ancora).
2. `python3 tests/build_master_db.py`
3. Se serve un contratto specifico (non solo "non deve sparire"), aggiungilo
   in `test_mapping.py` — guarda `_unica()` per il pattern.
4. `tests/run.sh`

## Un mapper nuovo per un `SsType` che oggi non e' implementato

`SsType` gia' ha una voce nel `master.db` (sezione "Non mappati" del
generatore): non serve aggiungere la fixture. Togli quel `SsType` dalla
lista `NON_MAPPATI` in cima a `test_mapping.py` — se il mapper funziona,
`test_i_non_mappati_non_producono_entita` te lo confermerebbe fallendo (nel
modo giusto: "questo e' mappato ma è ancora nella lista dei non mappati").
