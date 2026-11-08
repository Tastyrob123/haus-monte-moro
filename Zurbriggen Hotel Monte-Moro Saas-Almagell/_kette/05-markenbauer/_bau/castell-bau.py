#!/usr/bin/env python3
"""Station 05 · Markenbauer · Castell Son Claret. Baut aus den Originaldateien des Hauses das Paket marke/:
   Tapete aus der Rosette, Farbkarten, Probe (zwei Farbwelten), Logo richtig und falsch, Markenbuch, marke.json.
   python3 bau.py            → schreibt alles unter marke/ und marke.json
   Danach: bash aufnahmen.sh → Bilder unter bilder/ (Playwright, unsichtbar), briefing.json
   Nichts hier erfindet eine Farbe oder Schrift: jede Angabe trägt ihre Fundstelle (FARBEN, SCHRIFTEN)."""
import json, os, re, html

H = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(H, 'marke')
e = html.escape

# ---------------------------------------------------------------- Farben: gemessen, mit Fundstelle
FARBEN = [
    # name, hex, rolle, belegt, fundstelle
    ('Logo-Grau', '#575756', 'schrift', 'Logo', 'logo-dark.svg und sygnet.svg (fill), app.css 42 Fundstellen als Textfarbe'),
    ('Sand', '#BBB19D', 'heutige Seite', 'heutige Seite', 'Profitroom-Theme, Hauptfarbe, 8.758 Fundstellen im HTML aller 302 Seiten'),
    ('Stein', '#9B9382', 'betonung-hell', 'heutige Seite', 'Profitroom-Theme, Zweitfarbe (.wa-secondary-color), 9.060 Fundstellen'),
    ('Kalk', '#ECEAE4', 'flaeche-hell', 'heutige Seite', 'app.1c757d1e.css, 22 Fundstellen, helle Fläche'),
    ('Ornament-Grau', '#948F85', 'tapete', 'heutige Seite', 'ornament.svg (fill, Deckkraft 0,07) hinter dem Einstiegstext'),
    ('Nacht', '#0C1F41', 'flaeche-dunkel', 'Drucksache', 'Sa Clastra «Rosa de los vientos» (PDF, ENG/GER/ESP), Grund oben'),
    ('Nachtblau', '#1F3968', 'knopf-dunkel', 'Drucksache', 'Sa Clastra «Rosa de los vientos» (PDF), Grund unten'),
    ('Bar-Gold', '#C0A062', 'akzent', 'Drucksache', 'Castell Bar Karte 2025 (PDF), Band unten, 73 % der Fläche'),
    ('Mosaik-Gold', '#C8BA58', 'zeichen-bar', 'Drucksache', 'Castell Bar Karte 2025 (PDF), Mosaik-Zeichen'),
    ('Bar-Braun', '#8A7761', 'schrift-bar', 'Drucksache', 'Castell Bar Karte 2025 (PDF), Titel «CASTELL BAR»'),
    ('Hochzeits-Grau', '#696665', 'schrift-druck', 'Drucksache', 'Wedding Kit 2026 (PDF), Unterzeile «More than just a luxury hotel»'),
    ('Michelin-Rot', '#FB0024', 'sonder', 'Logo', 'sa-crasta.svg (Zeichen Sa Clastra), nur für den Stern'),
    ('Sandstein hell', '#E4DBCC', 'flaeche-creme', 'Foto', 'castell5.jpg, Fassade im Mittag, 13 % des Bildes'),
    ('Sandstein', '#D7C7B2', 'kante', 'Foto', 'castell3.jpg, Torpfeiler, 14 % des Bildes'),
    ('Oliv', '#72764D', 'betonung-hell-b', 'Foto', 'cscpanorama02.jpg, Olivenhain und Tramuntana, 21 %'),
    ('Oliv-Nacht', '#272915', 'flaeche-dunkel-b', 'Foto', 'castellsonclaretluxuryboutiquehotelmallorca4.jpg, Schatten im Hain, 21 %'),
    ('Oliv tief', '#414624', 'knopf-dunkel-b', 'Foto', 'cscpanorama02.jpg, 24 % des Bildes'),
    ('Messing', '#A67A4F', 'akzent-b', 'Foto', 'bar01.jpg, Theke der Castell Bar, 22 %'),
    ('Bougainvillea', 'nicht als Fläche', 'farbpunkt', 'Foto', 'Gartenfotos; bleibt im Bild, nie in der Gestaltung (Design-DNA: ein Farbpunkt je Bild)'),
]
F = {n: h for n, h, *_ in FARBEN}

WELTEN = {
    'a': dict(name='Stein und Nacht', satz='Sandstein am Tag, die Nacht von Sa Clastra am Abend. Das Blau kommt aus der Windrose des Hauses, das Gold aus der Karte der Castell Bar.',
              flaechen=['Kalk', 'Sandstein hell', 'Nacht'], akzent='Bar-Gold', betonung='Stein', knopf='Nachtblau',
              css={'nacht': F['Nacht'], 'blau': F['Nachtblau'], 'papier': F['Kalk'], 'creme': F['Sandstein hell'], 'sand': F['Sandstein'],
                   'gold': F['Bar-Gold'], 'tinte': F['Logo-Grau'], 'beton': F['Stein'], 'tap': F['Ornament-Grau']}),
    'b': dict(name='Oliv und Messing', satz='Sandstein am Tag, der Olivenhain am Abend. Das Dunkel kommt aus den Hainen unter dem Galatzó, das Messing von der Theke der Castell Bar.',
              flaechen=['Kalk', 'Sandstein hell', 'Oliv-Nacht'], akzent='Messing', betonung='Oliv', knopf='Oliv tief',
              css={'nacht': F['Oliv-Nacht'], 'blau': F['Oliv tief'], 'papier': F['Kalk'], 'creme': F['Sandstein hell'], 'sand': F['Sandstein'],
                   'gold': F['Bar-Gold'], 'tinte': F['Logo-Grau'], 'beton': F['Oliv'], 'tap': F['Ornament-Grau']}),
}

SCHRIFTEN = [
    dict(rolle='titel', name='Fahkwang', schnitt='400 (300 und 500 liegen bei)', datei='marke/schriften/fahkwang-400-latin.woff2',
         quelle='Google Fonts (Cadson Demak), auf der heutigen Seite über fonts.profitroom.com geladen; Dateien aus der Potenzialanalyse (castell-potenzialanalyse/assets/fonts)',
         lizenz='SIL Open Font License 1.1, darf vom eigenen Server geladen werden',
         belegt='Titelschrift aller 302 Seiten (.wa-headline-font {font-family: Fahkwang !important})',
         satz='Grosse Zeilen, Namen, Preise. Normale Schreibung, nie fett, nie kursiv; Betonung über Farbe.'),
    dict(rolle='kapitel', name='Montserrat', schnitt='400 Versalien, gesperrt 0,28 em', datei='marke/schriften/montserrat-400-latin.woff2',
         quelle='Google Fonts (Julieta Ulanovsky), auf der heutigen Seite geladen; Dateien aus der Potenzialanalyse',
         lizenz='SIL Open Font License 1.1',
         belegt='Unterzeile der Wortmarke «MALLORCA» (gleiche Geometrie, gesperrte Versalien) und Lauftext der heutigen Seite',
         satz='Ortszeile, Kapitelzeilen, kleine Versalzeilen wie in der Wortmarke.'),
    dict(rolle='lauf', name='Montserrat', schnitt='400 und 500', datei='marke/schriften/montserrat-400-latin.woff2',
         quelle='wie oben', lizenz='SIL Open Font License 1.1',
         belegt='Lauftext aller 302 Seiten (.wa-paragraph-font {font-family: Montserrat !important})',
         satz='Lesetext 17 bis 18 px, Zeilenabstand 1,64, höchstens 60 Zeichen breit. Nie dünn.'),
    dict(rolle='mono', name='DM Mono', schnitt='400 Versalien', datei='marke/schriften/DMMono-normal-400.woff2',
         quelle='Google Fonts (Colophon), Datei aus _Kette/karte/schriften', lizenz='SIL Open Font License 1.1',
         belegt='nicht aus dem Haus: Roberts Handschrift für Etiketten, Knöpfe und kleine Angaben',
         satz='Knöpfe, Etiketten, Zeiten und Preise in kleinen Versalien.'),
]
SCHRIFT_NICHT = [
    ('Josefin Sans, Gidole, Aileron, Glacial Indifference', 'Wedding Kit 2026 und MICE Kit 2026 (eingebettet in den PDFs)', 'Druckschriften der Agentur, auf der Website nicht; werden nicht übernommen'),
    ('Calibri, Abadi', 'Menü «Viento y Memoria» (PDF)', 'Systemschriften der Karte; werden nicht übernommen'),
    ('Schreibschrift «Erinnerung»', 'Menü «Viento y Memoria», Titelseite', 'nicht benannt, nicht belegt; die Wortbild-Fassung bleibt als Bild in der Karte'),
]

