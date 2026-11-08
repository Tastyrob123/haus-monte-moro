#!/usr/bin/env python3
"""Rücksprung auf die alte Höhe in jede Seite der Werkbank einsetzen (Robert 1.11.2026). Quelle: _werkbank/ruecksprung.js, eingesetzt als
<script id="ruecksprung"> vor </body> (wiederholbar, ersetzt einen vorhandenen Block). Läuft am Ende von haus.nach_bau und als letzter Schritt von bau_alles.sh.
   python3 _werkbank/ruecksprung.py [<website/_werkbank>]"""
import glob, os, re, sys

W = os.path.dirname(os.path.abspath(__file__))
ORDNER = ('werkbank', 'befund', 'unterlagen', 'drucksachen', 'untersetzer', 'sticker', 'postkarten', 'beigaben', 'feed', 'mails', 'material')


def block():
    js = open(os.path.join(W, 'ruecksprung.js'), encoding='utf-8').read()
    js = re.sub(r'^/\*.*?\*/\s*', '', js, count=1, flags=re.S).strip()
    return '<script id="ruecksprung">' + js + '</script>'


def anwenden(root):
    b, n = block(), 0
    for o in ORDNER:
        for f in glob.glob(os.path.join(root, o, '**', '*.html'), recursive=True):
            rel = os.path.relpath(f, root)
            name = os.path.basename(f)
            if name.startswith('_') or '/_' in rel or '.vor-' in rel:
                continue
            s = open(f, encoding='utf-8').read()
            if '</body>' not in s:
                continue
            neu = re.sub(r'<script id="ruecksprung">.*?</script>', '', s, flags=re.S)
            i = neu.rfind('</body>')
            neu = neu[:i] + b + neu[i:]
            if neu != s:
                open(f, 'w', encoding='utf-8').write(neu); n += 1
    return n


if __name__ == '__main__':
    print('ruecksprung:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(W)), 'Seiten')
