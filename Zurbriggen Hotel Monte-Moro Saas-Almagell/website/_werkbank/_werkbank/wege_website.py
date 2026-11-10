#!/usr/bin/env python3
"""Werkbank Monte-Moro: Wege zur Website, die unter jeder Adresse ankommen (Robert 10.11.2026: «dass ich mit jedem Button … dahin komme, wo ich hinkommen soll»).
Die Seiten der Werkbank verlinken die Website mit «../zimmer.html». Das geht nur auf dem eigenen Server (serve.py, 9388), der fehlende Seiten aus website/ nachreicht;
unter dem Kette-Server (8978) und im Ordner selbst zeigte es ins Leere («nicht gefunden»). Dieser Schritt schreibt jeden solchen Weg auf den echten Ort im Ordner um
(«../../zimmer.html»): im Ordner und unter dem Kette-Server ist das die Website, auf 9388 bleibt der Browser an der Wurzel stehen und serve.py liefert dieselbe Seite.
Läuft ganz am Ende jedes Baus (bau_alles.sh, papier_alles.sh) und allein:  python3 _werkbank/wege_website.py"""
import os, re, sys
HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # website/_werkbank
WEB = os.path.dirname(HIER)                                         # website
HREF = re.compile(r'(\bhref=")([^"#?]+)([^"]*)(")')


def weg(datei, h):
    if re.match(r'^([a-z]+:|/|#|data:)', h, re.I):
        return None
    ziel = os.path.normpath(os.path.join(os.path.dirname(datei), h))
    rel = os.path.relpath(ziel, HIER)
    if rel.startswith('..') or os.path.exists(ziel):
        return None
    web = os.path.join(WEB, rel)
    if not os.path.isfile(web):
        return None
    return os.path.relpath(web, os.path.dirname(datei)).replace(os.sep, '/')


def main():
    n = 0
    for wurzel, ordner, dateien in os.walk(HIER):
        ordner[:] = [o for o in ordner if o != '_werkbank' and '.vor-' not in o and o != 'assets']
        for d in dateien:
            if not d.endswith('.html') or '.vor-' in d:
                continue
            p = os.path.join(wurzel, d)
            s = open(p, encoding='utf-8').read()
            def ers(m):
                global_n = weg(p, m.group(2))
                return m.group(1) + global_n + m.group(3) + m.group(4) if global_n else m.group(0)
            t = HREF.sub(ers, s)
            if t != s:
                open(p, 'w', encoding='utf-8').write(t); n += 1
    print(f'wege_website: {n} Seiten auf den echten Ort der Website umgeschrieben')


if __name__ == '__main__':
    main()
