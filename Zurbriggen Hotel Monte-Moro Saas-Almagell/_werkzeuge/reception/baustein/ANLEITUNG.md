---
tags: [projekt, website]
status: aktiv
---

# Baustein: Anfrage-Fenster und Chat der Website → Rezeption · Hotel Monte-Moro

Gebaut am 08.11.2026 vom Chat `mm-reception` (Werkzeug «Die Rezeption»), Muster: Baustein des Culinarium Hannover. Auf der Website ist **nichts** eingebaut; das macht der Website-Bau (Revier `website/`), sobald der Oberchef es freigibt.

## Was heute schon geht (ohne Baustein)

- Das Anfrage-Fenster der Website (`website/assets/js/anfrage.js`, «Anfrage senden») schickt `POST /api/anfragen` mit Betreff, Art, Tag, Uhrzeit, Personen, Nachricht, Name, Kontakt, Seite. Auf dem Server der Rezeption (`:9384`) landet das sofort im Eingang (`reception.website_anfrage`: Art aus dem Betreff, z. B. «Haus Apollo» → Ferienwohnung, «Tisch im Röstihüs» → Tisch).
- Auf der Vorschau der Website (`website/serve.py`, `:8947`) legt `anfrage.js` die Anfrage in `website/_dienste/anfragen.jsonl` ab. Die Rezeption sieht jede Minute dort nach (nur lesen) und übernimmt jede Zeile genau einmal in den Eingang.
- Ausserhalb von `:8947` legt `anfrage.js` nichts ab (Designstudie). Das schliesst dieser Baustein.

## Was der Baustein tut

- Fängt «Anfrage senden» im Fang-Durchlauf am Dokument ab und schickt dieselben Angaben an `data-api` (Standard `/api/anfragen`). `anfrage.js` bleibt unverändert und zeigt seinen Dank wie bisher.
- Schickt jede Frage an die Rezeption im Chat (Eingabe und Vorschläge) an `/api/frage`. Der Server antwortet gleich wie `rezeption.js` (`gast/website_chat.py` über `assets/js/wissen.json`) und legt Frage und Antwort unter «Das wurde gefragt» ab; Mail-Adressen und Nummern werden abgedeckt. Lücken (zum Beispiel Check-in, Öffnungszeiten des Röstihüs) erscheinen dort als «ohne Antwort» zum Nachtragen.
- Nie `mailto:`, nie ein Mailprogramm, nichts an Dritte.

## Einbauen (Website-Bau, über `bau.py`)

1. `_werkzeuge/reception/baustein/anfrage.js` nach `website/assets/js/rezeption-weg.js` kopieren.
2. Auf jeder Seite **vor** `anfrage.js` und `rezeption.js` einhängen: `<script src="assets/js/rezeption-weg.js?v={VERSION}" defer></script>`.
3. Läuft die Website auf einem anderen Server als die Rezeption, `data-api` und `data-frage` mit voller Adresse setzen **und** eine Weiterleitung einrichten, weil die Rezeption nur Aufrufe von der eigenen Seite annimmt (Herkunft 403).
4. Datenschutz: die Datenschutzerklärung muss dann sagen, dass Anfragen und Chat-Fragen bei der Rezeption des Hauses liegen und nach zwölf Monaten gelöscht werden, auf Wunsch sofort. Vom Haus zu prüfen.

## Geprüft

Am 08.11.2026 auf dem Server der Rezeption: `POST /api/anfragen` mit den Feldern von `anfrage.js` (Zimmer, Haus Arizona, Tisch) liegt im Eingang mit Art, Seite und Hinweisen; ohne Kontakt antwortet der Server 422 «Bitte E-Mail oder Telefon angeben». `POST /api/frage` legt die Frage ab (mit `probe: true` nicht). Testeinträge wieder gelöscht.
