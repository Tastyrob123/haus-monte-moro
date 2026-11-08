---
tags: [projekt, website]
status: aktiv
---

# Lieferung Werkbank Kern · Hotel Monte-Moro (mm-werkbank-kern, 08.11.2026)

Teil Kern der Werkbank: Startseite «Alles auf einen Blick», Befund, KI-Seite, Karte «Ein Vorschlag.» mit PDF, Prüfbericht, Impressum. Papier, Drucksachen, Untersetzer, Sticker, Postkarten, Beigaben, Feed, Mails und Dateien: `LIEFERUNG-PAPIER.md` (mm-werkbank-papier). Nur lokal gebaut, nichts verschickt, nichts online, keine KI aufgerufen.

## Wo (Server `python3 website/_werkbank/serve.py 9388`)

| Seite | Adresse |
|---|---|
| Startseite | http://127.0.0.1:9388/werkbank/index.html |
| Befund (alle zwölf Punkte) | http://127.0.0.1:9388/befund/index.html |
| KI und Ihre Daten | http://127.0.0.1:9388/werkbank/ki.html |
| Ein Vorschlag. | http://127.0.0.1:9388/werkbank/karte.html · PDF http://127.0.0.1:9388/werkbank/vorschlag-montemoro.pdf |
| Prüfbericht | http://127.0.0.1:9388/werkbank/geprueft/index.html |
| Impressum (Tasty Studios) | http://127.0.0.1:9388/werkbank/impressum.html |

Bau: `bash website/_werkbank/bau_alles.sh` (mit Aufnahmen der Website und der Werkzeuge) oder `--ohne-aufnahmen`. Der Teil Papier läuft darin als `bash _werkbank/papier_alles.sh`. Kit unverändert (`_Werkbank-Kit/`), Inhalt in `_werkbank/haus.py` (Texte der Papier-Seiten über `mit_papier.py` aus `papier_haus.json`).

## Was steht

Aufbau, Wege und Funktionen aus dem Stamm (Auftakt, Brief, Worum es geht, Inhalt, acht Kapitel, Schluss, Fuss «Das Wichtigste vom Monte-Moro»), Inhalt und Kleid des Monte-Moro:

