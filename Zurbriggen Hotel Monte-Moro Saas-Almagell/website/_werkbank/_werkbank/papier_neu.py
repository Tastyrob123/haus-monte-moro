#!/usr/bin/env python3
"""Hotel Monte-Moro: gemeinsame Bausteine für Papier, Untersetzer, Sticker, Postkarten und Beigaben (Werkbank Papier, 08.11.2026;
Bauart wie papier_neu.py der Vorlage, Inhalt und Kleid des Hauses).
Farben aus dem Markenbuch und website/assets/css/montemoro.css (:root): Nacht, Nachtblau, Tiefnacht, Logo-Blau, Lärche, Lärche tief,
Messing (nur feine Linien), Papier, Fassade, Creme, Wandschatten, Tinte, Grau. Schrift: Fjalla One (Titel), Instrument Sans (Lauf),
DM Mono gesperrt in Versalien (kleine Zeilen, Zahlen). Zeichen: der Bergkamm, Wortmarke: das ganze Logo (beides aus dem Kleid, über haus.py).
Form: die Grat-Kante (Bergkamm-Linie der Website, --grat-maske) als Oberkante von Fotos.
Hauswerte nur aus website/inhalt/daten.py (gelesen, nie abgetippt); was in OFFEN steht, kommt nicht vor; die Gratis-Anreise ist abgelaufen."""
import html as _h
import os
import re
import sys
from kern import ROOT

WEB = os.path.dirname(ROOT)
IMG = os.path.join(WEB, 'assets', 'img')
sys.path.insert(0, os.path.join(WEB, 'inhalt'))
import daten as D  # noqa: E402  (website/inhalt/daten.py, nur gelesen)

# Farben (Markenbuch, montemoro.css :root)
NACHT, NACHTBLAU, TIEFNACHT, BLAU = '#0A2A4A', '#0D3F6F', '#071B2E', '#115595'
LAERCHE, LAERCHE_T, MESSING = '#C67144', '#9A4F2B', '#B39867'
PAPIER, FASSADE, CREME, WAND = '#F5F2EE', '#E7E1DC', '#EFE9E1', '#D6CCC1'
TINTE, GRAU = '#13263A', '#4A5D70'
LEISE = GRAU

FJ, IS, DM = "'Fjalla One'", "'Instrument Sans'", "'DM Mono'"

# ---------------------------------------------------------------- Hauswerte (website/inhalt/daten.py)
NAME = D.HAUS['name']                       # Hotel Monte-Moro
ORT = D.HAUS['ort']                         # Saas-Almagell
PLZ_ORT = D.HAUS['plz_ort']                 # CH-3905 Saas-Almagell
TEL = D.HAUS['tel']
FAX = D.HAUS['fax']
MAIL = D.HAUS['mail']
GASTGEBER = 'Esther und Fabian Zurbriggen'
GASTGEBER_KURZ = 'Esther & Fabian'
SATZ = D.HAUS['satz']                       # Mehr erleben, weniger zahlen.
TRADITION = D.TRADITION                     # Es lebe die Tradition!
SONNE_KURZ = 'Bei uns scheint fast immer die Sonne.'          # Fuss jeder Seite der Website
MORGEN = 'Und morgen scheint die Sonne wieder.'                # anreise.html
SEIT = 'Familie Zurbriggen · seit 1967'                        # Fuss der Website
WILLKOMMEN = 'Willkommen im Monte-Moro.'                       # anreise.html
REGIONAL = 'Regional und herzlich.'                            # roestihues.html
DABEI = 'Alles schon dabei.'                                   # preise.html
LIFT = 'Zwei Minuten bis zum Lift.'                            # index.html, preise.html
ROESTIHUES = 'Restaurant Röstihüs'
ROESTIS, CORDON, HOTELWEINE, SPRITZ, KOPF, RACLETTE = D.ROESTIS, D.CORDON, D.HOTELWEINE, D.SPRITZ, D.KOPF, D.RACLETTE
PREISE, INKLUSIVE, ZUSCHLAEGE, KINDER = D.PREISE, D.INKLUSIVE, D.ZUSCHLAEGE, D.KINDER
ROESTI_SATZ, ROESTI_LUST, RESTAURANT = D.ROESTI_SATZ, D.ROESTI_LUST, D.RESTAURANT
EURO = D.EURO
AB = 'Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag'
INKL_KURZ = [('Postauto', 'Im ganzen Saastal, Sommer und Winter'), ('Bergbahnen', 'Alle im Saastal ausser Metro Alpin, im Sommer'),
             ('Frühstück', 'Frühstücksbuffet'), ('Raclette', 'Wöchentlicher Racletteabend mit Halbpension'),
             ('Kidsclub', 'Montag bis Samstag 16:30 bis 21:00 Uhr'), ('Parkplatz', 'Hotelparkplatz')]
