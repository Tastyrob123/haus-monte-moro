#!/usr/bin/env python3
"""Hotel Monte-Moro: fünf Beigaben als Druckvorlage (Werkbank Papier, 08.11.2026; Bauart wie beigaben.py der Vorlage).
Der Bon der Rezeption zum Mitnehmen (die Idee der Website: alles Inklusive als Bon), ein Türhänger, ein Kofferanhänger wie die Etiketten der
alten Hotels, das Kärtchen auf dem Kissen und Servietten fürs Röstihüs. Kleid und Texte wie die Drucksachen (papier_neu.py), Seite beigaben/.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py _werkbank/beigaben.py "<website/_werkbank>"   →  satz/beigabe-*.html, beigaben_plan.json
   node _werkbank/sticker_druck.js "<…>" beigaben, dann  … mit_papier.py _werkbank/beigaben.py "<…>" --seite"""
import json, os, re, sys
import papier_kern as P
from papier_kern import t, lin, linv, rahmen, kasten, blatt, hw, hz, e
import kern as K
from kern import H, ROOT, W, kn, titel, kap, zahl
import papier_neu as N
from papier_neu import NACHT, BLAU, LAERCHE, LAERCHE_T, MESSING, PAPIER, CREME, WAND, TINTE, GRAU


def etk(x, y, text, farbe, gr=1.8, b=None, mehr=''):
    return t(x, y, e(text.upper()), 'm' + (' c' if b else ''), f'font-size:{gr}mm;letter-spacing:.2em;color:{farbe};{mehr}', b)


def falz(x, y, b, waag=True, farbe='rgba(179,152,103,.7)'):
    if waag:
        return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:0;border-top:.25mm dashed {farbe}"></i>'
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:0;height:{b}mm;border-left:.25mm dashed {farbe}"></i>'


def feld(x, y, b, h, farbe, r=1.4, d=.25):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;border:{d}mm solid {farbe};border-radius:{r}mm"></i>'


def kreis_feld(x, y, d=2.6, farbe=TINTE):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm;border:.3mm solid {farbe};border-radius:50%"></i>'


# ------------------------------------------------------------------ die fünf
def bon():
    """Der Bon der Rezeption zum Mitnehmen, 80 × 150 mm wie ein Kassenzettel, unten gezackt"""
    zahn = 16
    zack = ' '.join(f'{i * 80 / zahn:.2f},{146 if i % 2 == 0 else 150}' for i in range(zahn + 1))
    posten = ''.join(f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding:1.8mm 0;border-bottom:.2mm dashed {WAND}">'
                     f'<span style="font-family:\'Fjalla One\';font-size:4mm;color:{NACHT}">{e(k)}</span>'
                     f'<span style="font-family:\'DM Mono\';font-size:2.4mm;letter-spacing:.12em;color:{LAERCHE_T}">INKL.</span></div>' for k, _s in N.INKL_KURZ)
    inn = (f'<svg class="abs" style="left:0;top:0;width:80mm;height:150mm" viewBox="0 0 80 150"><polygon points="0,0 80,0 {" ".join(reversed(zack.split()))}" fill="{PAPIER}"/></svg>'
           + hw(40, 9, 30, BLAU)
           + etk(0, 25, 'Der Bon der Rezeption', GRAU, 1.5, 80)
           + t(0, 30, 'Ihr Aufenthalt', 's c', f'font-size:6.4mm;color:{NACHT}', 80)
           + f'<div class="abs" style="left:9mm;top:42mm;width:62mm">{posten}'
           f'<div style="display:flex;justify-content:space-between;align-items:baseline;padding-top:2.6mm"><span style="font-family:\'Fjalla One\';font-size:5mm;color:{NACHT}">Total</span>'
           f'<span style="font-family:\'DM Mono\';font-size:2.8mm;letter-spacing:.12em;color:{LAERCHE_T}">INKLUSIVE</span></div></div>'
           + t(6, 116, e(N.SATZ), 's c', f'font-size:4.6mm;color:{NACHT}', 68)
           + etk(0, 126, N.NAME + ' · ' + N.ORT, GRAU, 1.35, 80, 'letter-spacing:.12em')
           + etk(0, 130.5, 'Tel. ' + N.TEL, GRAU, 1.35, 80, 'letter-spacing:.12em'))
    return [blatt(80, 150, inn, '', 'background:transparent')]


