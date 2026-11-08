#!/usr/bin/env python3
"""Die Hausdruckerei · Hotel Monte-Moro, Saas-Almagell: Katalog und Vorlagen des Hauses.
   python3 bau_vorlagen.py → katalog.js, haeuser/montemoro/vorlagen/*.json + index.json, Beispielinhalte in start.js (INHALT) und vorlagen.js (DS.BEISPIEL).
Alle Hauswerte (Preise, Röstis, Cordon bleus, Hotelweine, Inklusive, Zuschläge, Kinderpreise, Spa-Tarife, Anreise, Kontakt) kommen aus website/inhalt/daten.py
(als Daten gelesen, nie abgetippt), die Sätze aus daten.py und den Seiten der Website (website/*.html). Was in OFFEN steht (Öffnungszeiten des Röstihüs, Strasse,
Storno, Fotos vom Kidsclub …), kommt nicht vor; die Gratis-Anreise ist am 31.10.2026 abgelaufen und wird nicht angeboten.
Prüfung am Ende: jede Zahl der Texte muss in den Quellen stehen."""
import ast, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HIER, 'haeuser', 'montemoro')
PROJ = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJ, 'website')


def daten():
    env = {}
    for n in ast.parse(open(os.path.join(WEB, 'inhalt', 'daten.py'), encoding='utf-8').read()).body:
        if isinstance(n, ast.Assign):
            try:
                exec(compile(ast.Module([n], []), 'daten.py', 'exec'), {}, env)
            except Exception:
                pass
    return env


D = daten()
H = D['HAUS']
NAME, ORT = H['name'], H['ort']                                   # Hotel Monte-Moro, Saas-Almagell
ADR = '%s · %s' % (H['name'], H['plz_ort'])                       # Hotel Monte-Moro · CH-3905 Saas-Almagell
TEL, MAIL = H['tel'], H['mail']
SATZ = H['satz']                                                  # Mehr erleben, weniger zahlen.
GAST = 'Esther und Fabian Zurbriggen'
KONTAKT = TEL + ' · ' + MAIL
glatt = lambda t: re.sub(r'\s+,', ',', re.sub(r',(?=\S)', ', ', t)).strip().rstrip(',')   # «Syrah,Merlot» → «Syrah, Merlot», Komma am Ende weg
ROESTIS = [{"name": n, "detail": glatt(d), "preis": p} for n, d, p in D['ROESTIS']]
CORDON = [{"name": n, "detail": glatt(d), "preis": p} for n, d, p in D['CORDON']]
WEINE = []
for n, wer, sorten, menge, p in D['HOTELWEINE']:
    kellerei, rest = wer.split(' | ')
    WEINE.append({"name": n.replace('«Hotelwein» ', ''), "detail": '%s · %s · %s · %s' % (kellerei, rest.replace(' (wurde von Fabian selber kreiert)', ''), glatt(sorten), menge), "preis": p,
                  "kellerei": kellerei, "stufe": rest.replace(' (wurde von Fabian selber kreiert)', '')})
SPRITZ = [{"name": n, "detail": glatt(d), "preis": p} for n, d, p in D['SPRITZ']]
KOPF = {"name": D['KOPF'][0].split(' (')[0], "detail": D['KOPF'][0].split(' (')[1].rstrip(')'), "preis": D['KOPF'][1]}
RACLETTE = {"name": D['RACLETTE'][0].split(' mit ')[0], "detail": 'mit ' + D['RACLETTE'][0].split(' mit ')[1], "preis": D['RACLETTE'][1]}
PREISE = [{"name": '%s, %s' % (z, a.replace('Zimmer mit ', '')), "detail": "", "preis": 'CHF ' + p} for z, a, p in D['PREISE']]
ZUSCHLAEGE = [{"name": n.replace(' / ', ' · '), "detail": "", "preis": p if '%' in p else 'CHF ' + p} for n, p in D['ZUSCHLAEGE']]
KINDER = [{"name": n, "detail": "", "preis": 'CHF ' + p} for n, p in D['KINDER']]
SPA = [{"name": n[0].upper() + n[1:], "detail": d, "preis": p} for n, p, d in D['SPA_TARIFE']]
INKL_KURZ = ['Postauto', 'Bergbahnen', 'Frühstück', 'Raclette', 'Kidsclub', 'Parkplatz']   # Kurznamen wie auf der Website (Der Bon)
INKL = [{"name": k, "detail": t, "preis": "inkl."} for k, t in zip(INKL_KURZ, D['INKLUSIVE'])]
KIDSCLUB = 'Montag bis Samstag, 16:30 bis 21:00 Uhr'
LAGE = D['LAGE']
S0 = {"ausr": "c", "rahmen": "einfach", "titel": 1, "zeichen": 1, "ecke": 2.4, "bild": 0.56}
S1 = {"ausr": "c", "rahmen": "ohne", "titel": 1.04, "zeichen": .95, "ecke": 2.4, "bild": 0.56}


def v(n, wo, fmt, vorlage, ton, inhalt, rueck=None, stil=S0):
    return {"n": n, "wo": wo, "format": fmt, "vorlage": vorlage, "ton": ton, "inhalt": inhalt, "rueck": rueck, "stil": stil}


