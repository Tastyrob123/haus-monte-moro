---
tags: [projekt, website]
status: aktiv
---

# Hotel Monte-Moro, Saas-Almagell · Werkzeuge, Werkbank, Drucksachen, Prüfung — gemeinsamer Auftrag (Oberchef, 08.11.2026)

Robert, 08.11.2026 (`AUFTRAG.md`, `CLAUDE.md` «Der Deal»): «Bitte eine Cloud-Sitzung starten, in der wir einmal die komplette Werkbank und die Werkzeuge alle bis ins Detail ausarbeiten und fertig machen.» «Fertig» heisst: Robert öffnet den Link und könnte das Paket so an Esther und Fabian schicken. **Nichts neu erfinden: kopieren, umkleiden, Hauswerte eintragen.**

Vorlage dieser Datei: `Walk on the Wild Side Hannover/_werkzeuge/AUFTRAG-GEMEINSAM.md` (31.10.2026), Hauswerte getauscht. **Stamm:** die sieben Werkzeuge und die Werkbank des Culinarium Hannover (`/tmp/culinarium/Culinarium Hannover/_werkzeuge/`, `.../website/_werkbank/`), über Wild Side schon einmal umgekleidet (`/tmp/wildside/Walk on the Wild Side Hannover/`, dort ist alles Haus-Eigene in `kleid/*.{js,css}` und `--wo-*` gebündelt). Der Oberchef hat den Wild-Side-Stand nach `_werkzeuge/` und `website/_werkbank/` kopiert (ohne Prüfordner und Sicherungen), überall `wildside` → `montemoro` und die Ports 928x → 938x getauscht, und das gemeinsame Kleid `_werkzeuge/oberflaeche/kleid/montemoro.{js,css}` + `montemoro-zeichen.svg` (Bergkamm) + `montemoro-marke.svg` (ganzes Logo) angelegt. **Inhalt und Texte sind noch die der Bar Wild Side: alles davon muss raus.**

## Das Haus in drei Zeilen

Hotel Monte-Moro mit Restaurant **Röstihüs**, Saas-Almagell im Saastal (Wallis, Schweiz), 3 Sterne, 18 Zimmer / 55 Betten, Familie Zurbriggen; Gastgeber **Esther und Fabian Zurbriggen** (dieselben wie im Wellness & Spa Pirmin Zurbriggen, dessen Spa die Gäste im Partnerhotel nutzen). Satz des Hauses: «Mehr erleben, weniger zahlen.» Zimmer mit Frühstück ab CHF 90.00 pro Person/Tag, Halbpension (4-Gänge) mit wöchentlichem Racletteabend im Stübli; inklusive Postautos im ganzen Saastal und (Sommer) aller Bergbahnen ausser Metro Alpin; Kidsclub Mo–Sa 16:30–21:00. Röstihüs: elf Röstis, fünf Cordon bleus, zwei Hotelweine «von Fabian selber kreiert», Sonnenterrasse. Dazu Ferienwohnungen Haus Apollo und Haus Arizona, Zimmer in der Residence Alpenhof.

Für die Werkzeuge heisst das (Aufbau und Funktionen aus dem Stamm bleiben, Inhalt kommt aus diesem Haus):
- **Karten** = Röstihüs-Karte (Röstis, Cordon bleus, Hotelweine, Spritz, Monte-Moro-Kopf, Raclette) und die Preislisten des Hotels (Zimmer mit Frühstück/Halbpension, Zuschläge, Kinder, Spa-Tarife).
- **Anfragen/Buchen** = Zimmer anfragen (Datum, Gäste, Zimmerart) und Tisch im Röstihüs; Buchung läuft heute über seekda (`HAUS.buchen`), Tisch über TheFork (`HAUS.tisch`).
- **Drucksachen** = was ein Hotel mit Restaurant druckt: Röstihüs-Karte, Preisliste/Aushang «Inklusive», Racletteabend, Kidsclub, Willkommensbrief im Zimmer, Tischkarte Hotelwein, Briefpapier, Gutschein, Beiträge. In der Sprache der Website (Fjalla One, Bergkamm, Grat-Kante, Papier auf Nacht).
- **Gäste-Chat (Rezeption)** = Fragen zu Zimmern, Preisen, Inklusive, Anreise (Zug/Postauto, Auto), Kidsclub, Spa, Röstihüs, Hund, Euro. Wissen: `website/assets/js/wissen.json` (vom Website-Bau aus `daten.py` erzeugt).

