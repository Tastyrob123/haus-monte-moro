---
tags: [projekt, feed]
status: aktiv
---

# Feed-Bestand und Gegenprobe · Hotel Monte-Moro (Werkbank Papier, 08.11.2026)

Bau: `_Werkbank-Kit/feed.py`, `feed_druck.js`, `feed_bestand.py` (unverändert), Daten `_werkbank/feed_daten.py` (REGEL `bogen`), danach `_werkbank/feed_leicht.py`. Seite: `feed/index.html`.

## Das Profil heute

- **@hotelmonte_moro**, «Hotel Monte Moro | Restaurant Röstihüs | Saas-Almagell», 19 Beiträge, 173 Follower, 1 gefolgt (`_quelle/extern/ig/profil.txt`).
- Im Material liegen zwölf Bilder (`_quelle/extern/ig/ig-01 … ig-12.jpg`, `herkunft.json`): zehn vom Konto des Hauses (21.09.2026 bis 19.02.2026: Fabian mit Blumen, «Wallis Baby», Spiegelsee, Zimmer, «Sommerferien im Monte Moro», Gratis-Anreise, Piste, Oster-Menü des Röstihüs, Loipe, Winterweg), zwei vom Partnerhotel Pirmin Zurbriggen. Die zehn eigenen stehen im Profil der Werkbank unter den neuen («Ihr Feed heute»), die zwei des Partnerhotels nicht.
- Profilbild: das Haus hat keines im Material; das Profil der Werkbank zeigt den Bergkamm aus dem Logo (Kit).

## Bestandsabgleich

`feed_bestand.py` gegen alle zwölf Bilder in `_quelle/extern/ig/` (auch die des Partnerhotels): **17 Fotos im Feed geprüft, 0 schon gepostet, 0 doppelt im Feed** (Bericht `feed/bestand.json`). Keine Ausnahmen.

## Konzept «Am Grat» (Feed-Planer, Master 5a Regel 10a)

Das Haus erzählt sich in drei Kapiteln, je ein Panorama des Saastals über eine ganze Reihe (drei Beiträge ergeben ein Bild): der Sommer im Tal, der Winter auf den Gletschern, der Stausee Mattmark. Die Panoramen sind die Fotos der Website im Format 2,4 : 1 und passen ohne Beschnitt über drei Kacheln. Dazwischen je zwei Reihen aus dem Haus (Zimmer, Frühstück, Röstihüs, Stübli, Empfang, das Haus im Sommer und im Winter) und je Reihe genau eine Tafel mit einem Satz der Website; ihr Platz wandert (Mitte, links, rechts …). Einmal ist die Tafel der **Bon der Rezeption** mit allem, was inklusive ist, wie auf der Startseite der neuen Website.

**Warum gerade dieses Haus so:** Das Logo ist ein Bergkamm, die Website fasst jedes Bild mit der Grat-Kante; der Feed nimmt diese Linie auf, indem die Berge über die ganze Breite laufen. «Mehr erleben, weniger zahlen.» und der Bon sind der Kern des Hauses (Inklusive-Leistungen) und kommen als Tafeln.

**Gegenprobe gegen die bisherigen Feeds:** Culinarium und Wild Side: «Fortsetzung» mit 60 Beiträgen, Plakate und Schrift-Tafeln in jeder Reihe, keine Panoramen. Carlton, Doldenhorn, Ruedihus, Gasterntal (Bogen): Hochformate über zwei Reihen, Blöcke 2 × 2, Bilder über sechs Beiträge. Hier: genau drei Panorama-Reihen als Kapitel in festem Takt (Reihe 1, 5, 9), sonst nur Einzelbilder, eine wandernde Tafel je Reihe, ein Bon als eigene Tafel-Art. Erste neun Kacheln: Panorama Sommer, Haus Sommer, Tafel Nacht, Röstihüs, Bon, Frühstück, Balkon – mit keinem bisherigen Feed gleich.

## Kleid

