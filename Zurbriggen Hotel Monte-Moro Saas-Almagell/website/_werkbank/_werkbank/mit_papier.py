#!/usr/bin/env python3
"""Umschlag für die Papier-Teile der Werkbank Monte-Moro (Werkbank Papier, 08.11.2026).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py <skript.py> "<website/_werkbank>" [weitere Argumente]
Lädt haus.py (Revier Werkbank Kern) und legt die Texte der Papier-Seiten aus _werkbank/papier_haus.json darüber
(PAPIER, PAPIER_SEITE, ETIKETTEN, MATERIAL, FEED); erst dann läuft das Skript (Kit oder eigenes) wie gewohnt als __main__.
Solange haus.py noch Name, Farben und Schrift eines anderen Hauses trägt, gelten die Angaben aus «_falls_fremd» (nur Grundwerte des Hauses).
Damit hängen die Papier-Seiten nicht davon ab, wann der Kern-Teil haus.py umstellt; nichts in haus.py wird geändert."""
import json
import os
import re
import runpy
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)


def werkzeugnamen():
    """die Namen der Werkzeuge aus _werkzeuge/oberflaeche/kleid/montemoro.js (eine Stelle, nie fest geschrieben)"""
    k = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), '_werkzeuge', 'oberflaeche', 'kleid', 'montemoro.js')
    m = re.search(r'namen:\s*\{([^}]*)\}', open(k, encoding='utf-8').read())
    return dict(re.findall(r"(\w+):\s*'([^']*)'", m.group(1))) if m else {}


def fall(name, art=None):
    """Name mit Artikel im richtigen Fall: art None = wie geschrieben («Das Kartenbrett»), 'klein' = «das Kartenbrett», 'im' = «im Kartenbrett» / «in der Rezeption»"""
    artikel, rest = name.split(' ', 1)
    if art == 'klein':
        return artikel.lower() + ' ' + rest
    if art == 'dativ':
        return ('der ' if artikel == 'Die' else 'dem ') + rest
    if art == 'im':
        return ('in der ' if artikel == 'Die' else 'im ') + rest
    return name


def anwenden(H):
    pfad = os.path.join(HIER, 'papier_haus.json')
    if not os.path.exists(pfad):
        return H
    roh = open(pfad, encoding='utf-8').read()
    namen = werkzeugnamen()
    roh = re.sub(r'\[\[(\w+)(?::(\w+))?\]\]', lambda m: fall(namen.get(m.group(1), m.group(0)), m.group(2)), roh)   # [[karten:im]] → «im Kartenbrett»
    daten = json.loads(roh)
    fremd = daten.pop('_falls_fremd', {})
    if 'monte' not in str(getattr(H, 'NAME', '')).lower():
        for n, v in fremd.items():
            setattr(H, n, [tuple(x) for x in v] if n == 'DRUCKSCHRIFT' else (tuple(v) if isinstance(v, list) and n not in ('SCHRIFT_MEHR', 'DRUCKQUELLEN') else v))
        if isinstance(H.SCHRIFT, dict):
            H.SCHRIFT = dict(fremd.get('SCHRIFT', H.SCHRIFT))
            H.SCHRIFT['titel'] = tuple(H.SCHRIFT['titel'])
    for n, v in daten.items():
        alt = getattr(H, n, None)
        if isinstance(alt, dict) and isinstance(v, dict):
            for k, w in v.items():
                if isinstance(alt.get(k), set):
                    alt[k] = set(w)
                elif k in ('karton',) and isinstance(w, dict):
                    alt[k] = {a: (b[0], [tuple(x) for x in b[1]]) for a, b in w.items()}
                elif k in ('auslage', 'etik_auslage', 'orte_e', 'orte_d', 'streu', 'zeichen') and isinstance(w, list):
                    alt[k] = [tuple(x) for x in w]
                elif k in ('etik_titel',) and isinstance(w, list):
                    alt[k] = tuple(w)
                else:
                    alt[k] = w
        else:
            setattr(H, n, v)
    # die eigenen Drucksachen (papier.py schreibt papier_neu_seite.json): Karton, Titel, Breite, Schatten, wie haus.py es auch tut
    ns = os.path.join(HIER, 'papier_neu_seite.json')
    S = getattr(H, 'PAPIER_SEITE', None)
    if os.path.exists(ns) and isinstance(S, dict):
        for k, v in json.load(open(ns, encoding='utf-8')).items():
            S.setdefault('karton', {})[k] = (v['karton'][0], [tuple(x) for x in v['karton'][1]])
            S.setdefault('titel', {})[k] = v['titel']
            S['breit'] = set(S.get('breit', ())) | set(v['breit'])
            S['schatten'] = set(S.get('schatten', ())) | {k}
    return H


def notlauf():
    """Nur solange haus.py (Revier Kern) noch Pfade eines anderen Hauses liest und beim Laden scheitert: haus.py mit zwei Weichen laden
    (fehlende Fotos → ein Foto dieses Hauses, fehlende Tapete → leer). Die Papier-Teile lesen aus haus.py nur Zeichen, Wortmarke und Rahmen."""
    import types
    src = open(os.path.join(HIER, 'haus.py'), encoding='utf-8').read()
    src = src.replace("open(os.path.join(WEB, 'assets', 'bild', 'haus-tapete.svg'), encoding='utf-8').read()", "'<svg xmlns=\"http://www.w3.org/2000/svg\"/>'")
    m = types.ModuleType('haus')
    m.__file__ = os.path.join(HIER, 'haus.py')
    sys.modules['haus'] = m
    import builtins
    _open = builtins.open

    def offen(p, *a, **k):
        try:
            return _open(p, *a, **k)
        except FileNotFoundError:
            if str(p).endswith(('.webp', '.jpg', '.png')):
                return _open(os.path.join(os.path.dirname(os.path.dirname(HIER)), 'assets', 'img', 'haus-sommer-s.webp'), *a, **k)
            raise
    src = src.replace("raise FileNotFoundError(f'Bild {key} fehlt in website/assets/bild')", "return os.path.join(WEB, 'assets', 'img', 'haus-sommer-l.webp')")
    import ast
    baum = ast.parse(src)
    for st in baum.body:   # Anweisung für Anweisung; was scheitert, bleibt weg
        try:
            exec(compile(ast.Module(body=[st], type_ignores=[]), m.__file__, 'exec'), m.__dict__)
        except Exception:   # noqa: BLE001
            pass


def main():
    skript = sys.argv[1]
    sys.argv = [skript] + sys.argv[2:]
    try:
        import haus  # noqa: F401
    except Exception as f:   # noqa: BLE001
        sys.modules.pop('haus', None)
        print('mit_papier: haus.py lädt nicht (' + type(f).__name__ + '), Notlauf', file=sys.stderr)
        notlauf()
    import kern  # noqa: F401  (lädt haus als kern.H)
    anwenden(kern.H)
    sys.modules['haus'] = kern.H
    runpy.run_path(skript, run_name='__main__')


if __name__ == '__main__':
    main()
