#!/usr/bin/env python3
"""Station 05 · Markenbauer · Hotel Monte-Moro, Saas-Almagell (Familie Zurbriggen), 17.10.2026.

Bauart wie das bestätigte Markenbuch des Castell Son Claret (castell-bau.py, Fassung 2), Inhalte von diesem Haus:
   python3 bau.py      → marke/zeichen/*, marke/farben.*, marke/probe.html, ../marke.json
   python3 bau2.py     → marke/markenbuch.html, marke/marke.css, marke/marke.js, marke/logo-richtig-falsch/
Nichts hier erfindet eine Farbe oder Schrift: gemessene Töne tragen ihre Fundstelle, abgeleitete Töne sagen, woraus.
Logo: das Haus hat nur eine PNG (allgem_logo.png, 1161 × 475). Die Vektoren sind potrace-Züge davon (Station 2/4), nie neu gezeichnet."""
import json, os, re, html

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(H)                      # _kette/05-markenbauer
M = os.path.join(P, 'marke')
e = html.escape

# ---------------------------------------------------------------- Farben: gemessen, mit Fundstelle
FARBEN = [
    # name, hex, rolle, belegt, fundstelle
    ('Logo-Blau', '#115595', 'knopf', 'Logo', 'allgem_logo.png, häufigste Farbe der Wortmarke (87.674 Bildpunkte, gemessen 17.10.2026)'),
    ('Seiten-Blau', '#005794', 'heutige Seite', 'heutige Seite', 'templates/zerone/css/template.css, Titel und Links; Kanten des Logos (#005793)'),
    ('Himmelblau', '#6BB1DE', 'heutige Seite', 'heutige Seite', 'template.css, 11 Fundstellen: Balken, Knöpfe «Speisekarte», Menü'),
    ('Geschenk-Grün', '#268369', 'heutige Seite', 'heutige Seite', 'template.css, 2 Fundstellen; Minze #CEF2CB in den Geschenk-Kacheln der Startseite. Wird nicht übernommen'),
    ('Seiten-Grau', '#595959', 'heutige Seite', 'heutige Seite', 'template.css, 4 Fundstellen, Lauftext. Wird nicht übernommen'),
    ('Nacht', '#0A2A4A', 'flaeche-dunkel', 'Logo, abgeleitet', 'Logo-Blau, auf 45 Prozent Helligkeit gezogen: die dunkle Fläche der Welt A und der Lesetext'),
    ('Nachtblau', '#0D3F6F', 'kuhle-dunkel', 'Logo, abgeleitet', 'zwischen Nacht und Logo-Blau: Kuhlen und Platten auf dunklem Grund'),
    ('Lärche', '#C67144', 'akzent', 'Foto', 'myswitzerland-00072098 (Fassade im Sommer, 3734 px), Median der besonnten Balkone, 16 Prozent des Bildes'),
    ('Lärche tief', '#9A4F2B', 'betonung-hell', 'Foto, abgeleitet', 'Lärche, dunkler gezogen, damit sie auf Papier als Schrift lesbar ist (Kontrast über 4,5 zu 1)'),
    ('Fassade', '#E7E1DC', 'flaeche-creme', 'Foto', 'myswitzerland-00072098, die weisse Wand im Sonnenlicht, Median'),
    ('Papier', '#F5F2EE', 'flaeche-hell', 'Foto, abgeleitet', 'Fassade, aufgehellt: die Grundfläche, auf der gelesen wird'),
    ('Wandschatten', '#D6CCC1', 'kante', 'Foto, abgeleitet', 'Fassade im Schatten unter den Balkonen: Kanten, Unterseite der Knöpfe'),
    ('Himmel', '#5381BD', 'nur-im-bild', 'Foto', 'myswitzerland-00072098, Himmel über dem Dach, 78 Prozent des oberen Streifens. Bleibt im Bild'),
    ('Schnee', '#E2E2E2', 'nur-im-bild', 'Foto', 'myswitzerland-00072097 (Haus im Winter), Schnee vor dem Haus. Bleibt im Bild'),
    ('Stubenholz', '#9A6521', 'holz', 'Foto', 'restau_restaurant.jpg (Röstihüs), Median des Holzes, 23 Prozent'),
    ('Jute', '#AF8343', 'akzent-b', 'Foto', 'restau_3.jpg, die Kartoffelsäcke vor dem Röstihüs, Median, 35 Prozent'),
    ('Jute tief', '#7E5A2B', 'betonung-hell-b', 'Foto, abgeleitet', 'Jute, dunkler gezogen für Schrift auf Papier (Welt B)'),
    ('Butzenglas', '#DBAF56', 'gold-b', 'Foto', 'TripAdvisor «Raclettestübli» (vom Haus, 2017), Butzenscheiben im Licht, 22 Prozent'),
]
F = {n: h for n, h, *_ in FARBEN}

WELTEN = {
    'a': dict(name='Bergnacht und Lärche', satz='Hell wie die Fassade in der Sonne, dunkel wie der Himmel über Saas-Almagell, wenn die Lichter angehen. Das Dunkel kommt aus dem Blau des Logos, der Akzent aus dem Holz der Balkone.',
              flaechen=['Papier', 'Fassade', 'Nacht'], akzent='Lärche', betonung='Lärche tief', knopf='Logo-Blau',
              css={'nacht': F['Nacht'], 'blau': F['Logo-Blau'], 'papier': F['Papier'], 'creme': F['Fassade'], 'sand': F['Wandschatten'],
                   'gold': F['Lärche'], 'tinte': F['Nacht'], 'beton': F['Lärche tief'], 'tap': F['Logo-Blau'], 'kuhle': F['Nachtblau']}),
    'b': dict(name='Logo-Blau und Butzenglas', satz='Hell wie die Fassade, und wo es dunkel wird, steht das Blau des Logos selbst, so kräftig wie heute auf dem Schild. Der Akzent ist das warme Licht der Butzenscheiben im Raclettestübli und die Jute der Kartoffelsäcke.',
              flaechen=['Papier', 'Fassade', 'Logo-Blau'], akzent='Butzenglas', betonung='Jute tief', knopf='Nacht',
              css={'nacht': F['Logo-Blau'], 'blau': F['Nacht'], 'papier': F['Papier'], 'creme': F['Fassade'], 'sand': F['Wandschatten'],
                   'gold': F['Butzenglas'], 'tinte': F['Nacht'], 'beton': F['Jute tief'], 'tap': F['Logo-Blau'], 'kuhle': '#0E4A82'}),
}

