#!/usr/bin/env python3
"""Ideen für Papier: Drucksachen und Untersetzer für das Hotel Monte-Moro (Werkbank Papier, 08.11.2026; Bauart wie papier.py der Vorlage,
Inhalt und Kleid des Hauses).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py _werkbank/papier.py "<website/_werkbank>"

Sieben eigene Stücke, so wie ein Hotel mit Restaurant druckt: die Karte am Tisch im Röstihüs (Röstis vorne, Cordon bleus, Dessert,
Apéro, Stübli und der Wein von Fabian hinten), der Aushang «Inklusive» als Bon der Rezeption, die Tischkarte zum Hotelwein, der Aushang
zum Racletteabend im Stübli, die Karte zum Kidsclub, der Willkommensbrief im Zimmer, Briefbogen und Umschlag. Dazu zwölf Untersetzer
für das Röstihüs (untersetzer_neu.py) und die fertigen Drucksachen der Hausdruckerei (_werkzeuge/imprimerie/haeuser/montemoro/drucksachen/,
nur kopiert → papier_mehr.json), sobald dort Stücke des Monte-Moro liegen.
Kleid: Papier, Nacht, Lärche als Akzent, Messing nur als feine Linie, Grat-Kante über den Fotos, Bergkamm als Zeichen, das ganze Logo als
Wortmarke. Schrift: Fjalla One, Instrument Sans, DM Mono (druckschrift.py). Fakten nur aus website/inhalt/daten.py (papier_neu.py)."""
import json, os, re, shutil
from PIL import Image
import papier_kern as P
import bogen_mitte  # noqa: F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import t, lin, kasten, foto, blatt, hw, hz
from kern import H, ROOT
import druckschrift
import mit_papier
import papier_neu as N
from papier_neu import (NACHT, NACHTBLAU, TIEFNACHT, BLAU, LAERCHE, LAERCHE_T, MESSING, PAPIER, FASSADE, CREME, WAND, TINTE, GRAU, e,
                        grat_deckel, grat_linie)

WEB = os.path.dirname(ROOT)
HAUS = os.path.dirname(WEB)
PW = os.path.join(HAUS, '_werkzeuge', 'imprimerie', 'haeuser', 'montemoro', 'drucksachen')
MEINS = ['Auswahl und Anordnung der Sätze und Angaben auf Karte, Aushängen, Tischkarte, Willkommensbrief und Untersetzern',
         'Die Zeilen «Gut zu wissen», «Ihre Rezeption» und «Mit herzlichem Gruss» im Willkommensbrief']
WM = 1425 / 3483   # Höhe : Breite der Wortmarke
BK = 696 / 3483    # Höhe : Breite des Bergkamms


def etk(x, y, text, farbe, gr=1.9, b=None, mehr=''):
    """kleine Zeile: DM Mono, gesperrte Versalien"""
    return t(x, y, e(text.upper()), 'm' + (' c' if b else ''), f'font-size:{gr}mm;letter-spacing:.2em;color:{farbe};{mehr}', b)


def fluss(x, y, b, h, innen, stil='', mitte=True):
    """Block im Fluss an mm-Koordinaten; mitte = senkrecht mittig in seiner Höhe"""
    fl = ('display:flex;flex-direction:column;justify-content:space-between;' if mitte == 'verteilt'
          else 'display:flex;flex-direction:column;justify-content:center;' if mitte else '')
    return f'<div class="abs fl" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;{fl}{stil}">{innen}</div>'


def ti(text, gr, farbe, mehr=''):
    return f'<p style="margin:0;font-family:\'Fjalla One\';font-weight:400;font-size:{gr}mm;line-height:1.08;color:{farbe};text-wrap:balance;{mehr}">{text}</p>'


def la(text, gr, farbe, mehr=''):
    return f'<p style="margin:0;font-family:\'Instrument Sans\';font-size:{gr}mm;line-height:1.45;color:{farbe};text-wrap:pretty;{mehr}">{text}</p>'


def mo(text, gr, farbe, mehr=''):
    return f'<p style="margin:0;font-family:\'DM Mono\';font-size:{gr}mm;line-height:1.4;letter-spacing:.2em;text-transform:uppercase;color:{farbe};{mehr}">{e(text)}</p>'


