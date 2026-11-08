"""Hotel Monte-Moro · Inhalte an einer Stelle. Jede Angabe wörtlich aus den Dateien des Hauses in ../_quelle (Abruf 09.10.2026,
Nachtrag 17.10.2026), Fundstelle je Block im Kommentar. Was nicht belegt ist, steht in OFFEN und nicht auf der Seite."""

HAUS = dict(name='Hotel Monte-Moro', ort='Saas-Almagell', plz_ort='CH-3905 Saas-Almagell',     # Impressum
            gastgeber='Esther & Fabian Zurbriggen-Zurbriggen',
            tel='+41 27 957 10 12', tel_href='+41279571012', fax='+41 27 957 37 12', mail='info@monte-moro.ch',
            satz='Mehr erleben, weniger zahlen.', satz2='Gratis an- und abreisen.',               # de.md
            buchen='https://www.monte-moro.ch/de/buchen.html',                                    # seekda (hotel:CH_VS_0086), bleibt
            tisch='https://widget.thefork.com/f5623bf8-e9d4-4f54-9280-07152923107a')              # TheFork, bleibt als zweiter Weg

# Preisliste «Zimmer mit Frühstück» und «Inklusive» (de__hotel__preise.html.md)
PREISE = [('Budgetzimmer', 'Zimmer mit Frühstück', '90.00'), ('Standardzimmer', 'Zimmer mit Frühstück', '100.00'),
          ('Budgetzimmer', 'Zimmer mit Halbpension (4-Gänge)', '120.00'), ('Standardzimmer', 'Zimmer mit Halbpension (4-Gänge)', '130.00')]
INKLUSIVE = ['Benutzung Postautos im ganzen Saastal (Sommer/Winter)', 'Benutzung aller Bergbahnen im Saastal (ohne Metro Alpin) (Sommer)',
             'ZF und HP: Frühstücksbuffet', 'Halbpension: wöchentlicher Racletteabend', 'Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr', 'Hotelparkplatz']
# Gratis-Anreise (de.md), läuft am Datum ab
ANREISE_GRATIS = dict(titel='An- und Abreise mit dem öffentlichen Verkehr (ab 2 Nächten) geschenkt!', bis='2026-10-31',
                      bedingungen=['Sie wohnen in der Schweiz.', 'Sie übernachten mindestens 2 Nächte bei uns.',
                                   'Sie buchen direkt über unsere Internetseite, per Telefon oder Email.', 'Sie buchen für den Zeitraum vom 1. Mai bis 31. Oktober 2026.'])
BERGBAHN_SATZ = 'Bergbahnen und Postautos im Sommer und Herbst ab der 1. Übernachtung inklusive!'   # de.md

# Zuschläge (de__hotel__preise.html.md)
ZUSCHLAEGE = [('Kurtaxe Erwachsene pro Tag (Winter)', '4.50'), ('Kurtaxe Erwachsene pro Tag (Sommer)', '7.00'),
              ('Kurtaxe Kinder (6 - 16 Jahre) pro Tag (Winter)', '2.25'), ('Kurtaxe Kinder (6 - 16 Jahre) pro Tag (Sommer)', '3.50'),
              ('Einzelzimmerzuschlag', '50 %'), ('Zuschlag für 1 - 3 Übernachtungen / pro Tag', '5.00'),
              ('Hund pro Tag ohne Futter', '7.00 - 10.00')]
KINDER = [('bis 5 Jahre', '50.00'), ('6 Jahre', '60.00'), ('7 Jahre', '70.00'), ('8 Jahre', '80.00'), ('9 - 16 Jahre', '90.00')]   # pro Kind/Tag inklusiv Halbpension
KINDER_SATZ = 'Kinderzuschläge im Zimmer der Eltern (Preis pro Kind/Tag) inklusiv Halbpension'
KINDER_EIGEN = 'Kinderzuschläge im eigenen Zimmer: normale Zimmerpreise'
EURO = 'Bezahlung in Euro möglich, Rückgeld in Franken.'   # de__hotel__preise.html.md (Fakten 03)

