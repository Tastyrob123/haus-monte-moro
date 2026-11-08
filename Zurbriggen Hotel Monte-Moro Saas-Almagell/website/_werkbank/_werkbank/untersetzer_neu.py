#!/usr/bin/env python3
"""Hotel Monte-Moro: zwölf Untersetzer für das Röstihüs, Bierdeckel rund 94 mm (Werkbank Papier, 08.11.2026; System wie die Untersetzer von
der Vorlage: Messinglinie 3 mm innen, jedes Motiv als Gruppe genau in der Mitte des Kreises, Höhe aus Versalhöhe und Grundlinie berechnet,
Zeile rundherum gleichmässig verteilt).
Motive nur aus dem Haus: die Wortmarke (Papier auf Nacht, Logo-Blau auf Papier), der Bergkamm in Lärche, «Es lebe die Tradition!»,
das Röstihüs, Rösti Tschug Tschug, das Cordon bleu Monte-Moro, der Zurbriggen Spritz, der Wein von Fabian, «Regional und herzlich.»,
«Bei uns scheint fast immer die Sonne.», dazu Fotos der Stube und des Raclettes randlos im Kreis. Aufruf aus papier.py (untersetzer_alle)."""
import math
import os
from fontTools.ttLib import TTFont
from papier_kern import etikett, hwz, hzz, e
from kern import W
import papier_neu as N
from papier_neu import NACHT, BLAU, LAERCHE, LAERCHE_T, MESSING, PAPIER, CREME, WAND, TINTE, GRAU

D = 94
R = D / 2
WM = 1425 / 3483       # Höhe : Breite der Wortmarke
BK = 696 / 3483        # Höhe : Breite des Bergkamms
_F = os.path.join(W, 'fonts')


def _cap(datei):
    f = TTFont(os.path.join(_F, datei))
    return f['OS/2'].sCapHeight / f['head'].unitsPerEm


CAP = {'s': _cap('FjallaOne-Regular.ttf'), 'm': _cap('DMMono-Regular.ttf'), 'i': _cap('InstrumentSans-Regular.ttf')}
FAM = {'s': 'Fjalla One', 'm': 'DM Mono', 'i': 'Instrument Sans'}
RING = 'Restaurant Röstihüs · Hotel Monte-Moro · Saas-Almagell'


def kreis(r=R):
    return f'M{R} {R - r}A{r} {r} 0 1 1 {R - .01} {R - r}Z'


def zeile(y_grund, text, gr, farbe, art='s', sperr=0, x=R, anker='middle'):
    return (f'<text x="{x:.2f}" y="{y_grund:.2f}" text-anchor="{anker}" font-family="{FAM[art]}" font-size="{gr}" letter-spacing="{sperr}em" fill="{farbe}">'
            f'{e(text.upper() if art == "m" else text)}</text>')


def gruppe(teile, mitte=R):
    """teile: ('text', text, gr, farbe, art, sperr, abstand_danach) oder ('form', hoehe, zeichnen(y_oben), abstand_danach);
    die ganze Gruppe (Versalhöhe bis Grundlinie, Formen ganz) steht senkrecht genau in der Mitte."""
    hoehe = sum((t[2] * CAP[t[4]] if t[0] == 'text' else t[1]) + t[-1] for t in teile) - teile[-1][-1]
    y = mitte - hoehe / 2
    aus = ''
    for t in teile:
        if t[0] == 'text':
            _, text, gr, farbe, art, sperr, ab = t
            h = gr * CAP[art]
            aus += zeile(y + h, text, gr, farbe, art, sperr)
            y += h + ab
        else:
            _, h, zeichnen, ab = t
            aus += zeichnen(y)
            y += h + ab
    return aus


def strich(b, farbe, d=.35):
    return lambda y: f'<rect x="{R - b / 2:.2f}" y="{y:.2f}" width="{b}" height="{d}" fill="{farbe}"/>'


def wortmarke(b, farbe):
    return lambda y: hwz(R, y, b, farbe)


