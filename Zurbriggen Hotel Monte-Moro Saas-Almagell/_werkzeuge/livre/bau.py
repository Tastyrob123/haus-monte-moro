#!/usr/bin/env python3
"""Das Markenbuch · Hotel Monte-Moro, Saas-Almagell: baut die Marke des Hauses zum Arbeiten aus der Website und dem Markenbuch der Station 05.
Aufbau aus dem Stamm (Markenbuch der Werkzeuge, von Robert abgenommen), Inhalt und Kleid des Hauses (08.11.2026).
Die Website wird nie angefasst und nie importiert: gelesen werden BILDER in website/inhalt/bilder.py (register.py, per ast), die Masse und Quellen
website/assets/img/_masse.json, website/assets/css/montemoro.css (Farben), website/assets/fonts/, das Markenbuch _kette/05-markenbauer/marke/
(farben.json mit Fundstellen, zeichen/, logo/) und, nur beim Bau, _quelle/ (Herkunft, Originale, KI-Vorlagen). Zur Laufzeit lädt nichts aus _quelle/.
Geschrieben wird nur in diesen Ordner.

   python3 _werkzeuge/livre/bau.py   → livre.json, dateien/, original/, _quellen.json (nur lokal), listen/, beispiel/, index.html

Farben = die Werte der Website heute (montemoro.css :root); jede wird dort gesucht, der Bau bricht ab, wenn eine fehlt. Fundstellen aus farben.json.
Herkunft je Foto aus dem Pfad der Quelle (_masse.json) und den herkunft.json im Material: vom Haus (Website des Hauses, Schweiz Tourismus aus der
Datenbank von HotellerieSuisse, Booking.com und Tripadvisor vom Haus hochgeladen), mit KI neu gerechnet (24.10.2026, nach dem Foto des Hauses, mit Vorher),
frei lizenziert (Wikimedia Commons, mit Fotograf und Lizenz), fremde Rechte (Portale)."""
import base64, hashlib, html, io, json, os, re, shutil, struct, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))              # …/Zurbriggen Hotel Monte-Moro Saas-Almagell
ROOT = os.path.join(PROJEKT, 'website')                        # die Website, nur gelesen; ausgeliefert unter / (server.py)
PROJEKTE = os.path.dirname(PROJEKT)
QUELLE = os.path.join(PROJEKT, '_quelle')
BILDER = os.path.join(ROOT, 'assets', 'img')
MASSE = os.path.join(BILDER, '_masse.json')
CSS = os.path.join(ROOT, 'assets', 'css', 'montemoro.css')
FONTS = os.path.join(ROOT, 'assets', 'fonts')
MARKE = os.path.join(PROJEKT, '_kette', '05-markenbauer', 'marke')
ZEICHEN = os.path.join(MARKE, 'zeichen')
DAT = os.path.join(HIER, 'dateien')
ORIG = os.path.join(HIER, 'original')
e = html.escape
HAUS = 'Hotel Monte-Moro'
ORT = 'Saas-Almagell'
STAND = time.strftime('%d.%m.%Y')
SCHLUESSEL = 'monte-moro'
KLEID = os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche', 'kleid', 'montemoro.js')
sys.path.insert(0, HIER)
import register  # noqa: E402


def namen_aus_kleid():
    """Sichtbare Namen der Werkzeuge: eine Stelle für alle, WO_HAUS.namen im gemeinsamen Kleid. Fehlt das Kleid, bricht der Bau ab (kein fester Name)."""
    m = re.search(r'namen:\s*\{([^}]*)\}', open(KLEID, encoding='utf-8').read())
    if not m:
        raise SystemExit('WO_HAUS.namen fehlt im Kleid, erst klären')
    return dict(re.findall(r"(\w+):\s*['\"]([^'\"]+)['\"]", m.group(1)))


NAMEN = namen_aus_kleid()
NAME = NAMEN['marke']


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- Farben: so wie montemoro.css sie trägt (Markenbuch, Farbwelt A, von Robert am 18.10.2026 gewählt)
# (Schlüssel, Name, Variable der Website, Rolle, Gruppe); Wert und Fundstelle kommen aus montemoro.css und farben.json
FARBEN = [
    ('papier', 'Papier', 'papier', 'Grundfläche, auf der gelesen wird', 'hell'),
    ('fassade', 'Fassade', 'fassade', 'zweite helle Fläche, Karten und Blätter', 'hell'),
    ('creme', 'Creme', 'creme', 'helle Fläche zwischen Papier und Fassade', 'hell'),
    ('wandschatten', 'Wandschatten', 'wandschatten', 'Kanten, Unterseite der Knöpfe', 'hell'),
    ('nacht', 'Nacht', 'nacht', 'dunkle Fläche am Abend, Lesetext auf Hell', 'blau'),
    ('nachtblau', 'Nachtblau', 'nachtblau', 'Platten auf dunklem Grund', 'blau'),
    ('tiefnacht', 'Tiefnacht', 'tiefnacht', 'tiefste dunkle Fläche, Fuss der Seite', 'blau'),
    ('blau', 'Logo-Blau', 'blau', 'das Blau der Wortmarke, Zeichen auf Hell', 'blau'),
    ('laerche', 'Lärche', 'laerche', 'Akzent, Hauptknopf, das letzte Wort im Titel', 'laerche'),
    ('laerche-tief', 'Lärche tief', 'laerche-tief', 'Betonung und kleine Zeilen auf Hell', 'laerche'),
    ('messing', 'Messing', 'messing', 'nur feine Linien', 'laerche'),
    ('tinte', 'Tinte', 'tinte', 'Lesetext auf Papier', 'schrift'),
    ('grau', 'Grau', 'grau', 'leise Zeilen, Bildunterschriften', 'schrift'),
]
GRUPPEN = [('hell', 'Papier und Fassade', 'Hell ist der Normalzustand: so hell wie die Fassade des Hauses in der Sonne. Papier trägt den Lesetext, Fassade und Creme die Blätter und Karten.'),
           ('blau', 'Das Blau', 'Aus der Wortmarke des Hauses. Logo-Blau ist das Zeichen auf Hell, Nacht die dunkle Fläche am Abend und die Farbe des Lesetextes.'),
           ('laerche', 'Lärche und Messing', 'Das Holz der Balkone in der Sonne. Lärche zeichnet und betont, schreibt nie den Lesetext; Messing steht nur als feine Linie.'),
           ('schrift', 'Schrift', 'Geschrieben wird in Tinte auf Papier, leise Zeilen in Grau. Nie reines Schwarz, nie reines Weiss.')]
