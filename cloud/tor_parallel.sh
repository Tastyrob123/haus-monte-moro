#!/usr/bin/env bash
# Tor-schnell über ausgewählte Ziele, mehrere gleichzeitig (Nachtsitzung 09.11.2026). Aufruf: cloud/tor_parallel.sh <aus> <parallel> <k> [k …]
# Je Ziel: <aus>/<k>/ und <aus>/<k>.log; Zeile «<k> ende <rc>» in <aus>/parallel.log.
set -uo pipefail
cd "$(dirname "$0")/.."
A="$1"; P="$2"; shift 2; mkdir -p "$A"
H="$(python3 -c "import json;print(json.load(open('cloud/haus.json'))['tor_ziele'])")"
export A H
printf '%s\n' "$@" | xargs -P "$P" -I{} bash -c 'timeout 50m node _Werkzeuge/abnahme-tor/tor-schnell.js "$H" "$A" --nur {} --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390 > "$A/{}.log" 2>&1; echo "{} ende $? $(tail -1 "$A/{}.log" | cut -c1-100)" >> "$A/parallel.log"'
echo "alle ende" >> "$A/parallel.log"