def zeile(name, preis, satz, farbe, leise, gr=4.4, mehr=''):
    """Gericht: Name links, Preis rechts (DM Mono), darunter der Satz"""
    return (f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:3mm;{mehr}">'
            f'<span style="font-family:\'Fjalla One\';font-size:{gr}mm;line-height:1.15;color:{farbe}">{e(name)}</span>'
            f'<span style="font-family:\'DM Mono\';font-size:{gr * .7:.2f}mm;color:{farbe};white-space:nowrap">{e(preis)}</span></div>'
            + (f'<p style="margin:.8mm 0 0;font-family:\'Instrument Sans\';font-size:{gr * .66:.2f}mm;line-height:1.38;color:{leise}">{e(satz.replace(" ,", ","))}</p>' if satz else ''))


def strich(b, farbe, d=.3, abst='0'):
    return f'<i style="display:block;width:{b}mm;height:{d}mm;background:{farbe};margin:{abst}"></i>'


def fuss(y, b, farbe, text=None):
    text = text or f'{N.NAME} · {N.PLZ_ORT} · {N.TEL}'
    return etk(0, y, text, farbe, 1.55, b, 'letter-spacing:.12em')


# ============================================================ Die Karte am Tisch im Röstihüs (A4 hoch, zwei Seiten)
def wein_zeile(w, s, menge):
    """«Fils Maye | Prestige Silber (wurde von Fabian selber kreiert)» → «Fils Maye · Prestige Silber», Trauben mit Abstand nach dem Komma"""
    kellerei = w.split(' (')[0].replace(' | ', ' · ')
    trauben = re.sub(r',\s*', ', ', s.rstrip(', ')).strip()
    return kellerei, trauben + ' · ' + menge.replace(' ', '\xa0')


def karte():
    v = (kasten(0, 0, 210, 297, f'background:{PAPIER}')
         + hw(105, 11, 44, BLAU)
         + foto('roesti-raum', 0, 34, 210, 62, '50% 46%')
         + grat_deckel(0, 34, 210, 9, PAPIER)
         + etk(0, 106, N.ROESTIHUES + ' · Saas-Almagell', LAERCHE_T, 2, 210)
         + t(0, 112, 'Best of Röstis.', 's c', f'font-size:13mm;line-height:1.05;color:{NACHT}', 210)
         + lin(97, 130, 16, MESSING, .3))
    links, rechts = N.ROESTIS[:6], N.ROESTIS[6:]
    for x, teil in ((20, links), (114, rechts)):
        v += fluss(x, 140, 76, 132 if len(teil) == 6 else 108, ''.join(f'<div>{zeile(n, p, s, NACHT, GRAU, 5)}</div>' for n, s, p in teil), mitte='verteilt')
    v += lin(20, 281, 170, MESSING, .25) + fuss(285, 210, GRAU, 'Preise in Franken · Karte vom 18.11.2024 · ' + N.REGIONAL[:-1])
    # Rückseite: Nacht, Cordon bleus, Dessert, Stübli, Apéro, Wein von Fabian
    r = (kasten(0, 0, 210, 297, f'background:{NACHT}')
         + hz(105, 14, 34, LAERCHE)
         + etk(0, 29, 'Röstihüs · Saas-Almagell', MESSING, 2, 210)
         + t(0, 35, 'Unsere Cordon bleus.', 's c', f'font-size:12mm;line-height:1.05;color:{PAPIER}', 210)
         + fluss(30, 56, 150, 86, ''.join(f'<div>{zeile(n, p, s, PAPIER, WAND, 5)}</div>' for n, s, p in N.CORDON), mitte='verteilt')
         + lin(20, 151, 170, MESSING, .25))
    kopf_n, kopf_s = N.KOPF[0].split(' (')[0], N.KOPF[0].split(' (')[1].rstrip(')')
    spalten = [('Zum Dessert', [(kopf_n, N.KOPF[1], kopf_s)]), ('Im Stübli', [(N.RACLETTE[0].split(' mit ')[0], N.RACLETTE[1], 'mit ' + N.RACLETTE[0].split(' mit ')[1])]),
               ('Zum Apéro', [(n, p, s) for n, s, p in N.SPRITZ])]
    for i, (kopf, posten) in enumerate(spalten):
        x = 20 + i * 59
        r += fluss(x, 159, 52, 44, mo(kopf, 1.9, LAERCHE, 'margin-bottom:3mm') + ''.join(f'<div style="margin-bottom:3mm">{zeile(n, p, s, PAPIER, WAND, 4.3)}</div>' for n, p, s in posten), mitte=False)
    r += (lin(20, 210, 170, MESSING, .25)
          + etk(0, 218, 'Wein von Fabian · selbst kreiert', LAERCHE, 1.9, 210))
    for i, (n, w, s, menge, p) in enumerate(N.HOTELWEINE):
        x = 20 + i * 90
        kel, rest = wein_zeile(w, s, menge)
        r += fluss(x, 226, 80, 30, zeile(n.replace('«Hotelwein» ', ''), p, kel + ' · ' + rest, PAPIER, WAND, 4.6), mitte=False)
    r += (hw(105, 258, 28, PAPIER) + fuss(283, 210, WAND))
    return [blatt(210, 297, v, '', f'background:{PAPIER}'), blatt(210, 297, r, '', f'background:{NACHT}')]