# Lage (de.md, «Zentrale Lage»)
LAGE_SATZ = 'Das Hotel Monte Moro befindet sich an bester Lage in Saas-Almagell.'
LAGE = [('2', 'Skigebiet Saas-Almagell', 'Gehminuten vom Skigebiet Saas-Almagell'),
        ('3', 'Busstation', 'Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee'),
        ('3', 'Dorfkern', 'Einkaufsmöglichkeiten, Bankomat, Tourismusbüro usw.')]
PARK = 'Parkplätze für Hotelgäste stehen zur Verfügung'

# Zimmer (de__hotel__zimmer.html.md) und Ferienwohnungen (de__ferienwohnungen__*.md)
ZIMMER_TITEL = 'Schöne Hotelzimmer - schöne Ferien'
ZIMMER_TEXT = 'Alle Zimmer sind mit Dusche/Bad, WC, Haarfön, TV, Safe und Balkon ausgestattet. Zum Schutz unserer Gäste haben wir eine Brandmeldeanlage.'
FAMILIE_TEXT = 'Wir haben gemütliche, komfortable Familienzimmer und Familienkombinationen - ideal für 3 - 6 Personen.'
ALPENHOF_TEXT = 'Wir bieten ebenfalls Hotelzimmer in der 4 Gehminuten entfernten Residence Alpenhof an (Frühstück und Abendessen im Hotel Monte-Moro).'
APOLLO = 'Das Haus Apollo befindet sich am Dorfeingang von Saas-Almagell. Da sich die Ferienwohnung im 4. Stock befindet, können wir Ihnen einen herrlichen Ausblick auf das ganze Dorf garantieren. Die Wohnung ist ausgestattet mit Fernseher, Geschirrspülmaschine, Kaffeemaschine und Südbalkon. Bett- und Frotteewäsche stehen Ihnen zur Verfügung. Der Parkplatz befindet sich direkt neben dem Haus.'
ARIZONA = 'Das Haus Arizona verfügt über gemütliche und geräumige 4½, 3½ und 2½-Zimmer - Wohnungen. Die Wohnungen sind komfortabel eingerichtet: TV, Radio, Geschirrspülmaschine, Kaffeemaschine und Mikrowelle. Bett- und Frotteewäsche stehen Ihnen zur Verfügung. Der Parkplatz befindet sich direkt neben dem Haus.'

# Restaurant Röstihüs (de__restaurant.html.md, speisekarte.pdf Stand 18.11.2024, Seite 4 und 5)
RESTAURANT = 'Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten, die mit Liebe, Herz und den besten regionalen Produkten zubereitet werden.'
TRADITION = 'Es lebe die Tradition!'
SONNE = 'Bei schönem Wetter (bei uns scheint fast immer die Sonne) können Sie übrigens auch unsere Sonnenterasse direkt vor dem Haus geniessen.'
ROESTIS = [('Rösti Albert', 'Mit Bauernwurst, Speck und Röstigraben und Käse', '25.–'), ('Rösti Dracula', 'Mit Knoblauch, Rahm und Käse überbacken', '25.–'),
           ('Rösti Macugnaga', 'Mit Birnen, Gorgonzola, Rahm und Käse überbacken', '25.–'), ('Rösti Exotic Palma', 'Mit Schinken, Ananas, Rahm und Käse überbacken', '25.–'),
           ('Rösti Tschug Tschug', 'Mit Apfelmus und Calvados flambiert, Rahm und Käse überbacken', '27.–'), ('Rösti Gartu', 'Mit Gemüse, Rahm ohne Käse', '25.–'),
           ('Rösti Saastal', 'Mit Schinken, Spiegelei, Rahm und Käse überbacken', '25.–'), ('Rösti Diavolo', 'Mit Mozzarella , Salami, scharfer Tomatensauce, Rahm und Parmesan', '25.–'),
           ('Schmugglerrösti', 'Mit Tomaten, Thon, Mozzarella, Rahm und Käse überbacken', '27.–'), ('Rösti Olma', 'Mit Olma-Bratwurst , Zwiebelringen, Rahm und Käse überbacken', '27.–'),
           ('Rösti Indian Style', 'Mit gegrillten Krevettenspiess, Zwiebelringen, Ananas, Currysauce, Rahm und Käse überbacken', '32.–')]
