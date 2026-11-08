# Fassung 3 (Master 1b Nr. 15, «Was genau»): die Stelle gross herausgezogen, mit Ankerpunkten (in Prozent) für Hinweislinien im HTML.
# Quellen: stellen2/<id>.png + anker.json (Website, 3-fache Dichte), Speisekarte (pdftotext -bbox), Reiter-Bild aus geraet.py.
#   python3 ausschnitt.py → ../potential/ausschnitte/<id>.webp + ausschnitte.json {id: {w, h, anker:[[x%, y%, w%, h%]], url}}
import json, os, re, subprocess, html
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(os.path.dirname(H), 'potential', 'ausschnitte'); os.makedirs(OUT, exist_ok=True)
A = json.load(open(H + '/stellen3/anker.json')); INFO = {}
KARTE = os.path.expanduser('~/Desktop/Website-Projekte/Zurbriggen Hotel Monte-Moro Saas-Almagell/_quelle/website/pdf/speisekarte.pdf')
def hoch_genug(x0, y0, x1, y1, n, Hmax):
    need = max(0, (x1 - x0) * (0.16 * n + 0.04) - (y1 - y0))
    y0 = max(0, y0 - need / 2); y1 = min(Hmax, y1 + need / 2)
    if (y1 - y0) < (x1 - x0) * (0.16 * n + 0.04): y0 = max(0, y1 - (x1 - x0) * (0.16 * n + 0.04)); y1 = min(Hmax, y0 + (x1 - x0) * (0.16 * n + 0.04))
    return y0, y1
def schnapp(y0, y1, zeilen, Hmax, luft=4):
    """Robert 17.10.2026: «Bei solchen Sachen schneidest du durch die Wörter durch.» Ober- und Unterkante nur zwischen zwei Zeilen."""
    for _ in range(30):
        alt = (y0, y1)
        for t, b in zeilen:
            if t < y0 < b: y0 = t - luft
            if t < y1 < b: y1 = b + luft
        if (y0, y1) == alt: break
    return max(0, y0), min(Hmax, y1)
SCHRIFT = {}   # Schriftgrösse der Anker in Bildpunkten des Ausschnitts (für die Prüfung «Lesbar oder raus»)
def speichern(id, im, boxen, url, marker=None):
    W, Hh = im.size
    marker = marker or [[b] for b in boxen]
    marker = [[[r[0], r[1], min(r[2], W - r[0] - 2), r[3]] for r in m if r[0] < W - 8] for m in marker]   # je Anker die Zeilenrechtecke (Textmarker statt Kreis, Robert 17.10.2026)
    if im.width > 1500:
        s_ = 1500 / im.width; marker = [[[v * s_ for v in r] for r in m] for m in marker]
    if im.width > 1500: s = 1500 / im.width; im = im.resize((1500, round(im.height * s)), Image.LANCZOS); boxen = [[v * s for v in b] for b in boxen]; W, Hh = im.size
    im.save(f'{OUT}/{id}.webp', 'WEBP', quality=86, method=6)
    INFO[id] = {'marker': [[[round(r[0] / W * 100, 2), round(r[1] / Hh * 100, 2), round(r[2] / W * 100, 2), round(r[3] / Hh * 100, 2)] for r in m] for m in marker], 'w': W, 'h': Hh, 'url': url, 'anker': [[round(b[0] / W * 100, 2), round(b[1] / Hh * 100, 2), round(b[2] / W * 100, 2), round(b[3] / Hh * 100, 2)] for b in boxen]}
