#!/usr/bin/env python3
"""Station 05 · Markenbauer · Hotel Monte-Moro, Saas-Almagell, 17.10.2026.

Baut das Markenbuch nach dem Muster von Le Livre des Grand Beau-Rivage, wie das bestätigte Markenbuch des Castell Son Claret
(castell-bau2.py): dieselbe Bauart und Bewegung (Vorlage _vorlage/gbr-markenbuch.py, gbr-marke.css, gbr-marke.js), übersetzt auf
Bergkamm, Wortmarke, Farben, Schriften und Fotos dieses Hauses. Inhalte (Farben mit Fundstelle, Schriften, Ton, Welten) aus bau.py.
   python3 bau2.py      → marke/markenbuch.html, marke/marke.css, marke/marke.js, marke/logo-richtig-falsch/index.html
Geräte: Laptop aus Blender (geraet/laptop.png + laptop.json, Render des Grand Beau-Rivage über das Castell), Bildschirm geraet/schirm/*.png
aus geraet/schirme.js; Handy aus Blender (geraet/handy_render.py), sonst bis zum Render ein gezeichneter Rahmen."""
import html, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import bau as B  # noqa: E402

M = B.M
V = os.path.join(H, '_vorlage')
e = html.escape
F = B.F
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
PU = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14h10"/></svg>'

# ---------------------------------------------------------------- Farben in Gruppen, alle aus bau.FARBEN
GRUPPEN = [
    ('hell', 'Helle Flächen', 'Der Normalzustand. Hier wird gelesen, so hell wie die Fassade in der Sonne.', [
        ('papier', 'Papier', F['Papier'], 'Grundfläche der Seite, Tapete hell'),
        ('fassade', 'Fassade', F['Fassade'], 'zweite helle Fläche, Karten'),
        ('wandschatten', 'Wandschatten', F['Wandschatten'], 'Kanten, Unterseite der Knöpfe')]),
    ('dunkel', 'Das Blau', 'Aus dem Logo. Nacht ist die dunkle Fläche der Welt A und die Farbe des Lesetextes, Logo-Blau trägt die Knöpfe.', [
        ('nacht', 'Nacht', F['Nacht'], 'dunkle Fläche, Lesetext'),
        ('nachtblau', 'Nachtblau', F['Nachtblau'], 'Kuhlen und Platten auf Dunkel'),
        ('logo-blau', 'Logo-Blau', F['Logo-Blau'], 'Knöpfe, Haken, Zeichen auf Hell')]),
    ('laerche', 'Lärche', 'Das Holz der Balkone und der Stube. Zeichnet und betont, schreibt nie den Lesetext.', [
        ('laerche', 'Lärche', F['Lärche'], 'Zeichen und Zeilen auf Nacht'),
        ('laerche-tief', 'Lärche tief', F['Lärche tief'], 'zweite Titelzeile auf Hell'),
        ('stubenholz', 'Stubenholz', F['Stubenholz'], 'Holzkanten, Karten des Röstihüs')]),
    ('welt-b', 'Butzenglas und Jute', 'Farbwelt B: das Licht im Raclettestübli und die Säcke vor dem Röstihüs, auf dem Blau des Logos.', [
        ('butzenglas', 'Butzenglas', F['Butzenglas'], 'Akzent in Welt B'),
        ('jute', 'Jute', F['Jute'], 'Linien und Zeichen in Welt B'),
        ('jute-tief', 'Jute tief', F['Jute tief'], 'zweite Titelzeile in Welt B')]),
    ('heute', 'Nur auf der heutigen Seite', 'Gemessen, aber nicht übernommen: nicht im Logo, nicht im Haus.', [
        ('seiten-blau', 'Seiten-Blau', F['Seiten-Blau'], 'heute Titel und Links'),
        ('himmelblau', 'Himmelblau', F['Himmelblau'], 'heute Balken und Knöpfe'),
        ('geschenk-gruen', 'Geschenk-Grün', F['Geschenk-Grün'], 'heute Geschenk-Kacheln'),
        ('seiten-grau', 'Seiten-Grau', F['Seiten-Grau'], 'heute Lauftext')]),
]
FK = {k: (n, h) for _, _, _, l in GRUPPEN for k, n, h, _ in l}

HERKUNFT = [
    ('fassade-sommer', 'Die Fassade im Sommer', 'Die weisse Wand in der Sonne und die Balkone aus Lärche, fotografiert für Schweiz Tourismus. Daraus sind die hellen Flächen geworden und der Akzent der Welt A.', ['papier', 'fassade', 'wandschatten', 'laerche', 'laerche-tief'], '50% 40%'),
    ('reception', 'Das Zeichen an der Rezeption', 'Der Bergkamm steht gross an der Wand neben der Rezeption. Das Blau kommt aus der Logo-Datei des Hauses; Nacht und Nachtblau sind daraus abgedunkelt.', ['logo-blau', 'nacht', 'nachtblau'], '55% 55%'),
    ('roestihues', 'Die Säcke vor dem Röstihüs', 'Kartoffelsäcke mit Gesichtern und das Holzschild mit dem Logo. Die Jute ist der Akzent der Welt B.', ['jute', 'jute-tief'], '50% 35%'),
    ('raclettestuebli', 'Die Butzenscheiben im Raclettestübli', 'Runde Scheiben im warmen Licht der Stube. Daraus das Butzenglas, das Gold der Welt B.', ['butzenglas'], '80% 50%'),
    ('stube', 'Die Stube des Röstihüs', 'Holzdecke, Tische und der Kartoffelsack auf dem Tresen. Das Stubenholz bleibt für Holzkanten und die Karte.', ['stubenholz'], '50% 50%'),
    ('fassade-winter', 'Das Haus im Schnee', 'Schnee und Himmel bleiben im Bild und werden nie Fläche: Blau kommt nur aus dem Logo, Weiss aus der Wand.', [], '50% 55%'),
]
WELT_B_CSS = (f'[data-welt="b"]{{--marine:{F["Logo-Blau"]};--blau:{F["Nacht"]};--aare:{F["Nacht"]};--gold:{F["Butzenglas"]};--akzent:{F["Jute tief"]};--taupe:{F["Jute tief"]};--taupe-tief:{F["Jute tief"]}}}\n'
              '[data-welt="b"] .tapete,[data-welt="b"] .leiste::after,[data-welt="b"] .tap__f--dunkel{background-image:url(zeichen/tapete-dunkel-b.svg)}')


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
    la, lb = lum(a), lum(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def streifen(key, n=5):
    from PIL import Image
    im = Image.open(os.path.join(M, 'bilder', key + '.jpg')).convert('RGB'); im.thumbnail((360, 360))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:n * 3]; ges = im.size[0] * im.size[1]
    t = [(c / ges, '#%02x%02x%02x' % tuple(pal[i * 3:i * 3 + 3])) for c, i in q.getcolors()]
    t.sort(key=lambda x: -lum(x[1])); return t


# ---------------------------------------------------------------- Bausteine
ZVB, WVB = B.ZVB, B.WVB


def zeichen(kl='', titel=''):
    lab = f' role="img" aria-label="{e(titel)}"' if titel else ' aria-hidden="true"'
    return f'<svg class="{kl}" viewBox="{ZVB}" fill="currentColor"{lab}><use href="#bergkamm"/></svg>'


def wort(kl=''):
    return f'<svg class="{kl}" viewBox="{WVB}" fill="currentColor" role="img" aria-label="Monte Moro, Saas-Almagell"><use href="#wortmarke"/></svg>'


