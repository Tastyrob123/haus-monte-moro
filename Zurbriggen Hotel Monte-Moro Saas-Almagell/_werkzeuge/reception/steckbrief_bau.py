#!/usr/bin/env python3
"""Steckbrief für «Das weiss der Chat» der Rezeption des Hotel Monte-Moro, Saas-Almagell (08.11.2026, Bauskript aus dem Culinarium über Wild Side).

Jede Zeile: Stichwort, Angabe, Beleg. Der Beleg ist eine Stelle, die wörtlich in `gast/gast_wissen.txt` (Angaben des Hauses aus website/inhalt/daten.py
und die Fragen und Antworten der Website) oder `gast/gast_umgebung.txt` (Kontakt, Lage, was das Haus nicht veröffentlicht) steht; dieses Skript bricht ab,
wenn ein Beleg dort nicht vorkommt oder eine Zahl der Angabe nicht im Umfeld des Belegs steht (nichts abgetippt oder verschönert).
Bewusst NICHT im Steckbrief, weil das Haus es nicht veröffentlicht (website/inhalt/daten.py OFFEN): Öffnungszeiten und Ruhetage des Röstihüs, die Strasse
des Hauses, Storno- und Geschäftsbedingungen, Preise der Ferienwohnungen, Zeiten für Check-in und Check-out. Fragt ein Gast danach, sagt der Chat, dass
Esther und Fabian das persönlich beantworten, und nennt keine Zahl. Die Gratis-Anreise ist am 31.10.2026 abgelaufen und steht nirgends.
«Veranstaltungen» und «Fragen & Antworten» füllt das Team selbst.
Ergebnis: steckbrief.json daneben, gelesen von gedaechtnis.py. Nach jedem neuen Wissen (python3 _bau/montemoro_wissen.py) erneut laufen lassen.
Aufruf: python3 _werkzeuge/reception/steckbrief_bau.py"""
import hashlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WISSEN = os.path.join(HIER, 'gast')
DATEIEN = ('gast_wissen.txt', 'gast_umgebung.txt')