TON = dict(
    charakter=['Ein mallorquinisches Landgut, in Aufzeichnungen seit 1450, seit Mai 2013 Hotel: 132 Hektar am Fuss des Galatzó, 43 Zimmer und Suiten, in Privatbesitz und unabhängig verwaltet.',
               'Das Haus erzählt Mallorca über Erde, Garten und Wind: eigenes Olivenöl, eigene Bäckerei, Gemüse aus dem Garten mit ESMENT, in Sa Clastra ein Menü nach den acht Winden der Insel.',
               'Luxus heisst hier leise und aus dem Ort: «The Luxury of being Yourself», EarthCheck seit 2023, 5 € je Buchung an die Marilles-Stiftung, Castell Classics mit der Kühne-Stiftung.'],
    eigene_worte=['«Es gibt Orte, die man einfach nicht beschreiben kann. Und auch nicht vergleichen.»', '«taucht man hier in das wahre Mallorca ein»', '«The Luxury of being Yourself»', '«Inspired by Nature»',
                  '«Wind und Erinnerung» (Sa Clastra)', '«Wurzeln & Avantgarde» (Olivera)', '«Eine Rückkehr zum Wesentlichen» (Olivera)', '«Nicht nur reden, sondern auch handeln»',
                  '«viel mehr sein als nur eine Luxus-Enklave für wenige»', '«Gemeinsam erreichen wir Grösse»', '«True alchemy happens when nature ignites flavor» (Castell Bar)',
                  'Possessió · Tafona · Aljub · Huerto', 'Sa Clastra · Olivera · Castell Bar · Bellesa de Claret · Sa Tafona · Castell Classics', 'Tramuntana · Galatzó · Es Capdellà',
                  'Tramuntana · Gregal · Llevant · Xaloc · Migjorn · Garbí · Ponent · Mistral (die acht Winde)'],
    nicht=['«Luxushotel Mallorca», «Sterne-Restaurant Mallorca», «Luxusrefugium» und jede fett gesetzte Suchwort-Formel', '«unvergleichliches Mittelmeer-Erlebnis», «atemberaubend», «einzigartig», «exklusiv»',
           '«Best-Preis-Garantie», «Sofortbestätigung» als Werbezeilen im Lesetext', '«Buchen sie» und jedes Du (22 Seiten der heutigen Seite duzen)',
           'Dreier-Parallelen, «nicht X, sondern Y», Pointen mit Punkt in der Mitte', 'Superlative in eigener Sache; die Auszeichnungen sprechen für sich'])

EIGENE_WELT = dict(
    satz=['Castell Son Claret ist die Welt des Landguts: Sandstein und Zisterne, Olivenhain und Garten, das Tor mit den zwei Pfeilern, die Allee bei Nacht, der Galatzó im Rücken.',
          'Die Seite ist hell wie der Tag auf dem Gut und wird nur dort dunkel, wo das Haus es selbst ist: am Abend in Sa Clastra mit der Windrose und am Tor bei Nacht. Zeichen sind die drei Türme, die Rosette und die Windrose, nicht Gold und Damast.',
          'Tragend ist das Anwesen selbst: Orte statt Kategorien (Castell, Wasserturm, Garten, Pool, Tafona), die acht Winde als Takt der Seite, Steinkanten statt Goldbänder, Tapete aus der Rosette statt Medaillon.'],
    unterschied_zu={
        'Carlton-Europe': 'Stadt, Dachterrasse, Vintage, Weinkeller, Türflügel als Auftakt, Navy mit Gold und Zwiebelbogen-Tapete. Das Castell ist Land, Stein und Garten, hell am Tag, Tor statt Tür.',
        'Grand Beau-Rivage': 'Belle Époque, Portier, Ballsaal, Rundgang durch die Räume, Cormorant und Cinzel, Goldband, Medaillon-Tapete, fünf Fenster. Das Castell hat keine Säle als Helden, sondern das Gelände; Fahkwang statt Garamond, Rosette statt Medaillon, kein Goldband.',
        'Hotel Seiler au Lac': '«Ein Tag am See», Dunst statt Vorhang, Sonnenlauf, Fahrplan-Tafel, Wellen-Tapete. Das Castell erzählt nicht den Tag, sondern den Ort: Tor, Gut, Winde.',
        'Waldhotel Doldenhorn': 'Alpine Wellness, Tannengrün und Stahlblau, Siegel, Drift im Dreiklang, Auszeichnungs-Laufband. Das Castell ist mediterran und mineralisch, kein Grün als Fläche in Welt A, Türme statt Siegel.',
        'Landgasthof Ruedihus': 'Holzhaus von 1753, Stube, Kerze, Abend bis Morgen, Rahmen hängen sich auf, Kompass der Herkunft. Das Castell ist Stein statt Holz, Tag statt Abend; die Windrose zeigt Winde, nicht Lieferanten.',
        'Berghotel Gasterntal': 'Berghütte, Schiefer und Holz, Kleber, Polaroids paarweise, «einfach, luxuriös». Das Castell ist ein Grand-Luxe-Haus mit 132 Hektar; nichts ist einfach, alles ist leise.',
        'Salt & Silver': 'Restaurant, Hafen bei Nacht, Antonio-Versalien, Vorhang mit Zeichen, Kursblatt, Bühne mit Abzügen. Das Castell ist ein Hotel mit normaler Schreibung, hell, ohne Vorhang.',
        'Tasty Grand Hotel': 'Erfundenes Haus als Werkbank-Vorlage. Dient nur als Muster für die Werkbank, nicht für die Website.'})

# ---------------------------------------------------------------- Dateien des Hauses lesen
def lies(p): return open(p, encoding='utf-8').read()
ORN = lies(os.path.join(M, 'logo/ornament.svg'))
ORN_PFADE = ''.join(re.findall(r'<path[^>]*/>', ORN))
ORN_PFADE = re.sub(r'\s(id|data-name|fill)="[^"]*"', '', ORN_PFADE)
SYG = lies(os.path.join(M, 'logo/sygnet.svg'))
SYG_INNEN = re.sub(r'\sfill="[^"]*"', '', re.search(r'<g id="Group_8381"[^>]*>(.*?)</g>\s*</g>', SYG, re.S).group(0))
SYG_INNEN = re.sub(r'\s(id|data-name)="[^"]*"', '', SYG_INNEN)
LOGO = lies(os.path.join(M, 'logo/logo-dark.svg'))
LOGO_INNEN = re.search(r'<g id="logo"[^>]*>(.*)</g>\s*</svg>', LOGO, re.S).group(1)
LOGO_INNEN = re.sub(r'\sfill="[^"]*"', '', LOGO_INNEN)
LOGO_INNEN = re.sub(r'\s(id|data-name)="[^"]*"', '', LOGO_INNEN)
LOGO_INNEN = LOGO_INNEN.replace('clip-path="url(#clip-path)"', '')
ROSE = lies(os.path.join(M, 'zeichen/windrose-sa-clastra.svg'))
ROSE_VB = re.search(r'viewBox="([^"]+)"', ROSE).group(1)
ROSE_INNEN = re.sub(r'\sfill="[^"]*"', '', re.search(r'<g[^>]*>(.*)</g>', ROSE, re.S).group(0))
MOS = lies(os.path.join(M, 'zeichen/castell-bar-mosaik.svg'))
MOS_VB = re.search(r'viewBox="([^"]+)"', MOS).group(1)
MOS_INNEN = re.sub(r'\sfill="[^"]*"', '', re.search(r'<g[^>]*>(.*)</g>', MOS, re.S).group(0))

def sym_defs():
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            f'<symbol id="rosette" viewBox="0 0 592 590.711">{ORN_PFADE}</symbol>'
            f'<symbol id="tuerme" viewBox="0 0 36.485 19.394"><g transform="translate(-659.305 -23)">{SYG_INNEN}</g></symbol>'
            f'<symbol id="wortmarke" viewBox="0 0 194.49 66.291"><g transform="translate(-582.755 -23)">{LOGO_INNEN}</g></symbol>'
            f'<symbol id="windrose" viewBox="{ROSE_VB}">{ROSE_INNEN}</symbol>'
            f'<symbol id="mosaik" viewBox="{MOS_VB}">{MOS_INNEN}</symbol>'
            f'</defs></svg>')