# je Gruppe ein eigenes Foto (Fehlerbuch 10a: ein Foto je Gruppe, nie wiederholt; Farbfeld ganz). Wege von der Seite des Werkzeugs aus.
GRUPPE_BILD = {'hell': ('haus-sommer', 'Die Fassade im Sommer, fotografiert für Schweiz Tourismus: daraus kommen Papier, Fassade und Wandschatten.'),
               'blau': ('empfang', 'Der Bergkamm an der Wand beim Empfang. Das Blau kommt aus der Logo-Datei des Hauses.'),
               'laerche': ('haus-sommer-g', 'Die Balkone aus Lärche in der Sonne: daraus kommen Lärche und Lärche tief.'),
               'schrift': None}   # kein eigenes Foto: Tinte und Grau stehen in jedem Text der Website


def css_werte():
    s = open(CSS, encoding='utf-8').read()
    root = re.search(r':root\{([^}]*)\}', s).group(1)
    return {k: v.upper() for k, v in re.findall(r'--([a-z-]+):(#[0-9A-Fa-f]{6})', root)}


def farben_liste():
    werte = css_werte()
    fund = {f['name']: f for f in json.load(open(os.path.join(MARKE, 'farben.json'), encoding='utf-8'))}
    aus = []
    for k, n, var, r, g in FARBEN:
        if var not in werte:
            raise SystemExit(f'Farbe {n} (--{var}) steht nicht in montemoro.css, erst klären')
        h = werte[var]
        f = fund.get(n)
        if f and f['hex'].upper() != h:
            raise SystemExit(f'Farbe {n}: Website {h}, Markenbuch {f["hex"]}, erst klären')
        woher = f'Wert der Website (montemoro.css); Markenbuch: {f["fundstelle"]}' if f else 'Wert der Website (montemoro.css)'
        aus.append((k, n, h, r, g, woher))
    return aus


# ---------------------------------------------------------------- Bildarchiv
REG = register.lesen()
MASS = json.load(open(MASSE, encoding='utf-8'))
BEREICHE = ['haus', 'zimmer', 'wohnungen', 'roestihues', 'kinder', 'spa', 'saastal']
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
STUFEN = ['s', 'm', 'l', 'x']


def benutzt():
    """Schlüssel, die die Website wirklich zeigt (Seiten und Stile), dazu die beiden Fotos, aus denen das Markenbuch die Farben misst."""
    s = ''
    for d, _, fs in os.walk(ROOT):
        if '_werkbank' in d or '/_' in d.replace(ROOT, ''):
            continue
        for f in fs:
            if f.endswith(('.html', '.css')):
                s += open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
    return set(re.findall(r'assets/img/([a-z0-9-]+?)-[smlx]\.webp', s)) | {'haus-sommer', 'haus-winter'}


def bereich(k):
    if k.startswith(('z-', 'zimmer-')):
        return 'zimmer'
    if k.startswith(('apollo', 'arizona')):
        return 'wohnungen'
    if k.startswith(('roesti-', 'stube', 'speise', 'fr-')) or k in ('stuebli', 'raclette', 'bar', 'saecke', 'fruehstueck'):
        return 'roestihues'
    if k in ('murmeli', 'kinder-rodel', 'rodel', 'spielburg'):
        return 'kinder'
    if k.startswith('spa-'):
        return 'spa'
    if k.startswith(('haus-', 'f-montemoro', 'fam-montemoro')) or k in ('empfang', 'rezeption', 'balkon', 'gondel'):
        return 'haus'
    return 'saastal'


def datum(s):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', s or '')
    return f'{int(m.group(3))}. {MONATE[int(m.group(2)) - 1]} {m.group(1)}' if m else ''


def hk(rel):
    """Eintrag aus der herkunft.json im Ordner der Quelle (oder darüber); rel relativ zu _quelle/."""
    p = os.path.join(QUELLE, rel); d = os.path.dirname(p)
    while d.startswith(QUELLE):
        f = os.path.join(d, 'herkunft.json')
        if os.path.exists(f):
            try:
                j = json.load(open(f, encoding='utf-8'))
            except ValueError:
                j = {}
            for key in (rel, os.path.relpath(p, d), os.path.basename(p)):
                if isinstance(j, dict) and isinstance(j.get(key), dict):
                    return j[key]
        d = os.path.dirname(d)
    return {}


