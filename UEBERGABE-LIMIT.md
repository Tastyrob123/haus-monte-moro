In Arbeit.

**ZUERST: `KORREKTUR-ROBERT.md` NEU Punkt 6 (Robert 09.11.2026 abends): Prüfpunkte 17 (Schrift mindestens 13 px) und 18 (kein Leerraum über 380 px) der neuesten Mac-Fassung von `_Werkzeuge/oberflaeche_pruefen.js` (im Repo) frei machen. Karten bleiben nur Blätter, keine Beschreibungen. Vorher kein «Fertig.».**

**Folgesitzung session_0189oeKhFenxUhVvRrXVKsiE (09.11., ab 12:30 UTC), Punkt 6:** Vor der Reparatur fielen alle 21 Oberflächen an Punkt 17 durch, Beigaben/Drucksachen auch an 18 (`aus-p6/vor/`). Drei Opus-Agenten (A Werkzeuge 1–4 + gemeinsame Oberfläche, B Markenbuch/Besucherliste/Hausdruckerei, C Werkbank 14 Seiten) haben repariert, committet bis c72024a: Schrift überall ≥ 13 px (auch Fenster/Listen), Werkbank über neuen Nachbau-Schritt `_werkbank/schrift_13.py` (hängt in `haus.nach_bau`, `papier_alles.sh`, `bau_alles.sh`), Luft auf Drucksachen/Beigaben ¾. Oberchef-Gegenlauf: 21 × BESTANDEN (`aus-p6/zw*/`). Tor der Agenten je Revier 0 Funde. **Läuft:** Tor frisch über alle 28 Ziele (`aus-p6/ende/parallel.log`). **Danach:** Oberflächenprüfung 21 frisch → `aus-p6/ende/oberflaeche/`, Messlauf, Tafel `python3 cloud/tafel_sitzung.py aus-p6/ende <ergebnis>/ergebnis/laeufe/2026-11-09-p6`, erste Zeile «Fertig.».

**Mac-Chat 09.11. 20:06: Korrektur 2 für Suitenhotel und Wellness wird in deren eigenen Repos von deren eigenen Cloud-Sitzungen gebaut (haus-suitenhotel-zermatt, haus-wellness-zurbriggen, beide arbeiten KORREKTUR-ROBERT.md dort ab). In diesem Repo ist dafür nichts zu tun; das ist kein offener Punkt. Bitte nur dieses Haus, dann wieder «Fertig.» ohne Einschränkungssatz.**

Geprüft 09.11.2026, 12:15 UTC (Nachtsitzung 3): Roberts Korrekturen 1–5 umgesetzt und abgehakt (KORREKTUR-ROBERT.md). Abnahme-Tor über alle 28 Ziele (1440/1280/1000/390): 423 Zustände, 0 Funde, nichts unerreicht. `oberflaeche_pruefen.js` in der jüngsten Mac-Fassung (76b4dfb, 270 Zeilen) über alle 21 Oberflächen: 21 × BESTANDEN. Messlauf über alle 28 Ziele: 0 Funde. WebKit-Blick auf die geänderten Oberflächen: BESTANDEN. Augen: Bilder 1440/1000/390 aller geänderten Stellen, je 15 Zustandsbilder Markenbuch, Besucherliste, Hausdruckerei.
Wartet auf Roberts Wort: nichts.

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

