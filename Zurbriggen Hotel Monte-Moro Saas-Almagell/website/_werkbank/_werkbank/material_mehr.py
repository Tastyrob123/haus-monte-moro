#!/usr/bin/env python3
"""Hotel Monte-Moro: der Ordner «Material» vollständig und frisch (Werkbank Papier, 08.11.2026; Vorlage material_mehr.py der Vorlage).
Läuft nach material.py des Kits und ist allein vollständig:
  1. leert die Ordner material/NN …, damit keine Datei einer früheren Fassung liegen bleibt,
  2. ruft material.py des Kits (unverändert) noch einmal: Unterlagen, Drucksachen, Untersetzer, Zeichen, Ansichten, Instagram,
  3. legt die übernommenen Drucksachen der Hausdruckerei (papier_mehr.json), Sticker, Beigaben, Postkarten und die Mails dazu,
  4. fehlt eine Quelle noch (ein anderer Teil baut gerade), fällt ihr Eintrag weg statt ins Leere zu zeigen,
  5. Kleid wie die übrigen Werkbank-Seiten (zeile_ganz, text_mitte, knopf_mitte), kein mailto.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/mit_papier.py _werkbank/material_mehr.py "<website/_werkbank>"   (wiederholbar)"""
import glob, json, os, re, shutil
import kern as K
from kern import H, ROOT, W, e, kap, kn, PF
import material as M

ZIEL = M.ZIEL
FEHLT = []
_lege_kit = M.lege


def lege(ordner, quelle, name=None):
    """wie material.lege, aber eine fehlende Quelle bricht nicht ab: der Eintrag wird danach aus der Seite genommen"""
    if not os.path.exists(quelle):
        FEHLT.append(os.path.relpath(quelle, ROOT))
        return ordner + '/' + (name or os.path.basename(quelle))
    return _lege_kit(ordner, quelle, name)


def leeren():
    for d in glob.glob(os.path.join(ZIEL, '[0-9][0-9] *')):
        shutil.rmtree(d) if os.path.isdir(d) else os.remove(d)