def medaillon(kl='', farbe='currentColor'):
    return f'<svg class="{kl}" viewBox="0 0 200 200" aria-hidden="true">{B.medaillon_innen(farbe)}</svg>'


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
    """Laptop aus Blender mit dem Bildschirminhalt der Probe darunter (Loch im Gehäuse, Mass aus laptop.json), daneben das Handy."""
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
    fonts = ("@font-face{font-family:'Fjalla One';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/FjallaOne-400.woff2') format('woff2')}\n"
             "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url('schriften/InstrumentSans-normal-400_600.woff2') format('woff2')}\n"
             "@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/DMMono-normal-400.woff2') format('woff2')}\n"
             "@font-face{font-family:'Sofia Sans Condensed';font-style:normal;font-weight:600;font-display:swap;src:url('schriften/SofiaSansCondensed-600.woff2') format('woff2')}\n"
             "@font-face{font-family:'Encode Sans Condensed';font-style:normal;font-weight:500;font-display:swap;src:url('schriften/EncodeSansCondensed-500.woff2') format('woff2')}\n"
             "@font-face{font-family:'Young Serif';font-style:normal;font-weight:400;font-display:swap;src:url('schriften/YoungSerif-400.woff2') format('woff2')}\n"
             "@font-face{font-family:'Titel Ersatz';src:local('Arial Narrow'),local('Arial');size-adjust:96%}\n")
    s = s.replace(kopf_alt, '/* Markenbuch Hotel Monte-Moro · Station 05 · Tasty Studios · 17.10.2026. Bauart und Bewegung wie Le Livre des Grand Beau-Rivage\n   (Vorlage _vorlage/gbr-marke.css), über das Markenbuch des Castell Son Claret; Farben, Schriften und Tapete dieses Hauses. Nur transform und opacity, nativer Scroll. */\n\n' + fonts)
    root_alt = re.search(r':root\{.*?\n\}', s, re.S).group(0)
    root_neu = (':root{\n'
                f"  --weiss:#FFFFFF; --papier:{F['Papier']}; --creme:{F['Fassade']}; --sand:{F['Wandschatten']};\n"
                f"  --marine:{F['Nacht']}; --blau:{F['Logo-Blau']}; --aare:{F['Nachtblau']}; --tinte:{F['Nacht']};\n"
                f"  --gold:{F['Lärche']}; --taupe:{F['Lärche tief']}; --akzent:{F['Lärche tief']}; --taupe-tief:{F['Lärche tief']}; --rot:#9b2c22;\n"
                "  --linie:rgba(10,42,74,.16); --linie-d:rgba(198,113,68,.24);\n"
                "  --serif:'Fjalla One','Titel Ersatz','Arial Narrow',sans-serif;\n"
                "  --caps:'Instrument Sans',Arial,sans-serif;\n"
                "  --sans:'Instrument Sans',system-ui,-apple-system,'Segoe UI',sans-serif;\n"
                "  --mono:'DM Mono',ui-monospace,'SF Mono',Menlo,monospace;\n"
                "  --e1:cubic-bezier(.16,1,.3,1); --e2:cubic-bezier(.32,.72,0,1); --e3:cubic-bezier(.19,1,.22,1);\n"
                "  --feder:cubic-bezier(.28,1.42,.42,1); --landen:cubic-bezier(.2,1.12,.3,1);\n"
                "  --rand:clamp(18px,5vw,96px); --max:1440px; --ab:clamp(110px,11.5vw,190px); --rund:clamp(28px,3.6vw,56px); --r:clamp(20px,2vw,28px);\n"
                "  --start:0s;\n}\n" + WELT_B_CSS)
    s = s.replace(root_alt, root_neu)
    s = s.replace('url(../../assets/img/tapete-dunkel.webp)', 'url(zeichen/tapete-dunkel.svg)').replace('url(../../assets/img/tapete-hell.webp)', 'url(zeichen/tapete-hell.svg)').replace('340px auto', '480px auto')
    karte = {'#1b2033': F['Nacht'], '#151a2b': '#08223D', '#181c2d': '#0B2D50', '#20263c': '#0D3358', '#232a43': '#0E365E', '#262c45': '#0F3963', '#171b2b': '#08223D', '#141827': '#071E36', '#1a1d28': F['Nacht'],
             '#323a58': F['Nachtblau'], '#3f4767': F['Nachtblau'], '#2c334d': F['Logo-Blau'],
             '#cdaa5c': F['Lärche'], '#fbf0cf': '#F6DCC9', '#ead39c': '#E4AE8A', '#c9a764': F['Lärche'], '#9c7b43': '#8A4626', '#dcc189': '#D9946B', '#f3e3b6': '#F1CDB3', '#e6d2a2': F['Lärche'],
             '#f9f1e1': '#F8F6F3', '#fdf5e8': '#FAF8F5', '#eee2cc': F['Fassade'], '#c8ba9e': F['Wandschatten'], '#fdf9f1': '#FFFFFF', '#e8dcc3': F['Fassade'], '#e7dcc6': F['Fassade'], '#efe4cf': F['Fassade'], '#f7f0e3': F['Papier'],
             '#fff7e2': '#FAF8F5', '#b0934f': F['Lärche tief'], '#967d40': F['Lärche tief'], '#826c35': F['Lärche tief'], '#6d5a2c': '#6E3A1F', '#e2d2b5': F['Wandschatten'], '#2aa198': '#1d7a55', '#7a1f2b': '#9b2c22'}
    s = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: karte.get(m.group(0).lower(), m.group(0)), s)
    for a, b in (('rgba(26,29,40', 'rgba(10,42,74'), ('rgba(253,249,241', 'rgba(255,255,255'), ('rgba(230,210,162', 'rgba(198,113,68'), ('rgba(130,108,53', 'rgba(154,79,43'),
                 ('rgba(150,166,214', 'rgba(107,160,214'), ('rgba(210,191,152', 'rgba(214,204,193')):
        s = s.replace(a, b)
    s += '''
/* ---------- Hotel Monte-Moro: Fjalla One hat nur eine Stärke, nie künstlich fett ---------- */
html{font-synthesis:none}
.welt__tafel{min-height:clamp(240px,22vw,320px)}
.welten{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(22px,3vw,52px)}
.welt{display:flex;flex-direction:column;gap:18px}
.welt__k{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap}
.welt__k h3{font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,2.4vw,2.5rem);line-height:1.05}
.welt__k h3 em{font-style:normal;color:var(--akzent)} .marine .welt__k h3 em{color:var(--gold)}
.welt__b{display:flex;gap:8px}
.welt__b i{width:34px;height:34px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.welt p{font-size:1rem;line-height:1.66;color:rgba(10,42,74,.84);max-width:48ch} .marine .welt p{color:rgba(255,255,255,.82)}
.ger{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 24%;align-items:end;gap:0}
.ger__laptop{position:relative;width:100%}
.ger__huelle{position:relative;z-index:2;width:100%;height:auto;display:block}
.ger__inhalt{position:absolute;z-index:1;object-fit:cover;object-position:50% 0;border-radius:1.8% 1.8% 0 0}
.ger__tel{position:relative;z-index:3;width:138%;margin-left:-38%;margin-bottom:-6%;height:auto;filter:drop-shadow(0 26px 22px rgba(10,42,74,.28))}
.ger__tel--css{display:block;width:30%;margin-left:-6%;margin-bottom:6%;padding:5px;border-radius:26px;background:#0b0c10;box-shadow:0 30px 40px -24px rgba(0,0,0,.6),inset 0 0 0 1px rgba(255,255,255,.08)}
.ger__tel--css img{width:100%;border-radius:21px}
.reihe5{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(14px,1.6vw,24px);margin-top:clamp(16px,1.8vw,28px)}
.zei{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;text-align:center;gap:14px;padding:clamp(22px,2.4vw,34px) 16px;border-radius:var(--r);background:var(--weiss);box-shadow:inset 0 0 0 1px var(--linie),0 30px 40px -32px rgba(10,42,74,.4)}
.zei svg,.zei img{height:clamp(54px,5.4vw,78px);width:auto;max-width:100%;color:var(--blau)}
.zei b{font-family:var(--serif);font-weight:400;font-size:1.2rem;line-height:1.15}
.zei small{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;line-height:1.4;color:rgba(10,42,74,.62)}
.regeln--4{grid-template-columns:repeat(4,minmax(0,1fr))}
.regel--f .regel__f{position:relative}
.regel--f .regel__f::before{content:'';position:absolute;inset:0;border-radius:14px;box-shadow:inset 0 0 0 1.5px var(--rot);pointer-events:none;z-index:2}
.regel--f .regel__f::after{content:'';position:absolute;right:10px;top:10px;width:26px;height:26px;z-index:3;background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'><circle cx='15' cy='15' r='15' fill='%239b2c22'/><path d='M10 10l10 10M20 10L10 20' stroke='white' stroke-width='2.4' stroke-linecap='round'/></svg>") center/contain no-repeat}
.lf{width:100%;min-height:170px;display:flex;align-items:center;justify-content:center;gap:16px;border-radius:14px;overflow:hidden}
.lf svg,.lf img{height:auto}
.satz3 ul{display:grid;gap:9px} .satz3 li{position:relative;padding-left:20px;font-size:.98rem;line-height:1.5;color:rgba(10,42,74,.8)}
.satz3 li::before{content:'';position:absolute;left:0;top:.7em;width:9px;height:1.5px;background:var(--akzent)}
.satz3 .nicht li::before{background:var(--rot)}
.unter{display:grid;gap:0;border-top:1px solid var(--linie-d)}
.unter li{display:grid;grid-template-columns:minmax(150px,260px) 1fr;gap:20px;padding:18px 0;border-bottom:1px solid var(--linie-d);opacity:0;transform:translate3d(0,22px,0);transition:opacity 1s var(--e2),transform 1.3s var(--e1);transition-delay:calc(var(--i,0)*90ms)}
.da .unter li,.unter.da li{opacity:1;transform:none}
.unter b{font-family:var(--serif);font-weight:400;font-size:1.25rem;line-height:1.15} .unter span{color:rgba(255,255,255,.82);font-size:.98rem;line-height:1.55}
/* Schriftwahl: freie Schriften neben der Wortmarke (Master 2.2) */
.wahl{display:grid;gap:0;margin-top:clamp(36px,4vw,64px);border-radius:var(--r);overflow:hidden;background:var(--weiss);box-shadow:inset 0 0 0 1px var(--linie),0 40px 60px -44px rgba(10,42,74,.5)}
.wahl__z{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(18px,3vw,48px);align-items:center;padding:clamp(18px,2vw,28px) clamp(20px,2.6vw,40px);border-bottom:1px solid var(--linie)}
.wahl__z:last-child{border-bottom:0}
.wahl__z--logo{background:var(--papier)}
.wahl__p{font-size:clamp(2.4rem,4.6vw,4.6rem);line-height:1;color:var(--blau);white-space:nowrap}
.wahl__p img{height:clamp(64px,6.4vw,104px);width:auto}
.wahl__n{display:flex;flex-direction:column;gap:6px}
.wahl__n b{font-family:var(--mono);font-weight:400;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tinte)}
.wahl__n em{font-style:normal;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--akzent)}
.wahl__n span{font-size:.98rem;line-height:1.5;color:rgba(10,42,74,.8)}
.wahl__z--gewaehlt{box-shadow:inset 4px 0 0 var(--gold)}
/* 18.10.2026, Robert 00:10: «Keine Einkerbungen benutzen bei den neuen Projekten» → Bildzeile ohne Ausschnitt: auf Fotos weich unten im Bild, auf Karten und Tafeln als ruhige Zeile unten mittig */
.kerbe.kerbe{position:absolute;left:0;right:0;top:auto;bottom:0;z-index:3;max-width:none;transform:none;margin:0;border-radius:0;padding:clamp(40px,3.4vw,56px) clamp(16px,1.6vw,24px) clamp(12px,1.2vw,18px);background:linear-gradient(180deg,rgba(10,42,74,0),rgba(10,42,74,.74));color:#fff;font-family:var(--serif);font-weight:400;font-size:clamp(1rem,1.2vw,1.2rem);line-height:1.15;text-align:left;white-space:normal;text-shadow:0 1px 3px rgba(3,10,16,.5)}
.kerbe.kerbe::before,.kerbe.kerbe::after{display:none;content:none}
.lock .kerbe.kerbe,.tap__f .kerbe.kerbe,.welt__tafel .kerbe.kerbe{background:none;text-shadow:none;padding:0 20px;bottom:clamp(20px,2vw,28px);text-align:center;font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.8)}
.lock--papier .kerbe.kerbe,.lock--quer .kerbe.kerbe,.tap__f--hell .kerbe.kerbe{color:var(--akzent)}
/* Helle Tapete mit Untergrund (Robert 00:10: «weiß auf weiß … Bitte macht da nochmal so einen Untergrund»): Papier mit Tapete auf einer Unterlage im Mittelton */
.tap__f--hell{background:var(--papier) url(zeichen/tapete-hell.svg) 50% 0/480px auto;box-shadow:inset 0 0 0 clamp(14px,1.8vw,24px) var(--sand),inset 0 0 0 calc(clamp(14px,1.8vw,24px) + 1px) rgba(10,42,74,.14),0 36px 48px -30px rgba(10,42,74,.5)}
.welt--gewaehlt .welt__k h3::after{content:'Gewählt';margin-left:14px;padding:5px 12px 4px;border-radius:999px;vertical-align:.35em;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:var(--blau)}
.welt--nicht{opacity:.62}
/* Übergänge als Bergkamm (Robert 00:10: «Übergang Linie wie ein Bergkamm»): jede Fläche beginnt mit dem Grat statt mit runder Kante */
.blatt{border-radius:0}
.blatt>.grat-naht{position:absolute;left:0;right:0;top:0;width:100%;height:clamp(22px,3vw,44px);transform:translateY(-99%);display:block;pointer-events:none;z-index:2}
/* Wortmarke auf Nacht immer in Papier, wie im Logo-Regelblatt */
.lock--marine .lock__w{color:var(--papier)}
/* Ortszeile am Handy: umbrechen zwischen den Orten, nie im Wort */
@media (max-width:620px){.titel__ort{flex-wrap:wrap;justify-content:center;letter-spacing:.22em;row-gap:10px;max-width:100%}}
/* Querform: der Kamm ist fünfmal so breit wie hoch */
.lock--quer .lock__z{width:clamp(120px,11vw,170px);color:var(--blau)}
.lock--quer .lock__w{width:auto;font-family:var(--serif);font-size:clamp(1.6rem,2.4vw,2.4rem);line-height:1;color:var(--tinte)}
/* Der Grat: die Naht zwischen hell und dunkel */
.gratnaht{position:relative;width:100%;height:clamp(70px,8vw,120px);border-radius:14px;overflow:hidden;background:var(--papier)}
.gratnaht .grat{position:absolute;left:0;right:0;bottom:0;width:100%;height:60%}
.gratnaht::after{content:'';position:absolute;left:0;right:0;bottom:0;height:12%;background:var(--marine)}
.f-ti{font-family:'Fjalla One','Titel Ersatz',sans-serif} .f-so{font-family:'Sofia Sans Condensed',sans-serif;font-weight:600} .f-en{font-family:'Encode Sans Condensed',sans-serif;font-weight:500} .f-yo{font-family:'Young Serif',Georgia,serif}
@media (max-width:1000px){.welten{grid-template-columns:1fr}.reihe5{grid-template-columns:repeat(2,minmax(0,1fr))}.regeln--4{grid-template-columns:repeat(2,minmax(0,1fr))}.wahl__z{grid-template-columns:1fr}}
@media (max-width:620px){.regeln--4{grid-template-columns:1fr}.unter li{grid-template-columns:1fr;gap:6px}.ger{grid-template-columns:minmax(0,1fr) 30%}.wahl__p{font-size:2.6rem}}
'''
    open(os.path.join(M, 'marke.css'), 'w', encoding='utf-8').write(s)
    js = open(os.path.join(V, 'gbr-marke.js'), encoding='utf-8').read().replace('Markenbuch Grand Beau-Rivage', 'Markenbuch Hotel Monte-Moro')
    js += '''
/* Farbwelt A/B im Markenbuch umschalten (wie Castell Son Claret): nur ein Attribut am body, die Farben kommen aus dem CSS */
(function(){var w=new URLSearchParams(location.search).get('welt');if(w==='b')document.body.setAttribute('data-welt','b');
document.querySelectorAll('[data-welt-knopf]').forEach(function(b){b.addEventListener('click',function(ev){ev.preventDefault();var x=b.getAttribute('data-welt-knopf');if(x==='b')document.body.setAttribute('data-welt','b');else document.body.removeAttribute('data-welt');
document.querySelectorAll('[data-welt-knopf]').forEach(function(k){k.classList.toggle('kn--linie',k!==b)});});});})();
'''
    open(os.path.join(M, 'marke.js'), 'w', encoding='utf-8').write(js)


