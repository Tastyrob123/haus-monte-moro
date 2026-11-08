#!/usr/bin/env python3
"""Station 04 · Analyst · Hotel Monte-Moro, Saas-Almagell: Potentialanalyse als Landingpage (17.10.2026).

Fassung 2 (17.10.2026 abends, Robert: für Laien, Schlimmstes zuerst, übersichtlicher, Blender-Geräte, eigener Aufbau je Haus; Master 1b Nr. 11 bis 14):
zwölf Punkte untereinander mit mitlaufender Liste, je Punkt Beispiel, Stelle, Idee, Gerät aus geraet.py. Fassung 1 liegt unter potential/fassung-1/,
ihr Bauskript als bau.py.vor-fassung-2.


Aufbau nach der Analyse des Castell Son Claret, Fassung 7 (Archiv `_Archiv/Castell Son Claret/_kette/04-analyst/bau2.py`, `_bau7/`):
kompakt, die Informationen vorn (Auftakt · Gruss mit Zahlen · Register mit «Was zuerst zählt» und den Bereichen), je Bereich ein Pult
mit Blättern, je Punkt echte Aufnahmen der Seite im Telefon, Quelltext-Schirme und PDF-Streifen mit rotem Kreis, «Was das für Sie bedeutet»,
«Was stimmt» und «Selbst beheben» als Blätter am Pult, ein Fenster, dazu der Teil «Wer hinter der heutigen Seite steht» (Robert 17.10.2026).
Inhalt: inhalt.py (einzige Wahrheit). Belege: stellen.js (Aufnahmen), code.py/code.js (Quelltext), pdf.py (Karte, AGB), beweise.py (Figuren).
Form: Werkbank-Kit (kern.gestaltung mit den Haken in potential/_werkbank/haus.py). Nur transform und opacity, nativer Scroll (Regel 55).

   python3 bau.py   → potential/index.html, potential/werkbank/*, potential/bilder/*, potential/beweise/*, potential/analyse.js
"""
import base64, html, io, json, os, re, shutil, sys

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(H), 'potential')
KIT = os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit')
Q = os.path.expanduser('~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle')
os.environ['HAUS'] = ROOT
sys.path.insert(0, KIT)
sys.argv = [sys.argv[0], ROOT]
import kern as K  # noqa: E402
sys.path.insert(0, H)
import inhalt as I  # noqa: E402
from kern import H as HAUS  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

e = html.escape
STAND = I.STAND
HEUTE = HAUS.HEUTE_URL
PF = K.PF
HAKEN = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.5"/></svg>'
ZU = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13"/></svg>'
HZ = K.HZ
V = 34  # Fassung der Dateien; bei jeder Änderung an CSS/JS/Bildern hochzählen

# ---------------------------------------------------------------- Fotos des Hauses (_quelle, Herkunft je Ordner in herkunft.json)
FOTOS = {
    'hero': ('extern/myswitzerland/myswitzerland-00072098_m.jpg', 'Das Hotel Monte-Moro im Sommer, mit den Balkonen aus Lärche'),
    'haus-winter': ('extern/myswitzerland/myswitzerland-00072097_m.jpg', 'Das Hotel Monte-Moro im Winter'),
    'ansicht': ('website/bilder/aktuel_hotel-monte-moro-saas-almagell-ansicht.jpg', 'Das Haus an der Dorfstrasse im Schnee'),
    'balkon': ('website/bilder/aktuel_hotel-monte-moro-saas-almagell-balkon.jpg', 'Blick vom Balkon ins Tal'),
    'dorf': ('website/bilder/stando_Saas_Almagell.jpg', 'Saas-Almagell am Abend'),
    'balkon-hell': ('website/bilder/aktuel_hotel-monte-moro-saas-almagell-balkon.jpg', 'Blick vom Balkon ins Tal'),
    'dorf-nacht': ('website/bilder/winter_1.jpg', 'Saas-Almagell im Winter'),
    'stube': ('website/bilder/restau_restaurant.jpg', 'Das Röstihüs'),
    'roestihues': ('website/bilder/restau_3.jpg', 'Das Schild des Röstihüs vor dem Haus'),
    'stube2': ('website/bilder/restau_5.jpg', 'Die Stube des Röstihüs'),
    'zimmer': ('website/bilder/zimmer_1.jpg', 'Ein Zimmer im Monte-Moro'),
    'zimmer2': ('extern/booking/booking-28199196.jpg', 'Doppelzimmer mit Balkon'),
    'apollo': ('website/bilder/apollo_1.jpg', 'Haus Apollo im Sommer und im Winter'),
    'wellness': ('website/bilder/wellne_wellness.jpg', 'Das Spa im Partnerhotel Pirmin Zurbriggen'),
    'fruehstueck': ('extern/booking/booking-133404915.jpg', 'Das Frühstücksbuffet am Morgen'),
    'gondel': ('extern/booking/booking-609882092.jpg', 'Die geschmückte Gondel am Haus'),
    'fassade-winter': ('extern/booking/booking-609882154.jpg', 'Das Haus nach frischem Schnee'),
    'robert': (os.path.join(ROOT, '_werkbank', 'robert.jpg'), 'Robert Reff'),
}
# Foto je Punkt (inhalt.py › foto) auf ein Foto oben
PFOTO = {'p-balkon': 'balkon', 'p-zimmer': 'zimmer', 'p-haus-winter': 'haus-winter', 'p-zimmer2': 'zimmer2', 'p-apollo': 'apollo', 'p-dorf': 'dorf',
         'p-stube': 'stube', 'p-winter': 'ansicht', 'p-haus': 'hero', 'p-roesti': 'roestihues', 'p-stube2': 'stube2', 'p-roesti2': 'stube',
         'p-wellness': 'wellness', 'p-roesti3': 'stube2', 'p-terrasse': 'fruehstueck', 'p-spa': 'wellness', 'p-dorf2': 'dorf', 'p-roesti4': 'roestihues',
         'p-haus2': 'haus-winter', 'p-haus3': 'ansicht', 'p-haus4': 'hero', 'p-fassade': 'fassade-winter'}
