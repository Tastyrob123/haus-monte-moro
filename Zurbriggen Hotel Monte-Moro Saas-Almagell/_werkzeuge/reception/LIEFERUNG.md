---
tags: [projekt, website]
status: aktiv
---

# Lieferung Die Rezeption (Gästen antworten) · Hotel Monte-Moro, Saas-Almagell (08.11.2026)

Kopie des Gästebuchs aus dem Stamm (Culinarium Hannover über Wild Side), umgebaut auf das Hotel Monte-Moro mit Restaurant Röstihüs. Gleicher Aufbau, gleiche Wege, gleiche Funktionen (Master 4.4, E01–E35). Alles Wild-Side-Eigene ist raus (Theke, Dinner, Feiern, DJ, Empore, Drinks, Duzen, Wortmarke der Bar). Nichts online, nichts verschickt, keine KI aufgerufen (Probe-Antworten, `probe_ki.py`), kein Schlüssel gelesen.

**Adresse:** http://127.0.0.1:9384/_werkzeuge/reception/ · Anleitung `anleitung.html` · Prüfung `pruefung.html`
Start aus dem Hausordner: `python3 _werkzeuge/reception/server.py 9384` (liefert die Website unter `/`, das Kleid unter `/assets/oberflaeche/`, den Chat unter `/api/gast`).

## Was steht

- **Kleid des Hauses:** Nacht, Papier, Lärche als Akzent, Messing nur als feine Linie; Fjalla One (Titel), Instrument Sans (Lauf), DM Mono (kleine Zeilen), nie fett, nie kursiv. Grundfarben der Kopie hängen an `--wo-*` aus `kleid/montemoro.css` (`studio/studio.css :root`); die übrigen festen Werte der Kopie mit `_bau/montemoro_kleid.py` in die Farbwelt des Markenbuchs gerechnet. Zeichen = Bergkamm (`zeichen-haus.svg`, `zeichen-haus-hell.svg`), Briefkopf = Logo «Monte Moro / Saas-Almagell» in Logo-Blau (`marke-haus.svg`, für Mails `marke-haus-weiss.png`), alle aus `_kette/05-markenbauer/marke/zeichen/`. Fotos nur aus `website/assets/img/` (Register `website/inhalt/bilder.py`). Namen nur über `WO.name()` / `kleid/montemoro.js`.
- **Sie-Form, Schweizer Schreibung** in Werkzeug, Anleitung, Rundgang, Chat und Briefen.
- **Eingang** mit vier Arten: Zimmer, Ferienwohnung (Haus Apollo, Haus Arizona), Tisch im Röstihüs, Nachricht. Hinweise je Anfrage aus `website/inhalt/daten.py`, nie gespeichert: Einzelzimmerzuschlag 50 %, Zuschlag 1–3 Übernachtungen CHF 5.00, Kinderzuschläge im Zimmer der Eltern und Kidsclub, Hund CHF 7.00–10.00, mehr als 6 Gäste (Familienzimmer 3–6), Preise der Ferienwohnungen und Öffnungszeiten des Röstihüs nicht veröffentlicht (persönlich klären), Allergien (Küche fragen), Gratis-Anreise abgelaufen (nicht anbieten).
- **Brief** von Esther und Fabian Zurbriggen im Ton der Website, Kopf mit dem Logo, Fuss mit Ort, Telefon und E-Mail (die Strasse ist OFFEN und steht nicht da). Vorlagen `vorlagen/zimmer.txt`, `wohnung.txt`, `tisch.txt`, gebaut von `_bau/montemoro_wissen.py` aus `daten.py`. Offene Felder wie [Zimmer prüfen], [Preis der Wohnung], [Tisch prüfen]. PDF «Hotel Monte-Moro – Name – Datum.pdf» (A4 vom Server, Messinglinie, Bergkamm auf Folgeseiten).
- **Wege zur Website wie im Stamm:** `POST /api/anfragen` (das Anfrage-Fenster der Website, `assets/js/anfrage.js`) landet sofort im Eingang (`reception.website_anfrage`, Art aus dem Betreff); was die Vorschau der Website (`:8947`) in `website/_dienste/anfragen.jsonl` ablegt, holt die Rezeption jede Minute ab (nur lesen, jede Zeile genau einmal). `POST /api/frage` legt eine Frage an den Chat unter «Das wurde gefragt» ab.
- **Chat:** antwortet ohne KI genau wie die Rezeption im Chat der Website (`gast/website_chat.py`, dieselbe Suche wie `assets/js/rezeption.js` über `assets/js/wissen.json`), ohne die abgelaufene Gratis-Anreise. Was das Haus nicht veröffentlicht (Öffnungszeiten Röstihüs, Check-in, Storno, Preise der Wohnungen, Strasse, Allergien), beantwortet er ehrlich ohne Zahl («Esther und Fabian beantworten das persönlich») und meldet es als Lücke.
- **Das weiss der Chat:** Steckbrief mit 70 belegten Zeilen in zehn Bereichen (`steckbrief_bau.py`, jeder Beleg wörtlich in `gast/gast_wissen.txt` / `gast_umgebung.txt`, jede Zahl beim Beleg geprüft).
- **Beispiele:** sieben Anfragen (Familienzimmer mit Kindern, Wochenende mit Hund, Tisch mit Gluten, Haus Arizona, Spa-Frage, Einzelzimmer auf Englisch mit deutscher Lesefassung, abgelaufene Gratis-Anreise) und zehn Fragen, zwei mit Absicht ohne Antwort (Öffnungszeiten Röstihüs, Check-in). Erfundene Gäste mit example.com bzw. 555-Nummern, als Beispiel beschriftet (`_bau/montemoro_beispiele.py` prüft jede Zahl gegen das Wissen). Nichts als nachgetragen erfunden.
- **Anleitung** mit zwölf Kapiteln auf das Haus umgeschrieben, Bilder neu (`_bau/anleitung_bilder.js` gegen einen Wegwerf-Server).
- **Baustein** `baustein/anfrage.js` + `ANLEITUNG.md`: schickt das Anfrage-Fenster auch ausserhalb der Vorschau an die Rezeption und die Chat-Fragen an `/api/frage`; auf der Website eingebaut am 09.11.2026 (`website/assets/js/rezeption-weg.js`, vor `anfrage.js`), Weg Website → Eingang und Chat → «Das wurde gefragt» geprüft.
- Speicher-Schlüssel im Browser `reception-montemoro-*`, `rundgang-montemoro-*`.