def svg_datei(name, vb, innen, farbe):
    s = f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{farbe}">{innen}</svg>\n'
    open(os.path.join(M, 'zeichen', name), 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- Zeichen als saubere SVG (eine Farbe, kein Clip, kein Opacity)
def zeichen():
    for k, farbe in (('grau', F['Logo-Grau']), ('gold', F['Bar-Gold']), ('kalk', F['Kalk'])):
        svg_datei(f'tuerme-{k}.svg', '0 0 36.485 19.394', f'<g transform="translate(-659.305 -23)">{SYG_INNEN}</g>', farbe)
        svg_datei(f'rosette-{k}.svg', '0 0 592 590.711', ORN_PFADE, farbe)
        svg_datei(f'wortmarke-{k}.svg', '0 0 194.49 66.291', f'<g transform="translate(-582.755 -23)">{LOGO_INNEN}</g>', farbe)
        svg_datei(f'windrose-{k}.svg', ROSE_VB, ROSE_INNEN, farbe)
    svg_datei('mosaik-castell-bar.svg', MOS_VB, MOS_INNEN, F['Mosaik-Gold'])

# ---------------------------------------------------------------- Tapete: Gitter mit Rosette, Ton in Ton
def tapete():
    T = 560; r = 150
    def kachel(grund, farbe, deck):
        pos = [(0, 0), (T, 0), (0, T), (T, T), (T / 2, T / 2)]
        rosen = ''.join(f'<use href="#r" x="{x - r / 2:.1f}" y="{y - r / 2:.1f}" width="{r}" height="{r}"/>' for x, y in pos)
        # feine Linien des Gitters zwischen den Rosetten (wie die Linien im heutigen Ornament-Grund)
        linien = (f'<path d="M{T/2} 0 L{T} {T/2} L{T/2} {T} L0 {T/2} Z" fill="none" stroke="{farbe}" stroke-opacity="{deck * .55:.3f}" stroke-width="1.2"/>')
        return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {T} {T}" width="{T}" height="{T}">'
                f'<defs><symbol id="r" viewBox="0 0 592 590.711">{ORN_PFADE}</symbol></defs>'
                f'<rect width="{T}" height="{T}" fill="{grund}"/><g fill="{farbe}" fill-opacity="{deck}">{rosen}</g>{linien}</svg>\n')
    open(os.path.join(M, 'zeichen/tapete-hell.svg'), 'w').write(kachel(F['Kalk'], F['Ornament-Grau'], 0.085))
    open(os.path.join(M, 'zeichen/tapete-dunkel.svg'), 'w').write(kachel(F['Nacht'], F['Kalk'], 0.075))
    open(os.path.join(M, 'zeichen/tapete-dunkel-b.svg'), 'w').write(kachel(F['Oliv-Nacht'], F['Kalk'], 0.075))

