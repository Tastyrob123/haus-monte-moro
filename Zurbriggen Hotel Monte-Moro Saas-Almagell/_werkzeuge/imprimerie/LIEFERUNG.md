---
tags: [projekt, website]
status: aktiv
---

# Drucksachen & Feed · Hotel Monte-Moro, Saas-Almagell · Lieferung

**Stand:** 08.11.2026 (Agent mm-imprimerie, Auftrag `_werkzeuge/AUFTRAG-GEMEINSAM.md`). Kopie der Plakatwerkstatt des Culinarium über den Stand des Wild Side, umgekleidet auf das Monte-Moro und mit den Inhalten des Hauses gefüllt. Lokal, nichts hochgeladen, nichts verschickt, keine KI aufgerufen (Probe-Antworten). Der Wild-Side-Stand liegt unverändert in `/tmp/wildside/…/_werkzeuge/imprimerie/` (Sicherung).

## Wo

- **Werkzeug:** http://127.0.0.1:9387/_werkzeuge/imprimerie/ · Server im Ordner `_werkzeuge/imprimerie`: `python3 serve.py 9387` (liefert jetzt `/assets/img/` und `/assets/fonts/` der Website)
- **Newsletter-Baukasten:** …/mail.html · **Prüfseite:** …/pruefung.html · **Anleitung:** …/hilfe/
- **Drucksachen des Hauses:** `haeuser/montemoro/drucksachen/` (PDF + Vorschaubild, `LISTE.md`, `liste.json` für die Werkbank)
- **Name:** nur `WO.name('druck')` aus `kleid/montemoro.js`; Dateien und Adressen bleiben `imprimerie`. Merker ohne Begrüssung: `localStorage['ds-montemoro-willkommen'] = '1'`.

## Wiederholbar gebaut

```
python3 bau.py                      Marke (marke.json), Schriften, Tapete, 95 Fotos der Website, 15 Bergbilder, Druckfassungen, Wissen für die Entwürfe
python3 bau_vorlagen.py             Katalog (katalog.js), 74 Vorlagen in 18 Arten, 6 Abteilungen, 4 Anlässe, Beispielinhalte; prüft, dass jede Zahl in den Quellen steht
NODE_PATH=$(npm root -g) node _bau/drucksachen.js     34 Drucksachen als PDF + JPG mit Druck- und Stilprüfung, LISTE.md, liste.json
NODE_PATH=$(npm root -g) node _bau/vorschaubilder.js  Vorschaubilder der Galerien (haeuser/montemoro/vorschau-dok/)
NODE_PATH=$(npm root -g) node _bau/mail_marken.js     Kopf, Fuss, Trenner der Mails (echte Wortmarke in Papier)
NODE_PATH=$(npm root -g) node _bau/filme.js           neun Kurzfilme der Führung und das Demo-Video (hilfe/)
```

## Kleid und Kennung

- Haus-Kennung `montemoro` überall (`haeuser/montemoro/`, `ds-montemoro-*`, `mm-imprimerie-fehler`). Event-Engine, SESSION-Plakat, weisses Plakat, Valentinskarte, Wellen, Schwarzweiss-Porträts und alle Plakatbilder der Bar sind entfernt.
- **Farben** aus dem Markenbuch (`_kette/05-markenbauer/marke/farben.json`): Nacht, Tiefnacht, Nachtblau, Logo-Blau, Lärche (Akzent), Lärche tief, Messing (nur Linie), Papier, Creme, Fassade, Tinte, Grau. Die Oberfläche: alle warmen Töne der Vorlage (Braun, Gold, Rot) in die Farbwelt des Hauses gedreht, Hauptknopf Lärche.
- **Schriften** wie die Website: Fjalla One (Titel, eine Stärke, normal geschrieben), Instrument Sans 400/500 (Lauf, betont), DM Mono (kleine Zeilen, Preise, Zeiten in Versalien gesperrt). Im PDF als TrueType eingebettet (Instrument Sans aus der variablen Datei als feste Instanzen 400 und 500 gerechnet); `pdffonts`: alle 97 Schriften CID TrueType, kein Type 3.
- **Zeichen:** Bergkamm (`kleid/montemoro-zeichen.svg`), ganze Wortmarke «Monte Moro / Saas-Almagell» (`kleid/montemoro-marke.svg`) in Logo-Blau oder Papier, die Grat-Kante der Website (`--grat-maske`) als drittes Zeichen.
- **Drei Aufbauten des Hauses** (`haeuser/montemoro/dokumente.js`): «Bild mit Grat» (Wortmarke, Etikett in Lärche, Titel, Satz, unten ein Foto mit Grat-Oberkante), «Brief des Hauses» (Briefpapier und Willkommensbrief), «Blatt auf Nacht» (Karte oder Preisliste als Papier auf Nacht).
- **Stilblatt:** `haeuser/montemoro/stilblatt.json` (Rollen, Schreibung, Trenner, Achse, Grössen, Mindestgrade, Farben, Ränder) – Abnahme-Tor und Druckprüfung prüfen jede Vorlage dagegen.
- **Anrede:** Sie in der ganzen Oberfläche, Schweizer Schreibung.