CORDON = [('Monte-Moro', 'Kalbfleisch mit Schinken und Käse', '42.–'), ('Val Antrona', 'Schweinefleisch mit Schinken und Gorgonzola', '39.–'),
          ('Knobli', 'Schweinefleisch mit Schinken, Zwiebeln, Käse und Knoblauch', '39.–'), ('Hawaii', 'Schweinefleisch mit Schinken, Ananas, Käse', '39.–'),
          ('Förster', 'Schweinefleisch mit Schinken, Trüffel, Pilzen und Käse', '41.–')]
HOTELWEINE = [('«Hotelwein» Cuvee Special', 'Fils Maye | Prestige Silber (wurde von Fabian selber kreiert)', 'Diolinoir, Syrah,Merlot, Pinot', '7 dl', '67.–'),
              ('«Hotelwein» Cuvee Special Eichenfass', 'Gilles Joel Cina | Prestige Gold (wurde von Fabian selber kreiert)', 'Diolinoir, Syrah, Merlot, Angelotta,', '7 dl', '67.–')]
SPRITZ = [('Zurbriggen Spritz', 'Lemonsoda, Prosecco, Blue Curaçao', '12.–'), ('Antrona Spritz', 'Prosecco, Früchte, Campari', '12.–')]
KOPF = ('Monte-Moro-Kopf (Eiweissschaum mit Schoko und Eis)', '15.–')
RACLETTE = ('Raclette gross mit Pellkartoffeln', '17.–')
FILM_JA = False   # «Wallis Baby» (Kanal Fabian Zurbriggen) nur mit Fabians Ja auf der Seite

# Spa im Partnerhotel (de__hotel__wellness.html.md); die Grösse steht bewusst nicht da (drei Angaben, Potentialanalyse Punkt 08)
SPA_TITEL = 'Im Partnerhotel Pirmin Zurbriggen ****S'
SPA_SATZ = 'Erleben Sie Entspannung pur im ausgezeichneten Spa vom Hotel Pirmin Zurbriggen****S. Hier können Sie die Seele baumeln lassen und dem Körper etwas Gutes tun.'
SPA_ANGEBOT = 'Das Angebot reicht vom Schwimmbad mit Filmvorführungen, Whirlpool, Saunalandschaft mit verschiedenen Saunen über Infrarotliegen, Isha-Whirlwanne, Kneippanlage, Solarium, Fitnesstower mit Hightech & TV, Massagepraxis, Hairstyling bis hin zum Beautysalon.'
SPA_TARIFE = [('pro Person und Eintritt', 'CHF 25.00', 'kann nicht auf andere Personen übertragen werden'), ('7 Tage Abo pro Person', 'CHF 150.00', '')]
SPA_INKL = 'Bademantel, Schuhe, Handtücher stehen zur Verfügung.'
SPA_LINK = 'https://www.wellnesshotel-zurbriggen.ch/de/wellness-massagen/'

# Saastal (de__region__sommer.html.md, de__region__winter.html.md, de__region__ausfluege.html.md)
SOMMER_SATZ = 'Im Sommer ein herrliches Wanderparadies. Ueber 250 km Wanderwege; von einfachen Spaziergängen über Bergwanderungen bis zur Besteigung von Viertausendern, somit findet sich bestimmt für jedermann das Richtige.'
SAASTAL = {
    'sommer': [('mattmark', 'Wandern', 'Ueber 250 km Wanderwege', True), ('wasserfall', 'Alpin Gorge', 'Durchquerung einer Gebirgsbachschlucht mit einem Bergführer', False),
               ('bach', 'Abenteuerwald', 'Suchen Sie eine besondere Herausforderung?', False), ('blumen', 'Tennis, Velofahren, Trottiplausch, Schwimmen + Minigolf', 'Sportmöglichkeiten', False),
               ('stausee', 'Tagesausflüge', 'Saas-Fee, Zermatt, Stresa, Chamonix, Montreux, Mattmark, Grande Dixence, Sitten, Glacier-Express', False)],
    'winter': [('skitour', 'Skifahren und Snowboarden', 'Saas-Almagell 2400m · Saas-Grund 3200m · Saas-Fee 3500m', False), ('huette', 'Wandern', 'mehrere Winterwanderwege', True),
               ('winterweg', 'Schneeschuhlaufen', 'aus «10 Dinge, die man im Saastal erlebt haben sollte»', False), ('metro', 'Saas-Fee', 'Metro Alpin mit dem höchstgelegenen Drehrestaurant auf 3\'500 M.ü.M.', False)],
}
POSTAUTO = 'Postauto im ganzen Saastal inklusive'