# ============================================================ Aushang «Inklusive» als Bon der Rezeption (A4 hoch)
def aushang():
    bx, bb = 38, 134
    zahn = 30
    zack = ' '.join(f'{bx + i * bb / zahn:.2f},{250 if i % 2 == 0 else 254}' for i in range(zahn + 1))
    bon = (f'<svg class="abs" style="left:0;top:0;width:210mm;height:297mm" viewBox="0 0 210 297"><polygon points="{bx},92 {bx + bb},92 {" ".join(reversed(zack.split()))} {bx},92" fill="{PAPIER}"/></svg>')
    posten = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:3.2mm 0;border-bottom:.25mm dashed {WAND}">'
                     f'<span><span style="display:block;font-family:\'Fjalla One\';font-size:6mm;line-height:1.1;color:{NACHT}">{e(k)}</span>'
                     f'<span style="display:block;font-family:\'Instrument Sans\';font-size:3.3mm;line-height:1.35;color:{GRAU};margin-top:.6mm">{e(s)}</span></span>'
                     f'<span style="font-family:\'DM Mono\';font-size:3.6mm;letter-spacing:.12em;color:{LAERCHE_T}">INKL.</span></div>' for k, s in N.INKL_KURZ)
    inhalt = (mo('Ihr Aufenthalt', 2.2, GRAU, 'text-align:center') + strich(16, MESSING, .3, '3mm auto 3mm') + posten
              + f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding-top:4mm"><span style="font-family:\'Fjalla One\';font-size:7mm;color:{NACHT}">Total</span>'
              f'<span style="font-family:\'DM Mono\';font-size:4.2mm;letter-spacing:.14em;color:{LAERCHE_T}">INKLUSIVE</span></div>')
    v = (kasten(0, 0, 210, 297, f'background:{NACHT}')
         + hz(105, 16, 30, LAERCHE)
         + etk(0, 29, 'Hotel Monte-Moro · Saas-Almagell', MESSING, 2.2, 210)
         + t(0, 36, 'Mehr erleben,<br>weniger zahlen.', 's c', f'font-size:16mm;line-height:1.04;color:{PAPIER}', 210)
         + bon
         + fluss(bx + 12, 96, bb - 24, 152, inhalt, mitte=True)
         + t(0, 264, e(N.AB) + '.', 'c', f'font-size:4.2mm;color:{PAPIER}', 210)
         + etk(0, 276, 'Rezeption · ' + N.TEL, MESSING, 2, 210))
    return [blatt(210, 297, v, '', f'background:{NACHT}')]