# ---------------------------------------------------------------- Logo richtig und falsch
def logo_karten(pre=''):
    k = F
    def wm(farbe, st=''): return f'<svg viewBox="{WVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#wortmarke"/></svg>'
    def zm(farbe, st=''): return f'<svg viewBox="{ZVB}" style="fill:{farbe};{st}" aria-hidden="true"><use href="#bergkamm"/></svg>'
    png = f'<img src="{pre}logo/logo-original-1161px.png" alt="" style="width:62%">'
    richtig = [
        ('Das Original', f'<div class="lf" style="background:#fff">{png}</div>', 'Die Datei des Hauses, in Logo-Blau auf Weiss. Sie geht überall dort, wo die Fläche hell ist.'),
        ('Wortmarke auf Nacht', f'<div class="lf tapete" style="background-color:{k["Nacht"]}">{wm(k["Papier"], "width:62%")}</div>', 'Auf dunkler Fläche in Papier, aus dem Vektor gezogen, Form unverändert.'),
        ('Der Bergkamm allein', f'<div class="lf" style="background:{k["Fassade"]}">{zm(k["Logo-Blau"], "width:56%")}</div>', 'Die zwei Gipfel stehen allein in der Leiste, über Überschriften und an der Wand, wie an der Rezeption.'),
        ('Bergkamm in Lärche', f'<div class="lf tapete" style="background-color:{k["Nacht"]}">{zm(k["Lärche"], "width:56%")}</div>', 'Auf Nacht darf der Bergkamm in Lärche stehen, in Welt B in Butzenglas.'),
        ('Mindestgrösse', f'<div class="lf" style="background:{k["Papier"]};flex-direction:column;gap:18px">{wm(k["Logo-Blau"], "width:150px")}<span class="mono" style="font-size:10px;color:{k["Lärche tief"]};letter-spacing:.12em">150 PX · DARUNTER NUR DER BERGKAMM</span></div>', 'Mit «Saas-Almagell» bleibt die Wortmarke bis 150 px Breite lesbar. Kleiner steht nur der Bergkamm.'),
        ('Schutzraum', f'<div class="lf" style="background:{k["Papier"]}"><div style="position:relative;padding:9%;outline:1px dashed {k["Lärche tief"]};width:84%">{wm(k["Logo-Blau"], "width:100%")}</div></div>', 'Rundum so viel Luft wie das «o» in «Moro» hoch ist. Nichts rückt näher heran.'),
        ('Auf dem Foto', f'<div class="lf" style="background:url({pre}{foto("fassade-sommer")}) 50% 0/cover">{wm(k["Papier"], "width:58%")}</div>', 'Nur auf einer ruhigen Fläche des Bildes, hier der Himmel, in Papier, nie mit Schatten oder Saum.'),
        ('Das Medaillon', f'<div class="lf" style="background:{k["Fassade"]};color:{k["Logo-Blau"]}">{medaillon("", k["Logo-Blau"]).replace("<svg ", "<svg style=\"width:52%\" ")}</div>', 'Der Bergkamm im Kreis ist das Siegel für Tapete, Stempel und das Zeichen im Browser, nie Ersatz für die Wortmarke.'),
    ]
    falsch = [
        ('Gestreckt', f'<div class="lf" style="background:{k["Papier"]}">{wm(k["Logo-Blau"], "width:60%;transform:scaleX(1.35)")}</div>', 'Die Proportion bleibt. Nie breiter oder höher gezogen.'),
        ('Umgefärbt', f'<div class="lf" style="background:{k["Papier"]}">{wm(k["Geschenk-Grün"], "width:62%")}</div>', 'Nur Logo-Blau, Nacht, Papier, Lärche und Butzenglas. Kein Grün, kein Verlauf.'),
        ('Mit Schatten und Glanz', f'<div class="lf" style="background:{k["Nacht"]}">{wm(k["Papier"], "width:62%;filter:drop-shadow(0 6px 10px rgba(0,0,0,.9)) drop-shadow(0 0 18px rgba(198,113,68,.9))")}</div>', 'Kein Schatten, kein Leuchten, kein Relief. Die Wortmarke liegt flach.'),
        ('Neu gesetzt', f'<div class="lf" style="background:{k["Papier"]};font-family:var(--serif);font-size:clamp(28px,3vw,44px);color:{k["Logo-Blau"]}">Monte Moro</div>', 'Der Name wird nie in der Titelschrift nachgeschrieben, auch nicht in Fjalla One. Die Wortmarke ist eine Datei.'),
        ('Auf unruhigem Foto', f'<div class="lf" style="background:url({pre}{foto("stube")}) 50% 50%/cover">{wm(k["Papier"], "width:58%")}</div>', 'Holz, Lampen und Tische hinter den Buchstaben: unlesbar. Ein anderes Foto oder eine Fläche.'),
        ('Gedreht und beschnitten', f'<div class="lf" style="background:{k["Papier"]}">{wm(k["Logo-Blau"], "width:66%;transform:rotate(-12deg) translate(18%,6%)")}</div>', 'Die Wortmarke steht immer waagrecht und ganz.'),
        ('Gipfel getrennt', f'<div class="lf" style="background:{k["Papier"]};flex-direction:column">{zm(k["Logo-Blau"], "width:40%")}<span style="font-family:var(--serif);font-size:26px;color:{k["Logo-Blau"]}">Monte Moro</span></div>', 'Bergkamm und Name stehen im Logo ineinander. Sie werden nie auseinandergenommen und neu gestellt.'),
        ('Zu klein', f'<div class="lf" style="background:{k["Papier"]}">{wm(k["Logo-Blau"], "width:80px")}</div>', 'Unter 150 px ist «Saas-Almagell» nicht mehr lesbar. Dann nur der Bergkamm.'),
    ]
    def karten(liste, kl):
        return ''.join(f'<div class="regel {kl}" data-r="feder" style="--i:{i % 4}"><div class="regel__f">{b}</div><h3>{e(t)}</h3><p>{e(s)}</p></div>' for i, (t, b, s) in enumerate(liste))
    return karten(richtig, 'regel--r'), karten(falsch, 'regel--f')


