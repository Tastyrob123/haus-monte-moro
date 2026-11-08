#!/usr/bin/env bash
# Teil der Schlussprüfung: nur die genannten Ziele (tor-schnell) bzw. «oberflaeche» für die Oberflächenprüfung.  bash cloud/schluss_teil.sh k1 k2 … | oberflaeche
set -uo pipefail
cd "$(dirname "$0")/.."
H="$(python3 -c "import json;print(json.load(open('cloud/haus.json'))['tor_ziele'])")"
A=aus-ende; mkdir -p "$A/oberflaeche"
if [ "${1:-}" = oberflaeche ]; then
  python3 -c "import json;print('\n'.join(z['url'] for z in json.load(open('$H'))['ziele'] if not z['k'].endswith('-anleitung') and z['k'] not in ('markenbuch-buch','hausdruckerei-mail')))" | while read -r u; do
    r=$(timeout 300 node _Werkzeuge/oberflaeche_pruefen.js "$u" 2>&1 | tee "$A/oberflaeche/$(echo "$u" | sed 's#[^A-Za-z0-9]#_#g').txt" | tail -1)
    echo "oberflaeche $u $r"
  done; exit 0
fi
for k in "$@"; do
  t0=$(date +%s)
  timeout 40m node _Werkzeuge/abnahme-tor/tor-schnell.js "$H" "$A" --nur "$k" --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390 > "$A/$k.log" 2>&1
  echo "$k ende $? $(( $(date +%s) - t0 ))s $(tail -1 "$A/$k.log" | cut -c1-120)"
done
