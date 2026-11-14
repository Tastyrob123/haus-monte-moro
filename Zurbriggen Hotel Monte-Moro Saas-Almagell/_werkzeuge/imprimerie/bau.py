#!/usr/bin/env python3
"""Drucksachen & Feed · Hotel Monte-Moro, Saas-Almagell: legt die Marke des Hauses für die Druckerei an (nichts abgetippt, alles aus dem Projekt gelesen).
   python3 bau.py   → haeuser/montemoro/ (marke.json, schriften, tapete, bilder, mini, kopf, mail, motive.json, druck, druck.json) + api/_daten/montemoro.json
Quellen (nur gelesen):
  Hauswerte   website/inhalt/daten.py (HAUS, ROESTI_SATZ …), als Daten gelesen (ast), nie abgetippt.
  Farben      _kette/05-markenbauer/marke/farben.json (Nacht, Nachtblau, Tiefnacht, Logo-Blau, Lärche, Lärche tief, Messing, Papier, Fassade, Creme, Tinte, Grau)
              und kleid/montemoro.css. Lärche ist der Akzent, Messing nur feine Linie, Papier auf Nacht.
  Schriften   wie die Website (website/assets/fonts): Fjalla One (Titel, eine Stärke, nie fett, nie kursiv, normale Schreibung), Instrument Sans 400/500
              (Lauf, betont über Stärke), DM Mono 400 (kleine Zeilen, Etiketten, Zahlen, in Versalien gesperrt). Für das PDF als feste TrueType-Schnitte
              (Instrument Sans aus der variablen Datei als Instanz 400 und 500 gerechnet), damit nichts als Type 3 eingebettet wird.
  Zeichen     der Bergkamm aus dem Logo (_werkzeuge/oberflaeche/kleid/montemoro-zeichen.svg), die ganze Wortmarke «Monte Moro / Saas-Almagell»
              (montemoro-marke.svg), beide unverändert nachgezogen; die Grat-Kante der Website (montemoro.css --grat-maske) als drittes Zeichen.
  Fotos       website/assets/img/<schlüssel>-<s|m|l|x>.webp mit Beschreibung aus BILDER in website/inhalt/bilder.py (als Daten gelesen). Nicht übernommen:
              die anderen Häuser der Familie (f-*, fam-* ausser dem Monte-Moro), die Massage aus dem Partnerhaus, das gerechnete Nebelmeer (wolkenmeer-ki)."""
import ast, glob, json, os, re
import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJ, 'website')
IMG = os.path.join(WEB, 'assets', 'img')
Z = os.path.join(HIER, 'haeuser', 'montemoro')
KLEID = os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid')

ROLLEN = ['Eigene Fotos', 'Das Haus', 'Zimmer', 'Frühstück & Speisesaal', 'Röstihüs & Stübli', 'Saastal im Sommer', 'Saastal im Winter', 'Spa nebenan',
          'Ferienwohnungen', 'Das Dorf']

# Nicht in den Drucksachen des Monte-Moro: die anderen Häuser der Familie (eigene Häuser, nur Verweis), Bild aus dem Partnerhaus, gerechnetes Nebelmeer
RAUS = re.compile(r'^(f-|fam-(?!montemoro)|spa-massage$|wolkenmeer-ki$|wolkenmeer-echt$)')


def gruppe(k):
    if re.match(r'^(haus-|fam-montemoro|empfang|rezeption|gondel|balkon|spielburg)', k):
        return 'Das Haus'
    if re.match(r'^(z-|zimmer-)', k):
        return 'Zimmer'
    if re.match(r'^(fr-|fruehstueck|speise)', k):
        return 'Frühstück & Speisesaal'
    if re.match(r'^(roesti-|stube|stuebli|bar$|saecke|raclette)', k):
        return 'Röstihüs & Stübli'
    if re.match(r'^(spa-)', k):
        return 'Spa nebenan'
    if re.match(r'^(apollo|arizona)', k):
        return 'Ferienwohnungen'
    if re.match(r'^(dorf-|tal-dorf)', k):
        return 'Das Dorf'
    if re.match(r'^(huette|skitour|winterweg|winterbach|gletscher|metro|drehrestaurant|kinder-rodel|rodel|wolkenmeer)', k):
        return 'Saastal im Winter'
    return 'Saastal im Sommer'


