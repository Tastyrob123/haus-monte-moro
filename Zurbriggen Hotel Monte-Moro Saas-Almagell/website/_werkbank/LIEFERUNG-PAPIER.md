---
tags: [projekt, website]
status: aktiv
---

# Lieferung Werkbank Papier · Hotel Monte-Moro (mm-werkbank-papier, 08.11.2026)

Teil Papier, Feed, Mails, Material der Werkbank. Nur lokal gebaut, nichts verschickt, nichts online, keine KI. Fakten nur aus `website/inhalt/daten.py`, `bilder.py`, den Seiten der Website und der Speisekarte im Zweig `quelle`; was in `OFFEN` steht (Öffnungszeiten des Röstihüs, Strasse, Storno, Kidsclub-Fotos …), kommt nicht vor; keine Gratis-Anreise.

## Wo (Server `python3 website/_werkbank/serve.py 9388`)

| Seite | Adresse | Stücke |
|---|---|---|
| Unterlagen | http://127.0.0.1:9388/unterlagen/index.html | 2 Karten des Röstihüs (Kartenbrett) neben den Seiten der heutigen Speisekarte (S. 4–5, S. 8) |
| Drucksachen | http://127.0.0.1:9388/drucksachen/index.html | 34 aus der Hausdruckerei (Bilder und PDF übernommen). Die 7 eigenen Fassungen (Karte am Tisch, Aushang «Inklusive», Tischkarte Hotelwein, Racletteabend, Kidsclub, Willkommensbrief, Briefpapier) fallen weg, weil die Hausdruckerei jedes Gegenstück hat (Oberchef 08.11.2026: keine Idee doppelt; `papier.py › GEGENSTUECK`) |
| Untersetzer | http://127.0.0.1:9388/untersetzer/index.html | 12 Bierdeckel fürs Röstihüs, rund 94 mm, 2 Druckbögen A3 |
| Sticker | http://127.0.0.1:9388/sticker/index.html | 24 Sticker fürs Hotel (Koffer, Skibox), rund/eckig/Kapsel/Grat, 2 Druckbögen A3 |
| Postkarten | http://127.0.0.1:9388/postkarten/index.html | 12 Postkarten A6 quer (Haus aussen und Saastal), Druck-PDF mit Beschnitt, 2 Sammelbögen SRA3, Fächer, Ständer an der Rezeption |
| Beigaben | http://127.0.0.1:9388/beigaben/index.html | 5 (Bon der Rezeption, Türhänger, Kofferanhänger, Kärtchen auf dem Kissen, Servietten fürs Röstihüs) |
| Feed | http://127.0.0.1:9388/feed/index.html | 30 neue Beiträge «Am Grat» über den 10 eigenen bisherigen; Gegenprobe `feed-bestand.md` |
| Mails | http://127.0.0.1:9388/mails/index.html | 6 (Anfrage, Angebot, Bestätigung, Vor Ihrer Anreise, Danke, Tisch im Röstihüs) |
| Material | http://127.0.0.1:9388/material/index.html | 9 Ordner (Unterlagen, Drucksachen, Untersetzer, Zeichen, Instagram, Sticker, Beigaben, Postkarten, Mails); «05 Ansichten» erscheint, sobald der Kern die Aufnahmen der Website neu gemacht hat |

## Kleid

Fjalla One (eine Stärke), Instrument Sans, DM Mono gesperrt in Versalien; feste Druckschnitte neu in `_werkbank/fonts/` (`druckschrift.py`, Prata/Hanken entfernt). Nacht, Nachtblau, Lärche (Akzent, letztes Wort), Lärche tief, Messing nur als Linie, Papier, Fassade, Creme, Wandschatten. Bergkamm als Zeichen, das ganze Logo als Wortmarke (beide aus `_werkzeuge/oberflaeche/kleid/`), Grat-Kante der Website über Fotos (Drucksachen), als Band (Postkarten), als Form (Sticker «Grat»), als Linie (Briefbogen). Karton der Vorschauen im Wandschatten (`papier_nach.py`).

## Befehle für bau_alles.sh (bitte eintragen, Teil Papier ersetzen)

Ein Schritt, der alle Teile in der richtigen Reihenfolge baut (rund 7 Minuten):