# Noten (befund.md › Noten, 17.10.2026); TripAdvisor bewusst nicht
NOTEN = [('Google', '4,5', 'von 5', '121 Bewertungen'), ('Booking.com', '8,3', 'von 10', '94 Bewertungen'),
         ('Personal', '9,0', 'Booking.com', ''), ('Lage', '9,0', 'Booking.com', ''), ('Sauberkeit', '8,8', 'Booking.com', '')]
NOTEN_STAND = 'Stand 17. Oktober 2026'

# Anreise (de__hotel__anreise.html.md)
ANREISE_ZUG = 'Wenn Sie mit dem Zug anreisen, erreichen Sie das Saastal über Visp, wo sie ins Postauto umsteigen. Es bestehen stündliche Verbindungen bis 20.10 Uhr ab Visp [bis Saas-Grund 22.40 ab Visp, sowie Freitag und Samstag um 23.40 Uhr]. In Saas-Grund müssen Sie umsteigen.'
ANREISE_ZUG_ZEIT = 'Zeitdauer Visp - Saas-Almagell ca. 45 Min.'
ANREISE_AUTO = 'Von Visp aus fahren sie durchs Vispertal, bei der Verzweigung in Stalden Richtung Saastal, in Saas-Grund, bei der Abzweigung nach Saas-Fee halten sie sich links und erreichen so Ihr Reiseziel - den Ferienort Saas-Almagell.'
ANREISE_AUTO_ZEIT = 'Zeitdauer Visp - Saas-Almagell ca. 40 Min.'

# Familie Zurbriggen (befund.md › Familie und weitere Häuser; Preise ab aus den Paketen der Häuser)
FAMILIE = [
    dict(k='montemoro', name='Hotel Monte-Moro', ort='Saas-Almagell', gast='Esther und Fabian', bild='f-montemoro', web='index.html', ab='Zimmer mit Frühstück ab CHF 90.00 pro Person / Tag',
         tags={'preis': 3, 'familie': 3, 'spa': 1, 'gourmet': 0, 'saastal': 3, 'zermatt': 0}),
    dict(k='wellness', name='Wellness & Spa Pirmin Zurbriggen', ort='Saas-Almagell', gast='Esther und Fabian', bild='f-wellness', web='https://www.wellnesshotel-zurbriggen.ch', ab='ab CHF 175,-- (Nice Price)',
         tags={'preis': 1, 'familie': 2, 'spa': 3, 'gourmet': 3, 'saastal': 3, 'zermatt': 0}),
    dict(k='loft', name='Loft-Suite Hotel', ort='Saas-Almagell', gast='Esther und Fabian', bild='f-loft', web='https://www.loftsuite.ch', ab='',
         tags={'preis': 1, 'familie': 1, 'spa': 2, 'gourmet': 2, 'saastal': 3, 'zermatt': 0}),
    dict(k='zermatt', name='Suitenhotel Zurbriggen', ort='Zermatt', gast='Moni und Pirmin', bild='f-zermatt', web='https://zurbriggen.ch/zermatt', ab='Suiten von 23 bis 145 m²',
         tags={'preis': 1, 'familie': 2, 'spa': 1, 'gourmet': 1, 'saastal': 0, 'zermatt': 3}),
    dict(k='rustica', name='Chalet Rustica', ort='Saas-Almagell', gast='Heidi und Damian', bild=None, web='http://chalet-rustica.ch', ab='',
         tags={'preis': 2, 'familie': 2, 'spa': 0, 'gourmet': 0, 'saastal': 2, 'zermatt': 0}),
]