# Kopf der Ansichten (buehne.js / oberflaeche.js): je Ansicht ein Raum des Hauses
KOPF = ['haus-sommer', 'roesti-raum', 'fr-tisch', 'z-licht', 'tal-sommer', 'stuebli', 'balkon', 'empfang', 'haus-winter-g', 'alpenrosen', 'dorf-nacht',
        'spa-wasser', 'gondel', 'mattmark', 'roesti-abend', 'z-sessel', 'dorf-weiss']
ERSATZ = 'haus-sommer'
# Druckfassungen (grösste Stufe der Website, 2200 px) für A4/A3 und die Druckprüfung (satz.js liest druck.json)
DRUCK = ['roesti-abend', 'spa-wasser', 'empfang', 'spielburg', 'murmeli', 'z-sessel', 'speisesaal', 'apollo-haus', 'raclette', 'haus-sommer', 'haus-sommer-g', 'haus-winter-g', 'tal-sommer', 'alpenrosen', 'mattmark', 'stausee', 'dorf-nacht', 'dorf-weiss', 'roesti-raum', 'roesti-stube',
         'stuebli', 'fr-tisch', 'z-licht', 'balkon', 'gondel', 'gletscher', 'see-blumen', 'bergbach', 'huette', 'spa-wasser']
# Bergbilder für das Grat-Plakat (motive.json, Ansicht «Bergbilder»): Landschaft und Haus, je mit einem Wort zum Thema
MOTIVE = [('tal-sommer', 'Das Saastal im Sommer', 'Sommer'), ('alpenrosen', 'Alpenrosen über dem Saastal', 'Sommer'), ('mattmark', 'Ein Bergsee über dem Saastal', 'Sommer'),
          ('stausee', 'Der Stausee Mattmark', 'Ausflug'), ('see-blumen', 'Blumen am Mattmarksee', 'Sommer'), ('bergbach', 'Ein Bergbach zwischen den Felsen', 'Sommer'),
          ('wasserfall', 'Ein Wasserfall im Saastal', 'Sommer'), ('gletscher', 'Über den Gletschern des Saastals', 'Winter'), ('huette', 'Eine Hütte im Schnee', 'Winter'),
          ('dorf-weiss', 'Das Dorf im Schnee', 'Winter'), ('dorf-nacht', 'Saas-Almagell am Abend', 'Dorf'), ('haus-sommer-g', 'Das Hotel mit der Sonnenterrasse', 'Haus'),
          ('haus-winter-g', 'Das Hotel im Winter', 'Haus'), ('gondel', 'Die Gondeln vor dem Röstihüs', 'Röstihüs'), ('wolkenmeer', 'Sonne über dem Nebelmeer', 'Ausflug')]

# Grat-Kante der Website (montemoro.css --grat-maske, viewBox 1000 × 60): das Bild ist unter der Linie sichtbar; als Zeichen die Fläche ÜBER der Linie
GRAT = [(0, 38), (70, 30), (118, 6), (150, 26), (196, 14), (250, 40), (300, 22), (338, 34), (380, 8), (430, 36), (486, 18), (540, 42), (600, 28), (640, 36), (700, 12),
        (748, 32), (800, 24), (860, 44), (920, 20), (962, 34), (1000, 26)]


def daten():
    """website/inhalt/daten.py als Daten lesen (nur Zuweisungen von Konstanten)."""
    env = {}
    for n in ast.parse(open(os.path.join(WEB, 'inhalt', 'daten.py'), encoding='utf-8').read()).body:
        if isinstance(n, ast.Assign):
            try:
                exec(compile(ast.Module([n], []), 'daten.py', 'exec'), {}, env)
            except Exception:
                pass
    return env


def bilder_register():
    src = open(os.path.join(WEB, 'inhalt', 'bilder.py'), encoding='utf-8').read()
    env = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'BILDER':
            exec(compile(ast.Module([n], []), 'bilder.py', 'exec'), {}, env)
    return env['BILDER']