KI_PLAN = {x['key']: x for x in json.load(open(os.path.join(QUELLE, 'ki-2026-10-24', 'ki-plan.json'), encoding='utf-8'))} if os.path.isdir(QUELLE) else {}


def quelle_rel(roh):
    """Weg aus _masse.json (relativ zur Website) → relativ zu _quelle/ oder None (Material ausserhalb des Hauses)."""
    p = os.path.normpath(os.path.join(ROOT, roh))
    return os.path.relpath(p, QUELLE) if p.startswith(QUELLE + os.sep) else None


def herkunft_von(rel):
    """(art, Quelle als Satz, Adresse) für eine Quelle relativ zu _quelle/."""
    h = hk(rel)
    if rel.startswith('extern/myswitzerland/'):
        return 'haus', 'Schweiz Tourismus (MySwitzerland), aus der Datenbank von HotellerieSuisse, vom Haus geliefert', h.get('seite', '')
    if rel.startswith('website/bilder/'):
        seite = {'sommer': ' (Seite Sommer)', 'winter': ' (Seite Winter)', 'ausflu': ' (Seite Ausflüge)', 'restau': ' (Seite Restaurant)', 'zimmer': ' (Seite Zimmer)',
                 'wellne': ' (Seite Wellness)', 'apollo': ' (Haus Apollo)', 'arizon': ' (Haus Arizona)'}.get(os.path.basename(rel)[:6], '')
        return 'haus', f'Heutige Website des Hauses (monte-moro.ch){seite}; Fotograf nicht genannt', ''
    if rel.startswith('extern/booking/'):
        return 'haus', 'Booking.com, vom Haus hochgeladen', h.get('seite', '')
    if rel.startswith('bearbeitet/') and 'booking-' in rel:
        return 'haus', 'Booking.com, vom Haus hochgeladen, aufgehellt', ''
    if rel.startswith('extern/tripadvisor/vom-hotel/'):
        return 'haus', f'Tripadvisor, vom Haus hochgeladen am {datum(h.get("hochgeladen", ""))}'.rstrip(' am'), h.get('seite', '')
    if rel.startswith('schlussbild-echt'):
        return 'frei', 'Foto: Christoph Strässler, «Valais under a sea of fog», Wikimedia Commons, Lizenz CC BY-SA 2.0 (Namensnennung, gleiche Lizenz)', 'https://commons.wikimedia.org/wiki/File:Valais_under_a_sea_of_fog.jpg'
    return 'haus', 'Aus dem Material des Hauses', ''


def herkunft(k, roh):
    """(art, Satz, Adresse, Vorlage relativ zu _quelle/ oder None) für den Schlüssel k mit der Quelle roh aus _masse.json."""
    rel = quelle_rel(roh)
    if rel is None:
        if 'Familie Zurbriggen' in roh and 'monte' in k:               # nur das Bild dieses Hauses aus dem Familienband; die anderen Häuser gehören nicht hierher
            return 'haus', 'Aus dem Bildbestand der Familie Zurbriggen (Familienband der Website)', '', None
        return None
    if rel.startswith('ki-2026-10-24/'):
        plan = KI_PLAN.get(k) or {}
        vor = quelle_rel(plan.get('datei', '')) if plan.get('datei') else None
        if not vor:
            return 'ki', 'Mit KI neu gerechnet (24. Oktober 2026)', '', None
        art, satz, u, _ = (*herkunft_von(vor), None)
        return 'ki', f'Mit KI neu gerechnet (24. Oktober 2026) nach einem Foto des Hauses. Vorlage: {satz}', u, vor
    return (*herkunft_von(rel), None)


def saison(k, alt, vorlage):
    s = f'{k} {alt} {vorlage or ""}'.lower()
    if re.search(r'winter|schnee|verschneit|ski|snowboard|fellen|gletscher|hütte', s):
        return 'winter'
    if re.search(r'sommer|alpenrosen|blumen|arnika|murmel|wasserfall|bergbach|stausee|mattmark|see\b', s):
        return 'sommer'
    return 'jahr'


def signatur(pfad):
    im = Image.open(pfad).convert('L').resize((17, 16), Image.LANCZOS)
    a = np.asarray(im, np.int16)
    return (a[:, 1:] > a[:, :-1]).flatten()


def stufen(k):
    """[(breite, datei)] der Website für den Schlüssel, nach Breite; doppelte Breiten (Quelle kleiner als die Stufe) nur einmal."""
    aus, gesehen = [], set()
    for s in STUFEN:
        p = os.path.join(BILDER, f'{k}-{s}.webp')
        if os.path.exists(p):
            w = Image.open(p).size[0]
            if w not in gesehen:
                gesehen.add(w); aus.append((w, f'{k}-{s}.webp'))
    return sorted(aus)