# ============================================================ Tischkarte zum Hotelwein (A6 hoch, zwei Seiten)
def hotelwein():
    v = (kasten(0, 0, 105, 148, f'background:{NACHT}')
         + foto('stube-holz', 0, 8, 105, 68, '50% 50%')
         + grat_deckel(0, 8, 105, 7, NACHT)
         + etk(0, 84, 'Im Röstihüs', MESSING, 1.7, 105)
         + t(0, 90, 'Wein von Fabian.', 's c', f'font-size:8.4mm;color:{PAPIER}', 105)
         + lin(46.5, 104, 12, LAERCHE, .3)
         + t(12, 109, 'Zwei Hotelweine, beide von Fabian selbst kreiert.', 'c', f'font-size:3.1mm;line-height:1.45;color:{WAND}', 81)
         + hz(52.5, 132, 18, LAERCHE))
    weine = ''.join(f'<div style="margin-bottom:{11 if i == 0 else 0}mm">'
                    + mo(n.split('» ')[0] + '»', 1.9, LAERCHE_T, 'margin-bottom:2mm')
                    + zeile(n.split('» ')[1], p, '', NACHT, GRAU, 6.6)
                    + la('<br>'.join(e(x) for x in wein_zeile(w, s, menge)), 3.6, GRAU, 'margin-top:1.8mm')
                    + '</div>' for i, (n, w, s, menge, p) in enumerate(N.HOTELWEINE))
    r = (kasten(0, 0, 105, 148, f'background:{PAPIER}')
         + hw(52.5, 11, 30, BLAU)
         + fluss(12, 30, 81, 92, weine)
         + lin(12, 126, 81, MESSING, .25)
         + etk(0, 131, 'Preise in Franken · 7 dl', GRAU, 1.45, 105, 'letter-spacing:.14em'))
    return [blatt(105, 148, v, '', f'background:{NACHT}'), blatt(105, 148, r, '', f'background:{PAPIER}')]


# ============================================================ Aushang Racletteabend im Stübli (A5 hoch)
def raclette():
    v = (kasten(0, 0, 148, 210, f'background:{PAPIER}')
         + foto('stuebli', 0, 12, 148, 94, '50% 55%')
         + grat_deckel(0, 12, 148, 9, PAPIER)
         + etk(0, 6, N.ROESTIHUES, LAERCHE_T, 1.7, 148)
         + etk(0, 114, 'Einmal in der Woche', LAERCHE_T, 2, 148)
         + t(0, 120, 'Racletteabend<br>im Stübli.', 's c', f'font-size:11.5mm;line-height:1.04;color:{NACHT}', 148)
         + lin(66, 147, 16, MESSING, .3)
         + t(20, 153, 'Einmal in der Woche ist im Stübli Racletteabend für alle mit Halbpension.', 'c', f'font-size:4mm;line-height:1.45;color:{TINTE}', 108)
         + t(20, 171, 'Auf der Karte des Röstihüs: ' + e(N.RACLETTE[0]) + ', Fr.\xa0' + e(N.RACLETTE[1]), 'c', f'font-size:3.1mm;line-height:1.45;color:{GRAU}', 108)
         + hz(74, 187, 16, LAERCHE)
         + fuss(197, 148, GRAU, N.ROESTIHUES + ' · ' + N.NAME))
    return [blatt(148, 210, v, '', f'background:{PAPIER}')]


# ============================================================ Karte zum Kidsclub (A6 quer, zwei Seiten)
def kidsclub():
    v = (kasten(0, 0, 148, 105, f'background:{NACHT}')
         + hz(74, 13, 26, LAERCHE)
         + etk(0, 25, 'Für unsere kleinsten Gäste', MESSING, 1.8, 148)
         + t(0, 31, 'Kidsclub.', 's c', f'font-size:15mm;color:{PAPIER}', 148)
         + lin(66, 54, 16, LAERCHE, .3)
         + t(0, 60, 'Montag bis Samstag', 'c', f'font-size:4.4mm;color:{PAPIER}', 148)
         + t(0, 67, '16:30 bis 21:00 Uhr', 's c', f'font-size:7.2mm;color:{PAPIER}', 148)
         + etk(0, 86, 'Im Zimmerpreis inklusive', MESSING, 1.7, 148))
    r = (kasten(0, 0, 148, 105, f'background:{PAPIER}')
         + foto('spielburg', 0, 0, 62, 105, '50% 62%')
         + fluss(72, 10, 66, 85, mo(N.NAME, 1.6, LAERCHE_T, 'margin-bottom:3mm') + ti('Die Spielburg vor dem Haus.', 6.4, NACHT, 'margin-bottom:3mm')
                 + strich(10, MESSING, .3, '0 0 3mm') + la(e(N.D.ROESTI_KINDER), 3.1, TINTE, 'margin-bottom:3mm')
                 + la('Kidsclub täglich von Montag bis Samstag, 16:30 bis 21:00 Uhr.', 3.1, GRAU)))
    return [blatt(148, 105, v, '', f'background:{NACHT}'), blatt(148, 105, r, '', f'background:{PAPIER}')]