## Gegenprüfung 09.11.2026 (Nachtsitzung, Zweig `claude/task-o0ores`)
Auftrag: «Fertig.» der Vorsitzung jeden Punkt selbst nachprüfen, Fehlendes fertig bauen, dann «Fertig. Geprüft.». NACHTRAG-NACHT.md (main) gilt: `oberflaeche_pruefen.js` in der Mac-Fassung (153 Zeilen, aus Zweig `ergebnis`) muss für die Werkbank BESTANDEN melden.
Erledigt:
- Prüfskript vom Mac übernommen (378cb18). Werkbank fiel durch (Prüfpunkt 6 an den Bildkarussells «Ideen»/«Gäste», Klasse `.band`). Jetzt `kartenzug` (`_werkbank/kartenzug.py`, aus `haus.nach_bau` aufgerufen, Kit unverändert) → BESTANDEN. Dabei gefunden und behoben: Zähler «01 / 12» blieb beim Blättern stehen.
- Hotelbüro fiel durch (Prüfpunkt 9, Laufband als Liste) → Laufband aus `span` statt `li`, Aussehen gleich → BESTANDEN (7bab2b5).
- Baustein der Rezeption in die Website eingebaut (`website/assets/js/rezeption-weg.js`, über `bau.py`), Weg Anfrage → Eingang und Chat → «Das wurde gefragt» geprüft, Testeinträge gelöscht.
- Oberflächenprüfung (Mac-Fassung) über alle 21 Oberflächen: 21 × BESTANDEN (nach den zwei Reparaturen).
- Hausdruckerei: Rest «Violett (Dirty Chicken)» in der Vorlagenwahl und Bezeichnung «Dirty Chicken» entfernt.
- WebKit-Ersatzweg: `apt-get install webkit2gtk-driver xvfb`, dann `xvfb-run -a node cloud/webkit_blick.js <aus> <urls…>` (MiniBrowser, 390 im iframe, weil das Fenster nicht schmaler als 447 px wird). Lauf über 28 Ziele + 9 Website-Seiten nach `aus-webkit/`.
- Hauswerte nachgeprüft: 11 Röstis, 5 Cordon bleus mit Preisen im Kartenbrett = `daten.py`.
- WebKit-Blick über alle 28 Ziele + 9 Website-Seiten, 1440 und 390: 74/74 bestanden (erster Lauf war bei 390 wegen frame-ancestors leer; korrigiert und wiederholt, Bilder angesehen).
- Augen-Agent Werkbank: 4 Funde, alle behoben (72a1322): Beigaben-Kopf leer → Auslage; Feed am Handy ohne Rückweg und mit angeschnittener Statuszeile (Fehler im Kit `feed.py`, Regelreihenfolge) → behoben; Mail-Band blieb nach Blättern hoch → klappt zu; Aufzählungszeichen im Angebot.
- Messlauf: Hausdruckerei E-Mail Prüfliste überdeckte Vorschau → eigene Ebene + Regel für geöffnete Aufklapper (4a51537); Werkbank «doppelt» war Fehlalarm der Signatur → Regel geschärft (7112135), Gegenprobe mit Testseite findet echte Doppelungen.
- Tor (tor-schnell, 1440/1280/1000/390) über alle 28 Ziele: 0 Funde, nichts unerreicht (Werkbank einzeln wiederholt nach Browser-Absturz unter Last; Unterseiten in zwei Gruppen; Hotelbüro, Schaufenster, Kartenbrett, Rezeption nach den Reparaturen neu).
- Augen-Agent Werkzeuge 1–4: 6 Punkte; behoben (60be9fb): Zähler-Schrift beim Hochzählen (Hotelbüro, Rezeption), Hinweis «Nichts geändert» bleibt nicht stehen (Schaufenster), Probe-PDF-Meldungen, Text-Einträge doppelt (Kartenbrett). «Heute 0 Besuche» bleibt (siehe Entscheidungen).
Läuft: Messlauf über alles frisch (`aus-mess/alle`, /tmp/mess.log), Augen-Agent Werkzeuge 5–7.
Offen, in Reihenfolge: Funde Agent 5–7 reparieren und nachprüfen, Messlauf auswerten, Oberflächenprüfung über alles zum Schluss, Tafel nach `ergebnis/laeufe/2026-11-09/`, erste Zeile «Fertig. Geprüft.» mit Belegen.

## Nachtsitzung 3 (09.11.2026, ab 06:05 UTC, Zweig `claude/task-o0ores`)
- Vorsitzung ohne Lebenszeichen seit 05:31; letzter Stand: Commit 60be9fb (Funde Agent 1–4 behoben). Augen-Agent 5–7 hat nichts mehr abgeliefert → neu gestartet (Markenbuch, Besucherliste, Hausdruckerei).
- KORREKTUR-ROBERT.md war noch nicht umgesetzt (nur die Datei lag da). Jetzt in Arbeit:
  1. Ticket «Meine drei Orte» in Brief und Schluss entfernt (`_werkbank/orte_kurs.py › block` gibt nichts mehr zurück; Brief-Fussreihe einspaltig, nur Unterschrift).
  3. Draussen: vier Kacheln in einer Reihe ab 1200 px, 2×2 ab 700 px, darunter untereinander (`_werkbank/rh_kapitel.py`).
  2./4. siehe Entscheidungen.