def katalog():
    aus, quellen, zusammen, gesehen = [], {}, {}, {}
    nutzt = benutzt()
    # Quellen, die in einer neu gerechneten Fassung schon als Vorher stehen: das Original nicht noch einmal als eigenes Foto
    vorlagen = {}
    for k in REG:
        if k in nutzt and k in MASS:
            h = herkunft(k, MASS[k][2])
            if h and h[3]:
                vorlagen[h[3]] = k
    for k, (q, alt) in REG.items():
        if k not in nutzt or k not in MASS:
            continue
        w, h_, roh = MASS[k]
        hh = herkunft(k, roh)
        if hh is None or (k.startswith(('f-', 'fam-')) and 'monte' not in k):   # Material und Bilder der anderen Häuser: gehören nicht in dieses Markenbuch
            print('anderes Haus, weggelassen:', k); continue
        art, satz, u, vor = hh
        rel = quelle_rel(roh)
        if rel and rel in vorlagen and vorlagen[rel] != k:
            zusammen[k] = vorlagen[rel]; continue
        if roh in gesehen:                                         # Fehlerbuch 10a: doppelte Einträge zusammenführen
            zusammen[k] = gesehen[roh]; continue
        gesehen[roh] = k
        st = stufen(k)
        if not st:
            print('nicht im Archiv:', k); continue
        gr = st[-1]; kl = st[0]; mi = max([s for s in st if s[0] <= 1500] or [kl])
        f = 'hoch' if h_ > w * 1.04 else 'quer' if w > h_ * 1.04 else 'quadrat'
        aus.append(dict(k=k, t={'de': re.sub(r'\s*\(Foto: [^)]*\)', '', alt)}, b=bereich(k), s=saison(k, alt, vor), f=f, w=w, h=h_, art=art, q=satz, u=u, ue=False, alt=False, vn=False,
                        fl=f'../../assets/img/{gr[1]}', fm=f'../../assets/img/{mi[1]}', fs=f'../../assets/img/{kl[1]}', sw=[[b, f'../../assets/img/{n}'] for b, n in st]))
        quellen[k] = dict(druck=os.path.join(QUELLE, rel) if rel else os.path.normpath(os.path.join(ROOT, roh)), ausschnitt=None,
                          original=os.path.join(QUELLE, vor) if vor else None)
    # gleiche Fotos unter verschiedenen Quellen (Bildvergleich, Abstand der Signaturen unter 0,08): ein Eintrag
    sigs = {d['k']: signatur(os.path.join(ROOT, d['fs'][6:])) for d in aus}
    weg = set()
    for i, a in enumerate(aus):
        for b in aus[i + 1:]:
            if b['k'] in weg or a['k'] in weg:
                continue
            if np.mean(sigs[a['k']] != sigs[b['k']]) < .08 and a['art'] == b['art'] and a['f'] == b['f']:
                bleibt, geht = (b, a) if b['w'] * b['h'] > a['w'] * a['h'] else (a, b)
                weg.add(geht['k']); zusammen[geht['k']] = bleibt['k']
    aus = [d for d in aus if d['k'] not in weg]
    for x in weg:
        quellen.pop(x, None)
    for x, z in list(zusammen.items()):                            # Ketten auflösen
        while z in zusammen:
            z = zusammen[z]
        zusammen[x] = z
    for v in quellen.values():
        for n in ('druck', 'original'):
            if v[n] and not os.path.exists(v[n]):
                v[n] = None
    return aus, quellen, zusammen


def originale(aus, quellen):
    """Das Foto des Hauses, aus dem die KI-Fassung gerechnet ist, auf die Grösse der Website gebracht (original/<k>.webp), gleicher Ausschnitt."""
    if os.path.isdir(ORIG):
        shutil.rmtree(ORIG)
    os.makedirs(ORIG)
    n = 0
    for d in aus:
        o = quellen[d['k']]['original']
        if not (d['art'] == 'ki' and o and os.path.exists(o)):
            continue
        mi = os.path.join(ROOT, d['fm'][6:])
        with Image.open(mi) as nach:
            groesse = nach.size
        im = ImageOps.exif_transpose(Image.open(o)).convert('RGB')
        w, h = im.size; z = groesse[0] / groesse[1]
        if abs(w / h - z) > .005:
            if w / h > z:
                nw = round(h * z); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = round(w / z); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize(groesse, Image.LANCZOS).save(os.path.join(ORIG, d['k'] + '.webp'), 'WEBP', quality=74, method=5)
        d['vn'] = True
        n += 1
    return n