# ============================================================ Willkommensbrief im Zimmer (A5 hoch)
def willkommen():
    gut = [('Frühstück', 'Das Frühstücksbuffet ist für alle Gäste gedeckt.'),
           ('Röstihüs', 'Elf Röstis, die Cordon bleus und der Wein von Fabian, bei schönem Wetter auf der Sonnenterrasse vor dem Haus.'),
           ('Saastal', 'Postauto im ganzen Saastal inklusive, im Sommer auch alle Bergbahnen ausser der Metro Alpin.'),
           ('Spa', 'Im Partnerhotel Pirmin Zurbriggen, pro Person und Eintritt CHF 25.00, Bademantel und Handtücher stehen bereit.'),
           ('Kidsclub', 'Montag bis Samstag, 16:30 bis 21:00 Uhr.')]
    assert 'CHF 25.00' == N.D.SPA_TARIFE[0][1]
    liste = ''.join(f'<div style="display:grid;grid-template-columns:22mm 1fr;gap:3mm;padding:2.4mm 0;border-top:.25mm solid {WAND}">'
                    f'<span style="font-family:\'DM Mono\';font-size:1.8mm;letter-spacing:.2em;text-transform:uppercase;color:{LAERCHE_T};padding-top:.7mm">{e(k)}</span>'
                    f'<span style="font-family:\'Instrument Sans\';font-size:3.05mm;line-height:1.42;color:{TINTE}">{e(s)}</span></div>' for k, s in gut)
    v = (kasten(0, 0, 148, 210, f'background:{PAPIER}')
         + hw(74, 12, 34, BLAU)
         + etk(0, 32, 'Im Zimmer', LAERCHE_T, 1.8, 148)
         + t(0, 37, 'Willkommen<br>im Monte-Moro.', 's c', f'font-size:10mm;line-height:1.05;color:{NACHT}', 148)
         + lin(66, 61, 16, MESSING, .3)
         + t(18, 66, 'Schön, dass Sie da sind. Das Hotel liegt an bester Lage in Saas-Almagell: zwei Gehminuten zum Skigebiet, drei zur Busstation und drei ins Dorf. '
                     'Und bei uns scheint fast immer die Sonne.', 'c', f'font-size:3.35mm;line-height:1.5;color:{TINTE}', 112)
         + fluss(18, 92, 112, 82, mo('Gut zu wissen', 1.8, GRAU, 'margin-bottom:2mm') + '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-between">' + liste + '</div>', mitte=False, stil='display:flex;flex-direction:column')
         + t(18, 180, 'Mit herzlichem Gruss', '', f'font-size:3.1mm;color:{GRAU}', 112)
         + t(18, 185, e(N.GASTGEBER), 's', f'font-size:5.4mm;color:{NACHT}', 112)
         + etk(18, 197, 'Ihre Rezeption · ' + N.TEL, LAERCHE_T, 1.55, None, 'letter-spacing:.12em')
         + hz(124, 196, 12, LAERCHE, False))
    return [blatt(148, 210, v, '', f'background:{PAPIER}')]


