# Auftrag: Website für das Hotel Monte-Moro mit Restaurant Röstihüs, Saas-Almagell

Fassung der Kette, Station 3 (Sammler), 17.10.2026. Sie löst für die Kette `../Familie Zurbriggen/Prompt 4 — Hotel Monte-Moro, Saas-Almagell.md` (09.10.2026) ab; jene Datei bleibt unverändert liegen. Abschnitt 3 und 4 sind neu und nennen zu jeder Angabe die Datei. `_quelle/` ist ein Verweis auf `../Familie Zurbriggen/_quelle/monte-moro/`.

Du baust für mich (Robert, Tasty Studios) die neue Website für das **Hotel Monte-Moro** mit dem Restaurant Röstihüs in Saas-Almagell (3 Sterne, Gastgeber laut Impressum Esther und Fabian Zurbriggen, dieselben wie im Wellness & Spa Pirmin Zurbriggen). Die heutige Seite ist ein Tabellen-Gerüst auf Joomla. Sie soll sich so anfühlen wie meine Carlton-Europe-Seite: ein Haus, das man betritt, mit luxuriöser Bewegung, grossen Fenstern, Texten, die man gern liest. Dasselbe Niveau, dieselbe Sorgfalt im Detail, aber ein eigenes Haus mit eigenem Aufbau und eigenen Farben. In der Kette entstehen Markenbuch (Station 5) und Konzept-Board (Station 6) vor dem Bau; gebaut wird in Station 7, Abschnitt für Abschnitt.

## 1 Zuerst lesen (vollständig, bevor du irgendetwas entwirfst)

