#!/usr/bin/env python3
"""Prüftafel der Schlussprüfung in der Sitzung (Oberchef 08.11.2026).
Aufruf: python3 cloud/tafel_sitzung.py <aus-ende> <ziel-ordner>
Schreibt <ziel>/index.html (Tafel: Ziel × Zustände × Funde × Oberflächenprüfung), <ziel>/b/<k>-*.jpg (je Ziel bis zu 6 Zustandsbilder,
1440 und 390), <ziel>/zahlen.json. Nur Dateien aus dem Lauf, nichts erfunden."""
import glob, html, json, os, random, sys
from PIL import Image
A, Z = sys.argv[1], sys.argv[2]; e = html.escape
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = json.load(open(os.path.join(WS, 'cloud', 'haus.json'), encoding='utf-8'))
ZL = json.load(open(os.path.join(WS, H['tor_ziele']), encoding='utf-8'))['ziele']
os.makedirs(os.path.join(Z, 'b'), exist_ok=True)
random.seed(11)

def zaehle(k):
    d = os.path.join(A, k); inv = os.path.join(d, 'inventar.json')
    if not os.path.exists(inv): return None
    j = json.load(open(inv, encoding='utf-8')); f = 0; zs = len(j.get('zustaende', []))
    f += sum(len(s.get('funde') or []) for s in j.get('zustaende', []))
    br = {'1440': zs}
    for s in sorted(glob.glob(os.path.join(d, 'stich-*.json'))):
        sj = json.load(open(s, encoding='utf-8')); b = os.path.basename(s)[6:-5]
        br[b] = len(sj.get('zustaende', [])); f += sum(len(x.get('funde') or []) for x in sj.get('zustaende', []))
    return dict(zustaende=zs, breiten=br, funde=f, nicht_erreicht=len(j.get('nichtErreicht') or []))

def oberflaeche(url):
    n = os.path.join(A, 'oberflaeche', ''.join(c if c.isalnum() else '_' for c in url) + '.txt')
    if not os.path.exists(n): return None
    t = open(n, encoding='utf-8').read().strip().splitlines()
    return t[-1] if t else None

def bilder(k):
    d = os.path.join(A, k); aus = []
    for teil, n in (('bilder', 4), ('stich-390', 2)):
        fs = sorted(glob.glob(os.path.join(d, teil, '*.jpg')))
        for i, f in enumerate(random.sample(fs, min(n, len(fs)))):
            im = Image.open(f).convert('RGB'); im.thumbnail((720, 720))
            nm = f'{k}-{teil}-{i}.jpg'; im.save(os.path.join(Z, 'b', nm), quality=78); aus.append(nm)
    return aus

zeilen, zahlen, summe = [], {}, dict(zustaende=0, funde=0, nicht_erreicht=0)
for z in ZL:
    k = z['k']; c = zaehle(k); o = oberflaeche(z['url']); zahlen[k] = dict(c or {}, oberflaeche=o, url=z['url'], name=z['name'])
    if c:
        for x in summe: summe[x] += c[x]
    gruen = c and c['funde'] == 0 and c['nicht_erreicht'] == 0 and (o is None or o == 'BESTANDEN')
    bs = bilder(k) if c else []
    zeilen.append(f"<tr class='{'ok' if gruen else 'rot'}'><td><b>{e(z['name'])}</b><br><small>{e(k)}</small></td>"
                  f"<td>{c['zustaende'] if c else '–'}<br><small>{e(' · '.join(f'{b}: {n}' for b, n in (c or {}).get('breiten', {}).items()))}</small></td>"
                  f"<td>{c['funde'] if c else '–'}</td><td>{c['nicht_erreicht'] if c else '–'}</td><td>{e(o or '–')}</td>"
                  f"<td class='bi'>{''.join(f'<a href=\"b/{b}\"><img loading=lazy src=\"b/{b}\"></a>' for b in bs)}</td></tr>")
json.dump(dict(summe=summe, ziele=zahlen), open(os.path.join(Z, 'zahlen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
alle_gruen = all(r.startswith("<tr class='ok'") for r in zeilen)
open(os.path.join(Z, 'index.html'), 'w', encoding='utf-8').write(f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prüftafel Monte-Moro</title><style>
body{{margin:0;background:#F5F2EE;color:#13263A;font:16px/1.5 system-ui,-apple-system,sans-serif}}main{{max-width:1280px;margin:0 auto;padding:40px 16px}}
h1{{font-size:clamp(32px,6vw,56px);margin:0 0 6px;color:#0A2A4A}}.kopf{{display:flex;gap:28px;flex-wrap:wrap;margin:22px 0 30px}}
.kopf div{{background:#0A2A4A;color:#F5F2EE;border-radius:14px;padding:16px 22px}}.kopf b{{display:block;font-size:34px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden}}td,th{{padding:10px 12px;border-bottom:1px solid #E7E1DC;vertical-align:top;text-align:left}}
th{{background:#0D3F6F;color:#F5F2EE;font-weight:500}}tr.ok td:nth-child(3){{color:#268369;font-weight:600}}tr.rot{{background:#fbe9e1}}
.bi{{display:flex;flex-wrap:wrap;gap:6px}}.bi img{{height:90px;border-radius:6px;border:1px solid #D6CCC1}}small{{color:#4A5D70}}
@media(max-width:760px){{td:nth-child(6),th:nth-child(6),td:nth-child(4),th:nth-child(4){{display:none}}table{{font-size:13px;width:100%}}td,th{{padding-left:5px;padding-right:5px}}td:first-child small{{word-break:break-all}}}}</style></head><body><main>
<h1>Prüftafel · Hotel Monte-Moro</h1><p>Schlussprüfung in der Sitzung, 8. November 2026: jedes Werkzeug und jede Seite der Werkbank mit dem Abnahme-Tor
(Start, jeder Navigationspunkt, jeder Reiter, jedes Fenster, je Gruppe drei Stücke, höchstens 40 Zustände) in 1440, 1280, 1000 und 390 px,
dazu die Oberflächenprüfung. Chromium (WebKit liess sich in der Cloud nicht laden). Bilder: zufällige Zustände aus dem Lauf.</p>
<div class="kopf"><div><b>{len(ZL)}</b>Ziele</div><div><b>{summe['zustaende']}</b>Zustände (1440)</div><div><b>{summe['funde']}</b>Funde</div><div><b>{summe['nicht_erreicht']}</b>nicht erreicht</div><div><b>{'grün' if alle_gruen else 'offen'}</b>Ergebnis</div></div>
<table><tr><th>Ziel</th><th>Zustände</th><th>Funde</th><th>Nicht erreicht</th><th>Oberfläche</th><th>Bilder</th></tr>{''.join(zeilen)}</table></main></body></html>""")
print('Ziele', len(ZL), summe, 'grün' if alle_gruen else 'offen')