# ============================================================ Briefbogen A4 und Umschlag DIN lang
def briefpapier():
    bogen = (hw(22, 15, 40, BLAU, False)
             + t(110, 17, e(N.NAME) + '<br>' + e(N.PLZ_ORT) + '<br>' + e(N.TEL) + '<br>' + e(N.MAIL), '', f'font-size:2.55mm;line-height:1.55;color:{TINTE};text-align:right', 78)
             + grat_linie(22, 36, 166, 5, MESSING, .25)
             + lin(4, 105, 5, 'rgba(19,38,58,.45)', .15) + lin(4, 210, 5, 'rgba(19,38,58,.45)', .15)
             + lin(22, 273, 166, MESSING, .25)
             + hz(105, 277, 12, LAERCHE)
             + etk(0, 284.5, f'{N.NAME} · {N.PLZ_ORT} · Tel. {N.TEL} · Fax {N.FAX} · {N.MAIL}', GRAU, 1.5, 210, 'letter-spacing:.08em'))
    umschlag = (kasten(0, 0, 220, 110, f'background:{NACHT}')
                + hw(14, 12, 40, PAPIER, False)
                + etk(14, 34, N.SEIT, MESSING, 1.7) + t(14, 39, e(N.PLZ_ORT) + ' · ' + e(N.TEL), '', f'font-size:2.6mm;color:{WAND}')
                + f'<i class="abs" style="left:118mm;top:52mm;width:90mm;height:44mm;background:{PAPIER};border-radius:1mm"></i>')
    return [blatt(210, 297, bogen, '', f'background:{PAPIER}'), blatt(220, 110, umschlag, '', f'background:{NACHT}')]


def untersetzer_alle():
    import untersetzer_neu
    return untersetzer_neu.alle()


# ============================================================ Drucksachen der Hausdruckerei (nur kopiert)
FREMD = re.compile(r'wild\s*side|wildside|negroni|session|culinarium|hannover|linden|momo|rudi|derya|cocktail', re.I)


def hausdruckerei():
    """liste.json bzw. LISTE.md der Hausdruckerei → drucksachen/img/*.webp, drucksachen/pdf/*.pdf, _werkbank/papier_mehr.json.
    Übernommen wird nur, was sicher vom Monte-Moro ist (kein Wort eines anderen Hauses in der Liste)."""
    ziel_json = os.path.join(ROOT, '_werkbank', 'papier_mehr.json')
    img = os.path.join(ROOT, 'drucksachen', 'img'); pdf = os.path.join(ROOT, 'drucksachen', 'pdf')
    os.makedirs(img, exist_ok=True); os.makedirs(pdf, exist_ok=True)
    for f in os.listdir(img):   # alte Übernahmen weg
        if f.startswith('pw-'):
            os.remove(os.path.join(img, f))
    for f in os.listdir(pdf):
        if f.startswith(f'{H.KURZ}-pw-'):
            os.remove(os.path.join(pdf, f))
    mehr = []
    lj = os.path.join(PW, 'liste.json')
    roh = open(lj, encoding='utf-8').read() if os.path.exists(lj) else ''
    if roh and not FREMD.search(roh):
        for d in json.loads(roh):
            k = d['k']
            namen = []
            for j, v in enumerate(d.get('vorschau', [])):
                nm = 'pw-' + k + ('' if j == 0 else f'-{j + 1}')
                im = Image.open(os.path.join(PW, v)).convert('RGB')
                if im.width > 1000:
                    im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
                im.save(os.path.join(img, nm + '.webp'), 'WEBP', quality=86, method=5)
                os.makedirs(os.path.join(ROOT, '_werkbank', 'roh', 'papier'), exist_ok=True)
                im.save(os.path.join(ROOT, '_werkbank', 'roh', 'papier', nm + '.png'))
                namen.append((nm, im.size))
            if not namen or not os.path.exists(os.path.join(PW, d['pdf'])):
                continue
            ziel = f'{H.KURZ}-pw-{k}.pdf'
            shutil.copy2(os.path.join(PW, d['pdf']), os.path.join(pdf, ziel))
            hoch = namen[0][1][1] > namen[0][1][0]
            if len(namen) >= 2:
                w = 44 if hoch else 84
                karton = [(namen[0][0], w, 'Vorderseite'), (namen[1][0], w, 'Rückseite')]
            else:
                r = namen[0][1][1] / namen[0][1][0]
                w = 40 if r > 1.6 else (54 if r > 1.3 else (64 if r > 1.05 else 86))
                karton = [(namen[0][0], w, '')]
            n = d.get('n', k)
            teile = n.rsplit(' ', 1)
            titel = [teile[0], teile[1] + ('' if teile[1].endswith(('.', '!', '?', '»')) else '.')] if len(teile) == 2 else ['', n]
            mehr.append(dict(id='pw-' + k, name=n, format=d.get('format', '') + (f' · {d["seiten"]} Seiten' if d.get('seiten', 1) > 1 else '') + ' · aus ' + mit_papier.fall(mit_papier.werkzeugnamen().get('druck', 'Die Hausdruckerei'), 'klein').replace('die ', 'der ', 1),
                             satz=d.get('was', ''), titel=titel, pdf=ziel, karton=karton[:2], masse={a: list(s) for a, s in namen},
                             schatten=True, haengt=False, seiten=d.get('seiten', 1)))
    json.dump({'druck': mehr}, open(ziel_json, 'w'), ensure_ascii=False, indent=1)
    return mehr


