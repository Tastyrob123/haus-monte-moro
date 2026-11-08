# Hotel Monte-Moro (aus Castell Fassung 7): Beweisbilder je Punkt (echte Aufnahmen der Kundenseite, Quelltext-Schirme, PDF-Streifen) → potential/beweise/*.webp + HTML-Figuren.
# Aufnahmen: stellen.js (stellen/<id>.png + lage.json), Quelltext: code.py/code.js, PDF: pdf.py (pdflage.json), Kanal: kanal.py.
import os, json, html
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); ST = H + '/stellen/'
LAGE = json.load(open(ST + 'lage.json')) if os.path.exists(ST + 'lage.json') else {}
PDFL = json.load(open(H + '/pdflage.json')) if os.path.exists(H + '/pdflage.json') else {}
e = lambda s: html.escape(s, quote=False)
# nr → Figuren aus inhalt.py (id, typ, titel, satz); typ: tel = Telefon, fen = Rechner-Fenster, dok = Dokument (PDF). Dazu die Figuren des Teils «Wer hinter der heutigen Seite steht».
import inhalt as I
BEW = {p['nr']: p['beweise'] for b in I.BEREICHE for p in b['punkte']}
BEW['z'] = [('z.1w', 'dok', 'Was die Seite über sich sagt', 'Die Vorlage von zerone und die Fassung von Joomla.')]
BEW['a'] = [('a.1p', 'dok', 'AGB von zerone, Ziffer 4c', 'Kündigung spätestens am 15. November.'), ('a.2p', 'dok', 'AGB von zerone, Ziffer 4f', 'Nach Vertragsablauf werden sämtliche Daten gelöscht.'),
            ('a.3p', 'dok', 'AGB von zerone, Ziffer 8a', 'Die Immaterialgüterrechte bleiben beim Provider.')]
# Rechtecke, die von Hand weiter gezogen sind als das gefundene Wort (Bild angesehen 17.10.2026)
BOX = {'2.1c': {'x': 34, 'y': 354, 'w': 172, 'h': 19}}
def kreis(box, W, Hh, pad=10):
    if not box: return None
    x, y, w, h = box['x'] - pad, box['y'] - pad, box['w'] + 2 * pad, box['h'] + 2 * pad
    x = max(2, x); y = max(2, y); w = min(w, W - 4 - x); h = min(h, Hh - 4 - y)
    return [round(x / W * 100, 2), round(y / Hh * 100, 2), round(w / W * 100, 2), round(h / Hh * 100, 2)]
INFO = {}
def vorbereiten(ziel, v):
    """stellen/*.png → ziel/beweise/<id>.webp; INFO[id] = Kreis in Prozent, Adresse, Masse."""
    os.makedirs(ziel, exist_ok=True)
    for nr, figs in BEW.items():
        for fid, typ, titel, satz in figs:
            q = ST + fid + '.png'
            if not os.path.exists(q): continue
            im = Image.open(q).convert('RGB'); info = {'typ': typ, 'url': None, 'kreis': None}
            if typ == 'tel':
                im = im.resize((600, 1299), Image.LANCZOS)
                l = LAGE.get(fid, {}); info['url'] = l.get('url'); info['kreis'] = kreis(BOX.get(fid) or l.get('box'), 390, 844)
            elif typ == 'fen':
                l = LAGE.get(fid, {}); info['url'] = l.get('url'); b = l.get('box')
                if b:   # Ausschnitt um die Stelle (1b Nr. 9: die Stelle gross und lesbar), 1000 × 600 um die Mitte des Rechtecks
                    cw, ch = 1000, 600; cx, cy = b['x'] + b['w'] / 2, b['y'] + b['h'] / 2
                    x0 = max(0, min(im.width - cw, cx - cw / 2)); y0 = max(0, min(im.height - ch, cy - ch / 2))
                    im = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
                    info['kreis'] = kreis({'x': b['x'] - x0, 'y': b['y'] - y0, 'w': b['w'], 'h': b['h']}, cw, ch, 8)
                else:
                    im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
            else:
                if im.width > 1100: im = im.resize((1100, round(im.height * 1100 / im.width)), Image.LANCZOS)
                pl = PDFL.get(fid); info['pdf'] = (pl['pdf'], pl['seite']) if pl else None
                info['url'] = 'https://www.monte-moro.ch/templates/zerone/templateDetails.xml' if fid == 'z.1w' else None
                if pl: info['url'] = 'https://www.zerone.ch/agb/agb.pdf' if 'zerone' in pl['pdf'] else 'https://www.monte-moro.ch/images/restaurant/speisekarte.pdf'
            im.save(f'{ziel}/{fid}.webp', 'WEBP', quality=74 if typ == 'tel' else 80, method=6)
            info['w'], info['h'] = im.size; INFO[fid] = info
    json.dump(INFO, open(H + '/beweise.json', 'w'), ensure_ascii=False, indent=1)
    return INFO