for _k, _v in INKL_KURZ:   # jede Zeile hat ihre Vorlage in INKLUSIVE
    assert any(_k.lower() in i.lower() or (_k == 'Parkplatz' and 'parkplatz' in i.lower()) for i in INKLUSIVE), _k
assert '16:30' in INKLUSIVE[4] and '21:00' in INKLUSIVE[4]
WEG = [('Visp', 'Zug bis hier, dann Postauto'), ('Stalden', 'Verzweigung Richtung Saastal'), ('Saas-Grund', 'umsteigen'), ('Saas-Almagell', 'drei Gehminuten zum Hotel')]

_Z = os.path.relpath(os.path.join(ROOT, 'werkbank', 'eigen'), os.path.join(ROOT, '_werkbank', 'satz'))
TAPETE = ''   # das Haus hat keine Tapete auf Drucksachen; die Fläche bleibt ruhig


def e(s):
    return _h.escape(s, quote=True)


def erster(s, n=1):
    teile = re.split(r'(?<=[.!?])\s+', s)
    return ' '.join(teile[:n])


def preis(p):
    """«25.–» → «25.–», «90.00» bleibt"""
    return p


def bild(key, art='x'):
    """grösste Fassung eines Fotos der Website (assets/img/<key>-<s|m|l|x>.webp)"""
    for a in (art, 'x', 'l', 'm', 's'):
        p = os.path.join(IMG, f'{key}-{a}.webp')
        if os.path.exists(p):
            return p
    raise FileNotFoundError(key)


def bild_satz(key, art='l'):
    """Adresse eines Fotos aus Sicht der Satzdateien (_werkbank/satz/*.html; assets ist im Projekt ein Verweis auf die Website)"""
    return '../../assets/img/' + os.path.basename(bild(key, art))


# ---------------------------------------------------------------- Grat-Kante (montemoro.css › --grat-maske, viewBox 1000 × 60)
GRAT = [(0, 38), (70, 30), (118, 6), (150, 26), (196, 14), (250, 40), (300, 22), (338, 34), (380, 8), (430, 36), (486, 18), (540, 42),
        (600, 28), (640, 36), (700, 12), (748, 32), (800, 24), (860, 44), (920, 20), (962, 34), (1000, 26)]


def grat_punkte(x, y, b, h):
    """die Gratlinie in mm: x, y = linke obere Ecke des Streifens, b Breite, h Höhe des Streifens"""
    return [(x + px / 1000 * b, y + py / 60 * h) for px, py in GRAT]


def grat_deckel(x, y, b, h, farbe):
    """Fläche über der Gratlinie in der Farbe des Grundes: legt sich über die Oberkante eines Fotos (SVG in mm, HTML-Satz)."""
    pk = grat_punkte(0, 0, b, h)
    d = 'M0 0H' + f'{b}' + 'V' + f'{pk[-1][1]:.2f}' + ''.join(f'L{px:.2f} {py:.2f}' for px, py in reversed(pk)) + 'Z'
    return (f'<svg class="abs" style="left:{x}mm;top:{y - .2}mm;width:{b}mm;height:{h + .2}mm;overflow:visible" viewBox="0 -.2 {b} {h + .2}">'
            f'<path d="M0 -.2H{b}V0H0Z" fill="{farbe}"/><path d="{d}" fill="{farbe}"/></svg>')


def grat_linie(x, y, b, h, farbe, d=.3):
    """die Gratlinie als feiner Strich (SVG in mm)"""
    pk = grat_punkte(0, 0, b, h)
    return (f'<svg class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;overflow:visible" viewBox="0 0 {b} {h}">'
            f'<polyline points="{" ".join(f"{px:.2f},{py:.2f}" for px, py in pk)}" fill="none" stroke="{farbe}" stroke-width="{d}" stroke-linejoin="round"/></svg>')


def grat_pfad(x, y, b, h):
    """Pfad (SVG-Koordinaten) einer Fläche mit Grat-Oberkante: oben der Grat, unten gerade (für clipPath in Etiketten)"""
    pk = grat_punkte(x, y, b, h)
    return 'M' + ' L'.join(f'{px:.2f} {py:.2f}' for px, py in pk)


# Nachbauten echter Plakate zeigt die Werkbank nicht (Robert 1.11.2026); beim Hotel gibt es keine.
PLAKAT_NACHBAU = set()


def satz_namen(*namen):
    """Satzdateien: Familien anderer Häuser heissen wie die Schrift des Hauses (Fjalla One, Instrument Sans, DM Mono)."""
    from kern import W
    import druckschrift
    for n in namen:
        p = os.path.join(W, 'satz', n)
        if not os.path.exists(p):
            continue
        t = open(p, encoding='utf-8').read()
        u = druckschrift.umstellen(t)
        if u != t:
            open(p, 'w', encoding='utf-8').write(u)


def stuecke(*_):
    return [], {}
