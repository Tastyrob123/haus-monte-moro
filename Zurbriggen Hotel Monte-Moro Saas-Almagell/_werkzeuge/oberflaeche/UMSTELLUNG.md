---
tags: [projekt, website]
status: aktiv
---

# Werkzeug-Oberfläche · Walk on the Wild Side Hannover

Übernommen am 31.10.2026 (Nachtbau) aus dem Culinarium Hannover, wo der Chat `culinarium-maison` das Paket am 28.10.2026 aus dem Schäfli angelegt hat. **Einziger Schreiber dieses Ordners ist `montemoro-maison` (Der Tresen)**; das Kleid hat der Oberchef am 31.10.2026 angelegt. Paket = Stamm der Häuser (`grund.css`, `rahmen-buehne.css`, `rahmen-inseln.css`, `oberflaeche.js`, `bewegung.js`, `muster.html`), Kleid eigen: `kleid/montemoro.js` + `kleid/montemoro.css` + `kleid/montemoro-zeichen.svg` + `kleid/montemoro-marke.svg` (die Wortmarke der Bar, wie die Website sie zeigt: `website/bau.py` `LOGO` aus `_quelle/logo/montemoro-logo-nachgezogen.svg`, unverändert). Rahmen «Die Bühne»: Kopf dunkel wie die Nacht der Bar, Raum hell wie das Creme der weissen Plakate.

## Einbinden (jedes Werkzeug gleich)

Der Server des Werkzeugs liefert `/assets/oberflaeche/…` aus **diesem Ordner** und `/assets/…` sonst aus `website/assets/` (Fotos `/assets/bild/<schlüssel>-<breite>.webp`, Schriften `/assets/schrift/`). Muster: `_werkzeuge/maison/server.py` (`translate_path`, Port 9381).

```html
<script src="/assets/oberflaeche/kleid/montemoro.js?v=1"></script>          <!-- vor allem anderen, ohne defer -->
<link rel="preload" href="/assets/schrift/prata-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v=1">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v=1">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/montemoro.css?v=1">
<!-- eigenes CSS des Werkzeugs danach -->
<script src="/assets/oberflaeche/oberflaeche.js?v=1"></script>            <!-- vor dem Skript des Werkzeugs -->
```

`?v=` beim Bau aus dem Inhalt bilden (M20), nie von Hand. Gerüst und Zeichen-Funktionen (`WO.kopf`, `WO.startbild`, `WO.rand`, `WO.leiste`, `WO.knopf`, `WO.name`) wie im Stamm. Musterseite mit jedem Baustein: http://127.0.0.1:9381/assets/oberflaeche/muster.html?haus=montemoro (Server des Tresens).

## Werte des Hauses (nur lesen, nie abtippen)