```
timeout 900 bash _werkbank/papier_alles.sh                            # Papier, Unterlagen, Sticker, Beigaben, Postkarten, Feed, Mails, Material
```

Er ersetzt in `bau_alles.sh` die Zeilen von `druckschrift.py` und den Blöcken «Papier» und «Feed, Mails, Dateien» (ohne `node "$K/ziele.js"`, das bleibt beim Kern). Reihenfolge darin (einzeln aufrufbar, jeder Python-Schritt über `_werkbank/mit_papier.py`):

1. `python3 _werkbank/druckschrift.py`
2. `mit_papier.py _werkbank/papier.py` → `node $K/papier_druck.js` → `mit_papier.py $K/papier_seiten.py`
3. `python3 _werkbank/sb_karten.py` → `mit_papier.py _werkbank/sb_karten.py . --seite` (braucht das Kartenbrett auf 9383)
4. `mit_papier.py _werkbank/sticker.py`, `… beigaben.py` → `node _werkbank/sticker_druck.js` → `… sticker.py --seite`, `… beigaben.py --seite`
5. `mit_papier.py _werkbank/postkarten.py` → `node _werkbank/postkarten_druck.js` → `… postkarten.py --seite`
6. `mit_papier.py $K/feed.py`, `node $K/feed_druck.js`, noch einmal beides (`--handy`), `python3 _werkbank/feed_leicht.py`
7. `python3 mails/_src/bau.py` → `node mails/_src/aufnahme.js`
8. `mit_papier.py _werkbank/material_mehr.py` (nach den Ansichten der Website, damit «05 Ansichten» die neuen Aufnahmen bekommt)
9. `python3 _werkbank/papier_nach.py` (Kleid und Nachbauten über alle Papier-Seiten)

Danach wie bisher der Kern-Bau (`bau.py`, `haus.nach_bau`).

## Bitte an den Kern (haus.py)

- `mit_papier.py` lädt `haus.py` und legt `_werkbank/papier_haus.json` darüber (PAPIER_SEITE, ETIKETTEN, UNTERLAGEN, MATERIAL; Werkzeugnamen als `[[karten:im]]` aus `kleid/montemoro.js`). Damit die Werkbank-Startseite dieselben Texte zeigt, bitte entweder die Werte aus `papier_haus.json` in haus.py übernehmen oder am Ende von haus.py `import mit_papier; mit_papier.anwenden(sys.modules[__name__])` aufrufen. Solange haus.py nicht lädt (heute: Pfade und Bilder der Vorlage), baut `mit_papier.py` im Notlauf mit den Grundwerten des Hauses (`_falls_fremd`).
- Zahlen für Kapitel «Für draussen» (aus `papier.json`, `papier_plan.json`, `papier_mehr.json`): 34 Drucksachen (alle aus der Hausdruckerei), 12 Untersetzer, 24 Sticker, 12 Postkarten, 5 Beigaben, 30 Beiträge, 6 Mails. `PAPIER['orte_d']` (in `papier_haus.json`) → `pw-roestihues-best-of-roestis`, `pw-aushang-inklusive`, `pw-willkommensbrief`; die PNG dazu liegen in `_werkbank/roh/papier/`; `orte_e` → `u01`–`u06`. Vorschaubilder: `<seite>/img/vorschau.webp`. Mails: `mails_reihe.py` (Texte im Sie, Kleid umgestellt), Feed-Bühne: `feed_buehne.py` (Polaroids 4, 6, 5, 11, 16, 20, 23, 8).
- `papier_kacheln.py` (schrieb werkbank/index.html) ist gelöscht; bitte nicht mehr aufrufen.
- Die Leiste der Unterseiten (Kit `rahmen`) zeigt den Bergkamm aus `werkbank.css` in der Farbe der Vorlage und läuft bei 390 px über («Zur Werkbank» abgeschnitten). Auf den Papier-Seiten löst das `papier_nach.py` (Bergkamm Lärche 18 px hoch, am Handy ohne Seitennamen); für Befund/Geprüft/KI bitte im Kern gleich lösen.

## Wie geprüft