def ring(k, eck=False):
    if not k: return ''
    return f'<span class="kreis{" kreis--eck" if eck or (k[2] > 70 and k[3] > 10) else ""}" style="left:{k[0]}%;top:{k[1]}%;width:{k[2]}%;height:{k[3]}%"></span>'
def figur(fid, typ, titel, satz, url_ersatz, v, kn_html):
    i = INFO.get(fid)
    if not i: return ''
    url = i.get('url') or url_ersatz
    knopf = kn_html('<span class="bw__l">Auf Ihrer Seite </span>ansehen', url) if url else ''
    cap = f'<figcaption><strong>{e(titel)}</strong><span>{e(satz)}</span>{knopf}</figcaption>'
    src = f'beweise/{fid}.webp?v={v}'
    if typ == 'tel':
        return (f'<figure class="bw bw--tel"><div class="tel"><div class="tel__schirm"><img src="{src}" width="600" height="1299" alt="{e(titel + ": " + satz)}" loading="lazy" decoding="async">{ring(i["kreis"])}</div>'
                f'<span class="tel__insel"></span><img class="tel__rahmen" src="bilder/rahmen-700.webp" srcset="bilder/rahmen-700.webp 700w, bilder/rahmen-1400.webp 1400w" sizes="(max-width:700px) 46vw, 260px" width="1400" height="2600" alt="" loading="lazy" decoding="async"></div>{cap}</figure>')
    if typ == 'fen':
        adr = (url or '').replace('https://', '').replace('http://', '')[:70]
        return (f'<figure class="bw bw--fen"><div class="fenster"><div class="fenster__kopf"><i></i><i></i><i></i><span>{e(adr)}</span></div><div class="fenster__b"><img src="{src}" width="{i["w"]}" height="{i["h"]}" alt="{e(titel + ": " + satz)}" loading="lazy" decoding="async">{ring(i["kreis"], True)}</div></div>{cap}</figure>')
    kopf = f'<div class="fenster__kopf"><i></i><i></i><i></i><span>{e(i["pdf"][0])} · Seite {i["pdf"][1]}</span></div>' if i.get('pdf') else '<div class="fenster__kopf"><i></i><i></i><i></i><span>monte-moro.ch · Quelltext, Abruf 17.10.2026</span></div>'
    return f'<figure class="bw bw--dok"><div class="fenster">{kopf}<div class="fenster__b"><img src="{src}" width="{i["w"]}" height="{i["h"]}" alt="{e(titel + ": " + satz)}" loading="lazy" decoding="async"></div></div>{cap}</figure>'
def beweise(nr, url_ersatz, v, kn_html, n=2):
    figs = [f for f in BEW.get(nr, []) if f[0] in INFO][:n]
    if not figs: return ''
    return f'<div class="pb__bew pb__bew--{len(figs)} steig" style="--i:2">' + ''.join(figur(*f, url_ersatz, v, kn_html) for f in figs) + '</div>'