def web(id, pad=16, nur=None, name=None, fenster=None):
    """Fassung 4 (Robert 17.10.2026: «auf dem Telefon ist alles in zwei Zeilen und du hast vier Zeilen rausgemacht»): Aufnahme aus derselben Ansicht wie
    das Gerät, ganze Zeilen der Spalte, in der die Stelle steht. Oben und unten endet der Ausschnitt zwischen zwei Zeilen, seitlich nach dem längsten Wort."""
    a = A[id]; f = a['f']; im = Image.open(H + '/stellen3/' + id + '.png').convert('RGB')
    bx = [x for k, x in enumerate(a['anker']) if not x.get('fehlt') and (nur is None or k in nur)]
    zl = [z for z in a['zeilen'] if z[1] - z[0] < 70]
    y0 = max(0, min(b['y'] for b in bx) - pad); y1 = min(a['H'], max(b['y'] + b['h'] for b in bx) + pad)
    x0 = min(b['x'] for b in bx); x1 = max(b['x'] + b['w'] for b in bx)
    for _ in range(30):   # Spalte wachsen lassen: jede Zeile im Band, die die Spalte berührt, kommt ganz hinein
        alt = (x0, x1, y0, y1)
        y0, y1 = schnapp(y0, y1, [z[:2] for z in zl if not (z[3] < x0 or z[2] > x1)], a['H'])
        for t, b_, l, r in zl:
            if b_ > y0 and t < y1 and not (r < x0 - 2 or l > x1 + 2): x0 = min(x0, l); x1 = max(x1, r)
        if (x0, x1, y0, y1) == alt: break
    x0 = max(0, x0 - 10); x1 = min(a['W'], x1 + 10)
    if fenster and x1 - x0 > fenster:
        # breiter als lesbar (Laptop, 1440): Zeilen bleiben, wie sie sind, rechts endet der Ausschnitt; ein Wort, das über den Rand liefe, fällt ganz weg
        x1 = x0 + fenster
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        from PIL import ImageFont
        W_ = [w for w in a.get('worte', []) if w[3] > y0 and w[1] < y1 and w[2] > x0]
        for l, t, r, b_ in [w for w in W_ if w[0] < x1 < w[2]]:
            zeile = sorted([w for w in W_ if abs(w[1] - t) < 2], key=lambda w: w[0]); eh = (b_ - t) * 1.05   # Platz für «…»
            bleibt = [w for w in zeile if w[2] + eh <= x1]
            weg_ab = min([w[0] for w in zeile if w not in bleibt] + [x1])
            grund = im.getpixel((max(0, round((weg_ab - 3) * f)), round((t + b_) / 2 * f)))
            d.rectangle((round((weg_ab - 1) * f), round((t - 1) * f), round(x1 * f) + 2, round((b_ + 1) * f)), fill=grund)
            if bleibt:   # Auslassungspunkte hinter dem letzten ganzen Wort: die Zeile geht auf der Seite weiter
                lw = bleibt[-1]; box = im.crop((round(lw[0] * f), round(lw[1] * f), round(lw[2] * f), round(lw[3] * f)))
                farbe = min(box.get_flattened_data() if hasattr(box, 'get_flattened_data') else box.getdata(), key=sum)
                fo = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', round((b_ - t) * .86 * f))
                d.text((round((lw[2] + (b_ - t) * .12) * f), round(t * f)), '…', font=fo, fill=farbe)
    c = im.crop((round(x0 * f), round(y0 * f), round(x1 * f), round(y1 * f)))
    VB[name or id] = round(x1 - x0, 1); FS[name or id] = min(b['fs'] for b in bx)
    speichern(name or id, c, [[(b['x'] - x0) * f, (b['y'] - y0) * f, b['w'] * f, b['h'] * f] for b in bx], a['url'],
              [[[(r[0] - x0) * f, (r[1] - y0) * f, r[2] * f, r[3] * f] for r in (b.get('zr') or [[b['x'], b['y'], b['w'], b['h']]])] for b in bx])