# ---------------- Abteilungen ----------------
ROESTIHUES = [
    v('Best of Röstis', 'am Tisch, im Röstihüs', 'a4h', 'blatt', 'dunkel', {"innen": "karte", "ueber": "Röstihüs · Saas-Almagell", "titel": "Best of Röstis", "text": "", "liste": ROESTIS[:6], "fuss": "Karte vom 18.11.2024 · Preise in Fr."},
      {"vorlage": "blatt", "inhalt": {"innen": "karte", "ueber": "Röstihüs · Saas-Almagell", "titel": "Best of Röstis", "text": "", "liste": ROESTIS[6:], "fuss": "Karte vom 18.11.2024 · Preise in Fr."}}),
    v('Unsere Cordon bleus', 'am Tisch, im Röstihüs', 'dlh', 'karte', 'creme', {"ueber": "Röstihüs · Saas-Almagell", "titel": "Unsere Cordon bleus", "text": "", "liste": CORDON, "fuss": "Karte vom 18.11.2024 · Preise in Fr."}),
    v('Wein von Fabian', 'am Tisch, im Röstihüs', 'dlh', 'karte', 'dunkel', {"ueber": "«Hotelwein» · von Fabian selber kreiert", "titel": "Wein von Fabian", "text": "",
      "liste": [{"name": w["name"], "detail": w["detail"], "preis": w["preis"]} for w in WEINE], "fuss": "Röstihüs · Preise in Fr."}),
    v('Zum Apéro und zum Dessert', 'am Tisch, im Röstihüs', 'a6h', 'karte', 'creme', {"ueber": "Röstihüs · Saas-Almagell", "titel": "Zum Apéro und zum Dessert", "text": "",
      "liste": SPRITZ + [KOPF], "fuss": "Preise in Fr."}),
    v('Röstihüs · Auszug der Karte', 'am Tisch, im Röstihüs', 'dlh', 'menue', 'creme', {"ueber": "Auszug der Karte", "titel": "Röstihüs",
      "liste": [{"gang": "Rösti", "name": ROESTIS[4]["name"], "detail": ROESTIS[4]["detail"]}, {"gang": "Rösti", "name": ROESTIS[6]["name"], "detail": ROESTIS[6]["detail"]},
                {"gang": "Cordon bleu", "name": CORDON[0]["name"], "detail": CORDON[0]["detail"]}, {"gang": "Im Stübli", "name": RACLETTE["name"], "detail": RACLETTE["detail"]},
                {"gang": "Zum Dessert", "name": KOPF["name"], "detail": KOPF["detail"]}], "fuss": NAME + " · " + ORT}),
    v('Es lebe die Tradition', 'Tischaufsteller', 'a6h', 'buehne', 'dunkel', {"bild": "roesti-raum", "ueber": "Restaurant Röstihüs", "titel": D['TRADITION'],
      "text": D['ROESTI_SATZ'], "aktion": ""}),
    v('Elf Röstis', 'Instagram', 'insta', 'geteilt', 'dunkel', {"bild": "roesti-stube", "ueber": "Restaurant Röstihüs", "titel": "Elf Röstis auf unserer Karte.",
      "text": "Die Rösti Tschug Tschug wird mit Calvados flambiert, die Rösti Saastal kommt mit Spiegelei.", "aktion": NAME}),
    v('Heute Abend im Röstihüs', 'Instagram', 'insta', 'grat', 'dunkel', {"bild": "gondel", "ueber": "Restaurant Röstihüs", "titel": "Heute Abend im Röstihüs.",
      "text": "Am Abend leuchten vor dem Röstihüs die alten Gondeln.", "aktion": ""}),
]

INKLUSIVE = [
    v('Inklusive', 'an der Rezeption, im Zimmer', 'a4h', 'blatt', 'dunkel', {"ueber": SATZ, "titel": "Alles schon dabei.", "text": "Ihr Aufenthalt", "liste": [{"name": t, "detail": "", "preis": "inkl."} for t in D['INKLUSIVE']], "fuss": ADR}),
    v('Preisliste Zimmer', 'an der Rezeption, zum Mitschicken', 'a4h', 'blatt', 'dunkel', {"ueber": "Preisliste · pro Person und Tag", "titel": "Zimmer mit Frühstück oder Halbpension",
      "text": "", "liste": PREISE, "fuss": ADR}),
    v('Zuschläge', 'an der Rezeption, zum Mitschicken', 'a5h', 'preisliste', 'creme', {"ueber": "Preisliste", "titel": "Gut zu wissen", "text": "", "liste": ZUSCHLAEGE, "fuss": ADR}),
    v('Kinderpreise', 'an der Rezeption, zum Mitschicken', 'a5h', 'preisliste', 'hell', {"ueber": "Kinder im Zimmer der Eltern · pro Kind und Tag", "titel": "Kinderpreise mit Halbpension",
      "text": D['KINDER_EIGEN'] + '.', "liste": KINDER, "fuss": ADR}),
    v('Bergbahnen und Postautos', 'Instagram', 'insta', 'grat', 'dunkel', {"bild": "tal-sommer", "ueber": "Inklusive ab der 1. Übernachtung", "titel": "Bergbahnen und Postautos.",
      "text": "Im Sommer und Herbst sind Bergbahnen und Postautos ab der 1. Übernachtung inklusive.", "aktion": ""}),
    v('Mehr erleben, weniger zahlen', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "haus-sommer", "ueber": NAME + " · " + ORT, "titel": SATZ,
      "text": "Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag.", "aktion": TEL}),
    v('Aushang Inklusive', 'an der Rezeption', 'a3h', 'grat', 'dunkel', {"bild": "haus-sommer-g", "ueber": "Inklusive", "titel": SATZ,
      "text": "Postauto im ganzen Saastal, im Sommer alle Bergbahnen ausser der Metro Alpin, Frühstücksbuffet, Kidsclub und Hotelparkplatz.", "aktion": NAME}),
]