SEITE_NEU = {   # Karton, Titel und Breite der eigenen Stücke (haus.py › PAPIER_SEITE liest papier_neu_seite.json; mit_papier.py ebenso)
    'karte': dict(karton=['', [['karte', 44, 'Vorderseite'], ['karte-r', 44, 'Rückseite']]], titel=['Die Karte', 'am Tisch.'], breit=['karte', 'karte-r']),
    'aushang': dict(karton=['', [['aushang', 52, '']]], titel=['Alles', 'schon dabei.'], breit=['aushang']),
    'hotelwein': dict(karton=['', [['hotelwein', 40, 'Vorderseite'], ['hotelwein-r', 40, 'Rückseite']]], titel=['Wein', 'von Fabian.'], breit=[]),
    'raclette': dict(karton=['', [['raclette', 50, '']]], titel=['Racletteabend', 'im Stübli.'], breit=['raclette']),
    'kidsclub': dict(karton=['', [['kidsclub', 70, 'Vorderseite'], ['kidsclub-r', 70, 'Rückseite']]], titel=['Der', 'Kidsclub.'], breit=['kidsclub', 'kidsclub-r']),
    'willkommen': dict(karton=['', [['willkommen', 52, '']]], titel=['Willkommen', 'im Zimmer.'], breit=['willkommen']),
    'briefpapier': dict(karton=['', [['umschlag', 92, 'Umschlag'], ['briefbogen', 38, 'Briefbogen']]], titel=['Briefbogen', 'und Umschlag.'], breit=['briefbogen', 'umschlag']),
}


# eigene Fassung → Stücke der Hausdruckerei, die dieselbe Idee sind (dann fällt die eigene weg)
GEGENSTUECK = {'karte': ['pw-roestihues-best-of-roestis', 'pw-roestihues-auszug'], 'aushang': ['pw-aushang-inklusive', 'pw-plakat-inklusive-a3'],
               'hotelwein': ['pw-tischkarte-hotelwein', 'pw-roestihues-wein-von-fabian'], 'raclette': ['pw-aushang-racletteabend'],
               'kidsclub': ['pw-aushang-kidsclub', 'pw-story-kidsclub'], 'willkommen': ['pw-willkommensbrief'], 'briefpapier': ['pw-briefpapier-a4']}


def css_umstellen():
    """Satz-CSS: feste Schnitte von Fjalla One, Instrument Sans und DM Mono; Titel und Lauf in der Schrift des Hauses."""
    p = os.path.join(ROOT, '_werkbank', 'satz', 'papier.css')
    css = druckschrift.umstellen(open(p, encoding='utf-8').read())
    marke = '/* Monte-Moro: feste Schnitte */'
    if marke in css:
        css = css[:css.index(marke)]
    css += ('\n' + marke + '\n' + druckschrift.FACES
            + ".t{font-family:'Instrument Sans',Arial,sans-serif}.t.s{font-family:'Fjalla One',sans-serif;font-weight:400;line-height:1.08}"
            ".t.m{font-family:'DM Mono',monospace;font-weight:400}.blatt{color:" + TINTE + "}.fl p{margin:0}\n")
    open(p, 'w', encoding='utf-8').write(css)


