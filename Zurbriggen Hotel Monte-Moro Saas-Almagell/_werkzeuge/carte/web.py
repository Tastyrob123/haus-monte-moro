"""Das Kartenbrett · Hotel Monte-Moro, Saas-Almagell — die Karten als Daten für die Website (08.11.2026, C27 in der Form des Hauses;
Vorlage: web.py des Stamms).

Die Website zeigt die Karte des Röstihüs (roestihues.html), die Preisliste (preise.html) und die Tarife des Spa (spa.html), gebaut aus
website/inhalt/daten.py (ROESTIS, CORDON, HOTELWEINE, SPRITZ, KOPF, RACLETTE, PREISE, ZUSCHLAEGE, KINDER, SPA_TARIFE).
Dieses Modul liest aus jeder veröffentlichten Karte ihre Rubriken mit Name, Zutaten und Preis (zeilen) und schreibt alle Karten nach karten.json:
  _werkzeuge/carte/anschluss/karten.json          immer nach dem Veröffentlichen (im Revier des Werkzeugs, ändert die Website nicht)
  _kette/10-kartenmacher/karten.json               Paket der Kette, Station 10 (python3 _werkzeuge/carte/web.py kette)
Die Website liest die Datei erst, wenn ihr Bau sie vor daten.py nimmt (Einbau in website/, nicht Revier des Kartenbretts; bis dahin bleibt
jede Seite Byte für Byte, wie sie ist). Eine Wochenkarte (Art «abend» des Stamms) stünde unter «karte»; das Haus führt keine."""
import datetime, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
GAENGE = [('d1', 'Eintrag 1'), ('d2', 'Eintrag 2'), ('d3', 'Eintrag 3'), ('d4', 'Eintrag 4'), ('d5', 'Eintrag 5'), ('d6', 'Eintrag 6')]


def _klasse(n):
    m = re.search(r'\sclass="([^"]*)"', n['a'][1] or '')
    return m.group(1).split() if m else []


def _text(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict) and x.get('fn') == 'el':
        return ''.join(_text(y) for y in x['a'][2:])
    return ''


def zeilen(d):
    """Rubriken der Karte als [{titel, eintraege: [{name, zutaten, preis}]}]; ausgeblendete Einträge zählen nicht."""
    if d.get('art') == 'abend':
        w = d['abend']
        t = w['tage'][0]
        e = [dict(name=t.get(k, '').strip(), zutaten=t.get(k + '_z', '').strip(), preis='') for k, _ in GAENGE if (t.get(k, '') + t.get(k + '_z', '')).strip()]
        return dict(ab=w['ab'], titel=w.get('motto') or w.get('titel', ''), mit=w.get('mit', ''), preis=w.get('preis', ''), rubriken=[dict(titel=w.get('mit', ''), eintraege=e)],
                    beispiel=bool(w.get('beispiel')))
    rubriken = []

    def geh(x):
        if not isinstance(x, dict) or x.get('aus'):
            return
        if x.get('fn') == 'seite':
            for y in x['a'][1:]:
                geh(y)
            return
        if x.get('fn') != 'el':
            return
        kl = _klasse(x)
        if 'sb-h' in kl:
            rubriken.append(dict(titel=_text(x).strip(), eintraege=[]))
            return
        if 'sb-m' in kl:
            f = {k: '' for k in ('sb-n', 'sb-dr', 'sb-mp')}
            for y in x['a'][2:]:
                if isinstance(y, dict) and y.get('fn') == 'el' and not y.get('aus'):
                    for k in f:
                        if k in _klasse(y):
                            f[k] = _text(y).strip()
            if not rubriken:
                rubriken.append(dict(titel='', eintraege=[]))
            rubriken[-1]['eintraege'].append(dict(name=f['sb-n'], zutaten=f['sb-dr'], preis=f['sb-mp']))
            return
        for y in x['a'][2:]:
            geh(y)
    for s in d.get('seiten', []):
        geh(s)
    return dict(rubriken=rubriken)


def karten_json(K, ziele, lies):
    """Alle veröffentlichten Karten (Stand) in der Form der Website."""
    aus = {'stand': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'quelle': 'Das Kartenbrett (_werkzeuge/carte/_daten/stand/)', 'karten': {}, 'karte': None}
    for z in ziele:
        s = lies(os.path.join(K, 'stand', z + '.json'))
        if not s:
            continue
        if z == 'abend':
            aus['karte'] = zeilen(s)
        else:
            aus['karten'][z] = dict(zeilen(s), name=s.get('name', ''))
    return aus


def schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(p + '.neu', encoding='utf-8'))
    os.replace(p + '.neu', p)


def anschliessen(K, ziele, lies):
    """Nach jedem Veröffentlichen: karten.json im Revier des Werkzeugs (nie in website/)."""
    eigen = os.path.realpath(K) == os.path.realpath(os.path.join(HIER, '_daten'))   # Prüfläufe mit Wegwerf-Daten schreiben neben ihre Daten, nie über die Datei des Hauses
    schreib(os.path.join(HIER if eigen else K, 'anschluss', 'karten.json'), karten_json(K, ziele, lies))
    return 'anschluss/karten.json'


if __name__ == '__main__':
    sys.path.insert(0, HIER)
    import carte
    d = karten_json(carte.K, carte.ZIELE, carte._lies)
    if sys.argv[1:] == ['kette']:
        schreib(os.path.join(HAUS, '_kette', '10-kartenmacher', 'karten.json'), d)
        print('_kette/10-kartenmacher/karten.json:', len(d['karten']), 'Karten')
    else:
        schreib(os.path.join(HIER, 'anschluss', 'karten.json'), d)
        print('anschluss/karten.json:', len(d['karten']), 'Karten')