# Bereich → Gruppen → Zeilen (Stichwort, Angabe, Beleg, weitere Belege)
S = [
 ('Das Haus', [
  ('Auf einen Blick', [
   ('Gastgeber', 'Esther und Fabian Zurbriggen', 'Esther und Fabian Zurbriggen sind die Gastgeber im Hotel Monte-Moro in Saas-Almagell'),
   ('Das Haus', '18 Zimmer, 55 Betten, 3 Sterne', 'Das Haus: 18 Zimmer, 55 Betten (Schweiz Tourismus), 3 Sterne.'),
   ('Lage', 'an bester Lage in Saas-Almagell', 'Das Hotel Monte Moro befindet sich an bester Lage in Saas-Almagell.'),
   ('Sonnenterrasse', 'direkt vor dem Haus, bei schönem Wetter', 'Bei schönem Wetter (bei uns scheint fast immer die Sonne) können Sie übrigens auch unsere Sonnenterasse direkt vor dem Haus geniessen.'),
   ('Satz des Hauses', 'Mehr erleben, weniger zahlen.', 'Mehr erleben, weniger zahlen.'),
  ]),
  ('Was Gäste sagen', [
   ('Google', '4,5 von 5 aus 121 Bewertungen (Stand 17. Oktober 2026)', 'Google: 4,5 von 5 (121 Bewertungen)', 'Noten der Gäste (Stand 17. Oktober 2026)'),
   ('Booking.com', '8,3 von 10 aus 94 Bewertungen; Personal 9,0, Lage 9,0', 'Booking.com: 8,3 von 10 (94 Bewertungen)', 'Personal: 9,0 Booking.com · Lage: 9,0 Booking.com'),
  ]),
 ]),
 ('Zimmer & Wohnungen', [
  ('Im Hotel', [
   ('Ausstattung', 'Dusche/Bad, WC, Haarfön, TV, Safe und Balkon; Brandmeldeanlage', 'Alle Zimmer sind mit Dusche/Bad, WC, Haarfön, TV, Safe und Balkon ausgestattet. Zum Schutz unserer Gäste haben wir eine Brandmeldeanlage.'),
   ('Laut Booking.com', 'Sitzbereich, Flachbild-TV, Schreibtisch, WLAN inklusive, Nichtraucherzimmer', 'Laut dem Eintrag des Hauses bei Booking.com: Sitzbereich, Flachbild-TV mit Satellitenkanälen, Schreibtisch, Kostenlose Pflegeprodukte, WLAN inklusive, Nichtraucherzimmer.'),
   ('Zimmerarten', 'Budgetzimmer und Standardzimmer, mit Frühstück oder Halbpension', 'Budgetzimmer, Zimmer mit Frühstück: CHF 90.00 pro Person / Tag', 'Standardzimmer, Zimmer mit Halbpension (4-Gänge): CHF 130.00 pro Person / Tag'),
   ('Familienzimmer', 'Familienzimmer und Familienkombinationen, ideal für 3 bis 6 Personen', 'Wir haben gemütliche, komfortable Familienzimmer und Familienkombinationen - ideal für 3 - 6 Personen.'),
   ('Residence Alpenhof', 'Hotelzimmer 4 Gehminuten entfernt, Frühstück und Abendessen im Hotel Monte-Moro', 'Wir bieten ebenfalls Hotelzimmer in der 4 Gehminuten entfernten Residence Alpenhof an (Frühstück und Abendessen im Hotel Monte-Moro).'),
  ]),
  ('Ferienwohnungen', [
   ('Haus Apollo', 'Wohnung im 4. Stock am Dorfeingang, Ausblick auf das ganze Dorf, Südbalkon', 'Das Haus Apollo befindet sich am Dorfeingang von Saas-Almagell. Da sich die Ferienwohnung im 4. Stock befindet, können wir Ihnen einen herrlichen Ausblick auf das ganze Dorf garantieren.'),
   ('Haus Arizona', 'Wohnungen mit 2½, 3½ und 4½ Zimmern', 'Das Haus Arizona verfügt über gemütliche und geräumige 4½, 3½ und 2½-Zimmer - Wohnungen.', 'TV, Radio, Geschirrspülmaschine, Kaffeemaschine und Mikrowelle'),
   ('Wäsche und Parkplatz', 'Bett- und Frotteewäsche stehen zur Verfügung, der Parkplatz direkt neben dem Haus', 'Bett- und Frotteewäsche stehen Ihnen zur Verfügung. Der Parkplatz befindet sich direkt neben dem Haus.'),
   ('Preise', 'stehen nicht auf der Website; Esther und Fabian beantworten das persönlich', 'Preise der Ferienwohnungen im Haus Apollo und im Haus Arizona.'),
  ]),
 ]),
 ('Preise', [
  ('Pro Person und Tag', [
   ('Budgetzimmer mit Frühstück', 'CHF 90.00', 'Budgetzimmer, Zimmer mit Frühstück: CHF 90.00 pro Person / Tag'),
   ('Standardzimmer mit Frühstück', 'CHF 100.00', 'Standardzimmer, Zimmer mit Frühstück: CHF 100.00 pro Person / Tag'),
   ('Budgetzimmer mit Halbpension', 'CHF 120.00, Halbpension mit 4 Gängen', 'Budgetzimmer, Zimmer mit Halbpension (4-Gänge): CHF 120.00 pro Person / Tag'),
   ('Standardzimmer mit Halbpension', 'CHF 130.00, Halbpension mit 4 Gängen', 'Standardzimmer, Zimmer mit Halbpension (4-Gänge): CHF 130.00 pro Person / Tag'),
  ]),
  ('Zuschläge', [
   ('Einzelzimmer', 'Zuschlag 50 %', 'Einzelzimmerzuschlag: 50 %'),
   ('1 bis 3 Nächte', 'Zuschlag CHF 5.00 pro Tag', 'Zuschlag für 1 - 3 Übernachtungen / pro Tag: CHF 5.00'),
   ('Kurtaxe Erwachsene', 'pro Tag CHF 4.50 im Winter, CHF 7.00 im Sommer', 'Kurtaxe Erwachsene pro Tag (Winter): CHF 4.50', 'Kurtaxe Erwachsene pro Tag (Sommer): CHF 7.00'),
   ('Kurtaxe Kinder', '6 bis 16 Jahre, pro Tag CHF 2.25 im Winter, CHF 3.50 im Sommer', 'Kurtaxe Kinder (6 - 16 Jahre) pro Tag (Winter): CHF 2.25', 'Kurtaxe Kinder (6 - 16 Jahre) pro Tag (Sommer): CHF 3.50'),
   ('Hund', 'pro Tag ohne Futter CHF 7.00 bis 10.00', 'Hund pro Tag ohne Futter: CHF 7.00 - 10.00'),
  ]),
  ('Bezahlung', [
   ('Euro', 'Bezahlung in Euro möglich, Rückgeld in Franken', 'Bezahlung in Euro möglich, Rückgeld in Franken.'),
  ]),
 ]),
 ('Inklusive', [
  ('Im Preis dabei', [
   ('Postauto', 'im ganzen Saastal, Sommer und Winter', 'Benutzung Postautos im ganzen Saastal (Sommer/Winter)'),
   ('Bergbahnen', 'alle Bergbahnen im Saastal im Sommer, ohne Metro Alpin; im Sommer und Herbst ab der 1. Übernachtung', 'Benutzung aller Bergbahnen im Saastal (ohne Metro Alpin) (Sommer)', 'Bergbahnen und Postautos im Sommer und Herbst ab der 1. Übernachtung inklusive!'),
   ('Frühstück', 'Frühstücksbuffet mit Frühstück und Halbpension', 'ZF und HP: Frühstücksbuffet'),
   ('Racletteabend', 'einmal in der Woche im Stübli, mit Halbpension', 'Halbpension: wöchentlicher Racletteabend im Stübli.'),
   ('Kidsclub', 'täglich Mo bis Sa, 16:30 bis 21:00 Uhr', 'Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr'),
   ('Parkplatz', 'Hotelparkplatz für Hotelgäste', 'Parkplätze für Hotelgäste stehen zur Verfügung. Hotelparkplatz inklusive.'),
  ]),
 ]),
 ('Kinder & Familie', [
  ('Im Zimmer der Eltern, mit Halbpension', [
   ('Bis 5 Jahre', 'CHF 50.00 pro Kind und Tag', 'bis 5 Jahre: CHF 50.00'),
   ('6 bis 8 Jahre', 'CHF 60.00, 70.00 und 80.00 pro Kind und Tag', '6 Jahre: CHF 60.00 · 7 Jahre: CHF 70.00 · 8 Jahre: CHF 80.00'),
   ('9 bis 16 Jahre', 'CHF 90.00 pro Kind und Tag', '9 - 16 Jahre: CHF 90.00'),
   ('Im eigenen Zimmer', 'normale Zimmerpreise', 'Kinderzuschläge im eigenen Zimmer: normale Zimmerpreise.'),
  ]),
  ('Für die Kinder', [
   ('Kidsclub', 'täglich Mo bis Sa, 16:30 bis 21:00 Uhr, inklusive', 'Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr, inklusive.'),
   ('Im Röstihüs', 'eine kleine Auswahl an Speisen für die kleinsten Gäste', 'Natürlich haben wir auch eine kleine Auswahl an Speisen für unsere kleinsten Gäste.'),
  ]),
 ]),
 ('Röstihüs', [
  ('Das Restaurant', [
   ('Küche', 'Schweizer Spezialitäten aus den besten regionalen Produkten', 'Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten, die mit Liebe, Herz und den besten regionalen Produkten zubereitet werden.'),
   ('Was die Gäste sagen', 'die wohl besten Röstis und Cordon bleus der Region', 'Unseren Gästen zufolge servieren wir damit die wohl besten Röstis und Cordon Bleus der Region.'),
   ('Tisch reservieren', 'Telefon +41 27 957 10 12 oder über TheFork', 'Telefon +41 27 957 10 12 oder über TheFork.'),
   ('Öffnungszeiten', 'stehen nicht auf der Website; die Rezeption gibt sie gern bekannt', 'Öffnungszeiten und Ruhetage des Röstihüs (die Rezeption gibt sie gern bekannt).'),
  ]),
  ('Auf der Karte', [
   ('Röstis', 'elf Röstis, Fr. 25.– bis 32.–', 'Rösti Albert: Mit Bauernwurst, Speck und Röstigraben und Käse, Fr. 25.–', 'Rösti Indian Style: Mit gegrillten Krevettenspiess, Zwiebelringen, Ananas, Currysauce, Rahm und Käse überbacken, Fr. 32.–'),
   ('Rösti Tschug Tschug', 'mit Apfelmus und Calvados flambiert, Fr. 27.–', 'Rösti Tschug Tschug: Mit Apfelmus und Calvados flambiert, Rahm und Käse überbacken, Fr. 27.–'),
   ('Rösti Gartu', 'mit Gemüse, Rahm ohne Käse, Fr. 25.–', 'Rösti Gartu: Mit Gemüse, Rahm ohne Käse, Fr. 25.–'),
   ('Cordon bleus', 'fünf Cordon bleus, Fr. 39.– bis 42.–', 'Cordon bleu Monte-Moro: Kalbfleisch mit Schinken und Käse, Fr. 42.–', 'Cordon bleu Val Antrona: Schweinefleisch mit Schinken und Gorgonzola, Fr. 39.–'),
   ('Raclette', 'Raclette gross mit Pellkartoffeln, Fr. 17.–', 'Raclette gross mit Pellkartoffeln: Fr. 17.–'),
   ('Monte-Moro-Kopf', 'Eiweissschaum mit Schoko und Eis, Fr. 15.–', 'Monte-Moro-Kopf (Eiweissschaum mit Schoko und Eis): Fr. 15.–'),
  ]),
  ('Im Glas', [
   ('Hotelweine', 'zwei Cuvées, von Fabian selber kreiert, 7 dl Fr. 67.–', '«Hotelwein» Cuvee Special, Fils Maye | Prestige Silber (wurde von Fabian selber kreiert)', '«Hotelwein» Cuvee Special Eichenfass, Gilles Joel Cina | Prestige Gold (wurde von Fabian selber kreiert)'),
   ('Aus der Region', 'Weine aus dem Wallis, Appenzeller Bier, Digestifs', 'Es werden hervorragende Weine aus dem Kanton Wallis angeboten. Frisches Appenzeller Bier serviert sowie verschiedene Digestifs.'),
   ('Zurbriggen Spritz', 'Lemonsoda, Prosecco, Blue Curaçao, Fr. 12.–', 'Zurbriggen Spritz: Lemonsoda, Prosecco, Blue Curaçao, Fr. 12.–'),
  ]),
 ]),
 ('Spa', [
  ('Im Partnerhotel Pirmin Zurbriggen', [
   ('Eintritt', 'CHF 25.00 pro Person und Eintritt, nicht übertragbar', 'CHF 25.00 pro Person und Eintritt (kann nicht auf andere Personen übertragen werden)'),
   ('7 Tage', 'Abo CHF 150.00 pro Person', 'CHF 150.00 7 Tage Abo pro Person'),
   ('Dabei', 'Bademantel, Schuhe, Handtücher', 'Bademantel, Schuhe, Handtücher stehen zur Verfügung.'),
   ('Angebot', 'Schwimmbad, Whirlpool, Saunalandschaft, Kneippanlage, Massagepraxis, Beautysalon', 'Das Angebot reicht vom Schwimmbad mit Filmvorführungen, Whirlpool, Saunalandschaft mit verschiedenen Saunen über Infrarotliegen, Isha-Whirlwanne, Kneippanlage, Solarium, Fitnesstower mit Hightech & TV, Massagepraxis, Hairstyling bis hin zum Beautysalon.'),
  ]),
 ]),
 ('Anreise & Lage', [
  ('Hinkommen', [
   ('Zug und Postauto', 'über Visp ins Postauto, Umsteigen in Saas-Grund, ca. 45 Min. ab Visp', 'Wenn Sie mit dem Zug anreisen, erreichen Sie das Saastal über Visp, wo sie ins Postauto umsteigen.', 'Zeitdauer Visp - Saas-Almagell ca. 45 Min.'),
   ('Verbindungen', 'stündlich bis 20.10 Uhr ab Visp; bis Saas-Grund 22.40, Freitag und Samstag 23.40 Uhr', 'Es bestehen stündliche Verbindungen bis 20.10 Uhr ab Visp [bis Saas-Grund 22.40 ab Visp, sowie Freitag und Samstag um 23.40 Uhr].'),
   ('Auto', 'durchs Vispertal, in Stalden Richtung Saastal, in Saas-Grund links; ca. 40 Min. ab Visp', 'Von Visp aus fahren sie durchs Vispertal, bei der Verzweigung in Stalden Richtung Saastal', 'Zeitdauer Visp - Saas-Almagell ca. 40 Min.'),
   ('Parkplatz', 'Parkplätze für Hotelgäste, inklusive', 'Parkplätze für Hotelgäste stehen zur Verfügung. Hotelparkplatz inklusive.'),
  ]),
  ('Zu Fuss ab dem Haus', [
   ('Skigebiet', '2 Gehminuten zum Skigebiet Saas-Almagell', '2 Gehminuten: Skigebiet Saas-Almagell'),
   ('Busstation', '3 Gehminuten; alle 30 Minuten ein Bus nach Saas-Grund oder Saas-Fee', '3 Gehminuten: Busstation (Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee)'),
   ('Dorfkern', '3 Gehminuten: Einkaufen, Bankomat, Tourismusbüro', '3 Gehminuten: Dorfkern (Einkaufsmöglichkeiten, Bankomat, Tourismusbüro usw.)'),
  ]),
 ]),
 ('Saastal', [
  ('Sommer und Winter', [
   ('Wandern', 'über 250 km Wanderwege, vom Spaziergang bis zum Viertausender', 'Im Sommer ein herrliches Wanderparadies. Ueber 250 km Wanderwege'),
   ('Skifahren', 'Saas-Almagell 2400 m, Saas-Grund 3200 m, Saas-Fee 3500 m', 'Skifahren und Snowboarden: Saas-Almagell 2400m · Saas-Grund 3200m · Saas-Fee 3500m'),
   ('Tagesausflüge', 'Saas-Fee, Zermatt, Stresa, Chamonix, Montreux, Mattmark, Glacier-Express', 'Tagesausflüge: Saas-Fee, Zermatt, Stresa, Chamonix, Montreux, Mattmark, Grande Dixence, Sitten, Glacier-Express'),
   ('Metro Alpin', 'in Saas-Fee, mit dem höchstgelegenen Drehrestaurant auf 3500 M.ü.M.', "Saas-Fee: Metro Alpin mit dem höchstgelegenen Drehrestaurant auf 3'500 M.ü.M."),
  ]),
 ]),
 ('Kontakt', [
  ('So erreichen Sie die Rezeption', [
   ('Telefon', '+41 27 957 10 12', 'Telefon +41 27 957 10 12, Fax +41 27 957 37 12, E-Mail info@monte-moro.ch.'),
   ('E-Mail', 'info@monte-moro.ch', 'Telefon +41 27 957 10 12, Fax +41 27 957 37 12, E-Mail info@monte-moro.ch.'),
   ('Adresse', 'Hotel Monte-Moro, CH-3905 Saas-Almagell', 'Hotel Monte-Moro, CH-3905 Saas-Almagell.'),
   ('Zimmer buchen', 'mit «Zimmer buchen» auf der Website, per Telefon oder E-Mail', 'Zimmer buchen: mit «Zimmer buchen» auf der Website (Buchungsfenster des Hauses), per Telefon oder E-Mail.'),
  ]),
 ]),
]


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main():
    quelle = {n: open(os.path.join(WISSEN, n), encoding='utf-8').read() for n in DATEIEN}
    roh = {n: norm(t) for n, t in quelle.items()}
    fehler, aus = [], []
    for bereich, gruppen in S:
        gl = []
        for gruppe, zeilen in gruppen:
            zl = []
            for was, angabe, beleg, *mehr in zeilen:
                datei = next((n for n, t in roh.items() if norm(beleg) in t), None)
                if not datei or any(not any(norm(m) in t for t in roh.values()) for m in mehr):
                    fehler.append(f'Beleg fehlt: {bereich} / {was}: «{beleg}»')
                    continue
                # jede Zahl der Angabe steht im Umfeld eines Belegs (±1500 Zeichen), nicht nur irgendwo im Wissen
                fen = ''
                for bl in [beleg] + mehr:
                    for t in roh.values():
                        i = t.find(norm(bl))
                        if i >= 0:
                            fen += t[max(0, i - 1500):i + 1500].replace('’', '')
                for zahl in re.findall(r'\d+(?:[.,]\d+)?', (gruppe + ' ' + angabe).replace('’', '')):
                    if zahl not in fen:
                        fehler.append(f'Zahl {zahl} nicht beim Beleg: {bereich} / {was}')
                fid = hashlib.sha1(f'{bereich}|{gruppe}|{was}'.encode('utf-8')).hexdigest()[:10]
                zl.append({'fid': fid, 'was': was, 'angabe': angabe, 'beleg': norm(beleg), 'datei': datei, 'mehr': [norm(m) for m in mehr]})
            gl.append({'gruppe': gruppe, 'zeilen': zl})
        aus.append({'bereich': bereich, 'gruppen': gl})
    if fehler:
        print('\n'.join(fehler)); sys.exit(1)
    json.dump({'stand': max(os.path.getmtime(os.path.join(WISSEN, n)) for n in DATEIEN), 'bereiche': aus},
              open(os.path.join(HIER, 'steckbrief.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(sum(len(g['zeilen']) for b in aus for g in b['gruppen']), 'Zeilen, alle belegt')


if __name__ == '__main__':
    main()
