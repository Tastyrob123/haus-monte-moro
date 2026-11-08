---
tags: [projekt, website]
status: aktiv
---

# Das Schaufenster (Website pflegen, Arbeitsname Le Bureau) · Hotel Monte-Moro, Saas-Almagell · Lieferung

**Stand: 08.11.2026, in der Cloud gebaut und geprüft (Bau-Agent mm-bureau). Nichts online, nichts verschickt, die Website (`website/`) wird nie geschrieben.** Vorlage: der Stamm der sieben Werkzeuge (Schreibtisch `_Werkzeuge/werkzeuge/website/` im Rahmen des Hauses), kopiert, umgekleidet, Hauswerte aus der gebauten Website gelesen.

## Wo

- **Werkzeug:** http://127.0.0.1:9382/_werkzeuge/bureau/ · Server `python3 _werkzeuge/bureau/serve.py 9382` im Hausordner (Prüfläufe mit `BUREAU_PRUEFLAUF=1`, sonst Grenze 900 Abfragen je Minute).
- **Anleitung:** http://127.0.0.1:9382/_werkzeuge/bureau/anleitung.html (neun Schritte, acht Bilder neu aufgenommen am 08.11.2026 aus dem Werkzeug des Monte-Moro)
- **Prüfseite:** http://127.0.0.1:9382/werkzeuge/website/pruefung.html?haus=montemoro (alle Punkte grün: 9 Seiten, Kopie, Stand, Byte für Byte, Bereiche Zimmer 4 / Preisliste 14 / Inklusive 6, Zeiten und Preise)
- **Rundgang:** http://127.0.0.1:9382/_werkzeuge/bureau/?rundgang
- **Stand-Weg für das Hotelbüro:** `GET /_werkzeuge/bureau/api/ueberblick` → `{aenderungen, zuletzt, bereiche, seiten}`
- **Website, wie «online» wäre (Probe-Kopie):** http://127.0.0.1:9382/werkzeuge/website/_probe/montemoro/online/index.html

## Was steht

| Teil | Was |
|---|---|
| `beschreibung.py` | Beschreibung des Hotels für den Schreibtisch des Stamms, **nie von Hand**: 9 Seiten aus dem Menü der gebauten Website (Startseite, Zimmer, Preise, Saastal, Spa, Röstihüs, Anreise) und aus dem Fuss (Impressum, Datenschutz); 8 Bereiche mit Foto der Website (Foto wird geprüft: es muss auf der Seite stehen); Angaben aus dem Fuss von `index.html` (Telefon mit Link zum Anrufen, E-Mail mit Link zum Schreiben, PLZ und Ort; eine Strasse ist offen und erscheint nicht); Listen des Hauses unter «Das Haus»: **Zimmer und Wohnungen** (Hotelzimmer, Familienzimmer/Residence Alpenhof, Haus Apollo, Haus Arizona mit Name, Zeile, Text, Angaben, Fotos), **Preisliste** (Zimmer mit Frühstück/Halbpension, Zuschläge, Kinder: 14 Zeilen), **Inklusive** (6 Zeilen des Bons); Zeiten & Preise mit den Schreibweisen des Hauses («CHF 90.00», «25.–», «7 dl», «50 %»), jeder Treffer mit Ziffer; Google-Texte; eigenes Foto hochladen nach `assets/img`. Der Server ruft `anlegen()` beim Start: `_Werkzeuge/haeuser/montemoro/haus.json`, `_Werkzeuge/werkzeuge/website/haeuser/montemoro.json` und die Probe-Kopie `_probe/montemoro/` entstehen so auch auf einem frischen Rechner. |
| Gesperrt (Karten) | Die Karte des Röstihüs (Röstis, Cordon bleus, Hotelweine) auf `roestihues.html` (`#karte .rk`, `#stube .bl__zeilen`) und `index.html` (`#roestihues .buch`, `#wein .wein__glaeser`) ist gesperrt, mit Weg ins Kartenbrett (eine Quelle für Karte und PDF). |
| Ausgelassen | Die Gratis-Anreise (am 31.10.2026 abgelaufen, die Website blendet alles mit `data-bis` aus) erscheint nirgends im Werkzeug und wird nicht angeboten; dazu das Familienband (gehört der Familie), Zeichen als SVG und das Fenster der Rezeption (Gäste-Chat). |
| Rahmen (`index.html`, `bureau.css`, `festigkeit.js`, `fehlermelder.js`, `rundgang.js`, `zur-werkbank.js`, `schweben.*`, `anleitung.*`, `pruefung-haus.*`, `bau.py`) | Kennung `montemoro`, Kleid nur aus `kleid/montemoro.{js,css}` und `--wo-*`, Schriften Fjalla One / Instrument Sans / DM Mono, Namen nur über `WO.name()` bzw. `WO_HAUS.namen`, Sie-Form. Rundgang fünf Schritte (Werkzeug, Zimmer/Preise/Inklusive, Bereiche, Angaben, Entwurf). «Zur Werkbank» im Knopf «kn--nacht» der Website (Pille Nacht, heller Knauf, DM Mono). Anleitung mit Bergkamm im Kopf. Fassungsnummern aus dem Inhalt (`bau.py`). |
| `serve.py` | Rahmen um den Server des Stamms: Seite, `/assets/oberflaeche/`, `/assets/` aus `website/assets/` (nur gelesen), Prüfseite im Kleid, Sicherheit S01–S03, Stand-Weg. Alles Fremde (DJ-Abende, Gastschichten, Du-Anrede, Fotostufen-Umleitung, Weindaten) ist entfernt. |
| `festigkeit.js` | Kleine Nachbesserungen am Werkzeug des Stamms, ohne dessen Dateien zu ändern: Kacheltitel ohne Einzelwort, «Ändern» als Zeichen, Bildtitel ganz, kein «×» als Zählzeichen, lange Werte als umbrechende Felder, schärfere Kachelfotos (-m statt -s), Wörter des Stamms, die es beim Hotel nicht gibt («Öffnungszeit», «Adresse» → «Uhrzeit», «E-Mail»), Preise «90.00» statt «90 .00» in den Listen. |
| Entfernt | `termine.py`, `termine-ansicht.js`, `gaeste.py`, `gaeste-ansicht.js`, das Bild `anleitung/termine.webp`: DJ-Abende und Gastschichten haben beim Hotel kein Gegenstück (keine Liste von Terminen auf der Website). |