- **Namen der Werkzeuge:** nur `WO.name('<teil>')` bzw. `WO_HAUS.namen` (Teile: zentrale, website, karten, gaeste, marke, besuche, druck): Der Tresen · Das Schaufenster · Die Pairing-Karte · Das Gästebuch · Das Markenbuch · Die Besucherliste · Die Plakatwerkstatt (gleicher Satz wie im Culinarium, Robert 28./29.10.2026); je Werkzeug ein Satz in `WO_HAUS.saetze`. Python-Seiten lesen sie aus `kleid/montemoro.js` (Regex auf `namen:`). Wechseln die Namen, ändert sich nur diese eine Zeile.
- **Wege und Ports:** `WO_HAUS.wege` (`/_werkzeuge/<werkzeug>/`), `WO_HAUS.ports` (9381 Zentrale … 9387 Drucksachen, 9388 Werkbank). Wege zu anderen Werkzeugen immer `http://127.0.0.1:<port>/…`, nie `localhost` (Fehlerbuch 10a); die Zentrale: `http://127.0.0.1:9381/_werkzeuge/maison/`.
- **Farben** (aus `website/assets/wild.css`, `CHARAKTER.md` 4): nur die Variablen. Dunkle Flächen `--wo-tief` (#130E0D Nacht), `--wo-nacht` (#1C1513), `--wo-nacht2` (#261E1A); Gold `--wo-gold` (#D8B264) **nur** als Haarlinie, Etikett, Knauf (Rahmen des Eckschilds); `--wo-akzent` (#7A5C24 Gold tief, Betonung auf Hell); Rot `--wo-rot`/`--wo-punkt` (#F0323F) **nur** als Punkt (Hauptknopf, Wortmarke); Raum `--wo-papier` (#EFE6D8), `--wo-blatt` (#F7F1E7), Creme der Plakate #F2E9DC; Schrift `--wo-tinte` (#1C1513), `--wo-leise` (#5E524A). Ultramarin #1A00AA nur über `.wo-dj` (DJ-Abende, SESSION-Plakate). Keine eigenen Hexwerte für Flächen.
- **Schrift:** Titel `var(--wo-titel)` = Prata (eine Stärke, nie fett, nie kursiv); Lauf `var(--wo-sans)` = Hanken Grotesk 400; Etiketten `var(--wo-etikett)` = Hanken 500 gesperrt; Zahlen `.wo-zahl` Hanken mit `tabular-nums`. Dateien `/assets/schrift/prata-latin.woff2`, `/assets/schrift/hanken-latin.woff2`. Fraunces, Urbanist, Instrument Sans, DM Mono gibt es hier nicht.
- **Form: das Eckschild.** Platten 18 px Radius mit Gold-Haarlinie innen und weichem Schatten, Kacheln 14 px; Knöpfe als Schild mit rundem Knauf: `.wo-kn--gold` = Hauptweg Rot mit Creme-Knauf, `.wo-kn--dunkel` = Nebenweg Nacht mit Goldlinie und Gold-Knauf, `.wo-kn--hell` = Creme mit Goldlinie. Über Zwischentiteln eine kurze Gold-Haarlinie, sonst kein Schmuck. Keine Einkerbungen, keine Pillen-Reihen, keine Tickets, keine Leuchtschrift, keine Sticker.
- **Zeichen und Wortmarke:** im Ring oben links (`.wo-marke-w`) die Wortmarke der Bar in Rot. Ganze Wortmarke, wo ein Werkzeug sie braucht: `<svg viewBox="0 0 1296 1600"><use href="/assets/oberflaeche/kleid/montemoro-marke.svg#wm"/></svg>`, Farbe über `color` (Rot #F0323F oder Creme). Nie als Schrift nachbauen.
- **Aussenfoto des Startbilds:** `WO_HAUS.foto` = `/assets/bild/schild-ecke-960.webp` (die Ecke Haasemannstraße am Abend); `WO_HAUS.fotoStufen` = Stufen der Website (480/960), `WO_HAUS.fotoAlt` = Alt-Text aus dem Bildregister. Weitere Fotos nur aus `website/bilder.py` (`BILDER`).
- **Texte:** die Bar duzt. Jeder Satz wertet auf (der einzelne Gast, der Drink, der Abend), nie Masse. Die Karte **wechselt** (nie «keine Karte»). E-Mail der Bar ist nicht belegt: keine erfinden.

## Änderungen

Nur `montemoro-maison` schreibt hier. Wer etwas am Kleid braucht, löst es im eigenen CSS und meldet es dem Oberchef; nie in diesem Ordner selbst ändern. Jede Änderung mit Sicherung (nicht eingecheckt) und Eintrag unten. Die Zeilen bis 30.10.2026 stammen aus dem Culinarium (Stamm, gelten hier mit).

| Datum | Was | Für wen |
|---|---|---|
| 31.10.2026 | Kleid Wild Side angelegt (Oberchef): Farben, Schriften Prata/Hanken, Eckschild-Form, Wortmarke der Bar im Ring | alle sieben |
| 31.10.2026 | `oberflaeche.js` Startbild-Foto: Stufen aus `WO_HAUS.fotoStufen` statt fest 640/1000 (die Website des Wild Side hat 480/960/1536; vorher 404 auf `schild-ecke-640/1000.webp` in jedem Startbild), Alt-Text aus `WO_HAUS.fotoAlt`; `kleid/montemoro.js` beide Werte neu. Nachgeschärft (Hinweis Oberchef/Besucherliste): grösste Stufe = die im Weg des Fotos genannte, kleine = 480 nur wenn kleiner; in allen sieben Werkzeugen und der Musterseite keine 404 mehr | alle sieben |
| 31.10.2026 | `kleid/montemoro.css`: Knopf «Bereiche» am Handy (bis 900 px) als Nebenweg des Eckschilds (Nacht, Gold-Haarlinie, 14 px) statt goldener Pille | alle sieben |
| 31.10.2026 | `kleid/montemoro.css` (Funde Markenbuch, Pairing-Karte über den Oberchef): Kopfmitte `.wo-kopf__mitte b` Zeile 1,42 statt 1,1 (Prata wurde unten abgeschnitten), Unterzeile ohne Abstand; 901–1240 px: die versteckte Beschriftung des runden Hauptknopfs liegt in der Mitte des Knaufs (1 px, clip-path) statt daneben (Regel «randlos») | alle sieben |
| 31.10.2026 | `kleid/montemoro.css` (Oberchef, «text-mitte» in WebKit): Sperrabstand optisch mittig. Grundfall symmetrisch (richtig in WebKit, das nach dem letzten Buchstaben keinen Sperrabstand anhängt); nur Chromium (`@supports (interpolate-size:allow-keywords)`) bekommt den Ausgleich: `.wo-kn>span`, `.wo-kopf__ber>span` mit `margin-right:calc(-1 * var(--wo-sperr))`, Text-Pillen `.wo-marke`, `.wo-sp`, `.wo-an__st em` und «Überspringen» im Rundgang (`.rdg-karte .rdg-zu`) mit `text-indent:var(--wo-sperr)`. **Für eigene Knöpfe:** Variable `--wo-sperr` (Sperrabstand des Knopfs in em, Standard .16em) setzen und Klasse `.wo-sperr-mitte` an den Knopf; Zeichen in `i`/`svg`/`img` rücken nicht mit. Gemessen Chromium 153: Tinte 1,12 px links → 0,12 px | alle sieben |
| 31.10.2026 | `kleid/montemoro.css` (Fund Gästebuch): Leiste unten am Handy (bis 900 px) – Hauptknopf rot mit hellem Zeichen statt gold aus grund.css | alle sieben |
| 31.10.2026 | `kleid/montemoro.css`: Hauptknopf `.wo-kn--gold` mit Creme-Knauf und rotem Pfeil (vorher dunkler Knauf aus dem Stamm), ohne hellen Schriftschatten | alle sieben |
| 28.10.2026 | Angelegt: Paket aus dem Schäfli, Kleid Culinarium, Zeichen «C» | alle sieben |
| 28.10.2026 | `kleid/montemoro.js`: lokal zeigen `WO_HAUS.wege` der anderen Werkzeuge auf `http://127.0.0.1:<port>/…` (Fund culinarium-reception); online relativ. Eigene Umschreibungen in den Werkzeugen nur noch für Wege, die mit «/» beginnen, oder ganz weg. Sicherung `kleid/montemoro.js.vor-wege-2026-10-28` | alle sechs |
| 28.10.2026 | Namen nach Roberts Wahl (Satz A «An der Bar») in `kleid/montemoro.js` (`namen`, neu `saetze`); Sicherung `kleid/montemoro.js.vor-namen-2026-10-28` | alle sieben |
| 29.10.2026 | `kleid/montemoro.js`: `namen.marke` heisst jetzt «Das Markenbuch» (Robert, über den Oberchef); Sicherung `kleid/montemoro.js.vor-markenbuch-2026-10-29` | alle sieben |
| 29.10.2026 | Startbild-Foto: srcset 640/1000 aus den Grössen der Website (bei 2× höchstens rund 2× die Anzeigebreite), erstes Startbild mit Vorrang, weitere (verborgene Ansichten) lazy, Platzhalter `WO_HAUS.fotoFarbe`; `WO_HAUS.foto` jetzt fassade-1000 statt -1600 (wer es vorlädt, lädt dasselbe Bild) | Oberchef, Leistung |
| 29.10.2026 | Bewegung für alle Werkzeuge: `bewegung.js` (vom Kleid async nachgeladen) lässt Zwischentitel, Karten, Blätter, Kacheln (`.wo-zw .wo-ag .wo-bk .wo-lage .wo-re .wo-bl .blatt .besuch .re-a .mw-t .wo__k`) gestaffelt heraufschweben, Fotos darin zoomen, Zahlen zoomen; Startbild-Auftritt in `kleid/montemoro.css` ruhiger und länger (Foto zoomt 2,6 s, Parallaxe per Scroll-Zeitachse), Knöpfe geben beim Drücken nach. Was eigene Bewegung hat (data-sw, data-r, laufende Animation), bleibt unberührt. Abschalten je Element: `data-wo-bw-nie` | Robert über Oberchef |
| 30.10.2026 | Bewegung vollständig (Kriterium 37): `kleid/montemoro.js` neu `WO_ZEILEN(el)` (Titel in Wörter mit Zeilennummer, bleibt ein Block, wenn sich der Umbruch ändern würde) und das Teilen des Startbild-Titels vor dem ersten Bild; `kleid/montemoro.css` Startbild-Titel Zeile für Zeile (0,11 s Staffel); `bewegung.js?v=2`: Zwischentitel (`.wo-zw`, `main h2`, `.wo-app h2`, `.ms-zeile > h2`) Zeile für Zeile, grosse Zahlen (ab 22 px, keine Jahreszahl) laufen von null hoch (Zwilling hält die Breite, schreibt das Werkzeug neu, gilt sein Wert), neu als Kacheln `.mk`, `.pk-karte` (Plakatwerkstatt), `.kap__b`, `.thema` (Anleitungen). Nie doppelt: alles in oder unter `[data-fd]`, `[data-r]`, `[data-sw]` bleibt dem Werkzeug, auch wenn es seine Bewegung erst später setzt. Gemessen: Tafel `_Oberchef/zeigen/culinarium/tresen-3010/`. Abschalten je Zahl: `data-wo-zl-nie` | Robert über Oberchef |
| 30.10.2026 | `bewegung.js?v=3`: `.blatt` aus der Liste genommen. In Plakatwerkstatt und Pairing-Karte ist `.blatt` das gesetzte Druckblatt, das vermessen wird (Fund culinarium-imprimerie: Schrift im PDF 3–5 mm daneben). Die Kennzahl-Blätter der Besucherliste bewegen sich selbst | alle sieben |

## 30.10.2026 (Abend) · Rand ohne ResizeObserver
- oberflaeche.js: Die Höhe des Randes (--wo-rand-top) wird nicht mehr über einen ResizeObserver nachgeführt, sondern über Mutation, Übergangsende, Aufklappen, load und Fenstergrösse (alles über ein requestAnimationFrame gebündelt, Wert nur geschrieben, wenn er sich ändert). Grund: WebKit meldete beim Laden des Schaufensters «ResizeObserver loop completed …», zusammen mit der neuen Bewegung; der Bedienlauf fiel auf 87/88. Danach 88/88 WebKit und Chromium 1440, 89/89 WebKit 390. Sicherung: oberflaeche.js.vor-ro-2026-10-30.

## Handy: Kopf-Knöpfe im Rand, Rundgang klappt den Rand auf (30.10.2026, Tor 5)
- `oberflaeche.js` `kopfImRand()`: Was der Kopf bis 900 px ausblendet (`.wo-kopf__r`), steht im Rand als `.wo-rand__kopf` noch einmal. Links mit Ziel, Knöpfe lösen den Kopf-Knopf aus. Was der Rand schon als Weg führt, steht nicht doppelt da. Den Block baut ein MutationObserver neu, wenn ein Werkzeug Kopf oder Rand neu zeichnet. Sichtbar ist er nur bis 900 px (`grund.css`).
- `WO.randZiel(e)` / `WO.randZurueck(ziel)`: Die Rundgänge (carte, bureau, registre, livre, reception/studio, maison/quelle/rundgang-vorlage) rufen sie in `sichtbar()`, in `zeige()` und in `ende()` auf. Liegt ein Ziel im zugeklappten Rand, klappt der Rundgang ihn auf. Ein kleines Ziel rückt dabei über die Karte. Beim nächsten Schritt ausserhalb des Rands und am Ende klappt der Rundgang ihn wieder zu. Einen Rand, den der Gast selbst geöffnet hat, lässt er offen.