def mehr():
    N = H.NAME
    sp = json.load(open(os.path.join(W, 'sticker_plan.json')))
    bp = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    st = [('Druckbogen A3', lege('07 Sticker', os.path.join(ROOT, 'sticker', 'pdf', f'{H.KURZ}-sticker-druckbogen-a3.pdf'), f'{N} Sticker Druckbogen A3.pdf')),
          ('Alle einzeln', lege('07 Sticker', os.path.join(ROOT, 'sticker', 'pdf', f'{H.KURZ}-sticker-einzeln.pdf'), f'{N} Sticker einzeln.pdf'))]
    for x in sp['etiketten']:
        lege('07 Sticker/Bilder', os.path.join(W, 'roh', 'sticker', x['id'] + '.png'), 'Sticker ' + x['id'][1:] + ' ' + re.sub(r'[/:’]', ' ', x['name']).strip() + '.png')
    bg = [(d['name'], lege('08 Beigaben', os.path.join(ROOT, 'beigaben', 'pdf', f"{H.KURZ}-{d['id']}.pdf"), f"{N} {re.sub(r'[/:?’]', '', d['name']).strip()}.pdf")) for d in bp['druck']]
    pk = [(t, lege('09 Postkarten', os.path.join(ROOT, 'postkarten', 'pdf', f'{H.KURZ}-postkarten-{d}.pdf'), f'{N} Postkarten {t}.pdf'))
          for d, t in (('druck', 'mit Beschnitt'), ('sammelbogen-a3', 'Sammelbogen SRA3'))
          if os.path.exists(os.path.join(ROOT, 'postkarten', 'pdf', f'{H.KURZ}-postkarten-{d}.pdf'))]
    n_pk = len(json.load(open(os.path.join(W, 'postkarten_plan.json')))['karten'])
    namen = [d['name'] for d in bp['druck']]
    teile = ''
    for i, (name, satz, dateien, ident) in enumerate([
            ('Sticker', f'{K.zahl(len(sp["etiketten"]))} Sticker: der Druckbogen mit Schnittlinien, jeder einzeln und alle als Bild.', st, 'o-sticker'),
            ('Beigaben', (', '.join(namen[:-1]) + ' und ' + namen[-1] if len(namen) > 1 else ''.join(namen)) + ', jede als PDF.', bg, 'o-beigaben'),
            ('Postkarten', f'{K.zahl(n_pk)} Postkarten: mit Beschnitt für die Druckerei und als Sammelbogen.', pk, 'o-postkarten')]):
        zeilen = ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(t)}</span><i>{PF}</i></a></li>' for k, (t, h) in enumerate(dateien))
        teile += f'''<section class="fl {['fl--papier', 'fl--creme', 'fl--papier'][i]} blatt ordnerz" id="{ident}">
  <div class="in">
    <div>{kap(7 + i, e(name))}<div class="lauf"><p data-a="worte">{e(satz)}</p></div></div>
    <ul class="dateien">{zeilen}</ul>
  </div>
</section>
'''
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<section class="fl [^"]*" id="o-(sticker|beigaben|postkarten)">.*?</section>\n', '', s, flags=re.S)
    s = s.replace('<section class="ausklang">', teile + '<section class="ausklang">', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return len(sp['etiketten']), len(bp['druck'])


def hausdruckerei():
    """02 Drucksachen: dazu die fertigen Drucksachen der Hausdruckerei, die papier.py übernommen hat (papier_mehr.json)."""
    try:
        mehr = json.load(open(os.path.join(W, 'papier_mehr.json'), encoding='utf-8'))['druck']
    except (OSError, ValueError, KeyError):
        return 0
    zeilen, k0 = '', 0
    for x in mehr:
        q = os.path.join(ROOT, 'drucksachen', 'pdf', x['pdf'])
        h = lege('02 Drucksachen', q, f"{H.NAME} {re.sub(r'[/:?’]', ' ', x['name']).strip()}.pdf")
        zeilen += f'<li data-a="auf" style="--i:{min(6, 5 + k0)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(x["name"])}</span><i>{PF}</i></a></li>'
        k0 += 1
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    m = re.search(r'(<section class="fl [^"]*" id="o2">.*?<ul class="dateien[^"]*">)(.*?)(</ul>)', s, flags=re.S)
    if m and zeilen:
        s = s[:m.start(2)] + m.group(2) + zeilen + s[m.end(2):]
        s = s.replace(m.group(1), m.group(1).replace('<ul class="dateien">', '<ul class="dateien dateien--2">'), 1)
        open(p, 'w', encoding='utf-8').write(s)
    return k0


def mails():
    """10 Mails: jede Mail als HTML-Datei mit ihren Bildern (zum Einsetzen ins Mailprogramm oder Buchungssystem)."""
    j = os.path.join(ROOT, 'mails', '_src', 'werkbank.json')
    if not os.path.exists(j):
        return 0
    liste = json.load(open(j, encoding='utf-8'))
    dateien = []
    for nr, ordner, name, _satz in liste:
        q = os.path.join(ROOT, 'mails', ordner, 'index.html')
        if not os.path.exists(q):
            continue
        t = open(q, encoding='utf-8').read().replace('../img/', 'Bilder/').replace("../../assets/fonts/", "Schriften/")
        z = os.path.join(ZIEL, '10 Mails'); os.makedirs(z, exist_ok=True)
        open(os.path.join(z, f'{nr} {name}.html'), 'w', encoding='utf-8').write(t)
        dateien.append((name, f'10 Mails/{nr} {name}.html'))
    for f in glob.glob(os.path.join(ROOT, 'mails', 'img', '*')):
        lege('10 Mails/Bilder', f)
    for f in ('FjallaOne-400.woff2', 'InstrumentSans-normal-400_600.woff2', 'DMMono-normal-400.woff2'):
        lege('10 Mails/Schriften', os.path.join(ROOT, 'assets', 'fonts', f))
    if not dateien:
        return 0
    zeilen = ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(t)}</span><i>{PF}</i></a></li>' for k, (t, h) in enumerate(dateien))
    teil = f'''<section class="fl fl--creme blatt ordnerz" id="o-mails">
  <div class="in">
    <div>{kap(10, 'Mails')}<div class="lauf"><p data-a="worte">{K.zahl(len(dateien))} Mails an Gäste, jede als HTML-Datei mit ihren Bildern und Schriften, zum Einsetzen ins Mailprogramm.</p></div></div>
    <ul class="dateien">{zeilen}</ul>
  </div>
</section>
'''
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<section class="fl [^"]*" id="o-mails">.*?</section>\n', '', s, flags=re.S)
    s = s.replace('<section class="ausklang">', teil + '<section class="ausklang">', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return len(dateien)


def nur_dieses_haus():
    """05 Ansichten: nur Bilder der Seiten dieses Hauses (die Aufnahmen macht der Kern-Teil; Namen wie in haus.py › SEITEN)"""
    seiten = {s[1] for s in getattr(H, 'SEITEN', [])}
    stand = os.path.getmtime(os.path.join(W, 'haus.py'))   # Aufnahmen, die älter sind als haus.py, stammen noch aus der Vorlage eines anderen Hauses
    for f in glob.glob(os.path.join(ZIEL, '05 Ansichten der neuen Website', '*', '*.jpg')):
        if (seiten and os.path.basename(f)[:-4] not in seiten) or os.path.getmtime(f) < stand:
            os.remove(f)


AUSLAGE = [   # (Quelle, Klasse, links %, oben %, Breite %, Drehung): ein Stapel aus dem, was in den Ordnern liegt
    (os.path.join(W, 'roh', 'papier', 'pw-roestihues-best-of-roestis.png'), 'blattbild', 2, 6, 32, -6),
    (os.path.join(W, 'roh', 'papier', 'pw-aushang-inklusive.png'), 'blattbild', 34, 0, 31, 3),
    (os.path.join(W, 'roh', 'papier', 'pw-willkommensbrief.png'), 'blattbild', 64, 10, 32, -3),
    (os.path.join(W, 'roh', 'papier', 'u03.png'), 'form', 18, 58, 25, 8),
    (os.path.join(W, 'roh', 'sticker', 's05.png'), 'form', 58, 62, 20, -9),
]


def auslage():
    """Die leere Auslage neben dem Titel füllen (H.MATERIAL['auslage'] ist leer): Drucksachen, ein Untersetzer, ein Sticker, klein als WebP."""
    from PIL import Image
    z = os.path.join(ZIEL, '_auslage'); os.makedirs(z, exist_ok=True)
    teile = ''
    for i, (q, kl, x, y, b, r) in enumerate(AUSLAGE):
        q = q if os.path.isabs(q) else os.path.join(ZIEL, q)
        if not os.path.exists(q):
            continue
        im = Image.open(q); im = im.convert('RGBA' if kl == 'form' else 'RGB'); im.thumbnail((560, 900), Image.LANCZOS)
        n = f'a{i + 1}.webp'; im.save(os.path.join(z, n), 'WEBP', quality=82, method=6)
        teile += (f'<div class="{kl}" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}">'
                  f'<img src="_auslage/{n}" width="{im.width}" height="{im.height}" alt="" loading="eager" decoding="async"></div>')
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<div class="auslage" aria-hidden="true">.*?</div>(?=\s*</div>\s*</section>)', '<div class="auslage" aria-hidden="true">' + teile + '</div>', s, count=1, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)


def nur_neue_beitraege():
    """06 Instagram: nur die neuen Beiträge (die bisherigen des Hauses stehen im Feed nur zum Vergleich)."""
    try:
        n = len(json.load(open(os.path.join(ROOT, 'feed', 'feed.json'), encoding='utf-8'))['posts'])
    except (OSError, KeyError, ValueError):
        return
    for f in glob.glob(os.path.join(ZIEL, '06 Instagram', 'Beiträge', 'Beitrag *.jpg')):
        m = re.search(r'Beitrag (\d+)\.jpg$', f)
        if m and int(m.group(1)) > n:
            os.remove(f)


def aufraeumen():
    """Einträge ohne Datei und leere Ordner-Abschnitte aus der Seite nehmen; Zahl der Ordner im Text nachziehen."""
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()

    def li(m):
        import html as _h
        return m.group(0) if os.path.exists(os.path.join(ZIEL, _h.unescape(m.group(1)))) else ''
    s = re.sub(r'<li data-a="auf"[^>]*><a href="([^"]+)" target="_blank" rel="noopener">.*?</li>', li, s, flags=re.S)
    s = re.sub(r'<section class="fl [^"]*blatt ordnerz" id="[^"]+">\s*<div class="in">(?:(?!</section>).)*?<ul class="dateien[^"]*"></ul>\s*</div>\s*</section>\n?', '', s, flags=re.S)   # nie über einen Abschnitt hinaus
    n = len(re.findall(r'class="fl [^"]*blatt ordnerz"', s))
    s = re.sub(r'liegt hier sortiert in \w+ Ordnern', f'liegt hier sortiert in {K.zahl(n).lower()} Ordnern', s)
    open(p, 'w', encoding='utf-8').write(s)
    return n


ZEICHEN_BILD = {'Wortmarke Logo-Blau': 'wortmarke-blau', 'Wortmarke Papier': 'wortmarke-papier', 'Wortmarke Nacht': 'wortmarke-nacht',
                'Bergkamm Lärche': 'bergkamm-laerche', 'Bergkamm Logo-Blau': 'bergkamm-blau'}


def vorschau():
    """Jede Datei der Liste mit ihrem Bild, wie es wb_kapitel.mit_vorschau (Kern) für PDF und Bilder tut; hier dazu die Zeichen (SVG,
    Bilder aus zeichen_bild.js) und die Mails (HTML, Aufnahme aus mails/_src/aufnahme.js). Danach ergänzt mit_vorschau die übrigen."""
    import hashlib, html as _h, urllib.parse
    from PIL import Image
    vz = os.path.join(ZIEL, '_vorschau'); os.makedirs(vz, exist_ok=True)
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()

    def quelle(href):
        name = os.path.basename(href)
        if href.startswith('04 Zeichen/'):
            k = next((v for a, v in ZEICHEN_BILD.items() if a in name), None)
            return os.path.join(W, 'roh', 'zeichen', k + '.png') if k else None
        if href.startswith('10 Mails/') and name.endswith('.html'):
            return os.path.join(W, 'ansichten', 'Mails', name[:2] + '.jpg')
        return None

    def eins(m):
        href = _h.unescape(m.group(2)); q = quelle(urllib.parse.unquote(href))
        if not q or not os.path.exists(q):
            return m.group(0)
        n = hashlib.sha1(href.encode()).hexdigest()[:12]
        im = Image.open(q).convert('RGB'); im.thumbnail((240, 240)); im.save(os.path.join(vz, n + '.webp'), 'WEBP', quality=78)
        return m.group(1) + f'<span class="dt-b"><img src="_vorschau/{n}.webp" alt="" loading="lazy" decoding="async"></span>'
    s = re.sub(r'(<li[^>]*><a href="([^"]+)"[^>]*>)(?!<span class="dt-b">)', eins, s)
    try:
        import wb_kapitel   # Kern: Vorschauen der PDF und Bilder und ihre Gestaltung (nur aufgerufen, nicht geändert)
        s = wb_kapitel.mit_vorschau(s, ZIEL)
    except Exception as f:   # noqa: BLE001
        print('material: Vorschauen des Kerns nicht verfügbar:', type(f).__name__)
    open(p, 'w', encoding='utf-8').write(s)


def kleid():
    """Titel des Hauses, kein mailto, die Nachbauten der Werkbank (kein Wort allein unten, Schrift mittig in Knöpfen)."""
    import zeile_ganz as ZG, text_mitte as TM
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    for a, b in (('Alles liegt für', 'Alle Dateien'), ('Sie bereit.', 'an einem Ort.'),
                 ('Ihre Unterlagen als Idee im Stil der neuen Seite, jede als PDF.', 'Die Karten des Röstihüs im neuen Satz, jede als PDF.'),
                 ('Fehlt Ihnen eine Datei oder ein Format, schreiben Sie mir gern.', 'Fehlt Ihnen eine Datei oder ein Format, lege ich sie gern dazu.')):
        s = s.replace(a, b)
    s = re.sub(r'<a class="kn [^"]*" href="mailto:[^"]*"[^>]*>.*?</a>', '', s, flags=re.S)   # nichts verschicken: kein mailto auf der Seite
    s = re.sub(r'<style id="material-(wild|haus)">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', '<style id="material-haus">@media (max-width:1400px){.dateien--2{grid-template-columns:minmax(0,1fr)}}.dateien a span{text-wrap:balance}@media (min-width:1000px){.ordnerz .in>div:first-child{position:sticky;top:clamp(110px,9vw,140px)}}</style></head>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    ZG.anwenden(ZIEL)
    TM.anwenden(ZIEL)
    import papier_nach
    papier_nach.nach('material')
    papier_nach.knopf_mitte(p)


def baue():
    K.gestaltung()
    leeren()
    M.lege = lege
    M.baue()
    nur_neue_beitraege()
    nur_dieses_haus()
    npw = hausdruckerei()
    ns, nb = mehr()
    nm = mails()
    n = aufraeumen()
    auslage()
    vorschau()
    kleid()
    dateien = sum(len([f for f in fs if not f.startswith('.')]) for dp, _, fs in os.walk(ZIEL) if '_vorschau' not in dp) - 1
    print('Material:', n, 'Ordner,', dateien, 'Dateien · Hausdruckerei', npw, '· Sticker', ns, '· Beigaben', nb, '· Mails', nm, ('· fehlt noch: ' + ', '.join(sorted(set(FEHLT)))) if FEHLT else '')


if __name__ == '__main__':
    baue()
