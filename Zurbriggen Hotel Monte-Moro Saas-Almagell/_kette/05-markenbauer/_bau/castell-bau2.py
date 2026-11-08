#!/usr/bin/env python3
"""Station 05 · Markenbauer · Castell Son Claret, Fassung 2 nach Roberts Rückgabe vom 15.10.2026 («nicht so wie beim Rivage»).

Baut das Markenbuch nach dem Muster von Le Livre des Grand Beau-Rivage (Master 5b, Regel 13.5 Nr. 12): dieselbe Bauart und dieselben
Bausteine (Vorlage _vorlage/gbr-markenbuch.py, gbr-marke.css, gbr-marke.js, am 15.10.2026 aus Grand Beau-Rivage/website/_werkbank und
marke/buch kopiert), übersetzt auf Zeichen, Farben, Schriften und Fotos dieses Hauses. Inhalte (Farben mit Fundstelle, Schriften, Zeichen,
Ton, zwei Farbwelten, eigene Welt) kommen unverändert aus bau.py.
   python3 bau2.py      → marke/markenbuch.html, marke/marke.css, marke/marke.js, marke/logo-richtig-falsch/index.html
Geräte: Laptop aus Blender (GBR werkzeuge_laptop.py, geraet/laptop.png + laptop.json), Handy aus Blender (geraet/handy_render.py nach
Carlton _gast/handy/render.py), Bildschirminhalte geraet/schirme.js."""
import html, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import bau as B  # noqa: E402

M = os.path.join(H, 'marke')
V = os.path.join(H, '_vorlage')
e = html.escape
F = B.F
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
PU = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14h10"/></svg>'

# ---------------------------------------------------------------- Farben in Gruppen (wie marke_daten.GRUPPEN), alle aus bau.FARBEN
GRUPPEN = [
    ('hell', 'Helle Flächen', 'Der Normalzustand. Hier wird gelesen, so hell wie der Tag auf dem Gut.', [
        ('weiss', 'Weiss', '#FFFFFF', 'Blätter, Karten, Briefbogen (app.css, 93 Fundstellen)'),
        ('kalk', 'Kalk', F['Kalk'], 'Grundfläche der Seite'),
        ('sandstein-hell', 'Sandstein hell', F['Sandstein hell'], 'zweite helle Fläche, Tapete hell'),
        ('sandstein', 'Sandstein', F['Sandstein'], 'Kanten, Unterseite der Knöpfe')]),
    ('dunkel', 'Die Nacht', 'Eine dunkle Fläche, immer mit Tapete: das Blau der Windrose von Sa Clastra.', [
        ('nacht', 'Nacht', F['Nacht'], 'die dunkle Fläche, mit Tapete'),
        ('nachtblau', 'Nachtblau', F['Nachtblau'], 'Knöpfe auf hellem Grund'),
        ('logo-grau', 'Logo-Grau', F['Logo-Grau'], 'Schrift auf Kalk und Sandstein, wie im Logo')]),
    ('gold', 'Gold und Stein', 'Zeichnet, schreibt nie den Lesetext. Das Gold kommt von der Karte der Castell Bar.', [
        ('bar-gold', 'Bar-Gold', F['Bar-Gold'], 'Zeichen und Zeilen auf Nacht'),
        ('stein', 'Stein', F['Stein'], 'zweite Titelzeile auf Hell, Linien'),
        ('bar-braun', 'Bar-Braun', F['Bar-Braun'], 'kleine Goldschrift auf Hell'),
        ('mosaik-gold', 'Mosaik-Gold', F['Mosaik-Gold'], 'nur das Mosaik der Castell Bar')]),
    ('hain', 'Der Olivenhain', 'Farbwelt B: das Dunkel der Haine unter dem Galatzó und das Messing der Theke.', [
        ('oliv-nacht', 'Oliv-Nacht', F['Oliv-Nacht'], 'die dunkle Fläche in Welt B'),
        ('oliv-tief', 'Oliv tief', F['Oliv tief'], 'Knöpfe in Welt B'),
        ('oliv', 'Oliv', F['Oliv'], 'zweite Titelzeile in Welt B'),
        ('messing', 'Messing', F['Messing'], 'Akzent in Welt B')]),
    ('sonder', 'Sonderfarbe', 'Nur für den Stern.', [
        ('michelin-rot', 'Michelin-Rot', F['Michelin-Rot'], 'Zeichen von Sa Clastra, der Stern')]),
]
FK = {k: (n, h) for _, _, _, l in GRUPPEN for k, n, h, _ in l}
FUND = {n: fund for n, hx, rolle, bel, fund in B.FARBEN}

# Herkunft: (Foto, Titel, Satz, Töne daraus (Schlüssel aus FK), Lage)
HERKUNFT = [
    ('tor', 'Das Tor mit den zwei Pfeilern', 'Sandstein im Mittag, warm und hell. Daraus sind die hellen Flächen geworden, auf denen gelesen wird: Kalk, Sandstein hell, Sandstein.', ['kalk', 'sandstein-hell', 'sandstein'], '50% 55%'),
    ('windrose-karte', 'Die Windrose von Sa Clastra', 'Das Blau der Karte «Rosa de los vientos», die das Haus selbst druckt. Die eine dunkle Fläche der Seite, Nacht und Nachtblau.', ['nacht', 'nachtblau'], '50% 30%'),
    ('bar-karte', 'Die Karte der Castell Bar', 'Das Gold des Bandes und das Mosaik aus goldenen Quadraten: die drei Türme, wie das Haus sie auf Papier setzt. Daraus Bar-Gold und Bar-Braun.', ['bar-gold', 'bar-braun', 'mosaik-gold'], '50% 50%'),
    ('bar', 'Die Theke der Castell Bar', 'Messing und dunkles Holz im Kutscherhaus. Das Messing ist der Akzent der Farbwelt B.', ['messing'], '50% 50%'),
    ('panorama', 'Der Olivenhain unter dem Galatzó', 'Oliv in drei Tiefen, gemessen im Hain. Farbwelt B nimmt daraus ihr Dunkel und die zweite Titelzeile.', ['oliv', 'oliv-tief', 'oliv-nacht'], '50% 50%'),
    ('garten', 'Bougainvillea im Garten', 'Das Rot der Blüten bleibt im Foto und wird bewusst nicht Teil der Palette: ein Farbpunkt je Bild, nie eine Fläche.', [], '50% 60%'),
]
WELT_B_CSS = f'[data-welt="b"]{{--marine:{F["Oliv-Nacht"]};--blau:{F["Oliv tief"]};--aare:{F["Oliv tief"]};--akzent:{F["Oliv"]};--taupe:{F["Oliv"]}}}\n[data-welt="b"] .tapete,[data-welt="b"] .leiste::after,[data-welt="b"] .tap__f--dunkel{{background-image:url(zeichen/tapete-dunkel-b.svg)}}'


def foto(key):
    p = os.path.join(M, 'bilder', key + '.jpg')
    if not os.path.exists(p):
        raise FileNotFoundError(key)
    return 'bilder/' + key + '.jpg'


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(h):
    def k(c):
        c /= 255; return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = rgb(h); return .2126 * k(r) + .7152 * k(g) + .0722 * k(b)


def kontrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)