def tuerhaenger():
    """Türhänger 90 × 220 mm mit Loch für die Klinke: vorne «Bitte nicht stören», hinten «Willkommen im Monte-Moro.»"""
    loch = f'<i class="abs" style="left:27mm;top:12mm;width:36mm;height:36mm;border-radius:50%;background:#fff;border:.3mm solid {MESSING}"></i>'
    schlitz = f'<i class="abs" style="left:44.6mm;top:0;width:.8mm;height:13mm;background:#fff"></i>'
    v = (kasten(0, 0, 90, 220, f'background:{NACHT}') + loch + schlitz
         + hz(45, 72, 40, LAERCHE)
         + etk(0, 92, 'Zimmer · Hotel Monte-Moro', MESSING, 1.6, 90)
         + t(0, 100, 'Bitte<br>nicht stören.', 's c', f'font-size:13.5mm;line-height:1.04;color:{PAPIER}', 90)
         + lin(39, 136, 12, LAERCHE, .3)
         + t(10, 143, 'Und morgen scheint<br>die Sonne wieder.', 'c', f'font-size:4.4mm;line-height:1.45;color:{WAND}', 70)
         + hw(45, 192, 30, PAPIER))
    r = (kasten(0, 0, 90, 220, f'background:{PAPIER}') + loch + schlitz
         + hz(45, 72, 40, LAERCHE)
         + etk(0, 92, 'Zimmer · Hotel Monte-Moro', LAERCHE_T, 1.6, 90)
         + t(0, 100, 'Gern<br>aufräumen.', 's c', f'font-size:13.5mm;line-height:1.04;color:{NACHT}', 90)
         + lin(39, 136, 12, MESSING, .3)
         + t(10, 143, 'Ein Zeichen für das Haus, dann ist Ihr Zimmer fertig, wenn Sie vom Berg zurückkommen.', 'c', f'font-size:4.4mm;line-height:1.45;color:{GRAU}', 70)
         + hw(45, 192, 30, BLAU))
    return [blatt(90, 220, v, '', f'background:{NACHT}'), blatt(90, 220, r, '', f'background:{PAPIER}')]


def anhaenger():
    """Kofferanhänger 60 × 110 mm mit Öse, wie früher die Etiketten der Hotels; hinten Name und Adresse zum Ausfüllen"""
    oese = f'<i class="abs" style="left:26mm;top:7mm;width:8mm;height:8mm;border-radius:50%;background:#fff;border:.6mm solid {MESSING}"></i>'
    v = (kasten(0, 0, 60, 110, f'background:{NACHT}') + oese
         + f'<i class="abs" style="left:4mm;top:20mm;width:52mm;height:86mm;border:.3mm solid {MESSING};border-radius:1.6mm"></i>'
         + hz(30, 30, 30, LAERCHE)
         + t(0, 42, 'Saas-<br>Almagell', 's c', f'font-size:9mm;line-height:1.02;color:{PAPIER}', 60)
         + etk(0, 66, 'Wallis · Schweiz', MESSING, 1.5, 60)
         + hw(30, 82, 32, PAPIER))
    linien = (t(6, 46, e(N.NAME) + '<br>' + e(N.PLZ_ORT) + '<br>Tel. ' + e(N.TEL) + '<br>' + e(N.MAIL), 'c', f'font-size:2.9mm;line-height:1.6;color:{TINTE}', 48)
              + t(6, 74, 'Mehr erleben,<br>weniger zahlen.', 's c', f'font-size:4.4mm;line-height:1.1;color:{NACHT}', 48))
    r = (kasten(0, 0, 60, 110, f'background:{PAPIER}') + oese
         + etk(0, 22, 'Gast im', LAERCHE_T, 1.5, 60)
         + t(0, 27, 'Monte-Moro.', 's c', f'font-size:6.4mm;color:{NACHT}', 60)
         + lin(24, 38, 12, MESSING, .3)
         + linien
         + hz(30, 98, 12, LAERCHE))
    return [blatt(60, 110, v, '', f'background:{NACHT}'), blatt(60, 110, r, '', f'background:{PAPIER}')]