# ---------------------------------------------------------------- Farbkarten
def farben_svg():
    w, h = 1400, 0
    gruppen = [('Belegt im Logo und auf der heutigen Seite', [f for f in FARBEN if f[3] in ('Logo', 'heutige Seite')]),
               ('Belegt in den Drucksachen des Hauses', [f for f in FARBEN if f[3] == 'Drucksache']),
               ('Gemessen in den Hausfotos', [f for f in FARBEN if f[3] == 'Foto' and f[1].startswith('#')])]
    y = 70; teile = []
    teile.append(f'<text x="60" y="44" font-family="Fahkwang,Georgia,serif" font-size="30" fill="{F["Logo-Grau"]}">Castell Son Claret · Farben, gemessen · Stand 15.10.2026</text>')
    for titel, liste in gruppen:
        teile.append(f'<text x="60" y="{y + 18}" font-family="Montserrat,Arial,sans-serif" font-size="12" letter-spacing="3" fill="{F["Stein"]}">{e(titel.upper())}</text>')
        y += 36
        for i, (n, hx, rolle, bel, fund) in enumerate(liste):
            x = 60 + (i % 5) * 262; yy = y + (i // 5) * 150
            teile.append(f'<rect x="{x}" y="{yy}" width="240" height="90" rx="14" fill="{hx}" stroke="{F["Sandstein"]}" stroke-width="1"/>')
            teile.append(f'<text x="{x}" y="{yy + 112}" font-family="Fahkwang,Georgia,serif" font-size="17" fill="{F["Logo-Grau"]}">{e(n)}</text>')
            teile.append(f'<text x="{x}" y="{yy + 130}" font-family="DM Mono,Menlo,monospace" font-size="11.5" letter-spacing="1.5" fill="{F["Stein"]}">{hx.upper()} · {e(rolle.upper())}</text>')
        y += ((len(liste) + 4) // 5) * 150 + 30
    h = y + 20
    s = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
         f'<rect width="{w}" height="{h}" fill="{F["Kalk"]}"/>' + ''.join(teile) + '</svg>\n')
    open(os.path.join(M, 'farben.svg'), 'w', encoding='utf-8').write(s)
    # dazu CSS und JSON wie bei Le Livre
    open(os.path.join(M, 'farben.css'), 'w', encoding='utf-8').write(
        '/* Castell Son Claret · Farben · Markenbauer, Oktober 2026 · jede Zeile mit Fundstelle */\n:root{\n'
        + ''.join(f'  --{slug(n)}:{hx};   /* {n}: {fund} */\n' for n, hx, rolle, bel, fund in FARBEN if hx.startswith('#')) + '}\n')
    json.dump([dict(name=n, hex=hx, rolle=rolle, belegt=bel, fundstelle=fund) for n, hx, rolle, bel, fund in FARBEN],
              open(os.path.join(M, 'farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ü', 'ue').replace('ä', 'ae').replace('ö', 'oe').replace('ß', 'ss')).strip('-')

# ---------------------------------------------------------------- gemeinsames CSS (Haus plus Roberts Handschrift)
def css():
    a, b = WELTEN['a']['css'], WELTEN['b']['css']
    def vars_(c): return ''.join(f'--{k}:{v};' for k, v in c.items())
    return f"""
@font-face{{font-family:'Fahkwang';font-weight:300;font-display:block;src:url('schriften/fahkwang-300-latin.woff2') format('woff2')}}
@font-face{{font-family:'Fahkwang';font-weight:400;font-display:block;src:url('schriften/fahkwang-400-latin.woff2') format('woff2')}}
@font-face{{font-family:'Fahkwang';font-weight:500;font-display:block;src:url('schriften/fahkwang-500-latin.woff2') format('woff2')}}
@font-face{{font-family:'Fahkwang';font-weight:400;font-display:block;src:url('schriften/fahkwang-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA,U+1E00-1EFF}}
@font-face{{font-family:'Montserrat';font-weight:400;font-display:block;src:url('schriften/montserrat-400-latin.woff2') format('woff2')}}
@font-face{{font-family:'Montserrat';font-weight:500;font-display:block;src:url('schriften/montserrat-500-latin.woff2') format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:block;src:url('schriften/DMMono-normal-400.woff2') format('woff2')}}
@font-face{{font-family:'Fahkwang Ersatz';src:local('Georgia');size-adjust:104%}}
@font-face{{font-family:'Montserrat Ersatz';src:local('Arial');size-adjust:104%}}
:root{{{vars_(a)}--serif:'Fahkwang','Fahkwang Ersatz',Georgia,serif;--sans:'Montserrat','Montserrat Ersatz',Arial,sans-serif;--mono:'DM Mono',ui-monospace,Menlo,monospace;
  --e1:cubic-bezier(.16,1,.3,1);--e2:cubic-bezier(.32,.72,0,1);--feder:cubic-bezier(.28,1.42,.42,1);
  --rand:clamp(20px,4.6vw,76px);--max:1480px;--abschnitt:clamp(72px,8.6vw,136px);--rund:28px;--tapete-hell:url(zeichen/tapete-hell.svg);--tapete-dunkel:url(zeichen/tapete-dunkel.svg)}}
[data-welt="b"]{{{vars_(b)}--tapete-dunkel:url(zeichen/tapete-dunkel-b.svg)}}
*,*::before,*::after{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;overflow-x:clip}}
body{{margin:0;background:var(--papier);color:var(--tinte);font-family:var(--sans);font-size:17.5px;line-height:1.64;-webkit-font-smoothing:antialiased;overflow-x:clip}}
h1,h2,h3,p,ul,figure{{margin:0;padding:0}} ul{{list-style:none}} img{{display:block;max-width:100%;height:auto}} a{{color:inherit;text-decoration:none}}
button{{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}}
.fl{{position:relative;padding:var(--abschnitt) var(--rand)}}
.fl--papier{{background:var(--papier) var(--tapete-hell) 50% 0/560px auto;color:var(--tinte)}}
.fl--creme{{background:var(--creme);color:var(--tinte)}}
.fl--nacht{{background:var(--nacht) var(--tapete-dunkel) 50% 0/560px auto;color:var(--papier)}}
.in{{max-width:var(--max);margin:0 auto;position:relative}}
.ort{{font-family:var(--sans);font-weight:400;font-size:12.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--beton)}}
.fl--nacht .ort{{color:var(--gold)}}
.t1,.t2{{font-family:var(--serif);font-weight:400;letter-spacing:0;line-height:1.08;text-wrap:balance}}
.t1{{font-size:clamp(2.4rem,5.4vw,5.4rem);line-height:1.04}} .t2{{font-size:clamp(1.7rem,3.2vw,3.1rem)}}
.t1 em,.t2 em{{font-style:normal;color:var(--beton)}} .fl--nacht .t1 em,.fl--nacht .t2 em{{color:var(--gold)}}
.z{{display:block;overflow:hidden;padding:.16em .04em .14em;margin:-.16em -.04em -.14em}}
.z>span{{display:block;transform:translateY(112%);transition:transform 1.3s var(--e1);transition-delay:calc(var(--n,0)*110ms)}}
.da .z>span{{transform:none}} .z:nth-child(2)>span{{--n:1}} .z:nth-child(3)>span{{--n:2}}
.lauf{{font-size:clamp(1.02rem,1.18vw,1.18rem);line-height:1.68;max-width:56ch;color:var(--tinte)}} .fl--nacht .lauf{{color:rgba(236,234,228,.84)}}
[data-a]{{opacity:0;transform:translateY(34px);transition:opacity 1.5s var(--e1),transform 2.2s var(--e1);transition-delay:calc(var(--i,0)*120ms)}}
.da [data-a]{{opacity:1;transform:none}}
.mono{{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase}}
/* Knopf mit Tiefe: Pille, runder Knauf mit Pfeil in der Gegenfarbe (Roberts Handschrift, Farben des Hauses) */
.kn{{--o:#f6f1e8;--m:var(--creme);--u:var(--sand);--t:var(--tinte);--licht:rgba(255,255,255,.92);--kante:rgba(87,87,86,.32);--tf:rgba(40,36,30,.5);--ko:var(--blau);--ku:var(--nacht);--kt:var(--papier);--klicht:rgba(255,255,255,.22);
  position:relative;overflow:hidden;isolation:isolate;display:inline-flex;align-items:center;gap:14px;height:56px;padding:0 8px 0 27px;border-radius:999px;
  font-family:var(--mono);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;color:var(--t);
  background:linear-gradient(180deg,var(--o) 0%,var(--m) 46%,var(--u) 100%);
  box-shadow:inset 0 1px 0 var(--licht),inset 0 -3px 0 var(--kante),inset 0 0 0 1px rgba(255,255,255,.08),0 1px 1px rgba(0,0,0,.25),0 16px 26px -14px var(--tf);
  transition:transform .55s var(--e2),box-shadow .55s var(--e2)}}
.kn:hover{{transform:translateY(-2px);box-shadow:inset 0 1px 0 var(--licht),inset 0 -3px 0 var(--kante),inset 0 0 0 1px rgba(255,255,255,.08),0 2px 2px rgba(0,0,0,.2),0 26px 34px -16px var(--tf)}}
.kn:active{{transform:translateY(1px) scale(.985);box-shadow:inset 0 2px 5px rgba(0,0,0,.25),inset 0 -1px 0 var(--kante),0 1px 1px rgba(0,0,0,.25)}}
.kn::after{{content:'';position:absolute;z-index:-1;top:-20%;bottom:-20%;left:0;width:38%;background:linear-gradient(100deg,transparent 0%,rgba(255,255,255,.55) 50%,transparent 100%);transform:translateX(-180%) skewX(-18deg)}}
.kn:hover::after{{transform:translateX(360%) skewX(-18deg);transition:transform 1s var(--e1)}}
.kn i{{flex:none;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,var(--ko),var(--ku));color:var(--kt);box-shadow:inset 0 1px 0 var(--klicht),inset 0 -2px 0 rgba(0,0,0,.28),0 3px 6px rgba(0,0,0,.3);transition:transform .6s var(--e2)}}
.kn:hover i{{transform:translateX(2px) scale(1.05)}} .kn svg{{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.3}}
.fl--nacht .kn{{--o:color-mix(in srgb,var(--blau) 80%,white);--m:var(--blau);--u:var(--nacht);--t:var(--papier);--licht:rgba(255,255,255,.22);--kante:rgba(0,0,0,.5);--tf:rgba(0,0,0,.55);--ko:#f6f1e8;--ku:var(--sand);--kt:var(--tinte);--klicht:rgba(255,255,255,.9)}}
.fl--nacht .kn::after{{background:linear-gradient(100deg,transparent 0%,rgba(255,255,255,.18) 50%,transparent 100%)}}
/* 3D-Kachel: randlos, weicher Schatten, Einkerbung in der Ecke */
.kachel{{position:relative;border-radius:var(--rund);overflow:hidden;box-shadow:0 40px 70px -40px rgba(40,36,30,.6),0 0 0 1px rgba(87,87,86,.08);aspect-ratio:4/3;background:var(--sand);isolation:isolate}}
.kachel img{{width:100%;height:100%;object-fit:cover;transform:scale(1.14);transition:transform 2.7s var(--e1)}}
.da .kachel img{{transform:scale(1)}}
.kerbe{{position:absolute;left:0;top:0;padding:12px 22px 14px 0;background:var(--papier);border-radius:0 0 22px 0;font-family:var(--serif);font-size:1.15rem;color:var(--tinte);z-index:2}}
.kerbe::before,.kerbe::after{{content:'';position:absolute;width:22px;height:22px;background:radial-gradient(circle at 100% 100%,transparent 21px,var(--papier) 22px)}}
.kerbe::before{{left:100%;top:0}} .kerbe::after{{left:0;top:100%}}
.kachel[data-r]{{transform:translateY(90px) scale(.96);transition:transform 2.4s var(--feder)}} .da .kachel[data-r]{{transform:none}}
@supports (animation-timeline:view()){{.kachel[data-r]{{animation:zug linear both;animation-timeline:view();animation-range:cover 0% cover 58vh;transition:none}}
  .da .kachel[data-r]{{animation:zug linear both,puls 2.6s var(--feder) both;animation-timeline:view(),auto;animation-range:cover 0% cover 58vh,normal}}}}
@keyframes zug{{from{{transform:translateY(90px)}}to{{transform:translateY(0)}}}}
@keyframes puls{{0%{{scale:.95}}100%{{scale:1}}}}
@media (prefers-reduced-motion:reduce){{.z>span,[data-a],.kachel[data-r],.kachel img{{transition:none;animation:none;transform:none;opacity:1}}}}
"""

KNOPF_PFEIL = '<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i>'

def knopf(text, href='#'):
    return f'<a class="kn" href="{href}"><span>{e(text)}</span>{KNOPF_PFEIL}</a>'

# ---------------------------------------------------------------- Probe: ein Abschnitt der künftigen Seite, hell, dazu das Nacht-Band von Sa Clastra
def probe():
    winde = ['Tramuntana', 'Gregal', 'Llevant', 'Xaloc', 'Migjorn', 'Garbí', 'Ponent', 'Mistral']
    s = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Probe · Castell Son Claret</title><meta name="robots" content="noindex">
<style>{css()}
.probe-kopf{{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:9;display:flex;gap:6px;padding:5px;border-radius:999px;background:rgba(87,87,86,.16);white-space:nowrap}}
.probe-kopf button{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:8px 14px;border-radius:999px;color:var(--tinte);background:var(--papier);white-space:nowrap}}
@media (max-width:600px){{.probe-kopf button{{font-size:10px;padding:7px 10px;letter-spacing:.08em}}}}
body.aufnahme .probe-kopf{{display:none}}
.probe-kopf button[aria-pressed="true"]{{background:var(--nacht);color:var(--papier)}}
.zwei{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(28px,5vw,80px);align-items:center}}
.text{{display:grid;gap:22px;justify-items:start}}
@media (max-width:860px){{.zwei{{grid-template-columns:1fr}} .text{{order:1}} .kachel{{order:0}} .fl{{padding-top:clamp(54px,9vw,90px);padding-bottom:clamp(54px,9vw,90px)}}}}
.band{{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(26px,4vw,64px);align-items:center}}
.band .rose{{width:clamp(130px,16vw,220px);aspect-ratio:1281/1357;color:var(--gold)}} .band .rose svg{{width:100%;height:100%;fill:currentColor}}
.winde{{display:flex;flex-wrap:wrap;gap:10px 26px;font-family:var(--sans);font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:rgba(236,234,228,.62)}}
.winde li:first-child{{color:var(--gold)}}
@media (max-width:860px){{.band{{grid-template-columns:1fr}} .band .rose{{width:140px}}}}
.marke{{display:flex;align-items:center;gap:14px;color:var(--tinte)}} .marke svg{{height:28px;width:auto;fill:currentColor}}
</style></head><body data-welt="a">
{sym_defs()}
<section class="fl fl--papier" id="anwesen">
  <div class="in zwei">
    <div class="text">
      <p class="ort" data-a style="--i:0">Es Capdellà · Mallorca</p>
      <h2 class="t1"><span class="z"><span>Ein Landgut am Fuß</span></span><span class="z"><span><em>des Galatzó.</em></span></span></h2>
      <p class="lauf" data-a style="--i:1">«Es gibt Orte, die man einfach nicht beschreiben kann. Und auch nicht vergleichen.» Castell Son Claret ist ein 132 Hektar großes Anwesen, das sich in Privatbesitz befindet und unabhängig verwaltet wird. Umgeben von einem parkähnlichen Garten sowie einer atemberaubenden Bergwelt und inspiriert von Traditionen und Kultur der Insel, taucht man hier in das wahre Mallorca ein.</p>
      <div data-a style="--i:2">{knopf('Das Anwesen entdecken')}</div>
    </div>
    <figure class="kachel" data-r><img src="bilder/luftbild.jpg" alt="Castell Son Claret von oben: das Landgut zwischen Olivenhainen und dem Tramuntana-Gebirge" width="1800" height="1199"><span class="kerbe">Seit 1450</span></figure>
  </div>