ABENDE = [
    v('Racletteabend im Stübli', 'an der Rezeption, im Speisesaal', 'a4h', 'grat', 'dunkel', {"bild": "stuebli", "ueber": "Halbpension", "titel": "Racletteabend im Stübli.",
      "text": "Einmal in der Woche ist im Stübli Racletteabend für alle mit Halbpension.", "aktion": NAME}),
    v('Raclette im Stübli', 'am Tisch', 'a6h', 'karte', 'creme', {"ueber": "Im Stübli", "titel": "Raclette", "text": "", "liste": [RACLETTE], "fuss": "Röstihüs · Preise in Fr."}),
    v('Kidsclub', 'an der Rezeption', 'a4h', 'aushang', 'hell', {"ueber": "Inklusive", "titel": "Kidsclub", "text": "Täglich " + KIDSCLUB + ".", "aktion": NAME}),
    v('Kidsclub · Karte', 'an der Rezeption, im Zimmer', 'a6h', 'aushang', 'creme', {"ueber": "Für die Kinder", "titel": "Kidsclub", "text": "Täglich " + KIDSCLUB + ", inklusive.", "aktion": ""}),
    v('Die Woche im Monte-Moro', 'an der Rezeption, im Zimmer', 'a5h', 'programm', 'dunkel', {"ueber": "Inklusive", "titel": "Die Woche im Monte-Moro",
      "termine": [{"wann": "Jeden Morgen", "was": "Frühstücksbuffet", "wo": "Zimmer mit Frühstück und Halbpension"},
                  {"wann": "Mo – Sa · 16:30 – 21:00 Uhr", "was": "Kidsclub", "wo": "inklusive"},
                  {"wann": "Einmal in der Woche", "was": "Racletteabend im Stübli", "wo": "für alle mit Halbpension"},
                  {"wann": "Sommer und Winter", "was": "Postauto im ganzen Saastal", "wo": "inklusive"},
                  {"wann": "Im Sommer", "was": "Bergbahnen im Saastal", "wo": "inklusive, ohne Metro Alpin"}]}),
    v('Spielburg vor dem Haus', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "spielburg", "ueber": "Kinder im Monte-Moro", "titel": "Kidsclub.", "unter": "Mo – Sa · 16:30 bis 21:00 Uhr",
      "text": "Täglich, inklusive. Vor dem Haus steht die Spielburg."}),
]

ZIMMER = [
    v('Willkommensbrief im Zimmer', 'im Zimmer', 'a4h', 'brief', 'hell', {"ueber": "Willkommen", "titel": "Willkommen im Monte-Moro.",
      "text": "Schön, dass Sie da sind. Bei uns scheint fast immer die Sonne, und vom Balkon Ihres Zimmers sehen Sie ins Tal.\n\n"
              "In Ihrem Aufenthalt ist vieles schon dabei: das Postauto im ganzen Saastal, im Sommer alle Bergbahnen im Saastal ausser der Metro Alpin, "
              "das Frühstücksbuffet und der Hotelparkplatz. Mit Halbpension essen Sie am Abend vier Gänge, und einmal in der Woche ist im Stübli Racletteabend.\n\n"
              "Für die Kinder ist der Kidsclub da, " + KIDSCLUB + ". Und nach dem Lift wartet das Spa im Partnerhotel Pirmin Zurbriggen.\n\n"
              "Für jede Frage sind wir an der Rezeption für Sie da.",
      "gruss": "Herzlich\n" + GAST}),
    v('Briefpapier A4', 'Briefe, Angebote', 'a4h', 'brief', 'hell', {}),
    v('Briefpapier A5', 'Briefe, kurze Grüsse', 'a5h', 'brief', 'hell', {}),
    v('In Ihrem Zimmer', 'im Zimmer', 'a6h', 'karte', 'hell', {"ueber": "Im Zimmer", "titel": "In Ihrem Zimmer", "text": "",
      "liste": [{"name": "Dusche/Bad und WC", "detail": "Haarfön und kostenlose Pflegeprodukte", "preis": ""}, {"name": "TV und Safe", "detail": "Flachbild-TV mit Satellitenkanälen", "preis": ""},
                {"name": "Balkon", "detail": "Jedes Zimmer hat seinen Balkon", "preis": ""}, {"name": "Internet", "detail": "WLAN inklusive", "preis": ""}], "fuss": ""}),
    v('Das Spa nebenan', 'im Zimmer, an der Rezeption', 'a6h', 'karte', 'dunkel', {"ueber": D['SPA_TITEL'].replace(' ****S', ''), "titel": "Das Spa nebenan", "text": D['SPA_INKL'], "liste": SPA, "fuss": ""}),
    v('Auch in Euro', 'an der Rezeption', 'a6h', 'aushang', 'creme', {"ueber": "Bezahlung", "titel": "Auch in Euro.", "text": D['EURO'], "aktion": ""}),
    v('Mit Hund', 'an der Rezeption, zum Mitschicken', 'a6h', 'aushang', 'hell', {"ueber": "Gut zu wissen", "titel": "Mit Hund.", "text": "Hund pro Tag ohne Futter: CHF 7.00 bis 10.00.", "aktion": ""}),
]
for w in WEINE:
    ZIMMER.append(v('Tischkarte · ' + w["name"], 'auf dem Tisch im Röstihüs', 'a7q', 'deckel', 'dunkel' if 'Eichenfass' in w["name"] else 'creme',
                    {"ueber": "«Hotelwein» von Fabian · " + w["preis"], "titel": w["name"], "unter": "Von Fabian selber kreiert", "text": ""}))

