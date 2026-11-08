# Hotel Monte-Moro · Website (Designstudie) · ÜBERGABE

**Stand 18.10.2026, Station 07 der Kette (Baumeister).** Nichts ist online. Nur lokal.

## Öffnen
- Über die Karte der Kette (Port 8978, läuft immer): http://127.0.0.1:8978/haus/Zurbriggen%20Hotel%20Monte-Moro%20Saas-Almagell/website/index.html
- Eigener Server: `cd website && python3 serve.py` → http://127.0.0.1:8947/ (antwortet nur dem eigenen Rechner)
- Auftakt im Winter ansehen: `index.html?jz=winter` (sonst Mai bis Oktober Sommer)

## Was wo liegt (`website/`)
- `bau.py` baut die Startseite und sechs Unterseiten aus `inhalt/daten.py` (Wortlaut der Quellen) und `inhalt/bilder.py`; schreibt `assets/js/wissen.json` (Chat) und `../Familie Zurbriggen/familienband.html` (Block für Wellness und Zermatt).
- `assets/css/montemoro.css`, `assets/js/montemoro.js` (ruhige Auftritte, Kopf, Menü, Buchung), `assets/js/anfrage.js` (Anfrage-Fenster, kein mailto), `assets/js/rezeption.js` (Chat), `assets/js/bilder.js` (Lader).
- `serve.py` (Port 8947) nimmt Anfragen unter POST /api/anfragen an und legt sie in `_dienste/anfragen.jsonl` ab; auf der Karte (8978) wird nichts abgelegt.

## Gebaut nach dem Drehbuch (`_kette/07-baumeister/DREHBUCH.md`, freigegeben 18.10.2026)
Ein Tag bei Esther und Fabian in acht Kapiteln: Morgen über Saas-Almagell · Aufwachen im Zimmer · Frühstück und der Bon · Der Tag im Saastal · Nach dem Lift: das Spa nebenan · Abend im Röstihüs · Die Kinder bis 21 Uhr · Der Wein von Fabian; Schluss «Und morgen scheint die Sonne wieder.», Fuss mit Familienband.
Unterseiten: zimmer.html, preise.html, saastal.html, spa.html, roestihues.html, anreise.html, je mit Anfang (grosses Foto) und Ende (Satz ins nächste Kapitel).
Kapitel liegen still (keine Staffelung mehr), Bilder als Paar oder Rahmen bündig ohne Lücken. Vorige Fassungen: `../website.vor-drehbuch-2026-10-18/`, `../website.edel-2026-10-18/` und älter.

## Gemessen
Alle Seiten 4× und 6× gedrosselt 120 Bilder/s, p95 9,2 ms, kein langes Bild. Chromium und WebKit 1440 und 390 ohne Konsolenfehler, kein seitliches Überlaufen; Anfrage-Fenster (Tisch, Fuss), Kalender geprüft, kein mailto ausgelöst.

## Offen
Siehe `_kette/07-baumeister/stand.json › offen` und `inhalt/daten.py › OFFEN`. Unterseiten folgen. Film «Wallis Baby» liegt hinter `FILM_JA = False` (nur mit Fabians Ja).

## Stand 19.10.2026 nachmittags (neue Projektleitung)
- **Mehr Bilder** (Robert 19.10.: «Wir haben die ganzen visuellen Materialien, aber wir benutzen sie nicht.»): 33 neue Fotos des Hauses in `inhalt/bilder.py` (Abschnitt «Mehr Bilder 19.10.2026»), auf der ganzen Seite jetzt 73 statt 40 verschiedene Fotos. Startseite: Aufbau und Einfälle unverändert, je Kapitel mehr Ebenen (Gastgeber 3, Zimmer 5, Saastal 5, Spa und Röstihüs als Ebenen statt Bildpaar). Lagen in `assets/css/bewegung.css` ab «Mehr Bilder».
- **Familienband:** Chalet Rustica jetzt mit dem Haus im Sommer (Holidu, Rustica 4). Die gemeinsame Vorlage `Familie Zurbriggen/familienband.html` bleibt beim alten Foto (bau.py ersetzt es dort zurück), die anderen Häuser entscheiden selbst.
- **Unterseiten nach `_kette/07-baumeister/PLAN-UNTERSEITEN.md`** (Robert «ja» 19.10.): Probe Zimmer und Röstihüs neu: Kopf der Tageszeit (`kopf_tag`), Zimmerarten als Blätter mit vier Ebenen und Angaben-Zeilen (`blatt`), «Alle Ansichten» im Fenster (`galerie`, `assets/js/galerie.js`), Karte als Zettel je Rubrik (`zettel`). Preise, Saastal, Spa, Anreise haben nur mehr Bilder bekommen, ihr Umbau folgt nach Roberts Blick auf die Probe.
- Stand davor: `../website.vor-mehr-bilder-2026-10-19/`.

## Stand 20.10.2026 abends (Roberts Runde 17:24–17:31)
- Startseite nach Roberts Bildschirmfotos: Bon füllt sich aus statt aufzustempeln, Röstihüs-Fotos ohne Lücken, Röstimenü ruhiger, Kidsclub-Uhr mit Luft, Wein mit verschiedenen Motiven, Schlussbild echtes Foto (Christoph Strässler, Commons, CC BY-SA 2.0).
- Unterseiten neu: Preise (Aushang mit zählenden Preisen), Saastal, Spa und Anreise je als eigene Datei in `website/seiten/` (`saastal.py`, `spa.py`, `anreise.py`, eigenes CSS `assets/css/seite-*.css`); Kopf aller Unterseiten wie Zimmer (Titel auf dem Himmel).
- Fuss 19 «Eingelassen» auf allen Seiten, Familienband im Fuss schwebt herein (Vorlage `Familie Zurbriggen/familienband.html` unverändert).

