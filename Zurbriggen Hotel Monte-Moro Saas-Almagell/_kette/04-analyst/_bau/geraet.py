# Fassung 2 (Robert 17.10.2026, Master 1b Nr. 13): Geräte nur als freigestellte Blender-Renders.
# Vorlage Carlton-Europe _werkbank/geraet/handy.png + handy.json, laptop.png + laptop.json: die Aufnahme sitzt im Schirm-Rechteck,
# das Gehäuse (mit Loch) liegt darüber. Der rote Kreis wird in die Aufnahme gezeichnet, er steht sofort mit dem Bild.
#   python3 geraet.py → ../potential/geraete/<id>.webp + geraete.json (Breite, Höhe, Adresse)
import json, os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); ST = H + '/stellen/'
G = os.path.expanduser('~/Desktop/Website-Projekte/Carlton-Europe Interlaken/_werkbank/geraet/')
OUT = os.path.join(os.path.dirname(H), 'potential', 'geraete'); os.makedirs(OUT, exist_ok=True)
LAGE = json.load(open(ST + 'lage.json'))
ROT = (196, 58, 36)
BOX = {'2.1c': {'x': 34, 'y': 354, 'w': 172, 'h': 19}}
HJ = json.load(open(G + 'handy.json')); LJ = json.load(open(G + 'laptop.json'))
HANDY = Image.open(G + 'handy.png').convert('RGBA'); LAPTOP = Image.open(G + 'laptop.png').convert('RGBA')
INFO = {}