## Inhalt (nur aus `website/inhalt/daten.py` und den Seiten der Website)

- **Abteilungen:** Röstihüs-Karte (Röstis, Cordon bleus, Wein von Fabian, Apéro und Dessert, Auszug, Tischaufsteller, Beiträge), Preise & Inklusive (Inklusive, Zimmerpreise, Zuschläge, Kinderpreise, Beiträge), Racletteabend & Kidsclub, Im Zimmer (Willkommensbrief, Briefpapier, Hinweise, Spa-Tarife, Tischkarten Hotelwein), Saastal & Anreise (Postauto, Auto, Wandern, Winter, Ansichtskarten, Spa-Story), Das Haus & Geschenke (Gutscheine, Flyer, Gastgeber, Noten, Ferienwohnungen).
- **Anlässe:** Racletteabend im Stübli (wöchentlich), Kidsclub (Mo–Sa), Winter und Sommer im Saastal (gedruckt wird nur «im Winter», «im Sommer»).
- **Aushang anlegen** (vorher «DJ-Abend anlegen») und **Bergbilder** (vorher «Plakat-Grund»): eigener Aushang mit Grat-Kante aus Titel, Satz, Foto und Grund.
- **Mails:** Racletteabend, Ihre Anfrage (mit Preisliste), Sommer im Saastal, Winter im Saastal, Vor Ihrer Anreise, Danke für Ihren Besuch. Kontakt: Telefon, E-Mail, Website des Hauses.
- **Nicht drin, weil das Haus es nicht veröffentlicht (OFFEN):** Öffnungszeiten des Röstihüs, Strasse, Storno, Fotos vom Kidsclub, Wochentag des Racletteabends. Die Gratis-Anreise ist abgelaufen und steht nirgends.

## Geprüft (08.11.2026, lokal, Chromium; WebKit ist in dieser Sitzung nicht installiert)

- **Abnahme-Tor schnell** (`tor-schnell.js --max 40 --tiefe 2 --breiten 1440,1280,1000,390`), letzter Lauf nach allen Reparaturen:
  - `hausdruckerei`: 178 Zustände (40 + 40 + 40 + 58), **0 Funde**, nichts «nicht erreicht».
  - `hausdruckerei-mail`: 172 Zustände (40 + 40 + 40 + 52), **0 Funde**, nichts «nicht erreicht».
  - Ergebnis in `aus/hausdruckerei/`, `aus/hausdruckerei-mail/`. Gelaufen mit einer Kopie der Zielliste, in der für `hausdruckerei` der Merker `ds-montemoro-willkommen` steht (die Zielliste des Oberchefs nennt noch `ds-wildside-willkommen`).
- **Messlauf** (`messlauf.js --nur hausdruckerei,hausdruckerei-mail --browser chromium --groesse 1440,390`): 1 Fund (Bildbeschreibung im Fotofach der Mail mit «…» gekürzt) → repariert. Der Messlauf erreicht in Drucksachen & Feed nur 5–6 Zustände, weil seine Zielliste keinen Begrüssungs-Merker setzt.
- **Oberflächenprüfung** (`oberflaeche_pruefen.js`): Werkzeug und Mail-Baukasten BESTANDEN.
- **Drucksachen:** 34 Stück (40 Seiten), Druck- und Stilprüfung ohne roten Befund; `pdffonts`: 97 Schriften, alle CID TrueType eingebettet, kein Type 3; `pdftotext`: kein «ß», keine Wörter der Bar, keine Gratis-Anreise.
- **Vorlagen:** alle 74 Vorlagen und jeder Aufbau in jedem seiner Formate gesetzt und gegen Druck- und Stilprüfung gelaufen; Zahlen der Texte gegen `daten.py` und die Seiten der Website geprüft (`bau_vorlagen.py`: nichts unbelegt).
- **Mit den Augen:** Übersicht, Anlässe, Aushang anlegen (mit Vorschau und Gründen), Bergbilder, Abteilungen, Hinweise, Newsletter, Fotos, Farben & Schriften, Arten und Vorlagen, Editor (1440/1000/390), Mail-Baukasten, Hilfe-Film, 32 zufällige Zustandsbilder des Tors, alle 34 Drucksachen als Bild.

## Offen

- Zielliste des Abnahme-Tors (`_Werkzeuge/abnahme-tor/ziele-monte-moro.json`, Oberchef): beim Schlüssel `hausdruckerei` den Merker `ds-montemoro-willkommen` statt `ds-wildside-willkommen`/`ds-culinarium-willkommen` eintragen. Zielliste des Messlaufs: denselben Merker als `localStorage` ergänzen, damit er über die Begrüssung hinauskommt.
- Das Markenbuch (`_werkzeuge/livre/livre.json`) wird nur genutzt, wenn es `haus` «Monte-Moro» und `hausdruckerei: true` meldet; bis dahin arbeitet Drucksachen & Feed mit ihrer eigenen Kopie der Website-Fotos.
- WebKit nicht geprüft (in dieser Sitzung nicht installierbar).
