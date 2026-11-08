#!/usr/bin/env python3
"""Das Kartenbrett: ?v= an jedem eingebundenen Skript und Stilblatt aus dem Inhalt der Datei (M20, nie von Hand).
    python3 _werkzeuge/carte/fassungen.py      schreibt index.html, anleitung.html, pruefung.html, satz/blatt.html neu"""
import hashlib, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
WERKZEUGE = os.path.dirname(HIER)
WEB = os.path.join(os.path.dirname(WERKZEUGE), 'website')


def datei(weg, von):
    if weg.startswith('/assets/oberflaeche/'):
        return os.path.join(WERKZEUGE, 'oberflaeche', weg[len('/assets/oberflaeche/'):])
    if weg.startswith('/_werkzeuge/'):
        return os.path.join(WERKZEUGE, weg[len('/_werkzeuge/'):])
    if weg.startswith('/assets/'):
        return os.path.join(WEB, weg[1:])
    return os.path.join(os.path.dirname(von), weg)


def ersetze(p):
    t = open(p, encoding='utf-8').read()

    def neu(m):
        weg = m.group(2)
        f = datei(weg, p)
        if not os.path.isfile(f):
            return m.group(0)
        return f'{m.group(1)}{weg}?v={hashlib.sha1(open(f, "rb").read()).hexdigest()[:10]}"'
    t2 = re.sub(r'((?:src|href)=")([^"?#]+\.(?:js|css))(?:\?v=[^"]*)?"', neu, t)
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2)
    return t2 != t


if __name__ == '__main__':
    for f in ('index.html', 'anleitung.html', 'pruefung.html', os.path.join('satz', 'blatt.html')):
        print(f, 'neu' if ersetze(os.path.join(HIER, f)) else 'gleich')
