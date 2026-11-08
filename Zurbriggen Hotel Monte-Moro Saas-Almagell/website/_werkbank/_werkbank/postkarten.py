#!/usr/bin/env python3
"""Hotel Monte-Moro: zwölf Postkarten (Werkbank Papier, 08.11.2026; Bauart wie postkarten.py der Vorlage).
Nur das Haus von aussen und die Landschaft des Saastals, keine Innenräume, keine Nachtbilder (Master 8, Ansichtskarten); der Titel nennt den Ort
wie auf einer echten Postkarte («Gruss aus Saas-Almagell», «Saastal», «Mattmark»). Fotos nur aus der Website (website/inhalt/bilder.py, die
Bildunterschrift dort ist die Zeile unter dem Titel).
Vorn A6 quer (die Fotos des Tals sind Panoramen): das Foto randlos, unten ein Band in Papier mit der Gratlinie als Oberkante, darin der Ort.
Hinten A6 quer auf Papier: links Bergkamm, Ort und Bildzeile, unten die Wortmarke; rechts Platz zum Schreiben, Adresslinien und ein Markenfeld.
Druck-PDF mit 3 mm Beschnitt, Sammelbogen SRA3 hoch, Fächer und Kartenständer an der Rezeption als Bild (postkarten_druck.js).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py _werkbank/postkarten.py "<website/_werkbank>"   → satz/postkarten*.html, postkarten_plan.json
   node _werkbank/postkarten_druck.js "<…>"   dann   … mit_papier.py _werkbank/postkarten.py "<…>" --seite"""
import json, os, shutil, sys
from PIL import Image
import papier_kern as P
from papier_kern import blatt, e, t, hw, hz
import kern as K
from kern import H, ROOT, W, kn, titel, kap, zahl
import papier_neu as N
from papier_neu import NACHT, BLAU, LAERCHE, LAERCHE_T, MESSING, PAPIER, WAND, TINTE, GRAU

sys.path.insert(0, os.path.join(N.WEB, 'inhalt'))
from bilder import BILDER  # noqa: E402  (website/inhalt/bilder.py, nur gelesen)

B = 3   # Beschnitt
KB, KH = 148, 105
# Schlüssel, Ort im Titel, Lage des Ausschnitts; die Zeile darunter ist die Bildunterschrift aus bilder.py
FOTOS = [('haus-sommer-g', 'Gruss aus Saas-Almagell', '50% 45%'), ('stausee', 'Mattmark', '50% 55%'), ('alpenrosen', 'Saastal', '60% 50%'),
         ('haus-winter-g', 'Saas-Almagell', '50% 45%'), ('tal-sommer', 'Das Saastal', '50% 50%'), ('gletscher', 'Saastal', '50% 45%'),
         ('see-blumen', 'Mattmark', '50% 60%'), ('dorf-winter', 'Saas-Almagell', '50% 55%'), ('wasserfall', 'Saastal', '55% 50%'),
         ('huette', 'Gruss aus dem Saastal', '40% 50%'), ('murmeltiere', 'Saastal', '45% 50%'), ('dorf-weiss', 'Saas-Almagell', '50% 55%')]


def karten():
    return [dict(id=f'pk{i + 1:02d}', key=k, name=ort, satz=BILDER[k][1], lage=lage) for i, (k, ort, lage) in enumerate(FOTOS)]


def et(text, gr, farbe, sp=.18):
    return f'<span style="font-family:\'DM Mono\';font-size:{gr}mm;letter-spacing:{sp}em;text-transform:uppercase;color:{farbe};line-height:1.4">{e(text)}</span>'


def band(b, y, h, farbe):
    """Fläche unter der Gratlinie (unten bis zum Rand)"""
    pk = N.grat_punkte(0, y, b, h)
    d = 'M' + ' L'.join(f'{x:.2f} {yy:.2f}' for x, yy in pk) + f' L{b} 400 L0 400Z'
    return f'<svg class="abs" style="left:0;top:0;width:{b}mm;height:400mm;overflow:visible" viewBox="0 0 {b} 400"><path d="{d}" fill="{farbe}"/></svg>'


def vorn(k, rand=0):
    """A6 quer, 148 × 105; rand = Beschnitt ringsum (Druck)."""
    b, h = KB + 2 * rand, KH + 2 * rand
    inn = (f'<img class="abs" src="{e(N.bild_satz(k["key"], "l"))}" style="left:0;top:0;width:{b}mm;height:{h - 12}mm;object-fit:cover;object-position:{k["lage"]}" alt="">'
           + band(b, rand + 78, 6, PAPIER)
           + f'<div class="abs" style="left:{rand + 8}mm;top:{rand + 87}mm;width:{KB - 16}mm;display:flex;justify-content:space-between;align-items:center">'
           f'<span style="font-family:\'Fjalla One\';font-size:6.4mm;line-height:1;color:{NACHT}">{e(k["name"])}</span>'
           f'<span style="display:block;width:22mm;color:{BLAU}">{hw(0, 0, 22, BLAU, False).replace("class=\"abs\" style=\"left:0mm;top:0mm;", "style=\"display:block;")}</span></div>')
    return blatt(b, h, inn, '', f'background:{PAPIER}')


