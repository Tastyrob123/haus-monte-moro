---
tags: [projekt, website]
status: aktiv
---

# Kontrollpanel (La Maison) · Hotel Monte-Moro, Saas-Almagell · Funktionsliste (08.11.2026)

Master Werkzeug-Bau 3 (R01–R24) und 4.1 (M01–M27). Vorlage: die abgenommene Zentrale des Stamms (28.–30.10.2026, über Wild Side 31.10.2026), kopiert, umgekleidet, Hauswerte eingetragen; Aufbau, Wege und Funktionen unverändert. Beleg je Zeile: schnelle Prüfung (`_Werkzeuge/abnahme-tor/tor-schnell.js … --nur hotelbuero`, Chromium, 1440/1280/1000/390), Messlauf, `oberflaeche_pruefen.js`, Bau-Ausgabe von `bau.py`, Augenprüfung der Bilder.

## Rahmen (R) — Kontrollpanel ändert nichts, R08–R14 betreffen es nicht

| Nr | Stand | Beleg |
|---|---|---|
| R01 Aufbau | Leiste, Empfang, Säle, Fuss, Startfehler-Tür, `aria-live` | `bau.py seite()` |
| R02 Auftakt | Fenster in der Motivfarbe sofort da, Fotos blenden nach dem Laden ein, kein Vorhang | Bilder |
| R03 Fehlermelder | `fehler.js` vor allem anderen, Schlüssel `montemoro_werkzeuge_fehler`, max. 20, Netzfehler nie | Code |
| R04 Startfehler-Tür | «Kontrollpanel startet nicht.» mit Grund, «Prüfung öffnen» (Prüfseite Website bearbeiten) und «Neu laden»; Wache 12 s | Code |
| R05 Kopfleiste | Insel mit Bergkamm in der Pille + «Kontrollpanel», Eck-Knöpfe «Anleitungen» (hell), «Website ansehen» (Hauptweg Lärche) | Bilder |
| R06 Rand | als Insel und Fuss (Wege, Anleitungen) | Fuss mit allen sechs Anleitungen |
| R07 Handy | unter 1180 nur Marke; 390 ohne seitliches Verrutschen, Fenster als Bänder | Prüfung 390 |
| R08–R14 | betrifft nicht (Kontrollpanel speichert und veröffentlicht nichts) | — |
| R16 Bühne | Empfang mit fünf Fenstern, Säle mit Kopf, Bergkamm, Titel | Bilder |
| R17 Bewegung | nur transform/opacity, «Weniger Bewegung» steht sofort | Code |
| R18 Rundgang | fünf Schritte, Schlüssel `rundgang-montemoro-maison`, `?rundgang`, nicht für Prüfprogramme, Sie-Form | Bilder der Rundgang-Schritte |
| R19 Zur Werkbank | `zur-werkbank.js`, Schlüssel `montemoro-wb`, nur mit Herkunft | Code |
| R20 / M27 Beispiele | Besucher und Rezeption mit beschrifteten Beispielwerten | Stand-Zeilen |
| R21 Hell mit Bühne | Empfang Nacht, Säle im Wechsel Creme / Nacht / Papier | Bilder |
| R24 Deutsch | `lang="de"`, Datum `de-DE`, Schweizer Schreibung (ss), Sie-Form (Bau bricht bei «du/dein» oder «ß» in der Seite ab) | Code |

## Kontrollpanel (M)

| Nr | Stand | Beleg |
|---|---|---|
| M01 Leiste als Insel | Namen nur, wenn sie zwischen die Eck-Knöpfe passen; Saal im Blick markiert | Bilder |
| M02 Eck-Knöpfe | «Anleitungen», «Website ansehen» | Bilder |
| M03 Gruss nach Tageszeit, Datum | `?gruss=morgen|tag|abend` | Code |
| M04 Empfang | fünf hohe Fenster mit Fotos des Hauses aus dem Bildregister der Website (das Haus von der Strasse, das Raclettestübli, die Gondel vor dem Röstihüs, der Empfang, die Rezeption mit dem Bergkamm), darüber das Logo in Papier, «Hotel mit Restaurant Röstihüs · Saas-Almagell · Saastal», «Kontrollpanel», Gruss, Datum, Kennzahlen | Bilder |
| M05 Stand je Werkzeug, live | aus den Stand-Wegen (`stand_wege.json`), ohne Antwort Satz ohne Zahl | Bilder |
| M06 Zahlenzeile | «Heute X Besuche · Y zur Buchung · Besucher öffnen», «Besuchszahlen als Beispiel» leise in der Datumszeile | Bilder |
| M07 Laufband | Namen der Werkzeuge, Hotel Monte-Moro, Restaurant Röstihüs, Saas-Almagell, Saastal, «Mehr erleben, weniger zahlen.» (alles aus `website/inhalt/daten.py`) | Code |
| M08 Säle mit echten Bildschirmen | zehn Bildschirme aus den Werkzeugen (`schirme.js`, Chromium 1440 × 932 @2x, feste Uhr 08.11.2026 10:30, nur GET) | Bilder |
| M09 Stücke | drei Karten aus Karten & Preislisten (Röstihüs-Karte, Wein und Apéro, Preisliste), Drucksachen aus Drucksachen & Feed (sobald sie Stücke des Hauses liefert, `stuecke.py DRUCK`), sechs Fotos des Hauses im Saal des Markenbuchs | Bilder |
| M10 Fuss | Logo in Logo-Blau, Das Haus (Name, Restaurant Röstihüs, CH-3905 Saas-Almagell, Telefon aus `daten.py`; keine Strasse, sie steht in `OFFEN`), Anleitungen, Fragen | Bilder |
| M11 Rundgang | fünf Schritte, Texte für das Hotel, Sie-Form | Bilder |
| M12 Taste 1–6 | wie Vorlage | Code |
| M13 Zwei Fassungen | `online/` ohne localhost, ohne Platzhalter (Bau bricht sonst ab) | `bau.py baue()` |
| M20 Fassung aus dem Inhalt; Knopf-Namen geprüft | `?v=` = Prüfsumme; jede «Knopf»-Angabe der Tafeln (`tafeln.json`) gegen den Code des Werkzeugs (`knoepfe()`) | Bau-Ausgabe |
| M21 Kacheln sanft | nichts hüpft, Foto zoomt ruhig | Code |
| M24 Ecke oben links gleich | Bergkamm in Lärche in der Pille aus Nacht 76 × 36, wie `.wo-marke-w` im gemeinsamen Kleid | alle Bildschirme |
| M25 Farben eine Reihe | bis zwölf Hausfarben aus `livre/livre.json` | Bild |