SCHRIFTEN = [
    dict(rolle='titel', name='Fjalla One', schnitt='Regular 400 (eine Stärke), normale Schreibung wie die Wortmarke',
         datei='marke/schriften/FjallaOne-400.woff2', quelle='Google Fonts (Sorkin Type), github.com/google/fonts/ofl/fjallaone, geladen 17.10.2026; Lizenz liegt bei (OFL-FjallaOne.txt)',
         lizenz='SIL Open Font License 1.1, darf vom eigenen Server geladen werden',
         belegt='abgeleitet aus der Wortmarke: schmale, kräftige Groteske mit schräg geschnittenem t, gleiche Strichstärke wie «Monte Moro»; neben acht freien Schriften gelegt (marke/schriftwahl), am nächsten an der Wortmarke',
         satz='Grosse Zeilen, Namen, Preise. Gross und klein geschrieben wie die Wortmarke, nie gesperrt, nie kursiv; Betonung über Farbe.'),
    dict(rolle='lauf', name='Instrument Sans', schnitt='400 und 600', datei='marke/schriften/InstrumentSans-normal-400_600.woff2',
         quelle='Google Fonts, Datei aus _Kette/karte/schriften', lizenz='SIL Open Font License 1.1',
         belegt='nicht aus dem Haus: Roberts Lesetext (Master 2.2). Die heutige Seite liest in Arial, die Unterzeile «Saas-Almagell» der Wortmarke steht in einer Systemschrift (Verdana-artig), beide nicht vom eigenen Server ladbar',
         satz='Lesetext 17 bis 18 px, Zeilenabstand 1,62, höchstens 60 Zeichen breit.'),
    dict(rolle='mono', name='DM Mono', schnitt='400 Versalien', datei='marke/schriften/DMMono-normal-400.woff2',
         quelle='Google Fonts (Colophon), Datei aus _Kette/karte/schriften', lizenz='SIL Open Font License 1.1',
         belegt='nicht aus dem Haus: Roberts Handschrift für Etiketten, Knöpfe und kleine Angaben',
         satz='Knöpfe, Etiketten, Zeiten und Preise in kleinen Versalien, gesperrt.'),
]
SCHRIFT_NICHT = [
    ('Deux Black', 'Speisekarte des Röstihüs (speisekarte.pdf, eingebettet, Stand 18.11.2024): die Namen der Röstis', 'Kaufschrift, Lizenz des Hauses für die Website nicht belegt; bleibt in der Karte'),
    ('Univers LT Std Condensed / Light Condensed', 'Speisekarte des Röstihüs (eingebettet)', 'Kaufschrift von Linotype, Lizenz nicht belegt; Fjalla One trägt dieselbe schmale Haltung'),
    ('Arial', 'heutige Seite (template.css, font-family: Arial, Helvetica, sans-serif)', 'Systemschrift; wird durch Instrument Sans ersetzt'),
]
SCHRIFTWAHL = [  # neben die Wortmarke gelegt (Master 2.2), Datei, Urteil
    ('Fjalla One', 'FjallaOne-400.woff2', 'gewählt', 'Am nächsten: dieselbe Enge, dieselbe Kraft, das t schräg geschnitten wie in «Monte».'),
    ('Sofia Sans Condensed 600', 'SofiaSansCondensed-600.woff2', 'zweite Wahl', 'Ruhiger und runder, etwas breiter als die Wortmarke. Viele Stärken.'),
    ('Encode Sans Condensed 500', 'EncodeSansCondensed-500.woff2', 'zu breit', 'Freundlich, aber deutlich breiter als «Monte Moro».'),
    ('Young Serif', 'YoungSerif-400.woff2', 'bisher in der Analyse', 'Kräftige Serifenschrift der Potentialanalyse. Hat mit der Wortmarke nichts gemein.'),
]

ROESTIS = ['Albert', 'Dracula', 'Macugnaga', 'Exotic Palma', 'Tschug Tschug', 'Gartu', 'Saastal', 'Diavolo', 'Schmugglerrösti', 'Olma', 'Indian Style']

TON = dict(
    charakter=['Ein familiäres Haus mit drei Sternen, 18 Zimmern und 55 Betten in Saas-Almagell, zwei Gehminuten vom Skigebiet, geführt von Esther und Fabian Zurbriggen, die nebenan auch das Wellness & Spa Pirmin Zurbriggen und das Loft-Suite Hotel führen.',
               'Das Haus rechnet für seine Gäste: Bergbahnen und Postautos sind ab der ersten Nacht inbegriffen, die Anreise mit dem öffentlichen Verkehr ab zwei Nächten geschenkt, das grosse Spa nebenan für Hotelgäste offen.',
               'Im Röstihüs kocht es Schweizer Spezialitäten mit eigenen Namen: elf Röstis von Albert bis Indian Style, zwei Hotelweine, die Fabian selbst kreiert hat, zum Schluss der «Monte-Moro-Kopf».'],
    eigene_worte=['«Mehr erleben, weniger zahlen.»', '«Gratis an- und abreisen.»', '«Es lebe die Tradition!»', '«bei uns scheint fast immer die Sonne»',
                  '«Schöne Hotelzimmer - schöne Ferien»', '«mit Liebe, Herz und den besten regionalen Produkten»', '«gemütlich, herzlich eingerichtet»',
                  '«wurde von Fabian selber kreiert» (Hotelweine)', '«Eigenkreation «Monte-Moro-Kopf»»', 'Zurbriggen Spritz · Antrona Spritz',
                  'Röstihüs · Raclettestübli · Sonnenterrasse', 'Rösti ' + ' · '.join(ROESTIS[:6]) + ' …', 'Saas-Almagell · Saastal · Monte Moro · Macugnaga · Val Antrona'],
    nicht=['«Luxus», «exklusiv», «Refugium» und jedes Wort, das das Haus grösser macht, als es ist', '«atemberaubend», «einzigartig», «unvergesslich»',
           '«JETZT BUCHEN» in Versalien als Werbezeile; Knöpfe sagen ruhig, was passiert', 'Zahlen, die sich widersprechen (12 Röstis auf der Startseite, 11 auf der Karte): die Karte gilt',
           'Dreier-Parallelen, «nicht X, sondern Y», Pointen mit Punkt in der Mitte', 'Du-Form; das Haus siezt seine Gäste'])