## Wer was macht (je Agent genau ein Revier)

| Agent | Werkzeug (Name) | Revier (nur hier schreiben) | Port | Schlüssel im Tor |
|---|---|---|---|---|
| mm-maison | Das Hotelbüro (Zentrale) | `_werkzeuge/maison/` **und** `_werkzeuge/oberflaeche/` (einziger Schreiber) | 9381 | `hotelbuero` |
| mm-bureau | Das Schaufenster (Website pflegen) | `_werkzeuge/bureau/` | 9382 | `schaufenster`, `schaufenster-anleitung` |
| mm-carte | Das Kartenbrett (Karten und Preislisten) | `_werkzeuge/carte/` | 9383 | `kartenbrett`, `kartenbrett-anleitung` |
| mm-reception | Die Rezeption (Gästen antworten) | `_werkzeuge/reception/` | 9384 | `rezeption`, `rezeption-anleitung` |
| mm-livre | Das Markenbuch (Marke und Bilder) | `_werkzeuge/livre/` | 9385 | `markenbuch`, `markenbuch-buch`, `markenbuch-anleitung` |
| mm-registre | Die Besucherliste (Besuche) | `_werkzeuge/registre/` | 9386 | `besucherliste`, `besucherliste-anleitung` |
| mm-imprimerie | Die Hausdruckerei (Drucksachen) | `_werkzeuge/imprimerie/` | 9387 | `hausdruckerei`, `hausdruckerei-mail` |
| mm-werkbank | Die Werkbank | `website/_werkbank/` | 9388 | `werkbank*` |

Oberchef: Ziellisten `_Werkzeuge/abnahme-tor/ziele-monte-moro.json`, `_Werkzeuge/messlauf/ziele-monte-moro.json`, `cloud/`, Pushes, Paketprüfung. `website/` (die Website selbst) und `Familie Zurbriggen/` ändert **niemand** (nur lesen).

## Kleid: Monte-Moro, nicht Wild Side umgefärbt

Gleicher Aufbau, gleiche Wege, gleiche Funktionen wie im Stamm. Das Kleid kommt aus der Website und dem Markenbuch des Hauses (`website/assets/css/montemoro.css` `:root`, `_kette/05-markenbauer/marke/` mit `farben.json`, `markenbuch.html`, `marke.css`):
- **Farben:** Nacht `#0A2A4A` (dunkle Fläche, Lesetext), Nachtblau `#0D3F6F`, Tiefnacht `#071B2E`, Logo-Blau `#115595`; Lärche `#C67144` (Akzent, Hauptknopf, in Titeln nur das letzte Wort), Lärche tief `#9A4F2B` (Betonung auf Hell); Messing `#B39867` nur für feine Linien; Papier `#F5F2EE`, Fassade `#E7E1DC`, Creme `#EFE9E1`, Wandschatten `#D6CCC1`; Tinte `#13263A`, Grau `#4A5D70`. Im Werkzeug nur die Variablen `--wo-*` aus `kleid/montemoro.css`, keine eigenen Hexwerte für Flächen.
- **Schrift:** Titel **Fjalla One** (eine Stärke, nie fett, nie kursiv, normale Schreibung), Lauf **Instrument Sans** 400, kleine Zeilen/Etiketten/Knöpfe **DM Mono** in Versalien gesperrt (.16–.24em), Zahlen DM Mono. Dateien `/assets/fonts/FjallaOne-400.woff2`, `/assets/fonts/InstrumentSans-normal-400_600.woff2`, `/assets/fonts/DMMono-normal-400.woff2`. Prata und Hanken (Wild Side), Fraunces und Urbanist (Culinarium) gibt es hier **nicht**: jede Stelle umstellen (auch Druck-/PDF-Satz, eingebettete Schriften, Canvas).
- **Zeichen:** der **Bergkamm** aus dem Logo (`/assets/oberflaeche/kleid/montemoro-zeichen.svg`, `currentColor`, viewBox 3483×696, breit!). **Wortmarke:** das ganze Logo «Monte Moro / Saas-Almagell» (`<svg viewBox="0 0 3483 1425"><use href="/assets/oberflaeche/kleid/montemoro-marke.svg#wm"/></svg>`, Farbe über `color`: Logo-Blau `#115595` auf Hell, Papier auf Nacht). Nie als Schrift nachbauen. Die rote Wortmarke von Wild Side, das «C» und das «x» des Culinarium dürfen nirgends mehr stehen.
- **Form (aus der Website):** Knöpfe als Pille mit Lichtkante oben, Schattenkante unten und rundem Knauf mit Pfeil (`.kn`, `.kn--laerche`, `.kn--nacht` in `montemoro.css`); Bilder mit **Grat-Oberkante** (Bergkamm-Maske `--grat-maske`), Szenen dunkel/hell im Wechsel, Blatt Papier auf dunklem Grund für Karte und Preise. Keine Einkerbungen, keine Punkt-Etiketten, keine Pillen-Reihen, kein Eckschild/Gold/Rot der Bar. Werkzeuge hell: Kopf dunkel (Nacht), Raum hell (Papier).
- **Fotos:** nur aus der Website: `website/assets/img/<schlüssel>-<s|m|l|x>.webp` (480/900/1440/2200 px breit), Register `website/inhalt/bilder.py`, Masse `website/assets/img/_masse.json`. Ausgeliefert unter `/assets/img/…`. Familienfotos nur aus `Familie Zurbriggen/`. Kein Bild der Bar.