1. `~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md`, besonders Abschnitt 2 (Gestaltung, 2.1 «Erlebnis statt Abschnitte»), 3 (Bausteine), 4 (Bewegung), 6 (wie ich Rückmeldung gebe), 10 (Abnahme), 13 (die Kette) und im Lernprotokoll der Eintrag «Carlton-Europe Interlaken».
2. `~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Briefing — Roberts Standard.md` ganz.
3. `~/SecondBrain/00 Kontext/Design-DNA — Vibe & Einflüsse.md` und `00 Kontext/Branding.md`.
4. CLAUDE.md Regel 55 (Flüssigkeit steht über allem), 57 (erst prüfen, dann sagen), 60.
5. Die Pakete der Kette: `_kette/02-spaeher/` (Befund, Einordnung, offene Punkte) und `_kette/03-sammler/` (`fakten.json`, `sprachen.json`). Was dort «offen» steht, bleibt offen, bis es belegt ist.
6. **Vorbild Carlton-Europe:** `~/Desktop/Website-Projekte/Carlton-Europe Interlaken/`. Starte sie (`(nohup python3 serve.py 8912 >/dev/null 2>&1 &)`, http://localhost:8912/) und geh jede Seite durch, als Bild und im Code: `assets/css/main.css`, `assets/js/main.js`, `assets/js/bilder.js`, `bau.py`, `inhalt/*.py`, `_qa/`.
7. **Referenzbau Salt & Silver:** `~/saltandsilver-website/` (http://localhost:8866/index.html). Von dort kommen die Bausteine.
8. **Das Material des Hauses:** `_quelle/Material-Übersicht.md`, `_quelle/notizen.md`, `_quelle/material.html`, jeder Bogen in `_quelle/_boegen/`, alle Texte in `_quelle/website/text/` (deutsch, voller Tabellen-Reste) und `_quelle/website/nachtrag-2026-10-17/text/` (englisch, französisch), die Speisekarten `_quelle/website/pdf/speisekarte.pdf` und `_quelle/website/nachtrag-2026-10-17/pdf/speisekarte-fr.pdf`, die Portaltexte in `_quelle/extern/`.
9. **Die Familie:** `../Familie Zurbriggen/_quelle/notizen.md`, `../Familie Zurbriggen/_quelle/pirmin-alte-seite/text/`, `../Familie Zurbriggen/_quelle/presse/`. Ist die Seite des Wellness & Spa in der Kette schon gebaut (`../Zurbriggen Wellnesshotel Saas-Almagell/website/`): ansehen, damit die beiden Häuser derselben Gastgeber verwandt wirken, ohne gleich zu sein (Regel «Jedes Haus eine eigene Welt»).

## 2 Was von den Vorbildern übernommen wird und was nicht

**Übernommen wird das Gefühl und das Handwerk:**
- dunkle Flächen mit Tiefe im Wechsel mit hellen, dazu ein Muster oder Zeichen des Hauses Ton in Ton
- Titel fahren zeilenweise aus einem Schlitz hoch, Bilder schweben von unten herauf und werden dabei grösser, Linien ziehen sich
- Fenster: ein stehendes echtes Bild zwischen zwei Abschnitten, über das die Seite hinwegzieht (zwei bis drei je Startseite)
- grosse Zahlen als eigener Abschnitt, Band zum Blättern mit grossen Karten, Blatt Papier auf dunklem Grund für Karte und Preise
- Bildrahmen mit doppeltem Rand und feiner Innenlinie, Einkerbung in der Bildecke, Glanzkante sparsam
- Knöpfe mit Tiefe: Pille, Lichtkante oben, Schattenkante unten, runder Knauf mit Pfeil
- Leiste oben als schmale Insel, Buchen immer erreichbar, Buchungsfenster mit Datum und Gästen
- Fuss mit dem Satz des Hauses gross und den Häusern der Familie Zurbriggen als Karten, nach Gastgebern geordnet: Esther und Fabian (Wellness & Spa Pirmin Zurbriggen, Loft-Suite Hotel, Hotel Monte-Moro, alle Saas-Almagell), Moni und Pirmin (Suitenhotel Zurbriggen, Zermatt), Heidi und Damian (Chalet Rustica, Saas-Almagell). Jede Karte mit echtem Foto und «Zum Haus»
- Ersatzschriften in gleicher Laufweite, damit beim Laden nichts springt

**Nicht übernommen wird:**
- der Seitenaufbau des Carlton. Er wird für dieses Haus neu gedacht. Kein Abschnitt steht nur da, weil das Carlton ihn hat.
- der Auftakt mit den zwei Türflügeln. Dieses Haus bekommt einen eigenen ersten Moment.
- die Farben (Navy, Creme, Messing) und die Schrift (Libre Baskerville). Farben und Titelschrift kommen aus der CI dieses Hauses (Station 5).
- alles, was ich am Carlton abgelehnt habe: Schieberegler, Lift-Fahrt, Buchstaben-Rollen, übergrosse Einzelwörter, Bögen ausserhalb des Restaurants, eine helle flache Fassung ohne Effekte.

**Ein Hotel wird als Hotel gedacht:** Ankunft mit Buchungsleiste, dann Fragen an den Gast, Zimmer, Essen, Erholung, Angebote, Geschichte, Anreise. Klare Knöpfe, grosse lesbare Schrift, nichts Verspieltes. Ruhig heisst nicht flach.

## 3 Das Haus (am 17.10.2026 an der Quelle gelesen)

- **Was es ist:** Hotel und Restaurant mit drei Sternen, 18 Zimmer, 55 Betten (`_quelle/extern/myswitzerland/myswitzerland-seiten-text.md`: «Dreistern», «Anzahl Zimmer 18», «Familiäres 3-Stern Hotel mit 55 Betten»). Im Impressum: «Hotel Monte-Moro, Esther und Fabian Zurbriggen-Zurbriggen», CH-3905 Saas-Almagell (`_quelle/website/text/de__impressum.html.md`). Die Seite nennt das Wellness & Spa Pirmin Zurbriggen das «Partnerhotel» (`_quelle/website/text/de.md`).
- **Adresse: offen.** Routenplaner der Seite «Talstrasse 129», Google «Furusandstrasse 12», Sitz der Resort Monte Moro AG seit März 2026 «Furusandstrasse 10» (`_kette/03-sammler/fakten.json` › adresse). Auf der Seite steht deshalb nur, was das Impressum nennt: «CH-3905 Saas-Almagell»; für den Weg dorthin der Routenplaner-Link der heutigen Seite.
- **Wem das Haus gehört: offen.** Im Handelsregister steht die Resort Monte Moro AG mit Oliver Wachs (Zürich) als einzigem Verwaltungsrat (`_quelle/presse/handelsregister-2026-10-17.md`). Impressum, Speisekarte und die Filme 2026 zeigen Esther und Fabian. Auf der Seite stehen nur die Gastgeber, wie sie im Impressum stehen.
- **Zimmer und Preise** (`_quelle/website/text/de__hotel__zimmer.html.md`, `de__hotel__preise.html.md`): alle Zimmer mit Dusche/Bad und WC, Haarfön, SAT-TV, Safe, W-LAN, Balkon, Lift. Budgetzimmer CHF 90.00, Standardzimmer CHF 100.00 pro Person und Tag mit Frühstück; mit Halbpension (4 Gänge) CHF 120.00 und 130.00. Zuschläge, Kurtaxen, Kinder und Hund stehen vollständig in der Datei, nichts runden. Familienzimmer und Familienkombinationen für 3 bis 6 Personen. Weitere Zimmer in der Residence Alpenhof, vier Gehminuten entfernt, Essen im Monte-Moro. Bezahlung in Euro möglich, Rückgeld in Franken. Saisonzeiten der Preise nennt die Seite nicht.
- **Ferienwohnungen** (`de__ferienwohnungen__apollo.html.md`, `…arizona.html.md`): Haus Apollo, Wohnung im 4. Stock am Dorfeingang mit Südbalkon; Haus Arizona mit 4½-, 3½- und 2½-Zimmer-Wohnungen. Preise und Grössen nennt die Seite nicht.
- **Restaurant Röstihüs** (`de__restaurant.html.md`, `de.md`, Karten als PDF): Schweizer Spezialitäten aus regionalen Produkten, Walliser Weine, Appenzeller Bier, Sonnenterrasse vor dem Haus, kleine Kinderauswahl. Eine Karte für alles (Speisen, Weine, Getränke), deutsch und französisch, beide vom 18.11.2024. Auf der Karte stehen elf Röstis und fünf Cordon Bleus; die Startseite sagt «12 verschiedenen Röstis und 7 verschiedenen Cordon Bleus»: die Karte gilt, die Zahl kommt aus der Karte. Zwei «Hotelweine» hat laut Karte «Fabian selber kreiert». Die Seite empfiehlt den «Zurbriggen Spritz» (Lemonsoda, Prosecco, Blue Curacao) und den «Antrona Spritz» (Prosecco, Früchte, Campari), Namen und Zutaten genau so. Tische über TheFork oder Telefon. **Öffnungszeiten: offen**, nirgends veröffentlicht.
- **Spa:** Monte-Moro-Gäste nutzen das Spa im Hotel Pirmin Zurbriggen: CHF 25.00 pro Person und Eintritt, 7-Tage-Abo CHF 150.00, Bademantel, Schuhe und Handtücher inbegriffen (`de__hotel__wellness.html.md`). Grösse widersprüchlich (1700 m² Sommer, 1000 m² Winter, an anderer Stelle 1100 m²): keine Zahl auf die Seite, das Spa wird mit seinem Angebot beschrieben.
- **Inbegriffen und Aktionen** (`de.md`, `de__hotel__preise.html.md`, `de__hotel__aktuelles.html.md`): Postautos im ganzen Saastal, Bergbahnen im Sommer «ohne Metro Alpin» (Schweiz Tourismus schreibt «auch Metro Alpin», Saas-Fee/Saastal Tourismus «ausser Metro Alpin»), Frühstücksbuffet, Racletteabend einmal die Woche bei Halbpension, Kidsclub Mo bis Sa 16:30 bis 21:00 Uhr, Parkplatz. Gratis-Anreise mit dem öffentlichen Verkehr ab zwei Nächten für Gäste aus der Schweiz, Buchungszeitraum 1. Mai bis 31. Oktober 2026. Pauschale «Top Winterzauber» CHF 999.00 ohne Saison. Aktionen an einer Stelle halten und mit Datum zeigen.
- **Lage** (`de.md`): zwei Gehminuten zum Skigebiet, drei zur Busstation und zum Dorfkern.
- **Anreise** (`de__hotel__anreise.html.md`): Zug bis Visp, Postauto mit Umsteigen in Saas-Grund, rund 45 Minuten; mit dem Auto rund 40 Minuten ab Visp.
- **Kontakt und Buchung:** Tel. +41 27 957 10 12, Fax +41 27 957 37 12, info@monte-moro.ch. Buchung über den eingebetteten Shop von seekda auf `https://www.monte-moro.ch/de/buchen.html`; die neue Seite übergibt dorthin.
- **Sprachen:** die heutige Seite in Deutsch, Englisch, Französisch; Gäste auf Booking schreiben vor allem Deutsch (46) und Französisch (29) (`_kette/03-sammler/sprachen.json`). Übersetzt wird erst in Station 15a.
- **Wie Gäste es sehen:** Google 4,5 (121), Booking 8,3 (94; Personal 9,0, Lage 9,0), beide 17.10.2026; TripAdvisor 3,9 (17, Stand 09.10.2026). Die TripAdvisor-Zahl gehört nicht auf die Seite, die Booking-Stärken schon.
- **Geschichte: offen.** Die Seite sagt nicht, seit wann es das Haus gibt.

## 4 CI und eigener Charakter

- **Wortmarke:** `_quelle/website/bilder/allgem_logo.png` (1161 × 475, blau): zwei Gipfel als «MM», darunter «Monte Moro» in einer schmalen Groteske und «Saas-Almagell». Als Vektor gezogen für die Dokumente der Kette: `_kette/02-spaeher/_bau/assets/logo/logo.svg` und `zeichen.svg` (nur die Gipfel). Die Titelschrift leitet Station 5 daraus ab.
- **Farben, gemessen, nicht festgelegt:** Logo-Blau `#115595` (häufigste Farbe der Wortmarke); Lärchenholz der Stube `#b77f49` (Median der warmen Töne in `restau_*.jpg`); Fassade mit Holzbalkonen in Orange-Braun und weisser Wand (`_quelle/extern/myswitzerland/myswitzerland-00072098_m.jpg`). Die heutige Seite arbeitet mit hellem Blau, Mintgrün in den Geschenk-Kacheln und Grau; als Hausfarben belegt ist davon nur das Blau des Logos. Zwei Farbwelten legt Station 5 vor.
- **Charakter:** das unkomplizierte Haus derselben Gastgeber. Familien, Wanderer, Skifahrer, ein Restaurant mit Rösti, Raclette und Walliser Wein, und wer will, geht nebenan ins grosse Spa. «Mehr erleben, weniger zahlen» sagt das Haus selbst. Herzlich und direkt, leichter und heller als das Wellnesshotel, mit weniger Kapiteln.
- **Bilder, ehrlich:** Das beste Bild ist die Fassade im Sommer bei Schweiz Tourismus, 3734 × 2447 px, scharf (`extern/myswitzerland/myswitzerland-00072098_m.jpg`); es trägt ein grosses Fenster und den ersten Eindruck. Gut: 11 Fotos vom Haus auf TripAdvisor, 2000 px (Fassade Sommer und Winter, Raclettestübli, Zimmer, Frühstück). Die 88 Bilder der Seite sind höchstens 1280 px breit, viele als breite Bildreihen; Booking liefert 37 Bilder bis 1440 px. Die Zimmerfotos wirken älter (warme Gelb- und Orangetöne). Region-Bilder ohne Herkunft, Wellness-Bilder zeigen das Partnerhotel. Instagram nur 640 px.
- **Filme:** Ein eigener Hotelfilm fehlt. Der Kanal «Fabian Zurbriggen» zeigt «Wallis Baby» (09.10.2026) mit Szenen im Röstihüs (`_quelle/video/familie/`): als Film im Bild mit Start per Klick denkbar, nie als Hintergrund, nur auf mein Wort. Gäste-Videos nie auf die Seite.
- **Denkanstösse, keine Vorgabe:**
  - ein erster Moment mit der Sommerfassade und der Zeile vom Preis
  - «Was ist inbegriffen?» als grosses, klares Kapitel (Bergbahnen, Postauto, Anreise, Kidsclub, Raclette)
  - das Röstihüs als eigenes Kapitel mit der Karte auf einem Blatt Papier, die Röstis mit ihren Namen (Albert, Dracula, Macugnaga, Tschug Tschug …), Bögen nur beim Essen
  - Fabians Hotelweine als kleine Geschichte am Tisch
  - die zwei Ferienhäuser nacheinander
  - der kurze Weg ins Spa nebenan

## 5 Bilder, Videos, Texte

- Auf die Seite kommen nur echte Bilder des Hauses: `_quelle/website/bilder/`, `_quelle/extern/myswitzerland/`, `_quelle/extern/booking/`, `_quelle/extern/tripadvisor/vom-hotel/`, `_quelle/extern/ig/`. Zu jedem verwendeten Bild kennst du Datei und Herkunft (`herkunft.json`).
- `gaestefotos/` und `video/gaeste/` gehören den Gästen. Sie zeigen, wie das Haus wirklich aussieht, und kommen nie auf die Seite.
- Kein laufendes Video hinter einer scrollenden Fläche (Regel 55).
- Erster Eindruck, grosse Hintergründe und Fenster sind immer echte Fotos, in voller Quellbreite gerechnet und nachgeschärft. Abdunklung ins Bild gerechnet statt als Verlauf darüber.
- Erzeugte Bilder nur auf mein Wort und nur als Platzhalter. Dann nach Master 2.4 und Regel 53/54.
- Fakten, Namen, Preise, Zeiten werden nie abgetippt oder verschönert, sondern aus dem Material gelesen und dagegen geprüft. Was das Haus nicht veröffentlicht, steht nicht auf der Seite. Auszeichnungen an der Quelle prüfen.
- Texte: herzlich, direkt, Schweizer Schreibung (ss statt ß, «Guillemets»), Sie-Ansprache. Keine Floskeln, keine Punkt-Etiketten über Überschriften, keine Nummern-Listen, keine grauen Kachel-Raster, keine Pillen-Reihen als Schmuck (Master 2.3 und 2.9). Jede Information steht einmal.

## 6 Vorgehen, Stück für Stück

1. **Einordnen:** Designstudie von Tasty Studios, nur lokal, `noindex`, im Fuss «Designstudie von Tasty Studios, nicht die offizielle Website». Nichts online nehmen ohne mein Wort. Die Seite kommt nach `~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/website/` (`einordnung.json` › website_ordner), eigener freier Port (vorher mit `lsof` prüfen), Start über eine eigene `serve.py` wie beim Carlton.
2. **Recherche ist abgeschlossen** (Station 3): `_kette/03-sammler/fakten.json` ist das Fakten-Blatt. Neu geholt wird nur, was gezielt fehlt.
3. **Bildauswahl:** aus allen Ordnern die besten echten Bilder je Thema, als Bogen zeigen, Lücken benennen.
4. **Markenbuch und Konzept-Board** in der Kette (Station 5 und 6). Gebaut wird erst nach meinem Wort.
5. **Website:** statischer Bau aus einem Skript, reines HTML, CSS, JS, keine Bibliothek, nativer Scroll. Inhalte an einer Stelle, Kopf und Fuss einmal. Abschnitt für Abschnitt: höchstens drei bis vier Scroll-Bewegungen, ein bewegtes Element pro Blick, nur `transform` und `opacity`.
6. **Nach jedem Abschnitt messen und ansehen:** Safari und Chrome, 320 bis 768 px und Desktop, gedrosselt (4× und 6×), nur der fertige Bau zählt. Vorher prüfen, ob der Mac im Stromsparmodus ist. Wert notieren. Im Konflikt fällt die Idee, nie die Flüssigkeit.
7. **Abnahme** nach Master Abschnitt 10: jeder Knopf geklickt, kein Weg führt auf die alte Seite, Rechtstexte im Wortlaut. Erst dann zeigst du mir die Seite, mit Adresse.
8. **Am Ende:** meine Korrekturen ins Lernprotokoll der Master-Datei (Abschnitt 11).

## 7 Wie du mit mir arbeitest

- Antworten im Chat kurz: was ist jetzt da, mit Adresse. Keine Fachbegriffe, keine Arbeitsschritte.
- «Mach das geiler» zu einem Bildschirmfoto heisst: nur diesen Abschnitt verfeinern, der Rest bleibt. Nach zwei abgelehnten Neuentwürfen zurück zum Ausgangsstand.
- Nichts behaupten, was du nicht selbst geprüft hast. Nichts abschicken, nichts veröffentlichen.
