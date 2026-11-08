#!/usr/bin/env python3
"""Nach papier_seiten.py (Kit) und den Seiten von Sticker, Beigaben, Postkarten, Unterlagen: die Papier-Seiten im Kleid und in den Worten
des Hotels Monte-Moro (Werkbank Papier, 08.11.2026; Bauart wie papier_nach.py der Vorlage).
Gleich grosse Stücke «je 94 mm», Bilder laden sofort (kein lazy, WebKit-Prüfung), Karton der Vorschauen in Wandschatten statt im Braun des Kits,
die Drucksachen-Seite sagt, woher die übernommenen Stücke kommen (Hausdruckerei), Vorschaubild je Seite unter <seite>/img/vorschau.webp
für das Kapitel Papier der Werkbank. Danach die Nachbauten zeile_ganz (kein Wort allein unten) und text_mitte/knopf_mitte (Schrift mittig).
Aufruf: python3 _werkbank/papier_nach.py (im Ordner website/_werkbank). Wiederholbar."""
import json, os, re
from PIL import Image

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(HIER, '_werkbank')
import sys; sys.path.insert(0, W)  # noqa: E401,E702
_MJ = os.path.join(W, 'papier_mehr.json')
MEHR = json.load(open(_MJ, encoding='utf-8'))['druck'] if os.path.exists(_MJ) else []
import mit_papier  # noqa: E402
DRUCK = mit_papier.fall(mit_papier.werkzeugnamen().get('druck', 'Die Hausdruckerei'), 'klein').replace('die ', 'der ', 1)   # «der Hausdruckerei», Name aus kleid/montemoro.js
ZAHL = {0: 'keine', 1: 'eine', 2: 'zwei', 3: 'drei', 4: 'vier', 5: 'fünf', 6: 'sechs', 7: 'sieben', 8: 'acht', 9: 'neun', 10: 'zehn', 11: 'elf', 12: 'zwölf',
        13: 'dreizehn', 14: 'vierzehn', 15: 'fünfzehn', 16: 'sechzehn', 17: 'siebzehn', 18: 'achtzehn', 19: 'neunzehn', 20: 'zwanzig'}
# Kleid der Papier-Seiten (nur hier, die Werkbank-Gestaltung selbst gehört dem Kern-Teil): Karton im Wandschatten des Hauses, Bildunterschriften in Grau
KLEID = ('<style id="papier-kleid">.karton,.bogenblick{background:#D6CCC1!important;border-radius:0!important}'
         '.karton figcaption{color:#4A5D70!important}'
         '.fl--nacht .karton,.fl--navy .karton,.fl--tief .karton{background:#E7E1DC!important}'
         '.etk .b{background:#E7E1DC}'
         # Leiste der Unterseiten: Bergkamm in Lärche (breites Zeichen, 3483 × 696), am Handy ohne den Seitennamen, damit «Zur Werkbank» ganz steht
         '.insel__m svg{color:#C67144!important;fill:#C67144!important;height:18px!important}'
         '.insel__m svg *{fill:#C67144!important}'
         '@media(max-width:480px){.insel__m span{display:none!important}}</style>')


def nach(ordner, fn=None):
    p = os.path.join(HIER, ordner, 'index.html')
    if not os.path.exists(p):
        return
    t = open(p, encoding='utf-8').read()
    n = re.sub(r'(\d+) bis \1 mm', r'je \1 mm', t).replace('Originalgröße', 'Originalgrösse')
    n = n.replace(' loading="lazy" decoding="async"', ' decoding="async"').replace(' loading="lazy"', '')
    n = re.sub(r'<style id="papier-kleid">.*?</style>', '', n, flags=re.S)
    n = n.replace('</head>', KLEID + '\n</head>', 1)
    if fn:
        n = fn(n)
    if n != t:
        open(p, 'w', encoding='utf-8').write(n)
        print('papier-nach:', ordner)