def bergkamm(b, farbe):
    return lambda y: hzz(R, y, b, farbe)


def ring_text(ident, text, farbe, r=37.4, gr=2.2, sperr=.18):
    """Zeile rundherum, mit textLength genau auf den Umfang verteilt; Grundlinie auf dem Kreis r."""
    umfang = 2 * math.pi * r
    stueck = text.upper() + ' · '
    n = max(1, round(umfang / (len(stueck) * gr * (0.6 + sperr))))
    return (f'<path id="{ident}r" d="M{R - r} {R}A{r} {r} 0 1 1 {R + r} {R}A{r} {r} 0 1 1 {R - r} {R}" fill="none"/>'
            f'<text font-family="DM Mono" font-size="{gr}" letter-spacing="{sperr}em" fill="{farbe}">'
            f'<textPath href="#{ident}r" textLength="{umfang - gr * sperr:.2f}" lengthAdjust="spacing">{e(stueck * n)}</textPath></text>')


def foto(ident, key, fx, fy, breite, hoehe_zu_breite):
    """Foto randlos im Kreis; der Punkt (fx, fy) des Bildes liegt genau in der Mitte."""
    h = breite * hoehe_zu_breite
    x, y = R - fx * breite, R - fy * h
    assert x <= 0 and y <= 0 and x + breite >= D and y + h >= D, (key, x, y)
    return (f'<clipPath id="{ident}c"><path d="{kreis()}"/></clipPath>'
            f'<image href="{e(N.bild_satz(key))}" x="{x:.2f}" y="{y:.2f}" width="{breite}" height="{h:.2f}" preserveAspectRatio="none" clip-path="url(#{ident}c)"/>')


def us(ident, grund, innen, name, satz, linie=MESSING, ring=None):
    z = f'<path d="{kreis()}" fill="{grund}"/>' + innen
    if ring:
        z += ring_text(ident, ring[0], ring[1])
    z += f'<circle cx="{R}" cy="{R}" r="{R - 3}" fill="none" stroke="{linie}" stroke-width=".35"/>'
    return etikett(ident, D, D, kreis(), z, name, satz)


