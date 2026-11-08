"""?v= in index.html und anleitung.vorlage.html aus dem Inhalt der Dateien (M20, nie von Hand): python3 _bau/fassungen.py
Eigene Dateien liegen neben index.html, /assets/oberflaeche/… unter _werkzeuge/oberflaeche/."""
import hashlib, os, re
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OF = os.path.join(os.path.dirname(H), 'oberflaeche')


def datei(weg):
    if weg.startswith('/assets/oberflaeche/'):
        return os.path.join(OF, weg[len('/assets/oberflaeche/'):])
    if not weg.startswith(('/', 'http')):
        return os.path.join(H, weg)
    return None


def neu(m):
    weg = m.group(2)
    p = datei(weg)
    if not p or not os.path.isfile(p):
        return m.group(0)
    v = hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10]
    return m.group(1) + weg + '?v=' + v + m.group(4)


for name in ('index.html', 'anleitung.vorlage.html'):
    p = os.path.join(H, name)
    t = open(p, encoding='utf-8').read()
    t2 = re.sub(r'((?:src|href)=")([^"?#]+\.(?:js|css))(\?v=[0-9a-z]+)?(")', neu, t)
    open(p, 'w', encoding='utf-8').write(t2)
    print(name, 'geändert' if t2 != t else 'gleich')