- **PDFs:** alle 20 PDFs mit `pdffonts`: kein Type 3, nur Fjalla One, Instrument Sans, DM Mono (Druck). `pdftotext` der Karte gegen `daten.py` (Röstis, Cordon bleus, Preise).
- **Angesehen:** jedes Stück als Bild (Drucksachen vorne/hinten, 12 Untersetzer, 24 Sticker, 5 Beigaben, 12 Postkarten vorne + Rückseite, Fächer, Ständer, Sammelbogen, 30 Feed-Kacheln, 6 Mails), jede Seite bei 1440 und 390.
- **Feed-Bestand:** 17 Fotos gegen die 12 Bilder in `_quelle/extern/ig/`: 0 schon gepostet, 0 doppelt.
- **Texte:** kein ß, keine Du-Form, keine Wörter der Vorlage auf den Seiten (Suchlauf über den sichtbaren Text); Grep des Auftrags über die Quellen: Treffer nur in den Prüfmustern (`FREMD` in papier.py/sb_karten.py) und in `druckschrift.umstellen` (ersetzt fremde Schriften), in `feed-bestand.md` die Gegenprobe gegen die Feeds der Vorlagen.
- **Tor:** siehe unten.

## Tor (tor-schnell, Chromium, 1440/1280/1000/390)

`node _Werkzeuge/abnahme-tor/tor-schnell.js _Werkzeuge/abnahme-tor/ziele-monte-moro.json aus --nur <k> --max 40 --tiefe 2 --breiten 1440,1280,1000,390 --browser chromium`

| Ziel | Zustände | Funde (1440/1280/1000/390) |
|---|---|---|
| werkbank-unterlagen | 2 | 0 |
| werkbank-drucksachen | 1 | 0 |
| werkbank-untersetzer | 1 | 0 |
| werkbank-sticker | 1 | 0 |
| werkbank-postkarten | 1 | 0 |
| werkbank-beigaben | 1 | 0 |
| werkbank-feed | 2 | 0 |
| werkbank-mails | 1 | 0 |
| werkbank-material | 1 | 0 |

Behoben auf dem Weg: «Zur Werkbank» in der Leiste bei 390 abgeschnitten (Unterlagen, Drucksachen; jetzt `papier_nach.py`), «Monte-Moro» allein in der letzten Zeile der Mail-Köpfe bei 1000 (geschützter Bindestrich, `text-wrap:balance`). Messlauf (`messlauf.js … --browser chromium --groesse 1440,390`) für unterlagen, drucksachen, untersetzer, feed, mails (7 Zustände), material: je 0 Funde. Auge: Auslage der Drucksachen, Untersetzer und Sticker auf der Nacht nur mit hellen Stücken (keine Nacht auf Nacht, Kriterium 29), ohne Überdeckung. WebKit ist in dieser Sitzung nicht installiert, nicht geprüft.

## Offen

- **Kern (haus.py) noch auf dem Stand der Vorlage:** bis 11:00 unverändert (09:56). Die Papier-Seiten sind im Notlauf von `mit_papier.py` gebaut; Rahmen, Leiste und `werkbank.css` kommen aus dem Kit mit den Grundwerten des Hauses. Sobald haus.py steht: `bash _werkbank/papier_alles.sh` noch einmal (rund 7 Minuten), damit Rahmen und Fuss die endgültigen Werte tragen.
- **Unterlagen:** nur die Karten des Röstihüs haben eine heutige Fassung (Speisekarte); Preisliste, Zuschläge und Spa aus dem Kartenbrett haben keine heutige Fassung als Blatt und stehen deshalb nicht in den Unterlagen. Die Ideen kommen aus dem Kartenbrett, das noch gebaut wird; ein neuer Lauf holt seinen letzten Stand.
- **Material «05 Ansichten der neuen Website»:** erscheint, sobald der Kern die Aufnahmen der Website neu macht (ältere Aufnahmen der Vorlage nimmt `material_mehr.py` nicht).
- **Profilbild Instagram:** im Material des Hauses gibt es keines; das Profil zeigt den Bergkamm (Kit).
- **Berichtigt aus der Quelle (für die Liste an Robert):** «Mozzarella , Salami» → «Mozzarella, Salami», «Olma-Bratwurst , Zwiebelringen» → ohne Leerzeichen vor dem Komma, «Syrah,Merlot» → «Syrah, Merlot», Komma am Ende der Trauben des Eichenfass-Weins weg (nur in den Drucksachen; Wortlaut sonst wie `daten.py`).
- WebKit nicht geprüft (in dieser Sitzung nicht installierbar).