</section>
<section class="fl fl--nacht" id="winde">
  <div class="in band">
    <div class="rose" data-a style="--i:0"><svg viewBox="{ROSE_VB}" aria-hidden="true"><use href="#windrose"/></svg></div>
    <div class="text">
      <p class="ort" data-a style="--i:1">Sa Clastra · ein Michelin-Stern</p>
      <h2 class="t2"><span class="z"><span>Wind und Erinnerung.</span></span></h2>
      <p class="lauf" data-a style="--i:2">Mallorca ist eine Insel der Winde, sie formen nicht nur die Landschaft und das Klima, sondern prägen seit Jahrhunderten auch die Kultur und Gastronomie. Jeder Gang des Menüs trägt den Namen eines Windes.</p>
      <ul class="winde" data-a style="--i:3">{''.join(f'<li>{w}</li>' for w in winde)}</ul>
      <div data-a style="--i:4">{knopf('Tisch in Sa Clastra reservieren')}</div>
    </div>
  </div>
</section>
<div class="probe-kopf" role="group" aria-label="Farbwelt"><button data-w="a" aria-pressed="true">A · Stein und Nacht</button><button data-w="b" aria-pressed="false">B · Oliv und Messing</button></div>
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

# ---------------------------------------------------------------- Logo richtig und falsch
def logo_regeln():
    def wm(farbe, st=''):
        return f'<svg viewBox="0 0 194.49 66.291" style="fill:{farbe};{st}" aria-hidden="true"><use href="#wortmarke"/></svg>'
    def tm(farbe, st=''):
        return f'<svg viewBox="0 0 36.485 19.394" style="fill:{farbe};{st}" aria-hidden="true"><use href="#tuerme"/></svg>'
    k = F
    richtig = [
        ('Wortmarke auf Papier', f'<div class="fla" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:260px")}</div>', 'Das Original: Zeichen und Name in Logo-Grau auf heller Fläche.'),
        ('Wortmarke auf Nacht', f'<div class="fla" style="background:{k["Nacht"]}">{wm(k["Kalk"], "width:260px")}</div>', 'Auf dunkler Fläche in Kalk, so wie das Haus es heute mit logo-white.svg macht.'),
        ('Das Zeichen allein', f'<div class="fla" style="background:{k["Sandstein hell"]}">{tm(k["Logo-Grau"], "width:72px")}</div>', 'Die drei Türme stehen allein in der Leiste, als Siegel und über Überschriften.'),
        ('Zeichen in Gold', f'<div class="fla" style="background:{k["Nacht"]}">{tm(k["Bar-Gold"], "width:72px")}</div>', 'Auf Nacht darf das Zeichen in Bar-Gold stehen, wie das Mosaik auf der Karte der Castell Bar.'),
        ('Mindestgrösse', f'<div class="fla" style="background:{k["Kalk"]};gap:22px;flex-direction:column;padding:0 18px;text-align:center">{wm(k["Logo-Grau"], "width:150px")}<span class="mono" style="font-size:10px">150 px · darunter nur das Zeichen (ab 22 px)</span></div>', 'Die Wortmarke bleibt lesbar bis 150 px Breite. Kleiner steht nur das Zeichen.'),
        ('Schutzraum', f'<div class="fla" style="background:{k["Kalk"]}"><div style="position:relative;padding:36px;outline:1px dashed {k["Stein"]}">{wm(k["Logo-Grau"], "width:220px")}<span class="mono" style="position:absolute;right:6px;top:6px;color:{k["Stein"]}">1 × Zeichenhöhe</span></div></div>', 'Rundum so viel Luft wie das Zeichen hoch ist. Nichts rückt näher heran.'),
        ('Auf dem Foto', f'<div class="fla foto" style="background:url(bilder/allee-nacht.jpg) 50% 50%/cover">{wm(k["Kalk"], "width:240px")}</div>', 'Nur auf einem ruhigen Foto mit Dunkel im Bild, in Kalk, nie mit Schatten oder Saum.'),
    ]
    falsch = [
        ('Gestreckt', f'<div class="fla" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:300px;height:70px;transform:scaleX(1.35)")}</div>', 'Die Proportion bleibt. Nie breiter oder höher gezogen.'),
        ('Umgefärbt', f'<div class="fla" style="background:{k["Kalk"]}">{wm("#1d8a4a", "width:260px")}</div>', 'Nur Logo-Grau, Kalk und Bar-Gold. Kein Grün, kein Rot, kein Verlauf.'),
        ('Mit Schatten und Glanz', f'<div class="fla" style="background:{k["Nacht"]}">{wm(k["Kalk"], "width:260px;filter:drop-shadow(0 6px 10px rgba(0,0,0,.9)) drop-shadow(0 0 18px rgba(192,160,98,.9))")}</div>', 'Kein Schatten, kein Leuchten, kein Relief. Das Zeichen liegt flach.'),
        ('Neu gesetzt', f'<div class="fla" style="background:{k["Kalk"]};font-family:Georgia,serif;font-style:italic;font-size:30px;color:{k["Logo-Grau"]}">Castell Son Claret</div>', 'Der Name wird nie in einer anderen Schrift neu geschrieben. Die Wortmarke ist eine Datei.'),
        ('Auf unruhigem Foto', f'<div class="fla foto" style="background:url(bilder/garten.jpg) 50% 60%/cover">{wm(k["Kalk"], "width:240px")}</div>', 'Blüten und Blätter hinter den Buchstaben: unlesbar. Dunkel ins Bild rechnen oder ein anderes Foto.'),
        ('Gedreht und beschnitten', f'<div class="fla" style="background:{k["Kalk"]};overflow:hidden">{wm(k["Logo-Grau"], "width:260px;transform:rotate(-12deg) translate(60px,10px)")}</div>', 'Die Wortmarke steht immer waagrecht und ganz.'),
        ('Zu klein', f'<div class="fla" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:80px")}</div>', 'Unter 150 px ist der Name nicht mehr lesbar. Dann nur das Zeichen.'),
    ]
    def karten(liste, kl):
        return ''.join(f'<li class="k {kl}"><div class="bild">{b}</div><h3>{e(t)}</h3><p>{e(s)}</p></li>' for t, b, s in liste)
    s = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Logo richtig und falsch · Castell Son Claret</title>
