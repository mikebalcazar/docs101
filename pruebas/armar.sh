#!/usr/bin/env bash
# Comprueba que el sitio se arma y que cada página quedó envuelta con la barra.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 armar.py --probar
python3 armar.py
n=$(ls paginas/*.html | wc -l)
c=$(grep -c '<a class="tarjeta"' dist/index.html)
[ "$c" = "$n" ] || { echo "FALLA: la portada tiene $c tarjetas y hay $n páginas"; exit 1; }
for f in dist/*/index.html; do
  grep -q 'class="d101-barra"' "$f" || { echo "FALLA: $f sin barra"; exit 1; }
  grep -q '<!doctype html>' "$f" || { echo "FALLA: $f sin doctype"; exit 1; }
done
echo "ok: $n páginas armadas y envueltas"
