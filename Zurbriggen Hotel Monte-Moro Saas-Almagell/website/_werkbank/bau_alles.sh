#!/bin/bash
# Werkbank Hotel Monte-Moro: das ganze Paket bauen (Werkbank Kern, 08.11.2026; Aufbau aus dem Stamm).
#   bash website/_werkbank/bau_alles.sh [--ohne-aufnahmen]
# Revier: website/_werkbank/ ist der Projektordner des Kits; die Website liegt eine Ebene höher und wird nur gelesen (assets ist ein Verweis).
# Voraussetzung: Vorschau-Server läuft:  python3 website/_werkbank/serve.py 9388, Werkzeug-Server 9381–9387 (cloud/server.sh). Kit unverändert, headless, nichts geht online.
# Teile: Kern (Startseite, Befund, KI, Karte, Geprüft), Papier (papier_alles.sh, Werkbank Papier).
set -e
K="${WERKBANK_KIT:-$(cd "$(dirname "$0")/../../.." && pwd)/_Werkbank-Kit}"
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"
export PYTHONPATH="$K:$P/_werkbank" WB_PORT=9388
python3 "$K/kern.py" "$P" | grep -v "Schrift fehlt" || true            # Plan und Gestaltung (werkbank.css, seiten.css, werkbank.js)
python3 "$K/schriften.py" "$P" > /dev/null || true
if [ "$1" != "--ohne-aufnahmen" ]; then
  timeout 900 node _werkbank/ansicht_lang.js "$P"                    # jede Seite der Website am Rechner und am Handy
  timeout 900 node _werkbank/sb_ideen.js                             # Ideen und Gäste-Funktionen
  timeout 900 node _werkbank/sb_werkzeuge.js                         # Bildschirme der sieben Werkzeuge (Adressen aus _werkbank/werkzeuge.json)
fi
python3 _werkbank/sb_heute.py                                        # heute (Aufnahme der Analyse) und neu
# ---------- Papier, Unterlagen, Sticker, Beigaben, Postkarten, Feed, Mails, Dateien (Werkbank Papier) ----------
timeout 900 bash _werkbank/papier_alles.sh
node "$K/ziele.js" "$P" || true
timeout 300 node _werkbank/geraete/schirme.js feed || true          # Bildschirm des Feeds für die Feed-Bühne der Startseite
# ---------- Kern: Startseite, Befund, KI, Karte «Ein Vorschlag.», Geprüft ----------
node _werkbank/sb_strom.js || true                                   # Befund, Prüfbericht, Karte, Markenbuch für die Objekte
python3 _werkbank/objekte_bau.py "$P"
python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"                    # die Werkbank (ruft haus.nach_bau: Kapitel, Befund, KI-Seite, Kleid)
node _werkbank/sb_strom.js || true
python3 _werkbank/objekte_bau.py "$P"
python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"
python3 "$K/ruecksprung.py" "$P"                                      # zuletzt: Rücksprung des Kits (Fassung mit Merkpunkt, wie geprüft) in jede Seite
echo "fertig: http://127.0.0.1:9388/werkbank/"
