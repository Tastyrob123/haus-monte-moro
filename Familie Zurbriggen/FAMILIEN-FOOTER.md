---
tags: [projekt, website]
status: aktiv
---
# Familien-Footer: gleiches Wiedererkennungszeichen auf allen drei Häusern

Robert, 18.10.2026: «wir bauen ja quasi drei Häuser einer Familie. Das bedeutet, dass wir die Wiedererkennungswerte auf jeden Fall im Footer haben sollten.»

Jeder Footer hat oben den Teil des eigenen Hauses (frei gestaltet, im Kleid des Hauses). Darunter folgt, auf allen drei Seiten gleich, das **Familienband**:

1. **Schrift:** Tenor Sans, die Schrift der Familienseite zurbriggen.ch (lokal :8961, `einstieg/site/`). Für Texte im Band keine andere Schrift.
2. **Zeichen:** der Pinselstrich der Familienseite (`einstieg/site/zeichen/pinsel-*.svg`), daneben «Familie Zurbriggen · seit 1967», verlinkt auf die Familienseite.
3. **Die vier Häuser in dieser Reihenfolge, Namen exakt wie auf der Familienseite:**
   - Wellness & Spa Pirmin Zurbriggen
   - Hotel Monte-Moro
   - Suitenhotel Zurbriggen
   - Chalet Rustica
   Bei Wellness steht dazu «mit dem Loft-Suite Hotel». Je Haus ein echtes Foto (`einstieg/site/bilder/`: wellness, monte-moro, zermatt, chalet), dazu Ort und Gastgeber. Das eigene Haus ist mit «Sie sind hier» markiert, die anderen verlinken auf ihre Seite.
4. **Gleich auf allen drei:** Aufbau, Reihenfolge, Texte, Schrift, Fotos. **Angepasst an das Haus:** nur die Farben (Grund und Akzent aus dem Haus).
5. **Verboten:** runde Fotos, Pillen-Kästen, Kreise (Master 2.1 Punkt 6a). Fotos eckig oder mit der Kante des jeweiligen Hauses, edel nach Punkt 6.
6. **Reihenfolge im Fuss:** oben der Teil des Hauses, darunter das Familienband, ganz unten die Rechtszeile (Designstudie-Hinweis, Fotonachweis, Impressum, Datenschutz).
7. **Form des Bandes seit 26.10.2026: «Vier Scheiben»** (Robert wählte «1» aus Wellness `_varianten/fuss-15b`). Vier hohe Scheiben im Format 2:3 Kante an Kante (6px Abstand), aussen gerundet (am Handy zwei Spalten, jede Scheibe gerundet); das eigene Haus trägt unten einen 4px Strich im Akzent statt des Rahmens. Grund wie der Fuss des Hauses, damit es eine Fläche ist. Jede Scheibe schwebt deckend herauf, sobald ihre Oberkante den unteren Rand erreicht, nur über transform. Inhalte, Reihenfolge, Texte und Fotos wie bisher.
   Umgesetzt auf allen drei Häusern (26.10.2026), je mit eigener `assets/css/familienband-scheiben.css` (Farben des Hauses) und `assets/js/familienband-scheiben.js`:
   - Wellness: `start_neu2.py`, `unterseiten_neu.py`
   - Monte-Moro: `bau.py` (`f3_familie()`); das Band steht jetzt unter der eingelassenen Fläche statt darin
   - Suitenhotel Zermatt: `bau.py` (`familienband()`, Link im `kopf()`)

Wer das Band zuerst baut, legt den HTML- und CSS-Block als `familienband.html` hier neben diese Datei. Die anderen beiden übernehmen ihn und passen nur die Farben an.

`familienband.html` (HTML, CSS und Skript der Form «Vier Scheiben») wird von Monte-Moro `website/bau.py` (`familienband_datei()`) bei jedem Bau neu geschrieben; Änderungen an der Vorlage deshalb dort machen, nicht in der Datei.
