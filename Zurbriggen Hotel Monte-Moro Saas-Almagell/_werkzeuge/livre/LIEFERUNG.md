---
tags: [projekt, website]
status: aktiv
---

# Das Markenbuch (livre) · Hotel Monte-Moro, Saas-Almagell · Lieferung 08.11.2026 (mm-livre)

Aufbau und Funktionen aus dem Stamm (Markenbuch der Werkzeuge), Inhalt und Kleid des Hauses. Nichts online, nichts verschickt, keine KI-Aufrufe.

**Adressen:** http://127.0.0.1:9385/_werkzeuge/livre/ · Hausregeln: http://127.0.0.1:9385/_werkzeuge/livre/buch.html · Anleitung: http://127.0.0.1:9385/_werkzeuge/livre/anleitung.html · Stand-Weg für das Hotelbüro: http://127.0.0.1:9385/marke/livre.json

Server: `python3 server.py 9385` im Ordner `_werkzeuge/livre` (Markenprüfung ohne Claude, Probe-Antwort). Neu bauen (nur mit `_quelle/` und laufendem Server 9385): `python3 bau.py && python3 buch.py`, Bilder der Anleitung `node anleitung_bilder.js && python3 anleitung_bau.py`.

## Was steht

- **Fotos (74):** alle Fotos, die die Website zeigt (`website/inhalt/bilder.py`, Masse und echte Quelle aus `website/assets/img/_masse.json`), dazu «Haus im Sommer/Winter» (Quelle der Farben). Doppelte zusammengeführt (2). Sieben Bereiche: Das Haus, Die Zimmer, Ferienwohnungen, Röstihüs und Frühstück, Für Kinder, Spa im Partnerhotel, Das Saastal; Saison Sommer/Winter/ganzjährig. Herkunft je Foto aus dem Material: 14 vom Haus (heutige Website, Schweiz Tourismus aus der HotellerieSuisse-Datenbank, Booking.com und Tripadvisor vom Haus), 59 mit KI neu gerechnet (24.10.2026, nach dem Foto des Hauses; «Vorher/Nachher/Schieber» mit dem Original, `original/`), 1 frei lizenziert (Christoph Strässler, CC BY-SA 2.0). Fotograf nur, wo belegt. Weggelassen: Bilder der anderen Häuser der Familie (Wellnesshotel, Zermatt, Chalet Rustica, Massage aus dem Wellnesshotel). Je Foto Beitrag, Story, Website, Druck (Druck aus der Quelle in voller Grösse).
- **Logo & Dateien (32):** Wortmarke in Logo-Blau, Nacht, Papier, Lärche; Bergkamm in denselben vier; Medaillon in Logo-Blau, Lärche, Papier (je SVG und PNG, aus `_kette/05-markenbauer/marke/zeichen/`); das Original `logo.png` (1161 × 475); Tapete auf Papier und auf Nacht; 13 Farben der Website (`montemoro.css`, mit Fundstelle aus `farben.json`) als CSS, JSON, ASE; Fjalla One, Instrument Sans, DM Mono (Dateien der Website, ZIP mit TTF und OFL); alles als ZIP.
- **Markenprüfung:** Farben ohne KI gemessen (ΔE 2000 gegen die Palette des Hauses), Rest Probe-Antwort (nur mit `LIVRE_KI=1` echt). Regeln des Hauses in `livre.py regeln()` (Farbwelt A, Schriften, Zeichen, Bausteine, Bilder, Ton, Sie-Form). Beispiel: eigens gezeichneter Beitrag «Luxus-Winter» mit Foto und Wortmarke, aber fetter Serifenschrift, Neon-Pink, reinem Schwarz, Du-Form und «JETZT BUCHEN».
- **Hausregeln (buch.html):** acht Blätter aus dem Markenbuch der Station 05: Haltung, Zeichen und Name, Farben, Schrift, Bausteine (Knöpfe, Grat, Tapete), Bilder, Logo richtig und falsch, Ton; zwei Fenster («Bei uns scheint fast immer die Sonne.», «Es lebe die Tradition!»); Fuss mit Adresse/Telefon/Mail aus `daten.py`; «Als PDF sichern».
- **Anleitung:** neun Kapitel in Sie-Form, Bilder aus dem echten Werkzeug.
- **Kleid:** `kleid/montemoro.{js,css}`, Namen über `WO_HAUS.namen`; eigenes CSS nur für Knöpfe als Pille mit Knauf (wie `.kn` der Website), Speicher `livre-montemoro-*`. Vercel-Teil (`online/`) entfernt.

## Wie geprüft (Chromium, 08.11.2026)

- `tor-schnell` `--nur markenbuch` (16 Zustände), `markenbuch-buch` (6), `markenbuch-anleitung` (8), je 1440/1280/1000/390, mit dem umgestellten Stilblatt der Hausdruckerei: **0 Funde.**
- Gegenprobe Oberchef: Lärche in Titeln nur im letzten Wort (Startbild «Guten Tag. Womit beginnen wir heute?», Hausregeln, Anleitung); Kachel Markenprüfung zeigt «13 Farben des Hauses» statt «ΔE 2000».
- Messlauf alle drei Schlüssel, 1440/1280/1000/390: 0 Funde.
- `oberflaeche_pruefen.js` auf `/_werkzeuge/livre/`: BESTANDEN.
- Mit den Augen: 16 Zustände 1440, 12 Zustände 390, Hausregeln ganz, Logo & Dateien ganz, die neun Anleitungsbilder, das Beispiel.

## Offen

- nichts.
