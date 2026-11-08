# Auftrag · Hotel Monte-Moro, Saas-Almagell (08.11.2026)

Robert: «Bitte eine Cloud-Sitzung starten, in der wir einmal die komplette Werkbank und die Werkzeuge alle bis ins Detail ausarbeiten und fertig machen.» Monte-Moro ist das erste der drei Zurbriggen-Häuser; Wellnesshotel und Suitenhotel Zermatt folgen danach nach diesem Muster (nicht hier bauen).

Du bist Oberchef dieses Hauses. Lies zuerst `CLAUDE.md` (vor allem «Der Deal», «Prüfen» und «Limit und Übergabe»), dann `_Werkzeuge/OBERCHEF-PAKET.md`, `_Werkzeuge/ROBERTS-KRITERIEN.md`, `/tmp/wildside/vorgaben/` (nach dem Klonen), `Zurbriggen Hotel Monte-Moro Saas-Almagell/UEBERGABE.md`, den Prompt des Hauses, `_kette/05-markenbauer/` (Markenbuch) und `_kette/11-werkbank/`.

**Was schon da ist:** die fertige Website (`website/`, sieben Seiten, Familienband im Fuss). Werkbank und Werkzeuge gibt es für dieses Haus noch nicht (Station 11 steht auf «wartet»).

1. **Werkbank** nach `/tmp/culinarium/Culinarium Hannover/website/_werkbank/` (mit `_Werkbank-Kit/`) für Monte-Moro bauen: alle Seiten mit Inhalt des Hauses, ohne Platzhalter.
2. **Die sieben Werkzeuge** aus `/tmp/culinarium/Culinarium Hannover/_werkzeuge/` nach `Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/` übernehmen und umkleiden: Name, Zeichen, Farben, Schriften aus Markenbuch und Website; Hauswerte eintragen (Zimmer und Preise, Röstihüs-Karte mit Röstis, Cordon bleus und Fabians Hotelweinen, Inbegriffenes, Anreise, Fotos aus `quelle`); aus der Werkbank verlinkt; Server in `cloud/haus.json` (Ports 9381–9388). Je Werkzeug ein Unteragent (`model: "opus"`), parallel, jeder mit klarem Revier.
3. **Drucksachen** der Plakatwerkstatt und der **Feed** für das Haus.
4. **Prüfen** wie in CLAUDE.md «Prüfen» (in der Sitzung, keine GitHub Actions): jedes Werkzeug gleich nach dem Bau, Funde reparieren, noch einmal prüfen; am Ende alles.
5. **Übergabe laufend:** `UEBERGABE-LIMIT.md` nach jedem fertigen Schritt nachführen und pushen. Commits auf `main` mit kurzer Nachricht, was fertig ist.

**Letzte Nachricht, genau eine:** «Fertig. <Link Werkbank> <Link Prüftafel>» – oder nur, wenn etwas fehlt: «Nicht fertig. <Links> – es fehlt: <Liste>». Keine Zwischenmeldungen, keine Begründungen, keine Technik. Deutsch, kurz, Alltagssprache.