def potrace_pfade(svg):
    """potrace-SVG (transform translate/scale, Befehle m M c l z, relativ) → absolute Pfade (y nach unten)."""
    tr = re.search(r'translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+),([-\d.]+)\)', svg)
    tx, ty, sx, sy = (float(x) for x in tr.groups()) if tr else (0, 0, 1, 1)
    alle = []
    for d in re.findall(r'\sd="([^"]+)"', svg):
        tok = re.findall(r'[MmCcLlZz]|-?\d*\.?\d+', d)
        i, cmd, x, y, sx0, sy0, teile = 0, None, 0.0, 0.0, 0.0, 0.0, []
        while i < len(tok):
            t = tok[i]
            if re.match(r'[A-Za-z]', t):
                cmd = t; i += 1
                if cmd in 'Zz':
                    teile.append(('Z',)); x, y = sx0, sy0
                continue
            n = {'M': 2, 'm': 2, 'L': 2, 'l': 2, 'C': 6, 'c': 6}[cmd]
            v = [float(q) for q in tok[i:i + n]]; i += n
            rel = cmd.islower()
            if cmd in 'Mm':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); sx0, sy0 = x, y
                teile.append(('M', x, y)); cmd = 'l' if rel else 'L'
            elif cmd in 'Ll':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); teile.append(('L', x, y))
            else:
                q = [(x + v[k], y + v[k + 1]) if rel else (v[k], v[k + 1]) for k in (0, 2, 4)]
                teile.append(('C', *q[0], *q[1], *q[2])); x, y = q[2]
        neu = []
        for t in teile:
            if t[0] == 'Z':
                neu.append(t); continue
            q = []
            for k in range(1, len(t), 2):
                q += [tx + sx * t[k], ty + sy * t[k + 1]]
            neu.append((t[0], *q))
        alle.append(neu)
    return alle