BEREICH_FOTO = {'hero': 'hero', 'zimmer': 'zimmer', 'balkon': 'balkon', 'roestihues': 'roestihues', 'wellness': 'wellness', 'haus': 'gondel',
                'dorf': 'dorf', 'dorf-nacht': 'dorf-nacht', 'fassade-winter': 'fassade-winter'}
DUNKEL = { 'balkon': (.34, .3), 'schluss': (.3, .4)}
BREITEN = [640, 1200, 1920]
BILD = {}


def quelle(datei):
    return datei if os.path.isabs(datei) else os.path.join(Q, datei)


def fotos_bauen():
    ziel = os.path.join(ROOT, 'bilder')
    os.makedirs(ziel, exist_ok=True)
    for key, (datei, _alt) in FOTOS.items():
        if key == 'robert':
            continue
        im = Image.open(quelle(datei)).convert('RGB')
        BILD[key] = []
        for b in BREITEN:
            bb = min(b, im.width)
            name = f'{key}-{bb}.webp'
            K.webp(im, os.path.join(ziel, name), bb, q=80 if b < 1900 else 76, dunkel=DUNKEL.get(key))
            BILD[key].append((bb, name))
            if b >= im.width:
                break
    shutil.copy2(FOTOS['robert'][0], os.path.join(ziel, 'robert.jpg'))
    # Schluss: Dorf am Abend mit Dunkel im Bild (nie etwas Durchscheinendes über Bewegtem)
    im = Image.open(quelle(FOTOS['dorf-nacht'][0])).convert('RGB')
    K.webp(im, os.path.join(ziel, 'schluss-1200.webp'), 1200, q=80, dunkel=DUNKEL['schluss'])
    BILD['schluss'] = [(1200, 'schluss-1200.webp')]


