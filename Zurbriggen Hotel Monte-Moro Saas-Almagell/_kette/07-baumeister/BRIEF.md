---
tags: [projekt, website]
status: aktiv
---

Station 07 für Hotel Monte-Moro, Saas-Almagell · Projektordner ~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/ · gehört zur Familie Zurbriggen (Zentrale: http://127.0.0.1:8978/?familie=Familie%20Zurbriggen)

# Auftrag: Baumeister · Station 7 «Website bauen» der Kette

Haus: Hotel Monte-Moro, Saas-Almagell
Projektordner: ~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/
Website heute: https://www.monte-moro.ch

Du arbeitest für mich (Robert, Tasty Studios) als **Baumeister** in der Kette: ein Haus, zwölf Rollen, Station für Station, jede Rolle ein eigener Chat. Du bist Station 7. Vor dir: der Konzepter (Station 6). Nach dir: der Bildmacher (Station 8), parallel der Prüfer (Station 9). Arbeite durch bis zum Ende, ohne Zwischenfragen. Was du nicht weisst oder nicht belegen kannst, bleibt als «offen» im Paket stehen, nicht als Frage im Chat. Ich lese dein Ergebnis auf der Karte der Kette und bestätige dort.

## 1 Zuerst lesen, vollständig

1. `~/SecondBrain/CLAUDE.md`, besonders Regel 52 (nur Ergebnis im Chat), 54 (kostenlos zuerst, keine Unteragenten), 55 (Flüssigkeit), 57 (erst prüfen, dann sagen), 58 (nichts abschicken), 59 (Design-DNA), 60 (Website-Bau), 61 (verschickt bleibt online).
2. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Briefing — Roberts Standard.md" ganz. Das ist mein Standard; wer ihn gelesen hat, braucht keine hundert Kleinkorrekturen.
3. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md": Abschnitt 1 (die Zeile deiner Station in der Tabelle), Abschnitt 13 (die Kette, besonders 13.2 und 13.5) und die Abschnitte unter Punkt 5 ff.
4. `~/Desktop/Website-Projekte/_Kette/LIESMICH.md`: Format der Pakete, `stand.json`, `briefing.json`, `kette.py`.
5. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Bau — Standards & Ablauf (Master).md", Abschnitt 1: Schritt 7 und «Zu Schritt 7» (statischer Bau aus einem Skript, Inhalte an einer Stelle, Kopf und Fuss einmal); Abschnitt 2 ganz, 3, 3a, 4, 6, 9, 9b, 9c; Abschnitt 13.5 Regel 4 (Station 7 läuft abschnittsweise).
6. "~/SecondBrain/04 Ressourcen/Design & Look & Feel/Website-Briefing — Roberts Standard.md" ganz, noch einmal mit Stift: 4 (Aufbau), 5 (Gestaltung), 6 (Bausteine), 7 (Bilder), 8 (Bewegung, 8.2 Standard-Rezept, 8.4 nie), 10, 11 (wiederkehrende Fehler von Claude), 12 (Handy), 12b (Technik-Fallen), 13 (Abnahme).
7. `~/SecondBrain/00 Kontext/Design-DNA — Vibe & Einflüsse.md` (Regel 59). CLAUDE.md Regel 55 ganz (Flüssigkeit, das Manifest) und 60h (UI-Fundus fortschreiben).
8. Referenzbau: `~/saltandsilver-website/` (`site/assets/css/main.css` mit Kommentarzeile je Block, `main.js`, `bilder.js`, `_qa/`). Die Machart der Familie, wenn `konzept.json` eine nennt (Nachbarordner). Der UI-Fundus (https://tasty-ui-fundus.vercel.app, lokal 8957): Bausteine beim Namen nehmen, Code von dort.
9. **Projekt Nummer 10 (Robert 15.10.2026, Master 2.1 und 13.5 Nr. 9, Website-Briefing Satz 1):** Jedes Haus bekommt eine eigene Welt, kein Haus bekommt das System. Deshalb liest du vor deiner Station die Konzepte und Baustein-Listen **aller bisherigen Häuser**: den UI-Fundus unter «Bereiche» (https://tasty-ui-fundus.vercel.app, lokal `~/Desktop/Website-Projekte/_UI-Fundus/`, dort je Haus jeder Bereich, wie er gebaut wurde) und `konzept.json` bzw. `_kette/06-konzepter/konzept.json` in jedem Nachbarordner unter `~/Desktop/Website-Projekte/` (Carlton-Europe, Grand Beau-Rivage, Hotel Seiler au Lac, Waldhotel Doldenhorn, Landgasthof Ruedihus, Berghotel Gasterntal, Salt & Silver, Tasty Grand Hotel). Du schreibst dir eine Liste: welcher Auftakt, welche Zimmer-Darstellung, welche tragenden Bausteine, welche Bewegung, welcher Rhythmus bei welchem Haus schon steht. Fundus und Bausteine sind Vorrat, nie Bauplan.
10. Die Pakete davor: `konzept.json` und `konzept.html` (Station 6), `marke.json` und `marke/probe.html` (Station 5), `fakten.json` (Station 3), `seitenliste.json` und `einordnung.json` (Station 2, dort `website_ordner`), `Prompt — [Name].md` des Sammlers (gleiche sieben Abschnitte wie bei allen Häusern; sein Abschnitt «Vorgehen und Arbeitsweise» gilt). Hat das Haus schon eine gebaute Seite im Projektordner (Carlton-Europe, Hotel Seiler au Lac): zuerst deren `UEBERGABE.md` oder `STAND.md`, nichts davon neu erfinden.

## 2 Bevor du anfängst

- Lies das Paket der Station davor vollständig: `~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/_kette/06-konzepter/` (alles, besonders `offen` in `stand.json` und das Briefing). Was dort offen ist, bleibt offen, bis es belegt ist.
- Lies die Nutzungsanzeige des Abos ab und merk dir den Prozentwert des Wochen-Budgets (`budget_vorher`). Nicht schätzen; wenn du sie nicht ablesen kannst, bleibt der Wert leer.
- Setz deinen Stand auf «läuft»:
  ```bash
  python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 läuft
  ```
  Weigert sich das Werkzeug, weil die Station davor nicht bestätigt ist: aufhören und mir das in einem Satz sagen. Die nächste Rolle startet erst nach meiner Bestätigung.
- Freien Port für den lokalen Server des Hauses wählen (`lsof -iTCP -sTCP:LISTEN`), `serve.py` wie bei den anderen Häusern anlegen, Port in die Notiz von `stand.json` und in die Übergabe-Datei des Projekts schreiben.

## 3 Aufgabe

**Erlebnis statt Abschnitte (Robert 17.10.2026, Grundlage der Arbeit, Master 2.1 erste Regel, Website-Briefing Satz 17).** Die Startseite ist eine Geschichte aus einem Guss, keine neu sortierte Gliederung der heutigen Seite: ein Faden vom Auftakt bis zum Schluss, jeder Teil beginnt dort, wo der vorige aufhört, wechselnde Einstiege statt Zeichen-Überschrift-Untertitel in jedem Teil, keine Leerflächen zwischen den Teilen, Umfang wie die Startseite des Grand Beau-Rivage (rund 24 Bildschirme am Rechner, Bildgruppen mit vielen echten Fotos). Ist die heutige Seite des Hauses schon gut, nennst du, womit wir darüber hinausgehen.

Die ganze Website, Abschnitt für Abschnitt, mit Fundus und Entwurfs-Maschine, eine Geschichte aus einem Guss.

**Bauweise.** Statischer Bau aus `bau.py` in den Ordner aus `einordnung.json` (`website_ordner`, bei neuen Häusern `website/`): reines HTML, CSS, JS, keine Bibliothek, nativer Scroll. Inhalte (Zeiten, Adressen, Preise, Namen, Karten) liegen an einer Stelle (`inhalt/`) und jede Seite liest von dort; Kopf und Fuss gibt es einmal. Gestaltung in einer Datei mit Kommentarzeile je Block. Bilder leicht ausgeliefert (Liefergrössen, Lader mit Reihenfolge, kleines echtes Abbild als Grund, nie aufblenden aus Schwarz). Rechtstexte Byte für Byte aus `_quelle/` (`fakten.json › rechtstexte`), nie von uns geschrieben. Buchungsmasken bleiben, alle anderen Links führen auf neue Seiten. Vor jeder Änderung an Bestehendem eine Sicherung.

**Abschnittsweise, so läuft Station 7:**
1. Die Abschnitte aus `konzept.json` anlegen, in Reihenfolge der Seite:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py teil "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 auftakt "Auftakt"
   ```
2. Je Abschnitt: `kette.py stand "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 läuft --teil auftakt` → bauen (Baustein beim Namen aus dem Fundus, Bewegung nach 8.2, Fläche nach dem Board) → selbst prüfen (Chromium und WebKit, 1440 × 900 und 390 × 844, unsichtbar; Konsole leer, kein seitliches Überlaufen, nach dem Scrollen nichts unsichtbar, Bilder rechtzeitig, kein Flackern) → **messen** (4-fach und 6-fach gedrosselt, Bildrate beim Scrollen, p95 je Bild, Ladegewicht; Stromsparmodus vorher aus; nur am fertigen Build, nie im Entwicklungsmodus) → Eintrag in `abschnitte.json` vervollständigen (`seite`, `baustein`, `messwert`) → die Adresse des Abschnitts eintragen, **mit Sprungmarke zum Abschnitt, kein Bild** (`python3 ~/Desktop/Website-Projekte/_Kette/kette.py adresse "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 "http://127.0.0.1:<Port>/index.html#auftakt" --teil auftakt`; jeder Abschnitt hat dafür eine `id`) → `kette.py stand "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 "liegt vor" --teil auftakt`. Ich öffne auf der Karte den Abschnitt selbst und scrolle darüber.
3. Du wartest nicht auf meine Antwort, du baust am nächsten Abschnitt weiter; ich bestätige in meinem Tempo auf der Karte. **Kommt ein Abschnitt zurück, hat er Vorrang vor allem Neuen:** Satz lesen (`rueckgaben` in `abschnitte.json`), nur diesen Abschnitt ändern, das Umfeld bleibt (Website-Briefing 2: «mach das geiler» zu einem Bildschirmfoto heisst dieses Stück). Nach zwei abgelehnten Neuentwürfen zurück zum Ausgangsstand und mir das sagen. Jedes Nein ist eine Regel: steht schon im Lernprotokoll, du musst es nicht noch einmal ablegen.
4. Unterseiten genauso, jede als eigener Abschnitt oder in Gruppen (`zimmer-classic`, `anreise`, `kontakt`, `rechtstexte`). Alles, was der Kunde heute hat, gibt es neu; `seitenliste.json` ist die Prüfliste.
5. **Eigene Bausteine je Haus (Projekt Nummer 10):** Die Entwurfs-Maschine ist kein Notnagel, sondern Pflicht: Für die tragenden Abschnitte dieses Hauses (Auftakt, Zimmer-Darstellung, der Abschnitt, der die Welt des Hauses trägt) entstehen eigene Bausteine, die es bei keinem bisherigen Haus gibt; der Unterschied aus `konzept.json › unterschied` wird gebaut, nicht nur behauptet. Was der Fundus nicht hat, entsteht in der Entwurfs-Maschine (`website/_varianten/<name>.html`, mehrere Fassungen mit echten Bildern, ich wähle per Nummer), und wandert, sobald es auf einer Seite im Einsatz ist, in den Fundus (Regel 60h: `bereiche.py`, `aufnahmen.js`, `abschnitte.js`, `site/style.css`, `bau.py`, Deploy aus `site/`). Ohne diesen Schritt ist Station 7 nicht fertig.
6. Station 7 liegt als Ganzes vor, wenn jeder Abschnitt «liegt vor» oder «bestätigt» ist, jede Seite der Seitenliste neu existiert, kein Link ins alte Design führt und die Fundus-Einträge gemacht sind.

**Rückläufe vom Prüfer (Station 9):** Schickt ich Station 9 zurück, liest du `_kette/09-pruefer/pruefung-website.md`, setzt die betroffenen Abschnitte wieder auf «läuft», behebst genau die Funde, lieferst sie neu; der Prüfer läuft danach wieder. Du prüfst deine Behebungen selbst, aber die Abnahme ist seine.

**Mehrwert-Runde (Robert 16.10.2026, Master Schritt 7a): nicht in den ersten Bau einbauen.** Erst wenn die Website steht und ich sie gesehen habe, stelle ich dir die Frage getrennt: «Was sind alles noch coole Erweiterungen …, mit noch mehr Mehrwert?» Dann liest du Haus, Umgebung, Konzept und das ganze Material noch einmal und legst nummerierte Ideen vor, je Idee ein Satz plus Beleg. Ich nicke je Nummer ab; erst dann baust du, je Idee ein Teil `erw-…` auf der Karte.

**Zusatz 17.10.2026:**
- **Gewählte Fassung 1:1.** Nennt Robert eine Nummer aus einer Varianten-Seite, kommt genau diese Fassung auf die Seite, mit denselben Massen, Schriftgrössen und derselben Lage. Nichts «verbessern». Danach Vorlage und Seite in derselben Breite nebeneinander ansehen.
- **Fotos.** Zimmerfotos immer von der Zimmerseite des Hauses, nie aus der Galerie, denn dort sind Kategorien oft falsch belegt. Kein Foto kommt auf einer Seite zweimal vor. Jedes Foto wird gegen seine Bildunterschrift angesehen. Nach einem Tausch prüfen, ob die ausgelieferte Datei wirklich neu ist (Master Lernprotokoll 17.10.2026, Castell Mehrwert-Runde).

## 4 Dein Paket: `_kette/07-baumeister/`

- `abschnitte.json` (ein Eintrag je Abschnitt, Format LIESMICH 3b, mit `adresse` = Link mit Sprungmarke). Keine Bilder der Seiten im Paket; Messungen und Prüf-Aufnahmen liegen in `_qa/`.
- Die Website selbst im `website_ordner` des Projekts (`bau.py`, `inhalt/`, `assets/`, `serve.py`, `_qa/` mit deinen Messskripten, `_varianten/`, `_sicherung/`), dazu eine `UEBERGABE.md` im Projektordner (Stand, Port, was wo liegt, Sicherungen), wie bei den anderen Häusern.

## 5 Am Ende: Stand, Verbrauch, Briefing

1. Offene Punkte je einzeln eintragen (Punkt plus Fundstelle):
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py offen "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 "Was fehlt oder nicht belegt ist" "wo es gesucht wurde"
   ```
2. **Das Dokument selbst ist das Briefing** (Robert 15.10.2026: «Ich will den Link zur Landingpage und nicht so eine dumme Übersicht mit irgendwelchen Screenshots.»). Dein Dokument ist eine fertige Seite auf dem Stand der Rivage-Werkbank (Abschnitt 6, erster Punkt), online oder lokal; die Adresse trägst du ein, die Karte öffnet sie direkt:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py adresse "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 "<Link zur Seite>"
   ```
   Lokale Seiten im Hausordner sind über `http://127.0.0.1:8978/haus/Zurbriggen Hotel Monte-Moro Saas-Almagell/…` erreichbar. Keine `briefing.html` mit Bildschirmfotos oder Zusammenfassung davor.
3. Nutzungsanzeige wieder ablesen und eintragen:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py verbrauch "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 <vorher> <nachher>
   ```
4. Stand auf «liegt vor» mit einem Satz:
   ```bash
   python3 ~/Desktop/Website-Projekte/_Kette/kette.py stand "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07 "liegt vor" --notiz "Ein Satz, was jetzt vorliegt."
   ```
5. Karte starten, falls sie nicht läuft (`python3 ~/Desktop/Website-Projekte/_Kette/karte/server.py`, Port 8978), deine Station dort öffnen (http://127.0.0.1:8978/?haus=Zurbriggen Hotel Monte-Moro Saas-Almagell) und ansehen: die Seite erscheint direkt, jede Lücke rot, kein Fehler in der Konsole. Erst dann melden. Je Abschnitt ein Link mit Sprungmarke, nicht je Website; die Adresse der Station ist die Startseite des Entwurfs.

Ich bestätige auf der Karte mit «so lassen (je Abschnitt)» oder schicke mit einem Satz zurück. Kommt es zurück: Satz lesen (steht in `stand.json` unter `rueckgaben` und im Lernprotokoll der Master-Datei), genau das ändern, nichts drumherum, wieder «läuft» → «liegt vor».

## 6 Regeln, die nicht verhandelbar sind

- **Nichts verschicken, nichts veröffentlichen, nichts online stellen.** Keine Mail, keine Nachricht, kein Formular, kein Upload. Der letzte Knopf bleibt meiner (Regel 58, 61; Station 16).
- **Keine Zahl erfinden, nichts schätzen.** Jede Angabe hat eine Quelle (Datei im Projektordner oder Adresse mit Datum) oder heisst «offen». Zahlen, an denen etwas hängt, zweimal unabhängig prüfen (Regel 57).
- **Nichts löschen, nichts überschreiben,** was ein anderer angelegt hat: Pakete anderer Stationen, `_quelle/`, Sicherungen, Upload-Ordner, Bild-Streifen verschickter Mails. Du schreibst nur in `_kette/<dein Ordner>/` und in die Ordner, die dein Paket nennt. Vor jeder Änderung an Bestehendem eine Sicherung daneben (`*.vor-<was>-<datum>`).
- **Nicht am Original des Kunden vorbei.** Namen, Preise, Zeiten, Rechtstexte, Formulierungen kommen aus seinen Dateien in `_quelle/` und werden dagegen geprüft, nie abgetippt oder verschönert (Regel 60d). Was der Kunde nicht hat, bauen wir nicht dazu.
- **Bauer und Prüfer sind nie derselbe Chat.** Du prüfst nicht ab, was du selbst gebaut hast, und baust nicht nach, was du prüfst.
- **Jedes Dokument hat den Stand der Rivage-Werkbank (Regel 13.5 Nr. 13, Robert 15.10.2026: «Alle Dokumente … sehen nicht so aus wie beim Rivage. Nicht so geil, nicht so schön, nicht so luxuriös.»).** Bevor du ein Dokument baust, öffnest du http://127.0.0.1:8940/werkbank/ (Master 5b) und legst es daneben. Du baust mit dem Werkbank-Kit (`~/Desktop/Website-Projekte/_Werkbank-Kit/kern.py`, `werkbank.css`, `seiten.css`; Haken wie in `Grand Beau-Rivage/website/_werkbank/haus.py`), nicht mit eigenem CSS. Woran Robert den Stand erkennt: Titelschrift des Hauses mit Betonung in Gold oder Taupe · Tapete als zartes Gitter mit Medaillon aus dem Zeichen, nie ein grosses freies Motiv · Blätter mit runder Kante, hell und dunkel im Wechsel · Platten mit Kuhle statt flacher Felder · Fenster mit Foto und Satz · Geräte aus Blender mit echtem Inhalt · Farbkarten mit dem Foto, aus dem die Farbe kommt, und den abgeleiteten Tönen darunter · Fächer, Band zum Blättern, Laufzeile · Knöpfe mit Tiefe und Glanz · Abschnittsköpfe mittig mit dem Zeichen in Gold · Auftritte federleicht von unten. Flache Flächen, Groteske als Titel, Textblöcke und Farbfelder ohne Foto: nicht fertig, kommt zurück.
- **Keine Bildschirmfotos gebauter Seiten** in Meldungen, Briefings oder auf der Karte (Robert 15.10.2026: «Ich will auf die Seiten selber gucken, ich will drüber scrollen. Gib mir da keine Screenshots von den Seiten.»). Keine Scroll-Streifen, keine Ausschnitte, keine Rechner/Handy-Paare. Eine Seite wird nur als Link gezeigt (online oder lokal über den Server der Karte). Bildschirmfotos bleiben Prüfwerkzeug in `_qa/` und in Prüfberichten.
- Keine bezahlten Werkzeuge, wenn ein kostenloses geht (Regel 54), keine Unteragenten, keine Workflows. Im Vault wird nichts angelegt, keine Notiz, kein Todo (Regel 27b); Erkenntnisse kommen ins Paket. Chrome nie in den Vordergrund, Messungen und Aufnahmen nur unsichtbar (Playwright, `NODE_PATH=~/Aussen-Pruefung/node_modules`, Helfer `~/Desktop/Website-Projekte/_Kette/aufnahme.js`), nie `pkill` auf Chrome (Regel 49).
- Flüssigkeit über allem (Regel 55): nur `transform` und `opacity`, ein Element in Bewegung pro Blick, kein Weichzeichner, Verlauf, Schatten oder Transparenz über Bewegtem, keine Layout-Werte animieren, kein Umbau des Scrollverhaltens, kein Autoplay-Video als Hintergrund. Im Konflikt fällt das Feature, nie die Flüssigkeit; Gestrichenes in `abschnitte.json` unter `gestrichen` eintragen.
- Bewegung ist Pflicht von der ersten Fassung an (8.2): Bilder schweben deckend von unten, pulsieren einmal, zoomen im Rahmen; Überschriften rollen aus dem Schlitz; nie seitwärts, kein Vorhang, Texte nie überblenden, Überschrift läuft nicht mit.
- Nur echte Bilder des Hauses, das Haus selbst zuerst. Erzeugte nur auf mein Wort, als Platzhalter benannt. Fotos ganz, nie freigestellt. Kein Bild aus einem anderen Haus.
- Nichts sieht nach KI aus: keine Punkt-Etiketten, Nummernlisten, grauen Kachelraster, Pillen-Reihen, Requisiten, Werbesätze. Text neben Bild als geschlossener Block mittig, Kachel rechts nie kleiner als der Text. Nichts hängt lose, nichts ist leer.
- Ticket/Billett nur beim Carlton und beim Grand Beau-Rivage. «Zur Werkbank» nie auf der Website.
- Kein Abschnitt eines bisherigen Hauses in neuen Farben. Gleicher Baustein in gleicher Folge wie bei einem anderen Haus ist ein Fund des Prüfers und kommt zurück.
- Nichts geht online. Der Entwurf läuft lokal; online nimmt nur ich (Station 16). Auch keine «Vorschau» auf Vercel ohne mein Wort.
- **Keine Einkerbungen** (Robert 18.10.2026, Markenbuch Monte-Moro: «Keine Einkerbungen benutzen bei den neuen Projekten, bitte. Die müssen wir jetzt mal austauschen.»). Keine Kachel, kein Foto und keine Fläche mit ausgeschnittener Ecke oder eingekerbtem Etikett, auch nicht für Bildnamen, Zahlen oder Gruss; Beschriftung je Haus anders lösen. Helle Muster und Tapeten nie weiss auf weiss, immer mit sichtbarem Untergrund. Master Abschnitt 2.3, letzter Absatz.

## 7 Meldung an mich

**Name plus klickbarer Link zur Seite, sonst nichts** (Robert 15.10.2026). Also: «Markenbuch Castell Son Claret: <Link>». Keine Zusammenfassung, kein Ablauf, keine Ursachen (Regel 52). Offene Punkte stehen in `stand.json` und auf der Karte, nicht im Chat. Je Abschnitt genügt beim Melden: «Auftakt liegt vor, 118 Bilder/s.»


## Gilt zusätzlich (Robert 18.10.2026)

- Start auf Roberts Wort im Kette-Chat: «Kannst du bitte erstmal mit den anderen drei weitermachen?» (06 bestätigt).
- Das Konzept-Board 06 mit allen Erweiterungen ist der Bauplan («yes hinzufügen alles»).
- Erst zeigen, dann bauen: nach jedem fertigen Abschnitt Bilder + eine Zeile in `~/Desktop/Website-Projekte/_Oberchef/zeigen/kette/LISTE.md`; Neues, das nicht im Board steht, nur als Idee an den Kette-Chat.
- Keine Einkerbungen, helle Muster nie weiss auf weiss (Master 2.3). Wellness: kein Pink/Magenta («in der ganzen CI ein kompletten Stilbruch»).
- Telefone und Rechner aus Blender gerade (Master 1b Nr. 17), höchstens ein Blender-Lauf zur Zeit (`pgrep -x Blender`).
- Nichts online, nichts verschicken. Meldung und Fragen nur an den Kette-Chat.
- Die Familienseite zurbriggen.ch macht der Kette-Chat ganz zum Schluss; im Fuss nur auf die Häuser verweisen.



## NEUER WEG 18.10.2026 ~02:20 · gilt vor allem darüber

Robert: «Wellness & Spa … nur der hier ist leider cool. Also da finde ich es richtig cool umgesetzt, die Kreativität und die Ideen einfallsreich … Da sieht man genau, da wurde eine Website gebaut mit richtig geilen Animationen, wie ich es machen würde, aber genau für die Marke passend und auf den Stil … Kannst du die anderen beiden bitte auch noch so machen? … das Monte Muro und das Zermatt Hotel, die sind beide, sehen nach Baukasten aus. Die sehen schon wieder aus wie die anderen Hotelseiten.»

**Beispiel für die Herangehensweise (kein Massstab, keine Vorlage, Robert hat sie noch nicht bearbeitet): die Startseite Wellness & Spa Pirmin Zurbriggen** (http://127.0.0.1:8946/, Ordner `~/Desktop/Website-Projekte/Zurbriggen Wellnesshotel Saas-Almagell/website/`). Erst ganz ansehen und den Code lesen. Was dort trägt: jeder Abschnitt ist ein **Gegenstand aus der Welt dieses Hauses mit eigener Bewegung** (Wegweiser für die Lage, runde Bildfenster wie die Holzscheiben von Heinz Julen, offene Menümappe, Wärmeleiter, Grössenleiter für die Zimmer, Kugeln für Auszeichnungen, Kofferanhänger fürs Gepäck), dazu warme Tiefe, viel Bild, wechselnde Formen. **Keinen dieser Einfälle übernehmen**: dein Haus bekommt eigene Gegenstände aus seiner eigenen Welt, auf demselben Niveau.

Deine Startseite ist heute ein Baukasten: rechteckige Bildkarten in Reihen, Bildgruppen, Text neben Foto, Fenster, wie die bisherigen Hotelseiten. Bau sie neu, Abschnitt für Abschnitt, Inhalte und Erweiterungen aus deinem Board 06 bleiben. Heutigen Stand vorher sichern (`website.vor-neubau-2026-10-18/`).

**Ideen als Startpunkt (vom Kette-Chat, prüfen, verwerfen oder besser machen; nur Belegtes):**
- Auftakt: die Sonne geht hinter dem Haus auf. Das Haus ist freigestellt (`~/Desktop/Website-Projekte/Familie Zurbriggen/proben2/mm-vorne.png`, Himmel transparent, aus myswitzerland-00072098), dahinter steigt beim Laden ein warmer Sonnenschein über den Bergkamm, Titel «Mehr erleben, weniger zahlen.» zwischen Himmel und Haus. Satz des Hauses: «bei uns scheint fast immer die Sonne».
- Was im Preis steckt: ein Kassenbon, der aus einem Schlitz gedruckt wird, Zeile für Zeile, unten «inklusive» statt Summe.
- Lage: der Bergkamm des Saastals als feine Reliefkarte (Robert hat die Bergkamm-Linie gewählt), darauf Gehminuten zum Lift, Bus und Dorf.
- Zimmer: das Schlüsselbrett der Rezeption, je Schlüssel eine Zimmerart; antippen öffnet das Zimmer.
- Röstihüs: die Jutesäcke mit den Gesichtern als Träger der Karte, die Rösti-Namen wie auf Sackleinen gedruckt.
- Kidsclub: die alten Gondelkabinen (Foto des Hauses) fahren an einem Seil durch den Abschnitt, in den Kabinen 16.30 und 21.00.
- Bergbahnen inklusive: Liniennetz der Saastaler Bahnen mit Stempel «inklusive».
- Anreise: Fallblatt-Anzeige wie am Bahnhof (Zug bis Visp, Postauto, Saas-Grund, Saas-Almagell), die Zeichen klappen um.

Regeln: Master 2.1 erster Punkt (Kein Baukasten, Beispiel Wellness), Briefing 8 Bewegung (Bilder fliegen herein, Texte pulsieren, federn, zoomen, Titel aus dem Schlitz), Regel 55 Flüssigkeit, keine Einkerbungen, keine Bögen oder Kreise als Ersatz für Kacheln, keine Tickets (Carlton/Rivage), keine Polaroids (Salt & Silver), keine Einfälle der Wellness-Seite. Vor dem Melden neben die Wellness-Seite und alle bisherigen Häuser legen: fühlt es sich nach «schon gesehen» an, ist es nicht fertig. Nichts online. `kette.py weiter "Zurbriggen Hotel Monte-Moro Saas-Almagell" 07`, nach jedem Abschnitt Bilder und eine Zeile in die LISTE, Meldung an den Kette-Chat, wenn die Startseite steht.

## VERFEINERUNG 18.10.2026 · edel statt verspielt (Robert)

Robert zu den drei neuen Startseiten, wörtlich: «deutlich besser … die sprechen alle eine andere Sprache, das finde ich sehr gut … verschiedene Visuals … Fussabdrücke … diesen Zacken zwischen Übergängen … alles sehr cool, aber … es ist zu verspielt, es ist zu kindisch teilweise. Auch diese Umsetzung mit diesen Türen, die aufgehen, diesen Gondeln, die da langfahren. Das ist alles cool, aber es ist nicht schön umgesetzt, es ist nicht elegant umgesetzt … wir müssen dann noch diesen luxuriösen, tasty, edligen Stil da hinbekommen. Und jetzt gerade fühlt es sich irgendwie so Smallland von Ikea.»

- Einfälle, Faden, eigene Sprache, Fussspuren und Zacken bleiben.
- Ausführung nach Master 2.1 Punkt 6 «Einfall ja, Kinderzimmer nein»:
  - keine CSS-Comic-Gegenstände;
  - stattdessen echtes Foto, feine 1-px-Linie (Messing, Gold oder Silber) oder ein hochwertiger Render (höchstens ein Blender-Lauf zur Zeit);
  - ruhige Farben, viel Raum, grosse Schrift;
  - Bewegung langsam und weich, ohne Hüpfen.
- Prüffrage: Würde das Haus diese Seite in einem Luxusmagazin zeigen?
- Bilder in die LISTE, nichts online, Meldung an den Kette-Chat, sobald die Startseite steht.

## KRITIK 18.10.2026 ~20:23 · Robert zur ganzen Startseite (Bilder in robert-2026-10-18-2021/)

Den Auftrag mit 15 Punkten hat die Projektleitung per Nachricht erhalten.

- Hero: hochwertig statt Preis-Spruch.
- Zimmer: viele grosse Bilder, kein Fenstereffekt.
- Kassenbon: schneller, links dichter.
- Lage: spektakulärer.
- Winterbild: Rahmen mit mehreren Bildern, wie das Ruedihus.
- Bergbahn: neu denken.
- Röstihüs und Menü: neu.
- Kinder: Preisliste und Bild neu.
- Wein: mehrere Bilder.
- Spa: eigener Bereich.
- Bewertungen: neu.
- «Gut zu wissen»: eleganter.
- Haus-Finder: mit Bildern.
- Anreise: lesbar.
- Footer: mit dem Familienband (FAMILIEN-FOOTER.md).
- Regel: Master 2.1 Punkte 6a und 6b.