def zeichen_aus(teile_liste, hoehe=140, box=None):
    pts = [(t[k], t[k + 1]) for p in teile_liste for t in p if t[0] != 'Z' for k in range(1, len(t), 2)]
    x0, y0, x1, y1 = box or (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    k = hoehe / (y1 - y0)
    f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')
    aus = []
    for p in teile_liste:
        s = []
        for t in p:
            if t[0] == 'Z':
                s.append('Z'); continue
            s.append(t[0] + ' '.join(f((t[j] - x0) * k) if j % 2 == 1 else f((t[j] - y0) * k) for j in range(1, len(t))))
        aus.append(''.join(s))
    return aus, [0, 0, round((x1 - x0) * k, 2), hoehe]


def schriften(S):
    """Die drei Schriften der Website als feste TrueType-Schnitte (PDF) und als lateinische woff2-Teilmenge (Bildschirm)."""
    from fontTools.ttLib import TTFont
    from fontTools import subset
    from fontTools.varLib import instancer
    os.makedirs(S, exist_ok=True)
    for f in glob.glob(os.path.join(S, '*')):
        os.remove(f)
    Q = os.path.join(WEB, 'assets', 'fonts')
    def ttf(quelle, ziel, wght=None):
        f = TTFont(os.path.join(Q, quelle))
        if wght is not None and 'fvar' in f:
            f = instancer.instantiateVariableFont(f, {'wght': wght}, updateFontNames=False)
        f.flavor = None
        f.save(os.path.join(S, ziel))
    ttf('FjallaOne-400.woff2', 'FjallaOne-400.ttf')
    ttf('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-400.ttf', 400)
    ttf('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-500.ttf', 500)
    ttf('DMMono-normal-400.woff2', 'DMMono-400.ttf')
    lic = os.path.join(Q, 'OFL-FjallaOne.txt')
    if os.path.exists(lic):
        open(os.path.join(S, 'OFL-FjallaOne.txt'), 'w', encoding='utf-8').write(open(lic, encoding='utf-8').read())
    U = list(range(0x20, 0x7f)) + list(range(0xa0, 0x250)) + list(range(0x2000, 0x2070)) + [0x20ac, 0x2122, 0x2190, 0x2192, 0x2212]
    for f in sorted(glob.glob(os.path.join(S, '*.ttf'))):
        o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True; o.legacy_kern = True
        ft = TTFont(f); u = subset.Subsetter(o); u.populate(unicodes=U); u.subset(ft); ft.flavor = 'woff2'; ft.save(f[:-4] + '.woff2')


def tapete(ziel, farbe, deck, groesse=448):
    """Feines Raster als Tapete (Haarlinie in Messing oder Tinte), Rapport 24 mm, WebP mit Alpha (nur Bildschirm der Werkstatt)."""
    im = Image.new('RGBA', (groesse, groesse), (0, 0, 0, 0))
    px = im.load(); r, g, b = (int(farbe[i:i + 2], 16) for i in (1, 3, 5)); a = int(255 * deck)
    for i in range(groesse):
        for j in (0, groesse // 2):
            px[i, j] = (r, g, b, a); px[j, i] = (r, g, b, a)
    im.save(ziel, 'WEBP', lossless=True)


def stufe(key, gross=False):
    """Pfad der grössten Stufe ≤ 1440 px (gross: die grösste überhaupt) eines Fotos der Website."""
    for s in (('x', 'l', 'm', 's') if gross else ('l', 'm', 's')):
        p = os.path.join(IMG, '%s-%s.webp' % (key, s))
        if os.path.exists(p):
            return p
    return None


def druckfassungen():
    D = os.path.join(Z, 'druck'); os.makedirs(D, exist_ok=True)
    for f in os.listdir(D):
        os.remove(os.path.join(D, f))
    aus = {}
    for k in DRUCK:
        q = stufe(k, True)
        if not q:
            continue
        im = ImageOps.exif_transpose(Image.open(q)).convert('RGB')
        if max(im.size) <= 1600:
            continue
        im.save(os.path.join(D, k + '.jpg'), 'JPEG', quality=86); aus[k] = list(im.size)
    json.dump(aus, open(os.path.join(Z, 'druck.json'), 'w'))
    return aus


def main():
    for u in ('schriften', 'bilder', 'mini', 'kopf', 'mail'):
        os.makedirs(os.path.join(Z, u), exist_ok=True)
    H = daten()
    HAUS = H['HAUS']
    farbe = {f['name']: f['hex'] for f in json.load(open(os.path.join(PROJ, '_kette', '05-markenbauer', 'marke', 'farben.json'), encoding='utf-8'))}
    # Rollen der Farben wie im Stamm (navy = dunkle Fläche, weiss = hellste Fläche, tanne = Titel auf Hell, taupe = Etikett auf Hell, kander = Akzent)
    F = dict(navy=farbe['Nacht'], nacht=farbe.get('Tiefnacht', '#071B2E'), blau=farbe['Logo-Blau'], tinte=farbe.get('Tinte', '#13263A'), papier=farbe.get('Creme', '#EFE9E1'),
             creme=farbe['Fassade'], weiss=farbe['Papier'], gold=farbe.get('Messing', '#B39867'), taupe=farbe['Lärche tief'], messing=farbe.get('Messing', '#B39867'),
             tanne=farbe['Nacht'], kander=farbe['Lärche'], laden=farbe['Nachtblau'], rot=farbe['Lärche'], logo=farbe['Logo-Blau'], leise=farbe.get('Grau', '#4A5D70'),
             akzent=farbe['Lärche'])
    F = {k: v.upper() for k, v in F.items()}
    N = dict(navy='Nacht', nacht='Tiefnacht', blau='Logo-Blau', tinte='Tinte', papier='Creme', creme='Fassade', weiss='Papier', gold='Messing', taupe='Lärche tief',
             messing='Messing', tanne='Nacht', kander='Lärche', laden='Nachtblau', rot='Lärche', logo='Logo-Blau', leise='Grau', akzent='Lärche')

    zeichen, vb = zeichen_aus(potrace_pfade(open(os.path.join(KLEID, 'montemoro-zeichen.svg'), encoding='utf-8').read()))
    wm_svg = open(os.path.join(KLEID, 'montemoro-marke.svg'), encoding='utf-8').read()
    wm, vb2 = zeichen_aus(potrace_pfade(wm_svg))
    oben = 'M0 0L1000 0' + ''.join('L%d %d' % (x, y) for x, y in reversed(GRAT)) + 'Z'
    grat = dict(vb=[0, 0, 1000, 60], pfade=[oben], verh=60 / 1000, name='Die Grat-Kante der Website (Fläche über dem Bergkamm, liegt in der Grundfarbe auf der Oberkante eines Fotos)')

    S = os.path.join(Z, 'schriften')
    schriften(S)
    SCHRIFTEN = {
        'titel': ('Fjalla One', 'FjallaOne-400.ttf', 'Titel wie die Website: Fjalla One, eine Stärke, nie fett, nie kursiv, normal geschrieben'),
        'kapitale': ('DM Mono', 'DMMono-400.ttf', 'Kleine Zeilen in Versalien, gesperrt (Name des Hauses auf Rückseiten, Zeile über der Karte)'),
        'text': ('Instrument Sans', 'InstrumentSans-400.ttf', 'Lesetext wie die Website'),
        'kursiv': ('Instrument Sans 500', 'InstrumentSans-500.ttf', 'Betont (das Haus setzt nie kursiv, Betonung über die Stärke)'),
        'mono': ('DM Mono', 'DMMono-400.ttf', 'Etiketten, Zahlen, Preise, Daten und Zeiten: DM Mono in Versalien gesperrt, Ziffern gleich breit'),
    }

    tapete(os.path.join(Z, 'tapete-dunkel.webp'), F['gold'], .10)
    tapete(os.path.join(Z, 'tapete-hell.webp'), F['tinte'], .06)
    tapete(os.path.join(Z, 'tapete-ui-dunkel.webp'), F['gold'], .06)
    tapete(os.path.join(Z, 'tapete-ui-hell.webp'), F['tinte'], .04)
    t = Image.open(os.path.join(Z, 'tapete-dunkel.webp')).convert('RGBA'); g = Image.new('RGBA', t.size, F['navy']); g.alpha_composite(t)
    g.convert('RGB').save(os.path.join(Z, 'mail', '_tapete.jpg'), 'JPEG', quality=86)

    B = bilder_register()
    bilder, gesehen = [], {}
    for key, (q, alt) in B.items():
        if RAUS.match(key):
            continue
        p = stufe(key)
        if not p:
            continue
        if q in gesehen and key not in KOPF and key not in DRUCK:   # dieselbe Datei unter zwei Schlüsseln: nur einmal
            continue
        gesehen[q] = key
        im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
        if max(im.size) > 1600:
            im.thumbnail((1600, 1600), Image.LANCZOS)
        w, h = im.size
        im.save(os.path.join(Z, 'bilder', key + '.webp'), 'WEBP', quality=84, method=5)
        k = im.copy(); k.thumbnail((520, 520), Image.LANCZOS); k.save(os.path.join(Z, 'mini', key + '.webp'), 'WEBP', quality=74, method=5)
        k = im.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'mail', key + '.jpg'), 'JPEG', quality=76, optimize=True, progressive=True)
        if key in KOPF:
            k = im.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '.webp'), 'WEBP', quality=78, method=5)
            k = im.copy(); k.thumbnail((800, 800), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '-800.webp'), 'WEBP', quality=76, method=5)
        bilder.append(dict(key=key, alt=alt, w=w, h=h, gruppe=gruppe(key), quelle='website/assets/img'))

    da = {b['key'] for b in bilder}
    for u, end in (('bilder', '.webp'), ('mini', '.webp'), ('mail', '.jpg')):
        for f in os.listdir(os.path.join(Z, u)):
            if f.endswith(end) and not f.startswith('_') and f[:-len(end)] not in da:
                os.remove(os.path.join(Z, u, f))
    for f in os.listdir(os.path.join(Z, 'kopf')):
        if re.sub(r'(-800)?\.webp$', '', f) not in KOPF:
            os.remove(os.path.join(Z, 'kopf', f))
    bilder.sort(key=lambda b: (ROLLEN.index(b['gruppe']), b['key']))
    idx = {b['key']: b for b in bilder}
    motive = [dict(key=k, titel=t, quelle='foto', schrift=False, schlagworte=dict(thema=th, ort='Saastal'), akzent=F['kander'], kopf_frei=True,
                   kopf_farbe=F['weiss'], rueck_farbe=F['navy'], ganz=None, kopf_box=None, ganz_kopf_box=None) for k, t, th in MOTIVE if k in idx]
    json.dump(motive, open(os.path.join(Z, 'motive.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    druckfassungen()

    marke = dict(
        key='montemoro', name='Monte-Moro', voll=HAUS['name'], ort=HAUS['ort'], artikel='das',
        zeile=HAUS['satz'],
        satz=H['ROESTI_SATZ'],
        adr='%s · %s' % (HAUS['name'], HAUS['plz_ort']), tel=HAUS['tel'], mail=HAUS['mail'], web='www.monte-moro.ch',
        gastgeber='Esther und Fabian Zurbriggen',
        farben=F, farbnamen=N,
        toene=dict(
            dunkel=dict(grund='navy', tapete=None, titel='weiss', text='papier', mono='kander', linie='gold', zeichen='weiss', schild='weiss', schild_text='navy'),
            hell=dict(grund='weiss', tapete=None, titel='tanne', text='tinte', mono='taupe', linie='gold', zeichen='logo', schild='navy', schild_text='weiss'),
            creme=dict(grund='papier', tapete=None, titel='tanne', text='tinte', mono='taupe', linie='gold', zeichen='logo', schild='navy', schild_text='weiss'),
            blau=dict(grund='laden', tapete=None, titel='weiss', text='papier', mono='kander', linie='gold', zeichen='weiss', schild='weiss', schild_text='navy'),
        ),
        schriften={k: dict(familie=f, datei=d, wofuer=w) for k, (f, d, w) in SCHRIFTEN.items()},
        tapete=dict(dunkel='tapete-dunkel.webp', hell='tapete-hell.webp', rapport_mm=24),
        zeichen=dict(vb=vb, pfade=zeichen, verh=vb[3] / vb[2], name='Der Bergkamm aus dem Logo des Hauses (nachgezogen)'),
        zeichen2=dict(vb=vb2, pfade=wm, verh=vb2[3] / vb2[2], name='Die Wortmarke «Monte Moro / Saas-Almagell» (das ganze Logo, nachgezogen)',
                      farben=dict(grund=F['weiss'], zeichen=F['logo'], text=F['tinte'], hell=F['weiss'])),
        zeichen3=grat,
        abende=[],
        betriebe=[(HAUS['name'], 'Hotel mit Restaurant Röstihüs in Saas-Almagell, Gastgeber Esther und Fabian Zurbriggen'),
                  ('Restaurant Röstihüs', 'das Restaurant im Haus: elf Röstis, fünf Cordon bleus, Racletteabend im Stübli'),
                  ('Wellness & Spa Pirmin Zurbriggen', 'Partnerhotel nebenan, dessen Spa die Gäste nutzen (nur als Verweis)')],
        regeln=['Anrede «Sie», Schweizer Schreibung (ss statt ß, «Guillemets»). Jeder Satz wertet auf: Sorgfalt, der einzelne Gast, Familie, Berg; nie Masse, nie Ausrufezeichen im Titel.',
                'Titel in Fjalla One, normal geschrieben, nie fett, nie kursiv. Lauf in Instrument Sans. Kleine Zeilen, Preise und Zeiten in DM Mono, Versalien, gesperrt.',
                'Lärche nur als Akzent, Messing nur als feine Linie, Papier auf Nacht. Bergkamm und Wortmarke nur in Logo-Blau oder Papier, nie als Schrift nachgebaut.',
                'Preise, Zeiten und Angebote nur, wie die Website sie nennt (Preisliste, Inklusive, Röstihüs-Karte vom 18.11.2024, Spa-Tarife). Was das Haus nicht veröffentlicht (Öffnungszeiten des Röstihüs, Strasse, Storno), steht nirgends.',
                'Die Gratis-Anreise mit dem öffentlichen Verkehr galt bis 31.10.2026 und wird nicht mehr angeboten.'],
        bilder=bilder, raus=[], ersatz=ERSATZ, doppelt={},
    )
    json.dump(marke, open(os.path.join(Z, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    api = dict(marke)
    api['bilder'] = ['%s | %s | %s' % (b['key'], 'quer' if b['w'] > b['h'] * 1.1 else 'hoch' if b['h'] > b['w'] * 1.1 else 'quadrat', b['alt']) for b in bilder]
    for k in ('zeichen', 'zeichen2', 'zeichen3'):
        api.pop(k, None)
    os.makedirs(os.path.join(HIER, 'api', '_daten'), exist_ok=True)
    json.dump(api, open(os.path.join(HIER, 'api', '_daten', 'montemoro.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # Wissen des Hauses für die Entwürfe: website/assets/js/wissen.json (vom Website-Bau aus daten.py erzeugt), als Text
    W = json.load(open(os.path.join(WEB, 'assets', 'js', 'wissen.json'), encoding='utf-8'))
    z = ['%s, %s · %s' % (HAUS['name'], HAUS['ort'], W.get('stand', '')), 'Telefon %s · E-Mail %s' % (W['telefon'], W['mail']), '']
    for e in W['eintraege']:
        z += ['[%s] %s' % (e['k'], e['q']), e['a'], '']
    open(os.path.join(HIER, 'api', '_daten', 'montemoro-wissen.txt'), 'w', encoding='utf-8').write('\n'.join(z))
    print('Marke:', len(bilder), 'Fotos,', len(motive), 'Bergbilder,', len(os.listdir(os.path.join(Z, 'druck'))), 'Druckfassungen')


if __name__ == '__main__':
    main()
