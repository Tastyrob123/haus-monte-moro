# Prüfbogen: alle Beweisbilder klein mit rotem Kreis, 12 je Bogen → /tmp scratch (nur zum Ansehen, nie für Robert)
import os, json, sys
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); ST = H + '/stellen/'
OUT = sys.argv[1]
L = json.load(open(ST + 'lage.json')) if os.path.exists(ST + 'lage.json') else {}
ids = [f[:-4] for f in sorted(os.listdir(ST)) if f.endswith('.png')]
def key(i):
    import re; m = re.match(r'(\d+)\.(\d+)(.*)', i); return (int(m.group(1)), int(m.group(2)), m.group(3)) if m else (99, 0, i)
ids.sort(key=key)
F = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22, index=1)
W = 260
tiles = []
for i in ids:
    im = Image.open(ST + i + '.png').convert('RGB'); l = L.get(i, {})
    s = W / im.width; im = im.resize((W, round(im.height * s)))
    b = l.get('box')
    if b:
        d = ImageDraw.Draw(im); f = im.width / l.get('W', 390)
        d.ellipse((b['x'] * f - 8, b['y'] * f - 6, (b['x'] + b['w']) * f + 8, (b['y'] + b['h']) * f + 6), outline=(220, 40, 40), width=3)
    if im.height > 640: im = im.crop((0, 0, W, 640))
    tiles.append((i, im))
per = 12; n = 0
for k in range(0, len(tiles), per):
    chunk = tiles[k:k + per]; cols = 6; rows = (len(chunk) + cols - 1) // cols
    sh = Image.new('RGB', (cols * (W + 12) + 12, rows * (660 + 40) + 12), (240, 240, 240)); d = ImageDraw.Draw(sh)
    for j, (i, im) in enumerate(chunk):
        x = 12 + (j % cols) * (W + 12); y = 12 + (j // cols) * 700
        sh.paste(im, (x, y + 30)); d.text((x, y), i, font=F, fill=(0, 0, 0))
    sh.save(f'{OUT}/bogen-{n}.png'); n += 1
print(n, 'Bögen', len(tiles), 'Bilder')