def baue():
    Dr = []

    def d(ident, name, format_, blaetter, vorschau, satz, quelle):
        Dr.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=vorschau, satz=satz, quelle=quelle))
    d('karte', 'Die Karte am Tisch', 'A4 hoch, zwei Seiten', karte(), [('karte', 1), ('karte-r', 2)],
      'Vorne die elf Röstis, hinten die Cordon bleus, der Monte-Moro-Kopf, die Spritz zum Apéro, das Raclette im Stübli und die zwei Hotelweine von Fabian. Jede Zeile und jeder Preis aus der Karte des Röstihüs.',
      'Karte des Röstihüs vom 18.11.2024, Seite «Röstihüs» der Website')
    d('aushang', 'Aushang «Inklusive»', 'A4 hoch, für die Rezeption', aushang(), [('aushang', 1)],
      'Der Bon der Rezeption als Aushang: Postauto, Bergbahnen, Frühstück, Raclette, Kidsclub und Parkplatz, alles im Zimmerpreis. Darüber der Satz des Hauses, gross genug für den Blick im Vorbeigehen.',
      'Preisliste und «Inklusive» der Website')
    d('hotelwein', 'Tischkarte zum Hotelwein', 'A6 hoch, zwei Seiten', hotelwein(), [('hotelwein', 1), ('hotelwein-r', 2)],
      'Steht auf den Tischen im Röstihüs: vorne die Stube, hinten die zwei Hotelweine, die Fabian selbst kreiert hat, mit Kellerei, Trauben und Preis.',
      'Karte des Röstihüs, «Wein von Fabian»')
    d('raclette', 'Aushang Racletteabend', 'A5 hoch', raclette(), [('raclette', 1)],
      'Für das Brett im Stübli und den Eingang zum Röstihüs: einmal in der Woche Racletteabend für alle mit Halbpension.',
      'Seite «Röstihüs» und «Inklusive» der Website')
    d('kidsclub', 'Karte zum Kidsclub', 'A6 quer, zwei Seiten', kidsclub(), [('kidsclub', 1), ('kidsclub-r', 2)],
      'Für die Rezeption und die Familienzimmer: wann der Kidsclub da ist, dazu die Spielburg vor dem Haus und die kleine Karte für die kleinsten Gäste.',
      '«Inklusive» der Website, Seite «Röstihüs»')
    d('willkommen', 'Willkommensbrief im Zimmer', 'A5 hoch', willkommen(), [('willkommen', 1)],
      'Liegt auf dem Kissen, wenn Sie ankommen: ein paar Zeilen von Esther und Fabian, und was man im Haus und im Tal gleich wissen möchte.',
      'Startseite, Preise, Spa und Röstihüs der Website')
    d('briefpapier', 'Briefbogen und Umschlag', 'Briefbogen A4, Umschlag DIN lang', briefpapier(), [('briefbogen', 1), ('umschlag', 2)],
      'Für Bestätigungen, Angebote und Dankesbriefe: der Briefbogen auf Papier mit der Wortmarke in Logo-Blau und der Gratlinie, der Umschlag in der Nacht des Hauses.',
      'Wortmarke und Fuss der Website')
    # Keine Idee doppelt (Kriterium 15, Oberchef 08.11.2026): hat die Hausdruckerei ein Gegenstück, fällt die eigene Fassung weg.
    mehr = hausdruckerei()
    da = {x['id'] for x in mehr}
    weg = {k for k, ersatz in GEGENSTUECK.items() if any(e in da for e in ersatz)}
    Dr[:] = [x for x in Dr if x['id'] not in weg]
    json.dump({k: v for k, v in SEITE_NEU.items() if k not in weg}, open(os.path.join(ROOT, '_werkbank', 'papier_neu_seite.json'), 'w'), ensure_ascii=False, indent=1)
    P.fertig(Dr, untersetzer_alle(), MEINS)
    css_umstellen()
    N.satz_namen('papier.css', 'etiketten.html', 'etiketten-bogen.html', *[x['id'] + '.html' for x in Dr])
    ids = {x['id'] + '.html' for x in Dr}
    for f in os.listdir(P.SATZ):   # Satzdateien anderer Häuser weg (nicht: Sticker, Beigaben, Postkarten, Etiketten)
        if f.endswith('.html') and f not in ids and not f.startswith(('etiketten', 'sticker', 'beigabe-', 'postkarten')):
            os.remove(os.path.join(P.SATZ, f))
    print('Eigene Drucksachen:', len(Dr), '· aus der Hausdruckerei:', len(mehr), '· weggelassen, weil die Hausdruckerei sie hat:', ', '.join(sorted(weg)) or '–')


if __name__ == '__main__':
    baue()
