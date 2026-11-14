---
tags: [projekt, website]
status: aktiv
---

# Kontrollpanel (Zentrale, Arbeitsname La Maison) · Hotel Monte-Moro, Saas-Almagell · Lieferung 08.11.2026

Agent `mm-maison`. Nichts online, nichts verschickt. Reviere: `_werkzeuge/maison/` und (einziger Schreiber) `_werkzeuge/oberflaeche/`.

**Adressen** (nur lokal)
- Kontrollpanel: http://127.0.0.1:9381/_werkzeuge/maison/ (Prüfserver `python3 server.py 9381` im Ordner `_werkzeuge/maison`)
- Rundgang: http://127.0.0.1:9381/_werkzeuge/maison/?rundgang
- Gemeinsames Kleid, Musterseite: http://127.0.0.1:9381/assets/oberflaeche/muster.html?haus=montemoro · Anleitung `_werkzeuge/oberflaeche/UMSTELLUNG.md`

## Was steht

1. **Gemeinsames Kleid** `_werkzeuge/oberflaeche/` (alle sieben Werkzeuge): Knöpfe wie `.kn` der Website (Pille, Lichtkante, Knauf; Hauptweg Lärche mit weissem Knauf, Nebenweg Nacht, hell mit blauem Knauf), Etiketten DM Mono gesperrt, Titelbetonung Lärche, Grat-Oberkante an Startbild- und Kachelfotos, Bergkamm oben links in einer Pille aus Nacht (76 × 36, Bergkamm 54 px, `zeichenMass` 5.004), Startbild-Foto mit srcset aus `/assets/img/<schlüssel>-<s|m|l|x>.webp` (keine 404). Musterseite fehlerfrei bei 1440 und 390. Alle Änderungen in `UMSTELLUNG.md` (Eintrag 08.11.2026).
2. **Kopie der abgenommenen Zentrale** (Stamm): gleicher Aufbau, gleiche Wege, gleiche Funktionen (Insel-Leiste, Empfang mit fünf Fenstern, Zahlenzeile Besucher, Laufband, je Werkzeug ein Saal mit echten Bildschirmen und der Tafel «So geht’s», Weg zur Buchung, Fuss mit allen Anleitungen, Rundgang, Startfehler-Tür, «Zur Werkbank», Online-Fassung).
3. **Kleid des Hauses** in `quelle/maison.css`: Nacht/Nachtblau/Tiefnacht, Papier und Creme, Lärche nur als Akzent, Messing nur für feine Linien; Fjalla One, Instrument Sans, DM Mono (aus `website/assets/fonts/`); Logo «Monte Moro / Saas-Almagell» in Papier auf Nacht (Empfang) und in Logo-Blau (Fuss); Bergkamm in Lärche (Ecke, Säle, Weg).
4. **Inhalt des Hauses**: Name, Ort, PLZ, Telefon, Satz des Hauses aus `website/inhalt/daten.py` (`HAUS`, `RESTAURANT`), Fotos nur aus `website/inhalt/bilder.py`; keine Strasse (steht in `OFFEN`). Sätze, Tafeln (`tafeln.json`, Knopf-Namen gegen den Code geprüft) und Rundgang für das Hotel, in Sie-Form und Schweizer Schreibung. Der Bau bricht ab bei Namen anderer Häuser, Wörtern der Bar, Du-Form oder «ß» in der Seite.
5. **Stücke der Säle**: drei Karten aus Karten & Preislisten (PDF bzw. gesetztes Blatt: Röstihüs-Karte, Wein und Apéro, Preisliste), sechs Fotos des Hauses im Saal des Markenbuchs, Hausfarben aus `livre/livre.json`. Drucksachen Drucksachen & Feed nur, wenn sie als Stück des Hauses vorliegen (`stuecke.py`, Liste `DRUCK`).
6. **Alle Aufnahmen in einem Befehl:** `bash "Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/maison/_bau/aufnahmen.sh"` (Stücke → `roh/karten`, `roh/druck`; Bildschirme der sechs Werkzeuge 9382–9387 → `roh/*.png`, Chromium 1440 × 932 @2x, Uhr fest auf 08.11.2026 10:30 Zürich, nur GET; dann `bau.py`). Einzelnes Werkzeug: `… aufnahmen.sh reception`.

