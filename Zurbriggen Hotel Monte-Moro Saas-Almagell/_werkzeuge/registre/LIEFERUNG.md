---
tags: [projekt, website]
status: aktiv
---

# Lieferung · Besucher (Le Registre, Besuche) · Hotel Monte-Moro, Saas-Almagell

Stand 08.11.2026 (Agent «mm-registre»), lokal, nichts online, nichts verschickt.

**Werkzeug:** http://127.0.0.1:9386/_werkzeuge/registre/ (Server aus dem Hausordner: `python3 _werkzeuge/registre/server.py 9386`; Bilder ohne Tagesgruss: `?gruss=tag`)
**Anleitung:** http://127.0.0.1:9386/_werkzeuge/registre/anleitung.html (zehn Kapitel, Bilder neu aus dem Werkzeug aufgenommen)
**Stand-Weg für Kontrollpanel:** http://127.0.0.1:9386/api/registre?tage=30&beispiel=1

## Was steht

- **Aufbau und Funktionen aus dem Stamm** (Besucher der Häuser, 28.10.2026 von Robert abgenommen): acht Ansichten (Übersicht; Besuche, Herkunft, Zeit; Seiten, Verlauf, Zur Buchung; So wird gezählt), Zeitraum 7/30/90 Tage, Besuchskarte mit Weg durch die Website, «Als Tabelle sichern», Rundgang, «Zur Werkbank», Startfehler-Tür, Fehlermelder. Rechnung (registre.py / registre.js) unverändert, nur die Hauswerte getauscht.
- **Kleid des Hauses:** Rahmen aus `_werkzeuge/oberflaeche/` (Kleid `montemoro`, Bergkamm als Zeichen, `WO.name('besuche')`); eigene Teile in `registre.css`/`registre-haus.css` nur über `--wo-*`: Nacht/Nachtblau, Papier, Lärche als Akzent (erste Balken, Siegel, «Zur Buchung»), Messing nur als Linie; Fjalla One (Titel, Akzent nur auf dem letzten Wort), Instrument Sans, DM Mono (Etiketten, Zahlen). Knöpfe überall `WO.knopf`; Rundgang-Karte und «Zur Werkbank» mit Lärche- bzw. Nacht-Pille und hellem Knauf.
- **Bühnen** je Ansicht mit Fotos der Website (`/assets/img/<schlüssel>-s/-m.webp`, Alt-Text aus `inhalt/bilder.py`): Übersicht das Haus im Sommer, Besuche die Rezeption mit dem Bergkamm, Herkunft Saas-Almagell im Saastal, Zeit das Dorf am Abend, Seiten der Blick vom Balkon, Verlauf die Gletscher, Zur Buchung ein helles Doppelzimmer, So wird gezählt die Stube aus Holz. Keines ist zugleich Seitenbild.
- **Seiten der Website** (`python3 registre.py seiten`, Namen aus der Leiste der Website): Startseite, Zimmer, Preise, Saastal, Spa, Röstihüs, Anreise, Impressum und Bildnachweis, Datenschutz; je Seite ihr erstes Foto (Familienfotos ausgenommen).
- **Wege des Hauses** (Master G14, Schlüssel wie in allen Häusern): `fenster` Zimmer-Anfrage begonnen (Fenster «Anfrage») · `buchung` Zimmer angefragt (erst mit «Danke.») · `booking` «Zimmer buchen» (seekda, `HAUS.buchen`) · `tisch` Tisch-Anfrage im Röstihüs begonnen · `anfrage` Tisch im Röstihüs angefragt · `anruf` Telefon · `mail` E-Mail-Adresse · `chat` Chat der Rezeption · `route` weiter zur Familie Zurbriggen (Spa nebenan, Familienband). «Zur Buchung» = Zimmer angefragt oder «Zimmer buchen». TheFork (`HAUS.tisch`) ist auf der Website nicht verlinkt, darum zählt der Tisch über das Anfrage-Fenster.
- **Beispielwerte**, überall als Beispiel beschriftet (Band, Leiste, Kopf, CSV-Name): Deutschschweiz und Wallis, Romandie, Tessin, Süddeutschland, Norditalien, wenige von weiter her; Herkunft Google, Booking.com, Schweiz Tourismus, Saas-Fee/Saastal, Instagram, Tripadvisor; Uhrzeit Europe/Zurich, Zahlen in Schweizer Schreibung. Keine Hausangaben erfunden.
- **Eigene Zählung des Hauses** (Master G09): eigener Schlüssel, in der Cloud-Sitzung erzeugt unter `/home/user/_Schluessel/monte-moro-registre.txt` (nicht eingecheckt; Prüfsumme in `anschluss.py` und `online/registre.py`), eigenes Geheimnis, eigener Speicher. Vorführ-Betrieb an: der Kunde sieht nur Beispielwerte.
- **Zählung für die Website liegt bereit, ist nicht eingebaut:** `vorschlag/messung.js` (Anfrage-Fenster `dialog.anf`, «Zimmer buchen», `tel:`, `mailto:`, `[data-chat-auf]`, Familienband, Spa-Link) und `vorschlag/datenschutz-text.md` (DSG/DSGVO, Sie-Form). Einbau nur auf Roberts Wort.
- Nicht mehr im Revier: der Volllauf `abnahme.js` und die daraus erzeugte `FUNKTIONSLISTE.md` der Bar (liefen nur an einer Probe-Kopie auf dem Mac gegen die Formulare der Bar). Hilfsskripte des Baus in `_bau/` (Bildschirmfotos, Messung, Fassungen `?v=`, Farbtabelle).

