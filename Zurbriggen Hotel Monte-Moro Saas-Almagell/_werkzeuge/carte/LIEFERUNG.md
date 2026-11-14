---
tags: [projekt, website]
status: aktiv
---

# Lieferung Karten & Preislisten (Karten und Preislisten) · Hotel Monte-Moro, Saas-Almagell (08.11.2026, mm-carte)

Kopie des Kartenwerkzeugs aus dem Stamm (Culinarium → Wild Side), umgekleidet ins Kleid des Monte-Moro und mit den Karten und Preislisten des Hauses gefüllt («kopieren, umkleiden, Hauswerte eintragen»). Name nur aus `_werkzeuge/oberflaeche/kleid/montemoro.js` (**Karten & Preislisten**; Ordner, Adressen und Schlüssel bleiben `carte`).

**Werkzeug:** http://127.0.0.1:9383/_werkzeuge/carte/ · **Anleitung:** http://127.0.0.1:9383/_werkzeuge/carte/anleitung.html · **Prüfung:** http://127.0.0.1:9383/_werkzeuge/carte/pruefung.html

## Was steht

Fünf Karten, je ein Blatt bzw. eine PDF im Satz des Hauses, links im Rand in zwei Gruppen:

- **Restaurant Röstihüs**
  - **Die Röstihüs-Karte** (2 Seiten): «Best of Röstis» (elf Röstis), «Unsere Cordon bleus» (fünf), «Zum Dessert» (Monte-Moro-Kopf), «Im Stübli» (Raclette gross mit Pellkartoffeln), darunter Beilagen und Herkunft des Fleisches wörtlich aus der Speisekarte. Titel «Restaurant Röstihüs», Zeile «Es lebe die Tradition!».
  - **Wein und Apéro**: ««Hotelwein»» – Cuvee Special und Cuvee Special Eichenfass («wurde von Fabian selber kreiert», 7 dl, 67.–) – und «Zum Apéro» mit den sieben Spritz der Speisekarte (darunter Zurbriggen und Antrona Spritz aus `daten.py`).
- **Hotel Monte-Moro**
  - **Die Preisliste**: Zimmer mit Frühstück (Budget CHF 90.00, Standard CHF 100.00), mit Halbpension (4-Gänge) (CHF 120.00 / 130.00), «Inklusive» (sechs Punkte), «Bezahlung in Euro möglich, Rückgeld in Franken.»
  - **Zuschläge und Kinder**: Kurtaxe Winter/Sommer, Einzelzimmerzuschlag 50 %, Zuschlag 1–3 Übernachtungen, Hund; Kinderzuschläge im Zimmer der Eltern (bis 5 Jahre … 9–16 Jahre).
  - **Spa im Partnerhotel**: Eintritt CHF 25.00 und 7 Tage Abo CHF 150.00, Satz und Angebot des Spa, «Bademantel, Schuhe, Handtücher stehen zur Verfügung.»
