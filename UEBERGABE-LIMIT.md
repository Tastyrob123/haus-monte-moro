In Prüfung.

Schlussprüfung 08.11.2026, 19:10 UTC: 28 Ziele (sieben Werkzeuge mit Anleitungen, Werkbank mit allen Unterseiten), 413 Zustände bei 1440 (dazu 1280/1000/390), 0 Funde, nichts unerreicht; Oberflächenprüfung 22 × BESTANDEN; Gegenprobe mit dem Auge (über 70 Bilder). Nur Chromium (WebKit in der Cloud nicht ladbar). Wartet auf Roberts Wort (Website-Revier, nicht Teil des Pakets): Baustein `reception/baustein/anfrage.js` in die Website, Datenschutz-Satz zu Anfragen/Chat.

# Übergabe (laufend) · Hotel Monte-Moro, Saas-Almagell

Stand: 08.11.2026, Oberchef-Sitzung (Zweig `claude/task-o0ores`).

## Auftrag
`AUFTRAG.md` + `CLAUDE.md`: komplette Werkbank und die sieben Werkzeuge im Kleid des Monte-Moro, Drucksachen, Feed, geprüft in der Sitzung (keine GitHub Actions), Unteragenten nur Opus. Letzte Nachricht an Robert genau eine: «Fertig. <Werkbank> <Prüftafel>» oder «Nicht fertig. … – es fehlt: …».

## Fertig
- Vorbilder geklont (`/tmp/culinarium`, `/tmp/wildside`, `/tmp/schloessli`), Kundenmaterial verlinkt (`/tmp/quelle`, `_quelle`).
- Stamm kopiert: Wild-Side-Stand (= Culinarium umgekleidet) nach `_werkzeuge/` und `website/_werkbank/`, Kennung `wildside`→`montemoro`, Ports 928x→938x (Skript-Wortlaut im Protokoll unten).
- Gemeinsames Kleid `_werkzeuge/oberflaeche/kleid/montemoro.{js,css}`, Zeichen Bergkamm `montemoro-zeichen.svg`, Wortmarke `montemoro-marke.svg#wm`.
- Namen: Das Hotelbüro · Das Schaufenster · Das Kartenbrett · Die Rezeption · Das Markenbuch · Die Besucherliste · Die Hausdruckerei (`kleid/montemoro.js › namen`).
- Ziellisten `_Werkzeuge/abnahme-tor/ziele-monte-moro.json`, `_Werkzeuge/messlauf/ziele-monte-moro.json`; Server in `cloud/haus.json` (9381–9388).
- Gemeinsamer Auftrag der Agenten: `Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/AUFTRAG-GEMEINSAM.md`.

## Stand der Agenten (08.11., abends)
- Alle sieben Werkzeuge fertig, 0 Funde (Chromium, 4 Breiten), committet und gepusht; Gegenprobe Oberchef mit eigenen Bildern 1440/390 (Scratchpad blick/).
- Nachbesserung Hausdruckerei läuft (Umbruch «Monte-/Moro» bei 390, goldene Knöpfe der Bar).
- Hotelbüro: Bildschirme der Werkzeuge neu (`maison/_bau/aufnahmen.sh`, Log /tmp/aufnahmen.log).
- Werkbank: Papier fertig (3301c99); Kern läuft, hat Bescheid, dass alle Werkzeuge stehen.
- Offen für Robert (nur Website-Revier, nicht gebaut): Baustein `reception/baustein/anfrage.js` in die Website, Datenschutz-Satz zu Anfragen/Chat.

## Offen, in Reihenfolge
1. Acht Bau-Agenten (Opus) parallel: Hotelbüro, Schaufenster, Kartenbrett, Rezeption, Markenbuch, Besucherliste, Hausdruckerei, Werkbank. Jeder: umkleiden, Hauswerte, `tor-schnell` 0 Funde, `LIEFERUNG.md`, Commit im Revier.
2. Oberchef: je Werkzeug Gegenprobe (15 Bilder ansehen), Funde zurück.
3. Werkbank: Bildschirme der Werkzeuge nach deren «fertig», `bau_alles.sh`, `oberflaeche_pruefen.js` BESTANDEN.
4. Prüfung über alles, Tafeln in Zweig `ergebnis` unter `ergebnis/laeufe/2026-11-08/`.
5. Meldung an Robert.