def kissen():
    """Kärtchen auf dem Kissen, A7 quer 105 × 74: vorne der Satz, hinten das Frühstück und der Racletteabend"""
    v = (kasten(0, 0, 105, 74, f'background:{NACHT}')
         + hz(52.5, 10, 22, LAERCHE)
         + t(0, 22, 'Und morgen scheint<br>die Sonne wieder.', 's c', f'font-size:7.4mm;line-height:1.08;color:{PAPIER}', 105)
         + lin(46.5, 44, 12, LAERCHE, .3)
         + etk(0, 50, 'Gute Nacht im Monte-Moro', MESSING, 1.6, 105))
    r = (kasten(0, 0, 105, 74, f'background:{PAPIER}')
         + etk(10, 12, 'Für morgen', LAERCHE_T, 1.6)
         + t(10, 17, 'Unten ist das Frühstück gedeckt.', 's', f'font-size:5.2mm;line-height:1.1;color:{NACHT}', 85)
         + lin(10, 31, 12, MESSING, .3)
         + t(10, 36, 'Das Frühstücksbuffet für alle Gäste. Mit dem Bon in der Tasche sind es zwei Minuten bis zum Lift, und das Postauto im ganzen Saastal ist inklusive.',
             '', f'font-size:3mm;line-height:1.45;color:{TINTE}', 85)
         + etk(10, 62, N.NAME + ' · ' + N.ORT, GRAU, 1.35, None, 'letter-spacing:.12em')
         + hz(90, 60, 10, LAERCHE))
    return [blatt(105, 74, v, '', f'background:{NACHT}'), blatt(105, 74, r, '', f'background:{PAPIER}')]


def serviette():
    """Serviette fürs Röstihüs 125 × 125 mm (gefaltet 62,5 mm): Papier mit der Wortmarke, Nacht mit «Es lebe die Tradition!»"""
    a = (falz(0, 62.5, 125, True, 'rgba(19,38,58,.18)') + falz(62.5, 0, 125, False, 'rgba(19,38,58,.18)')
         + feld(66, 66, 55, 55, MESSING) + hw(93.75, 80, 36, BLAU) + etk(62.5, 108, 'Röstihüs', LAERCHE_T, 1.5, 62.5))
    b = (kasten(0, 0, 125, 125, f'background:{NACHT}')
         + falz(0, 62.5, 125, True, 'rgba(179,152,103,.3)') + falz(62.5, 0, 125, False, 'rgba(179,152,103,.3)')
         + feld(66, 66, 55, 55, MESSING) + hz(93.75, 74, 16, LAERCHE)
         + t(66, 84, 'Es lebe<br>die Tradition!', 's c', f'font-size:6.2mm;line-height:1.08;color:{PAPIER}', 55)
         + etk(62.5, 108, 'Röstihüs', MESSING, 1.5, 62.5))
    return [blatt(125, 125, a, '', f'background:{PAPIER}'), blatt(125, 125, b, '', f'background:{NACHT}')]


BEIGABEN = [
    ('bon', 'Der Bon der Rezeption', 'Kassenzettel 80 × 150 mm', bon, [('bon', 1)], [('bon', 34, '')],
     ['Der Bon', 'zum Mitnehmen.'], 'Bei der Ankunft in die Hand: alles, was im Zimmerpreis steckt, als Bon wie auf der Website. Postauto, Bergbahnen, Frühstück, Raclette, Kidsclub, Parkplatz, und unten steht «inklusive».'),
    ('tuerhaenger', 'Türhänger', 'Türhänger 90 × 220 mm, zwei Seiten', tuerhaenger, [('tuerhaenger', 1), ('tuerhaenger-r', 2)], [('tuerhaenger', 30, 'Vorderseite'), ('tuerhaenger-r', 30, 'Rückseite')],
     ['Ein Zeichen', 'an der Tür.'], 'Vorne in der Nacht des Hauses «Bitte nicht stören.», hinten auf Papier die Bitte ums Aufräumen. Oben das Loch für die Klinke, unten die Wortmarke.'),
    ('anhaenger', 'Kofferanhänger', 'Anhänger 60 × 110 mm mit Öse, zwei Seiten', anhaenger, [('anhaenger', 1), ('anhaenger-r', 2)], [('anhaenger', 30, 'Vorderseite'), ('anhaenger-r', 30, 'Rückseite')],
     ['Ein Anhänger', 'für den Koffer.'], 'Wie früher die Etiketten der Hotels: vorne Saas-Almagell unter dem Bergkamm, hinten die Adresse des Hauses und sein Satz. Fährt mit dem Gast nach Hause.'),
    ('kissen', 'Kärtchen auf dem Kissen', 'A7 quer, 105 × 74 mm, zwei Seiten', kissen, [('kissen', 1), ('kissen-r', 2)], [('kissen', 46, 'Vorderseite'), ('kissen-r', 46, 'Rückseite')],
     ['Gute Nacht', 'im Monte-Moro.'], 'Am Abend auf dem Kissen: vorne der Satz von der Seite «Anreise», hinten, was am Morgen wartet.'),
    ('serviette', 'Servietten fürs Röstihüs', 'Serviette 125 × 125 mm, gefaltet 62,5 mm', serviette, [('serviette', 1), ('serviette-n', 2)], [('serviette', 46, 'Papier'), ('serviette-n', 46, 'Nacht')],
     ['Eine Serviette', 'im Röstihüs.'], 'Zwei Fassungen: Papier mit der Wortmarke in Logo-Blau, die Nacht mit dem Bergkamm und «Es lebe die Tradition!». Gefaltet liegt das Motiv oben.'),
]


