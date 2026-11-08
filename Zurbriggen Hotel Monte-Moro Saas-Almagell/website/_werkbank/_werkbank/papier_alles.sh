#!/bin/bash
# Werkbank Monte-Moro, Teil Papier (Werkbank Papier, 08.11.2026): Unterlagen, Drucksachen, Untersetzer, Sticker, Beigaben, Postkarten, Feed, Mails, Material.
#   bash website/_werkbank/_werkbank/papier_alles.sh          (rund 4 Minuten; einzeln laufen lassen oder aus bau_alles.sh)
# Voraussetzung: Vorschau-Server 9388 (serve.py) läuft, für die Unterlagen das Kartenbrett auf 9383; Playwright unter
# ~/Desktop/Apps & Tools/Tasty Website Builder/node_modules (Verweis auf /Users/robertreff/Aussen-Pruefung/node_modules), opencv für feed_bestand.
# Jeder Python-Schritt läuft über mit_papier.py: haus.py (Kern) + Texte der Papier-Seiten aus papier_haus.json.
set -e
P="$(cd "$(dirname "$0")/.." && pwd)"; cd "$P"
K="${WERKBANK_KIT:-$(cd "$P/../../.." && pwd)/_Werkbank-Kit}"
export PYTHONPATH="$K:$P/_werkbank" WB_PORT=9388
M="python3 _werkbank/mit_papier.py"
timeout 300 python3 _werkbank/druckschrift.py > /dev/null                      # feste Druckschnitte Fjalla One, Instrument Sans, DM Mono
# ---------- Drucksachen und Untersetzer
rm -rf drucksachen/img untersetzer/img                                       # vor papier.py: es legt die Bilder der Hausdruckerei schon hinein
timeout 300 $M _werkbank/papier.py "$P"
rm -rf _werkbank/roh/papier _werkbank/roh/einzel
timeout 900 node "$K/papier_druck.js" "$P" > /dev/null
timeout 300 $M "$K/papier_seiten.py" "$P" | grep -v "Schrift fehlt" || true
# ---------- Unterlagen (Karten des Röstihüs aus dem Kartenbrett neben der heutigen Speisekarte)
timeout 600 python3 _werkbank/sb_karten.py
timeout 600 $M _werkbank/sb_karten.py "$P" --seite | grep -v "Schrift fehlt" || true
# ---------- Sticker, Beigaben, Postkarten
timeout 120 $M _werkbank/sticker.py "$P"
timeout 120 $M _werkbank/beigaben.py "$P"
rm -rf _werkbank/roh/einzel-sticker _werkbank/roh/sticker _werkbank/roh/beigaben
timeout 900 node _werkbank/sticker_druck.js "$P" > /dev/null
timeout 300 $M _werkbank/sticker.py "$P" --seite
timeout 300 $M _werkbank/beigaben.py "$P" --seite
timeout 120 $M _werkbank/postkarten.py "$P"
rm -rf _werkbank/roh/postkarten _werkbank/roh/einzel-postkarten
timeout 900 node _werkbank/postkarten_druck.js "$P" > /dev/null
timeout 300 $M _werkbank/postkarten.py "$P" --seite
# ---------- Feed
timeout 300 $M "$K/feed.py" "$P"; timeout 300 node "$K/feed_druck.js" "$P"; timeout 300 $M "$K/feed.py" "$P"; timeout 300 node "$K/feed_druck.js" "$P" --handy
timeout 120 python3 _werkbank/feed_leicht.py
# ---------- Mails
timeout 120 python3 mails/_src/bau.py; timeout 300 node mails/_src/aufnahme.js
# ---------- Material (zuletzt: sammelt alles ein), dann die Nachbauten über alle Papier-Seiten
timeout 120 node _werkbank/zeichen_bild.js                                      # Bilder der Zeichen für die Liste im Material
timeout 300 $M _werkbank/material_mehr.py "$P"
timeout 120 python3 _werkbank/papier_nach.py
echo "Papier fertig: http://127.0.0.1:9388/drucksachen/index.html"
