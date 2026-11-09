"""Keine Lese-Schrift unter 13 px auf den Oberflächen der Werkbank (Robert 09.11.2026, Prüfpunkt 17).

Zuletzt nach jedem Bau (haus.nach_bau, papier_alles.sh, bau_alles.sh): jede Schriftgrösse in den
Stilblättern, <style>-Blöcken, style-Attributen und Skript-Texten der vierzehn Oberflächen, die unter
13 px liegen kann, wird auf mindestens 13 px gehoben:
  11px            -> 13px
  .8rem / .7em    -> max(13px,.8rem)
  clamp(10px,…)   -> clamp(13px,…)   (auch die Obergrenze, wenn sie darunter liegt)
  min(…), vw, var -> max(13px,…)
Kurzschrift «font: 400 11px/1.3 …» ebenso. 0 und 1px (versteckter Text) bleiben. Nicht angefasst:
die Mails selbst (mails/0x-*/, material/10 Mails), die Druckvorlagen des Feeds (feed/_*.html) und alles
in _werkbank/. Mehrfach anwendbar (was schon max(13px,…) ist, bleibt).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN = 13.0
DATEIEN = [
    'werkbank/werkbank.css', 'werkbank/kapitel.css', 'werkbank/seiten.css', 'werkbank/werkbank.js',
    'feed/uebergang.css', 'feed/uebergang.js', 'unterlagen/unterlagen.js',
    'werkbank/index.html', 'werkbank/ki.html', 'werkbank/karte.html', 'werkbank/impressum.html', 'werkbank/geprueft/index.html',
    'befund/index.html', 'unterlagen/index.html', 'drucksachen/index.html', 'untersetzer/index.html', 'sticker/index.html',
    'postkarten/index.html', 'beigaben/index.html', 'feed/index.html', 'mails/index.html', 'material/index.html',
]
ZAHL = re.compile(r'^(\d*\.?\d+)(px|rem|em|%)$')


def _px(t):
    """Grösse in px, wenn statisch bestimmbar (rem/em mit 16 px), sonst None."""
    m = ZAHL.match(t.strip())
    if not m:
        return None
    n, u = float(m.group(1)), m.group(2)
    return n if u == 'px' else n * 16 if u in ('rem', 'em') else n * 0.16


def _teile(s):
    """Argumente einer Funktion auf oberster Ebene."""
    out, tief, cur = [], 0, ''
    for c in s:
        if c == ',' and tief == 0:
            out.append(cur); cur = ''
            continue
        tief += c == '('
        tief -= c == ')'
        cur += c
    out.append(cur)
    return out


def groesse(v):
    """Neuer Wert für eine Schriftgrösse oder None (bleibt)."""
    w = v.strip()
    if not w or w.startswith('max(13px') or w in ('inherit', 'initial', 'unset', 'revert', 'medium', 'large', 'larger', 'x-large', 'xx-large'):
        return None
    m = ZAHL.match(w)
    if m:
        n, u = float(m.group(1)), m.group(2)
        if u == 'px':
            return None if n >= MIN or n <= 1 else '13px'
        if n == 0:
            return None
        if u == 'rem':
            return None if n * 16 >= MIN else f'max(13px,{w})'
        if u == 'em':
            return None if n >= 1 else f'max(13px,{w})'
        return None if n >= 100 else f'max(13px,{w})'
    if w in ('small', 'x-small', 'xx-small'):
        return '13px'
    if w == 'smaller':
        return 'max(13px,.83em)'
    if w.startswith('clamp(') and w.endswith(')'):
        a = _teile(w[6:-1])
        if len(a) == 3:
            lo, hi = _px(a[0]), _px(a[2])
            if lo is not None and hi is not None:
                if lo >= MIN:
                    return None
                a[0] = '13px'
                if hi < MIN:
                    a[2] = '13px'
                return 'clamp(' + ','.join(x.strip() for x in a) + ')'
    if w.startswith('max(') and w.endswith(')'):
        if any((_px(x) or 0) >= MIN for x in _teile(w[4:-1])):
            return None
    return f'max(13px,{w})'


RE_FS = re.compile(r'(font-size\s*:\s*)([^;}"\'<>!]+?)(\s*(?:!important)?\s*(?:[;}"\'<]|$))', re.M)
# Kurzschrift: [Stil/Gewicht …] Grösse[/Zeilenhöhe] Familie
RE_FONT = re.compile(r'(?<![-\w])(font\s*:\s*)((?:(?:italic|oblique|normal|bold|bolder|lighter|small-caps|\d{3})\s+)*)'
                     r'(\d*\.?\d+(?:px|rem|em|%)|clamp\([^;{}]*?\)|min\([^;{}]*?\))(?=\s*/|\s+[\'"A-Za-z-])')


def _fs(m):
    n = groesse(m.group(2))
    return m.group(0) if n is None else m.group(1) + n + m.group(3)


def _font(m):
    n = groesse(m.group(3))
    return m.group(0) if n is None else m.group(1) + m.group(2) + n


def text(t):
    t = RE_FS.sub(_fs, t)
    return RE_FONT.sub(_font, t)


# Prüfpunkt 18 (kein Leerraum über 380 px zwischen zwei Inhalten): auf Drucksachen und Beigaben liegen
# zwischen zwei Kartons zweimal die volle Abschnitt-Luft (am Rechner rund 398 px). Dort je drei Viertel.
LUFT = ('<style id="stueck-luft">.stueck.fl{padding-top:calc(var(--abschnitt)*.75)}'
        '.stueck.blatt{padding-bottom:calc(var(--abschnitt)*.75 + var(--rund))}</style>')
# Mails: die Spalte der Etiketten «Von/Wann/Betreff» (64 px) fasst «Betreff» in 13 px nicht mehr.
ETIKETT = '<style id="mb-etikett">.mb-ueber__t small{grid-template-columns:90px minmax(0,1fr)}</style>'
ZUSATZ = (('drucksachen/index.html', 'stueck-luft', LUFT), ('beigaben/index.html', 'stueck-luft', LUFT),
          ('mails/index.html', 'mb-etikett', ETIKETT),
          # Feed: die Schalter «Heute/Mit den nächsten 30» sperren .1em; in 13 px steht die Schrift sonst 0,6 px links der Mitte.
          # Im Band über dem Raster (378 px im Handy) fasst die Leiste 13 px nur mit etwas weniger Sperrung und Innenabstand.
          ('feed/index.html', 'fw-mitte', '<style id="fw-mitte">.fw button{text-indent:.1em}'
           '.fw.fw--band{letter-spacing:.06em;gap:6px;padding-left:6px;padding-right:6px}'
           '.fw.fw--band button{padding:0 9px;text-indent:.06em}</style>'))


def anwenden(root=ROOT):
    geaendert = []
    for rel, sid, css in ZUSATZ:
        f = os.path.join(root, rel)
        if os.path.exists(f):
            t = open(f, encoding='utf-8').read()
            if f'id="{sid}"' not in t and '</head>' in t:
                open(f, 'w', encoding='utf-8').write(t.replace('</head>', css + '</head>', 1))
    for rel in DATEIEN:
        f = os.path.join(root, rel)
        if not os.path.exists(f):
            continue
        alt = open(f, encoding='utf-8').read()
        neu = text(alt)
        if neu != alt:
            open(f, 'w', encoding='utf-8').write(neu)
            geaendert.append(rel)
    print('schrift_13: mindestens 13 px in', len(geaendert), 'Dateien')
    return geaendert


if __name__ == '__main__':
    anwenden(sys.argv[1] if len(sys.argv) > 1 else ROOT)