- **Kleid:** Nacht, Nachtblau, Tiefnacht, Logo-Blau, Lärche (Akzent, letztes Wort der Titel), Lärche tief auf Hell, Messing nur als Linie, Papier; Fjalla One nur für Titel, Instrument Sans zum Lesen, DM Mono für kleine Zeilen und Zahlen; der Bergkamm als einziges Zeichen (aus `kleid/montemoro-zeichen.svg`), das ganze Logo als Wortmarke; die Tapete des Markenbuchs (Grate) auf den Flächen; Knöpfe wie `.kn--laerche`/`.kn--nacht` der Website. Kein «C», kein «x», keine rote Wortmarke, keine Schrift der Vorlagen (`kleid_haus.py`, `sb_farbe.py`).
- **Auftakt** «Mehr erleben im Saastal.» für Esther und Fabian Zurbriggen, Rechner und Handy mit der neuen Startseite, drei Fotos des Hauses.
- **Brief** «Liebe Frau Zurbriggen, lieber Herr Zurbriggen» im Sie, Schweizer Schreibung; Preis ab CHF 90.00, Inklusive und Racletteabend aus `daten.py`; kein Geschenk, Bitte um ein Gespräch; «Meine drei Orte» als Ticket aus dem Kit.
- **Worum es geht** «Direkt gebucht, bleibt mehr im Haus.»: Rechner Direktbuchung statt Portal. Belegt nur der Preis CHF 90.00 (Budgetzimmer mit Frühstück, `daten.PREISE`); Übernachtungen (600), Provision (15 %) und Anteil (25 %) sind als Annahme beschriftet und überschreibbar.
- **I Befund** «Viel zu bieten, wenig zu sehen.»: die ersten vier Punkte der Potentialanalyse (`_kette/04-analyst/potential.json`, Stand 17.10.2026) mit der heutigen Seite im Blender-Gerät und dem Ausschnitt, von dem der Satz spricht; alle zwölf Punkte, was stark ist und was sonst auffällt auf `befund/`.
- **II Ihre Marke:** Logo in Papier auf Nacht, drei Schriften mit Rolle, neun Töne aus `farben.json` (Markenbuch), Herkunft an vier Fotos gemessen, Tapete, Knöpfe; Weg ins Markenbuch.
- **III Ihre Website:** heute (Aufnahme der Startseite von monte-moro.ch, 17.10.2026) neben neu, zwölf Ideen (Sätze gegen die Aufnahmen gelesen), Gefüge, alle Seiten mit Handy, «Bevor der Gast ankommt» (Buchen, Zimmeransicht, Anfrage, Chat der Rezeption, Inklusive, Anreise).
- **IV Karten:** Röstihüs und Weinkarte aus dem Kartenbrett (Teil Papier).
- **V Ihre Werkzeuge:** alle sieben im Laptop mit Namen aus `kleid/montemoro.js` (Hotelbüro, Schaufenster, Kartenbrett, Rezeption, Markenbuch, Besucherliste, Hausdruckerei), Klick bedient das echte Werkzeug; «Einmal ändern, überall richtig.» mit sechs Szenen.
- **VI Für draussen** (Teil Papier), **VII Geprüft** mit Prüfbericht, **VIII Das Angebot** «Ein Vorschlag für das Monte-Moro.»: Vorschlag, was Sie bekommen, Ihre Daten, so geht es weiter, Betreuung freiwillig; Karte «Ein Vorschlag.» + PDF ohne jeden Preis (`pdftotext`: nur das Datum als Zahl); KI-Seite mit drei Stellen (Rezeption im Chat, Antwortentwurf, Markenprüfung), ohne Betrag.
- **Schluss** «Und morgen scheint die Sonne wieder.» mit Gruss, Unterschrift und Ticket.

## Wie geprüft

- **Abnahme-Tor** (`tor-schnell`, Chromium, 1440/1280/1000/390): siehe Tabelle unten.
- **Oberflächen-Prüfung** `node _Werkzeuge/oberflaeche_pruefen.js http://127.0.0.1:9388/werkbank/index.html`: Punkte 1–5 und 7 ohne Fund. Punkt 6 («Laufband») meldet das Ideen- und das Gästeband: gemessen wird dort die Ziffer «01» im Bild der ersten Karte (`span.idee__n`), die Bänder sind Bildbänder zum Blättern, kein Laufband. Beleg: `band.js` (Scratchpad) gibt das gemessene Element aus. Vorschlag an den Oberchef: Regel 6 nur für Bänder mit Bewegung (Animation) oder `data-laufband`.
- **Angesehen:** jeder Abschnitt der Startseite bei 1440 und 390, Befund, KI, Karte, Prüfbericht bei 1440; alle Aufnahmen der Ideen, der Gäste-Funktionen und der sieben Werkzeuge.
- **Texte:** Suchlauf `python3 _werkbank/du_gang.py` (ß, Du/Ihr-Form, Wörter der Vorlagen) über alle Seiten des Kerns; Werkzeugnamen nur aus `kleid/montemoro.js`.
- **PDF:** `pdffonts` nur Fjalla One, Instrument Sans, DM Mono (eingebettet, kein Type 3).

## Offen

- Bildschirme der Werkzeuge: aufgenommen mit dem Stand vom 08.11.2026 mittags; Schaufenster, Rezeption und Hausdruckerei waren da noch in Arbeit. Neu aufnehmen mit `node _werkbank/sb_werkzeuge.js`, dann `bash bau_alles.sh --ohne-aufnahmen`.
- Prüfbericht: die Zahl der geprüften Zustände je Werkzeug steht erst, wenn alle sieben fertig gemeldet sind (`_werkbank/pruef_werkzeuge.json`).
