#!/usr/bin/env python3
"""Bilder leicht ausliefern (Hotel Monte-Moro). Liest inhalt/bilder.py, findet die Quelldatei (auch über den Zahlen-Stamm, wenn der Name
nicht genau passt), schreibt assets/img/<key>-<s|m|l|x>.webp (480 / 900 / 1440 / 2200 px breit, nie grösser als die Quelle) und ein winziges
echtes Abbild (24 px, JPEG, Base64) nach assets/img/_abbild.json, das bau.py als Grund hinter jedes Foto legt. Nie aufblenden aus Schwarz.
  python3 bilder.py            alles, was fehlt oder älter als die Quelle ist
  python3 bilder.py --alles    alles neu"""
import os, sys, json, base64, io, re
from PIL import Image, ImageOps
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inhalt'))
from bilder import BILDER
HIER = os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
QUELLE = '../_quelle'
ZIEL = 'assets/img'
GROESSEN = {'s': 480, 'm': 900, 'l': 1440, 'x': 2200}
Q = {'s': 74, 'm': 76, 'l': 78, 'x': 78}
os.makedirs(ZIEL, exist_ok=True)
# Neu gerechnete Fotos (24.10.2026): nur, was nach dem Vergleich mit dem Original freigegeben ist (_quelle/ki-2026-10-24/freigabe.json)
KI_ORDNER = os.path.join(QUELLE, 'ki-2026-10-24')
KI = {k: os.path.join(KI_ORDNER, k + '.png') for k in (json.load(open(os.path.join(KI_ORDNER, 'freigabe.json'))) if os.path.exists(os.path.join(KI_ORDNER, 'freigabe.json')) else [])
      if os.path.exists(os.path.join(KI_ORDNER, k + '.png'))}

def finde(name):
    if name.startswith('../'):
        p = os.path.join(HIER, name)
        return p if os.path.exists(p) else None
    p = os.path.join(QUELLE, name)
    if os.path.exists(p): return p
    m = re.search(r'_(\d{12,14})_', name)
    if not m: return None
    stamm = m.group(1)
    rest = name.split(stamm + '_', 1)[1].rsplit('.', 1)[0]
    kand = [f for f in os.listdir(QUELLE) if stamm in f]
    if not kand: return None
    kand.sort(key=lambda f: (0 if f.startswith('castel_') else 1 if f.startswith('2400') else 2 if f.startswith('1920') else 3, -os.path.getsize(os.path.join(QUELLE, f))))
    # gleicher Reststamm bevorzugt (z. B. castellsuite03 statt castellsuite01)
    best = [f for f in kand if rest[:12] and rest[:12] in f] or kand
    return os.path.join(QUELLE, best[0])

def main():
    alles = '--alles' in sys.argv
    abbild = json.load(open(os.path.join(ZIEL, '_abbild.json'))) if os.path.exists(os.path.join(ZIEL, '_abbild.json')) else {}
    alt_masse = json.load(open(os.path.join(ZIEL, '_masse.json'))) if os.path.exists(os.path.join(ZIEL, '_masse.json')) else {}
    masse = {}
    fehlt = []
    for key, (name, alt) in BILDER.items():
        src = finde(name)
        if not src: fehlt.append((key, name)); continue
        ki = KI.get(key)   # 24.10.2026: neu gerechnete Fassung (Robert «ja deutlich besser»), auf das Seitenverhältnis des Originals zugeschnitten
        if ki: src = ki
        ziele = {g: os.path.join(ZIEL, f'{key}-{g}.webp') for g in GROESSEN}
        # neue Quelle für denselben Schlüssel (Foto getauscht) baut immer neu, auch wenn die Datei älter ist
        gleich = (alt_masse.get(key) or [None, None, None])[2] == os.path.relpath(src, HIER)
        aktuell = gleich and all(os.path.exists(z) and os.path.getmtime(z) >= os.path.getmtime(src) for z in ziele.values()) and key in abbild
        im = Image.open(src); im = ImageOps.exif_transpose(im).convert('RGB')
        if ki:
            o = Image.open(finde(name)); ow, oh = ImageOps.exif_transpose(o).size; r = ow / oh; kw, kh = im.size
            if kw / kh > r: nw = round(kh * r); im = im.crop(((kw - nw) // 2, 0, (kw - nw) // 2 + nw, kh))
            else: nh = round(kw / r); im = im.crop((0, (kh - nh) // 2, kw, (kh - nh) // 2 + nh))
        w, h = im.size; masse[key] = [w, h, os.path.relpath(src, HIER)]
        if aktuell and not alles: continue
        neu = alles or not gleich
        for g, br in GROESSEN.items():
            if br >= w and g != 's':
                # nicht hochrechnen: grösste Stufe = Quelle, kleinere Kopien bleiben
                if os.path.exists(ziele[g]) and not neu: continue
                im.save(ziele[g], 'WEBP', quality=Q[g], method=6); continue
            k = im.copy(); k.thumbnail((br, br * 10), Image.LANCZOS)
            k.save(ziele[g], 'WEBP', quality=Q[g], method=6)
        t = im.copy(); t.thumbnail((24, 24), Image.LANCZOS)
        b = io.BytesIO(); t.save(b, 'JPEG', quality=50); abbild[key] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
        print('·', key, w, 'x', h)
    json.dump(abbild, open(os.path.join(ZIEL, '_abbild.json'), 'w'))
    json.dump(masse, open(os.path.join(ZIEL, '_masse.json'), 'w'), indent=0)
    for k, n in fehlt: print('FEHLT', k, n)
    print(len(BILDER) - len(fehlt), 'Bilder gebaut,', len(fehlt), 'fehlen')

if __name__ == '__main__': main()