def hinten(k, rand=0):
    """A6 quer, 148 × 105: links Ort und Bildzeile, rechts Adresse und Markenfeld."""
    b, h = KB + 2 * rand, KH + 2 * rand
    r = rand
    links = (f'<div class="abs" style="left:{r + 10}mm;top:{r + 12}mm;width:54mm;bottom:{r + 12}mm;display:flex;flex-direction:column;justify-content:space-between">'
             f'<div><div style="width:16mm;color:{LAERCHE}">{hz(0, 0, 16, LAERCHE, False).replace("class=\"abs\" style=\"left:0mm;top:0mm;", "style=\"display:block;")}</div><div style="height:4mm"></div>'
             f'{et("Hotel Monte-Moro", 1.7, LAERCHE_T, .18)}<div style="height:2.6mm"></div>'
             f'<div style="font-family:\'Fjalla One\';font-size:6.6mm;line-height:1.1;color:{NACHT}">{e(k["name"]).replace("Saas-Almagell", "<span style='white-space:nowrap'>Saas-Almagell</span>")}</div><div style="height:2.6mm"></div>'
             f'<i style="display:block;width:8mm;height:.35mm;background:{MESSING}"></i><div style="height:2.6mm"></div>'
             f'<div style="font-family:\'Instrument Sans\';font-size:3mm;line-height:1.45;color:{GRAU}">{e(k["satz"])}.</div></div>'
             f'<div>{et(N.PLZ_ORT, 1.45, GRAU, .1)}<div style="height:.8mm"></div>{et("Tel. " + N.TEL, 1.45, GRAU, .1)}</div></div>')
    trenn = f'<i class="abs" style="left:{r + 72}mm;top:{r + 12}mm;width:.25mm;height:81mm;background:{MESSING}"></i>'
    marke = (f'<div class="abs" style="left:{r + KB - 30}mm;top:{r + 10}mm;width:20mm;height:24mm;border:.3mm dashed rgba(19,38,58,.4);border-radius:.8mm"></div>'
             + hz(r + KB - 20, r + 19.5, 12, LAERCHE))
    linien = ''.join(f'<i class="abs" style="left:{r + 80}mm;top:{r + 50 + n * 11}mm;width:58mm;height:.25mm;background:rgba(19,38,58,.34)"></i>' for n in range(4))
    return blatt(b, h, f'<i class="abs" style="inset:0;background:{PAPIER}"></i>' + links + trenn + marke + linien, '', f'background:{PAPIER}')


def setzen():
    KK = karten()
    os.makedirs(os.path.join(P.SATZ, 'bild'), exist_ok=True)
    Image.open(N.bild('empfang', 'l')).convert('RGB').save(os.path.join(P.SATZ, 'bild', 'hintergrund.webp'), 'WEBP', quality=80)   # Hintergrund für den Kartenständer
    alt = os.path.join(P.SATZ, 'bild', 'barnacht.webp')
    if os.path.exists(alt):
        os.remove(alt)
    vor = [vorn(k) for k in KK]; hin = [hinten(k) for k in KK]
    P.seite('postkarten', [x for p in zip(vor, hin) for x in p], 'Postkarten')
    P.seite('postkarten-druck', [x for k in KK for x in (vorn(k, B), hinten(k, B))], 'Postkarten, Druck mit Beschnitt')
    BW, BH, LUFT = 320, 450, 3   # SRA3 hoch, zwei Spalten, vier Reihen
    boegen = []
    for s0 in range(0, len(KK), 8):
        teil = KK[s0:s0 + 8]; inn = ''
        x0, y0 = (BW - (2 * KB + LUFT)) / 2, (BH - (4 * KH + 3 * LUFT)) / 2 + 4
        for n, k in enumerate(teil):
            x, y = x0 + (n % 2) * (KB + LUFT), y0 + (n // 2) * (KH + LUFT)
            inn += f'<div class="abs" style="left:{x}mm;top:{y}mm;width:{KB}mm;height:{KH}mm;overflow:hidden">{vorn(k).replace('style="width:', 'style="margin:0;width:', 1)}</div>'
            inn += f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{KB}mm;height:{KH}mm;outline:.15mm solid #e6007e"></i>'
        inn += t(10, 4, f'{e(N.NAME)} · Postkarten · Sammelbogen {s0 // 8 + 1} von {(len(KK) + 7) // 8} · SRA3 hoch · Originalgrösse · Schnittlinie in Magenta', 'm', f'font-size:2.1mm;color:{TINTE}')
        boegen.append(blatt(BW, BH, inn, '', 'background:#fff'))
    P.seite('postkarten-bogen', boegen, 'Postkarten, Sammelbogen')
    json.dump({'karten': [{k2: k[k2] for k2 in ('id', 'key', 'name', 'satz')} for k in KK], 'boegen': len(boegen), 'quer': True},
              open(os.path.join(W, 'postkarten_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Postkarten gesetzt:', len(KK), 'Karten,', len(boegen), 'Sammelbögen')


def seite():
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'postkarten_plan.json')))
    KK = plan['karten']
    roh, ziel = os.path.join(W, 'roh', 'postkarten'), os.path.join(ROOT, 'postkarten', 'img')
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    os.makedirs(ziel)
    M = {}
    for f in os.listdir(roh):
        if not f.endswith('.png'): continue
        im = Image.open(os.path.join(roh, f)).convert('RGBA')
        if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(os.path.join(ziel, f[:-4] + '.webp'), 'WEBP', quality=88, method=5); M[f[:-4]] = im.size
    img = lambda n, alt='': f'<img src="img/{n}.webp" width="{M[n][0]}" height="{M[n][1]}" alt="{e(alt)}" decoding="async">'
    liste = ''.join(f'<li data-a="kipp" style="--i:{n % 4}"><span class="b pk-paar">{img(k["id"] + "-v", k["name"])}{img(k["id"] + "-h", "Rückseite")}</span><h3>{e(k["name"])}</h3><p>{e(k["satz"])}</p><small>A6 quer · vorn und hinten</small></li>' for n, k in enumerate(KK))
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(KK)), 'Postkarten', 'aus dem Saastal.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Das Haus im Sommer und im Winter, der Stausee Mattmark, Alpenrosen, Gletscher, Murmeltiere und das Dorf im Schnee, alles Fotos Ihrer Website. Vorne der Ort wie auf einer echten Postkarte, hinten Platz zum Schreiben und ein Markenfeld mit dem Bergkamm. Zum Auslegen an der Rezeption und zum Mitnehmen.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Druck-PDF', f'pdf/{H.KURZ}-postkarten-druck.pdf', 'kn--linie', neu=True)}</div>
    </div>
    <div class="auslage" aria-hidden="true"><div data-a="schweb" style="left:0;top:0;width:100%;--r:0deg;--r0:0deg;--i:2">{img("faecher", "")}</div></div>
  </div>
