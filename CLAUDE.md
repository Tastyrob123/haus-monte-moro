# Haus in der Cloud — Arbeitsweise für den Cloud-Chat

Dieser Ordner ist **ein Haus**: Hotel Monte-Moro mit Restaurant Röstihüs, Saas-Almagell (Familie Zurbriggen, Gastgeber Esther und Fabian Zurbriggen). Recherche, Konzept und Website hat Robert auf dem Mac gebaut. Hier entstehen **Werkbank und die sieben Werkzeuge**, bis ins Detail ausgearbeitet und fertig (Robert 08.11.2026). Du bist der Oberchef dieses Hauses.

## Aufbau des Ordners
- `Zurbriggen Hotel Monte-Moro Saas-Almagell/website/` Website (Quelle, gebaut von `bau.py`), `UEBERGABE.md`, `LIESMICH.md`, Prompt des Hauses, `_kette/` Stationen (Markenbuch in `_kette/05-markenbauer/`, Werkbank-Station `_kette/11-werkbank/`, Prüfer `_kette/12-pruefer-werkzeuge/`).
- `Familie Zurbriggen/` nur das, was die Website zum Bauen braucht (Familienband, `FAMILIEN-FOOTER.md`, vier Familienfotos).
- `_Werkzeuge/` Prüfwerkzeuge (Abnahme-Tor `abnahme-tor/`, Messlauf `messlauf/`, `oberflaeche_pruefen.js`), `ROBERTS-KRITERIEN.md`, `OBERCHEF-PAKET.md`.
- `_Werkbank-Kit/` Bausteine der Werkbank. `Carlton-Europe Interlaken/_werkbank/geraet/` die Blender-Geräte für Aufnahmen.
- `cloud/haus.json` Server und Ziellisten des Hauses · `cloud/*.sh|py` Einrichtung, Prüfung, Tafeln.
- Kundenmaterial liegt im Zweig `quelle`: `git fetch origin quelle && git worktree add /tmp/quelle origin/quelle && ln -sfn "/tmp/quelle/Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle" "Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle"`.

## Vorbilder (öffentlich, ohne Schlüssel)
- `git clone --depth 1 https://github.com/Tastyrob123/haus-culinarium-hannover /tmp/culinarium` — **Stamm** der Werkbank (`Culinarium Hannover/website/_werkbank/`) und der sieben Werkzeuge (`Culinarium Hannover/_werkzeuge/`).
- `git clone --depth 1 https://github.com/Tastyrob123/haus-wildside /tmp/wildside` — zuletzt fertig gebautes Haus nach demselben Weg; Regelwerke (Werkzeug-Master, Website-Bau Kern, Tasty-Sprache) in `/tmp/wildside/vorgaben/`.
- `git clone --depth 1 https://github.com/Tastyrob123/haus-schloessli /tmp/schloessli` — weiteres Haus nach demselben Weg.

## Der Deal mit Robert (verbindlich)
- **Was «fertig» heisst:** die komplette Werkbank wie beim Culinarium (Startseite, Karte, KI, Geprüft, Befund, Unterlagen, Drucksachen, Untersetzer/Sticker, Feed, Mails, Material) mit Inhalt des Monte-Moro, ohne Platzhalter; die sieben Werkzeuge im Kleid des Hauses (Name, Zeichen, Farben, Schriften aus Markenbuch und Website) mit eingetragenen Hauswerten, aus der Werkbank verlinkt; die Drucksachen; alles geprüft nach Roberts Zweck (Zustände, die ein Kunde öffnet, vier Breiten, Auge an den Bildern). Robert öffnet den Link und könnte das Paket so an den Kunden schicken.
- **Nichts neu erfinden:** kopieren, umkleiden, Hauswerte eintragen. Fakten, Namen, Preise, Zeiten nur aus dem Material des Hauses (Website `inhalt/daten.py`, `_kette/03-sammler/fakten.json`, Zweig `quelle`); was das Haus nicht veröffentlicht, bleibt offen und erscheint nicht.
- **Modell:** alle Sitzungen und Unteragenten auf Opus (`claude-opus-5-5`), nie Fable. Unteragenten mit `model: "opus"`.
- **Parallel, mit klarem Revier:** je Werkzeug ein Unteragent (Ordner, Port, Stamm-Vorlage, Kleid des Hauses); jeder prüft sein Werkzeug selbst und meldet «fertig». Du fügst zusammen und prüfst das Paket.
- **Reihenfolge, damit immer etwas ganz ist:** Werkbank-Rahmen zuerst, dann Werkzeug für Werkzeug: bauen, prüfen, reparieren, abhaken, nächstes. Reihenfolge: Tresen, Schaufenster, Pairing-Karte, Gästebuch, Markenbuch, Besucherliste, Plakatwerkstatt, dann Drucksachen und die übrigen Werkbank-Seiten.
- **Nicht fertig = Robert entscheidet.** Die Liste des Offenen ist die ganze Erklärung; kein Vorschlag, keine Technik, keine Begründung.

