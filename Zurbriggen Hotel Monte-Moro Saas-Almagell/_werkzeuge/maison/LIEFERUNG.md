---
tags: [projekt, website]
status: aktiv
---

# Das Hotelbüro (Zentrale, Arbeitsname La Maison) · Hotel Monte-Moro, Saas-Almagell · Lieferung 08.11.2026

Agent `mm-maison`. Nichts online, nichts verschickt. Reviere: `_werkzeuge/maison/` und (einziger Schreiber) `_werkzeuge/oberflaeche/`.

**Adressen** (nur lokal)
- Das Hotelbüro: http://127.0.0.1:9381/_werkzeuge/maison/ (Prüfserver `python3 server.py 9381` im Ordner `_werkzeuge/maison`)
- Rundgang: http://127.0.0.1:9381/_werkzeuge/maison/?rundgang
- Gemeinsames Kleid, Musterseite: http://127.0.0.1:9381/assets/oberflaeche/muster.html?haus=montemoro · Anleitung `_werkzeuge/oberflaeche/UMSTELLUNG.md`

## Was steht

1. **Gemeinsames Kleid** `_werkzeuge/oberflaeche/` (alle sieben Werkzeuge): Knöpfe wie `.kn` der Website (Pille, Lichtkante, Knauf; Hauptweg Lärche mit weissem Knauf, Nebenweg Nacht, hell mit blauem Knauf), Etiketten DM Mono gesperrt, Titelbetonung Lärche, Grat-Oberkante an Startbild- und Kachelfotos, Bergkamm oben links in einer Pille aus Nacht (76 × 36, Bergkamm 54 px, `zeichenMass` 5.004), Startbild-Foto mit srcset aus `/assets/img/<schlüssel>-<s|m|l|x>.webp` (keine 404). Musterseite fehlerfrei bei 1440 und 390. Alle Änderungen in `UMSTELLUNG.md` (Eintrag 08.11.2026).
2. **Kopie der abgenommenen Zentrale** (Stamm): gleicher Aufbau, gleiche Wege, gleiche Funktionen (Insel-Leiste, Empfang mit fünf Fenstern, Zahlenzeile der Besucherliste, Laufband, je Werkzeug ein Saal mit echten Bildschirmen und der Tafel «So geht’s», Weg zur Buchung, Fuss mit allen Anleitungen, Rundgang, Startfehler-Tür, «Zur Werkbank», Online-Fassung).
3. **Kleid des Hauses** in `quelle/maison.css`: Nacht/Nachtblau/Tiefnacht, Papier und Creme, Lärche nur als Akzent, Messing nur für feine Linien; Fjalla One, Instrument Sans, DM Mono (aus `website/assets/fonts/`); Logo «Monte Moro / Saas-Almagell» in Papier auf Nacht (Empfang) und in Logo-Blau (Fuss); Bergkamm in Lärche (Ecke, Säle, Weg).
4. **Inhalt des Hauses**: Name, Ort, PLZ, Telefon, Satz des Hauses aus `website/inhalt/daten.py` (`HAUS`, `RESTAURANT`), Fotos nur aus `website/inhalt/bilder.py`; keine Strasse (steht in `OFFEN`). Sätze, Tafeln (`tafeln.json`, Knopf-Namen gegen den Code geprüft) und Rundgang für das Hotel, in Sie-Form und Schweizer Schreibung. Der Bau bricht ab bei Namen anderer Häuser, Wörtern der Bar, Du-Form oder «ß» in der Seite.
5. **Stücke der Säle**: drei Karten aus dem Kartenbrett (PDF bzw. gesetztes Blatt: Röstihüs-Karte, Wein und Apéro, Preisliste), sechs Fotos des Hauses im Saal des Markenbuchs, Hausfarben aus `livre/livre.json`. Drucksachen der Hausdruckerei nur, wenn sie als Stück des Hauses vorliegen (`stuecke.py`, Liste `DRUCK`).
6. **Alle Aufnahmen in einem Befehl:** `bash "Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/maison/_bau/aufnahmen.sh"` (Stücke → `roh/karten`, `roh/druck`; Bildschirme der sechs Werkzeuge 9382–9387 → `roh/*.png`, Chromium 1440 × 932 @2x, Uhr fest auf 08.11.2026 10:30 Zürich, nur GET; dann `bau.py`). Einzelnes Werkzeug: `… aufnahmen.sh reception`.

## Wie geprüft

Siehe Abschnitt «Prüfstand» unten (wird mit dem letzten Lauf nachgeführt).