def streifen(key, n=5):
    from PIL import Image
    im = Image.open(os.path.join(M, 'bilder', key + '.jpg')).convert('RGB'); im.thumbnail((360, 360))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:n * 3]; ges = im.size[0] * im.size[1]
    t = [(c / ges, '#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3])) for c, i in q.getcolors()]
    t.sort(key=lambda x: -lum(x[1])); return t


# ---------------------------------------------------------------- Bausteine (wie gbr-markenbuch.py)
ZVB = '0 0 36.485 19.394'
WVB = '0 0 194.49 66.291'
# Der Name allein (ohne die drei Türme), aus logo-dark.svg: die Gruppe «Group_8381» ist das Zeichen, der Rest der Name und die Unterzeile
NAME_INNEN = re.sub(r'<g transform="translate\(582\.755 23\.001\)">\s*<rect[^>]*/>\s*<rect[^>]*/>\s*<path[^>]*/>', '<g transform="translate(582.755 23.001)">', B.LOGO_INNEN, count=1)
NVB = '0 0 194.49 66.291'


def zeichen(kl='', titel=''):
    lab = f' role="img" aria-label="{e(titel)}"' if titel else ' aria-hidden="true"'
    return f'<svg class="{kl}" viewBox="{ZVB}" fill="currentColor"{lab}><use href="#tuerme"/></svg>'


def wort(kl=''):
    return f'<svg class="{kl}" viewBox="{WVB}" fill="currentColor" role="img" aria-label="Castell Son Claret"><use href="#wortmarke"/></svg>'


def name(kl=''):
    """Nur der Name mit Unterzeile, ohne die drei Türme (für Stellen, an denen das Zeichen schon steht)."""
    return f'<svg class="{kl}" viewBox="{NVB}" fill="currentColor" role="img" aria-label="Castell Son Claret"><g transform="translate(-582.755 -23)">{NAME_INNEN}</g></svg>'


def zeichen_x(sym, vb, kl='', farbe=None):
    st = f' style="color:{farbe}"' if farbe else ''
    return f'<svg class="{kl}" viewBox="{vb}" fill="currentColor"{st} aria-hidden="true"><use href="#{sym}"/></svg>'


def kn(text, href, kl='', neu=False, laden=False):
    zus = (' target="_blank" rel="noopener"' if neu else '') + (' download' if laden else '')
    return f'<a class="kn {kl}" href="{href}"{zus}>{e(text)}<i>{PU if laden else PF}</i></a>'


def zeilen(liste):
    return ''.join(f'<span class="z"><span>{"<em>" + x + "</em>" if i == len(liste) - 1 and len(liste) > 1 else x}</span></span>' for i, x in enumerate(liste))


def kopf(kap, titel, lead):
    return f'''<header class="mk" data-r="kopf">
      <div><p class="mk__kap"><b>{e(kap)}</b><i></i></p>
      <h2 class="mk__t">{zeilen(titel)}</h2></div>
      <p class="mk__lead">{lead}</p>
    </header>'''


def kachel(key, name, label, text, i, lage='50% 50%'):
    return f'''<article class="k3 k3--karte" data-r="feder" style="--i:{i}">
        <div class="k3__b"><img src="{foto(key)}" alt="{e(name)}" loading="lazy" decoding="async" style="object-position:{lage}"></div>
        <div class="k3__n"><small>{e(label)}</small><b>{e(name)}</b><p>{text}</p></div>
      </article>'''


def chip(k):
    n, h = FK[k]
    return f'<span class="mini"><i style="background:{h}"></i>{e(n)}</span>'


def geraet(welt, i=0):
    """Laptop aus Blender mit dem Bildschirminhalt der Probe darunter (Loch im Gehäuse, Mass aus laptop.json), daneben das Handy aus Blender."""
    L = json.load(open(os.path.join(M, 'geraet', 'laptop.json')))
    x, y, w, h = L['schirm']
    handy = os.path.exists(os.path.join(M, 'geraet', f'handy-{welt}.png'))
    tel = (f'<img class="ger__tel" src="geraet/handy-{welt}.png" alt="Die Probe am Handy, Farbwelt {welt.upper()}" loading="lazy" decoding="async">' if handy
           else f'<span class="ger__tel ger__tel--css"><img src="geraet/schirm/handy-{welt}.png" alt="Die Probe am Handy, Farbwelt {welt.upper()}" loading="lazy" decoding="async"></span>')
    return f'''<div class="ger" data-r="feder" style="--i:{i}">
      <div class="ger__laptop"><img class="ger__inhalt" src="geraet/schirm/laptop-{welt}.png" alt="Die Probe am Rechner, Farbwelt {welt.upper()}" loading="lazy" decoding="async" style="left:{x * 100:.3f}%;top:{y * 100:.3f}%;width:{w * 100:.3f}%;height:{h * 100:.3f}%"><img class="ger__huelle" src="geraet/laptop.png" alt="" width="{L['groesse'][0]}" height="{L['groesse'][1]}" loading="lazy" decoding="async"></div>
      {tel}
    </div>'''


# ---------------------------------------------------------------- CSS: die Vorlage des Rivage auf dieses Haus übersetzt
def css():
    s = open(os.path.join(V, 'gbr-marke.css'), encoding='utf-8').read()
    kopf_alt = s[:s.index('@property')]
    fonts = ("@font-face{font-family:'Fahkwang';font-style:normal;font-weight:300;font-display:swap;src:url('schriften/fahkwang-300-latin.woff2') format('woff2')}\n"
             "@font-face{font-family:'Fahkwang';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/fahkwang-400-latin.woff2') format('woff2')}\n"
             "@font-face{font-family:'Fahkwang';font-style:normal;font-weight:500;font-display:swap;src:url('schriften/fahkwang-500-latin.woff2') format('woff2')}\n"
             "@font-face{font-family:'Fahkwang';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/fahkwang-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-024F,U+1E00-1EFF}\n"
             "@font-face{font-family:'Montserrat';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/montserrat-400-latin.woff2') format('woff2')}\n"
             "@font-face{font-family:'Montserrat';font-style:normal;font-weight:500;font-display:swap;src:url('schriften/montserrat-500-latin.woff2') format('woff2')}\n"
             "@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/DMMono-normal-400.woff2') format('woff2')}\n"
             "@font-face{font-family:'Serif Ersatz';src:local('Georgia');size-adjust:100%}\n")
    s = s.replace(kopf_alt, '/* Markenbuch Castell Son Claret · Station 05 · Tasty Studios · 15.10.2026. Bauart und Bewegung wie Le Livre des Grand Beau-Rivage\n   (Vorlage _vorlage/gbr-marke.css), Farben, Schriften und Tapete dieses Hauses. Nur transform und opacity, nativer Scroll. */\n\n' + fonts)
    root_alt = re.search(r':root\{.*?\n\}', s, re.S).group(0)
    root_neu = (':root{\n'
                f"  --weiss:#FFFFFF; --papier:{F['Kalk']}; --creme:{F['Sandstein hell']}; --sand:{F['Sandstein']};\n"
                f"  --marine:{F['Nacht']}; --blau:{F['Nachtblau']}; --aare:{F['Nachtblau']}; --tinte:{F['Logo-Grau']};\n"
                f"  --gold:{F['Bar-Gold']}; --taupe:{F['Stein']}; --akzent:{F['Stein']}; --taupe-tief:{F['Bar-Braun']}; --rot:#8a2b2b;\n"
                "  --linie:rgba(138,119,97,.28); --linie-d:rgba(192,160,98,.22);\n"
                "  --serif:'Fahkwang','Serif Ersatz',Georgia,serif;\n"
                "  --caps:'Montserrat',Arial,sans-serif;\n"
                "  --sans:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;\n"
                "  --mono:'DM Mono',ui-monospace,'SF Mono',Menlo,monospace;\n"
                "  --e1:cubic-bezier(.16,1,.3,1); --e2:cubic-bezier(.32,.72,0,1); --e3:cubic-bezier(.19,1,.22,1);\n"
                "  --feder:cubic-bezier(.28,1.42,.42,1); --landen:cubic-bezier(.2,1.12,.3,1);\n"
                "  --rand:clamp(18px,5vw,96px); --max:1440px; --ab:clamp(110px,11.5vw,190px); --rund:clamp(28px,3.6vw,56px); --r:clamp(20px,2vw,28px);\n"
                "  --start:0s;\n}\n" + WELT_B_CSS)
    s = s.replace(root_alt, root_neu)
    # Tapete: die Rosette des Hauses als Kachel (560 px), hell und dunkel
    s = s.replace('url(../../assets/img/tapete-dunkel.webp)', 'url(zeichen/tapete-dunkel.svg)').replace('url(../../assets/img/tapete-hell.webp)', 'url(zeichen/tapete-hell.svg)').replace('340px auto', '560px auto')
    s = s.replace('.tapete{background-color:var(--marine);background-image:url(zeichen/tapete-dunkel.svg)', '.tapete{background-color:var(--marine);background-image:url(zeichen/tapete-dunkel.svg)')
    # feste Töne der Vorlage → Töne dieses Hauses
    karte = {'#1b2033': F['Nacht'], '#151a2b': '#0A1B3A', '#181c2d': '#0F2550', '#20263c': '#152D5A', '#232a43': '#17315F', '#262c45': '#193465', '#171b2b': '#0A1B3A', '#141827': '#09182F',
             '#323a58': F['Nachtblau'], '#3f4767': F['Nachtblau'], '#2c334d': F['Nachtblau'],
             '#cdaa5c': F['Bar-Gold'], '#fbf0cf': '#F3E8CC', '#ead39c': '#DCC68F', '#c9a764': F['Bar-Gold'], '#9c7b43': '#8F7445', '#dcc189': '#D2B97F', '#f3e3b6': '#EBDCB1',
             '#f9f1e1': '#F4F2EC', '#fdf5e8': '#F6F4EE', '#eee2cc': F['Sandstein hell'], '#c8ba9e': F['Sandstein'], '#fdf9f1': '#FFFFFF', '#e8dcc3': F['Sandstein hell'], '#e7dcc6': F['Sandstein hell'],
             '#fff7e2': '#F6F4EE', '#b0934f': F['Stein'], '#6d5a2c': F['Bar-Braun'], '#e2d2b5': F['Sandstein'], '#2aa198': '#1d8a4a'}
    s = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: karte.get(m.group(0).lower(), m.group(0)), s)
    for a, b in (('rgba(26,29,40', 'rgba(87,87,86'), ('rgba(253,249,241', 'rgba(255,255,255'), ('rgba(230,210,162', 'rgba(192,160,98'), ('rgba(130,108,53', 'rgba(138,119,97'),
                 ('rgba(150,166,214', 'rgba(120,150,210'), ('rgba(210,191,152', 'rgba(215,199,178')):
        s = s.replace(a, b)
    s = s.replace('.leiste::after{content:\'\';position:absolute;inset:0;z-index:-1;background:url(zeichen/tapete-dunkel.svg) 0 0/560px auto;opacity:.45', '.leiste::after{content:\'\';position:absolute;inset:0;z-index:-1;background:url(zeichen/tapete-dunkel.svg) 0 0/560px auto;opacity:.5')
    # Eigenes dieses Hauses: Geräte, Logo-Regeln in vier Spalten, Welten, Zeichenreihe, Unterschiede
    s += '''
.welt__tafel{min-height:clamp(240px,22vw,320px)}
/* ---------- Castell Son Claret: Geräte aus Blender (Laptop nach GBR werkzeuge_laptop.py, Handy nach Carlton render.py) ---------- */
.welten{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(22px,3vw,52px)}
.welt{display:flex;flex-direction:column;gap:18px}
.welt__k{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap}
.welt__k h3{font-family:var(--serif);font-weight:500;font-size:clamp(1.7rem,2.4vw,2.5rem);line-height:1.05}
.welt__k h3 em{color:var(--akzent)} .marine .welt__k h3 em{color:var(--gold)}
.welt__b{display:flex;gap:8px}
.welt__b i{width:34px;height:34px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.welt p{font-size:1rem;line-height:1.66;color:rgba(87,87,86,.86);max-width:48ch} .marine .welt p{color:rgba(255,255,255,.8)}
.ger{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 24%;align-items:end;gap:0}
.ger__laptop{position:relative;width:100%}
.ger__huelle{position:relative;z-index:2;width:100%;height:auto;display:block}
.ger__inhalt{position:absolute;z-index:1;object-fit:cover;object-position:50% 0;border-radius:1.8% 1.8% 0 0}
.ger__tel{position:relative;z-index:3;width:138%;margin-left:-38%;margin-bottom:-6%;height:auto;filter:drop-shadow(0 30px 30px rgba(0,0,0,.35))}
.ger__tel--css{display:block;width:30%;margin-left:-6%;margin-bottom:6%;padding:5px;border-radius:26px;background:#0b0c10;box-shadow:0 30px 40px -24px rgba(0,0,0,.7),inset 0 0 0 1px rgba(255,255,255,.08)}
.ger__tel--css img{width:100%;border-radius:21px}
.reihe5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:clamp(14px,1.6vw,24px);margin-top:clamp(16px,1.8vw,28px)}
.zei{display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;padding:clamp(22px,2.4vw,34px) 16px;border-radius:var(--r);background:var(--weiss);box-shadow:inset 0 0 0 1px var(--linie),0 30px 40px -32px rgba(87,87,86,.45)}
.zei svg{height:clamp(54px,5.4vw,78px);width:auto;max-width:100%;color:var(--marine)}
.zei b{font-family:var(--serif);font-weight:500;font-size:1.15rem;line-height:1.15}
.zei small{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;line-height:1.4;color:rgba(87,87,86,.6)}
.regeln--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.regel--f .regel__f{position:relative}
.regel--f .regel__f::before{content:'';position:absolute;inset:0;border-radius:14px;box-shadow:inset 0 0 0 1.5px var(--rot);pointer-events:none;z-index:2}
.regel--f .regel__f::after{content:'';position:absolute;right:10px;top:10px;width:26px;height:26px;z-index:3;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'><circle cx='15' cy='15' r='15' fill='%238a2b2b'/><path d='M10 10l10 10M20 10L10 20' stroke='white' stroke-width='2.4' stroke-linecap='round'/></svg>") center/contain no-repeat}
.lf{width:100%;min-height:170px;display:flex;align-items:center;justify-content:center;gap:16px;border-radius:14px;overflow:hidden}
.lf svg{height:auto}
.satz3 ul{display:grid;gap:9px} .satz3 li{position:relative;padding-left:20px;font-size:.98rem;line-height:1.5;color:rgba(87,87,86,.8)}
.satz3 li::before{content:'';position:absolute;left:0;top:.7em;width:9px;height:1.5px;background:var(--akzent)}
.satz3 .nicht li::before{background:var(--rot)}
.unter{display:grid;gap:0;border-top:1px solid var(--linie-d)}
.unter li{display:grid;grid-template-columns:minmax(150px,230px) 1fr;gap:20px;padding:18px 0;border-bottom:1px solid var(--linie-d);opacity:0;transform:translate3d(0,22px,0);transition:opacity 1s var(--e2),transform 1.3s var(--e1);transition-delay:calc(var(--i,0)*90ms)}
.da .unter li,.unter.da li{opacity:1;transform:none}
.unter b{font-family:var(--serif);font-weight:500;font-size:1.2rem;line-height:1.15} .unter span{color:rgba(255,255,255,.8);font-size:.98rem;line-height:1.55}
.welt-schalter{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
@media (max-width:1000px){.welten{grid-template-columns:1fr}.reihe5{grid-template-columns:repeat(3,minmax(0,1fr))}.regeln--4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:620px){.reihe5{grid-template-columns:repeat(2,minmax(0,1fr))}.regeln--4{grid-template-columns:1fr}.unter li{grid-template-columns:1fr;gap:6px}.ger{grid-template-columns:minmax(0,1fr) 30%}}
'''
    open(os.path.join(M, 'marke.css'), 'w', encoding='utf-8').write(s)
    js = open(os.path.join(V, 'gbr-marke.js'), encoding='utf-8').read().replace('Markenbuch Grand Beau-Rivage', 'Markenbuch Castell Son Claret')
    js += '''
/* Farbwelt A/B im Markenbuch umschalten (Castell Son Claret, 15.10.2026): nur ein Attribut am body, die Farben kommen aus dem CSS */
(function(){var w=new URLSearchParams(location.search).get('welt');if(w==='b')document.body.setAttribute('data-welt','b');
document.querySelectorAll('[data-welt-knopf]').forEach(function(b){b.addEventListener('click',function(ev){ev.preventDefault();var x=b.getAttribute('data-welt-knopf');if(x==='b')document.body.setAttribute('data-welt','b');else document.body.removeAttribute('data-welt');
document.querySelectorAll('[data-welt-knopf]').forEach(function(k){k.classList.toggle('kn--linie',k!==b)});});});})();
'''
    open(os.path.join(M, 'marke.js'), 'w', encoding='utf-8').write(js)


# ---------------------------------------------------------------- die Seite
def logo_karten():
    k = F
    def wm(farbe, st=''): return f'<svg viewBox="{WVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#wortmarke"/></svg>'
    def tm(farbe, st=''): return f'<svg viewBox="{ZVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#tuerme"/></svg>'
    richtig = [
        ('Wortmarke auf Kalk', f'<div class="lf" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:62%")}</div>', 'Das Original: Zeichen und Name in Logo-Grau auf heller Fläche.'),
        ('Wortmarke auf Nacht', f'<div class="lf tapete" style="background-color:{k["Nacht"]}">{wm(k["Kalk"], "width:62%")}</div>', 'Auf dunkler Fläche in Kalk, so wie das Haus es heute mit logo-white.svg macht.'),
        ('Das Zeichen allein', f'<div class="lf" style="background:{k["Sandstein hell"]}">{tm(k["Logo-Grau"], "width:26%")}</div>', 'Die drei Türme stehen allein in der Leiste, als Siegel und über Überschriften.'),
        ('Zeichen in Gold', f'<div class="lf tapete" style="background-color:{k["Nacht"]}">{tm(k["Bar-Gold"], "width:26%")}</div>', 'Auf Nacht darf das Zeichen in Bar-Gold stehen, wie das Mosaik auf der Karte der Castell Bar.'),
        ('Mindestgrösse', f'<div class="lf" style="background:{k["Kalk"]};flex-direction:column;gap:18px">{wm(k["Logo-Grau"], "width:150px")}<span class="mono" style="font-size:10px;color:{k["Stein"]};letter-spacing:.12em">150 PX · DARUNTER NUR DAS ZEICHEN (AB 22 PX)</span></div>', 'Die Wortmarke bleibt lesbar bis 150 px Breite. Kleiner steht nur das Zeichen.'),
        ('Schutzraum', f'<div class="lf" style="background:{k["Kalk"]}"><div style="position:relative;padding:11%;outline:1px dashed {k["Stein"]};width:84%">{wm(k["Logo-Grau"], "width:100%")}</div></div>', 'Rundum so viel Luft wie das Zeichen hoch ist. Nichts rückt näher heran.'),
        ('Auf dem Foto', f'<div class="lf" style="background:url({foto("himmel")}) 50% 20%/cover">{wm(k["Kalk"], "width:58%")}</div>', 'Nur auf einem ruhigen Foto, auf einer ruhigen Fläche des Bildes, in Kalk, nie mit Schatten oder Saum.'),
        ('Die Zeichen der Häuser', f'<div class="lf" style="background:{k["Kalk"]};gap:9%;color:{k["Nacht"]}">{zeichen_x("windrose", B.ROSE_VB, "", k["Nacht"])}{zeichen_x("rosette", "0 0 592 590.711", "", k["Nacht"])}{zeichen_x("mosaik", B.MOS_VB, "", k["Mosaik-Gold"])}</div>', 'Windrose, Rosette und Mosaik stehen für Sa Clastra, die Tapete und die Castell Bar, nie anstelle der drei Türme.'),
    ]
    falsch = [
        ('Gestreckt', f'<div class="lf" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:66%;transform:scaleX(1.35)")}</div>', 'Die Proportion bleibt. Nie breiter oder höher gezogen.'),
        ('Umgefärbt', f'<div class="lf" style="background:{k["Kalk"]}">{wm("#1d8a4a", "width:62%")}</div>', 'Nur Logo-Grau, Kalk und Bar-Gold. Kein Grün, kein Rot, kein Verlauf.'),
        ('Mit Schatten und Glanz', f'<div class="lf" style="background:{k["Nacht"]}">{wm(k["Kalk"], "width:62%;filter:drop-shadow(0 6px 10px rgba(0,0,0,.9)) drop-shadow(0 0 18px rgba(192,160,98,.9))")}</div>', 'Kein Schatten, kein Leuchten, kein Relief. Das Zeichen liegt flach.'),
        ('Neu gesetzt', f'<div class="lf" style="background:{k["Kalk"]};font-family:Georgia,serif;font-style:italic;font-size:clamp(20px,2vw,30px);color:{k["Logo-Grau"]}">Castell Son Claret</div>', 'Der Name wird nie in einer anderen Schrift neu geschrieben. Die Wortmarke ist eine Datei.'),
        ('Auf unruhigem Foto', f'<div class="lf" style="background:url({foto("garten-weg")}) 50% 60%/cover">{wm(k["Kalk"], "width:58%")}</div>', 'Blätter und Licht hinter den Buchstaben: unlesbar. Dunkel ins Bild rechnen oder ein anderes Foto.'),
        ('Gedreht und beschnitten', f'<div class="lf" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:66%;transform:rotate(-12deg) translate(18%,6%)")}</div>', 'Die Wortmarke steht immer waagrecht und ganz.'),
        ('Zu klein', f'<div class="lf" style="background:{k["Kalk"]}">{wm(k["Logo-Grau"], "width:80px")}</div>', 'Unter 150 px ist der Name nicht mehr lesbar. Dann nur das Zeichen.'),
        ('Rosette statt Türme', f'<div class="lf" style="background:{k["Kalk"]};color:{k["Stein"]}">{zeichen_x("rosette", "0 0 592 590.711", "")}<span style="font-family:var(--caps);letter-spacing:.3em;font-size:12px;color:{k["Logo-Grau"]}">CASTELL SON CLARET</span></div>', 'Die Rosette ist Tapete, kein Logo. Das Zeichen des Hauses sind die drei Türme.'),
    ]
    def karten(liste, kl):
        return ''.join(f'<div class="regel {kl}" data-r="feder" style="--i:{i % 4}"><div class="regel__f">{b}</div><h3>{e(t)}</h3><p>{e(s)}</p></div>' for i, (t, b, s) in enumerate(liste))
    return karten(richtig, 'regel--r'), karten(falsch, 'regel--f')


def seite():
    alle = [(k, n, h, r) for _, _, _, l in GRUPPEN for k, n, h, r in l]
    n_f = len(alle)
    faecher = ''.join(f'''<button class="fa" type="button" data-hex="{h}" style="--c:{h};--t:{'#575756' if lum(h) > .35 else '#ECEAE4'};--j:{j};--w:{(j - (n_f - 1) / 2) * 5.4:.1f}deg" aria-label="{e(n)} {h.upper()} kopieren">
          <span class="fa__n"><b>{e(n)}</b><small>{h.upper()}</small></span><span class="fa__ok">kopiert</span>
        </button>''' for j, (k, n, h, r) in enumerate(alle))
    gruppen_html = ''
    for gk, gname, gsatz, liste in GRUPPEN:
        karten = ''.join(f'''<button class="fk" type="button" data-r="feder" data-hex="{h}" style="--i:{i};--c:{h};--t:{'#575756' if lum(h) > .35 else '#ECEAE4'}" aria-label="{e(n)} {h.upper()} kopieren">
            <span class="fk__f"><span class="fk__hex">{h.upper()}</span><span class="fk__ok">kopiert</span></span>
            <span class="fk__n">{e(n)}</span>
            <span class="fk__r">{e(r)}</span>
            <span class="fk__w"><span>HEX</span>{h.upper()}<span>RGB</span>{' · '.join(map(str, rgb(h)))}</span>
          </button>''' for i, (k, n, h, r) in enumerate(liste))
        gruppen_html += f'''<div class="gr gr--{gk}" data-g>
        <div class="gr__k" data-r style="--i:0"><p class="mk__kap"><b>{e(gname)}</b><i></i></p><p class="gr__s">{e(gsatz)}</p></div>
        <div class="gr__l gr__l--{len(liste)}">{karten}</div>
      </div>'''
    anteile = [('Kalk und Sandstein', 62, F['Kalk'], F['Logo-Grau']), ('Nacht', 26, F['Nacht'], F['Bar-Gold']), ('Gold', 8, F['Bar-Gold'], '#FFFFFF'), ('Logo-Grau', 4, F['Logo-Grau'], '#FFFFFF')]
    anteil_html = ''.join(f'<span style="--p:{p};--j:{j};background:{c};color:{t}"><b><span data-zahl="{p}">0</span> %</b><small>{e(n)}</small></span>' for j, (n, p, c, t) in enumerate(anteile))
    paare = [('Logo-Grau auf Kalk', 'logo-grau', 'kalk', 'Lesetext'), ('Bar-Gold auf Nacht', 'bar-gold', 'nacht', 'Titel und Zeichen auf Dunkel'),
             ('Kalk auf Nachtblau', 'kalk', 'nachtblau', 'Schrift im Knopf'), ('Bar-Braun auf Kalk', 'bar-braun', 'kalk', 'kleine Goldschrift'),
             ('Stein auf Kalk', 'stein', 'kalk', 'zweite Titelzeile'), ('Bar-Gold auf Kalk', 'bar-gold', 'kalk', 'nie als Schrift')]
    def urteil(r):
        if r >= 7: return 'Sehr gut, auch für langen Text'
        if r >= 4.5: return 'Gut für Lesetext'
        if r >= 3: return 'Nur für grosse Zeilen'
        return 'Nur Schmuck, nie Schrift'
    kontrast_html = ''
    for i, (t, a, b, w) in enumerate(paare):
        r = kontrast(FK[a][1], FK[b][1])
        kontrast_html += f'''<li class="ko" data-r="feder" style="--i:{i % 3};--g:{FK[b][1]};--s:{FK[a][1]}">
          <span class="ko__p"><span>Aa</span><small>Ein Landgut am Fuß des Galatzó</small></span>
          <span class="ko__n"><b>{e(t)}</b><small>{e(w)}</small></span>
          <span class="ko__z"><b><span data-zahl="{r:.1f}" data-komma>0</span></b><small>zu 1</small></span>
          <em class="ko__u">{urteil(r)}</em>
        </li>'''
    herkunft_html = ''
    for i, (key, t, x, toene, lage) in enumerate(HERKUNFT):
        st = streifen(key)
        st_html = ''.join(f'<i style="flex:{max(a, .06):.3f};background:{h};--j:{j}"></i>' for j, (a, h) in enumerate(st))
        werte = ' · '.join(h.upper() for _, h in st)
        wird = (f'<p class="her__wird"><span>Daraus</span>{"".join(chip(k) for k in toene)}</p>' if toene else '<p class="her__wird her__wird--nein"><span>Bleibt im Bild</span></p>')
        herkunft_html += f'''<article class="her k3" data-r="feder" style="--i:{i % 3}">
        <div class="k3__b her__b"><img src="{foto(key)}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{lage}"><span class="kerbe kerbe--d">{e(t)}</span></div>
        <div class="her__st" aria-label="Gemessene Töne: {werte}">{st_html}</div>
        <p class="her__m">aus dem Foto gemessen · {werte}</p>
        <p class="her__x">{e(x)}</p>
        {wird}
      </article>'''
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyzäöüß<br>0123456789 · 132 ha · 1450'
    schriften = [
        ('a', 'Grosse Zeilen', 'Fahkwang', 'Regular 400, nie fett, nie kursiv', 'Titel, Namen, Preise; die Titelschrift der heutigen Seite', 'Aa', 'Am Fuß des Galatzó', ALPHA),
        ('c', 'Kapitelzeilen', 'Montserrat', 'Regular 400, Versalien, gesperrt 0,28 em', 'wie die Unterzeile der Wortmarke: Ortszeilen, Kapitel, Schilder', 'AA', 'Es Capdellà · Mallorca', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>0123456789 · ÄÖÜ'),
        ('s', 'Lesetext', 'Montserrat', 'Regular 400 und Medium 500', 'alles, was gelesen wird; der Lauftext der heutigen Seite', 'Aa', 'Ein Tisch im Olivera', ALPHA),
        ('m', 'Kleine Angaben', 'DM Mono', 'Regular 400', 'Zeiten, Preise, Adressen, Knöpfe', 'Aa', 'Km 1,7 · 07196 Es Capdellà', ALPHA),
    ]
    def rollen(text):
        return ''.join(f'<span class="ro" style="--k:{i}" data-c="{e(c)}">{e(c)}</span>' if c != ' ' else ' ' for i, c in enumerate(text))
    schrift_html = ''.join(f'''<article class="sch" data-g>
        <div class="sch__k" data-r style="--i:0"><p class="mk__kap"><b>{e(r)}</b><i></i></p><h3 class="sch__n f-{c}">{e(n)}</h3><dl><dt>Schnitt</dt><dd>{e(s)}</dd><dt>Wofür</dt><dd>{e(w)}</dd></dl></div>
        <div class="sch__aa f-{c}" data-r="maske" aria-hidden="true"><span class="z"><span>{aa}</span></span></div>
        <div class="sch__r" data-r style="--i:2"><p class="sch__satz f-{c}" aria-label="{e(probe)}">{rollen(probe)}</p><p class="sch__abc f-{c}">{abc}</p></div>
      </article>''' for c, r, n, s, w, aa, probe, abc in schriften)
    rang = [('Titel gross', 'Fahkwang 400 · 92 px', 'r1', 'Ein Landgut am Fuß des Galatzó'), ('Titel', 'Fahkwang 400 · 64 px', 'r2', 'Zimmer und Suiten'),
            ('Zwischentitel', 'Fahkwang 400 · 36 px', 'r3', 'Garden Suite mit eigenem Garten'), ('Kleiner Titel', 'Fahkwang 400 · 22 px', 'r4', 'Frühstück im Olivera'),
            ('Kapitelzeile', 'Montserrat · 12 px · gesperrt', 'r5', 'Sa Clastra · ein Michelin-Stern'), ('Lesetext', 'Montserrat · 18 px · Zeilenabstand 1,64', 'r6', 'Castell Son Claret ist ein 132 Hektar großes Anwesen, das sich in Privatbesitz befindet und unabhängig verwaltet wird.'),
            ('Kleine Angabe', 'DM Mono · 12,5 px · gesperrt', 'r7', 'Check-in · Ctra. Capdellà-Galilea Km 1,7 · 07196 Es Capdellà')]
    rang_html = ''.join(f'<li data-r="maske"><span class="rang__m"><b>{e(a)}</b>{e(b)}</span><span class="{c}"><span class="z"><span>{e(s)}</span></span></span></li>' for a, b, c, s in rang)
    bilder = [('pool', 'Der Pool an der Steinmauer', 'b1', '50% 50%'), ('garden-suite', 'Garden Suite', 'b2', '50% 50%'), ('castell-suite', 'Castell Suite', 'b3', '50% 50%'),
              ('sa-clastra-raum', 'Sa Clastra', 'b4', '50% 50%'), ('classics', 'Castell Classics', 'b5', '50% 50%'), ('tramuntana', 'Die Tramuntana', 'b6', '50% 50%'),
              ('sa-clastra-teller', 'Ein Gang aus «Wind und Erinnerung»', 'b7', '50% 50%')]
    bilder_html = ''.join(f'<figure class="bi {c} k3" data-r="feder" style="--i:{i % 3}"><div class="k3__b"><img src="{foto(k)}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{l}"><figcaption class="kerbe">{e(t)}</figcaption></div></figure>' for i, (k, t, c, l) in enumerate(bilder))
    nein = [('zerr', 'Nicht verzerren'), ('dreh', 'Nicht drehen'), ('farbe', 'Nicht umfärben'), ('schatten', 'Keine Schatten')]
    nein_html = ''.join(f'<figure class="nein nein--{c}"><div>{zeichen()}<i></i></div><figcaption>{e(t)}</figcaption></figure>' for c, t in nein)
    richtig_html, falsch_html = logo_karten()
    unterschiede = ''.join(f'<li style="--i:{i}"><b>{e(k)}</b><span>{e(v)}</span></li>' for i, (k, v) in enumerate(B.EIGENE_WELT['unterschied_zu'].items()))
    T = B.TON
    welt_a, welt_b = B.WELTEN['a'], B.WELTEN['b']
    def welt_block(k, w, i):
        c = w['css']
        return f'''<div class="welt">
        <div class="welt__k"><h3>{k.upper()} · <em>{e(w['name'])}</em></h3><div class="welt__b">{''.join(f'<i style="background:{c[x]}"></i>' for x in ('papier', 'creme', 'nacht', 'blau', 'gold', 'beton'))}</div></div>
        <p>{e(w['satz'])}</p>
        <figure class="lock lock--marine tapete welt__tafel" data-r="flug" style="--i:{i};--fx:{'-10vw' if i == 0 else '10vw'};--fy:22vh;--fw:{'-5deg' if i == 0 else '5deg'};background-color:{c['nacht']};background-image:url(zeichen/tapete-dunkel{'-b' if k == 'b' else ''}.svg);color:{c['gold']}"><div>{wort('lock__w')}<p class="lock__o" style="color:{c['gold']}">Es Capdellà · Welt {k.upper()}</p></div><figcaption class="kerbe kerbe--c">{e(w['flaechen'][2])} · Knöpfe {e(w['knopf'])} · Betonung {e(w['betonung'])}</figcaption></figure>
        <div class="knr">{kn(f'Probe {k.upper()} öffnen', f'probe.html?welt={k}', neu=True)}<a class="kn {"kn--linie" if k == "b" else ""}" href="?welt={k}" data-welt-knopf="{k}">Markenbuch in {k.upper()}<i>{PF}</i></a></div>
      </div>'''
    KAPITEL = [('haltung', 'Haltung'), ('zeichen', 'Zeichen'), ('farben', 'Farben'), ('welten', 'Welten'), ('herkunft', 'Herkunft'), ('schrift', 'Schrift'), ('tapete', 'Tapete'), ('bilder', 'Bilder'), ('bausteine', 'Bausteine'), ('logo', 'Logo'), ('welt', 'Eigene Welt'), ('mitnehmen', 'Mitnehmen')]
    index_html = ''.join(f'<a href="#{k}" data-r style="--i:{i}"><span>{e(n)}</span></a>' for i, (k, n) in enumerate(KAPITEL))
    nav_html = ''.join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAPITEL[:10])
    v_css = int(os.path.getmtime(os.path.join(M, 'marke.css'))); v_js = int(os.path.getmtime(os.path.join(M, 'marke.js')))
    GOLD = '<linearGradient id="tgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3E8CC"/><stop offset=".34" stop-color="#DCC68F"/><stop offset=".52" stop-color="#C0A062"/><stop offset=".62" stop-color="#8F7445"/><stop offset=".8" stop-color="#D2B97F"/><stop offset="1" stop-color="#EBDCB1"/></linearGradient>'
    defs = B.sym_defs().replace('</defs>', GOLD + '</defs>')
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Markenbuch · Castell Son Claret</title>
<meta name="description" content="Zeichen, Farben und ihre Herkunft, Schriften, Tapete, Bilder und Bausteine für die neue Website des Castell Son Claret. Entwurf von Tasty Studios, Oktober 2026.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['Nacht']}">
<link rel="preload" href="schriften/fahkwang-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="schriften/montserrat-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="marke.css?v={v_css}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{defs}

<nav class="leiste" aria-label="Markenbuch">
  <a class="leiste__m" href="#oben">{zeichen()}<span><b>Markenbuch</b><small>Station 05 · Castell Son Claret</small></span></a>
  <div class="leiste__k">{nav_html}</div>
  <a class="glanz" href="probe.html" target="_blank" rel="noopener">Die Probe{PF}</a>
</nav>

<main>
<section class="titel tapete" id="oben">
  <div class="titel__in">
    <p class="titel__kap" data-r="hero" style="--i:0"><i></i><b>Markenbuch · Oktober 2026</b><i></i></p>
    <div class="titel__z" data-r="zeichen">{zeichen('', 'Die drei Türme').replace('fill="currentColor"', 'fill="url(#tgold) #C0A062"')}</div>
    <h1 class="titel__w" data-r="maske"><span class="z"><span>{name().replace('fill="currentColor"', 'fill="url(#tgold) #C0A062"')}</span></span></h1>
    <p class="titel__ort" data-r="hero" style="--i:2">Es Capdellà <span class="raute"></span> seit 1450</p>
    <p class="titel__lead" data-r="hero" style="--i:3">Alles, was Ihr Haus erkennbar macht, an einem Ort: die drei Türme und der Name, die Farben und woher sie kommen, die Schriften, die Rosette als Tapete, die Bilder und die Bausteine der neuen Website. Damit jedes neue Stück, ob Karte, Seite oder Schild, aussieht wie aus einem Guss.</p>
    <div class="knr knr--mitte" data-r="hero" style="--i:4">{kn('Lesen', '#haltung')}{kn('Die Probe', 'probe.html', 'kn--linie', neu=True)}</div>
  </div>
  <nav class="index" aria-label="Inhalt" data-g>{index_html}</nav>
  <span class="titel__runter" aria-hidden="true"><i></i></span>
</section>

<section class="ab blatt papier" id="haltung">
  <div class="in">
    {kopf('Haltung', ['Ein Landgut, seit 1450', 'am Fuß des Galatzó.'], 'Castell Son Claret ist eine Possessió: ein Landgut, das sich selbst versorgte, in Aufzeichnungen seit 1450, seit Mai 2013 ein Hotel mit 43 Zimmern auf 132 Hektar. Diese Herkunft ist das Produkt. Die Gestaltung zeigt Stein, Garten und Wind, bevor ein Wort gelesen wird.')}
    <div class="drei" data-g>
      {kachel('fassade', 'Stein, so hell wie der Tag.', 'Stein', 'Die Seite ist hell wie das Gut im Mittag: Kalk und Sandstein tragen den Lesetext. Dunkel wird sie nur dort, wo das Haus es selbst ist.', 0)}
      {kachel('terrasse', 'Der Ort ist der Held.', 'Garten', 'Grosse, echte Fotos aus dem Haus: Garten, Terrasse, Pool, Tramuntana. Bild zuerst, Schrift als Beigabe, nichts aus einer Bilddatenbank.', 1)}
      {kachel('olivera', 'Leise, aus dem Ort.', 'Ton', '«Es gibt Orte, die man einfach nicht beschreiben kann.» Das Haus redet nicht in Suchwörtern. Die Seite nimmt seine eigenen Sätze.', 2)}
    </div>
  </div>
</section>

<section class="fenster" aria-label="Die Allee bei Nacht">
  <div class="fenster__f">
    <div class="fenster__b"><img src="{foto('allee-nacht')}" alt="Die Palmenallee zum Castell Son Claret bei Nacht" decoding="async"></div>
    <div class="fenster__t"><p class="fenster__s"><span class="z"><span>Es gibt Orte, die man einfach</span></span><span class="z"><span><em>nicht beschreiben kann.</em></span></span></p><p class="fenster__u">«Und auch nicht vergleichen.» Castell Son Claret, über sich selbst.</p></div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="zeichen">
  <div class="in">
    {kopf('Zeichen und Name', ['Die drei Türme', 'und Ihr Name.'], 'Die drei Türme und die Wortmarke kommen als Vektor von Ihrer heutigen Seite (sygnet.svg, logo-dark.svg, logo-white.svg) und werden nie nachgezeichnet. Dazu die Rosette aus dem Hintergrund Ihres Einstiegstextes, die Windrose von Sa Clastra und das Mosaik der Castell Bar, beide aus Ihren Karten gezeichnet.')}
    <div class="lockups" data-g>
      <figure class="lock lock--marine tapete" data-r="flug" style="--i:0;--fx:-14vw;--fy:22vh;--fw:-6deg"><div>{wort('lock__w')}<p class="lock__o">Es Capdellà</p></div><figcaption class="kerbe kerbe--c">Hauptform auf Nacht</figcaption></figure>
      <figure class="lock lock--papier" data-r="flug" style="--i:1;--fx:14vw;--fy:22vh;--fw:6deg"><div>{wort('lock__w')}<p class="lock__o">Es Capdellà</p></div><figcaption class="kerbe kerbe--c">Hauptform auf Kalk</figcaption></figure>
      <figure class="lock lock--quer" data-r="flug" style="--i:2;--fx:-12vw;--fy:30vh;--fw:5deg"><div>{zeichen('lock__z')}<span class="lock__strich"></span>{name('lock__w')}</div><figcaption class="kerbe kerbe--c">Querform für Leisten und Briefköpfe</figcaption></figure>
      <figure class="lock lock--groessen tapete" data-r="flug" style="--i:3;--fx:12vw;--fy:30vh;--fw:-5deg"><div>{zeichen('g1')}{zeichen('g2')}{zeichen('g3')}{zeichen('g4')}</div><figcaption class="kerbe kerbe--c">Das Zeichen allein: Siegel, Stempel, Reiter im Browser</figcaption></figure>
    </div>
    <div class="reihe5" data-g>
      <div class="zei" data-r="feder" style="--i:0">{zeichen_x('tuerme', ZVB)}<b>Die drei Türme</b><small>sygnet.svg · das Castell als Zeichen</small></div>
      <div class="zei" data-r="feder" style="--i:1">{zeichen_x('rosette', '0 0 592 590.711', '', F['Stein'])}<b>Die Rosette</b><small>ornament.svg · heute 7 % hinter dem Text, neu als Tapete</small></div>
      <div class="zei" data-r="feder" style="--i:2">{zeichen_x('windrose', B.ROSE_VB)}<b>Die Windrose</b><small>Sa Clastra · acht Winde, aus der Karte gezeichnet</small></div>
      <div class="zei" data-r="feder" style="--i:3">{zeichen_x('mosaik', B.MOS_VB, '', F['Mosaik-Gold'])}<b>Das Mosaik</b><small>Castell Bar · die Türme in Gold, aus der Karte 2025</small></div>
      <div class="zei" data-r="feder" style="--i:0"><svg viewBox="0 0 80 80" style="height:clamp(54px,5.4vw,78px)" aria-hidden="true"><rect x="22" y="22" width="36" height="36" fill="{F['Michelin-Rot']}"/></svg><b>Der Stern</b><small>sa-crasta.svg · Michelin-Rot, nur für Sa Clastra</small></div>
    </div>
    <div class="regeln" data-g>
      <div class="regel" data-r="feder" style="--i:0">
        <div class="regel__f"><svg class="schutz" viewBox="-24 -24 84.485 67.394" aria-hidden="true">
          <rect class="schutz__r" x="-19.4" y="-19.4" width="75.3" height="58.2" rx="2" fill="none" stroke="currentColor" stroke-width=".6" stroke-dasharray="2.4 1.8"/>
          <g fill="currentColor"><use href="#tuerme"/></g>
          <path d="M0 -22 V-20.4 M0 -21.2 H-19.4 M-19.4 -22 V-20.4" stroke="currentColor" stroke-width=".5" fill="none"/>
          <text x="-9.7" y="-22.8" text-anchor="middle" font-size="5" fill="currentColor" font-family="DM Mono, monospace">x</text>
        </svg></div>
        <h3>Schutzraum</h3><p>Rund um das Zeichen bleibt so viel Luft, wie es hoch ist. Kein Text, kein Bildrand, keine Linie ragt hinein.</p>
      </div>
      <div class="regel" data-r="feder" style="--i:1">
        <div class="regel__f klein"><span>{zeichen()}<small>22 px</small></span><span>{zeichen()}<small>32 px</small></span><span>{zeichen()}<small>8 mm</small></span></div>
        <h3>Kleinste Grösse</h3><p>Die drei Türme allein am Bildschirm nicht unter 22 Pixel, im Druck nicht unter 8 Millimeter. Mit dem Namen darunter mindestens 150 Pixel oder 40 Millimeter breit.</p>
      </div>
      <div class="regel regel--breit" data-r="feder" style="--i:2">
        <div class="regel__f neine">{nein_html}</div>
        <h3>Was das Zeichen nicht darf</h3><p>Es steht gerade, in Logo-Grau, Kalk oder Bar-Gold, ohne Schatten und ohne Rahmen. Auf Fotos nur dort, wo die Fläche ruhig ist.</p>
      </div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="farben">
  <div class="in">
    {kopf('Farben', ['Achtzehn Töne,', 'jeder mit Fundstelle.'], 'Hell ist der Normalzustand: Kalk und Sandstein tragen den Lesetext. Nacht ist die eine dunkle Fläche, immer mit der Tapete; das Blau kommt aus der Windrose von Sa Clastra. Bar-Gold zeichnet und schreibt nie den Lesetext. Der Olivenhain ist die zweite Welt. Ein Klick auf eine Farbe kopiert ihren Wert.')}
    <div class="faecher" data-r="faecher"><div class="faecher__in">{faecher}</div><p class="faecher__h">Über den Fächer fahren, ein Klick kopiert den Farbwert.</p></div>
    <div class="anteil" data-r="anteil"><p class="mk__kap"><b>Mengenverhältnis</b><i></i><span>Richtwert für eine Seite oder ein Stück Papier</span></p><div class="anteil__b">{anteil_html}</div></div>
    {gruppen_html}
    <div class="kontrast">
      <div class="kontrast__k" data-r><p class="mk__kap"><b>Lesbarkeit</b><i></i></p><h3>Welche Farbe auf welcher stehen darf.</h3><p>Gerechnet nach dem internationalen Standard für Lesbarkeit im Netz (WCAG 2.1). Ab 4,5 zu 1 ist Lesetext gut lesbar, ab 3 zu 1 grosse Zeilen.</p></div>
      <ul class="kontrast__l" data-g>{kontrast_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="welten">
  <div class="in">
    {kopf('Zwei Farbwelten', ['Eine Entscheidung:', 'Nacht oder Hain.'], 'Beide Welten teilen Kalk, Sandstein und das Gold der Bar. Sie unterscheiden sich nur dort, wo die Seite dunkel wird und womit Titel betont werden. Welt A nimmt das Blau aus der Windrose von Sa Clastra, Welt B das Dunkel der Olivenhaine. Die Probe läuft in beiden Welten als eigene Seite, zum Scrollen. Robert wählt.')}
    <div class="welten" data-g>
      {welt_block('a', welt_a, 0)}
      {welt_block('b', welt_b, 1)}
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="herkunft">
  <div class="in">
    {kopf('Herkunft', ['Woher die Farben', 'kommen.'], 'Die Farben kommen nicht aus einem Fächer, sondern aus Ihrem Haus: aus dem Tor, aus Ihren eigenen Karten, aus der Bar und aus dem Olivenhain. Unter jedem Foto steht der Streifen, der beim Bau dieser Seite aus dem Bild selbst gemessen wurde, darunter die Töne, die daraus geworden sind.')}
    <div class="hers" data-g>{herkunft_html}</div>
  </div>
</section>

<section class="ab blatt papier" id="schrift">
  <div class="in">
    {kopf('Schrift', ['Die Schriften, die', 'das Haus schon hat.'], 'Fahkwang und Montserrat laden heute auf jeder Ihrer 302 Seiten. Fahkwang gibt den Titeln ihre Form, Montserrat hält lange Texte lesbar und steht in gesperrten Versalien wie die Unterzeile Ihrer Wortmarke. DM Mono steht bei Zeiten, Preisen und Adressen. Alle sind frei lizenziert und liegen als Dateien bei der Website, nichts wird von fremden Servern geladen.')}
    <div class="schs">{schrift_html}</div>
    <div class="rang">
      <div class="rang__k" data-r><p class="mk__kap"><b>Rangordnung</b><i></i></p><h3>Sieben Stufen, mehr braucht die Seite nicht.</h3><p>Grössen der neuen Website auf einem Rechner mit 1440 Pixel Breite. Auf dem Handy werden die Titel kleiner, der Lesetext bleibt.</p></div>
      <ul class="rang__l">{rang_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="tapete">
  <div class="in">
    {kopf('Tapete', ['Die Rosette', 'als Tapete.'], 'Das Muster ist die Rosette, die heute schon hinter dem Einstiegstext Ihrer Seite liegt, als Gitter mit feinen Rauten, zart und Ton in Ton. Es liegt auf der neuen Seite, in den Karten und auf den Drucksachen, immer im Wechsel: ein Abschnitt mit Tapete, der nächste ohne.')}
    <div class="tap" data-g>
      <figure class="tap__f tap__f--dunkel" data-r="feder" style="--i:0"><span class="streif"></span><figcaption class="kerbe kerbe--c">Auf Nacht</figcaption></figure>
      <figure class="tap__f tap__f--hell" data-r="feder" style="--i:1"><span class="streif"></span><figcaption class="kerbe kerbe--c">Auf Kalk und Sandstein</figcaption></figure>
    </div>
    <div class="prunk" data-r="prunk">
      <div class="prunk__z" style="--i:0"><b><span data-zahl="560">0</span></b><i></i><small>Pixel Rapport am Bildschirm</small></div>
      <div class="prunk__z" style="--i:1"><b><span data-zahl="8.5" data-komma>0</span></b><i></i><small>Prozent Deckkraft auf Hell, 7,5 auf Nacht</small></div>
      <div class="prunk__z" style="--i:2"><b><span>1 : 1</span></b><i></i><small>im Wechsel mit glatten Flächen</small></div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="bilder">
  <div class="in">
    {kopf('Bilder', ['Ihr Gut,', 'in echtem Licht.'], 'Gezeigt wird, was der Gast vorfindet: der Pool an der Steinmauer, die Suiten, Sa Clastra, das Konzert im Garten, die Tramuntana. Alle Fotos stammen von Ihrer Website; überarbeitet werden nur Schärfe und Licht, nie der Inhalt.')}
    <div class="collage" data-g>{bilder_html}</div>
    <div class="satz3" data-g>
      <div data-r style="--i:0"><h3>Fotos aus dem Haus.</h3><p>Jedes Bild zeigt einen echten Ort des Castell Son Claret. Erzeugte Bilder nur auf Roberts Wort, und dann als Platzhalter benannt.</p></div>
      <div data-r style="--i:1"><h3>Ein Farbpunkt je Bild.</h3><p>Die Bougainvillea, der Stern, ein Glas: ein kräftiger Punkt pro Foto, nie eine Fläche. Alles andere bleibt Stein, Grün, Himmel.</p></div>
      <div data-r style="--i:2"><h3>Der Name in der Einkerbung.</h3><p>Unten links, in Fahkwang, in einer ausgeschnittenen Bildecke mit runden Kanten. So steht jeder Name an derselben Stelle.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="bausteine">
  <div class="in">
    {kopf('Bausteine', ['Knöpfe, Linien', 'und Einkerbungen.'], 'Die kleinen Teile, die überall wiederkehren. Jeder Knopf hat Tiefe und einen runden Knauf mit Pfeil und gibt nach, wenn man ihn drückt. Probieren Sie es gern aus.')}
    <div class="baus" data-g>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f knr knr--mitte">{kn('Zimmer buchen', '#bausteine')}{kn('Das Anwesen', '#bausteine', 'kn--linie')}</div><h3>Knöpfe</h3><p>Sandstein auf Nacht, Nachtblau auf Kalk. Schrift in DM Mono, gesperrt, in Versalien.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f"><span class="strich">{zeichen()}</span></div><h3>Der Strich</h3><p>Eine feine Goldlinie über die ganze Breite, in der Mitte die drei Türme. Sie steht genau auf der Naht zwischen zwei Abschnitten.</p></div>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f"><figure class="kerbbild"><img src="{foto('luftbild')}" alt="" loading="lazy" decoding="async"><figcaption class="kerbe kerbe--d">Das Gut von oben</figcaption></figure></div><h3>Die Einkerbung</h3><p>Der Name eines Bildes in einer ausgeschnittenen Ecke mit runden Kanten, immer unten links.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f bau__f--titel" data-r="maske"><p class="mk__kap"><b>Es Capdellà · Mallorca</b><i></i></p><p class="bau__t"><span class="z"><span>Ein Landgut</span></span><span class="z"><span><em>am Fuß des Galatzó.</em></span></span></p></div><h3>Kapitelzeile und Titel</h3><p>Über jedem Titel eine Zeile in gesperrten Versalien mit wachsender Linie. Der Titel steigt Zeile für Zeile aus dem Schlitz, der zweite Teil in Gold.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="logo">
  <div class="in">
    {kopf('Logo richtig und falsch', ['Eingesetzt,', 'nie verändert.'], 'Die Wortmarke und das Zeichen sind Dateien aus Ihrem Haus. Sie werden eingesetzt, nie nachgezeichnet, nie verändert. Acht Dinge, die gehen, und acht, die nicht gehen.')}
    <p class="mk__kap" data-r><b>Richtig</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px;margin-bottom:clamp(40px,4vw,64px)">{richtig_html}</div>
    <p class="mk__kap" data-r><b>Falsch</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px">{falsch_html}</div>
  </div>
</section>

<section class="ab blatt papier" id="welt">
  <div class="in">
    {kopf('Die eigene Welt', ['Was nur', 'dieses Haus ist.'], ' '.join(e(x) for x in B.EIGENE_WELT['satz']))}
    <div class="satz3" data-g style="margin-top:0;padding-top:0;border-top:0">
      <div data-r style="--i:0"><h3>Charakter</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in T['charakter'])}</ul></div>
      <div data-r style="--i:1"><h3>Worte des Hauses</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in T['eigene_worte'])}</ul></div>
      <div data-r style="--i:2"><h3>Nicht</h3><ul class="nicht">{''.join(f'<li>{e(x)}</li>' for x in T['nicht'])}</ul></div>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="unterschied">
  <div class="in">
    {kopf('Projekt Nummer 10', ['Womit es sich von jedem', 'bisherigen Haus unterscheidet.'], 'Jedes Haus bekommt eine eigene Welt, kein Haus bekommt das System. Vor dieser Station wurden die Konzepte und Bausteine aller bisherigen Häuser gelesen; hier steht je Haus, was das Castell anders macht.')}
    <ul class="unter" data-g>{unterschiede}</ul>
  </div>