## Prüfen — hier in der Sitzung, nicht auf GitHub-Rechnern
Dieser Ordner ist **privat**. Prüfläufe auf GitHub-Rechnern (Actions) kosten bei privaten Ordnern Geld, sobald das Freikontingent aufgebraucht ist. Deshalb:
- **Keine Workflows anlegen, keine GitHub Actions starten**, auch nicht `[schnell]`/`[abnahme]` in Commit-Nachrichten.
- Einrichten (einmal je Sitzung): `bash cloud/vorbereiten.sh "chromium webkit"` und `bash cloud/server.sh` (Ports des Hauses 9381–9388, in `cloud/haus.json › server` eintragen).
- Ziellisten `_Werkzeuge/abnahme-tor/ziele-monte-moro.json` und `_Werkzeuge/messlauf/ziele-monte-moro.json` aus den Culinarium-Listen anlegen (Ports, Namen, Stilblatt-Pfad des Hauses).
- Je Werkzeug gleich nach dem Bau: `bash cloud/schnell.sh <werkzeug>` (Start, jeder Navigationspunkt, jeder Reiter, jedes Fenster, je Gruppe drei Stücke, höchstens 40 Zustände, 1440/1280/1000/390). Ergebnis in `aus/<werkzeug>/`. Dazu der Messlauf mit `_Werkzeuge/messlauf/` für dieses Werkzeug.
- Jede gebaute Oberfläche (Werkbank, Werkzeug-Übersicht) muss `node _Werkzeuge/oberflaeche_pruefen.js <adresse>` mit BESTANDEN durchlaufen.
- Mit den Augen prüfen: jedes Fundbild und mindestens 15 zufällige Zustandsbilder je Werkzeug mit dem Read-Werkzeug ansehen (Kriterien **A** in ROBERTS-KRITERIEN.md). Fehlalarm einer Prüfregel: Regel schärfen (mit Beleg), nie den Fund wegerklären.
- Prüfergebnisse (Tafeln, Fundbilder) in den Zweig `ergebnis` unter `ergebnis/laeufe/<datum>/` legen, damit Robert sie sieht.

## Feste Regeln (aus Roberts globalen Regeln)
- Nichts verschicken, nichts veröffentlichen, nichts bezahlen, kein Vercel, keine KI-Bildaufrufe, keine API-Schlüssel. KI-Funktionen der Werkzeuge nur mit Probe-Antworten (ohne `*_KI=1`).
- Nur dieses Haus. Wellnesshotel, Suitenhotel Zermatt und andere Häuser werden nicht angefasst. Grand Beau-Rivage nie. Port 8765 gehört nicht hierher.
- Texte für Gäste: Wertigkeit, Sorgfalt, der einzelne Gast; nie Masse, Abfertigung, Stückzahlen als Pointe. Schweizer Schreibung (ss, «Guillemets»), Sie-Ansprache.
- Aufnahmen von Website und Werkzeugen nur in den Blender-Geräten (`Carlton-Europe Interlaken/_werkbank/geraet/`), je Abschnitt eine Ansicht, kein Gerät im Gerät; jede Ansicht gefüllt; Zahlen, Stand und Knopf in einer Tafel; nicht dasselbe Bild in jeder Zeile; kein Fehler, kein Überlauf bei 1440 und 390.
- Sicherung vor jeder Änderung an Bestehendem (`…vor-<thema>-<datum>`, wird nicht eingecheckt).
- Antworten an Robert: Deutsch, kurz, Alltagssprache, Link vorne. Am Ende **eine** Nachricht: «Fertig. <Link Werkbank> <Link Prüftafel>» oder «Nicht fertig. <Links> – es fehlt: <Liste>».