## Geprüft (08.11.2026, Chromium; WebKit hier nicht installierbar)

- `tor-schnell --nur rezeption`: 40 Zustände in 1440/1280/1000/390, `--nur rezeption-anleitung`: 11 Zustände; Ergebnis siehe Meldung, Funde repariert (Schrift-Mitte Rundgang-Knopf und Auswahlfelder, Platzhalter am Handy, Fenster-Titel unter dem Schliessen-Knopf, zerfallende Zeilen am Handy, Kennzeile ohne Doppelung).
- Messlauf `--nur rezeption,rezeption-anleitung` 1440/390: 0 Funde (der Knopf «Chat ausprobieren» im Rand trägt jetzt `aria-haspopup="dialog"`, er öffnet ein Fenster und ist kein Navigationspunkt).
- `oberflaeche_pruefen.js`: Werkzeug, Anleitung, Prüfseite BESTANDEN.
- Wege von Hand: `/api/anfragen` (Zimmer, Haus Arizona, Tisch; ohne Kontakt 422), Abholen aus einer Probe-`anfragen.jsonl` (Wegwerf-Daten), `/api/frage` mit Probe. Testeinträge gelöscht; `daten/` ist leer und füllt sich beim ersten Öffnen mit den Beispielen.
- Über 15 Zustandsbilder angesehen (Start, Eingang mit Brief, Tisch, Ferienwohnung, Gefragt, Nachtragen, Nachgetragen, Wissen in mehreren Bereichen, Eintrag, Chat ausprobieren 1440 und 390, Rundgang, Anleitung, Lesefassung Deutsch, Gestalten).

## Offen

- Nichts. Erledigt am 09.11.2026: Baustein auf der Website eingebaut und geprüft; Datenschutz bleibt im Wortlaut des Hauses, der Anfragen über Formulare abdeckt (keine erfundene Frist).