EIGENE_WELT = dict(
    satz=['Das Hotel Monte-Moro ist die Welt des Bergkamms und des Röstihüs: zwei Gipfel als «MM» im Logo, Balkone aus Lärche in der Sonne, Kartoffelsäcke mit Gesichtern vor der Tür, elf Röstis mit Namen.',
          'Die Seite ist hell und direkt wie das Haus, wird am Abend dunkel wie der Himmel über dem Dorf, und ihre Nähte sind ein Grat nach den Gipfeln des Logos: Flächen enden nicht gerade, sondern als Bergkamm.',
          'Tragend ist, was der Gast bekommt: «Mehr erleben, weniger zahlen» als Rechnung, die man sehen kann (was inbegriffen ist, steht als Liste mit Haken), und das Röstihüs als Karte auf Papier, nicht als Restaurant-Kachel.'],
    unterschied_zu={
        'Carlton-Europe': 'Stadt, Dachterrasse, Vintage, Weinkeller, Türflügel als Auftakt, Navy mit Gold, Zwiebelbogen-Tapete, Libre Baskerville. Das Monte-Moro ist ein Bergdorf mit drei Sternen, schmale Groteske aus der Wortmarke, Lärche statt Gold, Bergkamm statt Bogen.',
        'Grand Beau-Rivage': 'Belle Époque, Portier, Ballsaal, Cormorant und Cinzel, Goldband, Medaillon aus Damast. Beim Monte-Moro gibt es keine Säle, sondern eine Stube; das Medaillon ist der Bergkamm im Kreis, Rhythmus kurz und hell.',
        'Hotel Seiler au Lac': '«Ein Tag am See», Dunst, Sonnenlauf, Wellen-Tapete. Das Monte-Moro erzählt keinen Tag, sondern rechnet vor, was inbegriffen ist, und führt in die Stube.',
        'Waldhotel Doldenhorn': 'Alpine Wellness, Tannengrün und Stahlblau, Siegel, Auszeichnungs-Laufband. Das Monte-Moro hat kein eigenes Spa (es liegt nebenan), kein Grün, Blau aus dem Logo und Lärche aus den Balkonen.',
        'Landgasthof Ruedihus': 'Holzhaus von 1753, Kerze, Abend bis Morgen, Rahmen hängen sich auf. Das Monte-Moro hat keine Geschichte auf der Seite und erfindet keine; es ist ein Haus von heute mit einer Rösti-Karte.',
        'Berghotel Gasterntal': 'Berghütte, Schiefer und Holz, Kleber, Polaroids. Das Monte-Moro ist ein Dorfhotel mit Lift und 18 Zimmern, keine Hütte; Papier und Haken statt Kleber.',
        'Castell Son Claret': 'Landgut auf Mallorca, Sandstein, Rosette, acht Winde, Fahkwang. Das Monte-Moro ist Bergdorf und Stube; der Grat ersetzt die Steinkante, die Rösti-Namen ersetzen die Winde als Takt.',
        'Salt & Silver': 'Restaurant, Hafen bei Nacht, Antonio-Versalien, Vorhang. Auch das Monte-Moro titelt in einer schmalen Groteske, aber gross und klein wie seine Wortmarke, hell am Tag, ohne Vorhang.',
        'Wellness & Spa Pirmin Zurbriggen (Familie)': 'Das Haus nebenan, vier Sterne Superior, Gourmet und 1700 m² Spa, gerade in eigener Arbeit (Station 5): dunkles Oliv und Marcellus in der Analyse. Das Monte-Moro bleibt das hellere, direktere Haus derselben Gastgeber, in Blau und Lärche.',
        'Suitenhotel Zurbriggen, Zermatt (Familie)': 'Andere Gastgeber (Moni und Pirmin), Suiten am Matterhorn, warmes Braun in der Analyse. Das Monte-Moro teilt nur den Familiennamen im Fuss, nicht die Farben.',
        'Tasty Grand Hotel': 'Erfundenes Haus als Werkbank-Vorlage. Dient nur als Muster für die Werkbank, nicht für die Website.'})


# ---------------------------------------------------------------- Dateien des Hauses lesen (potrace-Züge der Logo-PNG)
def lies(p): return open(p, encoding='utf-8').read()


def potrace_g(p):
    s = lies(p)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    vb = ' '.join(str(int(float(x))) for x in vb.split())
    g = re.search(r'<g transform=.*</g>', s, re.S).group(0)
    g = re.sub(r'\s(fill|stroke)="[^"]*"', '', g)
    return vb, re.sub(r'\s+', ' ', g)


ZVB, ZEICHEN_G = potrace_g(os.path.join(M, 'logo/bergkamm-zeichen-potrace.svg'))   # der Bergkamm «MM»
WVB, WORT_G = potrace_g(os.path.join(M, 'logo/wortmarke-potrace.svg'))              # das ganze Logo


def sym_defs():
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            f'<symbol id="bergkamm" viewBox="{ZVB}">{ZEICHEN_G}</symbol>'
            f'<symbol id="wortmarke" viewBox="{WVB}">{WORT_G}</symbol>'
            f'</defs></svg>')