def kreis(im, b, f, pad=10, breite=5):
    """Textmarker statt Kreis (Robert 17.10.2026: Kreise überlappen und schneiden Buchstaben): weicher roter Streifen hinter der Stelle, kräftige Linie darunter."""
    if not b: return
    from PIL import ImageChops
    x0, y0, x1, y1 = (b['x'] - 4) * f, (b['y'] - 2) * f, (b['x'] + b['w'] + 4) * f, (b['y'] + b['h'] + 2) * f
    ol = Image.new('RGB', im.size, (255, 255, 255)); d = ImageDraw.Draw(ol)
    d.rounded_rectangle((x0, y0, x1, y1), radius=round(4 * f), fill=(246, 178, 160))
    im.paste(ImageChops.multiply(im, ol))
    d2 = ImageDraw.Draw(im); lw = max(3, round(breite * .25))
    d2.rounded_rectangle((x0, y1 - lw, x1, y1), radius=lw // 2, fill=ROT)

def schatten(c, staerke=.30):
    """Robert 17.10.2026: «Mach die Schatten nur ganz dezent einfach hinter dem Telefon, dass man so einen 3D-Effekt hat.» Leise, knapp unter dem Gerät,
    läuft innerhalb des Bildes weich aus (nie abgehackt). Steht im Bild, kein Seitenschatten."""
    from PIL import ImageFilter
    bb = c.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox(); c = c.crop(bb); W, H = c.size; r = round(W * .06)
    leer = Image.new('RGBA', (W + 2 * r, H + 2 * r), (0, 0, 0, 0))
    m = Image.new('L', leer.size, 0); m.paste(c.split()[3], (r, r + round(W * .014)))
    m = m.filter(ImageFilter.GaussianBlur(W * .018)).point(lambda v: round(v * staerke))
    sch = Image.new('RGBA', leer.size, (6, 18, 34, 0)); sch.putalpha(m)
    leer.alpha_composite(sch); leer.alpha_composite(c, (r, r))
    return leer, (bb[0] - r, bb[1] - r)   # Lage des Ergebnisses im Eingangsbild

def handy3d(id):
    """Blender-Render (b3d/handy.py): Aufnahme als Bildschirm-Textur, gerade von vorn, Kantenlicht, freigestellt; dazu der leise Schatten.
    Die Stelle (grünes Feld im zweiten Durchgang) wird als Prozent-Rechteck für den Lichtkegel mitgeschrieben."""
    import numpy as np
    im = Image.open(f'{H}/b3d/out/{id}.png').convert('RGBA')
    mk = np.array(Image.open(f'{H}/b3d/out/{id}_mark.png').convert('RGBA'))
    c, (ox, oy) = schatten(im)
    g = (mk[:, :, 1] > 120) & (mk[:, :, 0] < 90) & (mk[:, :, 3] > 0); gy, gx = np.nonzero(g)
    s0 = 700 / c.width; cw, ch = c.size; c = c.resize((700, round(c.height * s0)), Image.LANCZOS)
    c.save(f'{OUT}/{id}.webp', 'WEBP', quality=86, method=6)
    INFO[id] = {'typ': 'handy', 'w': c.width, 'h': c.height, 'url': LAGE.get(id, {}).get('url'), 'b3d': True}
    if len(gx):
        INFO[id]['mark'] = [round((gx.min() - ox) / cw * 100, 2), round((gy.min() - oy) / ch * 100, 2), round((gx.max() - gx.min()) / cw * 100, 2), round((gy.max() - gy.min()) / ch * 100, 2)]

def handy(id, ziel=None, kein_kreis=False):
    a = Image.open(ST + id + '.png').convert('RGB'); l = LAGE.get(id, {})
    f = a.width / 390
    if not kein_kreis: kreis(a, BOX.get(id) or l.get('box'), f, pad=14, breite=round(8 * f))   # kräftig: im Gerät gut 3 px auf dem Schirm
    sw, sh = HJ['schirm_groesse']; x0, y0 = round(HJ['schirm'][0] * HJ['groesse'][0]), round(HJ['schirm'][1] * HJ['groesse'][1])
    a = a.resize((sw, round(a.height * sw / a.width)), Image.LANCZOS).crop((0, 0, sw, sh))
    c = Image.new('RGBA', HANDY.size, (0, 0, 0, 0)); c.paste(a, (x0, y0)); c.alpha_composite(HANDY)
    c = c.crop(c.getbbox()); c = c.resize((620, round(c.height * 620 / c.width)), Image.LANCZOS)
    n = (ziel or id); c.save(f'{OUT}/{n}.webp', 'WEBP', quality=82, method=6)
    INFO[n] = {'typ': 'handy', 'w': c.width, 'h': c.height, 'url': l.get('url')}

def laptop(id, tab=None, adresse=None, ziel=None):
    a = Image.open(ST + id + '.png').convert('RGB'); l = LAGE.get(id, {})
    f = a.width / 1440
    kreis(a, BOX.get(id) or l.get('box'), f, pad=24, breite=round(20 * f))   # kräftig: im Rechner gut 3 px auf dem Schirm
    FW, FH = LJ['fenster']
    bx = BOX.get(id) or l.get('box'); mark = None
    if bx: mark = tuple(v * FW / a.width for v in ((bx['x'] - 4) * f, (bx['y'] - 2) * f, (bx['x'] + bx['w'] + 4) * f, (bx['y'] + bx['h'] + 2) * f))
    if tab:   # Leiste eines Browsers mit dem echten Titel und der echten Adresse der Seite (Master 1b Nr. 2)
        k = 64; a = a.resize((FW, round(a.height * FW / a.width)), Image.LANCZOS)
        bild = Image.new('RGB', (FW, FH), (236, 236, 238)); bild.paste(a.crop((0, 0, FW, FH - k)), (0, k)); d = ImageDraw.Draw(bild)
        fo = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 17); fk = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 15)
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]): d.ellipse((18 + i * 22, 13, 30 + i * 22, 25), fill=c)
        d.rounded_rectangle((100, 6, 520, 34), 8, fill=(255, 255, 255)); d.text((114, 12), tab, font=fo, fill=(40, 40, 40))
        d.rounded_rectangle((100, 38, 900, 60), 7, fill=(255, 255, 255)); d.text((114, 41), adresse, font=fk, fill=(90, 90, 90))
        tw = d.textlength(tab, font=fo); 
        for o in range(5): d.ellipse((96 - o, 2 - o, 120 + tw + o, 38 + o), outline=ROT)
        z = bild.crop((0, 0, 620, 340)).resize((1240, 680), Image.LANCZOS); z.save(f'{OUT}/d8.1z.webp', 'WEBP', quality=88)
        INFO['d8.1z'] = {'typ': 'zoom', 'w': z.width, 'h': z.height, 'url': l.get('url')}
        a = bild; mark = (96, 2, 124 + tw, 38)
    else:
        a = a.resize((FW, round(a.height * FW / a.width)), Image.LANCZOS)
        if a.height < FH: z = Image.new('RGB', (FW, FH), (255, 255, 255)); z.paste(a, (0, 0)); a = z
        a = a.crop((0, 0, FW, FH))
    x0, y0, x1, y1 = LJ['render']['schirm_px']; s = LAPTOP.width / 3300 if LAPTOP.width != 3300 else 1
    gw, gh = LJ['groesse']; sx = round(LJ['schirm'][0] * gw); sy = round(LJ['schirm'][1] * gh); sw = round(LJ['schirm'][2] * gw); sh = round(LJ['schirm'][3] * gh)
    fx, fy = sw / a.width, sh / a.height
    a = a.resize((sw, sh), Image.LANCZOS)
    c = Image.new('RGBA', LAPTOP.size, (0, 0, 0, 0)); c.paste(a, (sx, sy)); c.alpha_composite(LAPTOP)
    c, (ox, oy) = schatten(c, .26)
    s0 = 1300 / c.width; c = c.resize((1300, round(c.height * s0)), Image.LANCZOS)
    n = (ziel or id); c.save(f'{OUT}/{n}.webp', 'WEBP', quality=84, method=6)
    INFO[n] = {'typ': 'laptop', 'w': c.width, 'h': c.height, 'url': l.get('url')}
    if mark:   # Lage der Stelle im fertigen Bild (Prozent), für den Lichtkegel zur Lupe
        mx0, my0, mx1, my1 = [(sx + v * fx - ox) * s0 if i % 2 == 0 else (sy + v * fy - oy) * s0 for i, v in enumerate(mark)]
        INFO[n]['mark'] = [round(mx0 / c.width * 100, 2), round(my0 / c.height * 100, 2), round((mx1 - mx0) / c.width * 100, 2), round((my1 - my0) / c.height * 100, 2)]