## Hauswerte (nie abtippen, aus der Quelle lesen und gegen sie prüfen)

`website/inhalt/daten.py` (HAUS, PREISE, INKLUSIVE, ZUSCHLAEGE, KINDER, LAGE, ZIMMER_*, ROESTIS, CORDON, HOTELWEINE, SPRITZ, KOPF, RACLETTE, SPA_*, SAASTAL, NOTEN, ANREISE_*, FAMILIE, BOOKING_ZIMMER, HAUS_ZAHLEN, **OFFEN**), `website/inhalt/bilder.py`, `website/*.html` (Texte), `website/assets/js/wissen.json`, `_kette/03-sammler/fakten.json`, `_kette/04-analyst/` (Potentialanalyse), `_kette/05-markenbauer/marke/`, Kundenmaterial `_quelle/` (Verweis auf den Zweig `quelle`, Speisekarte `_quelle/website/pdf/speisekarte.pdf`). Zur Laufzeit darf kein Werkzeug etwas aus `_quelle/` laden: was gebraucht wird, ins eigene Revier kopieren.
**Was in `OFFEN` steht, gibt es nicht** (Öffnungszeiten des Röstihüs, Strasse des Hauses, Storno-/Geschäftsbedingungen, Kidsclub-Fotos …): nicht erfinden, nicht als Lücke zeigen, weglassen. Preise nie raten. Die Gratis-Anreise ist am 31.10.2026 abgelaufen: nicht mehr anbieten.

## Namen der Werkzeuge

Nur über `WO.name('<teil>')` bzw. `WO_HAUS.namen` (eine Stelle: `kleid/montemoro.js`), nie fest schreiben: **Das Hotelbüro · Das Schaufenster · Das Kartenbrett · Die Rezeption · Das Markenbuch · Die Besucherliste · Die Hausdruckerei**. Python-Seiten lesen sie aus `kleid/montemoro.js` (Regex auf `namen:`). Grammatik mit Artikel im richtigen Fall («im Kartenbrett», «in der Rezeption», «in der Hausdruckerei»). Dateien, Ordner, Ports bleiben (maison, bureau, carte …).

## Texte

Schweizer Schreibung: **ss statt ß**, «Guillemets», **Sie-Ansprache** (Gäste und Gastgeber). Jeder Satz wertet auf: Sorgfalt, der einzelne Gast, Familie, Berg; nie Masse, Abfertigung, Stückzahlen als Pointe. Wer das Haus nicht kennt, versteht jeden Satz (kein Insider-Wort ohne Erklärung). Keine Bar-, Abend-, DJ-, Plakat-, Pairing-Wörter, wo sie nicht passen.

## Feste Regeln für jeden Agenten

