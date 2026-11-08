#!/usr/bin/env python3
"""Recherche Station 3 (Sammler) als Seite im Stand der Werkbank: Hotel Monte-Moro, Saas-Almagell.
Gestaltung aus dem Werkbank-Kit mit den Haken von ../../02-spaeher/_bau/_werkbank/haus.py (gleiche Farben, gleiches Zeichen).
Inhalt: ../fakten.json, ../sprachen.json, ../stand.json, _quelle/Material-Übersicht.md (Zahlen je Ordner), _quelle/_boegen/.
Aufruf: python3 recherche.py   →  ../recherche.html"""
import glob, json, os, sys, html
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
PAKET = os.path.dirname(HIER)
BAU02 = os.path.join(os.path.dirname(PAKET), '02-spaeher', '_bau')
sys.argv = [sys.argv[0], BAU02]
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K  # noqa: E402

e = html.escape
Q = os.path.expanduser('~/Desktop/Website-Projekte/Familie Zurbriggen/_quelle/monte-moro/')
IMG = os.path.join(HIER, 'img')
os.makedirs(IMG, exist_ok=True)
CSSPFAD = '../02-spaeher/_bau/werkbank/'

BILDER = {
    'fassade': (Q + 'extern/myswitzerland/myswitzerland-00072098_m.jpg', 2600, 'Das Hotel Monte-Moro im Sommer, Originaldatei bei Schweiz Tourismus'),
    'raclette': (Q + 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291892107-raclettestubli.jpg', 1200, 'Das Raclettestübli'),
    'stube': (Q + 'website/bilder/restau_restaurant.jpg', 1280, 'Die Stube des Röstihüs'),
}
DUNKEL = {'fassade': (.48, .6)}
M = {k: (K.webp(q, os.path.join(IMG, k + '.webp'), b, dunkel=DUNKEL.get(k)), alt) for k, (q, b, alt) in BILDER.items()}


def bild(k, klasse='', lazy=True):
    (w, h), alt = M[k]
    st = f' style="background-image:url({K.VORAB[k]})"' if k in K.VORAB else ''
    return f'<img src="_bau/img/{k}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=lazy decoding=async" if lazy else ""} class="ld {klasse}"{st}>'


fakten = json.load(open(os.path.join(PAKET, 'fakten.json'), encoding='utf-8'))
sprachen = json.load(open(os.path.join(PAKET, 'sprachen.json'), encoding='utf-8'))
stand = json.load(open(os.path.join(PAKET, 'stand.json'), encoding='utf-8'))
PF, HZ, kap, titel, kn = K.PF, K.HZ, K.kap, K.titel, K.kn


def kopf(nr, name, zeilen, text=''):
    return K.kopf(nr, name, zeilen, text) if text else f'<div class="kopfzeile"><div>{kap(nr, name)}{titel(zeilen)}</div></div>'


# ---------------------------------------------------------------- Vorrat je Quelle (gezählt aus den Ordnern, nicht abgeschrieben)
def zaehle(d, endungen=('.jpg', '.jpeg', '.png', '.webp')):
    fs = [f for f in glob.glob(os.path.join(Q, d, '*')) if f.lower().endswith(endungen)]
    gr = 0
    for f in fs:
        try:
            gr = max(gr, Image.open(f).size[0])
        except Exception:
            pass
    return len(fs), gr


VORRAT = []
for d, quelle, herkunft, rechte, bogen, neu in [
    ('website/bilder', 'Website monte-moro.ch', 'jedes Bild mit Adresse in herkunft.json, 09.10.2026', 'Haus (Impressum: Hotel Monte-Moro oder genannte Rechtsinhaber)', 'website_bilder', False),
    ('extern/myswitzerland', 'Schweiz Tourismus', 'Originale aus der Datenbank von HotellerieSuisse, 17.10.2026', 'vom Haus geliefert', 'extern_myswitzerland', True),
    ('extern/booking', 'Booking.com', 'vom Haus eingestellte Fotos, 09.10.2026', 'vom Haus bei Booking eingestellt', 'extern_booking', False),
    ('extern/tripadvisor/vom-hotel', 'TripAdvisor, vom Haus', 'Fotos des Hauses, 2017 und 2018 eingestellt', 'Haus', 'extern_tripadvisor_vom-hotel', False),
    ('extern/ig', 'Instagram @hotelmonte_moro', 'zwölf Beiträge ohne Anmeldung, am 17.10.2026 unverändert', 'Haus', 'extern_ig', False),
    ('extern/tripadvisor/gaestefotos', 'TripAdvisor, Gäste', 'Fotos von Gästen', 'bei den Gästen, nur zur Anschauung', 'extern_tripadvisor_gaestefotos', False),
]:
    n, gr = zaehle(d)
    VORRAT.append((d, quelle, n, gr, herkunft, rechte, bogen, neu))
summe = sum(v[2] for v in VORRAT)
videos = sorted(glob.glob(Q + 'video/**/*.mp4', recursive=True))
pdfs = sorted(glob.glob(Q + '**/*.pdf', recursive=True))
texte = [f for f in glob.glob(Q + '**/*.md', recursive=True) if os.path.basename(f) not in ('Material-Übersicht.md', 'notizen.md')]

for d, quelle, n, gr, herkunft, rechte, bogen, neu in VORRAT:
    q_ = os.path.join(Q, '_boegen', bogen + '.jpg')
    if os.path.exists(q_):
        M['b-' + bogen] = (K.webp(q_, os.path.join(IMG, 'b-' + bogen + '.webp'), 1800, q=80), 'Bogen ' + quelle)

zeilen_v = ''.join(f'<tr{" class=neu" if neu else ""}><td><b>{e(quelle)}</b><small class="mono">_quelle/{e(d)}</small></td><td class="zahl">{n}</td><td class="zahl">{gr} px</td><td>{e(herkunft)}</td><td>{e(rechte)}</td></tr>' for d, quelle, n, gr, herkunft, rechte, bogen, neu in VORRAT)
boegen = ''.join(f'<figure class="rc-bogen" data-a="auf" style="--i:{min(i, 4)}">{bild("b-" + b)}<figcaption><b>{e(qu)}</b> · {n} Bilder{" · neu am 17.10.2026" if neu else ""}</figcaption></figure>' for i, (d, qu, n, gr, h, r, b, neu) in enumerate(VORRAT) if 'b-' + b in M)

NEU = [
    ('Schweiz Tourismus', 'Zehn Originale aus der Datenbank von HotellerieSuisse, darunter die Sommerfassade mit 3734 × 2447 px, das schärfste Bild des Hauses. Dazu die Texte der Einträge «Monte-Moro Residence» und «Restaurant Röstihüs».'),
    ('Englisch und Französisch', 'Die ganze Seite in beiden Sprachen, 32 Seiten als Text, und die französische Speisekarte. Die deutsche Seite ist seit dem 09.10.2026 unverändert.'),
    ('Zwei Filme', 'Ein zweites Gäste-Video von 2022 und «Wallis Baby» vom Kanal «Fabian Zurbriggen» (09.10.2026), mit Szenen im Röstihüs und im Hotel Pirmin Zurbriggen.'),
    ('Handelsregister', 'Der Wortlaut der Meldungen zur Resort Monte Moro AG, zur Wellness Spa Zurbriggen Hotel AG und zur Zurbriggen Resort AG in Liquidation.'),
]
NICHT = [
    ('TripAdvisor', 'Chrome mit der Claude-Erweiterung war nicht verbunden. Note und Anzahl vom 09.10.2026 übernommen, ein möglicher Eintrag des Röstihüs nicht geprüft.'),
    ('Google', 'Fotos (128 laut Google) und die Sprachen der 121 Bewertungen lassen sich im Hintergrund nicht abrufen.'),
    ('Instagram, Facebook', 'Instagram ohne Anmeldung nur zwölf Beiträge, Facebook nur mit Anmeldung.'),
    ('Öffnungszeiten Röstihüs', 'Weder auf der Seite noch bei Schweiz Tourismus, das Feld dort ist leer.'),
    ('Wikipedia, Commons, Presse', 'Kein Artikel und kein freies Bild zum Haus, keine Presse zum Haus selbst.'),
]

# ---------------------------------------------------------------- Fakten als Tabelle (offen = rot)
NAMEN = [('name', 'Name'), ('sterne', 'Sterne'), ('adresse', 'Adresse'), ('telefon', 'Telefon'), ('mail', 'Mail'), ('zimmer', 'Zimmer'), ('preise_ab', 'Preise ab'),
         ('preise_ferienwohnungen', 'Preise Wohnungen'), ('restaurants', 'Restaurant'), ('oeffnungszeiten', 'Öffnungszeiten'), ('saison', 'Saison'), ('wellness', 'Spa'),
         ('inklusive', 'Inbegriffen'), ('lage', 'Lage'), ('anreise', 'Anreise'), ('buchungsweg', 'Buchung'), ('auszeichnungen', 'Auszeichnungen'), ('geschichte', 'Geschichte'),
         ('personen', 'Personen'), ('sprachen_website', 'Sprachen der Seite'), ('rechtstexte', 'Rechtstexte'), ('social', 'Social')]


def kurz(k, f):
    w = f.get('wert') if isinstance(f, dict) else None
    if k == 'zimmer':
        return f"{w['anzahl']} Zimmer, {w['betten']} Betten: " + ', '.join(w['kategorien'])
    if k == 'preise_ab':
        return ' · '.join(f"{p['kategorie']} CHF {p['preis']:.2f}" for p in w) + ' (pro Person und Tag)'
    if k == 'restaurants':
        r = w[0]
        return f"{r['name']}: {r['art']}"
    if k == 'buchungsweg':
        return f"{w['system']}, {w['link']}"
    if k == 'personen':
        return ' · '.join(f"{p['name']} ({p['rolle']})" for p in w)
    if k == 'rechtstexte':
        return 'Impressum und Datenschutz vorhanden; AGB, Widerruf, Storno: offen'
    if k == 'social':
        return f"Instagram {w['instagram']}"
    if k == 'auszeichnungen':
        return 'keine eigene'
    if isinstance(w, list):
        return ' · '.join(str(x) for x in w)
    if isinstance(w, dict):
        return ', '.join(f'{a}: {b}' for a, b in w.items())
    return '' if w is None else str(w)


def quelle(k, f):
    if k == 'rechtstexte':
        return f['impressum']
    return f.get('quelle', '') if f.get('quelle') != 'offen' else f.get('gesucht', '')


zeilen_f = ''
for k, n in NAMEN:
    f = fakten.get(k)
    if f is None:
        continue
    offen = (isinstance(f, dict) and f.get('quelle') == 'offen') or k == 'rechtstexte'
    wert = 'offen' if isinstance(f, dict) and f.get('quelle') == 'offen' else kurz(k, f)
    zeilen_f += f'<tr{" class=offen" if offen else ""}><td><b>{e(n)}</b></td><td>{e(wert)}</td><td class="q">{e(quelle(k, f))[:260]}</td></tr>'

noten = fakten['noten']['wert']
noten_html = ''.join(f'<div class="bf-note" data-a="kipp" style="--i:{i}"><b>{e(x["note"].split(" ")[0])}</b><small>{e(" ".join(x["note"].split(" ")[1:3]))}</small><h3>{e(x["portal"])}</h3><p class="mono">{x["anzahl"]} Bewertungen · {e(x["datum"])}</p></div>' for i, x in enumerate(noten))
spr_html = ''.join(f'<li><span>{e(g["sprache"])}</span><b>{g["anzahl"]}</b></li>' for g in sprachen['gaeste'])
offen_html = ''.join(f'<li><b>{e(o["punkt"])}</b><small>{e(o["wo"])}</small></li>' for o in stand.get('offen', [])) or '<li><b>Keine</b></li>'

T = []
T.append(f'''
<section class="auftakt bf-auftakt">
  {bild('fassade', 'bf-auftakt__bild', lazy=False)}
  <div class="in bf-auftakt__in">
    <div class="auftakt__t">
      <p class="gruss" data-a="auf">Station 3 · Der Sammler · 17.10.2026</p>
      {titel(['Alles, was es über', 'das Monte-Moro gibt.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:1600ms">{summe} Bilder aus sechs Quellen, {len(videos)} Filme, {len(pdfs)} Speisekarten, {len(texte)} Texte. Das Material vom 09.10.2026 ist geprüft und ergänzt, nichts wurde doppelt geholt oder verschoben.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:6">{kn('Zum Vorrat', '#vorrat')}{kn('Offene Punkte', '#offen', 'kn--linie')}</div>
    </div>
    <aside class="bf-urteil" data-a="kipp" style="--i:4">{HZ}<small>Das beste Bild</small><b>Sommerfassade, 3734 px</b><p>Neu von Schweiz Tourismus. Es trägt einen ersten Eindruck. Alles andere ist höchstens 2000 px breit.</p></aside>
  </div>
  <div class="in auftakt__fuss mono" data-a="auf" style="--i:9"><span class="runter"><i></i>Einfach nach unten scrollen</span><span>Stand 17.10.2026</span><span>Robert Reff · Tasty Studios</span></div>
</section>''')

T.append(f'''
<section class="fl fl--papier blatt" id="vorrat">
  <div class="in">
    {kopf(1, 'Vorrat', ['Was da ist,', 'Quelle für Quelle.'], 'Gezählt aus den Ordnern. Grösste Fassung je Quelle in Pixel Breite. Neu am 17.10.2026 ist hell hinterlegt.')}
    <div class="rc-tab" data-a="auf"><table><thead><tr><th>Quelle</th><th>Bilder</th><th>Grösste</th><th>Herkunft</th><th>Rechte</th></tr></thead><tbody>{zeilen_v}</tbody></table></div>
    <p class="rc-satz" data-a="auf"><b>Zu den Rechten:</b> Alles ausser den Gästefotos und Gäste-Videos stammt vom Haus selbst, auf der eigenen Seite oder bei Portalen eingestellt; die Gäste-Bilder dienen nur zur Anschauung und kommen nie auf eine Seite.</p>
  </div>
</section>''')

T.append(f'''
<section class="fl fl--navy tapete blatt" id="boegen">
  <div class="in">
    {kopf(2, 'Bögen', ['Jedes Bild', 'auf einen Blick.'], 'Je Quelle ein Bogen. Gehört jedes Bild zu diesem Haus? Ja, bis auf die Wellness-Bilder (Spa des Partnerhotels) und die Bilder der Region ohne Herkunft.')}
    <div class="rc-boegen">{boegen}</div>
  </div>
</section>''')

T.append(f'''
<section class="fl fl--papier blatt" id="neu">
  <div class="in bf-zwei">
    <div>
      {kap(3, 'Neu seit dem 09.10.2026')}
      {titel(['Was heute', 'dazukam.'])}
      <div class="bf-fehlt rc-neu">{''.join(f'<div class="bf-f" data-a="auf" style="--i:{i}"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(NEU))}</div>
    </div>
    <div class="bf-stapel">
      <div class="abzug bf-a1" data-a="schweb" style="--r:-2deg;--r0:-6deg;--i:1">{bild('stube')}<span>Die Stube des Röstihüs</span></div>
      <div class="abzug bf-a2" data-a="schweb" style="--r:2.4deg;--r0:7deg;--i:2">{bild('raclette')}<span>Das Raclettestübli</span></div>
    </div>
  </div>
</section>''')

T.append(f'''
<section class="fl fl--nacht blatt" id="karte">
  <div class="in">
    {kopf(4, 'Speisekarte', ['Eine Karte', 'für alles.'], 'Speisen, Weine und Getränke in einem PDF, deutsch und französisch, beide vom 18.11.2024 und heute noch auf der Seite. Eine eigene Getränke- oder Mittagskarte gibt es nicht.')}
    <div class="bf-platten">
      <div class="bf-platte" data-a="kipp" style="--i:1">{HZ}<h3>Best of Röstis</h3><p>Elf Röstis auf der Karte, von «Rösti Albert» bis «Rösti Indian Style», CHF 25.– bis 32.–. Dazu fünf Cordon Bleus, CHF 39.– bis 42.–. Die Startseite spricht von zwölf Röstis und sieben Cordon Bleus.</p></div>
      <div class="bf-platte" data-a="kipp" style="--i:2">{HZ}<h3>Fabians Hotelweine</h3><p>Zwei «Hotelweine» Cuvée Spécial, laut Karte «von Fabian selber kreiert», je 7 dl Fr. 67.–. Daneben Walliser Weine von FilsMaye, Cave Emery und Favre und sieben Spritz-Kreationen, darunter der «Zurbriggen Spritz».</p></div>
    </div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(30px,3.4vw,48px)">{kn('Karte deutsch', '../../_quelle/website/pdf/speisekarte.pdf', neu=True)}{kn('Karte französisch', '../../_quelle/website/nachtrag-2026-10-17/pdf/speisekarte-fr.pdf', 'kn--linie', neu=True)}</div>
  </div>
</section>''')

T.append(f'''
<section class="fl fl--navy tapete blatt" id="noten">
  <div class="in">
    {kopf(5, 'Noten und Sprachen', ['Wie Gäste es sehen,', 'und in welcher Sprache.'], 'Nur abgelesen, mit Datum. Die Sprachen der Gäste stammen von Booking; TripAdvisor und Google liessen sich dafür nicht öffnen.')}
    <div class="bf-noten">{noten_html}</div>
    <div class="bf-platten">
      <div class="bf-platte" data-a="kipp" style="--i:1">{HZ}<h3>Sprachen der Gäste auf Booking</h3><ul class="bf-liste">{spr_html}</ul><p class="mono">94 Bewertungen, 17.10.2026</p></div>
      <div class="bf-platte" data-a="kipp" style="--i:2">{HZ}<h3>Reihenfolge, nicht entschieden</h3><p>Deutsch, Französisch, Englisch, Niederländisch, Italienisch. Die heutige Seite und das Tourismusbüro Saas-Fee/Saastal sprechen Deutsch, Englisch und Französisch, Schweiz Tourismus zusätzlich Italienisch. Entschieden wird in Station 15a.</p></div>
    </div>
  </div>
</section>''')

T.append(f'''
<section class="fl fl--papier blatt" id="fakten">
  <div class="in">
    {kopf(6, 'Fakten', ['Jede Angabe', 'mit Quelle.'], 'Kurzfassung von fakten.json. Rot ist, was offen ist oder sich widerspricht.')}
    <div class="rc-tab rc-tab--fakten" data-a="auf"><table><thead><tr><th>Fakt</th><th>Wert</th><th>Quelle</th></tr></thead><tbody>{zeilen_f}</tbody></table></div>
  </div>
</section>''')

T.append(f'''
<section class="schluss" id="offen">
  {bild('fassade', 'schluss__b')}
  <div class="in">
    {kap(7, 'Lücken')}
    {titel(['Was fehlt und was', 'nicht zu bekommen war.'], 'h2', 't1')}
    <div class="bf-platten bf-platten--hell">
      {''.join(f'<div class="bf-platte" data-a="kipp" style="--i:{i}"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(NICHT))}
    </div>
    <div class="bf-offen" data-a="auf"><h3>Offen</h3><ul>{offen_html}</ul></div>
    <div class="kn-reihe" data-a="auf">{kn('Material-Übersicht', '../../_quelle/Material-%C3%9Cbersicht.md', neu=True)}{kn('Bau-Prompt', '../../Prompt%20%E2%80%94%20Hotel%20Monte-Moro,%20Saas-Almagell.md', 'kn--linie', neu=True)}</div>
  </div>
</section>''')

CSS02 = open(os.path.join(BAU02, 'befund.py'), encoding='utf-8').read().split("CSS = '''")[1].split("'''")[0]
CSS = CSS02 + '''
.rc-tab{margin-top:clamp(30px,3.4vw,50px);border-radius:var(--rund);overflow:auto;background:var(--weiss);box-shadow:inset 0 2px 10px rgba(21,32,46,.07),0 24px 50px -36px rgba(21,32,46,.45)}
.rc-tab table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5}
.rc-tab th{font-family:var(--mono);font-size:11px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:var(--taupe);text-align:left;padding:18px 20px 12px}
.rc-tab td{padding:14px 20px;border-top:1px solid rgba(21,32,46,.09);vertical-align:top}
.rc-tab td b{font-family:var(--serif);font-weight:500;font-size:17px;display:block}
.rc-tab td small{display:block;font-size:11px;color:var(--taupe);margin-top:2px}
.rc-tab td.zahl{font-family:var(--serif);font-size:22px;white-space:nowrap}
.rc-tab tr.neu td{background:rgba(207,162,108,.14)}
.rc-tab tr.offen td{color:var(--rot)}
.rc-tab tr.offen td b{color:var(--rot)}
.rc-tab--fakten td.q{font-size:12.5px;line-height:1.5;color:#5d6773;width:36%;overflow-wrap:anywhere}
.rc-tab--fakten td:first-child{width:16%}
.rc-satz{max-width:80ch;margin:22px 0 0;line-height:1.65}
.rc-boegen{display:grid;gap:clamp(18px,2vw,28px);margin-top:clamp(30px,3.4vw,50px)}
.rc-bogen{margin:0;background:var(--papier);border-radius:var(--rund);padding:clamp(12px,1.4vw,18px);box-shadow:0 30px 60px -36px rgba(0,0,0,.6)}
.rc-bogen img{width:100%;height:auto;border-radius:calc(var(--rund) - 10px);display:block;background-size:cover}
.rc-bogen figcaption{color:var(--tinte);font-size:14px;padding:12px 6px 4px}
.rc-bogen figcaption b{font-family:var(--serif);font-weight:500;font-size:18px}
.rc-neu{grid-template-columns:1fr 1fr!important}
@media (max-width:560px){.rc-neu{grid-template-columns:1fr!important}.rc-tab table{font-size:13.5px}.rc-tab td,.rc-tab th{padding:10px 12px}}
'''
nav = ''.join(f'<a href="#{a}">{b}</a>' for a, b in (('vorrat', 'Vorrat'), ('boegen', 'Bögen'), ('neu', 'Neu'), ('karte', 'Karte'), ('noten', 'Noten'), ('fakten', 'Fakten'), ('offen', 'Lücken')))
seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recherche · Hotel Monte-Moro</title>
<meta name="description" content="Station 3 der Kette: alles gesammelte Material zum Hotel Monte-Moro, Saas-Almagell, mit Noten, Fakten und Lücken.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{K.H.FARBEN['nacht']}">
<link rel="preload" href="{CSSPFAD}fonts/{K.H.SCHRIFT['titel'][1]}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{CSSPFAD}werkbank.css?v={K.v('werkbank.css')}">
<style>{CSS}</style>
</head>
<body class="haus-{K.H.KURZ}">
{K.sprite()}
<div class="gang-linie" aria-hidden="true"></div>
<header class="leiste"><div class="insel">
  <a class="insel__m" href="#oben">{HZ}<span>Recherche</span></a>
  <nav aria-label="Abschnitte">{nav}</nav>
  <a class="glanz" href="https://www.monte-moro.ch/de/" target="_blank" rel="noopener">Heutige Seite{PF}</a>
</div></header>
<main id="oben">
{''.join(T)}
</main>
<footer class="fuss fuss--kurz"><div class="in">
  <div><b>Recherche zum Entwurf</b><p>Kette, Station 3, Sammler. Interne Arbeitsseite von Robert Reff, Tasty Studios, nicht die offizielle Website des Hauses. Fotos gehören {K.H.RECHTE}</p></div>
  <div class="r mono"><span>Stand 17.10.2026</span></div>
</div></footer>
<script src="{CSSPFAD}werkbank.js?v={K.v('werkbank.js')}"></script>
</body>
</html>
'''
open(os.path.join(PAKET, 'recherche.html'), 'w', encoding='utf-8').write(seite)
print('geschrieben', os.path.join(PAKET, 'recherche.html'), len(seite), 'Bilder', summe, 'Videos', len(videos), 'PDFs', len(pdfs), 'Texte', len(texte))