# ---------------------------------------------------------------- Zeichnen mit Chromium (SVG → PNG, unsichtbar, ein Lauf, eigener Prozess)
def svg_png(paare):
    """paare: [(svg, png, breite)]; jedes SVG in der gewünschten Breite auf durchsichtigem Grund (SVG als data:-Adresse)."""
    js = os.path.join(HIER, '_svg_png.js')
    open(js, 'w').write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const [svg, png, w, h] of JSON.parse(process.argv[2])) {
    await p.setViewportSize({ width: w, height: h });
    const d = 'data:image/svg+xml;base64,' + require('fs').readFileSync(svg).toString('base64');
    await p.setContent(`<html><body style="margin:0;background:transparent"><img src="${d}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
    await p.waitForFunction(() => document.images[0].complete && document.images[0].naturalWidth > 0);
    await p.screenshot({ path: png, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }); }
  await b.close(); })();''')
    liste = []
    for svg, png, breite in paare:
        s = open(svg, encoding='utf-8').read()
        vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
        liste.append([svg, png, breite, round(breite * vb[3] / vb[2])])
    try:
        subprocess.run(['node', js, json.dumps(liste)], check=True, timeout=300, cwd=HIER)
    finally:
        os.remove(js)


def ase(farben):
    def block(name, r, g, b):
        n = (name + '\0').encode('utf-16-be')
        body = struct.pack('>H', len(name) + 1) + n + b'RGB ' + struct.pack('>fff', r / 255, g / 255, b / 255) + struct.pack('>H', 2)
        return struct.pack('>HI', 1, len(body)) + body
    bl = b''.join(block(n, *rgb(h)) for n, h in farben)
    return b'ASEF' + struct.pack('>HHI', 1, 0, len(farben)) + bl


SCHRIFTEN = [
    ('t', 'Fjalla One', 'FjallaOne-400.woff2', 'Titel', '400, eine Stärke; gross und klein, nie fett, nie kursiv', 'Mehr erleben, weniger zahlen.', 400),
    ('s', 'Instrument Sans', 'InstrumentSans-normal-400_600.woff2', 'Lesetext', '400, 17,5 px, Zeilenabstand 1,7', 'Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten.', 400),
    ('e', 'DM Mono', 'DMMono-normal-400.woff2', 'Kapitelzeilen und Knöpfe', '400, 11 px, Versalien, 0,16 bis 0,24 em gesperrt', 'Restaurant Röstihüs · Saas-Almagell', 400),
    ('z', 'DM Mono', 'DMMono-normal-400.woff2', 'Zeiten, Preise, Adressen', 'gleich breite Ziffern, Preise mit Punkt wie auf der Preisliste', 'Mo–Sa 16:30–21:00 · CHF 90.00', 400),
]

# Zeichen des Hauses aus dem Markenbuch (zeichen/<form>-<farbe>.svg): je Form die Farben, die das Markenbuch erlaubt (Farbwelt A)
FORMEN = [('wortmarke', 'Wortmarke', [('blau', 'hell'), ('nacht', 'hell'), ('papier', 'dunkel'), ('laerche', 'dunkel')], 1600),
          ('bergkamm', 'Bergkamm', [('blau', 'hell'), ('nacht', 'hell'), ('papier', 'dunkel'), ('laerche', 'dunkel')], 1600),
          ('medaillon', 'Medaillon', [('blau', 'hell'), ('laerche', 'hell'), ('papier', 'dunkel')], 1000)]


def dateien(fa):
    if os.path.isdir(DAT):
        shutil.rmtree(DAT)
    os.makedirs(DAT)
    F = {k: h for k, n, h, r, g, w in fa}
    liste, render = [], []
    for form, titel, farben, breite in FORMEN:
        var = []
        for farbe, grund in farben:
            quelle = os.path.join(ZEICHEN, f'{form}-{farbe}.svg')
            s = f'{SCHLUESSEL}-{form}-{farbe}.svg'; p = s[:-4] + '.png'
            inhalt = open(quelle, encoding='utf-8').read()
            inhalt = re.sub(r'<\?xml[^>]*\?>\s*', '', inhalt)
            if '<title>' not in inhalt:
                inhalt = re.sub(r'(<svg[^>]*>)', r'\1<title>Hotel Monte-Moro, Saas-Almagell</title>', inhalt, count=1)
            open(os.path.join(DAT, s), 'w', encoding='utf-8').write(inhalt)
            render.append((os.path.join(DAT, s), os.path.join(DAT, p), breite))
            var.append(dict(k=f'{form}-{farbe}', farbe=farbe, grund=grund, dateien=[s, p]))
        liste.append(dict(k=form, var=var))
    # Das Original: logo.png von der heutigen Seite des Hauses (1161 × 475), unverändert
    n = f'{SCHLUESSEL}-logo-original.png'
    shutil.copyfile(os.path.join(MARKE, 'logo', 'logo-original-1161px.png'), os.path.join(DAT, n))
    liste.append(dict(k='original', var=[dict(k='original', grund='hell', dateien=[n], px=list(Image.open(os.path.join(DAT, n)).size))]))
    # Tapete: das Medaillon im Rautengitter (Markenbuch, zeichen/tapete-hell.svg und tapete-dunkel.svg), auf Papier und auf Nacht
    var = []
    for k, grund in (('hell', 'hell'), ('dunkel', 'dunkel')):
        s = f'{SCHLUESSEL}-tapete-{k}.svg'; p = s[:-4] + '.png'; w = s[:-4] + '.webp'
        inhalt = re.sub(r'<\?xml[^>]*\?>\s*', '', open(os.path.join(ZEICHEN, f'tapete-{k}.svg'), encoding='utf-8').read())
        open(os.path.join(DAT, s), 'w', encoding='utf-8').write(inhalt)
        render.append((os.path.join(DAT, s), os.path.join(DAT, p), 960))
        var.append(dict(k=k, grund=grund, dateien=[p, s, w], farbe=F['papier'] if k == 'hell' else F['nacht']))
    liste.append(dict(k='tapete', var=var))
    svg_png(render)
    for g in liste:
        for v in g['var']:
            png = next((x for x in v['dateien'] if x.endswith('.png')), None)
            if png and 'px' not in v:
                v['px'] = list(Image.open(os.path.join(DAT, png)).size)
    for v in next(g for g in liste if g['k'] == 'tapete')['var']:
        Image.open(os.path.join(DAT, v['dateien'][0])).convert('RGB').save(os.path.join(DAT, v['dateien'][2]), 'WEBP', quality=90)
    # Farben als Datei: CSS, JSON und ASE
    css = ':root{\n' + ''.join(f'  --{k}:{h}; /* {n}: {r} */\n' for k, n, h, r, g, w in fa) + '}\n'
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.css'), 'w', encoding='utf-8').write(f'/* {HAUS}, {ORT} · Farben der Marke ({STAND}), Werte der Website */\n' + css)
    json.dump([dict(name=n, hex=h, rgb=list(rgb(h)), rolle=r, gruppe=g, woher=w) for k, n, h, r, g, w in fa], open(os.path.join(DAT, f'{SCHLUESSEL}-farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.ase'), 'wb').write(ase([(n, h) for k, n, h, r, g, w in fa]))
    liste.append(dict(k='farben', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-farben.css', f'{SCHLUESSEL}-farben.json', f'{SCHLUESSEL}-farben.ase'])]))
    # Schriften: die Dateien der Website, dazu als ZIP mit TTF und Lizenz (SIL Open Font License 1.1, Urheber aus der Schrift selbst)
    from fontTools.ttLib import TTFont
    ofl = open(os.path.join(HIER, '_ofl-vorlage.txt'), encoding='utf-8').read()
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-schriften.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for datei in sorted({s_[2] for s_ in SCHRIFTEN}):
            z.write(os.path.join(FONTS, datei), 'web/' + datei)
            f = TTFont(os.path.join(FONTS, datei)); recht = f['name'].getDebugName(0) or ''; fam = f['name'].getDebugName(1) or datei.split('-')[0]
            f.flavor = None
            b = io.BytesIO(); f.save(b); z.writestr('programme/' + datei.replace('.woff2', '.ttf'), b.getvalue())
            z.writestr('lizenz/OFL-' + fam.lower().replace(' ', '-') + '.txt', recht + '\n' + ofl)
        z.writestr('LIESMICH.txt', f'''{HAUS}, {ORT} · Schriften der Marke ({STAND})

Fjalla One 400: Titel. Eine Stärke, gross und klein geschrieben, nie fett, nie kursiv.
Instrument Sans 400: Lesetext, 17,5 px, Zeilenabstand 1,7.
DM Mono 400: Kapitelzeilen, Etiketten und Knöpfe in Versalien, 0,16 bis 0,24 em gesperrt;
             Zeiten, Preise und Adressen mit gleich breiten Ziffern.

Alle drei stehen unter der SIL Open Font License 1.1 (frei für Druck, Website und Programme, auch gewerblich; nicht als Schrift allein verkaufen).
web/        die Dateien der Website
programme/  dieselben Schriften als TTF zum Installieren
lizenz/     Lizenztexte
''')
    liste.append(dict(k='schriften', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-schriften.zip'])]))
    alle = sorted(n_ for n_ in os.listdir(DAT) if not n_.endswith('-marke.zip') and not n_.endswith('.webp'))   # erst die Liste, dann das ZIP
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-marke.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n_ in alle:
            z.write(os.path.join(DAT, n_), n_)
    return liste


# ---------------------------------------------------------------- Beispiel für die Markenprüfung
def _schrift(namen, gr):
    for n in namen:
        for d in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/truetype/liberation', '/usr/share/fonts/truetype', '/usr/share/fonts'):
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, gr)
    r = subprocess.run(['fc-match', '-f', '%{file}', namen[0].split('.')[0]], capture_output=True, text=True)
    return ImageFont.truetype(r.stdout, gr) if r.stdout and os.path.exists(r.stdout) else ImageFont.load_default(gr)


def beispiel(F, fotos):
    """Ein eigens gezeichneter Entwurf, wie ihn eine Agentur schicken könnte: ein Beitrag für den Winter mit einem Foto des Hauses und der Wortmarke,
    aber in einer fremden Schrift (eine Serifenschrift fett), mit Neon-Pink und reinem Schwarz statt Nacht, Papier und Lärche, im Du und mit «Luxus».
    Geprüft mit der Prüfung selbst ohne Claude (LIVRE_KI=0); die Farben bleiben gemessen, Schrift, Zeichen, Bild und Ton bekommen Beispiel-Urteile, beschriftet."""
    os.environ['LIVRE_KI'] = '0'
    import livre as LV
    LV._livre.cache_clear()
    zb = os.path.join(HIER, 'beispiel')
    if os.path.isdir(zb):
        shutil.rmtree(zb)
    os.makedirs(zb)
    W, H = 1080, 1350
    PINK, SCHWARZ = (0xFF, 0x2E, 0xB8), (0, 0, 0)
    im = Image.new('RGB', (W, H), SCHWARZ)
    foto = Image.open(os.path.join(ROOT, (fotos.get('haus-winter-g') or fotos['haus-winter-b'])['fl'][6:])).convert('RGB')
    sk = max(W / foto.width, 860 / foto.height); foto = foto.resize((round(foto.width * sk), round(foto.height * sk)), Image.LANCZOS)
    y0 = round((foto.height - 860) * .5)
    im.paste(foto.crop(((foto.width - W) // 2, y0, (foto.width - W) // 2 + W, y0 + 860)), (0, 0))
    dr = ImageDraw.Draw(im)
    titel = _schrift(['DejaVuSerif-Bold.ttf', 'LiberationSerif-Bold.ttf'], 54)
    lese = _schrift(['DejaVuSerif.ttf', 'LiberationSerif-Regular.ttf'], 32)
    knopf = _schrift(['DejaVuSans-Bold.ttf', 'LiberationSans-Bold.ttf'], 28)
    dr.text((72, 910), 'Luxus-Winter im Monte Moro!', font=titel, fill=(255, 255, 255))
    dr.text((72, 1022), 'Gönn dir eine Auszeit in den Bergen.', font=lese, fill=(225, 225, 225))
    dr.text((72, 1068), 'Saas-Almagell · Wallis', font=lese, fill=(225, 225, 225))
    dr.rectangle((72, 1170, 400, 1242), fill=PINK)
    dr.text((104, 1191), 'JETZT BUCHEN', font=knopf, fill=SCHWARZ)
    logo = Image.open(os.path.join(DAT, f'{SCHLUESSEL}-wortmarke-papier.png')).convert('RGBA'); logo.thumbnail((300, 130), Image.LANCZOS)
    dunkel = Image.new('RGBA', (W, 300), (0, 0, 0, 0)); dd = ImageDraw.Draw(dunkel)
    for i in range(300):
        dd.line((0, i, W, i), fill=(0, 0, 0, int(140 * (1 - i / 300))))
    im.paste(dunkel, (0, 0), dunkel); im.paste(logo, (W - logo.width - 64, 40), logo)
    im.save(os.path.join(zb, 'entwurf.png'), optimize=True)
    b = io.BytesIO(); im.save(b, 'PNG')
    j = LV.pruefen(dict(name='Beispiel-Entwurf «Luxus-Winter», Instagram-Beitrag', typ='image/png', daten='data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), sprache='de'))
    j['beispiel'] = True
    kk = j.setdefault('ki', {})
    farb = [x for x in kk.get('punkte', []) if x.get('bereich') == 'farben']
    for x in farb:
        x['text'] = x['text'].replace('Gemessen ohne KI: ', 'Gemessen: ')
    kk['punkte'] = farb + [
        dict(bereich='farben', urteil='passt_nicht', titel='Neon-Pink und reines Schwarz', text=f'Der Knopf trägt ein Neon-Pink, die Fläche reines Schwarz. Im Monte-Moro trägt Nacht {F["nacht"]} die dunklen Flächen, Papier {F["papier"]} die hellen; betont wird mit Lärche {F["laerche"]}.'),
        dict(bereich='schrift', urteil='passt_nicht', titel='Titel in einer fetten Serifenschrift', text='Der Titel steht fett in einer fremden Serifenschrift. Das Haus setzt Titel in Fjalla One, eine Stärke, gross und klein; Knöpfe und kleine Zeilen in DM Mono, Versalien, gesperrt.'),
        dict(bereich='zeichen', urteil='passt', titel='Die Wortmarke steht richtig', text='Die Wortmarke steht in Papier auf dem ruhigen, dunklen Himmel, unverzerrt, ganz und mit Luft rundherum.'),
        dict(bereich='bild', urteil='passt', titel='Das Haus im Winter', text='Ein Foto aus dem Bildarchiv: das Haus selbst, in echtem Licht. Genau das gehört nach vorn.'),
        dict(bereich='ton', urteil='passt_nicht', titel='Du statt Sie, «Luxus» statt der Rechnung', text='Das Haus siezt seine Gäste und macht sich nicht grösser, als es ist. «Luxus» und «JETZT BUCHEN» klingen nach Werbung; das Haus sagt ruhig, was der Gast bekommt.'),
    ]
    kk['gesamt'] = ('Ein guter Anfang: Foto und Wortmarke passen zum Monte-Moro. Schrift, Pink und Schwarz kommen nicht aus der Marke, und der Text spricht nicht wie das Haus; '
                    'mit Fjalla One, Nacht, Papier und einem Knopf in Lärche wird daraus ein Beitrag, der aussieht wie die Website.')
    kk['ton'] = [dict(stelle='Luxus-Winter im Monte Moro!', vorschlag='Winter im Monte-Moro.'),
                 dict(stelle='Gönn dir eine Auszeit in den Bergen.', vorschlag='Postautos im ganzen Saastal sind für Sie inbegriffen.'),
                 dict(stelle='JETZT BUCHEN', vorschlag='Zimmer anfragen')]
    j['probe'] = False
    json.dump(j, open(os.path.join(zb, 'pruefung.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return j


def listen_bilder():
    z = os.path.join(HIER, 'listen')
    if os.path.isdir(z):
        shutil.rmtree(z)
    os.makedirs(z)
    port = 9385
    seiten = [f'http://127.0.0.1:{port}/{n}' for n in ('index.html', 'roestihues.html', 'zimmer.html', 'preise.html')]
    r = subprocess.run(['node', os.path.join(HIER, 'listen_bilder.js'), z] + seiten, timeout=420, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        raise SystemExit('listen_bilder.js: ' + r.stderr[-600:])
    for n in os.listdir(z):
        im = Image.open(os.path.join(z, n)).convert('RGB'); im.thumbnail((1200, 800), Image.LANCZOS)
        im.save(os.path.join(z, n[:-4] + '.webp'), 'WEBP', quality=84, method=5); os.remove(os.path.join(z, n))


# Worte des Hauses (Markenbuch, Station 05 «Die eigene Welt»; die Gratis-Anreise ist am 31.10.2026 abgelaufen und steht hier nicht mehr)
TON = dict(eigene_worte=['Mehr erleben, weniger zahlen.', 'Es lebe die Tradition!', 'Bei uns scheint fast immer die Sonne.', 'Schöne Hotelzimmer – schöne Ferien',
                         'mit Liebe, Herz und den besten regionalen Produkten', 'gemütlich, herzlich eingerichtet', 'von Fabian selber kreiert'],
           nicht=['Du-Form', 'Luxus', 'exklusiv', 'Refugium', 'atemberaubend', 'einzigartig', 'unvergesslich', 'JETZT BUCHEN als Werbezeile'])


def main():
    t0 = time.time()
    fa = farben_liste()
    F = {k: h for k, n, h, r, g, w in fa}
    aus, quellen, zusammen = katalog()
    n_orig = originale(aus, quellen)
    liste = dateien(fa)
    groessen = {f: os.path.getsize(os.path.join(DAT, f)) for f in sorted(os.listdir(DAT))}
    daten = dict(haus=HAUS, ort=ORT, fotos=aus, dateien=liste,
                 farben=[dict(k=k, n=n, h=h.upper(), rgb=list(rgb(h)), r=r, g=g, woher=w) for k, n, h, r, g, w in fa],
                 gruppen=[dict(k=k, n=n, s=s) for k, n, s in GRUPPEN], glanz=[], groessen=groessen,
                 bereiche=[b for b in BEREICHE if any(f['b'] == b for f in aus)],
                 schriften=[dict(k=k, n=fam, d=d, r=r, e=ein, p=p, w=w) for k, fam, d, r, ein, p, w in SCHRIFTEN],
                 namen=NAMEN, zusammen=zusammen, ton=TON,
                 stand=dict(fotos=len(aus), haus=sum(1 for x in aus if x['art'] == 'haus'), frei=sum(1 for x in aus if x['art'] == 'frei'),
                            ki=sum(1 for x in aus if x['art'] == 'ki'), fremd=sum(1 for x in aus if x['art'] == 'fremd'), partner=0,
                            ue=sum(1 for x in aus if x['ue']), vn=n_orig, original=sum(1 for v in quellen.values() if v['druck']),
                            dateien=len([f for f in groessen if not f.endswith('.webp')]), datum=STAND))
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({k: dict(druck=v['druck'] and os.path.relpath(v['druck'], PROJEKTE), ausschnitt=v['ausschnitt'],
                       original=v['original'] and os.path.relpath(v['original'], PROJEKTE)) for k, v in quellen.items()},
              open(os.path.join(HIER, '_quellen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    fotos = {f['k']: f for f in aus}
    beispiel(F, fotos)
    if '--ohne-listen' not in sys.argv:
        listen_bilder()
    for g in daten['gruppen']:
        if not GRUPPE_BILD.get(g['k']):
            continue
        b, satz = GRUPPE_BILD[g['k']]
        g['bild'] = b if '/' in b else fotos[b]['fm']
        g['bild_t'] = satz
    for s_ in daten['schriften']:
        s_['bild'] = f'listen/schrift-{s_["k"]}.webp'
    for g in [g for g in daten['gruppen'] if g.get('bild')]:
        p = os.path.join(ROOT, g['bild'][6:]) if g['bild'].startswith('../../') else os.path.join(HIER, g['bild'])
        if not os.path.exists(p):
            print('Hinweis: Gruppenbild fehlt', g['bild']); g.pop('bild'); g.pop('bild_t')
    for s_ in daten['schriften']:
        if not os.path.exists(os.path.join(HIER, s_['bild'])):
            print('Hinweis: Schriftbild fehlt', s_['bild']); s_.pop('bild')
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    seite(F)
    st = daten['stand']
    print(f'livre.json: {len(aus)} Fotos ({st["haus"]} vom Haus, {st["ki"]} mit KI neu gerechnet, {st["frei"]} frei, {st["fremd"]} fremde Rechte, '
          f'{n_orig} mit Vorher, {st["original"]} mit Original) · {len(zusammen)} doppelte zusammengeführt · {st["dateien"]} Dateien · {time.time() - t0:.0f} s')


def v_von(*namen):
    h = hashlib.sha1()
    for n in namen:
        p = os.path.join(HIER, n)
        h.update(open(p, 'rb').read() if os.path.exists(p) else b'-')
    return h.hexdigest()[:10]


def seite(F):
    v = v_von('livre.json'); vc = v_von('livre.css'); vj = v_von('livre.js')
    open(os.path.join(HIER, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{NAME} · {HAUS}, {ORT}</title>
<meta name="description" content="{NAME}, die Marke des {HAUS} zum Arbeiten: Bildarchiv mit fertigen Grössen, Wortmarke, Bergkamm, Medaillon, Tapete und Farben als Dateien, Markenprüfung für Entwürfe, Hausregeln.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']}">
<link rel="icon" href="/assets/oberflaeche/kleid/montemoro-zeichen.svg" type="image/svg+xml">
<script src="/assets/oberflaeche/kleid/montemoro.js?v={v_von('../oberflaeche/kleid/montemoro.js')}"></script>
<link rel="preload" href="/assets/fonts/FjallaOne-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="livre.json?v={v}" as="fetch" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v={v_von('../oberflaeche/grund.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v={v_von('../oberflaeche/rahmen-buehne.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/montemoro.css?v={v_von('../oberflaeche/kleid/montemoro.css')}">
<link rel="stylesheet" href="livre.css?v={vc}">
</head>
<body class="li wo-app">
<header class="wo-kopf" id="kopf"></header>
<aside class="wo-rand" id="rand" aria-label="{NAME}"></aside>
<main class="wo-raum" id="haupt"><div id="ansicht"></div></main>
<footer class="wo-leiste" id="leiste" aria-live="polite"></footer>
<div class="fenster" id="fenster" hidden></div>
<div class="meldung" id="meldung" aria-live="polite"></div>
<noscript><p class="li-noscript">{NAME} braucht JavaScript.</p></noscript>
<script src="start.js?v={v_von('start.js')}" data-v="{vj}"></script>
<script src="/assets/oberflaeche/oberflaeche.js?v={v_von('../oberflaeche/oberflaeche.js')}"></script>
<script src="livre.js?v={vj}"></script>
</body>
</html>
''')


if __name__ == '__main__':
    if sys.argv[1:] == ['seite']:
        seite({k: h for k, n, h, r, g, w in farben_liste()})
    else:
        main()