for i in ['1.1', '1.1b', '1.2', '1.3', '2.1', '2.1c', '2.2', '2.2b', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3', '5.1', '5.1b', '6.1', '6.2', '6.3', '7.1', '7.1b', '7.2', '8.2', '8.2b', '9.1']:
    if os.path.exists(ST + i + '.png'): handy(i, kein_kreis=(i == '9.1'))
for i in json.load(open(H + '/b3d/jobs.json')):
    i = os.path.basename(i['out'])[:-4]
    if os.path.exists(f'{H}/b3d/out/{i}_mark.png'): handy3d(i)
laptop('d1.1'); laptop('d2.1'); laptop('d6.3')
laptop('d8.1', tab='Aktuelles | Hotel Monte Moro Saas-Almagell', adresse='monte-moro.ch/de/', ziel='d8.1t')
laptop('9.1b')
for i in ['4.1p', '6.1p', 'a.1p', 'a.2p']:   # Ausschnitte aus echten PDFs, als Blatt ohne Gerät
    d = Image.open(ST + i + '.png').convert('RGB')
    if d.width > 1100: d = d.resize((1100, round(d.height * 1100 / d.width)), Image.LANCZOS)
    d.save(f'{OUT}/{i}.webp', 'WEBP', quality=84, method=6)
    INFO[i] = {'typ': 'dok', 'w': d.width, 'h': d.height, 'url': 'https://www.zerone.ch/agb/agb.pdf' if i.startswith('a.') else 'https://www.monte-moro.ch/images/restaurant/speisekarte.pdf'}
json.dump(INFO, open(H + '/geraete.json', 'w'), indent=1)
print(len(INFO), 'Geräte')
