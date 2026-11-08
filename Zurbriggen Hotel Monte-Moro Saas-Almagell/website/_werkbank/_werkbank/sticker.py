#!/usr/bin/env python3
"""Hotel Monte-Moro: vierundzwanzig Sticker für das Hotel (Werkbank Papier, 08.11.2026; Bauart wie sticker.py der Vorlage).
Für den Koffer, die Skibox, die Trinkflasche und das Fotoalbum der Gäste, im Geist der alten Kofferetiketten der Hotels (Master 5a, Regel 3).
Gebaut wie die Untersetzer (papier_kern.etikett, Druckbogen A3 mit Schnittlinie in Magenta), in einen eigenen Ordner sticker/.
Formen: rund, eckig, Kapsel und der Grat (Rechteck mit der Bergkamm-Linie der Website als Oberkante). Inhalte nur vom Haus: die Wortmarke,
der Bergkamm, die Sätze der Website («Mehr erleben, weniger zahlen.», «Und morgen scheint die Sonne wieder.», «Bei uns scheint fast immer
die Sonne.», «Es lebe die Tradition!», «Willkommen im Monte-Moro.», «Zwei Minuten bis zum Lift.»), die Skigebiete des Saastals mit ihren
Höhen, «Familie Zurbriggen · seit 1967» und Fotos des Hauses und des Tals aus der Website.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py _werkbank/sticker.py "<website/_werkbank>"   →  satz/sticker*.html, sticker_plan.json
   danach  node _werkbank/sticker_druck.js "<…>" sticker   und   … mit_papier.py _werkbank/sticker.py "<…>" --seite"""
import json, os, sys
import papier_kern as P
import bogen_mitte  # noqa: F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import etikett, hwz, hzz, blatt, t, e
from kern import H, W
import papier_neu as N
from papier_neu import NACHT, BLAU, LAERCHE, LAERCHE_T, MESSING, PAPIER, CREME, WAND, TINTE, GRAU, FASSADE
from untersetzer_neu import CAP, FAM

WM = 1425 / 3483   # Höhe : Breite der Wortmarke
BK = 696 / 3483    # Höhe : Breite des Bergkamms


# ---------------------------------------------------------------- Formen (SVG-Pfade in mm)
def kreis(d):
    r = d / 2
    return f'M{r} 0A{r} {r} 0 1 1 {r - .01} 0Z'


def eck(b, h, r=3):
    return f'M{r} 0H{b - r}A{r} {r} 0 0 1 {b} {r}V{h - r}A{r} {r} 0 0 1 {b - r} {h}H{r}A{r} {r} 0 0 1 0 {h - r}V{r}A{r} {r} 0 0 1 {r} 0Z'


def kapsel(b, h):
    return eck(b, h, h / 2)