</section>

<section class="ab blatt marine tapete schluss" id="mitnehmen">
  <div class="in">
    {kopf('Zum Mitnehmen', ['Alles für das', 'nächste Stück.'], 'Das Zeichen und die Wortmarke als Vektor, die Rosette, die Windrose, die Farben als fertige Datei und die Schriften. Wer eine neue Karte, ein Schild oder eine Seite gestaltet, findet hier alles dafür.')}
    <ul class="laden" data-g>
      <li data-r style="--i:0"><span><b>Die drei Türme</b><small>Vektor, SVG, in jeder Grösse scharf</small></span>{kn('Laden', 'zeichen/tuerme-grau.svg', laden=True)}</li>
      <li data-r style="--i:1"><span><b>Wortmarke</b><small>Original des Hauses, SVG</small></span>{kn('Laden', 'logo/logo-dark.svg', laden=True)}</li>
      <li data-r style="--i:2"><span><b>Rosette</b><small>Tapete, SVG</small></span>{kn('Laden', 'zeichen/rosette-grau.svg', laden=True)}</li>
      <li data-r style="--i:3"><span><b>Windrose</b><small>Sa Clastra, SVG</small></span>{kn('Laden', 'zeichen/windrose-grau.svg', laden=True)}</li>
      <li data-r style="--i:4"><span><b>Farben</b><small>alle Töne mit Fundstelle als CSS-Datei</small></span>{kn('Laden', 'farben.css', laden=True)}</li>
      <li data-r style="--i:5"><span><b>Fahkwang</b><small>Regular 400, WOFF2</small></span>{kn('Laden', 'schriften/fahkwang-400-latin.woff2', laden=True)}</li>
      <li data-r style="--i:6"><span><b>Montserrat</b><small>400 und 500, WOFF2</small></span>{kn('Laden', 'schriften/montserrat-400-latin.woff2', laden=True)}</li>
      <li data-r style="--i:7"><span><b>DM Mono</b><small>Regular 400, WOFF2</small></span>{kn('Laden', 'schriften/DMMono-normal-400.woff2', laden=True)}</li>
    </ul>
    <div class="ende" data-r="ende">
      <span class="strich strich--gross">{zeichen()}</span>
      <p class="ende__w">{name()}</p>
      <p class="ende__s">Markenbuch Castell Son Claret · Station 05 der Kette · Entwurf von Tasty Studios, Oktober 2026. Drei Punkte offen: die Schrift der Wortmarke, die Herkunft der Rosette, Druckvorlagen des Logos.</p>
      <div class="knr knr--mitte">{kn('Die Probe', 'probe.html', neu=True)}{kn('Logo richtig und falsch', 'logo-richtig-falsch/index.html', 'kn--linie', neu=True)}</div>
    </div>
  </div>