</section>
<section class="fl fl--nacht blatt stueck" id="staender">
  <div class="in">
    <div class="stueck__t">{kap(1, 'An der Rezeption')}{titel(['Im Ständer', 'beim Empfang.'])}<div class="lauf"><p data-a="worte">So könnten die Karten an der Rezeption stehen, unter dem Bergkamm an der Wand: für einen Gruss nach Hause, solange man noch im Tal ist.</p></div></div>
    <div class="karton"><figure class="sch" data-a="schweb" style="width:96%">{img("staender", "Kartenständer an der Rezeption")}</figure></div>
  </div>
</section>
<section class="fl fl--papier blatt" id="karten">
  <div class="in">
    <div class="kopfzeile"><div>{kap(2, 'Die Karten')}{titel([zahl(len(KK)), 'Postkarten.'])}</div><div class="lauf"><p data-a="worte">Nur das Haus von aussen und die Landschaft, keine Innenräume und keine Nacht. Jedes Foto randlos bis zum Band mit der Gratlinie.</p></div></div>
    <ul class="etk">{liste}</ul>
  </div>
</section>
<section class="fl fl--creme blatt stueck" id="druck">
  <div class="in">
    <div class="stueck__t">{kap(3, 'Für die Druckerei')}{titel(['Der', 'Sammelbogen.'])}
      <div class="lauf"><p data-a="worte">Alle Karten mit 3 mm Beschnitt als ein PDF, dazu {zahl(plan["boegen"]).lower()} Sammelbögen SRA3 mit Schnittlinien.</p></div>
      <div class="kn-reihe" data-a="auf">{kn('Druck-PDF', f'pdf/{H.KURZ}-postkarten-druck.pdf', neu=True)}{kn('Sammelbogen SRA3', f'pdf/{H.KURZ}-postkarten-sammelbogen-a3.pdf', 'kn--linie', neu=True)}</div></div>
    <div class="bogenblick" data-a="gross">{img("bogen", "Sammelbogen SRA3")}</div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Sticker und Beigaben im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}{kn('Beigaben', '../beigaben/index.html', 'kn--linie')}</div></div></section>'''
    css = '<style>.etk .b.pk-paar{display:flex!important;flex-direction:row!important;gap:4%;align-items:center;justify-content:center;height:auto!important;aspect-ratio:auto!important}.etk .b.pk-paar img{position:static!important;width:48%!important;height:auto!important;max-height:none!important}</style>'
    K.schreib(os.path.join(ROOT, 'postkarten', 'index.html'), K.rahmen('Postkarten', f'{zahl(len(KK))} Postkarten des Hotels Monte-Moro.', 'Postkarten', css + haupt))
    Image.open(os.path.join(ziel, 'faecher.webp')).save(os.path.join(ziel, 'vorschau.webp'), 'WEBP', quality=86)
    print('Seite gebaut: postkarten/ ·', len(KK), 'Karten')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
