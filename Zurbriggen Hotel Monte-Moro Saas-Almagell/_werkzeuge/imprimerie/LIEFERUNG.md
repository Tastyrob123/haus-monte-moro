---
tags: [projekt, website]
status: entwurf
---

# Die Plakatwerkstatt (L’Imprimerie) · Walk on the Wild Side Hannover · Lieferung

**Stand:** 31.10.2026, Nachtbau (Auftrag Oberchef, `_werkzeuge/AUFTRAG-GEMEINSAM.md`). Kopie der von Robert abgenommenen Plakatwerkstatt des Culinarium, umgekleidet und mit den Inhalten der Bar gefüllt. Lokal, nichts hochgeladen, nichts verschickt, keine KI aufgerufen (Probe-Antworten).

## Wo

- **Werkzeug:** http://127.0.0.1:9387/_werkzeuge/imprimerie/ · Server im Ordner `_werkzeuge/imprimerie`: `python3 serve.py 9387`
- **Newsletter-Baukasten:** http://127.0.0.1:9387/_werkzeuge/imprimerie/mail.html · **Prüfseite:** …/pruefung.html · **Anleitung:** …/hilfe/
- **Drucksachen der Bar:** `haeuser/montemoro/drucksachen/` (PDF + Vorschaubild, Liste `LISTE.md`, `liste.json`)
- **Name:** aus `_werkzeuge/oberflaeche/kleid/montemoro.js` (`WO.name('druck')`), Dateien und Adressen bleiben `imprimerie`. Merker ohne Begrüssung: `localStorage['ds-montemoro-willkommen'] = '1'`.

## Wiederholbar gebaut

```
python3 bau.py                       Marke (marke.json), Schriften, Tapete, 202 Fotos der Website, die vier weissen Plakate der Bar, drei Wellen, 15 Schwarzweiss-Porträts, Druckfassungen
python3 bau_vorlagen.py              Katalog (katalog.js), 84 Vorlagen in 16 Arten, Beispielinhalte (start.js INHALT, vorlagen.js DS.BEISPIEL); prüft, dass jede Zahl in den Quellen steht
NODE_PATH=$(npm root -g) node _bau/drucksachen.js    20 Drucksachen als PDF + JPG mit Druckprüfung, LISTE.md
NODE_PATH=$(npm root -g) node _bau/mail_marken.js    Kopf, Fuss, Trenner der Mails (echte Wortmarke)
NODE_PATH=$(npm root -g) node _bau/filme.js          neun Kurzfilme der Führung und das Demo-Video (hilfe/)
```

## Kleid und Kennung

- Haus-Kennung `montemoro` überall (`haeuser/montemoro/`, `ds-montemoro-*`, `montemoro-wb`, `ws-imprimerie-fehler`); `haeuser/culinarium/` gelöscht.
- Farben aus dem Kleid: Nacht `#130E0D`, Platte `#1C1513`/`#261E1A`, Creme `#F2E9DC`, Gold `#D8B264` als Linie, Rot `#F0323F` nur für die Wortmarke; Ultramarin `#1A00AA`, Plakatrot `#D21C0A`, Plakatcreme `#EBE2D8` nur bei SESSION. Alle rosa, violetten und Kerzen-Töne der Vorlage umgefärbt.
- Schriften (OFL, feste TrueType-Schnitte, im PDF eingebettet): Prata (Titel), Hanken Grotesk 400/500/600 (Lauf, Etiketten, Zeilen der weissen Plakate), Rammetto One (SESSION-Plakate, breite fette Versalien wie auf den echten Plakaten).
- Zeichen und Wortmarke: das echte Logo (`kleid/montemoro-marke.svg`), nie als Schrift.
- Stilblatt: `haeuser/montemoro/stilblatt.json` (Rollen, Versalien, Trenner, Schreibung, Farben, Ränder, Achse).

## Inhalt (nur aus Website, Plakaten und Beiträgen der Bar)

- **Zwei neue Aufbauten in der Plakat-Sprache der Bar** (`vorlagen.js`): «SESSION-Plakat» (Wellen, «SESSION / SIP & SOUNDS», Gesicht in Schwarzweiss, Name, «17|10», «10 PM TO 1 AM», Wortmarke und Adresse) und «Weisses Plakat der Bar» (Bild, rote Wortmarke, «Eure Nachbarschafts-Mixology-Bar», Titel in Versalien, Datum «31 | 12 | 25», Angaben, Adresse).
- **Abteilungen:** Plakate der Bar (17 echte Plakate ganz), SESSION-Plakate (9 DJ-Abende aus `LINEUP` + A3, Story, Beitrag, Programm), Feste und Gäste (Silvester, Tanz in den Mai, Relaunch, Geburtstag, Konzert, Valentinstag, Oktoberfest, 5 Gastschichten), Karte & Drinks (Drunk in Love mit Preisen vom Plakat, Preise der Bar, Klassiker, Techniken, Tischaufsteller), Feiern im Wild Side (Angebote mit Preisen aus `tafel.html`, Gutschein), Das Haus.
- **Anlässe:** Oktoberfest des Event Klub (31.10./01.11.2026), SESSION am Samstag, Geburtstag der Bar (im Winter, Termin auf Instagram), Silvester, Valentinstag, Tanz in den Mai.
- **DJ-Abend anlegen** (vorher «Abend beschreiben»): Name, Uhrzeit, Samstag → 3–5 SESSION-Plakate sofort, ohne KI. **Plakat-Grund** (vorher «Plakat-Motive»): Wellen und Schwarzweiss-Gesichter.
- **Mails:** sechs versendbare Mails der Bar (nächster DJ-Abend, Feiern, Jeder Abend ein Plakat, Live am Donnerstag, Reservierung, Danke). Kein `mailto`, keine erfundene Mail-Adresse: Telefon und Instagram.

## Offen, mit Grund

- **Nächster DJ-Abend:** steht nicht fest (kündigt die Bar auf Instagram an). Die SESSION-Beispiele tragen die vergangenen Abende; das Foto im Plakat ist ein Bild der Bar in Schwarzweiss, die DJ-Porträts gibt es nur in den fertigen Plakaten.
- **Silvester 2026, dritter Geburtstag:** Uhrzeiten und Datum nicht angekündigt, stehen nicht auf den Vorlagen.
- **E-Mail-Adresse der Bar:** nicht belegt, nirgends eingetragen.
- **Online:** `online.json` vorbereitet, kein Online-Projekt der Bar.

## Geprüft (31.10.2026, schnelles Abnahme-Tor lokal, Chromium, 1440/1280/1000/390)

- `plakatwerkstatt`: 176 Zustände (40 + 40 + 40 + 56), 0 Funde, nichts «nicht erreicht».
- `plakatwerkstatt-mail`: 170 Zustände (40 + 40 + 40 + 50), 0 Funde, nichts «nicht erreicht».
- Drucksachen: 20 Stück, Druckprüfung ohne roten Befund, Schriften als CID TrueType eingebettet (`pdffonts`).
- Mit den Augen: Übersicht, Anlässe, Abteilungen, Hinweise, Newsletter, Fotos, Farben & Schriften, DJ-Abend anlegen, Plakat-Grund, Editor (1440/1000/390), Mail-Baukasten, Prüfseite, Anleitung, alle 20 Drucksachen als Bild.
