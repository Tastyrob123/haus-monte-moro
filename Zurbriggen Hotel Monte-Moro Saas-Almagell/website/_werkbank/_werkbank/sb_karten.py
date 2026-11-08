#!/usr/bin/env python3
"""Werkbank Hotel Monte-Moro, Seite «Unterlagen» (Werkbank Papier, 08.11.2026; Bauart wie sb_karten.py der Vorlage).
Die Karten des Röstihüs, neu gesetzt mit dem Kartenbrett (_werkzeuge/carte, Druck über carte/drucke.js auf dem Werkzeug-Server 9383),
jede neben den Seiten der heutigen Speisekarte des Hauses (_quelle/website/pdf/speisekarte.pdf, Stand 18.11.2024): die Röstis und Cordon bleus
(heute Seiten 4 und 5) und der Wein von Fabian mit dem Apéro (heute Seite 8, die Hotelweine).
Das Heute-Material kommt aus _quelle/ (Zweig quelle) und wird als PDF nach _werkbank/heute/ kopiert, damit die Seite auch ohne _quelle baut.
Ist das Kartenbrett nicht erreichbar, bleibt die vorige Idee liegen; fehlt sie ganz, steht die Unterlage nicht auf der Seite.
   python3 _werkbank/sb_karten.py            → unterlagen/pdf/<ziel>.pdf, _werkbank/heute/<ziel>.pdf, _werkbank/unterlagen.json
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py _werkbank/sb_karten.py . --seite   → unterlagen/index.html (Kit unterlagen.py)"""
import json, os, re, subprocess, sys
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
CARTE = os.path.join(PROJ, '_werkzeuge', 'carte')
SPEISEKARTE = os.path.join(PROJ, '_quelle', 'website', 'pdf', 'speisekarte.pdf')
# Ziel, Name, Gruppe, Karte im Kartenbrett, Seiten der heutigen Speisekarte
KARTEN = [
    ('roestihues', 'Röstis und Cordon bleus', 'Röstihüs', 'roestihues', [4, 5]),
    ('wein-apero', 'Wein von Fabian und Apéro', 'Röstihüs', 'wein-apero', [8]),
]
FREMD = re.compile(r'Wild Side|Negroni|Culinarium|Hannover|Momo', re.I)


def heute_pdf(seiten, ziel):
    subprocess.run(['pdfseparate', '-f', str(min(seiten)), '-l', str(max(seiten)), SPEISEKARTE, ziel + '-%d.teil'], check=True)
    teile = [f'{ziel}-{s}.teil' for s in seiten]
    if len(teile) == 1:
        os.replace(teile[0], ziel)
    else:
        subprocess.run(['pdfunite', *teile, ziel], check=True)
    for s in range(min(seiten), max(seiten) + 1):
        if os.path.exists(f'{ziel}-{s}.teil'):
            os.remove(f'{ziel}-{s}.teil')


def bau():
    os.makedirs(os.path.join(ROOT, 'unterlagen', 'pdf'), exist_ok=True); os.makedirs(os.path.join(W, 'heute'), exist_ok=True)
    for alt in ('angebot-feiern', 'dishes-in-love', 'drunk-in-love', 'preisliste'):   # Unterlagen eines anderen Hauses
        for p in (os.path.join(W, 'heute', alt + '.pdf'), os.path.join(ROOT, 'unterlagen', 'pdf', alt + '.pdf')):
            if os.path.exists(p):
                os.remove(p)
    plan = []
    for ziel, name, gruppe, karte, seiten in KARTEN:
        aus = os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf')
        r = subprocess.run(['node', os.path.join(CARTE, 'drucke.js'), karte, 'stand', aus + '.neu.pdf'], capture_output=True, text=True, timeout=240)
        neu = aus + '.neu.pdf'
        if r.returncode == 0 and os.path.exists(neu):
            text = subprocess.run(['pdftotext', neu, '-'], capture_output=True, text=True).stdout
            if FREMD.search(text) or 'Rösti' not in text and karte == 'roestihues':
                print('Kartenbrett liefert noch keine Karte des Hauses:', ziel); os.remove(neu)
            else:
                os.replace(neu, aus)
        else:
            print('Kartenbrett nicht erreichbar, bleibt:', ziel, r.stderr[-200:])
            if os.path.exists(neu):
                os.remove(neu)
        h = os.path.join(W, 'heute', ziel + '.pdf')
        if os.path.exists(SPEISEKARTE):
            heute_pdf(seiten, h)
        if not (os.path.exists(aus) and os.path.exists(h)):
            print('fehlt', ziel); continue
        plan.append(dict(ziel=ziel, quelle=os.path.relpath(h, ROOT), name=name, gruppe=gruppe, seiten=0, b=210, h=297, dazu='', fehlt=''))
    json.dump(plan, open(os.path.join(W, 'unterlagen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Unterlagen:', ', '.join(p['ziel'] for p in plan))


def seite():
    import kern as K
    import unterlagen as U
    plan = json.load(open(os.path.join(W, 'unterlagen.json'), encoding='utf-8'))
    K.H.FAECHER = [(p['ziel'], p['name']) for p in plan][:4]
    U.baue()
    p = os.path.join(ROOT, 'unterlagen', 'index.html')
    t = open(p, encoding='utf-8').read().replace(' loading="lazy"', '')
    t = t.replace('keine offiziellen Unterlagen des Hauses', 'keine offiziellen Unterlagen des Hotels Monte-Moro')
    open(p, 'w', encoding='utf-8').write(t)
    q = os.path.join(ROOT, 'unterlagen', 'img', f'n-{plan[0]["ziel"]}-01.webp')
    im = Image.open(q); im.thumbnail((1200, 1200)); im.save(os.path.join(ROOT, 'unterlagen', 'img', 'vorschau.webp'), 'WEBP', quality=86)
    ids = {x['ziel'] for x in plan}
    for f in os.listdir(os.path.join(ROOT, 'unterlagen', 'img')):   # alte Seitenbilder, die zu keiner Unterlage mehr gehören
        m = re.match(r'[nh]-(.+)-\d\d\.webp$', f)
        if m and m.group(1) not in ids:
            os.remove(os.path.join(ROOT, 'unterlagen', 'img', f))
    for f in os.listdir(os.path.join(ROOT, 'unterlagen', 'pdf')):
        if f[:-4] not in ids:
            os.remove(os.path.join(ROOT, 'unterlagen', 'pdf', f))
    roh = os.path.join(W, 'roh', 'unterlagen')
    for f in os.listdir(roh) if os.path.isdir(roh) else []:
        m = re.match(r'[nh]-(.+?)(-\d+\.png|\.json)$', f)
        if m and m.group(1) not in ids:
            os.remove(os.path.join(roh, f))


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else bau()
