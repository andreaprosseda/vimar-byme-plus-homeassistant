#!/usr/bin/env bash
# Lancia la suite in locale, come in CI: ambiente isolato, dipendenze
# installate, master.db rigenerato, poi pytest.
#
# Serve Python 3.14: lo stack di test (pytest-homeassistant-custom-component
# all'ultima versione + la homeassistant che porta con se') lo richiede. Se
# `python3` non e' gia' 3.14, indica un interprete con la variabile PYTHON:
#   PYTHON=python3.14 tests/run.sh
#   PYTHON="$(uv python find 3.14)" tests/run.sh   # se usi uv
#
# Uso:
#   tests/run.sh              # tutta la suite
#   tests/run.sh -k mapping   # solo i test il cui nome contiene "mapping"
#   tests/run.sh tests/test_setup.py   # solo un file
#
# Qualunque argomento passato viene inoltrato a pytest cosi' com'e'.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

PYTHON="${PYTHON:-python3}"
VENV=".venv"
if [ ! -d "$VENV" ]; then
  echo "== creo l'ambiente virtuale ($VENV) con $PYTHON =="
  "$PYTHON" -m venv "$VENV"
fi
source "$VENV/bin/activate"

echo "== installo le dipendenze di test =="
pip install -q -r requirements-test.txt

# Il master.db si rigenera sempre, ma NON se ne confrontano i byte con quello
# committato: il formato binario del file dipende dalla versione di SQLite del
# Python in uso, quindi un diff darebbe falsi allarmi. La deriva vera (il
# generatore cambiato senza rigenerare gli snapshot) la coglie test_snapshot.py.
echo "== rigenero il master.db =="
python3 tests/build_master_db.py

echo "== eseguo la suite =="
python3 -m pytest tests/ "$@"