## Stand Folgesitzung (08.11., Nacht)
- Alle acht Reviere haben `LIEFERUNG.md` (Hotelbüro, Schaufenster, Kartenbrett, Rezeption, Markenbuch, Besucherliste, Hausdruckerei, Werkbank Kern + Papier). Kein Agent fehlt, keiner neu gestartet.
- `.claude/` und `CLAUDE.md` von main übernommen (Lebenszeichen).
- Schlussprüfung `bash cloud/schluss.sh > /tmp/schluss.log` läuft (28 Ziele, danach oberflaeche_pruefen.js je Oberfläche), Ergebnis in `aus-ende/`.
- Zwischenstand Schlussprüfung (18:25): Hotelbüro, Schaufenster (+Anleitung), Kartenbrett (+Anleitung), Rezeption (+Anleitung), Markenbuch (+Buch, +Anleitung): je 0 Funde, nichts «nicht erreicht». Messlauf über alles läuft parallel (`aus-ende/messlauf/alle/`), bisher 0 Funde.
- Augen (Oberchef): Werkbank 1440/390, Drucksachen, Feed, Kartenbrett, Rezeption, Markenbuch, Besucherliste, Hausdruckerei angesehen; Feed-Zahlen aus `_quelle/extern/ig/profil.txt` belegt.

## Erste Sitzung (Oberchef, läuft parallel weiter, 18:50 UTC)
- Eigene Schlussprüfung in `aus-ende/` dieser Sitzung: 16 Ziele frisch 0 Funde (Hotelbüro bis Werkbank, Werkbank-KI). Rest der Werkbank-Ziele und Oberflächenprüfung über alle Oberflächen laufen (`cloud/schluss_teil.sh`, Zählen: `python3 cloud/funde_zaehlen.py aus-ende`).
- 32 zufällige Zustandsbilder aller Werkzeuge mit dem Auge angesehen: ohne Befund.
- Diese Sitzung legt nach Abschluss die Tafel in `ergebnis` an und meldet Robert. Folgesitzung: bitte nichts doppelt prüfen; Funde hier eintragen.

## Folgesitzung (session_01QrxqqiMfjLjmUkccW3eNq2, 18:55 UTC)
- Zwei Funde mit dem Auge, repariert und gepusht (vom Tor nicht gemeldet):
  1. Schaufenster «Zeiten & Preise»: «ab CHF 90 .00» → «90.00» (`bureau/festigkeit.js › zahlwert`, nur Anzeige).
  2. Hausdruckerei: Kopfbild der Bereichsköpfe (Alle Vorlagen, Arten) am Handy nur 60 % breit → ganze Breite (`imprimerie/haeuser/montemoro/hell.css` Z. 71).
- Die Folgesitzung prüft Schaufenster und Hausdruckerei nach diesen Reparaturen frisch (tor-schnell, 4 Breiten) und trägt das Ergebnis hier ein; dazu der Messlauf über alle Ziele (`aus-ende/messlauf/alle/`), den die erste Sitzung nicht hat. Tafel `ergebnis` und Meldung an Robert macht die erste Sitzung.

## Nächster genauer Schritt
Läuft `cloud/schluss.sh` nicht mehr und fehlt `aus-ende/ende.json`: neu starten. Danach Funde reparieren, Fundbilder ansehen, Tafeln nach Zweig `ergebnis` unter `ergebnis/laeufe/2026-11-08/`, Meldung.

## Entscheidungen der Nacht
- Gearbeitet wird auf `claude/task-o0ores` (Auftrag der Folgesitzung), nicht auf main.
- Geprüft nur in Chromium (WebKit nicht ladbar, siehe Stolpersteine).
- Schaufenster «Zeiten & Preise» zeigte «90 .00» (Leser des Stamms setzt Leerschlag für Tags). Korrigiert nur in der Anzeige des Hauses (`bureau/festigkeit.js › zahlwert`), Stamm-Leser unverändert, weil seine Kennungen gespeicherte Änderungen tragen. Schaufenster nach der Schlussprüfung neu prüfen.

## Wartet auf Roberts Wort
- Baustein `reception/baustein/anfrage.js` in die Website, Datenschutz-Satz zu Anfragen/Chat (Website-Revier).


## Einrichten in einer neuen Sitzung
- `git fetch origin quelle && git worktree add /tmp/quelle origin/quelle && ln -sfn "/tmp/quelle/Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle" "Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle"`
- Playwright: `mkdir -p /Users/robertreff/Aussen-Pruefung/node_modules && ln -sfn /opt/node-tools/node_modules/playwright /Users/robertreff/Aussen-Pruefung/node_modules/playwright` (dazu `playwright-core`), `ln -sfn $PWD /Users/robertreff/Desktop/Website-Projekte`, `_Befund-Vorschlaege/node_modules/playwright` ebenso (für `oberflaeche_pruefen.js`). `vorbereiten.sh` nicht nötig.
- `bash cloud/server.sh` (Ports 9381–9388).
- Vorbilder klonen wie in CLAUDE.md.

## Stolpersteine
- WebKit lässt sich in dieser Umgebung nicht laden (Netz sperrt cdn.playwright.dev): geprüft wird in Chromium.
- `website/_werkbank/` ist gross (Wild-Side-Bilder aus der Kopie); erst nach dem Neubau einchecken, Wild-Side-Ausgaben vorher löschen.
- Agenten: keine Heredocs / eingebetteten Skripte in der Shell (hängen an der Freigabe).
