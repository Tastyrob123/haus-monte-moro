#!/usr/bin/env python3
"""Karten & Preislisten · Hotel Monte-Moro, Saas-Almagell: liest die Karten und Preislisten des Hauses einmal als Daten ein (08.11.2026, C17).
Kopie von einlesen.py des Stamms.

Nichts wird abgetippt. karten_lesen.py liest die Karten aus der Website (_daten/quelle/<karte>.json, gegen daten.py, die Speisekarte und die gebaute
Website geprüft), satz_bau.py setzt sie im Satz des Hauses nach satz/u-<karte>.html. Dieses Skript zerlegt den Satz in einen Baum: Elemente (Tag,
Merkmale, Kinder), Texte (das, was das Haus ändert) und feste Teile (Logo, Bergkamm). Aus diesem Baum setzt satz/satz.js dasselbe HTML Zeichen für
Zeichen wieder (python3 _werkzeuge/carte/pruefe.py rund).

Eine Wochenkarte (Art «abend» des Stamms) führt das Haus nicht; sie wird nur angelegt, wenn _daten/quelle/abend.json liegt.

Geschrieben wird nur in _werkzeuge/carte/ (_daten/, bilder/z/, bilder/g/, bilder/fotos.json).

    python3 _werkzeuge/carte/einlesen.py            nur wo noch kein Stand liegt (ein Stand des Hauses wird nie überschrieben)
    python3 _werkzeuge/carte/einlesen.py --grund    nur den Grundstand neu (_daten/grundstand/), für den Rundlauf und «Ursprünglicher Stand»
"""
import datetime, html, json, os, re, shutil, sys

HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(HIER))
PROJ = os.path.join(_WURZEL, 'website')   # Website in website/
QD = os.path.join(HIER, '_daten', 'quelle')
DATEN = os.environ.get('CARTE_DATEN') or os.path.join(HIER, '_daten')
sys.path.insert(0, HIER)

# Karten, die Karten & Preislisten pflegt: Kennung = Satz satz/u-<kennung>.html = Name der PDF (karten_lesen.py); Reihenfolge wie im Rand
REIHE = ['roestihues', 'wein-apero', 'preisliste', 'zuschlaege', 'spa']
KARTEN = {}
for _z in REIHE + sorted(f[:-5] for f in os.listdir(QD) if f.endswith('.json') and f[:-5] not in REIHE + ['abend', 'pruefung']):
    if os.path.isfile(os.path.join(QD, _z + '.json')):
        _q = json.load(open(os.path.join(QD, _z + '.json'), encoding='utf-8'))
        KARTEN[_q['ziel']] = dict(name=_q['name'], unter=_q['unter'], gruppe=_q['gruppe'], quelle=_q['quelle'], ab=_q['ab'], plakat=_q['plakat'], key=_q['key'], foto=_q['foto'])
LEER_TAG = {'img', 'br', 'hr', 'meta', 'link', 'input', 'wbr', 'col', 'source'}
A, Z = '', ''          # Platzhalter für feste Teile (Bilder als data:, Zeichen als svg) im Baum
TOKEN = re.compile(r'<!--.*?-->|<svg\b.*?</svg>|</?([a-zA-Z][\w-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>', re.S)


class Teile:
    """Feste Teile einer Karte: jedes nur einmal gespeichert, im Baum steht der Platzhalter."""
    def __init__(self):
        self.liste, self.idx = [], {}

    def ref(self, s):
        if s not in self.idx:
            self.idx[s] = len(self.liste)
            self.liste.append(s)
        return f'{A}{self.idx[s]}{Z}'

    def at(self, s):   # data:-Bilder in Merkmalen
        return re.sub(r'data:[a-z]+/[\w.+-]+;base64,[A-Za-z0-9+/=]+', lambda m: self.ref(m.group(0)), s)


def text_kind(raw, T):
    """Text zwischen Tags: als Text (wenn er sich genau so wieder schreibt), sonst fest"""
    t = html.unescape(raw)
    if html.escape(t) == raw:
        return t
    return {'fn': 'roh', 'a': [T.at(raw)]}


def baum(s, T):
    """HTML → Liste von Kindern (Texte, Elemente {fn:'el', a:[tag, merkmale, *kinder]}, feste Teile {fn:'roh'})"""
    wurzel = {'fn': 'el', 'a': ['#', '']}
    stapel = [wurzel]
    pos = 0
    for m in TOKEN.finditer(s):
        if m.start() > pos:
            stapel[-1]['a'].append(text_kind(s[pos:m.start()], T))
        tok = m.group(0)
        pos = m.end()
        if tok.startswith('<!--'):
            stapel[-1]['a'].append({'fn': 'roh', 'a': [tok]})
            continue
        if tok.startswith('<svg'):
            stapel[-1]['a'].append({'fn': 'roh', 'a': [T.ref(tok) if len(tok) > 200 else tok]})
            continue
        tag, at = m.group(1), m.group(2)
        if tok.startswith('</'):
            oben = stapel.pop()
            assert oben['a'][0] == tag, ('Tag passt nicht', oben['a'][0], tag, s[max(0, m.start() - 80):m.start() + 20])
            continue
        el = {'fn': 'el', 'a': [tag, T.at(at)]}
        stapel[-1]['a'].append(el)
        if tag.lower() not in LEER_TAG and not at.rstrip().endswith('/'):
            stapel.append(el)
    if pos < len(s):
        stapel[-1]['a'].append(text_kind(s[pos:], T))
    assert len(stapel) == 1, ('offene Tags', [x['a'][0] for x in stapel])
    return wurzel['a'][2:]