VB, FS = {}, {}   # Breite in Bildschirmpunkten des Geräts und kleinste Schrift dort: daraus rechnet bau.py die Vergrösserung
def pdf(id, seite, worte, dpi=300, pad=40, ganze_breite=False, breite_pt=250):
    x = subprocess.run(['pdftotext', '-bbox', '-f', str(seite), '-l', str(seite), KARTE, '-'], capture_output=True, text=True).stdout
    pw = float(re.search(r'<page width="([\d.]+)"', x).group(1)); ph = float(re.search(r'height="([\d.]+)"', x).group(1))
    W_ = [(html.unescape(m.group(5)), *map(float, m.group(1, 2, 3, 4))) for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x)]
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(seite), '-l', str(seite), '-png', '-singlefile', KARTE, H + '/_tmp'], check=True)
    im = Image.open(H + '/_tmp.png').convert('RGB'); os.remove(H + '/_tmp.png'); sx, sy = im.width / pw, im.height / ph
    boxen = []
    for folge in worte:   # Folge von Wörtern, die nacheinander stehen
        for i in range(len(W_)):
            if all(i + k < len(W_) and folge[k] in W_[i + k][0] for k in range(len(folge))):
                t = W_[i:i + len(folge)]; boxen.append([min(w[1] for w in t) * sx, min(w[2] for w in t) * sy, (max(w[3] for w in t) - min(w[1] for w in t)) * sx, (max(w[4] for w in t) - min(w[2] for w in t)) * sy]); break
        else: print(id, 'FEHLT', folge)
    x0 = max(0, min(b[0] for b in boxen) - 14 * sx); x1 = min(im.width, x0 + breite_pt * sx)
    y0 = max(0, min(b[1] for b in boxen) - pad); y1 = min(im.height, max(b[1] + b[3] for b in boxen) + pad)
    y0, y1 = hoch_genug(x0, y0, x1, y1, len(boxen), im.height)
    # Kanten nur zwischen Wörtern und Zeilen (Schmuckschrift über 25 pt bleibt aussen vor):
    # links beginnt der Ausschnitt vor dem ersten Wort der Zeile, rechts endet er nach dem letzten Wort, das vor der Breitengrenze beginnt
    wb = [(w[1] * sx, w[2] * sy, w[3] * sx, w[4] * sy) for w in W_ if (w[4] - w[2]) < 25]; wt = [w[0] for w in W_ if (w[4] - w[2]) < 25]
    rechts_min = max(b[0] + b[2] for b in boxen) + 6
    grenze = x0 + breite_pt * sx
    for _ in range(40):
        alt = (x0, x1, y0, y1)
        band = [w for w in wb if not (w[3] <= y0 or w[1] >= y1)]
        for a0, b0, a1, b1 in band:
            if a0 < x0 < a1: x0 = a0 - 8
        x1 = max([w[2] for w in band if w[0] < grenze] + [x0 + 10]) + 8
        fr = [w[0] for w, t in zip(wb, wt) if t == 'Fr.' and not (w[3] <= y0 or w[1] >= y1) and w[0] > rechts_min]
        if fr and id in ('z12p',):   # Röstiliste: die Beschreibungen stehen nicht als Text im PDF; der Schnitt liegt vor der Preisspalte, wo keine Zeile mehr läuft
            x1 = min(fr) - 1.5 * sx
        for a0, b0, a1, b1 in wb:
            if a1 <= x0 or a0 >= x1: continue
            if b0 < y0 < b1: y0 = b0 - 6
            if b0 < y1 < b1: y1 = b1 + 6
        if (x0, x1, y0, y1) == alt: break
    x1 = min(im.width, x1)
    x0 = max(0, x0); y0 = max(0, y0); y1 = min(im.height, y1)
    c = im.crop((round(x0), round(y0), round(x1), round(y1)))
    SCHRIFT[id] = min(b[3] for b in boxen) * 0.75 * (min(1, 1500 / c.width))   # Wortkasten → Schriftgrösse
    speichern(id, c, [[b[0] - x0, b[1] - y0, b[2], b[3]] for b in boxen], 'https://www.monte-moro.ch/images/restaurant/speisekarte.pdf')
FENSTER = {'z01a': 520}
TEIL = {'z01': [('z01a', [0, 1]), ('z01b', [2])], 'z02': [('z02a', [0, 1]), ('z02b', [2, 3])], 'z03a': [('z03a', [0, 1])], 'z08b': [('z08b', [1, 2])]}
for i in A:
    for name, nur in TEIL.get(i, [(i, None)]): web(i, nur=nur, name=name, fenster=FENSTER.get(name))
pdf('z06p', 4, [['Rösti', 'Albert'], ['Rösti', 'Indian', 'Style']], pad=60, breite_pt=400)   # ganze Zeilen bis zum Preis: eine Beschreibung läuft bis an die Preisspalte
pdf('z06q', 5, [['Monte-Moro'], ['Förster']], pad=60)
pdf('z10p', 7, [['Cuvee', 'Special'], ['(wurde', 'von', 'Fabian', 'selber', 'kreiert)']], pad=120)
pdf('z12p', 4, [['Rösti', 'Tschug', 'Tschug'], ['Apfelmus', 'und', 'Calvados', 'flambiert,']], pad=150)
# Reiter des Browsers aus geraet.py (Titel und Adresse echt, die Leiste nachgezeichnet)
z = Image.open(os.path.join(os.path.dirname(H), 'potential', 'geraete', 'd8.1z.webp')).convert('RGB'); s = z.width / 620
z = z.crop((round(90 * s), 0, round(420 * s), round(200 * s))); _dx = 90
from PIL import ImageFont, ImageDraw
fo = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 17); tw = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength('Aktuelles | Hotel Monte Moro Saas-Almagell', font=fo)
tw1 = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength('Aktuelles', font=fo)
speichern('z11', z, [[(114 - _dx) * s, 10 * s, tw1 * s, 18 * s], [(114 - _dx + tw1 + 6) * s, 10 * s, min(tw - tw1 - 6, 320 - tw1) * s, 18 * s], [(114 - _dx) * s, 40 * s, 130 * s, 16 * s]], 'https://www.monte-moro.ch/de/')
for k, v in SCHRIFT.items(): INFO[k]['schrift_px'] = round(v, 1)
for k in VB: INFO[k]['vb'] = VB[k]; INFO[k]['fs'] = round(FS[k], 2); INFO[k]['desk'] = A[k[:3] if k[:3] in A else k].get('desk', False) if k not in A else A[k].get('desk', False)
json.dump(INFO, open(H + '/ausschnitte.json', 'w'), indent=1)
print(len(INFO), 'Ausschnitte', {k: (v['w'], v['h']) for k, v in INFO.items()})
