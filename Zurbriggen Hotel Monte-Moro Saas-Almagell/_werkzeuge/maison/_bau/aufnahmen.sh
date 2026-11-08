#!/usr/bin/env bash
# Alle Aufnahmen des Hotelbüros in einem Befehl neu (mm-maison 08.11.2026):
#   1. Stücke der Säle aus Kartenbrett (9383) und Hausdruckerei (Revier imprimerie)   → roh/karten, roh/druck
#   2. Bildschirme der sechs Werkzeuge (9382–9387), Chromium 1440 × 932 @2x, feste Uhr  → roh/*.png
#   3. Bau beider Fassungen (index.html und online/)
# Aufruf aus beliebigem Ordner:  bash "Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/maison/_bau/aufnahmen.sh" [werkzeug …]
# Die Server müssen laufen (bash cloud/server.sh). Nur lesend: jede Anfrage ausser GET/HEAD wird in der Aufnahme abgewiesen.
set -euo pipefail
MAISON="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MAISON"
python3 stuecke.py
node schirme.js "$@"
python3 bau.py