OFFEN = [
    ('Öffnungszeiten und Ruhetage des Röstihüs', 'Station 03, alle Seiten'),
    ('Welches Zimmerfoto zeigt welche Kategorie (die Zimmerseite trennt Budget- und Standardzimmer nicht)', 'de/hotel/zimmer.html'),
    ('Fotos vom Kidsclub', '_quelle'),
    ('Übergabe von Datum und Gästen an das Buchungsfenster von seekda (heute ein eingebetteter Shop ohne Adressparameter)', 'de/buchen.html'),
    ('Ja von Fabian zum Film «Wallis Baby» auf der Seite', '_quelle/video/familie'),
    ('Ob die Gratis-Anreise 2027 weiterläuft', 'de.md'),
    ('Strasse des Hauses (Talstrasse 129, Furusandstrasse 12 oder 10)', 'fakten.json › adresse'),
    ('Storno- und Geschäftsbedingungen', 'alle Seiten'),
    ('Foto des Chalet Rustica', 'Familie Zurbriggen/_quelle/chalet-rustica (nur Grafiken)'),
]

# Röstihüs, Wortlaut der Startseite des Hauses (de.md) und der Restaurantseite (de__restaurant.html.md)
ROESTI_SATZ = 'In unserem Röstihüs setzen wir auf Gastfreundschaft und Regionalität. Unseren Gästen zufolge servieren wir damit die wohl besten Röstis und Cordon Bleus der Region.'
ROESTI_GETRAENKE = 'Auch bei den Getränken setzen wir auf Regionalität. Es werden hervorragende Weine aus dem Kanton Wallis angeboten. Frisches Appenzeller Bier serviert sowie verschiedene Digestifs.'
# Robert 20.10.2026 14:18: «Text irgendwie noch mehr Lust machend». Nur Fakten des Hauses: Karte 18.11.2024 (elf Röstis, Tschug Tschug mit Calvados,
# Saastal mit Spiegelei), ROESTI_SATZ (Cordon bleus), Hotelwein «wurde von Fabian selber kreiert», Halbpension mit wöchentlichem Racletteabend im Stübli.
ROESTI_LUST = ('Elf Röstis stehen auf unserer Karte. Die Rösti Tschug Tschug wird mit Calvados flambiert, die Rösti Saastal kommt mit Spiegelei. '
               'Unsere Gäste sagen, bei uns gebe es die wohl besten Cordon bleus der Region. Dazu passt ein Walliser Wein oder der Hotelwein, den Fabian selbst kreiert hat. '
               'Und einmal in der Woche ist im Stübli Racletteabend für alle mit Halbpension.')
ROESTI_KINDER = 'Natürlich haben wir auch eine kleine Auswahl an Speisen für unsere kleinsten Gäste.'
SPA_FLAECHE = 'Sommer 1700m2 Spa - Winter 1000m2 Spa'   # Startseite des Hauses (Aktuelles nennt 1100 m², offen)
GASTGEBER_KURZ = 'Esther & Fabian Zurbriggen-Zurbriggen'   # Impressum

# Zimmeransicht (24.10.2026, Robert: «für jedes Zimmer noch eine Zimmeransicht … mit allen Infos die uns vorliegen»).
# Booking.com, Eintrag des Hauses (extern/booking/booking-angaben.json, abgerufen 09.10.2026): «Alle Wohneinheiten … sind versehen mit einem Sitzbereich,
# einem Flachbild-TV mit Satellitenkanälen, einem Safe und einem eigenen Badezimmer mit einer Dusche, kostenlosen Pflegeprodukten und einem Haartrockner.
# Die Gästezimmer verfügen über einen Schreibtisch.» Ausstattung: «WLAN inklusive», «Nichtraucherzimmer».
BOOKING_ZIMMER = ['Sitzbereich', 'Flachbild-TV mit Satellitenkanälen', 'Schreibtisch', 'Kostenlose Pflegeprodukte', 'WLAN inklusive', 'Nichtraucherzimmer']
HAUS_ZAHLEN = ('18', '55')   # Zimmer, Betten (Schweiz Tourismus, extern/myswitzerland/myswitzerland-seiten-text.md)
