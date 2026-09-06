#!/usr/bin/env bash
# Lancia la suite in locale, allo stesso modo in cui gira in CI: ambiente
# isolato (.venv, mai il Python di sistema), dipendenze installate, master.db
# rigenerato e confrontato con quello committato prima di far girare pytest.
#
# Uso:
#   tests/run.sh              # tutta la suite
#   tests/run.sh -k mapping   # solo i test il cui nome contiene "mapping"
#   tests/run.sh tests/test_setup.py   # solo un file
#
# Qualunque argomento passato viene inoltrato a pytest cosi' com'e'.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

VENV=".venv"
if [ ! -d "$VENV" ]; then
  echo "== creo l'ambiente virtuale ($VENV) =="
  python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"

echo "== installo le dipendenze di test =="
pip install -q -r requirements-test.txt

echo "== rigenero il master.db e verifico che sia allineato al generatore =="
python3 tests/build_master_db.py
if ! git diff --quiet -- tests/fixtures/master.db 2>/dev/null; then
  echo
  echo "ATTENZIONE: tests/fixtures/master.db e' cambiato rispetto a quello"
  echo "committato. Se hai appena toccato tests/build_master_db.py e' atteso:"
  echo "rivedi il diff e committa il nuovo master.db insieme al generatore."
  echo
fi

echo "== eseguo la suite =="
python3 -m pytest tests/ "$@"