SAASTAL = [
    v('Mit Zug und Postauto', 'zum Mitschicken, an der Rezeption', 'a5h', 'programm', 'hell', {"ueber": "Ab Visp ca. 45 Min.", "titel": "Mit Zug und Postauto",
      "termine": [{"wann": "Zug", "was": "Visp", "wo": "Zug bis hier, dann Postauto"}, {"wann": "Postauto", "was": "Stalden", "wo": "Verzweigung Richtung Saastal"},
                  {"wann": "Postauto", "was": "Saas-Grund", "wo": "umsteigen"}, {"wann": "Ankunft", "was": "Saas-Almagell", "wo": "3 Gehminuten von der Busstation bis zum Hotel"}]}),
    v('Anreise mit dem Postauto', 'zum Mitschicken, an der Rezeption', 'a4h', 'aushang', 'dunkel', {"ueber": "Ab Visp ca. 45 Min.", "titel": "Anreise mit dem Postauto",
      "text": "Ab Visp fährt das Postauto stündlich bis 20.10 Uhr, bis Saas-Grund um 22.40 Uhr, Freitag und Samstag um 23.40 Uhr. In Saas-Grund steigen Sie um.", "aktion": TEL}),
    v('Mit dem Auto', 'zum Mitschicken', 'a5h', 'aushang', 'creme', {"ueber": "Ab Visp ca. 40 Min.", "titel": "Mit dem Auto",
      "text": "Von Visp durchs Vispertal, in Stalden Richtung Saastal, in Saas-Grund bei der Abzweigung nach Saas-Fee links. Parkplätze für Hotelgäste stehen zur Verfügung.", "aktion": ""}),
    v('Wanderparadies', 'an der Rezeption, Instagram', 'a3h', 'grat', 'dunkel', {"bild": "alpenrosen", "ueber": "Saastal im Sommer", "titel": "Ein herrliches Wanderparadies.",
      "text": "Über 250 km Wanderwege, von einfachen Spaziergängen bis zur Besteigung von Viertausendern.", "aktion": ""}),
    v('Zwei Minuten bis zum Lift', 'Instagram', 'insta', 'grat', 'hell', {"bild": "dorf-weiss", "ueber": "Saastal im Winter", "titel": "Zwei Minuten bis zum Lift.",
      "text": "Zwei Gehminuten zum Skigebiet Saas-Almagell, drei zur Busstation, drei ins Dorf.", "aktion": ""}),
    v('Ansichtskarte Sommer', 'zum Mitnehmen', 'a6q', 'ansicht', 'dunkel', {"bild": "tal-sommer", "titel": ORT, "unter": "Saastal · Wallis"},
      {"vorlage": "kartengruss", "inhalt": {"titel": "Grüsse aus dem Saastal", "text": ""}}),
    v('Ansichtskarte Winter', 'zum Mitnehmen', 'a6q', 'ansicht', 'hell', {"bild": "dorf-weiss", "titel": ORT, "unter": "Saastal im Winter"},
      {"vorlage": "kartengruss", "inhalt": {"titel": "Grüsse aus dem Saastal", "text": ""}}),
    v('Das Spa nebenan · Story', 'Instagram-Story', 'story', 'grat', 'dunkel', {"bild": "spa-wasser", "ueber": "Im Partnerhotel Pirmin Zurbriggen", "titel": "Das Spa nebenan.",
      "text": D['SPA_INKL'], "aktion": "CHF 25.00 pro Person und Eintritt"}),
]

