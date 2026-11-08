#!/usr/bin/env python3
"""Stücke der Säle für das Hotelbüro holen (Hotel Monte-Moro, mm-maison 08.11.2026): je drei echte Ergebnisse der Werkzeuge nach roh/,
damit der Saal mehr zeigt als einen Bildschirm (Fehlerbuch 10a, M09). Nur lesen, nichts in den Werkzeugen ändern.

  python3 _werkzeuge/maison/stuecke.py      dann  python3 _werkzeuge/maison/bau.py

- Drucksachen: die fertig gesetzten Vorschaubilder der Hausdruckerei (imprimerie/haeuser/montemoro/drucksachen/, liste.json) → roh/druck/<n>-<name>.png
- Karten: die PDF des Kartenbretts (veröffentlicht, sonst die Probe), erste Seite mit pdftoppm → roh/karten/<n>-<ziel>.png;
  gibt es keine PDF, das gesetzte Blatt der Karte aus dem Werkzeug (Bildschirm des Blatts, nur GET, kartenblatt.js).
Namen der Stücke in roh/<art>/namen.json (aus den Werkzeugen, nichts erfunden)."""
import glob, json, os, shutil, subprocess, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WZ = os.path.dirname(HIER)
ROH = os.path.join(HIER, 'roh')

# Drei Drucksachen, die zeigen, was die Hausdruckerei kann: in dieser Reihenfolge, so weit vorhanden (Schlüssel aus drucksachen/liste.json der Hausdruckerei).
# Nie ein Stück eines anderen Hauses (Wörter der Bar in Schlüssel oder Name: weglassen).
DRUCK = ['roestihues-karte', 'racletteabend', 'willkommensbrief', 'aushang-inklusive', 'kidsclub', 'tischkarte-hotelwein', 'briefpapier']
FREMD = ('session', 'dj', 'negroni', 'drunk', 'bar', 'mixology', 'falstaff', 'musa', 'magst', 'ghazouani', 'konzert', 'tanz', 'silvester', 'feiern', 'oeffnungszeiten')
KARTEN = ['roestihues', 'wein-apero', 'preisliste']   # Ziele des Kartenbretts (api/status), in dieser Reihenfolge, so weit vorhanden


def druck():
    """Aus der Liste der Plakatwerkstatt (drucksachen/liste.json: k, n, vorschau) die drei gewählten Stücke, Name wie dort."""
    from PIL import Image
    q = os.path.join(WZ, 'imprimerie', 'haeuser', 'montemoro', 'drucksachen')
    try:
        liste = {x['k']: x for x in json.load(open(os.path.join(q, 'liste.json'), encoding='utf-8'))}
    except (OSError, ValueError, KeyError):
        liste = {}
    z = os.path.join(ROH, 'druck'); shutil.rmtree(z, ignore_errors=True); os.makedirs(z)
    namen = {'_quelle': 'Hausdruckerei, haeuser/montemoro/drucksachen/liste.json'}
    i = 0
    reihe = [k for k in DRUCK if k in liste]   # nur Stücke, die als Drucksache des Hauses bekannt sind (DRUCK), nie geraten
    for k in reihe:
        if any(w in (k + ' ' + str((liste.get(k) or {}).get('n', ''))).lower() for w in FREMD):
            continue
        x = liste.get(k) or {}
        bild = next((os.path.join(q, v) for v in (x.get('vorschau') or []) + [k + '.png', k + '.jpg'] if os.path.exists(os.path.join(q, v))), '')
        if not bild or i >= 3:
            continue
        i += 1
        Image.open(bild).convert('RGB').save(os.path.join(z, f'{i}-{k}.png'))
        namen[f'{i}-{k}'] = x.get('n') or k
    json.dump(namen, open(os.path.join(z, 'namen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Drucksachen:', ', '.join(f'{k} ({v})' for k, v in namen.items() if not k.startswith('_')) or 'keine')


def karten():
    import urllib.request
    try:
        st = json.load(urllib.request.urlopen('http://127.0.0.1:9383/_werkzeuge/carte/api/status', timeout=8))
    except Exception as f:
        print('Karten: das Kartenbrett antwortet nicht', f); return
    k = {x['ziel']: x for x in st.get('karten', [])}
    z = os.path.join(ROH, 'karten'); shutil.rmtree(z, ignore_errors=True); os.makedirs(z)
    namen = {'_quelle': 'Kartenbrett /api/status und seine PDF'}
    reihe = [x for x in KARTEN if x in k] + [x for x in k if x not in KARTEN]
    n = 0
    for ziel in reihe:
        if n >= 3:
            break
        pdf = next((p for p in (os.path.join(WZ, 'carte', '_daten', 'stand', d, ziel + '.pdf') for d in ('live', 'probe')) if os.path.exists(p)), '')
        if not pdf:
            pdf = next(iter(glob.glob(os.path.join(WZ, 'carte', '**', ziel + '.pdf'), recursive=True)), '')
        ziel_png = os.path.join(z, f'{n + 1}-{ziel}')
        if pdf:
            subprocess.run(['pdftoppm', '-png', '-r', '110', '-f', '1', '-l', '1', '-singlefile', pdf, ziel_png], check=True)
        else:
            r = subprocess.run(['node', os.path.join(HIER, 'kartenblatt.js'), ziel, ziel_png + '.png'], capture_output=True, text=True)
            if r.returncode or not os.path.exists(ziel_png + '.png'):
                print('Karten:', ziel, 'ohne PDF und ohne Blatt', r.stderr[-300:]); continue
        n += 1
        namen[f'{n}-{ziel}'] = 'Karte: ' + k[ziel].get('name', ziel)
    json.dump(namen, open(os.path.join(z, 'namen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Karten:', ', '.join(x for x in namen if not x.startswith('_')) or 'keine')


if __name__ == '__main__':
    was = sys.argv[1:] or ['druck', 'karten']
    if 'druck' in was:
        druck()
    if 'karten' in was:
        karten()