- Keine Fragen an Robert. Offenes in die Schlussmeldung an den Oberchef.
- Nur im eigenen Revier schreiben. `oberflaeche/` nur mm-maison; wer dort etwas braucht, löst es im eigenen CSS und nennt es in der Meldung.
- Haus-Kennung überall `montemoro` (Ordner `haeuser/montemoro`, Speicher-Schlüssel, localStorage `*-montemoro-*`). Am Ende im eigenen Revier: `grep -rIn -i "wild side\|wildside\|culinarium\|rudi\|momo\|derya\|linden\|hannover\|haasemann\|prata\|hanken\|fraunces\|urbanist\|DJ\|session\|cocktail\|negroni\|F0323F\|D8B264\|130E0D\|ß\|Beau-Rivage\|Schäfli\|Schlössli" <revier>` (ohne Bilddateien) — jeder Treffer muss gewollt sein (praktisch keiner).
- Kein Platzhalter, kein «Lorem», kein «TODO», keine leere Kachel, keine erfundenen Namen/Preise/Termine/Gästenamen ausser klar als Beispiel gekennzeichneten Probe-Anfragen im Werkzeug (Vornamen wie im Stamm sind ok, Hausdaten nie).
- Headless (Chromium, `require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright')` bzw. `require('playwright')`), eine Instanz, eigene Prozesse per PID beenden, **nie pkill/killall** auf chrome/python/node. mailto/tel nie ausführen. Nichts verschicken, nichts veröffentlichen, nichts online stellen. KI nur mit Probe-Antworten (kein `*_KI=1`, keine Schlüssel).
- **Shell:** keine Heredocs und kein `python3 -`/`node -e` mit langen eingebetteten Skripten (wartet auf Freigabe und hängt). Skripte mit dem Schreibwerkzeug als Datei anlegen (im Revier unter `_bau/` oder im Scratchpad), dann ausführen. Kein `sleep` im Vordergrund.
- Server laufen schon (`bash cloud/server.sh`, Logs `/tmp/server/<port>.log`). Nach einer Änderung an Python nur den eigenen Prozess neu starten: PID über `ss -ltnp | grep :<port>`, `kill <pid>`, dann im richtigen Ordner (siehe `cloud/haus.json`) `nohup <befehl> > /tmp/server/<port>.log 2>&1 &`.
- Git: nur das eigene Revier committen (`git add "<revier>" && git commit -m "<Werkzeug>: …"`), nie `git add -A`, **nie pushen** (pusht der Oberchef), kein Force. Schlägt der Commit wegen `index.lock` fehl: kurz warten, wiederholen. Sicherungen (`*.vor-<thema>-2026-11-08`) werden nicht eingecheckt.

## Prüfen (jedes Werkzeug gleich nach dem Bau, dann reparieren, noch einmal)

Im Stamm des Repos (`/home/user/haus-monte-moro`):
```
node _Werkzeuge/abnahme-tor/tor-schnell.js _Werkzeuge/abnahme-tor/ziele-monte-moro.json aus --nur <k> --max 40 --tiefe 2 --breiten 1440,1280,1000,390
```
(entspricht `bash cloud/schnell.sh <k>`; Chromium; WebKit ist in dieser Sitzung nicht installierbar). Ergebnis in `aus/<k>/` (Inventar, Bilder, Funde). Dazu `node _Werkzeuge/messlauf/messlauf.js _Werkzeuge/messlauf/ziele-monte-moro.json aus/mess-<k> --nur <k> --browser chromium --groesse 1440,390` für das eigene Werkzeug (siehe `_Werkzeuge/messlauf/ANLEITUNG.md`) und `node _Werkzeuge/oberflaeche_pruefen.js <adresse>` (muss BESTANDEN melden). Mindestens 15 Zustandsbilder und jedes Fundbild mit dem Read-Werkzeug ansehen (Kriterien A in `_Werkzeuge/ROBERTS-KRITERIEN.md`: nichts von Wild Side/Culinarium mehr sichtbar, Inhalt des Monte-Moro, Kleid des Hauses). Fehlalarm einer Prüfregel: nicht wegerklären, mit Beleg dem Oberchef melden. **Fertig = null offene Funde, nichts «nicht erreicht», alles im Kleid des Hauses mit Inhalt des Hauses**, `LIEFERUNG.md` im Revier (was steht, wie geprüft, offen), Commit, Meldung an den Oberchef.

## Reihenfolge

Hotelbüro, Schaufenster, Kartenbrett, Rezeption, Markenbuch, Besucherliste, Hausdruckerei laufen parallel; die Werkbank baut Rahmen und Seiten sofort und holt die Bildschirme der Werkzeuge, sobald sie fertig sind. Am Ende Prüfung über alles (Oberchef).