- **Quelle und Prüfung der Inhalte** (`karten_lesen.py`): liest `website/inhalt/daten.py` als Text (ROESTIS, CORDON, HOTELWEINE, SPRITZ, KOPF, RACLETTE, PREISE, INKLUSIVE, ZUSCHLAEGE, KINDER, SPA_*, EURO, HAUS), Rubriken, Spritz, Beilagen und Herkunft wörtlich aus der Speisekarte (`_quelle/website/pdf/speisekarte.pdf`, Stand 18.11.2024; pdftotext als Beleg in `_daten/beleg/`, zur Laufzeit lädt nichts aus `_quelle/`). Bricht ab, wenn ein Wort nicht in daten.py, Speisekarte oder Website steht, ein Restaurant-Preis nicht so in der Speisekarte oder ein Hotelpreis nicht so auf `preise.html`/`spa.html` steht, oder etwas aus `OFFEN` (Öffnungszeiten, Ruhetage) auftaucht. Nur Typografie geändert, Wortlaut gleich: «Mozzarella , Salami» → «Mozzarella, Salami», «Syrah,Merlot» → «Syrah, Merlot», «Übernachtungen / pro Tag» → «Übernachtungen, pro Tag», «|» auf dem Blatt als «·».
- **Satz des Hauses** (`satz_bau.py`, `satz/satz.css`, A4 hoch, Machart der Karte auf `roestihues.html` und der Preisliste): Papier mit doppelter Messing-Linie, oben das Logo des Hauses (Logo-Blau, `montemoro-marke.svg #wm`, unverändert) bzw. auf Seite 2 der Bergkamm in Lärche, Titel in Fjalla One mit dem letzten Wort in Lärche, kleine Zeile in DM Mono, Rubriken mittig mit kurzer Messing-Linie, Name · Punktlinie · Preis in Lärche tief, Beschreibung in Instrument Sans; unten die Nacht mit der Grat-Kante der Website (Linie in Lärche) und der Adresse. Preise wie das Haus: Röstihüs «25.–», Hotel «CHF 90.00». Feste Schnitte für das PDF aus den Schriften der Website (`fonts_statisch.py` → `fonts/FjallaOne-400.ttf`, `InstrumentSans-400/500.ttf`, `DMMono-400.ttf`).
- **Werkzeug** wie im Stamm (Master 4.3): Einfach / Fortgeschritten, Entwurf, Quittung, Rückgängig, Vorher/nachher, Probe-PDF, Veröffentlichen mit Wort-für-Wort-Prüfung, frühere Fassungen, Protokoll, Prüfseite, Export, Rundgang, Zur Werkbank (9388), Ansicht Website (Röstihüs, Preise, Spa; rollt zur Karte, zur Preisliste bzw. zu den Tarifen). Sie-Form, Schweizer Schreibung. Gestalten mit den Schriften und Farben des Hauses (Fjalla One, Instrument Sans, DM Mono; Nacht, Logo-Blau, Tinte, Grau, Lärche, Lärche tief, Messing, Papier). Preise im Fenster in der Schreibweise des Hauses («25» → «25.–» bzw. «CHF 25.00» je nach Karte). Fotos je Karte aus `website/assets/img/` (gedeckte Tische im Röstihüs, Raclettestübli, Frühstücksbuffet, Kinder beim Rodeln, Ruheraum im Spa), klein `bilder/z/`, gross `bilder/g/`.
- **Jede Karte einmal veröffentlicht** (08.11.2026, «Team Monte-Moro · Direktion», Protokoll «Erste PDF»): `_daten/live/<karte>.pdf` steht bereit, das Werkzeug zeigt «Alles veröffentlicht · PDF vom 08.11.2026».
- **Eine Quelle für Karte und Website (C27):** jedes Veröffentlichen schreibt `anschluss/karten.json`.
- **Demo-Sperre:** Datei `DEMO` liegt; Karten & Preislisten schreibt nie in `website/`. Die ganze Speisekarte der Website (`assets/pdf/speisekarte.pdf`) wird auch mit Anschluss nie überschrieben.
- Die Wochenkarte des Stamms (Kennung `abend`) führt das Haus nicht; ihr Code bleibt ruhend und wird nur aktiv, wenn `_daten/quelle/abend.json` liegt.

## Starten und neu bauen

- `python3 _werkzeuge/carte/serve.py 9383` → http://127.0.0.1:9383/_werkzeuge/carte/
- Karten neu: `python3 _werkzeuge/carte/karten_lesen.py` → `python3 _werkzeuge/carte/satz_bau.py` → `python3 _werkzeuge/carte/einlesen.py` (ein Stand des Hauses wird nie überschrieben); Schriften `fonts_statisch.py`; `?v=` der Seiten `fassungen.py`.
- `python3 _werkzeuge/carte/pruefe.py alles` (Server muss laufen).

## Wie geprüft (08.11.2026)

