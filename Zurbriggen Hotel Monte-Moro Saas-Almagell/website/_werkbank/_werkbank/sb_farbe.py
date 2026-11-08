#!/usr/bin/env python3
"""Werkbank Monte-Moro: letzter Farbgang (Werkbank Kern, 08.11.2026). Jede fremde Farbe der Bausteine, die noch in den gebauten Seiten steht,
wird auf die Töne des Hauses umgerechnet (website/assets/css/montemoro.css): dunkel wird Nacht, die warme Mitte Lärche, hell Papier und Fassade.
Helligkeit bleibt. Fotos werden nicht angefasst, nur Text in CSS und HTML. Mehrfach anwendbar."""
import colorsys, glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
# Töne des Hauses: Nacht #0A2A4A, Nachtblau #0D3F6F, Tiefnacht #071B2E, Logo-Blau #115595, Lärche #C67144, Lärche tief #9A4F2B, Messing #B39867,
# Papier #F5F2EE, Fassade #E7E1DC, Creme #EFE9E1, Wandschatten #D6CCC1, Tinte #13263A, Grau #4A5D70.
FEST = {
    # Töne der Vorlagen, fest zugeordnet
    '#130e0d': '#0a2a4a', '#1c1513': '#082339', '#261e1a': '#0d3f6f', '#33281f': '#115595', '#f2e9dc': '#f5f2ee', '#e7dccb': '#e7e1dc', '#f7f1e7': '#f5f2ee',
    '#d8b264': '#c67144', '#a07f3a': '#9a4f2b', '#b08a43': '#b39867', '#f0323f': '#c67144', '#1b1512': '#13263a', '#6e5d4e': '#4a5d70', '#e7cf98': '#e6b394',
    '#d9cbb6': '#d6ccc1', '#ede4d8': '#efe9e1', '#fbf5ea': '#f5f2ee', '#fbf6ea': '#f5f2ee', '#dcc68f': '#c67144', '#c2a560': '#c67144', '#b78f51': '#c67144',
    '#fd9964': '#c67144', '#e8875a': '#c67144', '#fec7aa': '#e6b394', '#c42e13': '#9a4f2b', '#a8260f': '#9a4f2b', '#e0a96a': '#c67144', '#7d433a': '#0d3f6f',
    '#ef7649': '#c67144', '#f5a689': '#e6b394', '#b15736': '#9a4f2b', '#16151a': '#0a2a4a', '#16141b': '#0a2a4a', '#3a3845': '#0d3f6f', '#faf4f4': '#f5f2ee', '#8953a9': '#c67144',
    '#f3d49a': '#e6b394', '#dcae66': '#c67144', '#b98443': '#9a4f2b', '#9a672b': '#9a4f2b', '#8a6f35': '#9a4f2b', '#e6007e': '#c67144',
}
HAUS = {(0x0a, 0x2a, 0x4a), (0x0d, 0x3f, 0x6f), (0x07, 0x1b, 0x2e), (0x08, 0x23, 0x39), (0x11, 0x55, 0x95), (0xc6, 0x71, 0x44), (0x9a, 0x4f, 0x2b), (0xb3, 0x98, 0x67),
        (0xf5, 0xf2, 0xee), (0xe7, 0xe1, 0xdc), (0xef, 0xe9, 0xe1), (0xd6, 0xcc, 0xc1), (0x13, 0x26, 0x3a), (0x4a, 0x5d, 0x70), (0xe6, 0xb3, 0x94), (0xd3, 0x84, 0x5a), (0xae, 0x5e, 0x34), (0x15, 0x46, 0x6f)}


def _ton(r, g, b):
    if (r, g, b) in HAUS:
        return r, g, b
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if s < .1 or l > .985 or l < .02:
        return r, g, b
    if l < .42:          # dunkel: Nacht (Blau des Logos)
        nh, ns = 210 / 360, .72
    elif l < .84:        # warme Mitte: Lärche; kühle Mitte: Logo-Blau
        if 150 / 360 < h < 260 / 360:
            nh, ns = 209 / 360, .7
        else:
            nh, ns = 21 / 360, .54
    else:                # hell: Papier und Fassade
        nh, ns = 30 / 360, .3
    nr, ng, nb = colorsys.hls_to_rgb(nh, l, ns)
    return round(nr * 255), round(ng * 255), round(nb * 255)


_blau = _ton


def faerbe(t):
    def hexf(m):
        x = m.group(1)
        if len(x) == 3:
            x = ''.join(c * 2 for c in x)
        if len(x) != 6:
            return m.group(0)
        k = '#' + x.lower()
        if k in FEST:
            return FEST[k]
        return '#%02x%02x%02x' % _blau(*(int(x[i:i + 2], 16) for i in (0, 2, 4)))
    t = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![0-9a-fA-F-])', hexf, t)
    # Goldlinien der Vorlage werden Messing (feine Linien), sonst wird jede Farbe in rgba() auf die Töne gerechnet
    t = re.sub(r'rgba\(\s*(?:216\s*,\s*178\s*,\s*100|220\s*,\s*198\s*,\s*143|183\s*,\s*143\s*,\s*81|150\s*,\s*125\s*,\s*64|176\s*,\s*138\s*,\s*67)\s*,', 'rgba(179,152,103,', t)
    t = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', lambda m: '%s(%d,%d,%d' % ((m.group(1),) + _blau(int(m.group(2)), int(m.group(3)), int(m.group(4)))), t)
    return t


def nur_style(t):
    """In HTML nur <style>-Blöcke und style=""-Werte umrechnen, nie Text, Adressen oder eingebettete Bilder."""
    t = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t, flags=re.S)
    t = re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t)
    t = re.sub(r'(<meta name="theme-color" content=")(#[0-9a-fA-F]{6})', lambda m: m.group(1) + faerbe(m.group(2)), t)
    t = re.sub(r'(<svg\b.*?</svg>)', lambda m: faerbe(m.group(1)) if 'data:image' not in m.group(1) else m.group(1), t, flags=re.S)
    return t


def ohne_fett(t):
    """Nie fett (Tasty-Sprache Stufe 2 Nr. 8): kräftige Schnitte werden Medium, Titel bleiben Regular."""
    t = re.sub(r'font-weight:\s*(?:600|700|800|900|bold)\b', 'font-weight:500', t)
    return re.sub(r'(font:\s*)(?:600|700|800|900|bold)\b', r'\g<1>500', t)


def anwenden():
    n = 0
    for p in glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.css'), recursive=True):
        a = open(p, encoding='utf-8').read(); b = ohne_fett(faerbe(a))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    seiten = (glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.html'), recursive=True)
              + [os.path.join(ROOT, d, 'index.html') for d in ('befund',)])   # nur das eigene Revier (die Papier-Seiten baut Werkbank Papier)
    for p in seiten:
        if not os.path.exists(p):
            continue
        a = open(p, encoding='utf-8').read(); b = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + ohne_fett(m.group(2)) + m.group(3), nur_style(a), flags=re.S)
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


if __name__ == '__main__':
    print('umgefärbt:', anwenden(), 'Dateien')
