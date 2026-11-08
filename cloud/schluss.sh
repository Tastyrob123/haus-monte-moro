#!/usr/bin/env bash
# Schlussprüfung in der Sitzung (Oberchef 08.11.2026): jedes Ziel der Zielliste frisch mit tor-schnell (1440/1280/1000/390, Chromium),
# danach oberflaeche_pruefen.js über jede Oberfläche. Ergebnis: aus-ende/<k>/, aus-ende/oberflaeche/, aus-ende/ende.json
set -uo pipefail
cd "$(dirname "$0")/.."
H="$(python3 -c "import json;print(json.load(open('cloud/haus.json'))['tor_ziele'])")"
A=aus-ende; mkdir -p "$A/oberflaeche"
KS=$(python3 -c "import json;print(' '.join(z['k'] for z in json.load(open('$H'))['ziele']))")
for k in $KS; do
  t0=$(date +%s)
  timeout 40m node _Werkzeuge/abnahme-tor/tor-schnell.js "$H" "$A" --nur "$k" --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390 > "$A/$k.log" 2>&1
  echo "$k ende $? $(( $(date +%s) - t0 ))s $(tail -1 "$A/$k.log" | cut -c1-120)"
done
python3 -c "import json;print('\n'.join(z['url'] for z in json.load(open('$H'))['ziele'] if not z['k'].endswith('-anleitung') and z['k'] not in ('markenbuch-buch','hausdruckerei-mail')))" | while read -r u; do
  r=$(timeout 300 node _Werkzeuge/oberflaeche_pruefen.js "$u" 2>&1 | tee "$A/oberflaeche/$(echo "$u" | sed 's#[^A-Za-z0-9]#_#g').txt" | tail -1)
  echo "oberflaeche $u $r"
done