- `pruefe.py alles`: Rundlauf 5/5 Zeichen für Zeichen gleich; Wortlaut jeder gedruckten Karte gegen ihre Quelle 5/5 gleich (233 / 110 / 96 / 131 / 90 Wörter); Karten in der Form der Website = Quelle 5/5; Schriften aller PDFs nur feste Schnitte (pdffonts: FjallaOne-Regular, DMMono-Regular, InstrumentSans-Regular, CID TrueType, kein Type 3), pdftotext ganze Wörter. GESAMT GRÜN. Veröffentlichen hat jede PDF zusätzlich Wort für Wort gegen die Daten geprüft (245 / 116 / 101 / 135 / 96 Wörter).
- Schnelle Prüfung, Messlauf, Oberfläche: siehe «Prüfstand».
- Mit den Augen: jede PDF-Seite (6) und über 20 Zustandsbilder 1440/390 (Start jeder Karte, Fortgeschritten, Website-Ansicht, Rundgang, Fenster Protokoll, Neuer Eintrag, Daten der Karte, Vorher/nachher, Handy-Rand, Anleitung). Unterwegs repariert: Knopfschrift 0,5 px zu hoch (DM Mono), Rubrik-Wahl 1 px zu tief, Einzelwörter in Listenzeilen, Versalien nur in DM Mono, «Monte-Moro» brach am Bindestrich, Website-Ansicht rollt zur Stelle selbst, Startbild ohne angeschnittene Schrift im Foto (Sack «Röstihüs» → gedeckte Tische), Spa-Foto ohne Collage.

## Prüfstand

Letzter Lauf 08.11.2026 (Chromium; WebKit in dieser Sitzung nicht installiert), Ergebnis in `aus/kartenbrett*/`, `aus/mess-kartenbrett*/`:
- `tor-schnell` **kartenbrett**: 20 Zustände, 1440/1280/1000/390, **0 Funde**, nichts «nicht erreicht», keine Browserfehler.
- `tor-schnell` **kartenbrett-anleitung**: 15 Zustände, **0 Funde**, nichts «nicht erreicht».
- Messlauf kartenbrett 1440 (18 Zustände) und 390 (23 Zustände): **0 Funde**; kartenbrett-anleitung: **0 Funde**.
- `oberflaeche_pruefen.js` Werkzeug und Anleitung: **BESTANDEN**.
- `pruefe.py alles`: **GRÜN**.

## Offen, mit Grund

- **Öffnungszeiten und Ruhetage des Röstihüs** stehen in `OFFEN` (daten.py): auf keiner Karte.
- **Übrige Rubriken der Speisekarte** (Vorspeisen, Suppen, Warme Speisen, Kinderkarte, Weine, Getränke) sind belegt, aber nicht Teil des Auftrags; sie lassen sich mit `karten_lesen.py` wörtlich aus dem Beleg nachziehen.
- **Website liest Karten & Preislisten noch nicht:** Einbau von `karten.json` in den Bau der Website (Revier `website/`, mit Auftrag und ohne DEMO).
- **Kleid (für mm-maison):** nichts fehlte; im eigenen CSS gelöst: Knopf-Grundlinie DM Mono (`.kn{padding-top:1px}`), `.lc .wo-sb__zier .nw{white-space:nowrap}` (die Zier des Startbilds bricht sonst «Monte-Moro» am Bindestrich).
- **Prüfregel (für den Oberchef):** `oberflaeche_pruefen.js` Regel 3 «Abschnitt fast leer» zählt ein `iframe` nicht als Inhalt; die Vorschau Karten & Preislisten (Karte im Rahmen) fiel deshalb zuerst durch. Gelöst mit einer sinnvollen Kopfzeile («Vorschau: <Karte> · n Seiten, so wie in der PDF»); Vorschlag: `iframe` in die Liste `img,video,canvas,svg image` aufnehmen.
- **Online** nicht gebaut und nicht hochgeladen (Auftrag).