## Stand 23.10.2026 (Feinschliff für den Brief, nur lokal)
- **Pflichtseiten:** `impressum.html` (Wortlaut des Hauses + Bildnachweis), `datenschutz.html` (Wortlaut des Hauses), `404.html`, `robots.txt` (Sperre), `sitemap.xml`; gebaut von `bau.py` (`seite_impressum`, `seite_datenschutz`, `seite_404`, `nebendateien`). Fuss verlinkt die eigenen Seiten statt der heutigen Seite des Hauses. `serve.py` liefert `404.html` für unbekannte Adressen. Pflicht-Liste 9d: `website/_qa/pflicht.md`.
- **Gratis-Anreise läuft am 31.10.2026 ab:** Startseite (drei Aussagen → zwei, mittig) und Preise (Titel und Bon mittig) bleiben danach ohne Lücke; Anreise hatte es schon. Prüfen mit `?heute=2026-11-05` an jeder Adresse.
- **Zimmer:** Bei Familienzimmer und Haus Arizona lagen Fotos über Angaben und Knopf «Alle Ansichten» (1000 bis 1512 px). Text bleibt jetzt in seiner Spalte, drei Knöpfe brechen mittig um, unter 1180 px stehen die Blätter untereinander. Startseite Gastgeber: Talfoto bei 900 bis 1200 px nicht mehr über dem Text.
- **Röstihüs-Karte:** kein Name bricht mehr um (Weine als «Cuvee Special» / «… Eichenfass» mit «Hotelwein» in der kleinen Zeile, Raclette als «Raclette gross» + «mit Pellkartoffeln»), unter 1100 px eine Spalte.
- **Anfrage-Fenster** verlinkt den Datenschutz. Startseite-Kurzbeschreibung 158 Zeichen. `google-haus.json` angelegt (Strasse und Koordinaten offen). Cache-Zeichen `?v=` folgt jetzt allen Stil- und Skriptdateien.
- **Prüfwerkzeug:** Überdeckung von Text durch Fotos misst `node _qa/deckung.js <adresse> [breiten]`; geprüft 1512/1440/1280/1180/1000/920/390.
- Sicherungen: `website/_sicherung/*.vor-pflicht-2026-10-23`, `*.vor-ablauf-2026-10-23`, `*.vor-karte-2026-10-23`, `*.vor-blatt-2026-10-23`, `anfrage.js.vor-datenschutz-2026-10-23`.
- **Gemessen 23.10.** (gedrosselt, Stromsparmodus am Mac an, Rechnerlast um 9): Startseite 4× 1440 119 Bilder/s, 6× 390 111; Zimmer, Preise, Saastal, Spa, Röstihüs, Anreise je 4× 1440 und 6× 390: 120 Bilder/s, keine langen Bilder. Chromium und WebKit 1440 und 390 sowie WebKit 320 × 640 und 375 × 620 ohne Fehler und Überlauf.
- **Vor dem Hochladen offen:** Familienband-Links und Familienseite zeigen noch auf 127.0.0.1 (Karte der Kette); Tenor Sans kommt von Google Fonts (lokal nur mit Roberts Ja); `google.py setzen --adresse …`; Besuchszählung; echtes iPhone.

## Stand 24.10.2026 (Robert sieht durch, nur lokal)
- **Fotos 1:1 neu gerechnet:** 60 Fotos der Seite mit GPT Image 2.5 (Robert: «ja deutlich besser»), Fassungen und Liste in `../Familie Zurbriggen/_quelle/monte-moro/ki-2026-10-24/` (`freigabe.json`, `LIESMICH.md`, Rohfassungen in `roh/`). `website/bilder.py` nimmt jede freigegebene Fassung statt des Originals, zugeschnitten auf dessen Seitenverhältnis. Fotos mit Menschen bleiben Original. Stand der Bilder davor: `website/_sicherung/img-vor-ki-2026-10-24/`. 180,75 Guthaben (317,08 → 136,33).
- **Überleitungen mittig** mit Linie links und rechts, Knopf oder Link darunter (`bau.py › kapitel()`, CSS «Überleitungen mittig» in `bewegung.css`).
- **Zimmeransicht** statt «Alle Ansichten» auf der Zimmerseite (`bau.py › zimmeransicht()`, `steckbrief()`, `assets/js/zimmeransicht.js`); Angaben aus Website, Preisliste und Booking-Eintrag des Hauses (`inhalt/daten.py › BOOKING_ZIMMER`).
- **Dorfkarte** am Schluss des Anreise-Flugs statt der zweiten Fussspur (`website/seiten/dorfkarte.py`, Daten `../Familie Zurbriggen/_quelle/monte-moro/karte-2026-10-24/`, © OpenStreetMap im Impressum).
- **Startseite:** Speisesaal-Foto im Bon-Kapitel links bündig mit dem Frühstücksfoto.
- **Gemessen 24.10. nach den neuen Fotos:** Startseite 4× 1440 117 Bilder/s (erster Lauf bei Rechnerlast 103, wiederholt 117), 6× 390 105; Zimmer und Anreise 117–120. Ladegewicht Startseite 2965 kB statt 2413 kB. Alle sieben Seiten Chromium und WebKit 1440/390 ohne Fehler und Überlauf.