def svg_datei(name, vb, innen, farbe):
    s = f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{farbe}">{innen}</svg>\n'
    open(os.path.join(M, 'zeichen', name), 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- Zeichen als saubere SVG (eine Farbe)
def zeichen():
    for k, farbe in (('blau', F['Logo-Blau']), ('nacht', F['Nacht']), ('laerche', F['Lärche']), ('butzenglas', F['Butzenglas']), ('papier', F['Papier'])):
        svg_datei(f'bergkamm-{k}.svg', ZVB, ZEICHEN_G, farbe)
        svg_datei(f'wortmarke-{k}.svg', WVB, WORT_G, farbe)
    # Medaillon: der Bergkamm im Kreis (für Tapete, Siegel, Reiter im Browser)
    for k, farbe in (('blau', F['Logo-Blau']), ('laerche', F['Lärche']), ('papier', F['Papier'])):
        open(os.path.join(M, 'zeichen', f'medaillon-{k}.svg'), 'w', encoding='utf-8').write(medaillon_svg(farbe))


def medaillon_innen(farbe, deck=1, strich=1.0):
    """Kreis 200 × 200, darin der Bergkamm auf einer Linie (Talboden), wie ein Stempel."""
    zh = 200 * 0.56 * 696 / 3483  # Höhe des Kamms bei 56 % Breite
    return (f'<circle cx="100" cy="100" r="92" fill="none" stroke="{farbe}" stroke-opacity="{deck}" stroke-width="{3*strich}"/>'
            f'<circle cx="100" cy="100" r="83" fill="none" stroke="{farbe}" stroke-opacity="{deck * .6:.3f}" stroke-width="{1.2*strich}"/>'
            f'<svg x="44" y="{108 - zh:.1f}" width="112" height="{zh:.1f}" viewBox="{ZVB}" fill="{farbe}" fill-opacity="{deck}">{ZEICHEN_G}</svg>'
            f'<path d="M40 112 H160" stroke="{farbe}" stroke-opacity="{deck}" stroke-width="{1.6*strich}"/>')


def medaillon_svg(farbe):
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{medaillon_innen(farbe)}</svg>\n'


# ---------------------------------------------------------------- Tapete: Gitter aus Gratlinien mit dem Medaillon, Ton in Ton
def tapete():
    T = 480; r = 104

    def kachel(grund, farbe, deck):
        pos = [(0, 0), (T, 0), (0, T), (T, T), (T / 2, T / 2)]
        med = ''.join(f'<g transform="translate({x - r / 2:.1f} {y - r / 2:.1f}) scale({r / 200})">{medaillon_innen(farbe, deck, 1.6)}</g>' for x, y in pos)
        # das Gitter: Rauten, deren Kanten als feiner Grat gezackt sind (wie die Linie des Bergkamms)
        def grat(x1, y1, x2, y2, n=6, a=7):
            pts = []
            for i in range(n * 2 + 1):
                t = i / (n * 2)
                x = x1 + (x2 - x1) * t; y = y1 + (y2 - y1) * t
                dx, dy = (y2 - y1), -(x2 - x1); ln = (dx * dx + dy * dy) ** .5
                o = (a if i % 2 else 0)
                pts.append(f'{x + dx / ln * o:.1f},{y + dy / ln * o:.1f}')
            return 'M' + ' L'.join(pts)
        h = T / 2
        wege = [grat(h, 0, T, h), grat(T, h, h, T), grat(h, T, 0, h), grat(0, h, h, 0)]
        linien = ''.join(f'<path d="{w}" fill="none" stroke="{farbe}" stroke-opacity="{deck * .7:.3f}" stroke-width="1.2" stroke-linejoin="round"/>' for w in wege)
        return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {T} {T}" width="{T}" height="{T}">'
                f'<rect width="{T}" height="{T}" fill="{grund}"/>{linien}{med}</svg>\n')
    open(os.path.join(M, 'zeichen/tapete-hell.svg'), 'w').write(kachel(F['Papier'], F['Logo-Blau'], 0.16))
    open(os.path.join(M, 'zeichen/tapete-creme.svg'), 'w').write(kachel(F['Fassade'], F['Logo-Blau'], 0.11))
    open(os.path.join(M, 'zeichen/tapete-dunkel.svg'), 'w').write(kachel(F['Nacht'], F['Papier'], 0.10))
    open(os.path.join(M, 'zeichen/tapete-dunkel-b.svg'), 'w').write(kachel(F['Logo-Blau'], F['Papier'], 0.11))


# ---------------------------------------------------------------- Grat: die Naht zwischen zwei Flächen, aus dem Bergkamm des Logos
GRAT_PFAD = 'M0 60 L0 38 L70 30 L118 6 L150 26 L196 14 L250 40 L300 22 L338 34 L380 8 L430 36 L486 18 L540 42 L600 28 L640 36 L700 12 L748 32 L800 24 L860 44 L920 20 L962 34 L1000 26 L1000 60 Z'


def grat_svg(farbe):
    return f'<svg class="grat" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{GRAT_PFAD}" fill="{farbe}"/></svg>'


# ---------------------------------------------------------------- Farbkarten
def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss')).strip('-')