def alle():
    U = []
    T = lambda *a: ('text',) + a
    # 1, 2: die Wortmarke gross
    U.append(us('u01', NACHT, gruppe([('form', 58 * WM, wortmarke(58, PAPIER), 0)]), 'Die Wortmarke auf der Nacht',
                'Das Logo des Hauses in Papier auf der Nacht, mit der Messinglinie rundherum.'))
    U.append(us('u02', PAPIER, gruppe([('form', 58 * WM, wortmarke(58, N.BLAU), 0)]), 'Die Wortmarke in Logo-Blau',
                'Das Logo in seinem eigenen Blau auf dem Papier der Website.', LAERCHE_T))
    # 3: Es lebe die Tradition!
    U.append(us('u03', PAPIER, gruppe([T('Es lebe', 9.6, NACHT, 's', 0, 3.6), T('die Tradition!', 9.6, NACHT, 's', 0, 5.4), ('form', .35, strich(12, LAERCHE), 0)]),
                'Es lebe die Tradition!', 'Der Satz der Röstihüs-Seite, rundherum Restaurant und Hotel.', LAERCHE_T, (RING, LAERCHE_T)))
    # 4: das Röstihüs, Foto der Stube mit den Säcken
    U.append(us('u04', NACHT, foto('u04', 'roesti-raum', .36, .5, 150, 1356 / 2048), 'Die Stube',
                'Die Stube des Röstihüs mit den Kartoffelsäcken, randlos im Kreis.'))
    # 5: Bergkamm und Röstihüs
    U.append(us('u05', NACHT, gruppe([('form', 40 * BK, bergkamm(40, LAERCHE), 6), T('Röstihüs', 13, PAPIER, 's', 0, 5), T('Saas-Almagell', 2.4, MESSING, 'm', .22, 0)]),
                'Röstihüs', 'Der Bergkamm in Lärche über dem Namen des Restaurants.'))
    # 6: Rösti Tschug Tschug
    U.append(us('u06', PAPIER, gruppe([T('Rösti', 5, LAERCHE_T, 's', 0, 3), T('Tschug Tschug', 9, NACHT, 's', 0, 5), ('form', .35, strich(12, LAERCHE), 5),
                                        T('Mit Calvados flambiert', 2.2, GRAU, 'm', .16, 0)]),
                'Rösti Tschug Tschug', 'Die Rösti mit Apfelmus, mit Calvados flambiert, von der Karte des Röstihüs.', LAERCHE_T, (RING, LAERCHE_T)))
    # 7: Cordon bleu Monte-Moro
    n, s, p = N.CORDON[0]
    U.append(us('u07', NACHT, gruppe([T('Cordon bleu', 5, LAERCHE, 's', 0, 3), T(n, 10.4, PAPIER, 's', 0, 5), ('form', .35, strich(12, MESSING), 5),
                                       T('Kalbfleisch mit Schinken', 2.2, WAND, 'm', .14, 2.4), T('und Käse', 2.2, WAND, 'm', .14, 0)]),
                'Cordon bleu Monte-Moro', 'Das Cordon bleu, das den Namen des Hauses trägt: Kalbfleisch mit Schinken und Käse.', MESSING, (RING, MESSING)))
    # 8: Zurbriggen Spritz
    n, s, p = N.SPRITZ[0]
    U.append(us('u08', BLAU, gruppe([T('Zum Apéro', 2.4, PAPIER, 'm', .22, 5), T('Zurbriggen', 9.6, PAPIER, 's', 0, 3.4), T('Spritz', 9.6, PAPIER, 's', 0, 5),
                                      T('Lemonsoda · Prosecco', 2.1, WAND, 'm', .14, 2.2), T('Blue Curaçao', 2.1, WAND, 'm', .14, 0)]),
                'Zurbriggen Spritz', 'Der Spritz, der den Namen der Familie trägt, im Logo-Blau.', MESSING))
    # 9: Wein von Fabian
    U.append(us('u09', NACHT, gruppe([T('Wein', 11, PAPIER, 's', 0, 3.4), T('von Fabian.', 11, PAPIER, 's', 0, 5), ('form', .35, strich(12, LAERCHE), 5),
                                       T(N.HOTELWEINE[0][0].replace('«Hotelwein» ', ''), 2.3, MESSING, 'm', .2, 0)]),
                'Wein von Fabian', 'Die zwei Hotelweine, die Fabian selbst kreiert hat.', MESSING, (RING, MESSING)))
    # 10: Raclette, Foto
    U.append(us('u10', NACHT, foto('u10', 'raclette', .76, .5, 226, 500 / 1200), 'Raclette',
                'Der Käse am Feuer, wie am Racletteabend im Stübli.'))
    # 11: Regional und herzlich.
    U.append(us('u11', CREME, gruppe([('form', 30 * BK, bergkamm(30, LAERCHE_T), 6), T('Regional', 10.4, NACHT, 's', 0, 3.4), T('und herzlich.', 10.4, NACHT, 's', 0, 0)]),
                'Regional und herzlich.', 'Der Titel der Stube auf der Röstihüs-Seite.', LAERCHE_T, (RING, LAERCHE_T)))
    # 12: Bei uns scheint fast immer die Sonne.
    U.append(us('u12', LAERCHE_T, gruppe([T('Bei uns scheint', 7.4, PAPIER, 's', 0, 3), T('fast immer', 7.4, PAPIER, 's', 0, 3), T('die Sonne.', 7.4, PAPIER, 's', 0, 5),
                                           T('Sonnenterrasse vor dem Haus', 2.1, CREME, 'm', .14, 0)]),
                'Bei uns scheint fast immer die Sonne.', 'Der Satz am Fuss jeder Seite, für die Tische auf der Sonnenterrasse.', CREME))
    return U