<style>{css()}
body{{background:{F['Kalk']}}} .wrap{{max-width:1480px;margin:0 auto;padding:48px var(--rand) 80px}}
h1{{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,4vw,3.4rem);margin-bottom:8px}} h2{{font-family:var(--serif);font-weight:400;font-size:1.7rem;margin:54px 0 20px;display:flex;align-items:center;gap:14px}}
h2 b{{font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;padding:6px 12px;border-radius:999px;background:{F['Nacht']};color:{F['Kalk']}}} h2.f b{{background:#8a2b2b}}
.gr{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px}}
.k{{background:#fff;border-radius:22px;padding:14px;box-shadow:0 20px 40px -30px rgba(40,36,30,.5),0 0 0 1px rgba(87,87,86,.08)}}
.k .bild{{border-radius:14px;overflow:hidden}} .fla{{height:190px;display:flex;align-items:center;justify-content:center;gap:16px;border-radius:14px}}
.k h3{{font-family:var(--serif);font-weight:400;font-size:1.25rem;margin:14px 4px 4px}} .k p{{font-size:.95rem;color:#6b6a68;margin:0 4px;line-height:1.5}}
.f .bild{{position:relative}} .f .bild::after{{content:'';position:absolute;inset:0;border-radius:14px;box-shadow:inset 0 0 0 2px #8a2b2b}}
.f .bild::before{{content:'';position:absolute;right:12px;top:12px;width:30px;height:30px;z-index:3;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'><circle cx='15' cy='15' r='15' fill='%238a2b2b'/><path d='M10 10l10 10M20 10L10 20' stroke='white' stroke-width='2.4' stroke-linecap='round'/></svg>") center/contain no-repeat}}
.mono{{color:{F['Stein']}}}
</style></head><body>{sym_defs()}<div class="wrap">
<p class="ort">Castell Son Claret · Markenbuch</p><h1>Logo richtig und falsch.</h1><p class="lauf">Die Wortmarke und das Zeichen kommen als Datei aus dem Haus (logo-dark.svg, logo-white.svg, sygnet.svg). Sie werden eingesetzt, nie nachgezeichnet, nie verändert.</p>
<h2><b>Richtig</b> So steht das Logo</h2><ul class="gr">{karten(richtig, 'r')}</ul>
<h2 class="f"><b>Falsch</b> So nicht</h2><ul class="gr">{karten(falsch, 'f')}</ul>
</div></body></html>"""
    open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(s)
    # relative Pfade: die Seite liegt eine Ebene tiefer
    t = open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), encoding='utf-8').read()
    t = t.replace("url('schriften/", "url('../schriften/").replace('url(zeichen/', 'url(../zeichen/').replace('url(bilder/', 'url(../bilder/')
    open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(t)

# ---------------------------------------------------------------- Markenbuch (Werkbank-Stil, Stück von Le Livre)
def markenbuch():
    def kopf(ort, titel, satz='', dunkel=False):
        return (f'<header class="kopf"><p class="ort">{e(ort)}</p><h2 class="t2"><span class="z"><span>{titel}</span></span></h2>' + (f'<p class="lauf">{satz}</p>' if satz else '') + '</header>')
    farbkarten = ''.join(
        f'<li class="fk"><i style="background:{hx}"></i><b>{e(n)}</b><span class="mono">{hx.upper()}</span><small>{e(bel)} · {e(fund)}</small></li>'
        for n, hx, rolle, bel, fund in FARBEN if hx.startswith('#'))
    welten = ''.join(
        f'''<li class="welt" data-welt="{k}"><div class="wflaechen"><i style="background:{w['css']['papier']}"></i><i style="background:{w['css']['creme']}"></i><i style="background:{w['css']['nacht']}"></i><i style="background:{w['css']['blau']}"></i><i style="background:{w['css']['gold']}"></i><i style="background:{w['css']['beton']}"></i></div>
        <h3 class="t3">{k.upper()} · {e(w['name'])}</h3><p>{e(w['satz'])}</p>
        <p class="mono">Flächen {e(' · '.join(w['flaechen']))} · Akzent {e(w['akzent'])} · Betonung {e(w['betonung'])} · Knöpfe {e(w['knopf'])}</p>
        <figure class="fen"><img src="../bilder/probe-{k}-rechner.jpg" alt="Probe Farbwelt {k.upper()} am Rechner" loading="lazy"></figure>
        <p><a class="kn" href="probe.html?welt={k}" target="_blank"><span>Probe {k.upper()} öffnen</span>{KNOPF_PFEIL}</a></p></li>''' for k, w in WELTEN.items())
    schriften = ''.join(
        f'''<li class="schrift"><p class="ort">{e(s['rolle'])}</p><p class="muster muster--{s['rolle']}">{'Ein Landgut am Fuß des Galatzó.' if s['rolle']=='titel' else 'Es Capdellà · Mallorca · seit 1450' if s['rolle']=='kapitel' else 'Tisch in Sa Clastra reservieren' if s['rolle']=='mono' else 'Umgeben von einem parkähnlichen Garten sowie einer Bergwelt, inspiriert von Traditionen und Kultur der Insel.'}</p>
        <h3 class="t3">{e(s['name'])} <small>{e(s['schnitt'])}</small></h3><p>{e(s['satz'])}</p><p class="klein"><b>Belegt:</b> {e(s['belegt'])}<br><b>Datei:</b> {e(s['datei'])}<br><b>Lizenz:</b> {e(s['lizenz'])}</p></li>''' for s in SCHRIFTEN)
    schrift_nicht = ''.join(f'<li><b>{e(a)}</b> · {e(b)} · {e(c)}</li>' for a, b, c in SCHRIFT_NICHT)
    ton = (f'<div class="drei"><div><p class="ort">Charakter</p><ul class="liste">{"".join(f"<li>{e(x)}</li>" for x in TON["charakter"])}</ul></div>'
           f'<div><p class="ort">Worte des Hauses</p><ul class="liste">{"".join(f"<li>{e(x)}</li>" for x in TON["eigene_worte"])}</ul></div>'
           f'<div><p class="ort">Nicht</p><ul class="liste nicht">{"".join(f"<li>{e(x)}</li>" for x in TON["nicht"])}</ul></div></div>')
    welt_saetze = ''.join(f'<p class="lauf">{e(x)}</p>' for x in EIGENE_WELT['satz'])
    unterschiede = ''.join(f'<li><b>{e(k)}</b><span>{e(v)}</span></li>' for k, v in EIGENE_WELT['unterschied_zu'].items())
    s = f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Markenbuch · Castell Son Claret</title><meta name="robots" content="noindex">
<style>{css()}
body{{background:var(--nacht)}}
.blatt{{border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);padding-bottom:calc(var(--abschnitt) + var(--rund))}}
.kopf{{display:grid;gap:16px;max-width:60ch;margin-bottom:clamp(30px,4vw,56px)}}
.hero{{min-height:92svh;display:grid;align-content:end;gap:22px;padding-bottom:clamp(60px,8vw,110px)}}
.hero .wm{{width:min(420px,60vw);fill:var(--papier)}} .hero .wm svg{{width:100%;height:auto}}
.t3{{font-family:var(--serif);font-weight:400;font-size:1.5rem;line-height:1.15}} .t3 small{{font-family:var(--sans);font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--beton);margin-left:10px}}
.fl--nacht .t3 small{{color:var(--gold)}}
.zeichen{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}}
.zeichen li{{border-radius:22px;padding:28px;display:grid;gap:14px;justify-items:center;text-align:center;background:rgba(255,255,255,.04);box-shadow:inset 0 0 0 1px rgba(236,234,228,.12)}}
.fl--papier .zeichen li{{background:#fff;box-shadow:0 20px 40px -30px rgba(40,36,30,.5),0 0 0 1px rgba(87,87,86,.08)}}
.zeichen svg{{height:84px;width:auto;max-width:100%;fill:currentColor}} .zeichen .wmk svg{{height:64px}}
.zeichen b{{font-family:var(--serif);font-weight:400;font-size:1.15rem}} .zeichen small{{font-size:.86rem;color:rgba(236,234,228,.7)}} .fl--papier .zeichen small{{color:#6b6a68}}
.farben{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}}
.fk{{display:grid;gap:6px;background:#fff;border-radius:18px;padding:12px;box-shadow:0 0 0 1px rgba(87,87,86,.1)}} .fk i{{display:block;height:80px;border-radius:12px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}}
.fk b{{font-family:var(--serif);font-weight:400;font-size:1.1rem}} .fk .mono{{color:var(--beton)}} .fk small{{font-size:.82rem;line-height:1.4;color:#6b6a68}}
.welten{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:26px}}
.welt{{display:grid;gap:14px;background:rgba(255,255,255,.04);border-radius:26px;padding:22px;box-shadow:inset 0 0 0 1px rgba(236,234,228,.12)}}
.wflaechen{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}} .wflaechen i{{height:46px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}}
.welt p{{color:rgba(236,234,228,.84)}} .welt .mono{{color:var(--gold)}}
.fen{{border-radius:16px;overflow:hidden;background:rgba(0,0,0,.2);box-shadow:0 0 0 1px rgba(236,234,228,.12),0 50px 70px -40px rgba(0,0,0,.8)}}
.schriften{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:22px}}
.schrift{{background:#fff;border-radius:22px;padding:22px;display:grid;gap:10px;box-shadow:0 0 0 1px rgba(87,87,86,.1)}}
.muster{{font-size:2.1rem;line-height:1.1;font-family:var(--serif)}} .muster--kapitel{{font-family:var(--sans);font-size:13px;letter-spacing:.28em;text-transform:uppercase;color:var(--beton)}}
.muster--lauf{{font-family:var(--sans);font-size:1.05rem;line-height:1.64}} .muster--mono{{font-family:var(--mono);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase}}
.klein{{font-size:.84rem;line-height:1.5;color:#6b6a68}} .klein b{{font-weight:500;color:var(--tinte)}}
.tap{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px}} .tap li{{height:280px;border-radius:22px;background-size:420px auto;box-shadow:inset 0 0 0 1px rgba(236,234,228,.14);display:grid;align-content:end;padding:18px}}
.tap li span{{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase}}
.drei{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:30px}}
.liste{{display:grid;gap:10px}} .liste li{{position:relative;padding-left:22px;line-height:1.5}} .liste li::before{{content:'';position:absolute;left:0;top:.66em;width:9px;height:1.5px;background:var(--beton)}}
.liste.nicht li::before{{background:#8a2b2b}}
.unter{{display:grid;gap:12px}} .unter li{{display:grid;grid-template-columns:minmax(140px,220px) 1fr;gap:18px;padding:12px 0;border-bottom:1px solid rgba(236,234,228,.14)}}
.unter b{{font-family:var(--serif);font-weight:400;font-size:1.1rem}} .unter span{{color:rgba(236,234,228,.84)}}
.bilder{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:22px}}
.handys{{display:grid;grid-template-columns:repeat(2,minmax(0,300px));gap:22px;margin-top:22px}} @media (max-width:680px){{.handys{{grid-template-columns:1fr 1fr}}}}
.dateien{{columns:2;gap:40px;font-family:var(--mono);font-size:12px;letter-spacing:.06em;line-height:2}} @media (max-width:720px){{.dateien{{columns:1}}}}
.kn-reihe{{display:flex;flex-wrap:wrap;gap:12px}}
</style></head><body>{sym_defs()}
<section class="fl fl--nacht"><div class="in hero">
  <p class="ort" data-a>Markenbuch · Station 05 · Stand 15.10.2026</p>
  <div class="wm" data-a style="--i:1"><svg viewBox="0 0 194.49 66.291" aria-label="Castell Son Claret"><use href="#wortmarke"/></svg></div>
  <h1 class="t1"><span class="z"><span>Stein, Garten, Wind.</span></span><span class="z"><span><em>Die Marke des Castell Son Claret.</em></span></span></h1>
  <p class="lauf" data-a style="--i:2">Alles auf diesen Seiten kommt aus dem Haus: das Zeichen mit den drei Türmen, die Rosette, die Windrose von Sa Clastra, das Gold der Castell Bar, der Sandstein der Fassade. Dazu Roberts Handschrift: Knöpfe mit Tiefe, Kacheln ohne Rahmen, Tapete Ton in Ton, Bewegung von unten.</p>
  <div class="kn-reihe" data-a style="--i:3"><a class="kn" href="probe.html" target="_blank"><span>Die Probe ansehen</span>{KNOPF_PFEIL}</a><a class="kn" href="logo-richtig-falsch/index.html" target="_blank"><span>Logo richtig und falsch</span>{KNOPF_PFEIL}</a></div>
</div></section>

<section class="fl fl--papier blatt"><div class="in">
  {kopf('Zeichen und Wortmarke', 'Drei Türme, eine Rosette, <em>eine Windrose.</em>', 'Die Wortmarke und das Zeichen liegen als Vektor auf der heutigen Seite (logo-dark.svg, logo-white.svg, sygnet.svg) und werden nie nachgezeichnet. Die Rosette steht heute hinter dem Einstiegstext (ornament.svg, 7 % Deckkraft). Die Windrose ist mit potrace aus der Karte «Rosa de los vientos» von Sa Clastra gezeichnet, das Mosaik aus der Karte der Castell Bar.')}
  <ul class="zeichen">
    <li class="wmk" style="color:{F['Logo-Grau']}"><svg viewBox="0 0 194.49 66.291"><use href="#wortmarke"/></svg><b>Wortmarke</b><small>logo-dark.svg · Original des Hauses</small></li>
    <li style="color:{F['Logo-Grau']}"><svg viewBox="0 0 36.485 19.394"><use href="#tuerme"/></svg><b>Die drei Türme</b><small>sygnet.svg · das Castell als Zeichen</small></li>
    <li style="color:{F['Ornament-Grau']}"><svg viewBox="0 0 592 590.711"><use href="#rosette"/></svg><b>Die Rosette</b><small>ornament.svg · heute 7 % hinter dem Text, neu als Tapete</small></li>
    <li style="color:{F['Nacht']}"><svg viewBox="{ROSE_VB}"><use href="#windrose"/></svg><b>Die Windrose</b><small>Sa Clastra · acht Winde, aus dem PDF vektorisiert</small></li>
    <li style="color:{F['Mosaik-Gold']}"><svg viewBox="{MOS_VB}"><use href="#mosaik"/></svg><b>Das Mosaik</b><small>Castell Bar · die Türme in Gold, aus der Karte 2025</small></li>
  </ul>
</div></section>

<section class="fl fl--creme blatt"><div class="in">
  {kopf('Farben', 'Gemessen, nicht <em>nachempfunden.</em>', 'Jede Farbe mit ihrer Fundstelle: Logo, heutige Seite, Drucksachen, Hausfotos. Die Bougainvillea bleibt im Foto, nie in der Gestaltung.')}
  <ul class="farben">{farbkarten}</ul>
</div></section>

<section class="fl fl--nacht blatt"><div class="in">
  {kopf('Zwei Farbwelten', 'Eine Entscheidung: <em>Nacht oder Hain.</em>', 'Beide Welten teilen Kalk, Sandstein und das Gold der Bar. Sie unterscheiden sich nur dort, wo die Seite dunkel wird und womit Titel betont werden. Welt A nimmt das Blau aus der Windrose von Sa Clastra, Welt B das Dunkel der Olivenhaine. Robert wählt.')}
  <ul class="welten">{welten}</ul>
</div></section>

<section class="fl fl--papier blatt"><div class="in">
  {kopf('Schriften', 'Die Schriften, die das Haus <em>schon hat.</em>', 'Fahkwang und Montserrat laden heute auf jeder der 302 Seiten. Beide sind frei (SIL Open Font License) und liegen als Dateien im Paket, damit nichts von fremden Servern kommt. Dazu DM Mono für Etiketten und Knöpfe, Roberts Handschrift.')}
  <ul class="schriften">{schriften}</ul>
  <p class="ort" style="margin-top:40px">Nicht übernommen</p><ul class="liste" style="margin-top:12px;max-width:80ch">{schrift_nicht}</ul>
  <p class="klein" style="margin-top:18px;max-width:80ch"><b>Die Schrift der Wortmarke selbst ist nicht belegt.</b> Sie wird deshalb nie neu gesetzt; die Unterzeile «MALLORCA» entspricht Montserrat in gesperrten Versalien, daraus kommen Ortszeile und Kapitelzeilen.</p>
</div></section>

<section class="fl fl--nacht blatt"><div class="in">
  {kopf('Tapete', 'Die Rosette, <em>Ton in Ton.</em>', 'Ein Gitter aus der Rosette des Hauses, zart (hell 8,5 %, dunkel 7,5 %), auf ruhigen hellen und dunklen Flächen. Kein freies Motiv, kein Papierkorn, kein Damast.')}
  <ul class="tap">
    <li style="background:{F['Kalk']} url(zeichen/tapete-hell.svg) 50% 0;color:{F['Logo-Grau']}"><span>tapete-hell.svg · Kalk mit Ornament-Grau</span></li>
    <li style="background:{F['Nacht']} url(zeichen/tapete-dunkel.svg) 50% 0;color:{F['Kalk']}"><span>tapete-dunkel.svg · Nacht (Welt A)</span></li>
    <li style="background:{F['Oliv-Nacht']} url(zeichen/tapete-dunkel-b.svg) 50% 0;color:{F['Kalk']}"><span>tapete-dunkel-b.svg · Oliv-Nacht (Welt B)</span></li>
  </ul>
</div></section>

<section class="fl fl--creme blatt"><div class="in">
  {kopf('Logo richtig und falsch', 'Eingesetzt, <em>nie verändert.</em>', 'Mindestgrösse, Schutzraum, Untergründe und sieben Dinge, die nicht gehen. Als eigene Seite mit allen Karten: <a href="logo-richtig-falsch/index.html" target="_blank" style="text-decoration:underline">logo-richtig-falsch</a>.')}
  <div class="bilder"><figure class="fen"><img src="../bilder/logo-richtig.jpg" alt="Logo richtig" loading="lazy"></figure><figure class="fen"><img src="../bilder/logo-falsch.jpg" alt="Logo falsch" loading="lazy"></figure></div>
</div></section>

<section class="fl fl--papier blatt"><div class="in">
  {kopf('Ton', 'Leise, erzählend, <em>aus dem Ort.</em>', 'Drei Sätze zum Charakter aus fakten.json und befund.md, die Worte, die das Haus selbst benutzt, und die, die wir nicht benutzen.')}
  {ton}
</div></section>

<section class="fl fl--nacht blatt"><div class="in">
  {kopf('Die eigene Welt', 'Projekt Nummer 10: <em>was nur dieses Haus ist.</em>')}
  <div class="kopf">{welt_saetze}</div>
  <p class="ort">Womit es sich von jedem bisherigen Haus unterscheidet</p>
  <ul class="unter" style="margin-top:14px">{unterschiede}</ul>
</div></section>

<section class="fl fl--creme blatt"><div class="in">
  {kopf('Die Probe', 'Ein Abschnitt der künftigen Seite, <em>Kunde plus Handschrift.</em>', 'Titelschrift, Farbwelt, Knopf mit Tiefe, Tapete, ein echtes Foto. Oben das Anwesen (hell), darunter Sa Clastra mit der Windrose (dunkel). Beide Farbwelten zum Umschalten.')}
  <div class="bilder"><figure class="fen"><img src="../bilder/probe-a-rechner.jpg" alt="Probe A am Rechner" loading="lazy"><figcaption class="mono" style="padding:10px 14px;color:#6b6a68">A · Rechner 1440 × 900</figcaption></figure><figure class="fen"><img src="../bilder/probe-b-rechner.jpg" alt="Probe B am Rechner" loading="lazy"><figcaption class="mono" style="padding:10px 14px;color:#6b6a68">B · Rechner 1440 × 900</figcaption></figure></div>
  <div class="handys"><figure class="fen"><img src="../bilder/probe-a-handy.jpg" alt="Probe A am Handy" loading="lazy"><figcaption class="mono" style="padding:10px 14px;color:#6b6a68">A · Handy 390 × 844</figcaption></figure><figure class="fen"><img src="../bilder/probe-b-handy.jpg" alt="Probe B am Handy" loading="lazy"><figcaption class="mono" style="padding:10px 14px;color:#6b6a68">B · Handy 390 × 844</figcaption></figure></div>
  <p style="margin-top:26px"><a class="kn" href="probe.html" target="_blank"><span>Probe lebendig öffnen</span>{KNOPF_PFEIL}</a></p>
</div></section>

<section class="fl fl--nacht blatt"><div class="in">
  {kopf('Dateien', 'Alles liegt <em>im Paket.</em>', 'marke/ im Ordner der Station 05. Originale unter logo/, Zeichen als SVG unter zeichen/, Schriften unter schriften/.')}
  <ul class="dateien">{''.join(f'<li>{e(p)}</li>' for p in dateiliste())}</ul>
</div></section>
<script>
var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{en.target.classList.add('da');io.unobserve(en.target)}}}})}},{{rootMargin:'0px 0px -10% 0px'}});
document.querySelectorAll('section').forEach(function(s){{io.observe(s)}});
</script></body></html>"""
    open(os.path.join(M, 'markenbuch.html'), 'w', encoding='utf-8').write(s)

def dateiliste():
    aus = []
    for d in ('logo', 'zeichen', 'schriften', 'bilder', 'logo-richtig-falsch'):
        p = os.path.join(M, d)
        if os.path.isdir(p):
            aus += [f'marke/{d}/{n}' for n in sorted(os.listdir(p)) if not n.startswith('.')]
    aus += ['marke/farben.svg', 'marke/farben.css', 'marke/farben.json', 'marke/probe.html', 'marke/markenbuch.html']
    return aus

# ---------------------------------------------------------------- marke.json
def marke_json():
    d = dict(
        haus='Castell Son Claret', ort='Es Capdellà, Mallorca', stand='2026-10-15',
        farben=[dict(name=n, hex=hx, rolle=rolle, belegt=bel, fundstelle=fund) for n, hx, rolle, bel, fund in FARBEN],
        farbwelten=[dict(k=k, name=w['name'], satz=w['satz'], flaechen=[F[x] for x in w['flaechen']], akzent=F[w['akzent']], betonung=F[w['betonung']], knopf=F[w['knopf']], css=w['css']) for k, w in WELTEN.items()],
        schriften=[dict(rolle=s['rolle'], name=s['name'], schnitt=s['schnitt'], datei=s['datei'], quelle=s['quelle'], lizenz=s['lizenz'], belegt=s['belegt']) for s in SCHRIFTEN],
        schriften_nicht=[dict(name=a, wo=b, warum=c) for a, b, c in SCHRIFT_NICHT],
        wortmarke=dict(datei='marke/logo/logo-dark.svg', art='svg', weitere=['marke/logo/logo-white.svg', 'marke/logo/logo.svg', 'marke/logo/logo_castell-524px.png'],
                       zeichen_allein='marke/logo/sygnet.svg', abgeleitete_titelschrift='Fahkwang 400 (Titelschrift der heutigen Seite); die Schrift der Wortmarke selbst ist nicht belegt, die Unterzeile entspricht Montserrat Versalien gesperrt',
                       herkunft='https://www.castellsonclaret.com/templates/castellsonclaret/images/ (15.10.2026)'),
        zeichen=[f'marke/zeichen/{n}' for n in sorted(os.listdir(os.path.join(M, 'zeichen')))],
        tapete=dict(hell='marke/zeichen/tapete-hell.svg', dunkel='marke/zeichen/tapete-dunkel.svg', dunkel_b='marke/zeichen/tapete-dunkel-b.svg', motiv='Rosette (ornament.svg) im Gitter mit Rauten-Linien', deckkraft={'hell': 0.085, 'dunkel': 0.075}),
        ton=TON, welt='grand', eigene_welt=EIGENE_WELT, familie_machart=None,
        familie=dict(name='The Fontenay, Hamburg', stand='noch nicht gebaut; beide Häuser bilden später eine Designwelt und bleiben zwei Seiten (Master 2.1)'),
        probe=dict(datei='marke/probe.html', abschnitte=['Das Anwesen (hell, Tapete, 3D-Kachel mit Einkerbung, Knopf)', 'Sa Clastra, Wind und Erinnerung (Nacht, Windrose in Gold, acht Winde)'],
                   eigene_saetze_von_mir=['Ein Landgut am Fuß des Galatzó.', 'Jeder Gang des Menüs trägt den Namen eines Windes.']),
        markenbuch='marke/markenbuch.html', logo_regeln='marke/logo-richtig-falsch/index.html')
    json.dump(d, open(os.path.join(H, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    zeichen(); tapete(); farben_svg(); probe(); logo_regeln(); markenbuch(); marke_json()
    print('gebaut:', M)