def grat(b, h, gh=None):
    """Rechteck mit der Gratlinie als Oberkante (gh = Höhe des Grats), unten gerundet"""
    gh = gh or b * .09
    pk = N.grat_punkte(0, 0, b, gh)
    return ('M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in pk) + f' L{b} {h - 2.4}A2.4 2.4 0 0 1 {b - 2.4} {h}H2.4A2.4 2.4 0 0 1 0 {h - 2.4}Z')


# ---------------------------------------------------------------- Bausteine
def grund(form, farbe):
    return f'<path d="{form}" fill="{farbe}"/>'


def ring_kreis(d, farbe, ab=2.4):
    return f'<circle cx="{d / 2}" cy="{d / 2}" r="{d / 2 - ab}" fill="none" stroke="{farbe}" stroke-width=".3"/>'


def ring_eck(b, h, farbe, ab=2.2, r=1.6, d=.3):
    return f'<rect x="{ab}" y="{ab}" width="{b - 2 * ab}" height="{h - 2 * ab}" rx="{r}" fill="none" stroke="{farbe}" stroke-width="{d}"/>'


def zl(cx, y, text, gr, farbe, art):
    sp = {'m': .18, 's': 0, 'i': 0}[art]
    return (f'<text x="{cx:.2f}" y="{y:.2f}" text-anchor="middle" font-family="{FAM[art]}" font-size="{gr}" letter-spacing="{sp}em" fill="{farbe}">'
            f'{e(text.upper() if art == "m" else text)}</text>')


def mitte(cx, cy, teile):
    """Gruppe senkrecht genau um cy: ('s'|'m'|'i', text, gr, farbe, abstand) oder ('form', hoehe, zeichnen(y), abstand)"""
    hoehe = sum((x[2] * CAP[x[0]] if x[0] != 'form' else x[1]) + x[-1] for x in teile) - teile[-1][-1]
    y = cy - hoehe / 2
    aus = ''
    for x in teile:
        if x[0] == 'form':
            aus += x[2](y); y += x[1] + x[3]
        else:
            art, text, gr, farbe, ab = x
            h = gr * CAP[art]
            aus += zl(cx, y + h, text, gr, farbe, art); y += h + ab
    return aus


def wm(cx, b, farbe):
    return ('form', b * WM, lambda y: hwz(cx, y, b, farbe), 0)


def bk(cx, b, farbe, ab=4):
    return ('form', b * BK, lambda y: hzz(cx, y, b, farbe), ab)


def strich(cx, b, farbe, ab=4):
    return ('form', .35, lambda y: f'<rect x="{cx - b / 2:.2f}" y="{y:.2f}" width="{b}" height=".35" fill="{farbe}"/>', ab)


def foto(key, b, h, ident, form, lage='xMidYMid slice', rand=2.5):
    """Foto im Sticker, mit schmalem Rand in der Grundfarbe; form = Pfad derselben Form, verkleinert"""
    s = (b - 2 * rand) / b
    return (f'<clipPath id="{ident}c"><path d="{form}" transform="translate({rand} {rand}) scale({s:.4f} {(h - 2 * rand) / h:.4f})"/></clipPath>'
            f'<image href="{e(N.bild_satz(key))}" x="{rand}" y="{rand}" width="{b - 2 * rand}" height="{h - 2 * rand}" preserveAspectRatio="{lage}" clip-path="url(#{ident}c)"/>')


# ---------------------------------------------------------------- die vierundzwanzig (gemischt: Form, Grösse und Farbe wechseln)
def alle():
    S, n = [], [0]

    def s(b, h, form, innen, name, satz):
        n[0] += 1
        S.append(etikett(f's{n[0]:02d}', b, h, form, innen, name, satz))

    def nid():
        return f's{n[0] + 1:02d}'
    f = kreis(60)
    s(60, 60, f, grund(f, PAPIER) + ring_kreis(60, MESSING) + mitte(30, 30, [wm(30, 44, BLAU)]), 'Die Wortmarke', 'Rund, 60 mm. Das Logo in Logo-Blau auf Papier.')
    f = grat(70, 48)
    s(70, 48, f, grund(f, NACHT) + mitte(35, 27, [bk(35, 30, LAERCHE, 5), ('s', 'Saas-Almagell', 7.2, PAPIER, 4.4), ('m', 'Wallis · Schweiz', 2.2, MESSING, 0)]),
      'Saas-Almagell', 'Der Grat, 70 × 48 mm. Der Bergkamm über dem Namen des Dorfs.')
    f = kapsel(104, 24)
    s(104, 24, f, grund(f, NACHT) + mitte(52, 12, [('s', N.SATZ, 7, PAPIER, 0)]), N.SATZ, 'Kapsel, 104 mm. Der Satz des Hauses.')
    f = eck(60, 60, 2.4)
    s(60, 60, f, grund(f, PAPIER) + foto('haus-sommer-g', 60, 60, nid(), f, 'xMidYMid slice'), 'Das Haus im Sommer', 'Eckig, 60 mm. Die Balkone aus Lärche in der Sonne.')
    f = kreis(52)
    s(52, 52, f, grund(f, LAERCHE_T) + mitte(26, 26, [('s', 'Und morgen', 5.6, PAPIER, 2.4), ('s', 'scheint die', 5.6, PAPIER, 2.4), ('s', 'Sonne wieder.', 5.6, PAPIER, 0)]),
      N.MORGEN, 'Rund, 52 mm. Der letzte Satz der Seite «Anreise».')
    f = eck(50, 66, 2.4)
    s(50, 66, f, grund(f, NACHT) + ring_eck(50, 66, MESSING, 2.6) + mitte(25, 33, [('m', 'Skigebiete', 2, MESSING, 6),
      ('s', 'Saas-Fee', 6, PAPIER, 1.8), ('m', '3500 m', 2.8, LAERCHE, 5), ('s', 'Saas-Grund', 6, PAPIER, 1.8), ('m', '3200 m', 2.8, LAERCHE, 5),
      ('s', 'Saas-Almagell', 6, PAPIER, 1.8), ('m', '2400 m', 2.8, LAERCHE, 0)]),
      'Die Skigebiete', 'Eckig, 50 × 66 mm. Die drei Skigebiete des Saastals mit ihren Höhen, wie auf der Seite «Saastal».')
    f = kreis(46)
    s(46, 46, f, grund(f, NACHT) + mitte(23, 23, [bk(23, 30, LAERCHE, 0)]), 'Der Bergkamm', 'Rund, 46 mm. Das Zeichen aus dem Logo, in Lärche.')
    f = grat(80, 56)
    s(80, 56, f, grund(f, PAPIER) + foto('mattmark', 80, 56, nid(), f, 'xMidYMid slice', 0), 'Ein Bergsee', 'Der Grat, 80 × 56 mm. Ein Bergsee über dem Saastal, das Foto bis an den Rand.')
    f = kapsel(96, 22)
    s(96, 22, f, grund(f, PAPIER) + mitte(48, 11, [('m', N.SEIT, 2.9, LAERCHE_T, 0)]), N.SEIT, 'Kapsel, 96 mm. Wie die Familie im Fuss der Website steht.')
    f = kreis(56)
    s(56, 56, f, grund(f, PAPIER) + ring_kreis(56, LAERCHE_T) + mitte(28, 28, [('s', 'Es lebe', 7, NACHT, 2.6), ('s', 'die Tradition!', 7, NACHT, 4), ('m', 'Röstihüs', 2.2, LAERCHE_T, 0)]),
      N.TRADITION, 'Rund, 56 mm. Der Satz des Röstihüs.')
    f = eck(60, 60, 2.4)
    s(60, 60, f, grund(f, PAPIER) + foto('haus-winter-g', 60, 60, nid(), f), 'Das Haus im Winter', 'Eckig, 60 mm. Das Monte-Moro im frischen Schnee.')
    f = eck(70, 40, 2.4)
    s(70, 40, f, grund(f, BLAU) + mitte(35, 20, [('s', 'Zwei Minuten', 7, PAPIER, 2.4), ('s', 'bis zum Lift.', 7, PAPIER, 0)]), N.LIFT, 'Eckig, 70 × 40 mm. Vom Haus zum Skigebiet Saas-Almagell.')
    f = kreis(50)
    s(50, 50, f, grund(f, NACHT) + mitte(25, 25, [wm(25, 38, PAPIER)]), 'Die Wortmarke auf der Nacht', 'Rund, 50 mm. Das Logo in Papier auf der Nacht.')
    f = grat(70, 52)
    s(70, 52, f, grund(f, CREME) + mitte(35, 29, [('m', 'Im Sommer', 2.2, LAERCHE_T, 4.6), ('s', 'Über 250 km', 8.4, NACHT, 3), ('s', 'Wanderwege.', 8.4, NACHT, 0)]),
      'Über 250 km Wanderwege', 'Der Grat, 70 × 52 mm. Das Saastal im Sommer, wie es das Haus beschreibt.')
    f = eck(60, 60, 2.4)
    s(60, 60, f, grund(f, PAPIER) + foto('alpenrosen', 60, 60, nid(), f, 'xMaxYMid slice'), 'Alpenrosen', 'Eckig, 60 mm. Alpenrosen über dem Saastal.')
    f = kapsel(100, 24)
    s(100, 24, f, grund(f, LAERCHE_T) + mitte(50, 12, [('m', 'Postauto im ganzen Saastal inklusive', 2.6, PAPIER, 0)]), N.D.POSTAUTO, 'Kapsel, 100 mm. Im Zimmerpreis, Sommer und Winter.')
    f = kreis(56)
    s(56, 56, f, grund(f, CREME) + ring_kreis(56, MESSING) + mitte(28, 28, [bk(28, 22, LAERCHE, 4.4), ('s', 'Willkommen', 6.6, NACHT, 2.4), ('s', 'im Monte-Moro.', 6.6, NACHT, 0)]),
      N.WILLKOMMEN, 'Rund, 56 mm. Der Gruss an der Rezeption.')
    f = eck(60, 60, 2.4)
    s(60, 60, f, grund(f, PAPIER) + foto('murmeltiere', 60, 60, nid(), f), 'Murmeltiere', 'Eckig, 60 mm. Zwei Murmeltiere im Saastal.')
    f = eck(54, 54, 2.4)
    s(54, 54, f, grund(f, NACHT) + ring_eck(54, 54, MESSING, 2.6) + mitte(27, 27, [('s', 'Bei uns', 6.4, PAPIER, 2.4), ('s', 'scheint fast', 6.4, PAPIER, 2.4), ('s', 'immer', 6.4, PAPIER, 2.4), ('s', 'die Sonne.', 6.4, LAERCHE, 0)]),
      N.SONNE_KURZ, 'Eckig, 54 mm. Der Satz am Fuss jeder Seite.')
    f = grat(80, 56)
    s(80, 56, f, grund(f, PAPIER) + foto('dorf-winter', 80, 56, nid(), f, 'xMidYMid slice', 0), 'Das Dorf im Winter', 'Der Grat, 80 × 56 mm. Saas-Almagell im Schnee.')
    f = kreis(46)
    s(46, 46, f, grund(f, PAPIER) + ring_kreis(46, LAERCHE_T) + mitte(23, 23, [('m', 'Saastal', 2.4, LAERCHE_T, 3.4), ('s', 'Mattmark', 7, NACHT, 0)]),
      'Mattmark', 'Rund, 46 mm. Ein Tagesausflug aus der Liste des Hauses.')
    f = kapsel(92, 24)
    s(92, 24, f, grund(f, NACHT) + mitte(46, 12, [('s', 'Monte-Moro · Saas-Almagell', 5.4, PAPIER, 0)]),
      'Monte-Moro · Saas-Almagell', 'Kapsel, 92 mm. Für den Koffer, wie früher an der Rezeption.')
    f = eck(60, 60, 2.4)
    s(60, 60, f, grund(f, PAPIER) + foto('gletscher', 60, 60, nid(), f), 'Über den Gletschern', 'Eckig, 60 mm. Über den Gletschern des Saastals.')
    f = grat(66, 50)
    s(66, 50, f, grund(f, BLAU) + mitte(33, 28, [('s', 'Mehr erleben,', 7, PAPIER, 2.6), ('s', 'weniger zahlen.', 7, PAPIER, 0)]),
      'Der Satz unter dem Grat', 'Der Grat, 66 × 50 mm. Mehr erleben, weniger zahlen, im Logo-Blau.')
    return S


def fertig(S):
    """Satzdateien und Druckbögen wie papier_kern.fertig, aber für den Ordner sticker/."""
    alle_ = ''
    for x in S:
        svg = f'<svg class="abs" style="inset:0;width:{x["b"]}mm;height:{x["h"]}mm" viewBox="0 0 {x["b"]} {x["h"]}">{x["innen"]}</svg>'
        alle_ += blatt(x['b'], x['h'], svg, 'etikett', 'background:transparent')
    P.seite('sticker', [alle_], 'Sticker')
    boegen, akt, x0, y0, zh = [], [], 14, 16, 0
    for x in S:
        if x0 + x['b'] > 420 - 14:
            x0, y0, zh = 14, y0 + zh + 9, 0
        if y0 + x['h'] > 297 - 12:
            boegen.append(akt); akt, x0, y0, zh = [], 14, 16, 0
        akt.append((x, x0, y0)); x0 += x['b'] + 9; zh = max(zh, x['h'])
    boegen.append(akt)
    seiten = []
    for nr, akt in enumerate(boegen):
        inn = ''.join(f'<svg class="abs" style="left:{ox}mm;top:{oy}mm;width:{x["b"]}mm;height:{x["h"]}mm;overflow:visible" viewBox="0 0 {x["b"]} {x["h"]}">'
                      f'{x["innen"].replace("id=\"", "id=\"b" + x["id"]).replace("url(#", "url(#b" + x["id"]).replace("href=\"#", "href=\"#b" + x["id"]).replace("#b" + x["id"] + "hz", "#hz").replace("#b" + x["id"] + "hw", "#hw")}'
                      f'<path d="{x["form"]}" fill="none" stroke="#e6007e" stroke-width=".15"/></svg>' for x, ox, oy in akt)
        inn += t(14, 6.5, f'{e(N.NAME)} · Sticker · Druckbogen {nr + 1} von {len(boegen)} · A3 quer · Originalgrösse · Schnittlinie in Magenta', 'm', f'font-size:2.1mm;color:{TINTE}')
        seiten.append(blatt(420, 297, inn, '', 'background:#fff'))
    P.seite('sticker-bogen', seiten, 'Sticker, Druckbogen')
    plan = {'etiketten': [{k: x[k] for k in ('id', 'b', 'h', 'name', 'satz', 'form')} for x in S], 'boegen': len(boegen),
            'masse': [min(min(x['b'], x['h']) for x in S), max(max(x['b'], x['h']) for x in S)]}
    json.dump(plan, open(os.path.join(W, 'sticker_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Sticker gesetzt:', len(S), 'Stück,', len(boegen), 'Druckbögen')


def _auslage():
    """Auslage neben dem Titel: nur helle und farbige Sticker (dunkle verschwänden auf der Nacht der Seite, Kriterium 29), ohne Überdeckung."""
    lage = {0: (2, 2, 24, -4), 3: (30, 0, 24, 3), 4: (58, 4, 22, -3), 7: (2, 36, 30, 2), 9: (36, 34, 22, -3), 10: (62, 32, 24, 4),
            11: (6, 68, 28, -2), 13: (38, 64, 27, 3), 14: (70, 64, 24, -4)}
    return [lage.get(i, (0, 0, 0, 0)) for i in range(40)]


def seite():
    """sticker/index.html mit der Seite der Untersetzer (papier_seiten.etiketten), umgestellt auf den Ordner sticker/."""
    import papier_seiten as PS
    from kern import zahl
    plan = json.load(open(os.path.join(W, 'sticker_plan.json')))
    PS.plan = dict(PS.plan, etiketten=plan['etiketten'], boegen=plan['boegen'], masse=plan['masse'])
    PS.ROH = os.path.join(W, 'roh', 'sticker')
    PS.ET = dict(ordner='sticker', name='Sticker', einzahl='Sticker')
    n = len(plan['etiketten'])
    PS.S = dict(PS.S, etik_titel=('Sticker', 'für den Koffer.'),
                etik_text='Früher klebte das Hotel sein Etikett auf den Koffer. Hier sind {n} Ideen dafür, für Koffer, Skibox und Trinkflasche: rund, eckig, als Kapsel und mit dem Grat des Bergkamms als Oberkante.',
                etik_kap='Die Sticker', etik_kopf=[zahl(n), 'Sticker.'],
                etik_kopftext='Die Wortmarke und der Bergkamm aus Ihrem Logo, die Sätze Ihrer Website, die Skigebiete des Saastals und Fotos vom Haus und vom Tal.',
                etik_auslage=_auslage(), etik_haufen=None)
    PS.etiketten()
    p = os.path.join(os.path.dirname(W), 'sticker', 'index.html')
    tx_ = open(p, encoding='utf-8').read().replace(' loading="lazy"', '')
    open(p, 'w', encoding='utf-8').write(tx_)
    from PIL import Image
    im = Image.open(os.path.join(os.path.dirname(W), 'sticker', 'img', 's05.webp')); im.save(os.path.join(os.path.dirname(W), 'sticker', 'img', 'vorschau.webp'), 'WEBP', quality=86)
    print('Seite gebaut: sticker/ ·', n, 'Sticker')


if __name__ == '__main__':
    if '--seite' in sys.argv:
        import kern as K
        K.gestaltung(); seite()
    else:
        fertig(alle())
        N.satz_namen('sticker.html', 'sticker-bogen.html')