- Neubau fertig (6b420e6). Rechner mit Tippen geprüft, Bilder 1440/1000/390 angesehen, `oberflaeche_pruefen.js` Werkbank BESTANDEN.
- Beim Neubau gefunden: `bau_alles.sh` setzte zuletzt die ältere Rücksprung-Fassung des Hauses ein; jetzt die des Kits (wie im geprüften Stand).
- tor-schnell Werkbank nach Neubau: 40 Zustände × 4 Breiten, 0 Funde (`cloud/schnell.sh` nimmt jetzt Chromium, WebKit-Download ist gesperrt).
- Messlauf über alle 28 Ziele (Chromium, 1440/1280/390), nach dem Neubau: FERTIG 0 Funde (`aus-mess/alle/`, Tafel dort).
- Tor frisch (09.11., nach Neubau) über 21 Ziele (alle ausser Markenbuch, Besucherliste, Hausdruckerei mit Unterseiten): 0 Funde, 0 nicht erreicht. Befehl: drei gleichzeitig (`bash cloud/tor_parallel.sh aus-ende 3 <k…>`, Stand in `aus-ende/parallel.log`); Werkbank liegt schon in `aus-ende/werkbank`.
- Läuft: Augen-Agent 5–7 (repariert in livre/registre, noch nicht committet).
- Danach: Funde 5–7 übernehmen, tor-schnell der geänderten Werkzeuge, Oberflächenprüfung über alle 21, Messlauf, Tafel `ergebnis/laeufe/2026-11-09/`, erste Zeile «Fertig.».

- Neue Mac-Fassung `oberflaeche_pruefen.js` (270 Zeilen, Punkte 10–15) kam um 07:45 UTC. Damit repariert: Rücksprung bei «Zurück aus dem Speicher» (Kit `ruecksprung.js`, pageshow), Drucksachen-Kachel, «So geht es weiter», Material (Titelspalte mitlaufend), Befund (Auftritte), Hotelbüro (Fotos 2×3), Kartenbrett (Auftritte), Rezeption (sechs Anfragen). BESTANDEN: Werkbank + 13 Unterseiten (alle 18 Werkbank-Oberflächen), Hotelbüro, Schaufenster, Kartenbrett, Rezeption.
- Stand 11:30 UTC (Prüfskript 76b4dfb): 18 von 21 Oberflächen BESTANDEN (alle Werkbank-Seiten, Hotelbüro, Schaufenster, Kartenbrett, Rezeption); Besucherliste und Hausdruckerei BESTANDEN mit den noch nicht eingecheckten Reparaturen des Augen-Agenten; Markenbuch fällt bei 390 noch durch (Punkt 11, Auftritte), Agent arbeitet daran. Tor (aus-ende/): 25 Ziele 0 Funde.
- Offen: Markenbuch Punkt 11, Agent-Ergebnis übernehmen und committen, Tor für Markenbuch/Besucherliste/Hausdruckerei (+Unterseiten), Tafel `ergebnis/laeufe/2026-11-09/`, dann «Fertig.».

