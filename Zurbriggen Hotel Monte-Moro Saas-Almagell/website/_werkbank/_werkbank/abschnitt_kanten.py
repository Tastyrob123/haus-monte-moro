#!/usr/bin/env python3
"""Werkbank: jedes Kapitel als eigene Fläche mit abgerundeten Ecken (Robert 10.11.2026: «wo man sonst so lange über leere Flächen scrollt
Abschnitte mit abgerundeten Ecken … dass das nach bisschen mehr Substanz aussieht», «bei allen Werkbänken»). Ursache der leeren Strecken: zwei
Abschnitte hintereinander mit derselben Grundfarbe, die runde Kante dazwischen ist unsichtbar. Dieser Schritt gibt einem solchen Abschnitt einen
anderen Ton des Hauses (nacht, navy, tief, blau bzw. papier, creme), sodass er als abgerundete Fläche über dem vorigen liegt, und legt an jede
runde Kante einen feinen Schatten. Texte, Bilder, Abstände bleiben. Läuft am Ende von haus.nach_bau, wiederholbar.
   python3 _werkbank/abschnitt_kanten.py [<werkbank-root>]"""
import glob, os, re, sys

DUNKEL = ['nacht', 'navy', 'tief', 'blau']
HELL = ['papier', 'creme']
CSS = ('.blatt{box-shadow:0 -1px 0 rgba(255,255,255,.07),0 -22px 46px -26px rgba(0,0,0,.55)}'
       '.fl--papier.blatt,.fl--creme.blatt{box-shadow:0 -1px 0 rgba(255,255,255,.5),0 -22px 46px -26px rgba(0,0,0,.45)}')
BLOCK = '<style id="abschnitt-kanten">' + CSS + '</style>'
SEC = re.compile(r'<section class="fl fl--([a-z]+)((?: [^"]*)?) blatt([^"]*)"')


def _farben_da(s):
    return {f for f in DUNKEL + HELL if '.fl--' + f + '{' in s}


def seite(s, css):
    da = _farben_da(css)
    treffer = list(SEC.finditer(s))
    farben = [m.group(1) for m in treffer]
    neu = list(farben)
    for i in range(1, len(farben)):
        if neu[i] != neu[i - 1]:
            continue
        reihe = DUNKEL if neu[i] in DUNKEL else HELL
        nach = farben[i + 1] if i + 1 < len(farben) else None
        wahl = [f for f in reihe if f in da and f != neu[i - 1] and f != nach]
        if wahl:
            neu[i] = wahl[0]
    aus, pos, n = [], 0, 0
    for m, f0, f1 in zip(treffer, farben, neu):
        aus.append(s[pos:m.start()])
        aus.append(m.group(0) if f0 == f1 else m.group(0).replace('fl--' + f0, 'fl--' + f1, 1))
        pos = m.end(); n += f0 != f1
    return ''.join(aus) + s[pos:], n


def anwenden(root):
    css = ''
    for c in glob.glob(os.path.join(root, 'werkbank', '*.css')) + glob.glob(os.path.join(root, '*.css')):
        css += open(c, encoding='utf-8', errors='ignore').read()
    gesamt = 0
    for f in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
        rel = os.path.relpath(f, root)
        if rel.startswith(('_werkbank', '_sicherung', 'node_modules')) or '.vor-' in rel:
            continue
        s = open(f, encoding='utf-8').read()
        if ' blatt' not in s or '</body>' not in s:
            continue
        s, n = seite(s, css + s)
        s = re.sub(r'<style id="abschnitt-kanten">.*?</style>', '', s, flags=re.S)
        i = s.rfind('</body>'); s = s[:i] + BLOCK + s[i:]
        open(f, 'w', encoding='utf-8').write(s); gesamt += n
    return gesamt


if __name__ == '__main__':
    print('abschnitt-kanten:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Abschnitte abgesetzt')