## Wie geprüft

- **Schnelle Prüfung** (`tor-schnell.js`, Chromium, höchstens 40 Zustände, Tiefe 2, 1440/1280/1000/390), letzter Lauf 08.11.2026: `schaufenster` 40 Zustände, **0 Funde**, nichts «nicht erreicht», keine Skriptfehler; `schaufenster-anleitung` 21 Zustände, **0 Funde**, nichts «nicht erreicht». Ergebnis in `aus/schaufenster/`, `aus/schaufenster-anleitung/`. Repariert auf dem Weg: Gruppe «Rezeption … ×» (Gäste-Chat der Seite, jetzt ausgelassen), Einzelwort-Funde in den Listen des Hauses (Zeile über dem Namen als eigener Absatz), zerfallende Namen bei 1000 px (zwei Einträge je Reihe), «Ausblenden: …» ohne Luft im Knopf, Gruppenname mit den Ziffernwalzen «0 1 2 … 9» (Zählwerk ausgelassen), «CHF» allein als Angabe.
- **Messlauf** (`messlauf.js`, Chromium, 1440 und 390): `schaufenster` 75 und 89 Zustände, **0 Funde**; `schaufenster-anleitung` **0 Funde**. Repariert: «inkl.» 1 px zu tief (Kriterium 35), zwei Wege ins Kartenbrett (Kopf und Rand, Kriterium 15: der Rand-Eintrag fällt weg).
- **Oberfläche:** `node _Werkzeuge/oberflaeche_pruefen.js http://127.0.0.1:9382/_werkzeuge/bureau/` → BESTANDEN.
- **Prüfseite** des Werkzeugs: alle Punkte grün.
- **Auge:** Übersicht, Bereiche, Zimmer und Wohnungen, Preisliste, Inklusive, Zeiten & Preise, Angaben, Foto tauschen, Google-Texte, Entwurf, Frühere Fassungen, Prüfseite, Anleitung bei 1440/1000/390 angesehen.

## Offen

- **Dateien des Stamms:** `_Werkzeuge/haeuser/montemoro/haus.json` und `_Werkzeuge/werkzeuge/website/haeuser/montemoro.json` liegen ausserhalb des Reviers (Oberchef checkt sie ein); der Server schreibt sie beim Start nur neu, wenn `beschreibung.py` etwas anderes ergibt. Die Probe-Kopie `_probe/montemoro/` ist nicht in Git und entsteht beim Start.
- **Neue Einträge:** Ein Zimmer oder eine Preiszeile lässt sich ändern und ausblenden, nicht neu anlegen (Grenze des Stamms; neu entsteht mit dem nächsten Bau der Website).
- **Online:** nur lokal; Veröffentlichen schreibt in die Probe-Kopie, nie in `website/`.