def setzen():
    plan = []
    for ident, name, fmt, fn, vorschau, karton, tit, satz in BEIGABEN:
        bl = fn()
        P.seite('beigabe-' + ident, bl, name)
        plan.append(dict(id=ident, name=name, format=fmt, vorschau=vorschau, satz=satz, seiten=len(bl), karton=karton, titel=tit))
    json.dump({'druck': plan}, open(os.path.join(W, 'beigaben_plan.json'), 'w'), ensure_ascii=False, indent=1)
    ids = {'beigabe-' + b[0] + '.html' for b in BEIGABEN}
    for f in os.listdir(P.SATZ):
        if f.startswith('beigabe-') and f not in ids:
            os.remove(os.path.join(P.SATZ, f))
    print('Beigaben gesetzt:', len(plan))


def seite():
    from PIL import Image
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    roh, ziel = os.path.join(W, 'roh', 'beigaben'), os.path.join(ROOT, 'beigaben', 'img')
    os.makedirs(ziel, exist_ok=True)
    for f in os.listdir(ziel):
        os.remove(os.path.join(ziel, f))
    M = {}
    for d in plan['druck']:
        for name, _ in d['vorschau']:
            im = Image.open(os.path.join(roh, name + '.png')).convert('RGBA')
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(os.path.join(ziel, name + '.webp'), 'WEBP', quality=88, method=5); M[name] = im.size
    FL = ['fl--papier', 'fl--nacht tapete-leicht', 'fl--creme', 'fl--papier', 'fl--creme']
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(plan['druck'])) + ' Beigaben', 'für Ihre Gäste.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Kleine Dinge, die ein Gast im Monte-Moro in die Hand bekommt, an der Tür findet oder mit nach Hause nimmt. Alle im Stil der neuen Seite, jede als Druckvorlage. Was nicht passt, lassen Sie einfach weg.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Drucksachen', '../drucksachen/index.html', 'kn--linie')}</div>
    </div>
  </div>
</section>
'''
    for i, d in enumerate(plan['druck']):
        figs = ''.join(f'<figure class="sch" data-a="schweb" style="width:{w}%;--i:{k % 4}"><img src="img/{nm}.webp" width="{M[nm][0]}" height="{M[nm][1]}" alt="{e(d["name"])}" decoding="async">'
                       f'{f"<figcaption>{e(u)}</figcaption>" if u else ""}</figure>' for k, (nm, w, u) in enumerate(d['karton']))
        haupt += f'''<section class="fl {FL[i % len(FL)]} blatt stueck{" stueck--r" if i % 2 else ""}" id="{d['id']}">
  <div class="in">
    <div class="stueck__t">
      {kap(i + 1, e(d['name']))}
      {titel(d['titel'])}
      <div class="lauf"><p data-a="worte">{e(d['satz'])}</p></div>
      <p class="stueck__f" data-a="auf">{e(d['format'])}</p>
      <div class="kn-reihe" data-a="auf">{kn('Als PDF ansehen', f"pdf/{H.KURZ}-{d['id']}.pdf", neu=True)}</div>
    </div>
    <div class="karton">{figs}</div>
  </div>
</section>
'''
    haupt += f'''<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Untersetzer, Sticker und Postkarten im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}{kn('Postkarten', '../postkarten/index.html', 'kn--linie')}</div></div></section>'''
    K.schreib(os.path.join(ROOT, 'beigaben', 'index.html'), K.rahmen('Beigaben', f'{zahl(len(plan["druck"]))} Beigaben für die Gäste des Hotels Monte-Moro.', 'Beigaben', haupt))
    Image.open(os.path.join(ziel, 'bon.webp')).save(os.path.join(ziel, 'vorschau.webp'), 'WEBP', quality=86)
    ids = {d['id'] for d in plan['druck']}
    pd = os.path.join(ROOT, 'beigaben', 'pdf')
    for f in os.listdir(pd):
        if not any(f == f'{H.KURZ}-{i}.pdf' for i in ids):
            os.remove(os.path.join(pd, f))
    print('Seite gebaut: beigaben/ ·', len(plan['druck']), 'Beigaben')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