def farben_svg():
    w = 1400
    gruppen = [('Belegt im Logo und auf der heutigen Seite', [f for f in FARBEN if f[3] in ('Logo', 'heutige Seite')]),
               ('Aus dem Logo abgeleitet', [f for f in FARBEN if f[3] == 'Logo, abgeleitet']),
               ('Gemessen in den Hausfotos und daraus abgeleitet', [f for f in FARBEN if f[3].startswith('Foto')])]
    y = 70; teile = [f'<text x="60" y="44" font-family="Fjalla One,Arial Narrow,sans-serif" font-size="30" fill="{F["Nacht"]}">Hotel Monte-Moro · Farben, gemessen · Stand 17.10.2026</text>']
    for titel, liste in gruppen:
        teile.append(f'<text x="60" y="{y + 18}" font-family="DM Mono,Menlo,monospace" font-size="12" letter-spacing="3" fill="{F["Lärche tief"]}">{e(titel.upper())}</text>')
        y += 36
        for i, (n, hx, rolle, bel, fund) in enumerate(liste):
            x = 60 + (i % 5) * 262; yy = y + (i // 5) * 150
            teile.append(f'<rect x="{x}" y="{yy}" width="240" height="90" rx="14" fill="{hx}" stroke="{F["Wandschatten"]}" stroke-width="1"/>')
            teile.append(f'<text x="{x}" y="{yy + 112}" font-family="Fjalla One,Arial Narrow,sans-serif" font-size="18" fill="{F["Nacht"]}">{e(n)}</text>')
            teile.append(f'<text x="{x}" y="{yy + 130}" font-family="DM Mono,Menlo,monospace" font-size="11.5" letter-spacing="1.5" fill="{F["Lärche tief"]}">{hx.upper()} · {e(rolle.upper())}</text>')
        y += ((len(liste) + 4) // 5) * 150 + 30
    h = y + 20
    s = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
         f'<rect width="{w}" height="{h}" fill="{F["Papier"]}"/>' + ''.join(teile) + '</svg>\n')
    open(os.path.join(M, 'farben.svg'), 'w', encoding='utf-8').write(s)
    open(os.path.join(M, 'farben.css'), 'w', encoding='utf-8').write(
        '/* Hotel Monte-Moro · Farben · Markenbauer, Oktober 2026 · jede Zeile mit Fundstelle */\n:root{\n'
        + ''.join(f'  --{slug(n)}:{hx};   /* {n}: {fund} */\n' for n, hx, rolle, bel, fund in FARBEN) + '}\n')
    json.dump([dict(name=n, hex=hx, rolle=rolle, belegt=bel, fundstelle=fund) for n, hx, rolle, bel, fund in FARBEN],
              open(os.path.join(M, 'farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- CSS der Probe (Haus plus Roberts Handschrift)
def css():
    a, b = WELTEN['a']['css'], WELTEN['b']['css']
    def vars_(c): return ''.join(f'--{k}:{v};' for k, v in c.items())
    return f"""
@font-face{{font-family:'Fjalla One';font-weight:400;font-display:block;src:url('schriften/FjallaOne-400.woff2') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:block;src:url('schriften/InstrumentSans-normal-400_600.woff2') format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:block;src:url('schriften/DMMono-normal-400.woff2') format('woff2')}}
@font-face{{font-family:'Fjalla Ersatz';src:local('Arial Narrow'),local('Helvetica Neue Condensed Bold'),local('Arial');size-adjust:96%}}
@font-face{{font-family:'Instrument Ersatz';src:local('Arial');size-adjust:100%}}
:root{{{vars_(a)}--titel:'Fjalla One','Fjalla Ersatz','Arial Narrow',sans-serif;--sans:'Instrument Sans','Instrument Ersatz',Arial,sans-serif;--mono:'DM Mono',ui-monospace,Menlo,monospace;
  --e1:cubic-bezier(.16,1,.3,1);--e2:cubic-bezier(.32,.72,0,1);--feder:cubic-bezier(.28,1.42,.42,1);
  --rand:clamp(20px,4.6vw,76px);--max:1400px;--abschnitt:clamp(72px,8.6vw,136px);--rund:26px;--tapete-hell:url(zeichen/tapete-hell.svg);--tapete-dunkel:url(zeichen/tapete-dunkel.svg)}}
[data-welt="b"]{{{vars_(b)}--tapete-dunkel:url(zeichen/tapete-dunkel-b.svg)}}
*,*::before,*::after{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;overflow-x:clip}}
body{{margin:0;background:var(--papier);color:var(--tinte);font-family:var(--sans);font-size:17.5px;line-height:1.62;-webkit-font-smoothing:antialiased;overflow-x:clip}}
h1,h2,h3,p,ul,figure{{margin:0;padding:0}} ul{{list-style:none}} img{{display:block;max-width:100%;height:auto}} a{{color:inherit;text-decoration:none}}
.fl{{position:relative;padding:var(--abschnitt) var(--rand)}}
.fl--papier{{background:var(--papier) var(--tapete-hell) 50% 0/480px auto;color:var(--tinte)}}
.fl--nacht{{background:var(--nacht) var(--tapete-dunkel) 50% 0/480px auto;color:var(--papier)}}
.in{{max-width:var(--max);margin:0 auto;position:relative}}
.grat{{position:absolute;left:0;right:0;width:100%;height:clamp(22px,3.2vw,46px);display:block;pointer-events:none}}
.fl>.grat--oben{{top:0;transform:translateY(-99%)}}
.ort{{display:flex;align-items:center;gap:14px;font-family:var(--mono);font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--beton)}}
.ort svg{{width:46px;height:auto;fill:currentColor;flex:none}}
.fl--nacht .ort{{color:var(--gold)}}
.t1,.t2{{font-family:var(--titel);font-weight:400;letter-spacing:.005em;line-height:1.06;text-wrap:balance}}
.t1{{font-size:clamp(2.6rem,6vw,6rem)}} .t2{{font-size:clamp(2rem,4vw,3.8rem)}}
.t1 em,.t2 em{{font-style:normal;color:var(--beton)}} .fl--nacht .t1 em,.fl--nacht .t2 em{{color:var(--gold)}}
.z{{display:block;overflow:hidden;padding:.12em .04em .1em;margin:-.12em -.04em -.1em}}
.z>span{{display:block;transform:translateY(112%);transition:transform 1.3s var(--e1);transition-delay:calc(var(--n,0)*110ms)}}
.da .z>span{{transform:none}} .z:nth-child(2)>span{{--n:1}} .z:nth-child(3)>span{{--n:2}}
.lauf{{font-size:clamp(1.02rem,1.18vw,1.16rem);line-height:1.66;max-width:56ch;color:var(--tinte)}} .fl--nacht .lauf{{color:rgba(245,242,238,.86)}}
[data-a]{{opacity:0;transform:translateY(34px);transition:opacity 1.5s var(--e1),transform 2.2s var(--e1);transition-delay:calc(var(--i,0)*120ms)}}
.da [data-a]{{opacity:1;transform:none}}
/* Knopf mit Tiefe: Pille, runder Knauf mit Pfeil in der Gegenfarbe (Roberts Handschrift, Farben des Hauses) */
.kn{{--o:#fbf9f6;--m:var(--creme);--u:var(--sand);--t:var(--tinte);--licht:rgba(255,255,255,.92);--kante:rgba(10,42,74,.22);--tf:rgba(10,42,74,.45);--ko:color-mix(in srgb,var(--blau) 82%,white);--ku:var(--blau);--kt:var(--papier);--klicht:rgba(255,255,255,.26);
  position:relative;overflow:hidden;isolation:isolate;display:inline-flex;align-items:center;gap:14px;height:56px;padding:0 8px 0 27px;border-radius:999px;
  font-family:var(--mono);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;color:var(--t);
  background:linear-gradient(180deg,var(--o) 0%,var(--m) 46%,var(--u) 100%);
  box-shadow:inset 0 1px 0 var(--licht),inset 0 -3px 0 var(--kante),0 1px 1px rgba(0,0,0,.2),0 16px 26px -14px var(--tf);
  transition:transform .55s var(--e2),box-shadow .55s var(--e2)}}
.kn:hover{{transform:translateY(-2px)}}
.kn:active{{transform:translateY(1px) scale(.985);box-shadow:inset 0 2px 5px rgba(0,0,0,.25),inset 0 -1px 0 var(--kante)}}
.kn::after{{content:'';position:absolute;z-index:-1;top:-20%;bottom:-20%;left:0;width:38%;background:linear-gradient(100deg,transparent 0%,rgba(255,255,255,.55) 50%,transparent 100%);transform:translateX(-180%) skewX(-18deg)}}
.kn:hover::after{{transform:translateX(360%) skewX(-18deg);transition:transform 1s var(--e1)}}
.kn i{{flex:none;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,var(--ko),var(--ku));color:var(--kt);box-shadow:inset 0 1px 0 var(--klicht),inset 0 -2px 0 rgba(0,0,0,.28),0 3px 6px rgba(0,0,0,.25)}}
.kn svg{{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.3}}
.fl--nacht .kn{{--o:color-mix(in srgb,var(--kuhle) 70%,white 12%);--m:var(--kuhle);--u:color-mix(in srgb,var(--kuhle) 70%,black);--t:var(--papier);--licht:rgba(255,255,255,.22);--kante:rgba(0,0,0,.45);--tf:rgba(0,0,0,.5);--ko:#fbf9f6;--ku:var(--sand);--kt:var(--nacht);--klicht:rgba(255,255,255,.9)}}
.fl--nacht .kn::after{{background:linear-gradient(100deg,transparent 0%,rgba(255,255,255,.18) 50%,transparent 100%)}}
/* 3D-Kachel: randlos, weicher Schatten, Einkerbung in der Ecke */
.kachel{{position:relative;border-radius:var(--rund);overflow:hidden;box-shadow:0 40px 70px -40px rgba(10,42,74,.55),0 0 0 1px rgba(10,42,74,.06);aspect-ratio:4/3;background:var(--sand);isolation:isolate}}
.kachel img{{width:100%;height:100%;object-fit:cover;transform:scale(1.12);transition:transform 2.7s var(--e1)}}
.da .kachel img{{transform:scale(1)}}
.kerbe{{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:48px 22px 16px;background:linear-gradient(180deg,rgba(10,42,74,0),rgba(10,42,74,.72));font-family:var(--titel);font-size:1.25rem;color:#fff;text-shadow:0 1px 3px rgba(3,10,16,.5)}}
@media (prefers-reduced-motion:reduce){{.z>span,[data-a],.kachel img{{transition:none;animation:none;transform:none;opacity:1}}}}
"""


KNOPF_PFEIL = '<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i>'
HAKEN = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.5"/></svg>'


def knopf(text, href='#'):
    return f'<a class="kn" href="{href}"><span>{e(text)}</span>{KNOPF_PFEIL}</a>'


# ---------------------------------------------------------------- Probe: ein Abschnitt der künftigen Seite, hell, dann das Röstihüs am Abend
INBEGRIFFEN = [  # wörtlich nach de__hotel__preise.html.md («Inklusive») und de.md (Stand 09.10.2026)
    ('Postautos', 'Benutzung Postautos im ganzen Saastal (Sommer/Winter)'),
    ('Bergbahnen', 'Benutzung aller Bergbahnen im Saastal (ohne Metro Alpin) (Sommer)'),
    ('Frühstücksbuffet', 'ZF und HP: Frühstücksbuffet; Halbpension: wöchentlicher Racletteabend'),
    ('Kidsclub', 'täglich Mo - Sa 16:30 bis 21:00 Uhr'),
    ('Hotelparkplatz', ''),
]


def probe():
    zk = f'<svg viewBox="{ZVB}" aria-hidden="true"><use href="#bergkamm"/></svg>'
    liste = ''.join(f'<li data-a style="--i:{i + 2}"><i>{HAKEN}</i><span><b>{e(a)}</b>{e(b)}</span></li>' for i, (a, b) in enumerate(INBEGRIFFEN))
    roesti = ''.join(f'<span>Rösti {e(n)}</span><i>{zk}</i>' if not n.endswith('rösti') else f'<span>{e(n)}</span><i>{zk}</i>' for n in ROESTIS)
    s = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Probe · Hotel Monte-Moro</title><meta name="robots" content="noindex">
<link rel="preload" href="schriften/FjallaOne-400.woff2" as="font" type="font/woff2" crossorigin>
<style>{css()}
.probe-kopf{{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:9;display:flex;gap:6px;padding:5px;border-radius:999px;background:rgba(10,42,74,.18);backdrop-filter:none;white-space:nowrap}}
.probe-kopf button{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:8px 14px;border-radius:999px;color:var(--tinte);background:var(--papier);border:0;cursor:pointer;white-space:nowrap}}
@media (max-width:600px){{.probe-kopf button{{font-size:10.5px;padding:8px 14px}} .probe-kopf .l{{display:none}}}}
body.aufnahme .probe-kopf{{display:none}}
.probe-kopf button[aria-pressed="true"]{{background:var(--nacht);color:var(--papier)}}
.zwei{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:clamp(28px,5vw,80px);align-items:center}}
.text{{display:grid;gap:22px;justify-items:start}}
.inkl{{display:grid;gap:0;width:100%;max-width:560px;border-radius:22px;padding:8px 22px;background:linear-gradient(180deg,#fff,var(--papier) 60%,var(--creme));box-shadow:inset 0 1px 0 #fff,inset 0 0 0 1px rgba(10,42,74,.1),0 30px 44px -30px rgba(10,42,74,.45)}}
.inkl li{{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;padding:13px 0;border-bottom:1px solid rgba(10,42,74,.1)}} .inkl li:last-child{{border-bottom:0}}
.inkl i{{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,color-mix(in srgb,var(--blau) 80%,white),var(--blau));color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 4px 8px -4px rgba(10,42,74,.6)}}
.inkl i svg{{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}
.inkl span{{display:flex;flex-direction:column;font-size:.98rem;line-height:1.45;color:color-mix(in srgb,var(--tinte) 80%,transparent)}} .inkl b{{font-family:var(--titel);font-weight:400;font-size:1.22rem;color:var(--tinte)}}
@media (max-width:860px){{.zwei{{grid-template-columns:1fr}} .fl{{padding-top:clamp(54px,9vw,90px);padding-bottom:clamp(64px,10vw,100px)}}}}
.stube{{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(28px,5vw,80px);align-items:center}}
@media (max-width:860px){{.stube{{grid-template-columns:1fr}}}}
.karte{{position:relative;border-radius:18px;padding:clamp(26px,3vw,40px);background:linear-gradient(180deg,#fffdf9,#f3eee6);color:var(--nacht);box-shadow:0 2px 0 var(--sand),0 50px 70px -40px rgba(0,0,0,.7);transform:rotate(-1.2deg)}}
.karte h3{{font-family:var(--titel);font-weight:400;font-size:clamp(1.6rem,2.4vw,2.2rem);line-height:1.05;display:flex;align-items:center;gap:14px}}
.karte h3 svg{{width:56px;height:auto;fill:var(--beton)}}
.karte p{{margin-top:6px;font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--beton)}}
.karte ol{{margin:18px 0 0;padding:0;list-style:none;columns:2;column-gap:28px}}
.karte li{{break-inside:avoid;padding:7px 0;border-bottom:1px dotted rgba(10,42,74,.22);font-family:var(--titel);font-size:1.1rem}}
.lz{{margin-top:clamp(40px,5vw,72px);overflow:hidden;border-block:1px solid rgba(245,242,238,.16);padding:16px 0;mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}}
.lz__b{{display:flex;width:max-content;align-items:center;gap:22px;animation:lz 46s linear infinite}}
.lz__b span{{font-family:var(--titel);font-size:clamp(1.3rem,2vw,1.9rem);color:var(--papier);white-space:nowrap}}
.lz__b i svg{{width:38px;height:auto;fill:var(--gold);display:block}}
@keyframes lz{{to{{transform:translateX(-50%)}}}}
@media (prefers-reduced-motion:reduce){{.lz__b{{animation:none}}}}
</style></head><body data-welt="a">
{sym_defs()}
<section class="fl fl--papier" id="inbegriffen">
  <div class="in zwei">
    <div class="text">
      <p class="ort" data-a style="--i:0">{zk}Saas-Almagell · Saastal</p>
      <h2 class="t1"><span class="z"><span>Mehr erleben,</span></span><span class="z"><span><em>weniger zahlen.</em></span></span></h2>
      <p class="lauf" data-a style="--i:1">Was im Preis steckt, steht vorn: Bergbahnen und Postautos im Sommer und Herbst ab der 1. Übernachtung inklusive, und die An- und Abreise mit dem öffentlichen Verkehr ab 2 Nächten geschenkt.</p>
      <ul class="inkl">{liste}</ul>
      <div data-a style="--i:8">{knopf('Zimmer buchen')}</div>
    </div>
    <figure class="kachel" data-a style="--i:1"><img src="bilder/fassade-sommer.jpg" alt="Das Hotel Monte-Moro im Sommer, mit den Balkonen aus Lärche" width="1800" height="1180"><figcaption class="kerbe">Hotel Monte-Moro</figcaption></figure>
  </div>
</section>
<section class="fl fl--nacht" id="roestihues">
  {grat_svg('var(--nacht)').replace('class="grat"', 'class="grat grat--oben"')}
  <div class="in stube">
    <div class="text">
      <p class="ort" data-a style="--i:0">{zk}Restaurant Röstihüs</p>
      <h2 class="t2"><span class="z"><span>Es lebe</span></span><span class="z"><span><em>die Tradition!</em></span></span></h2>
      <p class="lauf" data-a style="--i:1">Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten, die mit Liebe, Herz und den besten regionalen Produkten zubereitet werden.</p>
      <div data-a style="--i:2">{knopf('Tisch reservieren')}</div>
    </div>
    <div class="karte" data-a style="--i:2"><h3>{zk}Elf Röstis</h3><p>Speisekarte des Röstihüs, Seite 4</p><ol>{''.join(f'<li>{e(n if n.endswith("rösti") else "Rösti " + n)}</li>' for n in ROESTIS)}</ol></div>
  </div>
  <div class="lz" aria-hidden="true"><div class="lz__b">{roesti}{roesti}</div></div>
</section>
<div class="probe-kopf" role="group" aria-label="Farbwelt"><button data-w="a" aria-pressed="true">Welt A<span class="l"> · {e(WELTEN['a']['name'])}</span></button><button data-w="b" aria-pressed="false">Welt B<span class="l"> · {e(WELTEN['b']['name'])}</span></button></div>
<script>
(function(){{
  var w=new URLSearchParams(location.search).get('welt');if(w==='b')setze('b');
  function setze(x){{document.body.setAttribute('data-welt',x);document.querySelectorAll('.probe-kopf button').forEach(function(b){{b.setAttribute('aria-pressed',b.dataset.w===x?'true':'false')}})}}
  document.querySelectorAll('.probe-kopf button').forEach(function(b){{b.addEventListener('click',function(){{setze(b.dataset.w)}})}});
  var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{en.target.classList.add('da');io.unobserve(en.target)}}}})}},{{rootMargin:'0px 0px -12% 0px'}});
  document.querySelectorAll('section').forEach(function(s){{io.observe(s)}});
}})();
</script></body></html>"""
    open(os.path.join(M, 'probe.html'), 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- marke.json
def marke_json():
    d = dict(
        haus='Hotel Monte-Moro', ort='Saas-Almagell, Wallis', stand='2026-10-17',
        farben=[dict(name=n, hex=hx, rolle=rolle, belegt=bel, fundstelle=fund) for n, hx, rolle, bel, fund in FARBEN],
        farbwelten=[dict(k=k, name=w['name'], satz=w['satz'], flaechen=[F[x] for x in w['flaechen']], akzent=F[w['akzent']], betonung=F[w['betonung']], knopf=F[w['knopf']], css=w['css']) for k, w in WELTEN.items()],
        farbwelt_gewaehlt=dict(k='a', name=WELTEN['a']['name'], wort='Robert 18.10.2026 00:10: «Und Farbe A. Die Schrift so wie im Logo. Und Übergang Linie wie ein Bergkamm.»'),
        schriften=[dict(rolle=s['rolle'], name=s['name'], schnitt=s['schnitt'], datei=s['datei'], quelle=s['quelle'], lizenz=s['lizenz'], belegt=s['belegt']) for s in SCHRIFTEN],
        schriften_nicht=[dict(name=a, wo=b, warum=c) for a, b, c in SCHRIFT_NICHT],
        schriftwahl=[dict(name=a, datei='marke/schriften/' + b, urteil=c, satz=d_) for a, b, c, d_ in SCHRIFTWAHL],
        wortmarke=dict(datei='marke/logo/logo-original-1161px.png', art='png', vektor='marke/logo/wortmarke-potrace.svg (potrace-Zug der PNG, Station 4)',
                       zeichen_allein='marke/logo/bergkamm-zeichen-potrace.svg', abgeleitete_titelschrift='Fjalla One 400 (aus der Wortmarke «Monte Moro»: schmale Groteske, schräg geschnittenes t)',
                       herkunft='https://www.monte-moro.ch/images/allgemeines/logo.png (_quelle/website/bilder/allgem_logo.png, 09.10.2026)'),
        zeichen=[f'marke/zeichen/{n}' for n in sorted(os.listdir(os.path.join(M, 'zeichen')))],
        tapete=dict(hell='marke/zeichen/tapete-hell.svg', creme='marke/zeichen/tapete-creme.svg', dunkel='marke/zeichen/tapete-dunkel.svg', dunkel_b='marke/zeichen/tapete-dunkel-b.svg',
                    motiv='Medaillon (Bergkamm im Kreis) im Rautengitter, dessen Kanten als feiner Grat gezackt sind', rapport_px=480, deckkraft={'hell': 0.16, 'dunkel': 0.10}),
        linie=dict(name='Der Grat', satz='Die Linie des Hauses ist der Bergkamm aus dem Logo; der Grat ist danach gezogen (kein Zug aus der Datei), von Robert am 18.10.2026 freigegeben («Übergang Linie wie ein Bergkamm»): Nähte zwischen hellen und dunklen Flächen enden als Grat, nicht gerade. Knöpfe bleiben Pillen mit Knauf (Roberts Handschrift), Leisten schmal und gerade. Keine Einkerbungen (Robert 18.10.2026): Bildnamen stehen unten im Foto auf weichem Schatten.', pfad=GRAT_PFAD),
        ton=TON, welt='land', eigene_welt=EIGENE_WELT, familie_machart=None,
        familie=dict(name='Familie Zurbriggen', haeuser=['Wellness & Spa Pirmin Zurbriggen (Station 5 läuft)', 'Loft-Suite Hotel (Kapitel der Wellness-Seite)', 'Suitenhotel Zurbriggen, Zermatt (Station 5 läuft)'],
                     stand='noch keine Seite der Familie abgenommen; der Fuss wird bei allen Häusern gleich gebaut (Master 2.8), Farben und Zeichen je Haus'),
        probe=dict(datei='marke/probe.html', abschnitte=['Mehr erleben, weniger zahlen (hell, Tapete, Liste mit Haken, 3D-Kachel mit Einkerbung, Knopf)', 'Röstihüs, Es lebe die Tradition! (dunkel, Grat als Naht, Karte auf Papier, Laufzeile mit den elf Röstis)'],
                   saetze_des_hauses=['Mehr erleben, weniger zahlen.', 'Es lebe die Tradition!', 'Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten …'],
                   eigene_saetze_von_mir=['Was im Preis steckt, steht vorn: Bergbahnen und Postautos im Sommer und Herbst ab der 1. Übernachtung inklusive, und die An- und Abreise mit dem öffentlichen Verkehr ab 2 Nächten geschenkt.', 'Elf Röstis']),
        markenbuch='marke/markenbuch.html', logo_regeln='marke/logo-richtig-falsch/index.html')
    json.dump(d, open(os.path.join(P, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    zeichen(); tapete(); farben_svg(); probe(); marke_json()
    print('gebaut:', M)