Tafeln in Nacht (Verlauf Nachtblau → Nacht) und Papier, oben der Bergkamm in Lärche, das letzte Wort des Titels in Lärche (auf Papier Lärche tief), Messinglinie; Fjalla One, Instrument Sans, DM Mono aus `website/assets/fonts`. Wortmarke nur auf der Tafel «Willkommen im Monte-Moro.». Sie-Ansprache, Schweizer Schreibung.

## Die 30 Beiträge

Beitragstexte von Tasty Studios, nur mit Fakten aus `website/inhalt/daten.py` (keine Zeiten des Röstihüs, keine Preise ausser den veröffentlichten, keine Gratis-Anreise).

| Feld (oben links = 1) | Reihenfolge zum Posten | Stück | Satz woher | Beitragstext |
|---|---|---|---|---|
| 1 | 30 | Foto `tal-sommer` (Teil 1 von 3, Panorama) – Das Saastal im Sommer | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Das Saastal im Sommer: über 250 km Wanderwege, vom einfachen Spaziergang bis zum Viertausender. |
| 2 | 29 | Foto `tal-sommer` (Teil 2 von 3, Panorama) – Das Saastal im Sommer | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Mittendrin liegt Saas-Almagell. Das Postauto im ganzen Saastal ist bei uns im Zimmerpreis inklusive. |
| 3 | 28 | Foto `tal-sommer` (Teil 3 von 3, Panorama) – Das Saastal im Sommer | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Im Sommer auch alle Bergbahnen im Saastal, ausser der Metro Alpin. Mehr erleben, weniger zahlen. |
| 4 | 27 | Foto `haus-sommer-g` – Das Hotel Monte-Moro im Sommer, mit der Sonnenterrasse | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Das Hotel Monte-Moro im Sommer, mit den Balkonen aus Lärche und der Sonnenterrasse vor dem Haus. |
| 5 | 26 | Tafel «Mehr erleben, weniger zahlen.» | Satz des Hauses (daten.py HAUS.satz, Startseite und Preise der Website); «ab CHF 90.00» aus PREISE | Mehr erleben, weniger zahlen. Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag, Postauto und im Sommer die Bergbahnen inklusive. |
| 6 | 25 | Foto `roesti-raum` – Die Stube des Röstihüs mit den Säcken | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Das Röstihüs. Unsere Gäste sagen, hier gebe es die wohl besten Röstis und Cordon bleus der Region. |
| 7 | 24 | Tafel «Ihr Aufenthalt» | Der Bon der Rezeption (index.html, preise.html; INKLUSIVE in daten.py) | Der Bon der Rezeption: Postauto, Bergbahnen im Sommer, Frühstücksbuffet, Racletteabend mit Halbpension, Kidsclub und Parkplatz. Alles schon dabei. |
| 8 | 23 | Foto `fr-tisch` – Das Frühstücksbuffet | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Unten ist das Frühstück gedeckt. Das Buffet gehört zu jedem Zimmer. |
| 9 | 22 | Foto `balkon` – Blick vom Balkon ins Tal | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Die Sonne steht schon über dem Balkon. Alle Zimmer im Monte-Moro haben einen. |
| 10 | 21 | Foto `alpenrosen` – Alpenrosen über dem Saastal | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Alpenrosen über dem Saastal. Im Sommer ein herrliches Wanderparadies. |
| 11 | 20 | Foto `murmeltiere` – Murmeltiere im Saastal | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Murmeltiere im Saastal, gleich neben den Wanderwegen. |
| 12 | 19 | Tafel «Bei uns scheint fast immer die Sonne.» | Fuss jeder Seite der Website; SONNE in daten.py (Sonnenterrasse) | Bei uns scheint fast immer die Sonne. Dann sitzen Sie auf der Sonnenterrasse direkt vor dem Haus. |
| 13 | 18 | Foto `gletscher` (Teil 1 von 3, Panorama) – Über den Gletschern des Saastals | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Winter im Saastal: Skifahren bis auf 3500 m in Saas-Fee. |
| 14 | 17 | Foto `gletscher` (Teil 2 von 3, Panorama) – Über den Gletschern des Saastals | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Saas-Grund bis 3200 m, Saas-Almagell bis 2400 m. Drei Skigebiete in einem Tal. |
| 15 | 16 | Foto `gletscher` (Teil 3 von 3, Panorama) – Über den Gletschern des Saastals | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee, das Postauto ist inklusive. |
| 16 | 15 | Foto `haus-winter-g` – Das Hotel Monte-Moro im Winter | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Das Monte-Moro im frischen Schnee. |
| 17 | 14 | Tafel «Zwei Minuten bis zum Lift.» | index.html «Zwei Minuten bis zum Lift.»; LAGE in daten.py (2/3/3 Gehminuten) | Zwei Gehminuten zum Skigebiet Saas-Almagell, drei zur Busstation, drei ins Dorf. Das Hotel liegt an bester Lage. |
| 18 | 13 | Foto `dorf-winter` – Saas-Almagell im Winter | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Saas-Almagell im Winter. Einkaufen, Bankomat und Tourismusbüro sind drei Gehminuten entfernt. |
| 19 | 12 | Tafel «Es lebe die Tradition!» | roestihues.html, TRADITION in daten.py; «Elf Röstis und fünf Cordon bleus» = ROESTIS, CORDON | Es lebe die Tradition! Die Rösti Tschug Tschug wird mit Calvados flambiert, die Rösti Saastal kommt mit Spiegelei. |
| 20 | 11 | Foto `stuebli` – Das Raclettestübli | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Das Stübli. Einmal in der Woche ist hier Racletteabend für alle mit Halbpension. |
| 21 | 10 | Foto `z-hell` – Ein helles Doppelzimmer | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Schöne Hotelzimmer, schöne Ferien. Alle mit Dusche oder Bad, Safe und Balkon. |
| 22 | 9 | Foto `empfang` – Der Empfang mit dem Bergkamm des Hauses | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Der Empfang, an der Wand der Bergkamm des Hauses. Willkommen. |
| 23 | 8 | Foto `see-blumen` – Blumen am Mattmarksee | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Blumen am Mattmarksee. Ein Tagesausflug im Saastal, mit dem Postauto inklusive. |
| 24 | 7 | Tafel «Wein von Fabian.» | roestihues.html «Wein von Fabian»; HOTELWEINE in daten.py («wurde von Fabian selber kreiert») | Wein von Fabian: zwei Hotelweine, die Fabian selbst kreiert hat. Im Röstihüs zur Rösti oder zum Cordon bleu. |
| 25 | 6 | Foto `stausee` (Teil 1 von 3, Panorama) – Der Stausee Mattmark | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Der Stausee Mattmark. |
| 26 | 5 | Foto `stausee` (Teil 2 von 3, Panorama) – Der Stausee Mattmark | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Ein Tagesausflug aus dem Saastal, wie ihn das Haus empfiehlt. |
| 27 | 4 | Foto `stausee` (Teil 3 von 3, Panorama) – Der Stausee Mattmark | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Und am Abend zurück ins Röstihüs. |
| 28 | 3 | Foto `wasserfall` – Ein Wasserfall im Saastal | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Ein Wasserfall im Saastal. In der Alpin Gorge geht es mit einem Bergführer durch eine Gebirgsbachschlucht. |
| 29 | 2 | Tafel «Willkommen im Monte-Moro.» | anreise.html «Willkommen im Monte-Moro.»; HAUS.gastgeber in daten.py | Willkommen im Monte-Moro. Ihre Gastgeber Esther und Fabian Zurbriggen. |
| 30 | 1 | Foto `fr-detail` – Konfitüren und Brot am Buffet | Bildunterschrift aus website/inhalt/bilder.py; Text von Tasty Studios mit Fakten aus daten.py | Konfitüren und Brot am Buffet. Guten Morgen aus Saas-Almagell. |