# ---------------------------------------------------------------- die Seite
def seite():
    alle = [(k, n, h, r) for _, _, _, l in GRUPPEN[:4] for k, n, h, r in l]
    n_f = len(alle)
    TD, TH = F['Nacht'], F['Papier']
    faecher = ''.join(f'''<button class="fa" type="button" data-hex="{h}" style="--c:{h};--t:{TD if lum(h) > .35 else TH};--j:{j};--w:{(j - (n_f - 1) / 2) * 5.4:.1f}deg" aria-label="{e(n)} {h.upper()} kopieren">
          <span class="fa__n"><b>{e(n)}</b><small>{h.upper()}</small></span><span class="fa__ok">kopiert</span>
        </button>''' for j, (k, n, h, r) in enumerate(alle))
    gruppen_html = ''
    for gk, gname, gsatz, liste in GRUPPEN:
        karten = ''.join(f'''<button class="fk" type="button" data-r="feder" data-hex="{h}" style="--i:{i};--c:{h};--t:{TD if lum(h) > .35 else TH}" aria-label="{e(n)} {h.upper()} kopieren">
            <span class="fk__f"><span class="fk__hex">{h.upper()}</span><span class="fk__ok">kopiert</span></span>
            <span class="fk__n">{e(n)}</span>
            <span class="fk__r">{e(r)}</span>
            <span class="fk__w"><span>HEX</span>{h.upper()}<span>RGB</span>{' · '.join(map(str, rgb(h)))}</span>
          </button>''' for i, (k, n, h, r) in enumerate(liste))
        gruppen_html += f'''<div class="gr gr--{gk}" data-g>
        <div class="gr__k" data-r style="--i:0"><p class="mk__kap"><b>{e(gname)}</b><i></i></p><p class="gr__s">{e(gsatz)}</p></div>
        <div class="gr__l gr__l--{len(liste)}">{karten}</div>
      </div>'''
    anteile = [('Papier und Fassade', 62, F['Papier'], F['Nacht']), ('Nacht', 24, F['Nacht'], F['Lärche']), ('Logo-Blau', 8, F['Logo-Blau'], '#FFFFFF'), ('Lärche', 6, F['Lärche'], '#FFFFFF')]
    anteil_html = ''.join(f'<span style="--p:{p};--j:{j};background:{c};color:{t}"><b><span data-zahl="{p}">0</span> %</b><small>{e(n)}</small></span>' for j, (n, p, c, t) in enumerate(anteile))
    paare = [('Nacht auf Papier', 'nacht', 'papier', 'Lesetext'), ('Papier auf Nacht', 'papier', 'nacht', 'Lesetext auf Dunkel'),
             ('Lärche auf Nacht', 'laerche', 'nacht', 'Titel und Zeichen auf Dunkel'), ('Lärche tief auf Papier', 'laerche-tief', 'papier', 'zweite Titelzeile'),
             ('Papier auf Logo-Blau', 'papier', 'logo-blau', 'Schrift im Knopf, Welt B'), ('Butzenglas auf Logo-Blau', 'butzenglas', 'logo-blau', 'Zeichen in Welt B'),
             ('Lärche auf Papier', 'laerche', 'papier', 'nur grosse Zeilen'), ('Jute auf Papier', 'jute', 'papier', 'nie als Schrift')]
    def urteil(r):
        if r >= 7: return 'Sehr gut, auch für langen Text'
        if r >= 4.5: return 'Gut für Lesetext'
        if r >= 3: return 'Nur für grosse Zeilen'
        return 'Nur Schmuck, nie Schrift'
    kontrast_html = ''
    for i, (t, a, b, w) in enumerate(paare):
        r = kontrast(FK[a][1], FK[b][1])
        kontrast_html += f'''<li class="ko" data-r="feder" style="--i:{i % 3};--g:{FK[b][1]};--s:{FK[a][1]}">
          <span class="ko__p"><span>Aa</span><small>Mehr erleben, weniger zahlen.</small></span>
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
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyzäöüß<br>0123456789 · CHF 90.00 · 3905'
    schriften = [
        ('a', 'Grosse Zeilen', 'Fjalla One', 'Regular 400, gross und klein, nie gesperrt', 'Titel, Namen, Preise; aus der Wortmarke abgeleitet', 'Aa', 'Mehr erleben, weniger zahlen.', ALPHA),
        ('s', 'Lesetext', 'Instrument Sans', 'Regular 400 und Semibold 600', 'alles, was gelesen wird, Kapitelzeilen', 'Aa', 'Es lebe die Tradition!', ALPHA),
        ('m', 'Kleine Angaben', 'DM Mono', 'Regular 400', 'Zeiten, Preise, Adressen, Knöpfe', 'Aa', 'Kidsclub · Mo - Sa 16:30', ALPHA),
    ]
    def rollen(text):
        return ''.join(f'<span class="ro" style="--k:{i}" data-c="{e(c)}">{e(c)}</span>' if c != ' ' else ' ' for i, c in enumerate(text))
    schrift_html = ''.join(f'''<article class="sch" data-g>
        <div class="sch__k" data-r style="--i:0"><p class="mk__kap"><b>{e(r)}</b><i></i></p><h3 class="sch__n f-{c}">{e(n)}</h3><dl><dt>Schnitt</dt><dd>{e(s)}</dd><dt>Wofür</dt><dd>{e(w)}</dd></dl></div>
        <div class="sch__aa f-{c}" data-r="maske" aria-hidden="true"><span class="z"><span>{aa}</span></span></div>
        <div class="sch__r" data-r style="--i:2"><p class="sch__satz f-{c}" aria-label="{e(probe)}">{rollen(probe)}</p><p class="sch__abc f-{c}">{abc}</p></div>
      </article>''' for c, r, n, s, w, aa, probe, abc in schriften)
    wkl = {'Fjalla One': 'f-ti', 'Sofia Sans Condensed 600': 'f-so', 'Encode Sans Condensed 500': 'f-en', 'Young Serif': 'f-yo'}
    wahl_html = (f'<div class="wahl__z wahl__z--logo" data-r style="--i:0"><span class="wahl__p"><img src="logo/logo-original-1161px.png" alt="Die Wortmarke des Hauses"></span><span class="wahl__n"><b>Die Wortmarke</b><em>Original des Hauses</em><span>Eine schmale, kräftige Groteske, gross und klein geschrieben, das t schräg geschnitten, die Gipfel darüber von Hand gezogen.</span></span></div>'
                 + ''.join(f'<div class="wahl__z{" wahl__z--gewaehlt" if u == "gewählt" else ""}" data-r style="--i:{i + 1}"><span class="wahl__p {wkl[n]}">Monte Moro</span><span class="wahl__n"><b>{e(n)}</b><em>{e(u)}</em><span>{e(s)}</span></span></div>' for i, (n, d, u, s) in enumerate(B.SCHRIFTWAHL)))
    rang = [('Titel gross', 'Fjalla One · 96 px', 'r1', 'Mehr erleben, weniger zahlen.'), ('Titel', 'Fjalla One · 64 px', 'r2', 'Zimmer und Ferienwohnungen'),
            ('Zwischentitel', 'Fjalla One · 36 px', 'r3', 'Familienzimmer für 3 bis 6 Personen'), ('Kleiner Titel', 'Fjalla One · 22 px', 'r4', 'Rösti Tschug Tschug'),
            ('Kapitelzeile', 'DM Mono · 12 px · gesperrt', 'r5', 'Restaurant Röstihüs · Saas-Almagell'), ('Lesetext', 'Instrument Sans · 18 px · Zeilenabstand 1,62', 'r6', 'Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten, die mit Liebe, Herz und den besten regionalen Produkten zubereitet werden.'),
            ('Kleine Angabe', 'DM Mono · 12,5 px · gesperrt', 'r7', 'Tel. +41 27 957 10 12 · CH-3905 Saas-Almagell')]
    rang_html = ''.join(f'<li data-r="maske"><span class="rang__m"><b>{e(a)}</b>{e(b)}</span><span class="{c}"><span class="z"><span>{e(s)}</span></span></span></li>' for a, b, c, s in rang)
    bilder = [('fassade-winter', 'Das Haus im Winter', 'b1', '50% 50%'), ('stube-weit', 'Das Röstihüs', 'b2', '50% 50%'), ('zimmer-dach', 'Zimmer unter dem Dach', 'b3', '50% 50%'),
              ('raclettestuebli', 'Das Raclettestübli', 'b4', '60% 50%'), ('gondel', 'Die Gondel vor dem Haus', 'b5', '50% 50%'), ('fruehstueck', 'Das Frühstücksbuffet', 'b6', '50% 50%'),
              ('balkon', 'Blick vom Balkon ins Tal', 'b7', '50% 50%')]
    bilder_html = ''.join(f'<figure class="bi {c} k3" data-r="feder" style="--i:{i % 3}"><div class="k3__b"><img src="{foto(k)}" alt="{e(t)}" loading="lazy" decoding="async" style="object-position:{l}"><figcaption class="kerbe">{e(t)}</figcaption></div></figure>' for i, (k, t, c, l) in enumerate(bilder))
    nein = [('zerr', 'Nicht verzerren'), ('dreh', 'Nicht drehen'), ('farbe', 'Nicht umfärben'), ('schatten', 'Keine Schatten')]
    nein_html = ''.join(f'<figure class="nein nein--{c}"><div>{zeichen()}<i></i></div><figcaption>{e(t)}</figcaption></figure>' for c, t in nein)
    richtig_html, falsch_html = logo_karten()
    unterschiede = ''.join(f'<li style="--i:{i}"><b>{e(k)}</b><span>{e(v)}</span></li>' for i, (k, v) in enumerate(B.EIGENE_WELT['unterschied_zu'].items()))
    T = B.TON
    welt_a, welt_b = B.WELTEN['a'], B.WELTEN['b']
    def welt_block(k, w, i):
        c = w['css']
        geraet_html = geraet(k, i) if os.path.exists(os.path.join(M, 'geraet', 'schirm', f'laptop-{k}.png')) else ''
        return f'''<div class="welt {'welt--gewaehlt' if k == 'a' else 'welt--nicht'}">
        <div class="welt__k"><h3>{k.upper()} · <em>{e(w['name'])}</em></h3><div class="welt__b">{''.join(f'<i style="background:{c[x]}"></i>' for x in ('papier', 'creme', 'nacht', 'blau', 'gold', 'beton'))}</div></div>
        <p>{e(w['satz'])}</p>
        <figure class="lock lock--marine tapete welt__tafel" data-r="flug" style="--i:{i};--fx:{'-10vw' if i == 0 else '10vw'};--fy:22vh;--fw:{'-5deg' if i == 0 else '5deg'};background-color:{c['nacht']};background-image:url(zeichen/tapete-dunkel{'-b' if k == 'b' else ''}.svg);color:{c['papier']}"><div>{wort('lock__w')}<p class="lock__o" style="color:{c['gold']}">Saas-Almagell · Welt {k.upper()}</p></div><figcaption class="kerbe kerbe--c">{e(w['flaechen'][2])} · Knöpfe {e(w['knopf'])} · Akzent {e(w['akzent'])}</figcaption></figure>
        {geraet_html}
        <div class="knr">{kn(f'Probe {k.upper()} öffnen', f'probe.html?welt={k}', neu=True)}<a class="kn {"kn--linie" if k == "b" else ""}" href="?welt={k}" data-welt-knopf="{k}">Markenbuch in {k.upper()}<i>{PF}</i></a></div>
      </div>'''
    KAPITEL = [('haltung', 'Haltung'), ('zeichen', 'Zeichen'), ('farben', 'Farben'), ('welten', 'Welten'), ('herkunft', 'Herkunft'), ('schrift', 'Schrift'), ('tapete', 'Tapete'), ('bilder', 'Bilder'), ('bausteine', 'Bausteine'), ('logo', 'Logo'), ('welt', 'Eigene Welt'), ('mitnehmen', 'Mitnehmen')]
    index_html = ''.join(f'<a href="#{k}" data-r style="--i:{i}"><span>{e(n)}</span></a>' for i, (k, n) in enumerate(KAPITEL))
    nav_html = ''.join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAPITEL[:10])
    v_css = int(os.path.getmtime(os.path.join(M, 'marke.css'))); v_js = int(os.path.getmtime(os.path.join(M, 'marke.js')))
    GOLD = '<linearGradient id="tgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3CDB2"/><stop offset=".34" stop-color="#E09A70"/><stop offset=".52" stop-color="#C67144"/><stop offset=".64" stop-color="#8A4626"/><stop offset=".82" stop-color="#D98E62"/><stop offset="1" stop-color="#F1C6A8"/></linearGradient>'
    defs = B.sym_defs().replace('</defs>', GOLD + '</defs>')
    offen_satz = 'Gewählt am 18.10.2026: Farbwelt A, Fjalla One, der Grat. Offen: das Logo liegt beim Haus nur als PNG vor (die Vektoren sind Züge davon), die Schriftlizenz der Speisekarte.'
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Markenbuch · Hotel Monte-Moro</title>
<meta name="description" content="Bergkamm und Wortmarke, Farben und ihre Herkunft, Schriften, Tapete, Bilder und Bausteine für die neue Website des Hotel Monte-Moro in Saas-Almagell. Entwurf von Tasty Studios, Oktober 2026.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['Nacht']}">
<link rel="icon" href="zeichen/medaillon-blau.svg" type="image/svg+xml">
<link rel="preload" href="schriften/FjallaOne-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="schriften/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="marke.css?v={v_css}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{defs}

<nav class="leiste" aria-label="Markenbuch">
  <a class="leiste__m" href="#oben">{zeichen()}<span><b>Markenbuch</b><small>Station 05 · Hotel Monte-Moro</small></span></a>
  <div class="leiste__k">{nav_html}</div>
  <a class="glanz" href="probe.html" target="_blank" rel="noopener">Die Probe{PF}</a>
</nav>

<main>
<section class="titel tapete" id="oben">
  <div class="titel__in">
    <p class="titel__kap" data-r="hero" style="--i:0"><i></i><b>Markenbuch · Oktober 2026</b><i></i></p>
    <div class="titel__z" data-r="zeichen">{medaillon('', 'url(#tgold)').replace('<svg ', '<svg style="width:clamp(84px,9vw,132px);height:auto" ')}</div>
    <h1 class="titel__w" data-r="maske"><span class="z"><span>{wort().replace('fill="currentColor"', 'fill="#F5F2EE"')}</span></span></h1>
    <p class="titel__ort" data-r="hero" style="--i:2"><span style="white-space:nowrap">Saas-Almagell</span> <span class="raute"></span> Saastal <span class="raute"></span> Wallis</p>
    <p class="titel__lead" data-r="hero" style="--i:3">Alles, was Ihr Haus erkennbar macht, an einem Ort: der Bergkamm und die Wortmarke, die Farben und woher sie kommen, die Schriften, das Medaillon als Tapete, die Bilder und die Bausteine der neuen Website. Damit jedes neue Stück, ob Karte, Seite oder Schild, aussieht wie aus einem Guss.</p>
    <div class="knr knr--mitte" data-r="hero" style="--i:4">{kn('Lesen', '#haltung')}{kn('Die Probe', 'probe.html', 'kn--linie', neu=True)}</div>
  </div>
  <nav class="index" aria-label="Inhalt" data-g>{index_html}</nav>
  <span class="titel__runter" aria-hidden="true"><i></i></span>
</section>

<section class="ab blatt papier" id="haltung">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--papier)"/></svg>
  <div class="in">
    {kopf('Haltung', ['Mehr erleben,', 'weniger zahlen.'], 'Der Satz steht heute ganz oben auf Ihrer Startseite, und er beschreibt das Haus: drei Sterne, 18 Zimmer, Bergbahnen und Postautos inbegriffen, das Spa nebenan offen, im Röstihüs elf Röstis mit Namen. Die Gestaltung ist hell, direkt und herzlich, so wie das Haus mit seinen Gästen redet.')}
    <div class="drei" data-g>
      {kachel('fassade-sommer', 'Hell wie die Fassade.', 'Licht', 'Papier und Fassade tragen den Lesetext. Dunkel wird die Seite am Abend, im Blau des Logos.', 0, '50% 35%')}
      {kachel('roestihues', 'Das Haus mit Gesicht.', 'Röstihüs', 'Kartoffelsäcke mit Gesichtern, Röstis mit Namen, Weine von Fabian: die Seite zeigt, was es nur hier gibt.', 1, '50% 35%')}
      {kachel('zimmer', 'Ehrlich gerechnet.', 'Ton', '«Mehr erleben, weniger zahlen.» Was inbegriffen ist, steht vorn und als Liste, ohne grosse Worte.', 2)}
    </div>
  </div>
</section>

<section class="fenster" aria-label="Blick vom Balkon ins Tal">
  <div class="fenster__f">
    <div class="fenster__b"><img src="{foto('balkon')}" alt="Blick vom Balkon des Hotel Monte-Moro ins Tal, Sonne über den Bergen" decoding="async"></div>
    <div class="fenster__t"><p class="fenster__s"><span class="z"><span>Bei uns scheint</span></span><span class="z"><span><em>fast immer die Sonne.</em></span></span></p><p class="fenster__u">Hotel Monte-Moro, auf der Seite des Röstihüs.</p></div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="zeichen">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--creme)"/></svg>
  <div class="in">
    {kopf('Zeichen und Name', ['Zwei Gipfel', 'und Ihr Name.'], 'Ihr Logo ist eine Datei von Ihrer heutigen Seite (logo.png, 1161 × 475 Pixel): zwei Gipfel als «MM», darunter «Monte Moro» und «Saas-Almagell». Eine Vektor-Fassung hat das Haus nicht; für Farben und grosse Drucke liegt ein genauer Zug der Datei bei, der die Form nicht verändert. Aus den Gipfeln kommen das Medaillon und der Grat.')}
    <div class="lockups" data-g>
      <figure class="lock lock--marine tapete" data-r="flug" style="--i:0;--fx:-14vw;--fy:22vh;--fw:-6deg"><div>{wort('lock__w')}<p class="lock__o">Saas-Almagell · Saastal</p></div><figcaption class="kerbe kerbe--c">Hauptform auf Nacht</figcaption></figure>
      <figure class="lock lock--papier" data-r="flug" style="--i:1;--fx:14vw;--fy:22vh;--fw:6deg"><div><img src="logo/logo-original-1161px.png" alt="Logo Monte Moro, Saas-Almagell" style="width:min(420px,70%);height:auto;margin:0 auto"></div><figcaption class="kerbe kerbe--c">Das Original auf Papier</figcaption></figure>
      <figure class="lock lock--quer" data-r="flug" style="--i:2;--fx:-12vw;--fy:30vh;--fw:5deg"><div>{zeichen('lock__z')}<span class="lock__strich"></span><span class="lock__w">Hotel Monte-Moro</span></div><figcaption class="kerbe kerbe--c">Querform für Leisten und Briefköpfe</figcaption></figure>
      <figure class="lock lock--groessen tapete" data-r="flug" style="--i:3;--fx:12vw;--fy:30vh;--fw:-5deg"><div>{medaillon('g1')}{medaillon('g2')}{medaillon('g3')}{medaillon('g4')}</div><figcaption class="kerbe kerbe--c">Das Medaillon: Siegel, Stempel, Zeichen im Browser</figcaption></figure>
    </div>
    <div class="reihe5" data-g>
      <div class="zei" data-r="feder" style="--i:0">{zeichen('', 'Der Bergkamm')}<b>Der Bergkamm</b><small>aus logo.png · die zwei Gipfel als «MM»</small></div>
      <div class="zei" data-r="feder" style="--i:1">{medaillon()}<b>Das Medaillon</b><small>Bergkamm im Kreis · für die Tapete</small></div>
      <div class="zei" data-r="feder" style="--i:2">{B.grat_svg('currentColor').replace('class="grat"', 'style="height:clamp(30px,3vw,46px);width:100%;color:var(--blau)"')}<b>Der Grat</b><small>nach dem Kamm gezogen · jede Naht zwischen Flächen</small></div>
      <div class="zei" data-r="feder" style="--i:3"><img src="{foto('reception')}" alt="Der Bergkamm an der Wand neben der Rezeption" style="height:clamp(54px,5.4vw,78px);width:auto;border-radius:10px"><b>An der Wand</b><small>Rezeption · TripAdvisor, vom Haus, 2017</small></div>
    </div>
    <div class="regeln" data-g>
      <div class="regel" data-r="feder" style="--i:0">
        <div class="regel__f"><svg class="schutz" viewBox="-700 -700 4883 2096" aria-hidden="true">
          <rect x="-560" y="-560" width="4603" height="1816" rx="40" fill="none" stroke="currentColor" stroke-width="18" stroke-dasharray="70 52"/>
          <g fill="currentColor"><use href="#bergkamm" width="3483" height="696"/></g>
        </svg></div>
        <h3>Schutzraum</h3><p>Rund um den Bergkamm bleibt so viel Luft, wie er hoch ist. Kein Text, kein Bildrand, keine Linie ragt hinein.</p>
      </div>
      <div class="regel" data-r="feder" style="--i:1">
        <div class="regel__f klein"><span>{zeichen()}<small>48 px</small></span><span>{zeichen()}<small>72 px</small></span><span>{zeichen()}<small>15 mm</small></span></div>
        <h3>Kleinste Grösse</h3><p>Der Bergkamm allein am Bildschirm nicht unter 48 Pixel breit, im Druck nicht unter 15 Millimeter. Die ganze Wortmarke mindestens 150 Pixel oder 40 Millimeter breit.</p>
      </div>
      <div class="regel regel--breit" data-r="feder" style="--i:2">
        <div class="regel__f neine">{nein_html}</div>
        <h3>Was das Zeichen nicht darf</h3><p>Es steht gerade, in Logo-Blau, Nacht, Papier, Lärche oder Butzenglas, ohne Schatten und ohne Rahmen. Auf Fotos nur dort, wo die Fläche ruhig ist.</p>
      </div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="farben">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--papier)"/></svg>
  <div class="in">
    {kopf('Farben', ['Achtzehn Töne,', 'jeder mit Fundstelle.'], 'Hell ist der Normalzustand: Papier und Fassade tragen den Lesetext. Das Blau kommt aus dem Logo, als Nacht für dunkle Flächen und als Logo-Blau für Knöpfe. Die Lärche der Balkone zeichnet und betont. Butzenglas und Jute sind die zweite Welt. Was nur auf der heutigen Seite steht, ist gemessen und bleibt draussen. Ein Klick auf eine Farbe kopiert ihren Wert.')}
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
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--creme)"/></svg>
  <div class="in">
    {kopf('Farbwelt', ['Gewählt:', 'Bergnacht und Lärche.'], 'Robert hat am 18.10.2026 Welt A gewählt: «Farbe A». Welt B bleibt hier zum Nachlesen. Beide Welten teilen Papier, Fassade und den Bergkamm. Sie unterscheiden sich dort, wo die Seite dunkel wird und womit Titel betont werden. Welt A zieht das Blau des Logos zur Nacht und betont mit der Lärche der Balkone, Welt B setzt das Logo-Blau selbst als Fläche und betont mit dem Licht der Butzenscheiben. Die Probe läuft in beiden Welten als eigene Seite, zum Scrollen.')}
    <div class="welten" data-g>
      {welt_block('a', welt_a, 0)}
      {welt_block('b', welt_b, 1)}
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="herkunft">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--marine)"/></svg>
  <div class="in">
    {kopf('Herkunft', ['Woher die Farben', 'kommen.'], 'Die Farben kommen aus Ihrem Haus: aus der Logo-Datei, aus der Fassade, vom Schild vor dem Röstihüs und aus dem Raclettestübli. Unter jedem Foto steht der Streifen, der beim Bau dieser Seite aus dem Bild gemessen wurde, darunter die Töne, die daraus geworden sind.')}
    <div class="hers" data-g>{herkunft_html}</div>
  </div>
</section>

<section class="ab blatt papier" id="schrift">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--papier)"/></svg>
  <div class="in">
    {kopf('Schrift', ['Aus der Wortmarke', 'abgeleitet.'], '«Monte Moro» steht in Ihrem Logo in einer schmalen, kräftigen Groteske. Die Titelschrift nimmt diese Haltung auf: Fjalla One, gross und klein geschrieben wie die Wortmarke. Instrument Sans hält lange Texte lesbar, DM Mono steht bei Zeiten, Preisen und Adressen. Alle sind frei lizenziert und liegen als Dateien bei der Website, nichts wird von fremden Servern geladen.')}
    <div class="schs">{schrift_html}</div>
    <div class="rang">
      <div class="rang__k" data-r><p class="mk__kap"><b>Neben der Wortmarke</b><i></i></p><h3>Vier freie Schriften, eine passt.</h3><p>Vor der Wahl wurden acht freie Schriften neben «Monte Moro» gelegt; hier die vier, die am nächsten kamen, und die Schrift, die die Potentialanalyse bisher trug.</p></div>
      <div class="wahl" data-g>{wahl_html}</div>
    </div>
    <div class="rang">
      <div class="rang__k" data-r><p class="mk__kap"><b>Rangordnung</b><i></i></p><h3>Sieben Stufen, mehr braucht die Seite nicht.</h3><p>Grössen der neuen Website auf einem Rechner mit 1440 Pixel Breite. Auf dem Handy werden die Titel kleiner, der Lesetext bleibt.</p></div>
      <ul class="rang__l">{rang_html}</ul>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="tapete">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--creme)"/></svg>
  <div class="in">
    {kopf('Tapete', ['Das Medaillon', 'als Tapete.'], 'Das Muster ist der Bergkamm im Kreis, gesetzt in ein Rautengitter, dessen Kanten fein gezackt sind wie die Linie der Gipfel. Zart und Ton in Ton liegt es auf der neuen Seite, in den Karten und auf den Drucksachen, immer im Wechsel: ein Abschnitt mit Tapete, der nächste ohne.')}
    <div class="tap" data-g>
      <figure class="tap__f tap__f--dunkel" data-r="feder" style="--i:0"><span class="streif"></span><figcaption class="kerbe kerbe--c">Auf Nacht</figcaption></figure>
      <figure class="tap__f tap__f--hell" data-r="feder" style="--i:1"><span class="streif"></span><figcaption class="kerbe kerbe--c">Auf Papier und Fassade</figcaption></figure>
    </div>
    <div class="prunk" data-r="prunk">
      <div class="prunk__z" style="--i:0"><b><span data-zahl="480">0</span></b><i></i><small>Pixel Rapport am Bildschirm</small></div>
      <div class="prunk__z" style="--i:1"><b><span data-zahl="12">0</span></b><i></i><small>Prozent Deckkraft auf Hell, 10 auf Nacht</small></div>
      <div class="prunk__z" style="--i:2"><b><span>1 : 1</span></b><i></i><small>im Wechsel mit glatten Flächen</small></div>
    </div>
  </div>
</section>

<section class="ab blatt papier" id="bilder">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--papier)"/></svg>
  <div class="in">
    {kopf('Bilder', ['Ihr Haus,', 'in echtem Licht.'], 'Gezeigt wird, was der Gast vorfindet: das Haus im Schnee, die Stube, die Zimmer unter dem Dach, das Raclettestübli, die Gondel vor der Tür, das Frühstück, der Blick vom Balkon. Die Fotos stammen von Ihrer Seite, von Schweiz Tourismus, Booking.com und TripAdvisor, jeweils vom Haus selbst; überarbeitet werden nur Schärfe und Licht, nie der Inhalt.')}
    <div class="collage" data-g>{bilder_html}</div>
    <div class="satz3" data-g>
      <div data-r style="--i:0"><h3>Fotos aus dem Haus.</h3><p>Jedes Bild zeigt das Monte-Moro oder das Röstihüs. Bilder der Region nur mit bekannter Herkunft; erzeugte Bilder nur auf Roberts Wort.</p></div>
      <div data-r style="--i:1"><h3>Warm bleibt warm.</h3><p>Viele Zimmerfotos sind gelb und orange. Licht und Weiss werden ausgeglichen, das Holz bleibt Holz. Ein Farbpunkt je Bild, nie eine Fläche.</p></div>
      <div data-r style="--i:2"><h3>Der Name im Bild.</h3><p>Unten links, in Fjalla One, auf einem weichen Schatten im Foto. So steht jeder Name an derselben Stelle, ohne ausgeschnittene Ecke.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt marine tapete" id="bausteine">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--marine)"/></svg>
  <div class="in">
    {kopf('Bausteine', ['Knöpfe, Grat', 'und Bildzeile.'], 'Die kleinen Teile, die überall wiederkehren. Jeder Knopf hat Tiefe und einen runden Knauf mit Pfeil und gibt nach, wenn man ihn drückt. Die Naht zwischen hellen und dunklen Flächen ist ein Grat, gezogen nach den Gipfeln des Logos. Probieren Sie es gern aus.')}
    <div class="baus" data-g>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f knr knr--mitte">{kn('Zimmer buchen', '#bausteine')}{kn('Zur Karte', '#bausteine', 'kn--linie')}</div><h3>Knöpfe</h3><p>Fassade auf Nacht, Logo-Blau auf Papier. Schrift in DM Mono, gesperrt, in Versalien. Der Knopf sagt, was passiert.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f"><div class="gratnaht">{B.grat_svg('var(--marine)')}</div></div><h3>Der Grat</h3><p>Wo eine helle Fläche in eine dunkle übergeht, endet sie nicht gerade, sondern als Kamm, nach den Gipfeln des Logos gezogen. An jeder Naht zwischen zwei Flächen, so wie in diesem Markenbuch; nie an Kacheln oder Bildern.</p></div>
      <div class="bau" data-r="feder" style="--i:0"><div class="bau__f"><figure class="kerbbild"><img src="{foto('haus-winter-tag')}" alt="" loading="lazy" decoding="async"><figcaption class="kerbe kerbe--d">Nach frischem Schnee</figcaption></figure></div><h3>Die Bildzeile</h3><p>Der Name eines Bildes steht unten links im Foto, auf einem weichen Schatten. Keine ausgeschnittenen Ecken.</p></div>
      <div class="bau" data-r="feder" style="--i:1"><div class="bau__f bau__f--titel" data-r="maske"><p class="mk__kap"><b>Restaurant Röstihüs</b><i></i></p><p class="bau__t"><span class="z"><span>Es lebe</span></span><span class="z"><span><em>die Tradition!</em></span></span></p></div><h3>Kapitelzeile und Titel</h3><p>Über jedem Titel eine Zeile in gesperrten Versalien mit wachsender Linie. Der Titel steigt Zeile für Zeile aus dem Schlitz, der zweite Teil in Lärche.</p></div>
    </div>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="logo">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--creme)"/></svg>
  <div class="in">
    {kopf('Logo richtig und falsch', ['Eingesetzt,', 'nie verändert.'], 'Die Wortmarke und der Bergkamm sind Dateien aus Ihrem Haus. Sie werden eingesetzt, nie nachgezeichnet, nie verändert. Acht Dinge, die gehen, und acht, die nicht gehen.')}
    <p class="mk__kap" data-r><b>Richtig</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px;margin-bottom:clamp(40px,4vw,64px)">{richtig_html}</div>
    <p class="mk__kap" data-r><b>Falsch</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px">{falsch_html}</div>
  </div>
</section>

<section class="ab blatt papier" id="welt">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--papier)"/></svg>
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
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--marine)"/></svg>
  <div class="in">
    {kopf('Projekt Nummer 10', ['Womit es sich von jedem', 'bisherigen Haus unterscheidet.'], 'Jedes Haus bekommt eine eigene Welt, kein Haus bekommt das System. Vor dieser Station wurden die Konzepte und Bausteine der bisherigen Häuser und die Analysen der Familie Zurbriggen gelesen; hier steht je Haus, was das Monte-Moro anders macht.')}
    <ul class="unter" data-g>{unterschiede}</ul>
  </div>
</section>

<section class="ab blatt marine tapete schluss" id="mitnehmen">
  <svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="var(--marine)"/></svg>
  <div class="in">
    {kopf('Zum Mitnehmen', ['Alles für das', 'nächste Stück.'], 'Die Wortmarke als Original und als Vektor, der Bergkamm, das Medaillon, die Farben als fertige Datei und die Schriften. Wer eine neue Karte, ein Schild oder eine Seite gestaltet, findet hier alles dafür.')}
    <ul class="laden" data-g>
      <li data-r style="--i:0"><span><b>Wortmarke</b><small>Original des Hauses, PNG 1161 px</small></span>{kn('Laden', 'logo/logo-original-1161px.png', laden=True)}</li>
      <li data-r style="--i:1"><span><b>Wortmarke als Vektor</b><small>Zug der PNG, SVG, in jeder Grösse scharf</small></span>{kn('Laden', 'zeichen/wortmarke-blau.svg', laden=True)}</li>
      <li data-r style="--i:2"><span><b>Der Bergkamm</b><small>SVG</small></span>{kn('Laden', 'zeichen/bergkamm-blau.svg', laden=True)}</li>
      <li data-r style="--i:3"><span><b>Das Medaillon</b><small>Tapete und Siegel, SVG</small></span>{kn('Laden', 'zeichen/medaillon-blau.svg', laden=True)}</li>
      <li data-r style="--i:4"><span><b>Farben</b><small>alle Töne mit Fundstelle als CSS-Datei</small></span>{kn('Laden', 'farben.css', laden=True)}</li>
      <li data-r style="--i:5"><span><b>Fjalla One</b><small>Regular 400, WOFF2, Lizenz OFL</small></span>{kn('Laden', 'schriften/FjallaOne-400.woff2', laden=True)}</li>
      <li data-r style="--i:6"><span><b>Instrument Sans</b><small>400 bis 600, WOFF2</small></span>{kn('Laden', 'schriften/InstrumentSans-normal-400_600.woff2', laden=True)}</li>
      <li data-r style="--i:7"><span><b>DM Mono</b><small>Regular 400, WOFF2</small></span>{kn('Laden', 'schriften/DMMono-normal-400.woff2', laden=True)}</li>
    </ul>
    <div class="ende" data-r="ende">
      <span class="strich strich--gross">{zeichen()}</span>
      <p class="ende__w">{wort()}</p>
      <p class="ende__s">Markenbuch Hotel Monte-Moro · Station 05 der Kette · Entwurf von Tasty Studios, Oktober 2026. {offen_satz}</p>
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
    richtig_html, falsch_html = logo_karten('../')
    v_css = int(os.path.getmtime(os.path.join(M, 'marke.css'))); v_js = int(os.path.getmtime(os.path.join(M, 'marke.js')))
    s = f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Logo richtig und falsch · Hotel Monte-Moro</title><meta name="robots" content="noindex, nofollow">
<link rel="icon" href="../zeichen/medaillon-blau.svg" type="image/svg+xml">
<link rel="stylesheet" href="../marke.css?v={v_css}"><script>document.documentElement.classList.add('js')</script></head>
<body>{B.sym_defs()}
<nav class="leiste" aria-label="Markenbuch"><a class="leiste__m" href="../markenbuch.html">{zeichen()}<span><b>Markenbuch</b><small>Logo richtig und falsch</small></span></a><div class="leiste__k"></div><a class="glanz" href="../markenbuch.html#logo">Zum Markenbuch{PF}</a></nav>
<main>
<section class="ab creme tapete-h" id="logo" style="padding-top:clamp(60px,7vw,110px)">
  <div class="in">
    {kopf('Logo richtig und falsch', ['Eingesetzt,', 'nie verändert.'], 'Die Wortmarke ist eine Datei aus Ihrem Haus (logo.png, 1161 × 475 Pixel). Sie wird eingesetzt, nie nachgezeichnet, nie verändert; die Vektor-Fassung ist ein genauer Zug dieser Datei.')}
    <p class="mk__kap" data-r><b>Richtig</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px;margin-bottom:clamp(40px,4vw,64px)">{richtig_html}</div>
    <p class="mk__kap" data-r><b>Falsch</b><i></i></p>
    <div class="regeln regeln--4" data-g style="margin-top:18px">{falsch_html}</div>
  </div>
</section>
</main>
<script src="../marke.js?v={v_js}" defer></script></body></html>'''
    s = s.replace('url(zeichen/', 'url(../zeichen/')
    os.makedirs(os.path.join(M, 'logo-richtig-falsch'), exist_ok=True)
    open(os.path.join(M, 'logo-richtig-falsch', 'index.html'), 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    css()
    open(os.path.join(M, 'markenbuch.html'), 'w', encoding='utf-8').write(seite())
    logo_seite()
    print('gebaut: markenbuch.html, marke.css, marke.js, logo-richtig-falsch/')