def tapeten():
    """Zartes Gitter mit Medaillon aus dem Zeichen (Bergkamm des Logos), 560 px, dunkel und hell (Rivage-Stand: Gitter, nie ein grosses freies Motiv)."""
    ziel = os.path.join(ROOT, 'bilder')
    z = Image.open(os.path.join(H, 'marke', 'zeichen.pbm')).convert('L')
    z = z.point(lambda v: 255 - v)                       # weiss = Zeichen
    for name, grund, linie, zeichen_f in (('tapete-dunkel', '#0B2A4C', (255, 255, 255, 9), (201, 138, 90, 22)),   # Ton in Ton (Robert 17.10.: zu unruhig)
                                         ('tapete-hell', '#F7F5F0', (11, 42, 76, 9), (168, 96, 60, 20))):
        S = 560 * 2
        im = Image.new('RGBA', (S, S), grund)
        ol = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(ol)   # eigene Ebene, damit die Deckkraft wirklich gilt
        for k in range(-S, 2 * S, S // 2):
            d.line([(k, 0), (k + S, S)], fill=linie, width=2)
            d.line([(k + S, 0), (k, S)], fill=linie, width=2)
        for cx, cy in ((S // 2, S // 2), (0, 0), (S, 0), (0, S), (S, S)):
            d.ellipse((cx - 118, cy - 118, cx + 118, cy + 118), outline=linie, width=2)
            m = z.resize((196, round(196 * z.height / z.width)), Image.LANCZOS)
            m = m.point(lambda v, a=zeichen_f[3]: round(v * a / 255))
            farbe = Image.new('RGBA', m.size, zeichen_f[:3] + (255,)); farbe.putalpha(m)
            ol.alpha_composite(farbe, (cx - m.width // 2, cy - m.height // 2 - 6))
        im.alpha_composite(ol)
        im = im.convert('RGB').resize((560, 560), Image.LANCZOS)
        im.save(os.path.join(ziel, name + '.webp'), 'WEBP', quality=90, method=6)


def bild(key, alt=None, sizes='100vw', klasse='', lazy=True, prio=False, stil=''):
    key = PFOTO.get(key, key)
    liste = BILD[key]
    alt = FOTOS[key][1] if alt is None else alt
    srcset = ', '.join(f'bilder/{n}?v={V} {b}w' for b, n in liste)
    src = f'bilder/{liste[-1][1]}?v={V}'
    vorab = K.VORAB.get(liste[0][1][:-5], '')
    st = f'background-image:url({vorab});' if vorab else ''
    return (f'<img class="ld{(" " + klasse) if klasse else ""}" src="{src}" srcset="{srcset}" sizes="{sizes}" alt="{e(alt)}" '
            f'loading="{"lazy" if lazy else "eager"}" decoding="async"{" fetchpriority=\"high\"" if prio else ""} style="{st}{stil}">')


# ---------------------------------------------------------------- Fassung 2 (Robert 17.10.2026): hell, für Laien, zwölf Punkte, Blender-Geräte
# Aufbau eigen für dieses Haus (Master 1b Nr. 14): kein Pult, keine Blätter. Auftakt hell mit gerahmtem Hausfoto, Gruss mit den zwölf Punkten,
# dann die Punkte untereinander mit einer mitlaufenden Liste am Rand, je Punkt ein Beispiel, ein Satz zur Seite, eine Idee und das Gerät.
GER = json.load(open(os.path.join(H, 'geraete.json')))


def fenster(fid, key, zeilen, klein, alt):
    liste = BILD[key]
    src = f'bilder/{liste[-1][1]}?v={V}'
    srcset = ', '.join(f'bilder/{n}?v={V} {b}w' for b, n in liste)
    return f'''<section class="wfen" id="{fid}" aria-label="{e(' '.join(zeilen))}">
  <div class="wfen__f">
    <img src="{src}" srcset="{srcset}" sizes="100vw" alt="{e(alt)}" loading="lazy" decoding="async">
    <div class="wfen__in">{hz("wfen__z")}<h2 class="wfen__t"><span>{e(zeilen[0])}</span><span><em>{e(zeilen[1])}</em></span></h2><p class="wfen__k">{e(klein)}</p></div>
  </div>
</section>'''



def kn(text, href, klasse='', neu=False):
    return f'<a class="kn {klasse}" href="{href}"{" target=\"_blank\" rel=\"noopener\"" if neu else ""}>{text}<i>{PF}</i></a>'


def hz(kl=''):
    return f'<svg class="{kl}" viewBox="{HAUS.ZEICHEN[0]}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'


def inline(t):
    return t if '<code>' in t else e(t, quote=False)


def kopf_mitte(wort, zeilen, lauf=None):
    l = f'<div class="lauf" data-a="auf">{lauf}</div>' if lauf else ''
    return f'<div class="kopfzeile kopfzeile--mitte"><p class="kap kap--z" data-a="auf">{hz("kap__z")}<span>{e(wort)}</span></p>{K.titel(zeilen)}{l}</div>'


def geraet(gid, satz, i=0):
    g = GER[gid]
    src = f'geraete/{gid}.webp?v={V}'
    knopf = kn('<span class="mm-lang">Auf Ihrer Seite </span>ansehen', e(g['url']), 'kn--klein kn--linie', neu=True) if g.get('url') else ''
    return (f'<figure class="mm-g mm-g--{g["typ"]}" data-a="feder" style="--i:{i}"><img src="{src}" width="{g["w"]}" height="{g["h"]}" alt="{e(satz)}" loading="lazy" decoding="async">'
            f'<figcaption><span>{e(satz)}</span>{knopf}</figcaption></figure>')


AUS = json.load(open(os.path.join(H, 'ausschnitte.json')))


def ausschnitt(zid, labels, haupt, i=0, links=False, lupe=False):
    """«Was genau» (Master 1b Nr. 15): die Stelle gross, feine Hinweislinien zu kurzen Beschriftungen. Breite Streifen: Beschriftungen darunter,
    sonst rechts daneben, auf Höhe ihres Ankers und ohne Überschneidung. Linien über zwei SVG in Prozent, ohne Skript."""
    if zid == 'z11':   # Reiter als echter Text (nachgezeichnete Leiste, Titel und Adresse wörtlich aus dem Quelltext): bricht um, bleibt am Handy lesbar
        lab = ''.join(f'<li class="{"mm-tab__h" if k == haupt else ""}">{e(t)}</li>' for k, t in enumerate(labels))
        return (f'<figure class="mm-z mm-tab{" mm-z--lupe" if lupe else ""}" data-a="feder" style="--i:{i}"><div class="mm-tab__b" role="img" aria-label="Reiter des Browsers mit dem Titel «Aktuelles | Hotel Monte Moro Saas-Almagell»">'
                f'<div class="mm-tab__k"><i></i><i></i><i></i></div><div class="mm-tab__t"><span class="mm-tab__e">Aktuelles</span> | <span class="mm-tab__n">Hotel Monte Moro Saas-Almagell</span></div>'
                f'<div class="mm-tab__a">monte-moro.ch/de/</div></div><ul class="mm-tab__l">{lab}</ul></figure>')
    z = AUS[zid]; w, h = z['w'], z['h']; an = z['anker']
    # Fassung 4 (Robert 17.10.2026: «so wie auf dem Telefon, in zwei Zeilen»): die Vergrösserung zeigt die Zeilen genau wie das Gerät. Grösse aus der Breite
    # im Gerät (vb): am Rechner 1,6-fach (Handy) bzw. 1,3-fach (Laptop), am Handy mindestens so gross, dass die Schrift Fliesstext erreicht (sonst seitlich wischen)
    if z.get('vb'):
        ref = 16 if z.get('desk') else 12.8
        dw = round(z['vb'] * (1.3 if z.get('desk') else 1.6)); mw = round(z['vb'] * 16.8 / ref)
    elif z.get('schrift_px'):   # Speisekarte: so breit, dass die Schrift der Karte 17 px erreicht
        dw, mw = round(17 * w / z['schrift_px']), 0
    else:
        dw, mw = 360, 0
    unten = dw > 400
    masse = f'--dw:{dw}px;--mw:{mw}px'
    breit = ' mm-z--breit' if z.get('vb', 0) * 16.8 / (16 if z.get('desk') else 12.8) > 340 else ''
    def _e(a):
        x0 = max(0.5, a[0] - 1.6); x1 = min(99.5, a[0] + a[2] + 1.6); y0 = max(0.5, a[1] - 2.5); y1 = min(99.5, a[1] + a[3] + 2.5)
        return f'left:{x0:.2f}%;top:{y0:.2f}%;width:{x1 - x0:.2f}%;height:{y1 - y0:.2f}%'
    an = [[max(0, a[0]), a[1], min(100 - max(0, a[0]), a[2]), a[3]] for a in an]
    # Textmarker statt Kreis (Robert 17.10.2026: Kreise überlappen und schneiden Buchstaben): je Zeile ein weicher Farbstreifen hinter der Stelle
    ellipsen = ''.join(f'<span class="mm-z__m{" mm-z__m--h" if k == haupt else ""}" style="left:{max(0, r[0] - .8):.2f}%;top:{r[1] - .4:.2f}%;width:{min(100 - max(0, r[0] - .8), r[2] + 1.6):.2f}%;height:{r[3] + .8:.2f}%"></span>'
                       for k, m in enumerate(z.get('marker') or [[a] for a in an]) for r in m)
    if unten:
        # Beschriftungen unter ihrer Stelle (Mitte der ersten Zeile des Ankers), Abstand mindestens eine Beschriftungsbreite, nie über den Rand
        n = len(labels); mk = z.get('marker') or [[a] for a in an]
        cx = [min(97, max(3, mk[k][0][0] + mk[k][0][2] / 2)) if mk[k] else an[k][0] + an[k][2] / 2 for k in range(n)]
        lw = min(31, 100 / n - 2, 210 / dw * 100); gap = lw + 2
        order = sorted(range(n), key=lambda k: cx[k]); pos = {}
        for r, k in enumerate(order): pos[k] = max(cx[k], lw / 2, (pos[order[r - 1]] + gap) if r else -1e9)
        über = pos[order[-1]] - (100 - lw / 2)
        if über > 0:
            for r in range(n - 1, -1, -1):
                k = order[r]; pos[k] = min(pos[k], (100 - lw / 2) if r == n - 1 else pos[order[r + 1]] - gap)
        l1 = ''
        l2 = ''.join(f'<polyline points="{cx[k]:.2f},0 {cx[k]:.2f},18 {pos[k]:.2f},40 {pos[k]:.2f},48"/>' for k in range(n))
        lab = ''.join(f'<span class="mm-z__t{" mm-z__t--h" if k == haupt else ""}" style="left:{pos[k]:.2f}%;width:{lw:.2f}%">{e(labels[k])}</span>' for k in range(n))
        return (f'<figure class="mm-z mm-z--unten{breit}{" mm-z--lupe" if lupe else ""}" data-a="feder" style="--i:{i};{masse}"><div class="mm-z__b"><div class="mm-z__in"><img src="ausschnitte/{zid}.webp?v={V}" width="{w}" height="{h}" alt="{e("; ".join(labels))}" loading="lazy" decoding="async">{ellipsen}'
                f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{l1}</svg></div></div>'
                f'<div class="mm-z__u"><svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{l2}</svg>{lab}</div></figure>')
    # rechts: Beschriftungen auf Höhe des Ankers, Abstand mindestens 46 px bei rund 300 px Bildbreite
    hd = dw * h / w; gap = 46 / hd * 100
    ys = [a[1] + a[3] / 2 for a in an]; order = sorted(range(len(ys)), key=lambda k: ys[k]); ly = {}
    letzt = -1e9
    for k in order:
        y = max(ys[k], letzt + gap); ly[k] = y; letzt = y
    über = letzt - 96
    if über > 0:
        for k in ly: ly[k] -= über
    lo = min(ly.values())
    if lo < 4:
        for k in ly: ly[k] += 4 - lo
    l1 = ''
    if links:   # Gerät rechts: Beschriftungen links vom Bild, damit der Lichtkegel frei zur Lupe läuft
        l2 = ''.join(f'<polyline points="100,{ys[k]} 70,{ys[k]} 48,{ly[k]} 0,{ly[k]}"/>' for k in range(len(an)))
    else:
        l2 = ''.join(f'<polyline points="0,{ys[k]} 30,{ys[k]} 52,{ly[k]} 100,{ly[k]}"/>' for k in range(len(an)))
    lab = ''.join(f'<span class="mm-z__t{" mm-z__t--h" if k == haupt else ""}" style="top:{ly[k]}%">{e(labels[k])}</span>' for k in sorted(range(len(an)), key=lambda k: ly[k]))
    return (f'<figure class="mm-z mm-z--{"links" if links else "rechts"}{breit}{" mm-z--lupe" if lupe else ""}" data-a="feder" style="--i:{i};{masse}"><div class="mm-z__b"><div class="mm-z__in"><img src="ausschnitte/{zid}.webp?v={V}" width="{w}" height="{h}" alt="{e("; ".join(labels))}" loading="lazy" decoding="async">{ellipsen}'
            f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{l1}</svg></div></div>'
            f'<div class="mm-z__r"><svg class="mm-z__s" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{l2}</svg>{lab}</div></figure>')


def wo(gid, weg):
    g = GER[gid]
    knopf = kn('<span class="mm-lang">Auf Ihrer Seite </span>ansehen', e(g['url']), 'kn--klein kn--linie', neu=True) if g.get('url') else ''
    return (f'<div class="mm-s mm-s--wo"><p class="mm-l">Wo</p><p class="mm-weg">{e(weg)}</p>'
            f'<figure class="mm-g mm-g--{g["typ"]}" data-a="feder"><img src="geraete/{gid}.webp?v={V}" width="{g["w"]}" height="{g["h"]}" alt="{e(weg)}" loading="lazy" decoding="async"'
            f'{" data-mark=" + chr(34) + ",".join(map(str, g["mark"])) + chr(34) if g.get("mark") else ""}><figcaption>{knopf}</figcaption></figure></div>')


PAUSEN = {2: (['roestihues', 'stube2', 'fruehstueck'], 'Es lebe die Tradition!', 'Röstihüs, monte-moro.ch'),
          5: (['balkon-hell', 'dorf', 'haus-winter'], 'Mehr erleben, weniger zahlen.', 'Startseite, monte-moro.ch'),
          8: (['zimmer2', 'apollo', 'gondel'], 'Schöne Hotelzimmer - schöne Ferien', 'Zimmer, monte-moro.ch')}


def pause(j):
    """Robert 17.10.2026: «zwischendurch mal so ein paar kleine Bilder, dass es atmosphärisch ist, ein bisschen Lust macht». Drei echte Fotos und ein Satz des Hauses."""
    if j not in PAUSEN: return ''
    fotos, satz, quelle = PAUSEN[j]
    f = ''.join(f'<figure class="mm-pause__f mm-pause__f--{i}" data-a="feder" style="--i:{i}">{bild(k, None, "(max-width:700px) 46vw, 300px")}<figcaption>{e(FOTOS[k][1])}</figcaption></figure>' for i, k in enumerate(fotos))
    return f'<section class="mm-pause"><div class="in"><div class="mm-pause__r">{f}</div><p class="mm-pause__s" data-a="auf">«{e(satz)}»<small>{e(quelle)}</small></p></div></section>'


LUPE = {'01': 1, '02': 1}   # welche Vergrösserung dieselbe Zeile zeigt wie die Stelle im Gerät (Lichtkegel)


def punkt(p, j):
    b = I.BEWEIS[p['nr']]
    art = b['art']; lap = I.BEWEIS[p['nr']]['wo'] in GER and GER[b['wo']]['typ'] == 'laptop'
    was = ''.join(ausschnitt(z, l, hh, i, links=(art == 'gr' and not lap), lupe=(i == LUPE.get(p['nr'], 0))) for i, (z, l, hh) in enumerate(b['zs']))
    if b.get('wortlaut'):   # was im Bild zu klein wäre, steht wörtlich daneben (Master 1b Nr. 15, «Lesbar oder raus»)
        was += f'<p class="mm-wl"><b>{e(b["wortlaut"][0])}</b>{e(b["wortlaut"][1])}</p>'
    weg = ''.join(f'<li>{e(x)}</li>' for x in b['warum'])
    links = ''.join(kn(e(t), e(u), 'kn--klein kn--linie', neu=True) for t, u in p['nachsehen'])
    genau = ''.join(f'<p>{inline(a)}</p>' for a in p['genau'])
    teil_wo = wo(b['wo'], b['weg'])
    teil_was = f'<div class="mm-s mm-s--was"><p class="mm-l">Was genau</p>{was}</div>'
    teil_warum = f'<div class="mm-s mm-s--warum" data-a="auf"><p class="mm-l">Warum es stört</p><ol class="mm-weg3">{weg}</ol></div>'
    teil_wirkt = (f'<div class="mm-s mm-s--wirkt" data-a="auf" style="--i:1"><p class="mm-l">Was es bewirkt</p>'
                  f'<p class="mm-w"><b>Für Ihre Gäste</b>{e(b["gast"])}</p><p class="mm-w"><b>Für Ihr Haus</b>{e(b["haus"])}</p>'
                  f'<div class="mm-tun"><p class="mm-l"><i>{HAKEN}</i>Was wir tun würden</p><p>{e(p["tun"])}</p></div>'
                  f'<details class="mm-genau"><summary>Genauer nachlesen<i aria-hidden="true"></i></summary><div>{genau}<div class="mm-genau__l">{links}</div></div></details></div>')
    oben = f'<div class="mm-p__o mm-p__o--{"lap" if lap else art}">{teil_wo}{teil_was}<svg class="mm-kegel" aria-hidden="true"></svg></div>'
    ton = 'dunkel' if j % 2 else 'hell'
    return f"""<section class="mm-blatt mm-blatt--{ton}"><div class="in">
<article class="mm-p mm-p--{art}" id="p{p['nr']}">
  <header class="mm-p__kopf" data-a="auf"><span class="mm-p__foto">{bild(p['foto'], None, '180px')}</span><h2><span class="mm-p__nr">{p['nr']}</span> {e(p['titel'])}</h2></header>
  {oben}
  <div class="mm-p__u">{teil_warum}{teil_wirkt}</div>
</article></div></section>"""


def agentur():
    agb = [('Ein Vertrag läuft ein Kalenderjahr und verlängert sich von selbst um ein weiteres.', '3c, 4a'),
           ('Kündigen kann man bis zum 15. November, auf Ende Jahr.', '4c'),
           ('Nach Vertragsende löscht zerone alle Daten. Für eine Sicherung muss das Haus selbst sorgen.', '4f'),
           ('Die Adresse monte-moro.ch läuft auf den Namen, den das Haus angibt.', '5e'),
           ('Die Preise sind nicht veröffentlicht, bezahlt wird jährlich im Voraus.', '2a, 2c')]
    agb_html = ''.join(f'<li>{e(t)}<small>Ziffer {z}</small></li>' for t, z in agb)
    gehoert = ['Die Seite selbst, mit allen Dateien.', 'Die Adresse monte-moro.ch, auf Ihr Haus eingetragen.', 'Die Zugänge, bei Ihnen hinterlegt.',
               'Das Buchungsfenster und die Tischreservation bleiben, wo sie sind.']
    return f'''<section class="fl fl--papier blatt mm-ag" id="agentur">
<div class="in">
{kopf_mitte('Ihre Seite heute', ['Wer sie baut', 'und wem sie gehört.'], '<p>Ihre Seite hat zerone computer gmbh aus Brig-Glis gebaut und betreut sie seit mindestens 2014. Alles hier steht so in öffentlichen Quellen: auf Ihrer Seite, in den Bedingungen von zerone und im Handelsregister.</p>')}
<div class="mm-ag__r">
  <div class="mm-ag__b" data-a="auf">
    <h3>Das Programm hinter Ihrer Seite</h3>
    <p>Ihre Seite läuft auf Joomla 3, einem Baukasten für Websites. Für diese Fassung erscheinen seit Februar 2025 keine Sicherheits-Updates mehr. Für Ihre Gäste ändert sich dadurch heute nichts Sichtbares, die Seite steht aber auf einer Fassung, die nicht mehr gepflegt wird.</p>
    <details class="mm-genau"><summary>Genauer nachlesen<i aria-hidden="true"></i></summary><div><p>Fassung 3.10.12 vom Juli 2023 (monte-moro.ch, abgerufen am {STAND}). Für Joomla 3 endete die Pflege im August 2023, die bezahlte Verlängerung am 17. Februar 2025 (joomshaper.com). Die Vorlage «zerone» ist am 4. April 2019 angelegt und nennt «Copyright (C) zerone computer gmbh», Lizenz «None».</p></div></details>
  </div>
  <div class="mm-ag__b" data-a="auf" style="--i:1">
    <h3>Was die Bedingungen von zerone sagen</h3>
    <ul class="mm-ag__l">{agb_html}</ul>
    <p class="mm-q">Allgemeine Geschäftsbedingungen «Internet Services», Stand August 2018, zerone.ch/agb, abgerufen am {STAND}. Zur Gestaltung und zu den Texten der Seite selbst sagen sie nichts.</p>
  </div>
  <div class="mm-ag__g">{geraet('a.1p', 'Ziffer 4c: Kündigung bis 15. November')}{geraet('a.2p', 'Ziffer 4f: Daten werden gelöscht', 1)}</div>
</div>
<div class="mm-ag__u" data-a="auf">
  <div><h3>Was bei uns Ihnen gehört</h3><ul class="mm-ag__h">{''.join(f'<li>{e(x)}</li>' for x in gehoert)}</ul></div>
  <div class="mm-ag__offen"><h3>Offen fürs Gespräch</h3><p>Ihren Vertrag mit zerone kennen wir nicht. Was er kostet, was er umfasst und wann er endet, ist eine Frage an Sie, keine Annahme von uns.</p></div>
</div>
</div>
</section>'''


def seite():
    P = I.PUNKTE
    n = len(P)
    liste = ''.join(f'<a class="mm-reg__z" href="#p{p["nr"]}"><span class="mm-reg__b">{bild(p["foto"], None, "64px")}</span><b>{p["nr"]}</b><span class="mm-reg__t">{e(p["titel"])}</span><i class="knauf">{PF}</i></a>' for p in P)
    leiste = ''.join(f'<a href="#p{p["nr"]}" data-ziel="p{p["nr"]}"><b>{p["nr"]}</b><span>{e(p["kurz"])}</span></a>' for p in P)
    punkte = ''.join(punkt(p, j) + pause(j) for j, p in enumerate(P))
    weitere = ''.join(f'<li><span>{e(t)}</span><a href="{e(u)}" target="_blank" rel="noopener">ansehen{PF}</a></li>' for t, u in I.WEITERE)
    gut = ''.join(f'<figure class="mm-gut__k" data-a="feder" style="--i:{i % 3}"><span class="mm-gut__b">{bild(k, None, "(max-width:700px) 92vw, 30vw")}</span><figcaption><b>{e(t)}</b><span>{e(s)}</span></figcaption></figure>' for i, (k, t, s) in enumerate(I.GUT))
    luecken = ''.join(f'<li>{e(x)}</li>' for x in I.OFFEN_SEITE)
    lauf = ''.join(f'<span>{e(w)}</span>{hz("lz__z")}' for w in I.LAUFWORTE)
    nav = '<a href="#brief">Überblick</a><a href="#p01">Die zwölf Punkte</a><a href="#gut">Was gut ist</a><a href="#agentur">Ihre Seite heute</a>'
    titelschrift = HAUS.SCHRIFT['titel'][1]
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Website Potentialanalyse · Hotel Monte-Moro, Saas-Almagell</title>
<meta name="description" content="Was Gäste auf der heutigen Website des Hotel Monte-Moro erleben: zwölf Punkte in einfachen Worten, jeder mit einem Beispiel und der Stelle auf der Seite. Stand {STAND}.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#F7F5F0">
<link rel="preload" href="werkbank/fonts/{titelschrift}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="werkbank/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="werkbank/werkbank.css?v={K.v('werkbank.css')}">
</head>
<body class="haus-{HAUS.KURZ} mm">
{K.sprite()}
<div class="gang-linie" aria-hidden="true"></div>
<header class="leiste"><div class="insel">
  <a class="insel__m" href="#oben">{HZ}<span>Potentialanalyse</span></a>
  <nav aria-label="Abschnitte">{nav}</nav>
  <a class="glanz" href="{HEUTE}" target="_blank" rel="noopener">Zur Website{PF}</a>
</div></header>

<main id="oben">
<section class="mm-auf" id="auftakt">
  <div class="in mm-auf__in">
    <div class="mm-auf__t">
      <div class="mm-auf__z" data-a="auf">{hz("")}</div>
      <p class="mm-auf__k" data-a="auf" style="--i:1">Website Potentialanalyse · Stand {STAND}</p>
      <h1 data-a="auf" style="--i:2"><span>Hotel</span> <em>Monte-Moro</em></h1>
      <p class="mm-auf__o" data-a="auf" style="--i:3">Saas-Almagell · Saastal · Wallis</p>
      <p class="mm-auf__s" data-a="auf" style="--i:4">Ihre Website, gelesen wie von einem Gast, der zum ersten Mal ins Saastal kommt. Zwölf Punkte, die er bemerkt, in einfachen Worten und mit der Stelle auf Ihrer Seite.</p>
      <div class="kn-reihe" data-a="auf" style="--i:5">{kn('Die zwölf Punkte', '#brief')}</div>
    </div>
    <figure class="mm-auf__f" data-a="feder" style="--i:2">{bild('hero', sizes='(max-width:1480px) 96vw, 1400px', lazy=False, prio=True)}<figcaption class="kerbe">Saas-Almagell, im Sommer</figcaption></figure>
  </div>
</section>

<section class="fl fl--papier mm-brief" id="brief">
  <div class="in mm-brief__in">
    <div class="mm-brief__l" data-a="auf">
      <p class="kap kap--z kap--links">{hz("kap__z")}<span>Guten Tag nach Saas-Almagell</span></p>
      <h2 class="mm-h2"><span class="mm-zeile">Liebe Frau Zurbriggen,</span> <span class="mm-zeile">lieber Herr Zurbriggen</span></h2>
      <div class="lauf"><i class="mm-stuetze" aria-hidden="true"></i><span class="mm-ich"><img src="bilder/robert.jpg?v={V}" alt="Robert Reff" width="640" height="640" loading="lazy" decoding="async"></span><p>Ihr Haus hat vieles, was Gäste suchen: Bergbahnen und Postautos inbegriffen, das Skigebiet zwei Minuten entfernt, ein Röstihüs mit eigener Handschrift und das Spa nebenan. Ich habe Ihre Website gelesen wie ein Gast und zwölf Stellen gefunden, an denen sie das nicht so zeigt, wie es ist.</p><p>Ganz oben steht, was ein Gast am schnellsten merkt. Jeder Punkt hat ein Beispiel, die Stelle auf Ihrer Seite und eine Idee, was man tun kann. Diese Seite ist eine Analyse, kein Entwurf.</p></div>
      <p class="mm-sig"><img class="mm-sig__u" src="bilder/unterschrift-robert.webp?v={V}" width="890" height="282" alt="" loading="lazy" decoding="async"><b>Robert Reff</b><small>Tasty Studios, Hamburg</small></p>
    </div>
    <div class="mm-reg" data-a="feder"><p class="mm-reg__k">Die zwölf Punkte, das Wichtigste zuerst</p>{liste}</div>
  </div>
</section>

<div class="laufzeile" aria-label="Worte des Hauses: {e(', '.join(I.LAUFWORTE))}"><div class="lz__band" aria-hidden="true"><div class="lz__satz">{lauf}</div><div class="lz__satz">{lauf}</div></div></div>

<div class="mm-punkte" id="punkte">{punkte}</div>
<section class="mm-blatt mm-blatt--hell mm-blatt--weitere"><div class="in">
  <details class="mm-weitere" id="weitere"><summary><span>Was uns sonst aufgefallen ist</span><small>{len(I.WEITERE)} kleinere Punkte</small><i aria-hidden="true"></i></summary><ul>{weitere}</ul></details>
</div></section>

{fenster('fenster-sonne', 'balkon', ['Bei uns scheint', 'fast immer die Sonne.'], 'Restaurant Röstihüs · monte-moro.ch', FOTOS['balkon'][1])}

<section class="fl fl--papier mm-gut" id="gut">
  <div class="in">
    {kopf_mitte('Was schon gut ist', ['Was Ihre Seite', 'heute richtig macht.'])}
    <div class="mm-gut__r">{gut}</div>
  </div>
</section>

{agentur()}

<section class="schluss" id="schluss">
  <img class="schluss__b ld" src="bilder/schluss-1200.webp?v={V}" alt="{e(FOTOS['dorf-nacht'][1])}" loading="lazy" decoding="async">
  <div class="in">
    {kopf_mitte('Zum Schluss', ['Das meiste', 'ist schon da.'])}
    <div class="lauf" data-a="auf" style="--i:1"><p>Die Zimmerarten stehen im Buchungsfenster, die Röstis auf der Karte, die Familie im Fuss, die besten Fotos bei Schweiz Tourismus. Es muss nur an eine Stelle.</p></div>
    <div class="platte schluss__offen" data-a="feder"><p class="pb__ko pb__ko--mitte"><i>{HAKEN}</i>Was offen bleibt</p><p class="schluss__os">Diese Punkte haben wir nicht prüfen oder belegen können. Sie stehen hier, damit nichts als sicher gilt, was es nicht ist.</p><ul class="luecken">{luecken}</ul></div>
    <div class="gruss-u gruss-u--bild mm-sig-s" data-a="auf" style="--i:2"><span class="gruss-u__b"><img src="bilder/robert.jpg?v={V}" alt="Robert Reff" width="640" height="640" loading="lazy" decoding="async"></span><span class="mm-sig mm-sig--d"><img class="mm-sig__u" src="bilder/unterschrift-robert.webp?v={V}" width="890" height="282" alt="" loading="lazy" decoding="async"><b>Robert Reff</b><small>Tasty Studios, Hamburg</small></span></div>
    <div class="kn-reihe" data-a="auf" style="--i:3">{kn('Zurück zum Anfang', '#oben')}</div>
  </div>
</section>
</main>

<footer class="fuss"><div class="in fuss__u">
  <div><div class="siegel">{HZ}<b>Hotel Monte-Moro</b></div><b>Website Potentialanalyse</b><p>Stand {STAND}. Fotos, Zeichen und Texte des Hauses gehören {HAUS.RECHTE} Die Beispiele zeigen, wie ein Gast eine Stelle erlebt, sie beschreiben keine echte Begebenheit. Studie von Tasty Studios, nicht die offizielle Website des Hauses.</p></div>
  <div class="r mono"><span>robert@tasty-studios.de</span><span>Robert Reff · Tasty Studios · Hamburg</span></div>
</div></footer>
<script src="werkbank/werkbank.js?v={K.v('werkbank.js')}"></script>
<script src="mm.js?v={V}"></script>
</body>
</html>
'''


MMJS = r'''/* Potentialanalyse Hotel Monte-Moro, Fassung 2: mitlaufende Liste am Rand (nur Klassen), Sicherung für Auftritte. Nativer Scroll. */
(function () {
  'use strict';
  var d = document, $$ = function (s) { return [].slice.call(d.querySelectorAll(s)); };
  var links = $$('.mm-rand a'), arts = $$('.mm-p');
  if ('IntersectionObserver' in window && links.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) links.forEach(function (a) { a.classList.toggle('an', a.dataset.ziel === e.target.id); }); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    arts.forEach(function (a) { io.observe(a); });
  }
  function sicher() {
    var h = innerHeight * 1.05;
    $$('[data-a]:not(.da),.zt:not(.da),.wfen:not(.da)').forEach(function (el) { if (el.closest('details:not([open])')) return; if (el.getBoundingClientRect().top < h) el.classList.add('da'); });
  }
  var t = 0; addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(sicher, 260); }, { passive: true });
  addEventListener('load', function () { setTimeout(sicher, 1500); }); setTimeout(sicher, 3500);
  $$('.laufzeile').forEach(function (l) { if (!('IntersectionObserver' in window)) return; new IntersectionObserver(function (es) { l.classList.toggle('steht', !es[0].isIntersecting); }).observe(l); });
  $$('.wfen').forEach(function (f) {
    if (!('IntersectionObserver' in window)) { f.classList.add('da'); return; }
    f.classList.add('weg');
    new IntersectionObserver(function (es) { f.classList.toggle('weg', !es[0].isIntersecting); }).observe(f);
    new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { o.disconnect(); f.classList.add('da'); } }, { threshold: 0.35 }).observe(f);
  });
  /* Lichtkegel (Robert 17.10.2026, Master 1b Nr. 16): von der Stelle im Gerät zur Lupe. Gerechnet aus der Lage ohne Bewegung (offsetLeft/Top), neu bei Grössenänderung. */
  var NS = 'http://www.w3.org/2000/svg';
  function lage(el, root) { var x = 0, y = 0; while (el && el !== root) { x += el.offsetLeft; y += el.offsetTop; el = el.offsetParent; } return { x: x, y: y }; }
  function kegel(o) {
    var svg = o.querySelector('.mm-kegel'), img = o.querySelector('.mm-g img[data-mark]'), z = o.querySelector('.mm-z--lupe');
    if (!svg || !img || !z) return;
    var ziel = z.querySelector('.mm-z__b, .mm-tab__b'); if (!ziel || !img.offsetWidth) return;
    var m = img.dataset.mark.split(',').map(Number), p = lage(img, o), q = lage(ziel, o);
    var sx0 = p.x + img.offsetWidth * m[0] / 100, sy0 = p.y + img.offsetHeight * m[1] / 100;
    var sx1 = sx0 + img.offsetWidth * m[2] / 100, sy1 = sy0 + img.offsetHeight * m[3] / 100;
    var r = 14, cx0 = q.x, cy0 = q.y, cx1 = q.x + ziel.offsetWidth, cy1 = q.y + ziel.offsetHeight, pts, a, b;
    if (cx0 >= sx1 + 8) { pts = [[sx1, sy0], [cx0, cy0 + r], [cx0, cy1 - r], [sx1, sy1]]; a = [sx1, (sy0 + sy1) / 2]; b = [cx0, (cy0 + cy1) / 2]; }
    else if (cx1 <= sx0 - 8) { pts = [[sx0, sy0], [cx1, cy0 + r], [cx1, cy1 - r], [sx0, sy1]]; a = [sx0, (sy0 + sy1) / 2]; b = [cx1, (cy0 + cy1) / 2]; }
    else {   // untereinander: zur Oberkante der Lupe, rechts an der Beschriftung «Was genau» vorbei
      var l = o.querySelector('.mm-s--was > .mm-l'), lx = l ? lage(l, o).x + l.offsetWidth + 22 : cx0;
      var fx0 = Math.max(cx0 + r, Math.min(lx, cx1 - 60));
      pts = [[sx0, sy1], [fx0, cy0], [cx1 - r, cy0], [sx1, sy1]]; a = [(sx0 + sx1) / 2, sy1]; b = [(fx0 + cx1) / 2, cy0];
    }
    var W = o.offsetWidth, H = o.offsetHeight, id = 'kg' + (o.id || Math.random().toString(36).slice(2, 7));
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('width', W); svg.setAttribute('height', H);
    svg.innerHTML = '<defs><linearGradient id="' + id + '" gradientUnits="userSpaceOnUse" x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '">' +
      '<stop offset="0" class="mm-kegel__a"/><stop offset="1" class="mm-kegel__b"/></linearGradient></defs>' +
      '<polygon class="mm-kegel__f" fill="url(#' + id + ')" points="' + pts.map(function (v) { return v.join(','); }).join(' ') + '"/>' +
      '<line class="mm-kegel__l" x1="' + pts[0][0] + '" y1="' + pts[0][1] + '" x2="' + pts[1][0] + '" y2="' + pts[1][1] + '"/>' +
      '<line class="mm-kegel__l" x1="' + pts[3][0] + '" y1="' + pts[3][1] + '" x2="' + pts[2][0] + '" y2="' + pts[2][1] + '"/>' ;
  }
  // am Handy: breite Vergrösserungen als Band zum Wischen, es beginnt dort, wo die rote Stelle steht
  function band() { $$('.mm-z__b').forEach(function (b) { if (b.dataset.lage || b.scrollWidth <= b.clientWidth + 2) return; var m = b.querySelector('.mm-z__m--h'); b.dataset.lage = 1;
    if (m && m.offsetLeft + m.offsetWidth > b.clientWidth - 16) b.scrollLeft = Math.max(0, m.offsetLeft - 20); }); }
  addEventListener('load', band); setTimeout(band, 1200);
  var os = $$('.mm-p__o');
  os.forEach(function (o, i) { o.id = o.id || 'mo' + i; });
  function alle() { os.forEach(kegel); }
  if ('ResizeObserver' in window) { var ro = new ResizeObserver(function (es) { es.forEach(function (e) { kegel(e.target); }); }); os.forEach(function (o) { ro.observe(o); }); }
  addEventListener('load', alle); $$('.mm-p__o img').forEach(function (im) { if (!im.complete) im.addEventListener('load', function () { kegel(im.closest('.mm-p__o')); }); }); alle();
  if ('IntersectionObserver' in window) {
    var ko = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { kegel(e.target); e.target.classList.add('kegel'); ko.unobserve(e.target); } }); }, { threshold: 0.3 });
    os.forEach(function (o) { ko.observe(o); });
  } else os.forEach(function (o) { o.classList.add('kegel'); });
})();
'''


def main():
    fotos_bauen()
    tapeten()
    K.gestaltung()
    shutil.copy2(os.path.join(ROOT, 'bilder', 'tapete-hell.webp'), os.path.join(ROOT, 'werkbank', 'tapete-hell.webp'))
    open(os.path.join(ROOT, 'mm.js'), 'w', encoding='utf-8').write(MMJS)
    fehlt = [b['wo'] for b in I.BEWEIS.values() if b['wo'] not in GER] + [z for b in I.BEWEIS.values() for z, _, _ in b['zs'] if z not in AUS]
    print('Geräte ohne Bild:', fehlt or 'keine')
    t = seite()
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(t)
    print('index.html', len(I.PUNKTE), 'Punkte', len(t) // 1024, 'KB')


if __name__ == '__main__':
    main()