HAUS_ABT = [
    v('Gutschein für einen Aufenthalt', 'zum Verschenken', 'dlq', 'gutschein', 'dunkel', {"ueber": "Gutschein", "titel": "Ein Aufenthalt im Monte-Moro", "unter": SATZ, "wert": "",
      "text": "Ein Zimmer mit Balkon, das Frühstücksbuffet und das Postauto im ganzen Saastal."},
      {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen an der Rezeption des Hotel Monte-Moro, " + TEL + "."}}),
    v('Gutschein · hell', 'zum Verschenken', 'dlq', 'gutschein', 'hell', {"ueber": "Gutschein", "titel": "Ein Aufenthalt im Monte-Moro", "unter": SATZ, "wert": "",
      "text": "Ein Zimmer mit Balkon, das Frühstücksbuffet und das Postauto im ganzen Saastal."},
      {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen an der Rezeption des Hotel Monte-Moro, " + TEL + "."}}),
    v('Gutschein Röstihüs', 'zum Verschenken', 'dlq', 'gutschein', 'dunkel', {"ueber": "Gutschein", "titel": "Ein Abend im Röstihüs", "unter": "Restaurant Röstihüs", "wert": "",
      "text": "Elf Röstis, fünf Cordon bleus und der Wein von Fabian.", "bild": "roesti-abend"},
      {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen im Restaurant Röstihüs des Hotel Monte-Moro, " + TEL + "."}}),
    v('Flyer des Hauses', 'zum Mitnehmen', 'a6h', 'buehne', 'dunkel', {"bild": "haus-sommer-g", "ueber": NAME + " · " + ORT, "titel": "Bei uns scheint fast immer die Sonne.",
      "text": "Zwei Gehminuten zum Skigebiet, drei zur Busstation und drei ins Dorf. Und vor dem Haus die Sonnenterrasse.", "aktion": TEL},
      {"vorlage": "rueckseite", "inhalt": {"text": "Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag."}}),
    v('Ihre Gastgeber', 'Instagram', 'insta', 'fenster', 'creme', {"bild": "empfang", "ueber": "Ihre Gastgeber", "titel": GAST + ".", "unter": NAME,
      "text": "Willkommen im Hotel Monte-Moro in Saas-Almagell."}),
    v('9,0 für das Personal', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "speisesaal", "ueber": "Booking.com · " + D['NOTEN_STAND'], "titel": "9,0 für das Personal.",
      "text": "Und auf Google 4,5 von 5, aus 121 Bewertungen.", "aktion": ""}),
    v('Haus Apollo und Haus Arizona', 'Instagram', 'insta', 'geteilt', 'creme', {"bild": "apollo-haus", "ueber": "Ferienwohnungen", "titel": "Haus Apollo und Haus Arizona.",
      "text": "Ferienwohnungen in Saas-Almagell, Bett- und Frotteewäsche stehen zur Verfügung, der Parkplatz direkt neben dem Haus.", "aktion": TEL}),
]

ABTEILUNGEN = [
    {"k": "roestihues", "t": "Röstihüs-Karte", "satz": "Röstis, Cordon bleus, der Wein von Fabian, Apéro und Dessert, wie auf der Karte vom 18.11.2024.", "foto": "roesti-raum", "vorlagen": ROESTIHUES},
    {"k": "inklusive", "t": "Preise & Inklusive", "satz": "Was im Preis steckt, die Preisliste, Zuschläge und Kinderpreise.", "foto": "fr-tisch", "vorlagen": INKLUSIVE},
    {"k": "abende", "t": "Racletteabend & Kidsclub", "satz": "Der Racletteabend im Stübli, der Kidsclub, die Woche im Monte-Moro.", "foto": "stuebli", "vorlagen": ABENDE},
    {"k": "zimmer", "t": "Im Zimmer", "satz": "Willkommensbrief, Briefpapier, Hinweise im Zimmer und die Tischkarten des Hotelweins.", "foto": "z-licht", "vorlagen": ZIMMER},
    {"k": "saastal", "t": "Saastal & Anreise", "satz": "Mit Zug und Postauto oder dem Auto ins Saastal, Wandern, Winter, Ansichtskarten.", "foto": "tal-sommer", "vorlagen": SAASTAL},
    {"k": "haus", "t": "Das Haus & Geschenke", "satz": "Gutscheine, der Flyer, die Gastgeber, die Ferienwohnungen.", "foto": "haus-sommer-g", "vorlagen": HAUS_ABT},
]

HINWEISE = [
    v('Heute Abend im Stübli', 'sofort aushängen', 'a4h', 'aushang', 'dunkel', {"ueber": "Heute Abend", "titel": "Racletteabend im Stübli",
      "text": "Heute ist im Stübli Racletteabend für alle mit Halbpension.", "aktion": ""}),
    v('Kidsclub heute', 'sofort aushängen', 'a5h', 'aushang', 'hell', {"ueber": "Heute", "titel": "Kidsclub", "text": "Von 16:30 bis 21:00 Uhr, inklusive.", "aktion": ""}),
    v('Parkplatz', 'an der Tür', 'a5h', 'aushang', 'creme', {"ueber": "Für Hotelgäste", "titel": "Hotelparkplatz", "text": D['PARK'] + ".", "aktion": ""}),
    v('Bademantel, Schuhe, Handtücher', 'im Zimmer', 'a6h', 'aushang', 'creme', {"ueber": "Spa im Partnerhotel", "titel": "Alles ist bereit.", "text": D['SPA_INKL'], "aktion": ""}),
    v('Bezahlung in Euro', 'an der Rezeption', 'a6h', 'aushang', 'dunkel', {"ueber": "Bezahlung", "titel": "Auch in Euro.", "text": D['EURO'], "aktion": ""}),
    v('Postauto inklusive', 'an der Rezeption', 'a5h', 'aushang', 'hell', {"ueber": "Inklusive", "titel": "Das Postauto fährt mit.", "text": "Benutzung Postautos im ganzen Saastal, Sommer und Winter. Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee.", "aktion": ""}),
]

NEWSLETTER = [
    v('Sommer im Saastal', 'an alle Gäste', 'mail', 'fenster', 'dunkel', {"bild": "alpenrosen", "ueber": "Saastal im Sommer", "titel": "Ein herrliches Wanderparadies.", "unter": "Bergbahnen und Postautos inklusive",
      "text": "Über 250 km Wanderwege, und im Sommer sind alle Bergbahnen im Saastal ausser der Metro Alpin inklusive."}),
    v('Racletteabend', 'an die Gäste', 'mail', 'aushang', 'creme', {"ueber": "Halbpension", "titel": "Racletteabend im Stübli.",
      "text": "Einmal in der Woche ist im Stübli Racletteabend für alle mit Halbpension.", "aktion": TEL}),
    v('Mehr erleben, weniger zahlen', 'an die Gäste', 'mail', 'deckel', 'creme', {"ueber": NAME, "titel": SATZ, "unter": "Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag",
      "text": "Postauto im ganzen Saastal, im Sommer die Bergbahnen, Frühstücksbuffet, Kidsclub und Hotelparkplatz sind inklusive."}),
    v('Kopfbild Haus', 'über jeder E-Mail', 'mailkopf', 'ansicht', 'dunkel', {"bild": "haus-sommer", "titel": NAME, "unter": ORT}),
    v('Kopfbild Dorf', 'über jeder E-Mail', 'mailkopf', 'ansicht', 'dunkel', {"bild": "dorf-nacht", "titel": NAME, "unter": "Saastal · Wallis"}),
    v('Story: Röstihüs', 'Instagram', 'story', 'fenster', 'dunkel', {"bild": "roesti-abend", "ueber": "Restaurant Röstihüs", "titel": "Es lebe die Tradition.", "unter": NAME,
      "text": "Elf Röstis, fünf Cordon bleus und der Hotelwein, den Fabian selbst kreiert hat."}),
]

# ---------------- Anlässe (nur, was das Haus jede Woche oder jede Saison bietet; Daten nur zum Ordnen, gedruckt wird «im Winter», «im Sommer») ----------------
ANLAESSE = [
    {"k": "raclette", "t": "Racletteabend im Stübli", "z": "wöchentlich", "von": "2026-01-01", "bis": "2027-12-31", "wo": "haus", "ort": "Stübli des Röstihüs",
     "satz": "Einmal in der Woche ist im Stübli Racletteabend für alle mit Halbpension.", "fotos": ["stuebli", "raclette", "roesti-raum"]},
    {"k": "kidsclub", "t": "Kidsclub", "z": "Mo – Sa", "von": "2026-01-01", "bis": "2027-12-31", "wo": "haus", "ort": NAME + " · 16:30 bis 21:00 Uhr",
     "satz": "Täglich " + KIDSCLUB + ", inklusive.", "fotos": ["spielburg", "murmeli", "kinder-rodel"]},
    {"k": "winter", "t": "Winter im Saastal", "z": "im Winter", "von": "2026-11-01", "bis": "2027-04-15", "wo": "region", "ort": "Saas-Almagell 2400 m · Saas-Grund 3200 m · Saas-Fee 3500 m",
     "satz": "Zwei Gehminuten zum Skigebiet Saas-Almagell, das Postauto im ganzen Saastal inklusive.", "fotos": ["dorf-weiss", "skitour", "huette"]},
    {"k": "sommer", "t": "Sommer im Saastal", "z": "im Sommer", "von": "2027-05-01", "bis": "2027-10-31", "wo": "region", "ort": "Saastal · über 250 km Wanderwege",
     "satz": "Im Sommer ein herrliches Wanderparadies; Bergbahnen und Postautos ab der 1. Übernachtung inklusive.", "fotos": ["alpenrosen", "tal-sommer", "mattmark"]},
]
MOTIVE = {
    "raclette": [ABENDE[0], ABENDE[1], HINWEISE[0],
                 v('Story', 'Instagram-Story', 'story', 'grat', 'dunkel', {"bild": "stuebli", "ueber": "Halbpension", "titel": "Racletteabend im Stübli.", "text": "Einmal in der Woche, für alle mit Halbpension.", "aktion": ""})],
    "kidsclub": [ABENDE[2], ABENDE[3], ABENDE[5],
                 v('Beitrag', 'Instagram', 'insta', 'fenster', 'creme', {"bild": "murmeli", "ueber": "Kinder im Monte-Moro", "titel": "Kidsclub.", "unter": "Mo – Sa · 16:30 bis 21:00 Uhr", "text": "Täglich, inklusive."})],
    "winter": [SAASTAL[4], SAASTAL[6],
               v('Story', 'Instagram-Story', 'story', 'grat', 'dunkel', {"bild": "huette", "ueber": "Saastal im Winter", "titel": "Auf die Piste.", "text": "Saas-Almagell 2400 m · Saas-Grund 3200 m · Saas-Fee 3500 m.", "aktion": ""}),
               v('Aushang', 'an der Rezeption', 'a4h', 'aushang', 'creme', {"ueber": "Saastal im Winter", "titel": "Zwei Minuten bis zum Lift.", "text": "Zwei Gehminuten vom Skigebiet Saas-Almagell. Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee.", "aktion": "Postauto im ganzen Saastal inklusive"})],
    "sommer": [SAASTAL[3], INKLUSIVE[4], NEWSLETTER[0],
               v('Story', 'Instagram-Story', 'story', 'grat', 'dunkel', {"bild": "mattmark", "ueber": "Saastal im Sommer", "titel": "Ein herrliches Wanderparadies.", "text": "Über 250 km Wanderwege.", "aktion": ""})],
}

# ---------------- Beispielinhalte je Aufbau (DS.BEISPIEL) und je Art (INHALT) ----------------
BEISPIEL = {
    "deckel": {"ueber": NAME, "titel": SATZ, "unter": ADR, "text": "Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag."},
    "buehne": INKLUSIVE[5]["inhalt"],
    "ansicht": SAASTAL[5]["inhalt"],
    "karte": ROESTIHUES[1]["inhalt"],
    "einladung": {"ueber": "Restaurant Röstihüs", "titel": "Ein Abend im Röstihüs.", "wann": "Einmal in der Woche · Racletteabend", "wo": "Im Stübli", "text": "Für alle mit Halbpension.", "aktion": TEL},
    "programm": ABENDE[4]["inhalt"],
    "fenster": {"bild": "haus-winter-g", "ueber": NAME, "titel": "Bei uns scheint fast immer die Sonne.", "unter": ORT, "text": "Zwei Gehminuten zum Skigebiet, drei zur Busstation und drei ins Dorf."},
    "geteilt": dict(ROESTIHUES[6]["inhalt"], bild="roesti-raum"),
    "gutschein": HAUS_ABT[0]["inhalt"],
    "gutscheinrueck": HAUS_ABT[0]["rueck"]["inhalt"],
    "aushang": ABENDE[2]["inhalt"],
    "rueckseite": {"text": "Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag."},
    "kartengruss": {"titel": "Grüsse aus dem Saastal", "text": ""},
    "menue": ROESTIHUES[4]["inhalt"],
    "grat": ABENDE[0]["inhalt"],
    "brief": ZIMMER[0]["inhalt"],
    "blatt": INKLUSIVE[1]["inhalt"],
    "preisliste": INKLUSIVE[2]["inhalt"],
}
INHALT = {
    "speisekarte": {"blatt": ROESTIHUES[0]["inhalt"], "karte": ROESTIHUES[1]["inhalt"], "menue": ROESTIHUES[4]["inhalt"]},
    "getraenke": {"karte": ROESTIHUES[2]["inhalt"], "deckel": {"ueber": "«Hotelwein»", "titel": "Wein von Fabian", "unter": "Von Fabian selber kreiert", "text": "Cuvee Special und Cuvee Special Eichenfass, je 7 dl."}},
    "aushang": {"aushang": ABENDE[2]["inhalt"], "grat": ABENDE[0]["inhalt"], "deckel": {"ueber": "Inklusive", "titel": SATZ, "unter": NAME, "text": ""}},
    "plakat": {"grat": SAASTAL[3]["inhalt"], "buehne": INKLUSIVE[5]["inhalt"], "fenster": NEWSLETTER[0]["inhalt"]},
    "preisliste": {"blatt": INKLUSIVE[1]["inhalt"], "preisliste": INKLUSIVE[2]["inhalt"], "karte": INKLUSIVE[0]["inhalt"]},
    "zimmerkarte": {"brief": ZIMMER[0]["inhalt"]},
    "briefpapier": {"brief": {}},
    "flyer": {"buehne": HAUS_ABT[3]["inhalt"]},
    "programm": {"programm": ABENDE[4]["inhalt"]},
    "tisch": {"buehne": ROESTIHUES[5]["inhalt"], "karte": ROESTIHUES[3]["inhalt"]},
    "instagram": {"geteilt": dict(ROESTIHUES[6]["inhalt"], bild="roesti-raum"), "buehne": INKLUSIVE[5]["inhalt"], "grat": INKLUSIVE[4]["inhalt"]},
    "tischkarte": {"deckel": ZIMMER[7]["inhalt"]},
    "hinweiskarte": {"aushang": ZIMMER[5]["inhalt"]},
    "stoerung": {"aushang": HINWEISE[0]["inhalt"]},
    "story": {"fenster": NEWSLETTER[5]["inhalt"], "grat": MOTIVE["sommer"][3]["inhalt"]},
    "postkarte": {"ansicht": SAASTAL[5]["inhalt"]},
    "gutschein": {"gutschein": HAUS_ABT[0]["inhalt"]},
}

# ---------------- Bibliothek je Art (vorlagen/<art>.json) ----------------
ART_FORMAT = {"speisekarte": "dlh", "getraenke": "dlh", "preisliste": "a4h", "aushang": "a4h", "plakat": "a3h", "zimmerkarte": "a4h", "briefpapier": "a4h", "flyer": "a6h",
              "programm": "a5h", "tisch": "a6h", "instagram": "insta", "tischkarte": "a7q", "hinweiskarte": "a6h", "stoerung": "a4h", "story": "story",
              "newsletter": "mail", "postkarte": "a6q", "gutschein": "dlq"}
GRUPPE_NAME = {"speisekarte": "Karten des Röstihüs", "getraenke": "Karten des Röstihüs", "tischkarte": "Karten des Röstihüs", "preisliste": "Preise und Inklusive",
               "aushang": "Aushang und Hinweise", "stoerung": "Aushang und Hinweise", "hinweiskarte": "Aushang und Hinweise", "plakat": "Plakat",
               "zimmerkarte": "Brief und Zimmer", "briefpapier": "Brief und Zimmer", "flyer": "Flyer und Programm", "programm": "Flyer und Programm",
               "tisch": "Tischaufsteller", "instagram": "Instagram und Newsletter", "newsletter": "Instagram und Newsletter", "story": "Story",
               "postkarte": "Ansichtskarte und Gutschein", "gutschein": "Ansichtskarte und Gutschein"}
BIB = {k: [] for k in ART_FORMAT}


def neu(art, titel, bereich, x, fmt=None):
    BIB[art].append({"id": "%s-%03d" % (art, len(BIB[art]) + 1), "titel": titel, "bereich": bereich, "vorlage": x["vorlage"], "ton": x["ton"], "stil": x["stil"],
                     "inhalt": x["inhalt"], "rueck": x["rueck"], **({"format": fmt} if fmt else {})})


for x in ROESTIHUES[:2] + ROESTIHUES[4:5]:
    neu('speisekarte', x["n"], 'Röstihüs', x, x["format"])
for x in ROESTIHUES[2:4] + [ABENDE[1]]:
    neu('getraenke', x["n"], 'Röstihüs', x, x["format"])
for x in INKLUSIVE[:4] + [ZIMMER[4]]:
    neu('preisliste', x["n"], 'Preise', x, x["format"])
for x in [ABENDE[0], ABENDE[2], SAASTAL[1], INKLUSIVE[6], MOTIVE['winter'][3], HINWEISE[5]]:
    neu('aushang', x["n"], 'Aushang', x, x["format"])
for x in [SAASTAL[3], INKLUSIVE[6], ABENDE[0], INKLUSIVE[4], SAASTAL[4], ABENDE[2]]:
    neu('plakat', x["n"], 'Plakat', x, 'a3h')
neu('zimmerkarte', ZIMMER[0]["n"], 'Zimmer', ZIMMER[0])
neu('zimmerkarte', 'Willkommensbrief A5', 'Zimmer', ZIMMER[0], 'a5h')
for x in ZIMMER[1:3]:
    neu('briefpapier', x["n"], 'Zimmer', x, x["format"])
neu('flyer', HAUS_ABT[3]["n"], 'Haus', HAUS_ABT[3])
neu('flyer', 'Flyer Inklusive', 'Haus', v('Flyer Inklusive', '', 'a6h', 'grat', 'dunkel', INKLUSIVE[6]["inhalt"], {"vorlage": "rueckseite", "inhalt": {"text": "Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag."}}))
for x in [ABENDE[4], SAASTAL[0]]:
    neu('programm', x["n"], 'Programm', x, x["format"])
for x in [ROESTIHUES[5], ROESTIHUES[3], ZIMMER[3], ZIMMER[4], ABENDE[3]]:
    neu('tisch', x["n"], 'Tisch', x, 'a6h')
for x in [ROESTIHUES[6], ROESTIHUES[7], INKLUSIVE[4], INKLUSIVE[5], SAASTAL[4], HAUS_ABT[4], HAUS_ABT[5], HAUS_ABT[6], MOTIVE['kidsclub'][3]]:
    neu('instagram', x["n"], 'Instagram', x, 'insta')
for x in ZIMMER[7:]:
    neu('tischkarte', x["n"], 'Röstihüs', x)
neu('tischkarte', 'Reserviert · Röstihüs', 'Röstihüs', v('Reserviert', '', 'a7q', 'deckel', 'creme', {"ueber": "Restaurant Röstihüs", "titel": "Reserviert", "unter": "", "text": ""}))
neu('tischkarte', 'Reserviert · Stübli', 'Röstihüs', v('Reserviert', '', 'a7q', 'deckel', 'dunkel', {"ueber": "Im Stübli", "titel": "Reserviert", "unter": "", "text": ""}))
for x in [ZIMMER[5], ZIMMER[6], ABENDE[3], HINWEISE[3]]:
    neu('hinweiskarte', x["n"], 'Hinweise', x, 'a6h')
for x in HINWEISE[:3]:
    neu('stoerung', x["n"], 'Hinweise', x, 'a4h')
for x in [NEWSLETTER[5], ABENDE[5], SAASTAL[7]] + [m for k in MOTIVE for m in MOTIVE[k] if m["n"] == 'Story']:
    neu('story', x["n"], 'Story', x, 'story')
for x in NEWSLETTER:
    neu('newsletter', x["n"], 'Newsletter', x, x["format"])
for x in SAASTAL[5:7]:
    neu('postkarte', x["n"], 'Saastal', x, 'a6q')
neu('postkarte', 'Ansichtskarte Haus', 'Saastal', v('Ansichtskarte Haus', '', 'a6q', 'ansicht', 'dunkel', {"bild": "haus-sommer-g", "titel": NAME, "unter": ORT},
    {"vorlage": "kartengruss", "inhalt": {"titel": "Grüsse aus dem Monte-Moro", "text": ""}}))
for x in HAUS_ABT[:3]:
    neu('gutschein', x["n"], 'Geschenk', x, 'dlq')


def schreiben():
    vd = os.path.join(Z, 'vorlagen'); os.makedirs(vd, exist_ok=True)
    for f in os.listdir(vd):
        if f.endswith('.json'):
            os.remove(os.path.join(vd, f))
    index = []
    for art, l in BIB.items():
        if not l:
            continue
        json.dump({"art": art, "format": ART_FORMAT[art], "vorlagen": l}, open(os.path.join(vd, art + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        index.append({"art": art, "format": ART_FORMAT[art], "zahl": len(l), "gruppe": GRUPPE_NAME[art]})
    json.dump(index, open(os.path.join(vd, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    kat = ("/* Die Hausdruckerei · Hotel Monte-Moro, Saas-Almagell · Katalog des Hauses. GESCHRIEBEN VON bau_vorlagen.py, nicht von Hand ändern.\n"
           "   Fertig gesetzte Vorlagen nur aus dem, was das Haus selbst sagt (website/inhalt/daten.py, Seiten der Website); jede öffnet ohne KI und ohne Kosten. */\n(function () {\n"
           f"  const ABTEILUNGEN = {J(ABTEILUNGEN)};\n  const HINWEISE = {J(HINWEISE)};\n  const NEWSLETTER = {J(NEWSLETTER)};\n  const ANLAESSE = {J(ANLAESSE)};\n"
           f"  const MOTIVE = {J(MOTIVE)};\n  const motive = a => MOTIVE[a.k] || [];\n  window.DSKATALOG = {{ ABTEILUNGEN, HINWEISE, ANLAESSE, motive, NEWSLETTER }};\n}})();\n")
    open(os.path.join(HIER, 'katalog.js'), 'w', encoding='utf-8').write(kat)
    s = open(os.path.join(HIER, 'start.js'), encoding='utf-8').read()
    s = re.sub(r'  const INHALT = \{.*?\};\n', lambda m: '  const INHALT = ' + json.dumps(INHALT, ensure_ascii=False) + ';\n', s, count=1, flags=re.S)
    open(os.path.join(HIER, 'start.js'), 'w', encoding='utf-8').write(s)
    s = open(os.path.join(HIER, 'vorlagen.js'), encoding='utf-8').read()
    s = re.sub(r'  DS\.BEISPIEL = \{.*?\};\n', lambda m: '  DS.BEISPIEL = ' + json.dumps(BEISPIEL, ensure_ascii=False) + ';\n', s, count=1, flags=re.S)
    open(os.path.join(HIER, 'vorlagen.js'), 'w', encoding='utf-8').write(s)
    n = sum(len(l) for l in BIB.values())
    print('Vorlagen:', n, 'in', len(index), 'Arten ·', sum(len(a["vorlagen"]) for a in ABTEILUNGEN), 'in Abteilungen ·', len(ANLAESSE), 'Anlässe')
    for a in ABTEILUNGEN:
        print('  ', a['t'], len(a['vorlagen']))
    for art, l in BIB.items():
        print('  ', art, len(l))


def pruefen():
    """Jede Zahl der Texte muss in den Quellen stehen (daten.py, Seiten der Website)."""
    q = open(os.path.join(WEB, 'inhalt', 'daten.py'), encoding='utf-8').read()
    for f in os.listdir(WEB):
        if f.endswith('.html'):
            q += open(os.path.join(WEB, f), encoding='utf-8').read()
    q = q.replace('&nbsp;', ' ')
    texte = json.dumps([ABTEILUNGEN, HINWEISE, NEWSLETTER, ANLAESSE, MOTIVE, BIB], ensure_ascii=False)
    texte = re.sub(r'"(von|bis|id|bild|format|stil)": ?"[^"]*"', '', texte)
    texte = re.sub(r'"(titel|zeichen|ecke|bild)": ?[\d.]+', '', texte)
    fehl = sorted({z for z in re.findall(r'\d+', texte) if z not in q})
    print('NICHT BELEGT:', fehl if fehl else 'keine')
    verboten = [w for w in ('ß', 'Gratis', 'geschenkt', '!') if w in json.dumps([ABTEILUNGEN, HINWEISE, NEWSLETTER, MOTIVE], ensure_ascii=False)]
    if verboten:
        print('VERBOTEN:', verboten)


if __name__ == '__main__':
    pruefen()
    schreiben()