</section>
</main>
<script src="marke.js?v={v_js}" defer></script>
</body>
</html>
'''


def logo_seite():
    """Die Logo-Regeln als eigene Seite, derselbe Stil, eine Ebene tiefer."""
    richtig_html, falsch_html = logo_karten()
    v_css = int(os.path.getmtime(os.path.join(M, 'marke.css'))); v_js = int(os.path.getmtime(os.path.join(M, 'marke.js')))
    s = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Logo richtig und falsch · Castell Son Claret</title><meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="../marke.css?v={v_css}"><script>document.documentElement.classList.add('js')</script></head>
<body>{B.sym_defs()}
<nav class="leiste" aria-label="Markenbuch"><a class="leiste__m" href="../markenbuch.html">{zeichen()}<span><b>Markenbuch</b><small>Logo richtig und falsch</small></span></a><div class="leiste__k"></div><a class="glanz" href="../markenbuch.html#logo">Zum Markenbuch{PF}</a></nav>
<main>
<section class="ab creme tapete-h" id="logo" style="padding-top:clamp(60px,7vw,110px)">
  <div class="in">
    {kopf('Logo richtig und falsch', ['Eingesetzt,', 'nie verändert.'], 'Die Wortmarke und das Zeichen sind Dateien aus Ihrem Haus (logo-dark.svg, logo-white.svg, sygnet.svg). Sie werden eingesetzt, nie nachgezeichnet, nie verändert.')}
    <p class="mk__kap" data-r><b>Richtig</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px;margin-bottom:clamp(40px,4vw,64px)">{richtig_html}</div>
    <p class="mk__kap" data-r><b>Falsch</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px">{falsch_html}</div>
  </div>
</section>
</main>
<script src="../marke.js?v={v_js}" defer></script></body></html>'''
    s = re.sub(r'((?:href|src)=")(?!\.\./|#|http|data:|\?)', r'\1../', s)
    s = s.replace('href="../../marke.css', 'href="../marke.css').replace('src="../../marke.js', 'src="../marke.js').replace('url(bilder/', 'url(../bilder/')
    os.makedirs(os.path.join(M, 'logo-richtig-falsch'), exist_ok=True)
    open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    css()
    open(os.path.join(M, 'markenbuch.html'), 'w', encoding='utf-8').write(seite())
    logo_seite()
    print('gebaut: markenbuch.html, marke.css, marke.js, logo-richtig-falsch/')