def drucksachen(t):
    k = len(MEHR)
    plan = json.load(open(os.path.join(W, 'papier_plan.json'), encoding='utf-8'))
    eigen = len(plan['druck'])
    alt = 'Papier, das im Monte-Moro auf dem Tisch, an der Rezeption, im Zimmer oder im Umschlag landen könnte.'
    if k:
        neu = (f'{ZAHL.get(eigen, eigen).capitalize()} Ideen für Papier, dazu {ZAHL.get(k, k)} fertige Drucksachen aus ' + DRUCK + '. '
               'Papier, das im Monte-Moro auf dem Tisch, an der Rezeption, im Zimmer oder im Umschlag landen könnte.')
        t = t.replace(alt, neu)
    for d in MEHR:   # Stücke der Hausdruckerei: Knopf «PDF herunterladen»
        a = t.find(f'id="{d["id"]}"')
        if a < 0:
            continue
        b = t.find('</section>', a)
        teil = t[a:b].replace('Als PDF ansehen', 'PDF herunterladen')
        t = t[:a] + teil + t[b:]
    return t


def vorschau(ordner, quelle, breite=1200):
    """ein Vorschaubild je Seite für das Kapitel Papier der Werkbank"""
    q = os.path.join(HIER, ordner, 'img', quelle)
    if os.path.exists(q):
        im = Image.open(q)
        if im.width > breite:
            im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
        im.save(os.path.join(HIER, ordner, 'img', 'vorschau.webp'), 'WEBP', quality=86)


SEITEN = ('unterlagen', 'drucksachen', 'untersetzer', 'sticker', 'postkarten', 'beigaben', 'material', 'mails')


def nachbau():
    """die Nachbauten der Werkbank (zeile_ganz: kein Wort allein unten, text_mitte: Schrift mittig in Knöpfen) über die Papier-Seiten;
    haus.nach_bau macht dasselbe später über alle Seiten, beides ist wiederholbar"""
    import sys
    sys.path.insert(0, W)
    import zeile_ganz, text_mitte
    for o in SEITEN:
        if os.path.exists(os.path.join(HIER, o, 'index.html')):
            nach(o)
            zeile_ganz.anwenden(os.path.join(HIER, o))
            p = os.path.join(HIER, o, 'index.html')
            t = re.sub(r'<style id="text-mitte">.*?</style><script id="text-mitte-js">.*?</script>', '', open(p, encoding='utf-8').read(), flags=re.S)
            t = re.sub(r'<style id="knopf-mitte">.*?</style><script id="knopf-mitte-js">.*?</script>', '', t, flags=re.S)
            i = t.rfind('</body>')
            open(p, 'w', encoding='utf-8').write(t[:i] + text_mitte.BLOCK + t[i:])
            knopf_mitte(p)


def knopf_mitte(pfad):
    """Block aus knopf_mitte.css und knopf_mitte.js nach dem Block von text_mitte.py einfügen (wiederholbar)."""
    css = open(os.path.join(W, 'knopf_mitte.css'), encoding='utf-8').read()
    js = open(os.path.join(W, 'knopf_mitte.js'), encoding='utf-8').read().strip()
    css += '\n@media(max-width:480px){h1.t1{font-size:min(38px,9.4vw)!important}}'
    block = f'<style id="knopf-mitte">{css}</style><script id="knopf-mitte-js">{js}</script>'
    t = open(pfad, encoding='utf-8').read()
    t = re.sub(r'<style id="knopf-mitte">.*?</style><script id="knopf-mitte-js">.*?</script>', '', t, flags=re.S)
    i = t.rfind('</body>')
    t = t[:i] + block + t[i:]
    open(pfad, 'w', encoding='utf-8').write(t)


if __name__ == '__main__':
    nach('untersetzer')
    nach('drucksachen', drucksachen)
    vorschau('untersetzer', 'u03.webp')
    vorschau('drucksachen', 'karte.webp')
    nachbau()
