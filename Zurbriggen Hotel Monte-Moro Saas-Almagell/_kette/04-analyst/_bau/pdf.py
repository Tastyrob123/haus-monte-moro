# Ausschnitte aus echten PDFs (Speisekarte des Hauses, AGB von zerone) → stellen/<id>.png + pdflage.json
# Stelle mit rotem Kreis, wo ein Wort gemeint ist; ganze Seiten, wo die Seite selbst der Beleg ist (Master 1b Nr. 9).
import subprocess, re, os, json, html
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); OUT = H + '/stellen/'
KARTE = os.path.expanduser('~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle/website/pdf/speisekarte.pdf')
AGB = os.path.join(H, '..', '..', '02-spaeher', '_qa', 'zerone', 'agb.pdf')
DPI = 150
ROT = (181, 68, 44)
def seite(pdf, n, dpi=DPI):
    ziel = OUT + '_tmp'
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(n), '-l', str(n), '-png', '-singlefile', pdf, ziel], check=True)
    im = Image.open(ziel + '.png').convert('RGB'); os.remove(ziel + '.png'); return im
def woerter(pdf, n):
    x = subprocess.run(['pdftotext', '-bbox', '-f', str(n), '-l', str(n), pdf, '-'], capture_output=True, text=True).stdout
    pw = float(re.search(r'<page width="([\d.]+)"', x).group(1)); ph = float(re.search(r'height="([\d.]+)"', x).group(1))
    return pw, ph, [(html.unescape(m.group(5)), *map(float, m.group(1, 2, 3, 4))) for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x)]
def streifen(id, pdf, n, wort, nth=0, folge=1, hoch=520, name=None):
    pw, ph, w = woerter(pdf, n); im = seite(pdf, n); W, Hh = im.size; sx, sy = W / pw, Hh / ph
    treffer = [i for i, t in enumerate(w) if wort in t[0]]
    i = treffer[nth]; teil = w[i:i + folge]
    x0 = min(t[1] for t in teil) * sx; y0 = min(t[2] for t in teil) * sy; x1 = max(t[3] for t in teil) * sx; y1 = max(t[4] for t in teil) * sy
    cy = (y0 + y1) / 2; t0 = max(0, min(Hh - hoch, cy - hoch / 2))
    c = im.crop((0, round(t0), W, round(t0 + hoch))); d = ImageDraw.Draw(c)
    bx = [x0 - 16, y0 - t0 - 10, x1 + 16, y1 - t0 + 10]
    for o in range(5): d.ellipse((bx[0] - o, bx[1] - o, bx[2] + o, bx[3] + o), outline=ROT)
    c.save(OUT + id + '.png'); LAGE[id] = {'pdf': name or os.path.basename(pdf), 'seite': n, 'wort': ' '.join(t[0] for t in teil)}
    print(id, 'Seite', n, LAGE[id]['wort'], c.size)
def ganz(id, pdf, seiten, name=None, oben=None):
    ims = [seite(pdf, n, 110) for n in seiten]
    if oben: ims = [im.crop((0, 0, im.width, round(im.height * oben))) for im in ims]
    gap = 24; W = sum(i.width for i in ims) + gap * (len(ims) - 1); Hh = max(i.height for i in ims)
    c = Image.new('RGB', (W, Hh), (233, 229, 222)); x = 0
    for im in ims: c.paste(im, (x, 0)); x += im.width + gap
    c.save(OUT + id + '.png'); LAGE[id] = {'pdf': name or os.path.basename(pdf), 'seite': '–'.join(map(str, seiten)) if len(seiten) > 1 else seiten[0], 'wort': None}
    print(id, 'Seiten', seiten, c.size)
LAGE = {}
ganz('4.1p', KARTE, [4, 5])
ganz('4.3p', KARTE, [1, 2])
ganz('7.2p', KARTE, [2, 4])
streifen('6.1p', KARTE, 7, 'Fabian', 0, 3, hoch=430)
streifen('a.1p', AGB, 2, 'November', 0, 1, hoch=420, name='zerone.ch/agb/agb.pdf')
streifen('a.2p', AGB, 3, 'gelöscht', 0, 1, hoch=420, name='zerone.ch/agb/agb.pdf')
streifen('a.3p', AGB, 6, 'Immaterialgüterrechte', 0, 1, hoch=420, name='zerone.ch/agb/agb.pdf')
json.dump(LAGE, open(H + '/pdflage.json', 'w'), ensure_ascii=False, indent=1)