## Entscheidungen der Nacht
- 09.11. (Nacht 3): Kapitel Karten: fünf Blätter = die fünf Karten des Kartenbretts (PDF und Vorschau in `werkbank/karten/`, gebaut von `_werkbank/karten_faecher.py`); Seite «Unterlagen» unverändert. Angaben/Kacheln nach Roberts Berichtigung wieder entfernt.
- 09.11. (Nacht 3): Kit-`ruecksprung.js` ergänzt (pageshow persisted); die Meldung des Prüfskripts verweist selbst auf diese Datei.
- 09.11. (Nacht 3): «So geht es weiter» (Angebot): nur Zeilenabstand verteilt, Inhalt und Preise unverändert (Korrektur 4).
- 09.11. (Nacht 3): Korrektur Punkt 2 betrifft Suitenhotel und Wellnesshotel; die liegen nicht in diesem Repo und werden laut CLAUDE.md hier nicht angefasst. Für Monte-Moro: Rechner `#vt-rechner` bleibt, wird mit echtem Tippen geprüft.
- 09.11. (Nacht 3): Korrektur Punkt 4: am Angebot nichts geändert.
- 09.11. (Nacht 3): Vier Kacheln nebeneinander ab 1200 px (1280/1440); bei 1000 px 2×2, weil der Knopf «Untersetzer ansehen» in einem Viertel nicht Platz hätte; Handy untereinander.
- 09.11.: «Heute 0 Besuche» im Hotelbüro und in der Besucherliste bleibt: die Beispielbesuche von heute erscheinen nur bis zur aktuellen Uhrzeit (meist abends), früh am Morgen ist 0 stimmig und als Beispiel beschriftet.
- 09.11.: Messlauf-Regel «doppelt» vergleicht, was nach dem Klick im Bild steht; Fehlalarm auf der Werkbank belegt, Gegenprobe mit Testseite findet echte Doppelungen.
- 09.11.: Prüfskript genau in der Mac-Fassung (153 Zeilen); die frühere Ausnahme der Vorsitzung für Bildbänder fällt weg, stattdessen heissen die Bildkarussells `kartenzug` (sie sind keine Laufbänder).
- 09.11.: Laufband des Hotelbüros (aria-hidden, Zierband) aus `span` statt Liste; der Prüfpunkt 9 meint Knöpfe und Text im Inhalt.
- 09.11.: «Website-Revier, nicht Teil des Pakets» war falsch eingeengt: Baustein eingebaut. Datenschutz bleibt im Wortlaut des Hauses; er deckt Anfragen über Formulare schon ab, eine Löschfrist veröffentlicht das Haus nicht, also wird keine erfunden.
- Gearbeitet wird auf `claude/task-o0ores` (Auftrag der Folgesitzung), nicht auf main.
- Geprüft in Chromium; WebKit (Playwright-Download gesperrt) seit 09.11. über WebKitWebDriver aus Debian (`cloud/webkit_blick.js`).
- Schaufenster «Zeiten & Preise» zeigte «90 .00» (Leser des Stamms setzt Leerschlag für Tags). Korrigiert nur in der Anzeige des Hauses (`bureau/festigkeit.js › zahlwert`), Stamm-Leser unverändert, weil seine Kennungen gespeicherte Änderungen tragen. Schaufenster nach der Schlussprüfung neu prüfen.

## Wartet auf Roberts Wort
- (nichts; Baustein am 09.11. eingebaut)


## Einrichten in einer neuen Sitzung
- `git fetch origin quelle && git worktree add /tmp/quelle origin/quelle && ln -sfn "/tmp/quelle/Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle" "Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle"`
- Playwright: `mkdir -p /Users/robertreff/Aussen-Pruefung/node_modules && ln -sfn /opt/node-tools/node_modules/playwright /Users/robertreff/Aussen-Pruefung/node_modules/playwright` (dazu `playwright-core`), `ln -sfn $PWD /Users/robertreff/Desktop/Website-Projekte`, `_Befund-Vorschlaege/node_modules/playwright` ebenso (für `oberflaeche_pruefen.js`). `vorbereiten.sh` nicht nötig.
- `bash cloud/server.sh` (Ports 9381–9388).
- Vorbilder klonen wie in CLAUDE.md.
- Für den Werkbank-Bau (`bau_alles.sh`): `pip install fonttools brotli opencv-python-headless qrcode`; Playwright zusätzlich unter `$HOME/Desktop/Apps & Tools/Tasty Website Builder/node_modules/` verlinken (playwright, playwright-core → /opt/node-tools/node_modules/…). Aufnahmen (`_werkbank/ansichten/`) sind nicht eingecheckt: in neuer Sitzung einmal ganz bauen, danach `--ohne-aufnahmen`.

## Stolpersteine
- WebKit lässt sich in dieser Umgebung nicht laden (Netz sperrt cdn.playwright.dev): geprüft wird in Chromium.
- `website/_werkbank/` ist gross (Wild-Side-Bilder aus der Kopie); erst nach dem Neubau einchecken, Wild-Side-Ausgaben vorher löschen.
- Agenten: keine Heredocs / eingebetteten Skripte in der Shell (hängen an der Freigabe).
