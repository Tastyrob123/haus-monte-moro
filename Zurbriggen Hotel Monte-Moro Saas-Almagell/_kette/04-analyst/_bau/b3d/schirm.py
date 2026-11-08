# Bildschirm-Texturen für b3d/handy.py: Aufnahme (stellen/<id>.png, 390 breit) mit Textmarker an der Stelle, oben 59 pt Statusleiste wie am iPhone,
# dazu die Marken-Textur (schwarz, grünes Feld an der Stelle) für die Lage des Lichtkegels.   python3 b3d/schirm.py
import json, os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ns = {}; exec(open(H + '/geraet.py').read().split('def schatten')[0].replace("H = os.path.dirname(os.path.abspath(__file__))", f"H = {H!r}"), ns)
L = ns['LAGE']; BAND = 59
for j in json.load(open(H + '/b3d/jobs.json')):
    id = os.path.basename(j['out'])[:-4]; box = L[id]['box']
    a = Image.open(H + '/stellen/' + id + '.png').convert('RGB'); f = a.width / 390
    ns['kreis'](a, box, f, pad=14, breite=round(8 * f))
    m = Image.new('RGB', a.size, (0, 0, 0)); ImageDraw.Draw(m).rectangle(((box['x'] - 4) * f, (box['y'] - 2) * f, (box['x'] + box['w'] + 4) * f, (box['y'] + box['h'] + 2) * f), fill=(0, 255, 0))
    for im, ziel, grund in ((a, j['screen'], (255, 255, 255)), (m, j['mark'], (0, 0, 0))):
        im = im.resize((1406, 3054), Image.LANCZOS); b = round(3054 * BAND / 844)
        n = Image.new('RGB', (1406, 3054), grund); n.paste(im.crop((0, 0, 1406, 3054 - b)), (0, b)); n.save(ziel)
    print(id)