## Wie geprüft (08.11.2026, Chromium)

- `tor-schnell` `--nur besucherliste` (40 Zustände) und `--nur besucherliste-anleitung` (15 Zustände), 1440/1280/1000/390, nichts «nicht erreicht». Gefunden und behoben: Rundgang-Karte «Überspringen» 3 px neben der Kante, «Bildnachweis» allein in der letzten Zeile, Filter-Wahlen am Handy 0,9 px zu tief.
- Übrig nur Regel 12 «Versalien» (48–75 je Breite): Fehlalarm, siehe unten. Mit derselben Zielliste ohne das fremde Stilblatt (Rückfall-Regel der Liste «Versalien nur in Mono») ist der Lauf bei 0 Funden.
- Messlauf (`--nur besucherliste` 53 Zustände, `--nur besucherliste-anleitung` 9 Zustände, je 1440 und 390): 0 Funde.
- `oberflaeche_pruefen.js` Werkzeug und Anleitung: BESTANDEN (vorher behoben: viermal dasselbe Seitenbild in «Zuletzt zu Besuch» – die Besuchskarte zeigt jetzt die erste Seite nach der Startseite; «10» lose im Anleitungs-Titel – jetzt «Zehn Kapitel»).
- Mit dem Auge (Read): Startbild, Rundgang, alle acht Ansichten bei 1440, Besuche/Zur Buchung/Start bei 390, Zeit bei 1000, Besuchskarten, Anleitung und ihre Bilder: kein Wild-Side-Rest, Inhalt und Kleid des Monte-Moro.

## Offen (für den Oberchef)

- **Regel 12 (Stilblatt) Fehlalarm:** `ziele-monte-moro.json › stilblatt` zeigt auf `_werkzeuge/imprimerie/haeuser/montemoro/stilblatt.json`, das noch das Stilblatt der Bar ist (Versalien nur «Hanken», «Rammetto One» …, Quellen `wild.css`, SESSION-Plakate). Das Markenbuch des Monte-Moro will Etiketten in DM Mono, Versalien gesperrt. Sobald mm-imprimerie das Stilblatt umstellt (oder die Liste ohne es läuft), fallen alle Funde weg.
- Im Vollbild-Foto (Playwright `fullPage`) springen die Einträge im Rand während der Bewegung aus `bewegung.js` (Kleid); im Fenster und in allen Tor-Bildern stehen sie richtig.