def lies(kennung):
    pfad = os.path.join(HIER, 'satz', 'u-' + kennung + '.html')
    h = open(pfad, encoding='utf-8').read()
    b = h.index('<body>') + len('<body>')
    e = h.rindex('</body>')
    kopf, koerper, fuss = h[:b], h[b:e], h[e:]
    T = Teile()
    seiten = []
    for x in baum(koerper, T):
        if isinstance(x, dict) and x['fn'] == 'el' and x['a'][0] == 'section':
            seiten.append({'fn': 'seite', 'a': x['a'][1:]})
        else:
            raise AssertionError(('zwischen den Seiten steht etwas', kennung, str(x)[:120]))
    fmt = re.search(r'@page\{size:(\d+)mm (\d+)mm', kopf)
    k = KARTEN[kennung]
    return dict(art='satz', ziel=kennung, name=k['name'], unter=k['unter'], gruppe=k['gruppe'], quelle=k['quelle'], ab=k['ab'], plakat=k['plakat'], key=k['key'], schema=1,
                format=[int(fmt.group(1)), int(fmt.group(2))], kopf=kopf, fuss=fuss, seiten=seiten, teile=T.liste)


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


# Fotos des Hauses für Liste und Kacheln (Bildregister website/inhalt/bilder.py, ausgeliefert unter website/assets/img/<schlüssel>-<s|m|l|x>.webp,
# 480/900/1440/2200 px breit): je Karte ihr Bild aus _daten/quelle/<karte>.json (foto), Schlüssel aus dem Register, nicht geraten
STUFEN = [('s', 480), ('m', 900), ('l', 1440), ('x', 2200)]


def _breiten(nm):
    b = [(w, s) for s, w in STUFEN if os.path.isfile(os.path.join(PROJ, 'assets', 'img', f'{nm}-{s}.webp'))]
    if not b:
        raise SystemExit(f'Bild fehlt: website/assets/img/{nm}-*.webp')
    return b


def vorschaubilder():
    """Kleine Bilder für die Liste und die Kacheln (112 × 112 px) und je ein grosses für das Startbild (bis 1100 px breit, bilder/g/);
    fotos.json: Karte → Schlüssel."""
    from PIL import Image
    ziel, gross = os.path.join(HIER, 'bilder', 'z'), os.path.join(HIER, 'bilder', 'g')
    for o in (ziel, gross):
        shutil.rmtree(o, ignore_errors=True)
        os.makedirs(o, exist_ok=True)
    fotos = {k: v['foto'] for k, v in KARTEN.items()}
    for nm in sorted(set(fotos.values())):
        b = _breiten(nm)
        im = Image.open(os.path.join(PROJ, 'assets', 'img', '%s-%s.webp' % (nm, b[0][1]))).convert('RGB'); w, h = im.size; k = min(w, h)
        im.crop(((w - k) // 2, (h - k) // 2, (w - k) // 2 + k, (h - k) // 2 + k)).resize((112, 112), Image.LANCZOS).save(os.path.join(ziel, nm + '.webp'), 'WEBP', quality=80)
        g = max([x for x in b if x[0] <= 1100] or [b[0]])
        im = Image.open(os.path.join(PROJ, 'assets', 'img', '%s-%s.webp' % (nm, g[1]))).convert('RGB')
        im.save(os.path.join(gross, nm + '.webp'), 'WEBP', quality=80)
    _schreib(os.path.join(HIER, 'bilder', 'fotos.json'), fotos)
    return len(set(fotos.values()))


GAENGE = ('d1', 'd2', 'd3', 'd4', 'd5', 'd6')   # Plätze der Wochenkarte des Stamms (satz.js ABEND)


def abend():
    """Wochenkarte des Stamms (nur wenn _daten/quelle/abend.json liegt): jedes Feld wörtlich von dort."""
    d = json.load(open(os.path.join(QD, 'abend.json'), encoding='utf-8'))
    t = d['abend']['tage'][0]
    assert all(g in t and g + '_z' in t for g in GAENGE), ('Die Karte hat eine andere Form als erwartet', list(t))
    return dict(art='abend', ziel='abend', name=d['name'], unter=d['unter'], gruppe=d['gruppe'], quelle=d['quelle'],
                schema=1, format=[210, 297], abend=d['abend'], seiten=[], teile=[])


def alle():
    aus = {'abend': abend()} if os.path.isfile(os.path.join(QD, 'abend.json')) else {}
    aus.update({k: lies(k) for k in KARTEN})
    return aus


if __name__ == '__main__':
    grund_nur = '--grund' in sys.argv
    karten = alle()
    print('Vorschaubilder:', vorschaubilder())
    for kennung, d in karten.items():
        _schreib(os.path.join(DATEN, 'grundstand', kennung + '.json'), d)
        ziel = os.path.join(DATEN, 'stand', kennung + '.json')
        if grund_nur:
            continue
        if os.path.exists(ziel):
            print(f'{kennung}: Stand liegt schon, bleibt (Grundstand erneuert)')
            continue
        _schreib(ziel, dict(d, veroeffentlicht=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wer='Einlesen'))
        print(f'{kennung}: {len(d["seiten"]) or 1} Seiten eingelesen, {len(d["teile"])} feste Teile')