## Wie geprüft (08.11.2026, 10:42, nach der letzten Aufnahme)

- `node _Werkzeuge/oberflaeche_pruefen.js http://127.0.0.1:9381/_werkzeuge/maison/` → **BESTANDEN** (vorher 4 Funde: lose Zahlen im Saal Karten & Preislisten → in die Tafel geholt; Laufband 9 px neben der Mitte, weil der nächste Saal 18 px darüber liegt → Band unten um den Überstand höher).
- `tor-schnell.js … --nur hotelbuero --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390` → 4 Zustände (Start, Rundgang, Überspringen, Weiter), **0 Funde** in allen vier Breiten, nichts «nicht erreicht». Vorher Fund «oval» an der Pille oben links (64 × 44) → Pille 76 × 36.
- `messlauf.js … --nur hotelbuero --browser chromium --groesse 1440,390` → **0 Funde**. Vorher «oval» an derselben Pille: die Regel `messen.js` (Knauf in einem Link ohne Text mit svg muss kreisrund sein) hält eine Pille mit breitem Zeichen für einen ovalen Knauf. Gelöst wie im Kleid: der Bergkamm steht als Bild (`img/zeichen.svg`) in der Pille, nicht als eigenes svg. Hinweis an den Oberchef: die Regel kennt keine Pillen mit Bildmarke (Beleg `aus/mess-hotelbuero/funde.json` vor der Änderung, Pille 76 × 36, Radius 999px).
- Musterseite des Kleids: ohne Konsolenfehler, ohne 404, ohne Überlauf bei 1440 und 390.
- Mit den Augen: Empfang 1440/1280/1000/390, alle sechs Säle bei 1440, Handy ganz, Rundgang Schritt 1 und 2 in vier Breiten, alle zehn Bildschirme und die drei Karten (über 20 Bilder). Kein Wild-Side-Rest in der Seite Kontrollpanel; `grep` im Revier: Treffer nur in Prüflisten (`bau.py ohne_fremde`, `stuecke.py FREMD`), `sessionStorage`/`text-size-adjust` (Wortteile), Herkunftsangabe im Kopf von `bau.py`.

## Offen

- **Bildschirme Drucksachen & Feed und der Rezeption** zeigen noch den Stand dieser Werkzeuge von heute 10:40 (dort stehen noch Anlässe und Chat der Bar, z. B. «Valentinstag», «Wild Side · Fragen an die Bar»). Sobald beide fertig sind: `bash "Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/maison/_bau/aufnahmen.sh"`, danach `tor-schnell … --nur hotelbuero` und `oberflaeche_pruefen.js`.
- **Drucksachen im Saal Drucksachen & Feed**: noch keine (ihre Liste `drucksachen/liste.json` enthält heute nur Stücke der Bar, die bewusst weggelassen sind). `stuecke.py` nimmt die Schlüssel aus `DRUCK` (`roestihues-karte`, `racletteabend`, `willkommensbrief`, `aushang-inklusive`, `kidsclub`, `tischkarte-hotelwein`, `briefpapier`); heissen die fertigen Stücke anders, dort eintragen.
- **Tafeln «So geht’s»** (`tafeln.json`): Knopf-Namen gegen den heutigen Code geprüft; ändert ein Werkzeug einen Knopf, meldet `bau.py` «Knopf-Namen nicht im Code gefunden».
- Stufen «Weg zur Buchung» im Saal Besucher: bis Besucher `registre/stufen.json` liefert, gelten «Zimmer» oder «Preise» geöffnet → Buchen oder Anfrage geöffnet → im Haus.
