#!/usr/bin/env python3
"""Hotel Monte-Moro · Website «Ein Tag am Grat» (Designstudie Tasty Studios, nur lokal). Neubau 18.10.2026 nach Robert: «richtig luxuriös, elegant,
hochwertig und edel … mit richtig heftigen Übergängen, mit neuen innovativen Ideen», Geschichten erzählen statt aneinanderreihen (Master 2.1, Punkt 5).
Der Faden: ein Aufenthalt vom Sonnenaufgang hinter dem Haus bis zur nächsten Anreise. Jede Szene ist ein Gegenstand aus der Welt des Hauses
(Fensterläden aus Lärche, der Bon der Rezeption, Spuren im Schnee, die Kabinen am Seil, der Kartoffelsack des Röstihüs, das Zählwerk, die zwei Gläser
Hotelwein, der Dampf nebenan, die Gipfel der Gäste, die Rückseite des Bons, die Lichter der Familie, die Fallblatt-Tafel). Jede Szene schiebt sich mit dem
Bergkamm des Logos als Oberkante über die vorige, die vorige weicht zurück wie eine ferne Bergkette («Staffelung»).
Vorige Fassungen: ../website.vor-baukasten-2026-10-18/ (Baukasten), ../website.plakat-2026-10-18/ («Das Plakat», verworfen).
   python3 bilder.py && python3 bau.py   →  index.html  (Karte: http://127.0.0.1:8978/haus/…/website/index.html, eigener Server: python3 serve.py → 8947)"""
import html, json, math, os, re, sys
HIER = os.path.dirname(os.path.abspath(__file__)); os.chdir(HIER)
sys.path.insert(0, os.path.join(HIER, 'inhalt'))
import daten as D          # noqa: E402
from bilder import BILDER  # noqa: E402

e = html.escape
ABBILD = json.load(open('assets/img/_abbild.json'))
MASSE = json.load(open('assets/img/_masse.json'))
GROESSEN = {'s': 480, 'm': 900, 'l': 1440, 'x': 2200}
V = str(int(max(os.path.getmtime(os.path.join(d, f)) for d in ('assets/css', 'assets/js') for f in os.listdir(d) if f.endswith(('.css', '.js')))))   # alle Stile und Skripte (23.10.2026)
ZVB, WVB = '0 0 3483 696', '0 0 3483 1425'
# Der Grat (Markenbuch 05, von Robert am 18.10.2026 freigegeben: «Übergang Linie wie ein Bergkamm»)
GRAT = 'M0 60 L0 38 L70 30 L118 6 L150 26 L196 14 L250 40 L300 22 L338 34 L380 8 L430 36 L486 18 L540 42 L600 28 L640 36 L700 12 L748 32 L800 24 L860 44 L920 20 L962 34 L1000 26 L1000 60 Z'
GRAT_LINIE = GRAT.replace('M0 60 L0 38', 'M0 38').replace(' L1000 60 Z', '')
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'


def sym():
    z = open('assets/zeichen/bergkamm-blau.svg').read(); w = open('assets/zeichen/wortmarke-blau.svg').read()
    zi = re.search(r'<svg[^>]*>(.*)</svg>', z, re.S).group(1); wi = re.search(r'<svg[^>]*>(.*)</svg>', w, re.S).group(1)
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="kamm" viewBox="{ZVB}">{zi}</symbol>'
            f'<symbol id="wort" viewBox="{WVB}">{wi}</symbol></defs></svg>')


def kamm(kl=''):
    return f'<svg class="{kl}" viewBox="{ZVB}" fill="currentColor" aria-hidden="true"><use href="#kamm"/></svg>'


def wort(kl=''):
    return f'<svg class="{kl}" viewBox="{WVB}" fill="currentColor" role="img" aria-label="Monte Moro, Saas-Almagell"><use href="#wort"/></svg>'


def bild(key, kl='', sizes='100vw', vorn=False, lage='50% 50%', alt=None):
    """Foto mit Liefergrössen, kleinem echten Abbild als Grund; unter dem ersten Schirm gehalten (bilder.js)."""
    w, h = MASSE[key][:2]
    stufen = [g for g, br in GROESSEN.items() if br < w] + ([g for g, br in GROESSEN.items() if br >= w][:1])
    srcset = ', '.join(f'assets/img/{key}-{g}.webp {min(GROESSEN[g], w)}w' for g in stufen)
    src = f'assets/img/{key}-{"l" if "l" in stufen else stufen[-1]}.webp'
    a = e(alt if alt is not None else BILDER[key][1])
    grund = f'background-image:url({ABBILD[key]});background-size:cover;object-position:{lage}'
    if vorn:
        return f'<img class="{kl}" src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{a}" decoding="async" fetchpriority="high" style="{grund}">'
    return f'<img class="{kl}" data-src="{src}" data-srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{a}" loading="lazy" decoding="async" style="{grund}">'


def kn(text, href='#', kl='', neu=False, tag='a', attr=''):
    """Knopf des Markenbuchs: Pille mit Knauf (Roberts Handschrift)."""
    if tag == 'button':
        return f'<button class="kn {kl}" type="button" {attr}><span>{e(text)}</span><i>{PF}</i></button>'
    z = ' target="_blank" rel="noopener"' if neu else ''
    return f'<a class="kn {kl}" href="{e(href)}"{z} {attr}><span>{e(text)}</span><i>{PF}</i></a>'


def titel(text, em=None, kl='d2', tag='h2'):
    """Titel in Fjalla One; em = Teil in Lärche. Die Zeilen schneidet montemoro.js in Schlitze."""
    t = e(text)
    if em and em in text:
        i = text.index(em); t = e(text[:i]) + f'<em>{e(em)}</em>' + e(text[i + len(em):])
    return f'<{tag} class="{kl}" data-zeilen>{t}</{tag}>'


def ueber(text, kl=''):
    return f'<p class="ueber {kl}" data-s>{e(text)}</p>'


def grat_oben():
    return f'<svg class="grat-oben" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{GRAT}" fill="currentColor"/><path class="grat-oben__linie" d="{GRAT_LINIE}"/></svg>'


def szene(id_, kl, inhalt, aria, nr, grat=True):
    """Eine Szene: liegt, bis die nächste mit dem Grat als Oberkante darüberfährt; der Dunst legt sich dann über sie (Staffelung)."""
    return (f'<section class="szene {kl}" id="{id_}" aria-label="{e(aria)}" data-szene style="z-index:{nr}">'
            f'{grat_oben() if grat else ""}<div class="szene__innen">{inhalt}</div><i class="szene__dunst" aria-hidden="true"></i></section>')


def buchen_form(kl=''):
    return f'''<form class="leiste {kl}" action="{e(D.HAUS['buchen'])}" data-buchen>
      <label><span>Anreise</span><button type="button" class="wahl" data-an></button></label>
      <label><span>Abreise</span><button type="button" class="wahl" data-ab></button></label>
      <label><span>Gäste</span><button type="button" class="wahl" data-g></button></label>
      <button class="kn kn--laerche" type="submit"><span>Zimmer buchen</span><i>{PF}</i></button>
    </form>'''


NAV = [('zimmer.html', 'Zimmer'), ('preise.html', 'Preise'), ('saastal.html', 'Saastal'), ('spa.html', 'Spa'), ('roestihues.html', 'Röstihüs'), ('anreise.html', 'Anreise')]


def kopf(titel_, beschr, aktiv=''):
    links = ''.join(f'<a href="{h}"{" aria-current=page" if h == aktiv else ""}>{e(t)}</a>' for h, t in NAV)
    return f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titel_)}</title>
<meta name="description" content="{e(beschr)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0A2A4A">
<link rel="icon" href="assets/zeichen/medaillon-blau.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/FjallaOne-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tenor+Sans&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/montemoro.css?v={V}">
<link rel="stylesheet" href="assets/css/bewegung.css?v={V}">
<link rel="stylesheet" href="assets/css/fuss.css?v={V}">
<link rel="stylesheet" href="assets/css/familienband-scheiben.css?v={V}">
<link rel="stylesheet" href="assets/css/seite-saastal.css?v={V}">
<link rel="stylesheet" href="assets/css/seite-spa.css?v={V}">
<link rel="stylesheet" href="assets/css/seite-anreise.css?v={V}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{sym()}
<a class="sr" href="#inhalt">Zum Inhalt</a>
<header class="kopf" data-kopf>
  <a class="kopf__marke" href="index.html" aria-label="Hotel Monte-Moro, Startseite">{kamm()}<span>Monte-Moro</span></a>
  <nav class="kopf__nav" aria-label="Hauptmenü">{links}</nav>
  <a class="kn kn--klein kn--laerche kopf__buchen" href="{e(D.HAUS['buchen'])}" target="_blank" rel="noopener"><span>Zimmer buchen</span><i>{PF}</i></a>
  <button class="kopf__menue" type="button" data-menue-auf aria-label="Menü öffnen" aria-expanded="false"><i></i><i></i></button>
</header>
<div class="menue" data-menue aria-hidden="true">
  <button class="menue__zu" type="button" data-menue-zu>Schliessen</button>
  <a href="index.html">Startseite</a>{links}
  {kn('Zimmer buchen', D.HAUS['buchen'], 'kn--laerche', neu=True)}
</div>
<main id="inhalt">
'''


def chat_html():
    return ('<button class="chat-knopf weg" type="button" data-chat-auf aria-label="Fragen an die Rezeption"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg><span>Fragen an die Rezeption</span></button>'
            '<section class="chat" data-chat aria-label="Rezeption im Chat" hidden><header><b>Rezeption</b><small>Hotel Monte-Moro</small><button type="button" data-chat-zu aria-label="Schliessen">×</button></header>'
            '<div class="chat__verlauf" data-chat-verlauf><div class="chat__m chat__m--haus"><p>Guten Tag. Was möchten Sie über Ihren Aufenthalt wissen?</p></div><div class="chat__vorschlag" data-chat-vorschlag></div></div>'
            '<form class="chat__eingabe" data-chat-form><textarea rows="1" placeholder="Ihre Frage" aria-label="Ihre Frage" data-chat-feld></textarea><button type="submit" aria-label="Senden"><svg viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4"/></svg></button></form>'
            '<p class="chat__fuss">Antwortet aus den Angaben des Hauses. Fragen, die dort nicht stehen, gehen an die Rezeption.</p></section>')


def wissen():
    """Fragen und Antworten für die Rezeption im Chat: jede Antwort aus inhalt/daten.py (Wortlaut der Seiten des Hauses)."""
    E = []
    def q(k, frage, antwort): E.append(dict(k=k, q=frage, a=antwort))
    q('Preise', 'Was ist im Preis inbegriffen?', 'Inklusive: ' + '; '.join(D.INKLUSIVE) + '.')
    q('Preise', 'Was kostet ein Zimmer?', ' · '.join(f'{a}, {b}: CHF {c} pro Person / Tag' for a, b, c in D.PREISE) + '.')
    q('Preise', 'Wie hoch ist die Kurtaxe?', ' · '.join(f'{a}: CHF {b}' for a, b in D.ZUSCHLAEGE[:4]) + '.')
    q('Preise', 'Gibt es einen Zuschlag für Einzelzimmer oder kurze Aufenthalte?', f'Einzelzimmerzuschlag {D.ZUSCHLAEGE[4][1]}. Zuschlag für 1 - 3 Übernachtungen / pro Tag CHF {D.ZUSCHLAEGE[5][1]}.')
    q('Preise', 'Kann ich in Euro bezahlen?', D.EURO)
    q('Hund', 'Sind Hunde erlaubt?', f'Hund pro Tag ohne Futter: CHF {D.ZUSCHLAEGE[6][1]}.')
    q('Kinder', 'Gibt es einen Kidsclub für Kinder?', 'Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr, inklusive.')
    q('Kinder', 'Was kosten Kinder im Zimmer der Eltern?', D.KINDER_SATZ + ': ' + ' · '.join(f'{a}: CHF {b}' for a, b in D.KINDER) + '. ' + D.KINDER_EIGEN + '.')
    q('Zimmer', 'Gibt es Familienzimmer?', D.FAMILIE_TEXT)
    q('Zimmer', 'Wie sind die Zimmer ausgestattet?', D.ZIMMER_TEXT)
    q('Zimmer', 'Was ist die Residence Alpenhof?', D.ALPENHOF_TEXT)
    q('Ferienwohnung', 'Wie ist die Ferienwohnung im Haus Apollo?', D.APOLLO)
    q('Ferienwohnung', 'Welche Ferienwohnungen gibt es im Haus Arizona?', D.ARIZONA)
    q('Anreise', 'Wie komme ich mit dem Zug und Postauto zu Ihnen?', D.ANREISE_ZUG + ' ' + D.ANREISE_ZUG_ZEIT)
    q('Anreise', 'Wie komme ich mit dem Auto zu Ihnen?', D.ANREISE_AUTO + ' ' + D.ANREISE_AUTO_ZEIT)
    q('Anreise', 'Ist die Anreise mit dem Zug gratis?', D.ANREISE_GRATIS['titel'] + ' ' + ' '.join(D.ANREISE_GRATIS['bedingungen']))
    q('Lage', 'Wie weit ist es zum Skigebiet und zum Bus?', ' · '.join(f'{m} Gehminuten: {o} ({t})' for m, o, t in D.LAGE) + '.')
    q('Parkplatz', 'Gibt es einen Parkplatz beim Hotel?', D.PARK + '. Hotelparkplatz inklusive.')
    q('Bergbahnen', 'Sind die Bergbahnen und das Postauto inbegriffen?', D.BERGBAHN_SATZ + ' Laut Preisliste: ' + D.INKLUSIVE[0] + '; ' + D.INKLUSIVE[1] + '.')
    q('Röstihüs', 'Welche Röstis gibt es im Röstihüs?', ' · '.join(f'{n} (Fr. {p})' for n, _, p in D.ROESTIS) + '.')
    q('Röstihüs', 'Welche Cordon bleus gibt es?', ' · '.join(f'{n}: {z} (Fr. {p})' for n, z, p in D.CORDON) + '.')
    q('Röstihüs', 'Wie reserviere ich einen Tisch im Röstihüs?', f'Telefon {D.HAUS["tel"]} oder über TheFork. Die Öffnungszeiten erfahren Sie an der Rezeption.')
    q('Röstihüs', 'Gibt es Raclette?', f'Halbpension: wöchentlicher Racletteabend. Auf der Karte: {D.RACLETTE[0]}, Fr. {D.RACLETTE[1]}.')
    q('Wein', 'Was ist der Hotelwein?', ' · '.join(f'{n}, {h}, {r} {m} Fr. {p}' for n, h, r, m, p in D.HOTELWEINE))
    q('Spa', 'Was kostet das Spa im Partnerhotel?', ' · '.join(f'{p} {t}' for t, p, _ in D.SPA_TARIFE) + '. ' + D.SPA_INKL)
    q('Spa', 'Was bietet das Spa nebenan?', D.SPA_ANGEBOT)
    q('Saastal', 'Was kann man im Sommer im Saastal machen?', D.SOMMER_SATZ)
    q('Kontakt', 'Wie erreiche ich das Hotel?', f'Telefon {D.HAUS["tel"]}, Fax {D.HAUS["fax"]}, {D.HAUS["mail"]}, {D.HAUS["plz_ort"]}.')
    json.dump(dict(stand='Angaben der Seiten des Hauses (Abruf 09.10.2026)', telefon=D.HAUS['tel'], mail=D.HAUS['mail'], eintraege=E), open('assets/js/wissen.json', 'w', encoding='utf-8'), ensure_ascii=False)


def zaehlwerk(text):
    """Mechanisches Zählwerk: jede Ziffer eine Walze 0 bis 9, die auf ihre Zahl rollt."""
    aus = ''
    for i, c in enumerate(text):
        if c.isdigit():
            aus += f'<span class="walze" style="--d:{c};--w:{i}" aria-hidden="true"><span>' + ''.join(f'<i>{n}</i>' for n in range(10)) + '</span></span>'
        else:
            aus += f'<span class="walze-zeichen" aria-hidden="true">{e(c)}</span>'
    return f'<span class="zaehlwerk" role="img" aria-label="{e(text)}">{aus}</span>'


def glas(kl, farbe):
    """Ein Bordeauxglas als feine Linie (1 px Messing); der Wein steigt langsam."""
    kelch = 'M30 8 C24 70 26 132 60 150 C94 132 96 70 90 8'
    return f'''<svg class="glas glas--{kl}" viewBox="0 0 120 300" aria-hidden="true">
      <defs><clipPath id="kelch-{kl}"><path d="{kelch} Z"/></clipPath><linearGradient id="wein-{kl}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{farbe}" stop-opacity=".78"/><stop offset="1" stop-color="#2A0812" stop-opacity=".95"/></linearGradient></defs>
      <g clip-path="url(#kelch-{kl})"><g class="glas__wein"><rect x="0" y="82" width="120" height="80" fill="url(#wein-{kl})"/><rect x="0" y="82" width="120" height="1.2" fill="rgba(255,236,210,.55)"/></g></g>
      <path class="glas__linie" d="{kelch} M60 150 L60 270 M34 286 C44 278 76 278 86 286"/>
      <path class="glas__glanz" d="M40 22 C36 60 37 96 46 122"/>
    </svg>'''


FAMILIENBAND_HAEUSER = [('wellness', 'Wellness & Spa Pirmin Zurbriggen', 'mit dem Loft-Suite Hotel', 'Saas-Almagell', 'Esther und Fabian', 'http://127.0.0.1:8978/haus/Zurbriggen%20Wellnesshotel%20Saas-Almagell/website/index.html', 'fam-wellness'),
                        ('montemoro', 'Hotel Monte-Moro', '', 'Saas-Almagell', 'Esther und Fabian', 'http://127.0.0.1:8978/haus/Zurbriggen%20Hotel%20Monte-Moro%20Saas-Almagell/website/index.html', 'fam-montemoro'),
                        ('zermatt', 'Suitenhotel Zurbriggen', '', 'Zermatt', 'Moni und Pirmin', 'http://127.0.0.1:8978/haus/Zurbriggen%20Suitenhotel%20Zermatt/website/index.html', 'fam-zermatt'),
                        ('chalet', 'Chalet Rustica', '', 'Saas-Almagell', 'Heidi und Damian', None, 'fam-chalet-holidu')]


def familienband(hier='montemoro', bildweg='assets/img/', zeichenweg='assets/zeichen/'):
    """Das Familienband (Vorgabe Familie Zurbriggen/FAMILIEN-FOOTER.md): auf allen drei Häusern gleich in Aufbau, Reihenfolge, Texten, Schrift und Fotos;
    nur die Farben kommen aus dem Haus (--fb-grund, --fb-text, --fb-akzent)."""
    li = ''
    for k, n, zusatz, ort, gast, web, b in FAMILIENBAND_HAEUSER:
        ich = k == hier
        inhalt = (f'<figure><img src="{bildweg}{b}-m.webp" alt="{e(BILDER[b][1])}" width="{MASSE[b][0]}" height="{MASSE[b][1]}" loading="lazy" decoding="async"></figure>'
                  f'<span class="fb__name">{e(n)}</span>{f"<span class=fb__zusatz>{e(zusatz)}</span>" if zusatz else ""}<span class="fb__ort">{e(ort)} · {e(gast)}</span>'
                  + ('<span class="fb__hier">Sie sind hier</span>' if ich else ('<span class="fb__weiter">Zum Haus</span>' if web else '')))
        # ohne Link: das eigene Haus und das Chalet Rustica (auf chalet-rustica.ch steckt ein fremdes Umleitungsskript; Link erst mit dem Einseiter)
        li += f'<li class="fb__haus{" fb__haus--hier" if ich else ""}">' + (f'<a href="{e(web)}">{inhalt}</a>' if web and not ich else f'<div>{inhalt}</div>') + '</li>'
    return f'''<section class="familienband" aria-label="Familie Zurbriggen">
  <a class="fb__kopf" href="http://127.0.0.1:8961/"><img src="{zeichenweg}pinsel-schnee.svg" alt="" width="44" height="41"><span>Familie Zurbriggen · seit 1967</span></a>
  <ul class="fb__haeuser">{li}</ul>
</section>'''


# Form des Bandes seit 26.10.2026: Fassung 1 «Vier Scheiben» (Robert wählte «1» aus Wellness _varianten/fuss-15b), für die Vorlage ohne Hausfarben;
# die Häuser haben je eine eigene assets/css/familienband-scheiben.css mit ihren Farben.
FAMILIENBAND_SCHEIBEN = """/* ---------- Form «Vier Scheiben» (Robert 26.10.2026, Fassung 1 aus Wellness _varianten/fuss-15b): vier hohe Scheiben 2:3 Kante an Kante (6px), aussen gerundet,
   das eigene Haus mit 4px Strich im Akzent unten statt Rahmen; jede Scheibe schwebt deckend herauf (Skript unten), nur transform.
   Grund wie der Fuss des Hauses, damit es eine Fläche ist. ---------- */
.familienband{--fbr:clamp(14px,1.4vw,22px);padding-top:clamp(60px,6vw,96px);padding-bottom:clamp(50px,5vw,80px)}
.familienband .fb__haeuser{gap:6px;max-width:1320px}
.familienband .fb__kopf{max-width:1320px}
.familienband .fb__haus figure{position:relative;aspect-ratio:2/3;margin:0 0 18px;border-radius:0}
.familienband .fb__haus:first-child figure{border-radius:var(--fbr) 0 0 var(--fbr)}
.familienband .fb__haus:last-child figure{border-radius:0 var(--fbr) var(--fbr) 0}
.familienband .fb__haus--hier figure{outline:0}
.familienband .fb__haus--hier figure::after{content:'';position:absolute;left:0;right:0;bottom:0;height:4px;background:var(--fb-akzent)}
.familienband .fb__haus .fb__name,.familienband .fb__haus .fb__zusatz,.familienband .fb__haus .fb__ort,.familienband .fb__haus .fb__hier,.familienband .fb__haus .fb__weiter{padding-right:14px}
.familienband .fb__haus{transform:translate3d(0,110px,0) scale(.96);transition:transform 1.2s cubic-bezier(.22,.61,.36,1) calc(var(--n,0) * 70ms)}
.familienband .fb__haus.da{transform:none}
@media (max-width:800px){
  .familienband .fb__haeuser{grid-template-columns:1fr 1fr;row-gap:30px}
  .familienband .fb__haus figure,.familienband .fb__haus:first-child figure,.familienband .fb__haus:last-child figure{border-radius:var(--fbr)}
}
@media (prefers-reduced-motion:reduce){.familienband .fb__haus{transform:none!important;transition:none!important}}
"""


def familienband_datei():
    """Legt den Block für Wellness und Zermatt neben die Vorgabe (HTML, CSS und Skript der Form «Vier Scheiben», Farben über drei Variablen)."""
    css = open('assets/css/montemoro.css', encoding='utf-8').read()
    i = css.index('/* ---------- Familienband'); j = css.index('/* ---------- Ende Familienband')
    html_ = familienband(hier='montemoro', bildweg='BILDWEG/', zeichenweg='ZEICHENWEG/')
    # gemeinsame Vorlage bleibt beim Foto aus einstieg/site/bilder (19.10.2026: neues Rustica-Foto nur auf Monte-Moro, die anderen Häuser entscheiden selbst)
    html_ = html_.replace('fam-chalet-holidu-m.webp', 'fam-chalet-m.webp').replace(e(BILDER['fam-chalet-holidu'][1]), e(BILDER['fam-chalet'][1])).replace(f'width="{MASSE["fam-chalet-holidu"][0]}" height="{MASSE["fam-chalet-holidu"][1]}"', f'width="{MASSE["fam-chalet"][0]}" height="{MASSE["fam-chalet"][1]}"')
    ziel = os.path.join(HIER, '..', '..', 'Familie Zurbriggen', 'familienband.html')
    open(ziel, 'w', encoding='utf-8').write(
        '<!-- Familienband der Familie Zurbriggen, gebaut von Monte-Moro (18.10.2026) nach FAMILIEN-FOOTER.md.\n'
        '     Form seit 26.10.2026: Fassung 1 «Vier Scheiben» (Robert wählte «1» aus Wellness _varianten/fuss-15b), auf allen drei Häusern gleich.\n'
        '     Reihenfolge im Fuss: Teil des Hauses, darunter dieses Band, ganz unten die Rechtszeile (Designstudie, Impressum, Datenschutz).\n'
        '     Übernehmen: HTML unten einsetzen, BILDWEG und ZEICHENWEG auf die eigenen Ordner setzen (Fotos: einstieg/site/bilder, Zeichen: einstieg/site/zeichen),\n'
        '     «Sie sind hier» auf das eigene Haus setzen (Klasse fb__haus--hier, ohne Link), nur die drei Farben in .familienband ändern.\n'
        '     Schrift: Tenor Sans wie auf der Familienseite (Google Fonts, siehe Link).\n'
        '     Links (Kette-Chat 18.10.2026): Kopf auf die Familienseite http://127.0.0.1:8961/; die Häuser auf die neuen Seiten der Kette:\n'
        + ''.join(f'       {n}: {w}\n' for k, n, z, o, g, w, b in FAMILIENBAND_HAEUSER if w) +
        '       Chalet Rustica: ohne Link und ohne «Zum Haus» (auf chalet-rustica.ch steckt ein fremdes Umleitungsskript), bis der Einseiter steht. -->\n'
        '<link href="https://fonts.googleapis.com/css2?family=Tenor+Sans&display=swap" rel="stylesheet">\n<style>\n' + css[i:j] + FAMILIENBAND_SCHEIBEN + '</style>\n' + html_ + '\n'
        '<script>\n' + open('assets/js/familienband-scheiben.js', encoding='utf-8').read() + '</script>\n')
    return ziel




# ================================================================ Bausteine des Drehbuchs (Master 2.1 Punkt 6c): Kapitel liegen still, Bilder bündig
def hoehenlinien(n=11):
    """Reliefkarte des Saastals als Höhenlinien: weiche, gegeneinander verschobene Wellen, oben der Grat des Logos (Schema, keine Vermessung)."""
    zuege = []
    for i in range(n):
        f = i / max(1, n - 1); pts = []
        for x in range(0, 1001, 10):
            y = 46 + i * 50 + (1 - f * .55) * (26 * math.sin(x / 140 + i * .55) + 14 * math.sin(x / 61 + i * 1.3) + 8 * math.sin(x / 23 + i * 2.1)) + 30 * math.sin(x / 420 + 1.2) * f
            pts.append(f'{x} {y:.1f}')
        zuege.append('M' + ' L'.join(pts))
    grat = 'M' + ' L'.join(f'{float(a):.0f} {float(b) * 1.1 - 8:.1f}' for a, b in (p.split() for p in re.findall(r'(\d+ \d+)', GRAT_LINIE)))
    return f'<path class="relief__grat" d="{grat}"/>' + ''.join(f'<path d="{z}"/>' for z in zuege)



def flug(variante='tal', zeit=False):
    """Flug ins Tal (Robert 18.10.2026: «mit den Fussschritten, mit diesen verschiedenen Zielen, wo man dann reingezoomt ist»):
    erst das Saastal als feine Karte (Schema), beim Scrollen zoomt sie auf Saas-Almagell; dort laufen die Fussspuren zu den Zielen.
    variante 'tal' (Startseite, Kapitel 4): Lift, Bus, Dorf. variante 'anreise' (anreise.html): die Strecke Visp, Stalden, Saas-Grund, Saas-Almagell,
    am Ende zu Fuss von der Busstation bis vor das Haus. Die Bühne bleibt an ihrem Platz; nur die Karte bewegt sich (Regel 55)."""
    hx, hy = 575, 318
    if variante == 'anreise':
        orte = [('Visp', 'Zug bis hier, dann Postauto', 70, 46), ('Stalden', 'Verzweigung Richtung Saastal', 185, 100), ('Saas-Grund', 'umsteigen', 330, 200)]
        tal = 'M70 46 C120 62 160 88 185 100 S290 172 330 200 S480 280 575 318'
        ziele = [(D.LAGE[1], 552, 334)]
        haus_s = 'Ankunft'
        eins = f'''{ueber('Der Weg ins Saastal')}<h2 class="d2">Visp, Stalden, Saas-Grund, <em>Saas-Almagell.</em></h2><p class="leise">{e(D.ANREISE_ZUG_ZEIT.rstrip('.'))}. {e(D.ANREISE_AUTO_ZEIT.rstrip('.'))}.</p>'''
        zwei_kopf = f'''<p class="ueber">Ankunft · zu Fuss laut Haus</p><h2 class="d2">Bis vor <em>das Haus.</em></h2>'''
        liste = [(D.LAGE[1][0], 'Von der Busstation', 'Gehminuten bis zum Hotel Monte-Moro'), ('P', 'Parkplätze', D.PARK)]
    else:
        orte = [('Saas-Fee', 'Skigebiet bis 3500 m', 150, 118), ('Saas-Grund', 'Skigebiet bis 3200 m', 330, 200), ('Mattmark', 'Tagesausflug', 860, 468)]
        tal = 'M60 70 C170 120 250 170 330 200 S480 280 575 318 S760 420 940 500'
        ziele = [(D.LAGE[0], 603, 300), (D.LAGE[1], 552, 334), (D.LAGE[2], 590, 341)]
        haus_s = 'Skigebiet bis 2400 m'
        eins = f'''{ueber('Der Tag im Saastal')}<h2 class="d2">An bester Lage <em>in Saas-Almagell.</em></h2><p class="leise">{e(D.BERGBAHN_SATZ)}</p>'''
        zwei_kopf = f'''<p class="ueber">Ab dem Haus · Gehminuten laut Haus</p><h2 class="d2">Zwei Minuten <em>bis zum Lift.</em></h2>'''
        liste = [(m, o, s) for m, o, s in D.LAGE]
    punkte = ''.join(f'<g class="ort" transform="translate({x} {y})"><rect class="ort__p" x="-3.5" y="-3.5" width="7" height="7"/><text x="{14 if x < 800 else -14}" y="-10" text-anchor="{"start" if x < 800 else "end"}" class="ort__n">{e(n)}</text><text x="{14 if x < 800 else -14}" y="8" text-anchor="{"start" if x < 800 else "end"}" class="ort__s">{e(z)}</text></g>' for n, z, x, y in orte)
    def spur(x0, y0, x1, y1, n, k0):
        aus = []
        for k in range(n):
            t = (k + .5) / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            dx, dy = x1 - x0, y1 - y0; l = math.hypot(dx, dy) or 1; s = .55 if k % 2 else -.55
            aus.append(f'<ellipse cx="{x - dy / l * s:.2f}" cy="{y + dx / l * s:.2f}" rx=".75" ry=".38" transform="rotate({math.degrees(math.atan2(dy, dx)):.0f} {x - dy / l * s:.2f} {y + dx / l * s:.2f})" style="--k:{k0 + k}"/>')
        return ''.join(aus)
    detail, k = '', 0
    for (m, ort, satz), x, y in ziele:
        n = int(m) * 5
        # Robert 24.10.2026: «dafür sorgen, dass die Schriften nicht die Fussstapfen überschneiden» → Name auf der Seite des Ziels, die vom Haus wegzeigt
        anker = f'x="{2.4 if x > hx else -2.4}" y="{3.4 if y > hy else -1.4}" text-anchor="{"start" if x > hx else "end"}"'
        a0, b0, a1, b1 = (x, y, hx, hy) if variante == 'anreise' else (hx, hy, x, y)
        detail += spur(a0, b0, a1, b1, n, k) + f'<g class="ziel" transform="translate({x} {y})"><rect x="-1.1" y="-1.1" width="2.2" height="2.2"/><text {anker}>{e(ort)}</text></g>'
        k += n
    minuten = ''.join(f'<li><b>{e(m)}</b><span><strong>{e(o)}</strong><small>{e(s)}</small></span></li>' for m, o, s in liste)
    strecke = f'<path class="tal tal--strecke" d="{tal}"/>' if variante == 'anreise' else f'<path class="tal" d="{tal}"/>'
    karte = f'''<g class="relief__linien">{hoehenlinien()}</g>{strecke}{punkte}
        <g class="flug__detail">{detail}<g class="haus-ort" transform="translate({hx} {hy})"><rect x="-1.6" y="-1.6" width="3.2" height="3.2"/><text x="-2.6" y="-2" text-anchor="end">Hotel Monte-Moro</text></g></g>
        <g class="ort ort--haus" transform="translate({hx} {hy})"><rect class="ort__p" x="-5" y="-5" width="10" height="10"/><text x="16" y="-10" class="ort__n">Saas-Almagell</text><text x="16" y="8" class="ort__s">{e(haus_s)}</text></g>'''
    if zeit:
        # Robert 18.10.2026 13:23: «deutlich spektakulärer und schöner animiert». Nicht mehr am Scrollen: die Karte kommt als Platte von unten,
        # dann fliegt die Kamera von selbst nach Saas-Almagell (bremst auf drei Vierteln), und die Fussspuren laufen zu Lift, Bus und Dorf.
        zeilen = ''.join(f'<li data-steig><b>{e(m)}</b><span><strong>{e(o)}</strong><small>{e(s_)}</small></span></li>' for m, o, s_ in liste)
        return f'''<div class="lift">
      <div class="lift__kopf">{zwei_kopf.replace('<p class="ueber">', '<p class="ueber" data-steig>').replace('<h2 class="d2">', '<h2 class="d2" data-zeilen>')}</div>
      <div class="lift__platte" data-lift>
        <svg class="flug lift__karte" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g data-flugkarte>{karte}</g></svg>
        <p class="lift__schema">Das Saastal · Schema, nicht massstäblich</p>
      </div>
      <div class="lift__rechts">{ebene('haus-winter-g', 'lift__foto', None, 'satt', lage='50% 40%', s='(max-width:900px) 92vw, 30vw')}<ol class="flug__minuten lift__minuten">{zeilen}</ol></div>
    </div>'''
    return f'''<div class="flug__wrap" data-flug>
    <div class="flug__buehne">
      <svg class="flug" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g data-flugkarte>
        <g class="relief__linien">{hoehenlinien()}</g>{strecke}{punkte}
        <g class="flug__detail">{detail}<g class="haus-ort" transform="translate({hx} {hy})"><rect x="-1.6" y="-1.6" width="3.2" height="3.2"/><text x="-2.6" y="-2" text-anchor="end">Hotel Monte-Moro</text></g></g>
        <g class="ort ort--haus" transform="translate({hx} {hy})"><rect class="ort__p" x="-5" y="-5" width="10" height="10"/><text x="16" y="-10" class="ort__n">Saas-Almagell</text><text x="16" y="8" class="ort__s">{e(haus_s)}</text></g>
      </g></svg>
      <div class="flug__text flug__text--1" data-flugeins>{eins}</div>
      <div class="flug__text flug__text--2" data-flugzwei>{zwei_kopf}<ol class="flug__minuten">{minuten}</ol></div>
      <p class="flug__schema">Das Saastal · Schema, nicht massstäblich</p>
    </div>
  </div>'''


def fallblatt(text, n):
    """Fallblatt-Zeile: jedes Zeichen in seinem Blatt, von Anfang an lesbar; beim Erscheinen klappt jedes Blatt einmal kurz (anreise.html)."""
    t = text.upper().ljust(n)[:n]
    return f'<span class="fb" role="img" aria-label="{e(text)}">' + ''.join(f'<i aria-hidden="true"><b>{e(c) if c != " " else "&nbsp;"}</b></i>' for c in t) + '</span>'


def abfahrtstafel():
    ag = D.ANREISE_GRATIS
    reihen = [('Zug', 'Visp – Saas-Almagell', 'ca. 45 Min.', ''), ('Auto', 'Visp – Saas-Almagell', 'ca. 40 Min.', ''),
              ('Gratis', 'ÖV ab 2 Nächten', 'geschenkt', ag['bis']), ('Ankunft', 'Hotel Monte-Moro', '957 10 12', '')]
    zeilen = ''.join(f'<li{f" data-bis={chr(34)}{b}{chr(34)}" if b else ""} style="--r:{i}"><span class="tafel__art">{e(a)}</span>{fallblatt(z, 20)}{fallblatt(t, 11)}</li>' for i, (a, z, t, b) in enumerate(reihen))
    return f'<div class="tafel" data-tafel><p class="tafel__kopf"><span>Mit</span><span>Strecke</span><span>Dauer</span></p><ol>{zeilen}</ol></div>'


def ebene(key, kl, tiefe, art='', lage='50% 50%', s='(max-width:900px) 90vw, 50vw', laden=False):
    """Ein Foto als Ebene einer Komposition (Master 2.1 Punkt 6d): die Ebene wandert beim Scrollen mit ihrem Faktor (Drift, Gegenlauf),
    der Rahmen schwebt herein (Hochschweben oder edel von rechts), das Foto zoomt in seinen Rahmen und gleitet darin (tiefe.js)."""
    l = '<i class="laden laden--l" aria-hidden="true"></i><i class="laden laden--r" aria-hidden="true"></i>' if laden else ''
    t = f' data-tiefe="{tiefe}"' if tiefe is not None else ''
    return (f'<div class="eb {kl}"{t}><figure class="fo" data-r="{art}"{" data-laden" if laden else ""}>'
            f'{bild(key, sizes=s, lage=lage)}{l}</figure></div>')


def zahl(wert, wort, vor='', nach=''):
    """Grosse Zahl, die beim Erscheinen hochzählt; steht ohne Skript schon richtig da."""
    return f'<p class="zahl" data-steig><b>{e(vor)}<i data-zahl="{e(wert)}">{e(wert)}</i>{e(nach)}</b><span>{e(wort)}</span></p>'


def kapitel(id_, kl, inhalt, aria, weiter=None, grat=True, knopf=None):
    """Ein Kapitel des Tages. Liegt still an seinem Platz; die Grenze zum vorigen ist der Grat des Logos als feine Linie.
    weiter = (Satz, Ziel, Linktext) leitet zum nächsten Kapitel über."""
    w = ''
    if weiter:
        satz, ziel, text = weiter
        # Robert 24.10.2026: Überleitungen «überall mittig statt linksbündig», «wenn da so ein Button ist, dann den Button darunter mittig»
        w = (f'<div class="weiter-block"><p class="weiter" data-s><span>{e(satz)}</span></p>'
             + (f'<p class="weiter__link" data-s><a href="{e(ziel)}">{e(text)}</a></p>' if ziel else '')
             + (f'<div class="weiter__knopf" data-s>{knopf}</div>' if knopf else '') + '</div>')
    return (f'<section class="kapitel {kl}" id="{id_}" aria-label="{e(aria)}">{grat_oben() if grat else ""}'
            f'<div class="kapitel__innen">{inhalt}{w}</div></section>')


def paar(a, b, kl='', la='50% 50%', lb='50% 50%', s='(max-width:900px) 100vw, 50vw'):
    """Zwei grosse Fotos bündig nebeneinander, ohne Lücke."""
    return (f'<div class="paar {kl}" data-bilder><figure>{bild(a, sizes=s, lage=la)}<figcaption>{e(BILDER[a][1])}</figcaption></figure>'
            f'<figure>{bild(b, sizes=s, lage=lb)}<figcaption>{e(BILDER[b][1])}</figcaption></figure></div>')


def rahmen(gross, klein1, klein2, kl='', lagen=('50% 50%', '50% 50%', '50% 50%')):
    """Ein Rahmen mit drei Bildern, bündig: eines gross, zwei übereinander daneben (Robert: wie der erste Abschnitt beim Ruedihus)."""
    return (f'<div class="rahmen {kl}" data-bilder><figure class="rahmen__gross">{bild(gross, sizes="(max-width:900px) 100vw, 62vw", lage=lagen[0])}<figcaption>{e(BILDER[gross][1])}</figcaption></figure>'
            f'<figure>{bild(klein1, sizes="(max-width:900px) 50vw, 32vw", lage=lagen[1])}<figcaption>{e(BILDER[klein1][1])}</figcaption></figure>'
            f'<figure>{bild(klein2, sizes="(max-width:900px) 50vw, 32vw", lage=lagen[2])}<figcaption>{e(BILDER[klein2][1])}</figcaption></figure></div>')


def einzel(k, kl='', lage='50% 50%', s='(max-width:900px) 100vw, 60vw'):
    return f'<figure class="einzel {kl}" data-bilder>{bild(k, sizes=s, lage=lage)}<figcaption>{e(BILDER[k][1])}</figcaption></figure>'


def anfrage(text, betreff, kl='kn--linie', art='', mail_betreff=None):
    """Anfrage im Fenster auf der Seite (Regel «Anfragen im Fenster, nie mailto»); der mailto-Verweis bleibt nur für Besucher ohne Skript."""
    b = mail_betreff or betreff
    return f'<a class="kn {kl}" href="mailto:{D.HAUS["mail"]}?subject={e(b)}" data-anfrage="{e(betreff)}"{f" data-art={chr(34)}{art}{chr(34)}" if art else ""}><span>{e(text)}</span><i>{PF}</i></a>'


def spuren_zeile(n, k0=0):
    return ''.join(f'<i style="--k:{k0 + k}"></i>' for k in range(n))


def bon_html():
    worte = [('Postauto', D.INKLUSIVE[0]), ('Bergbahnen', D.INKLUSIVE[1]), ('Frühstück', D.INKLUSIVE[2]), ('Raclette', D.INKLUSIVE[3]), ('Kidsclub', D.INKLUSIVE[4]), ('Parkplatz', D.INKLUSIVE[5])]
    zeilen = ''.join(f'<li><span><b>{e(w)}</b><small>{e(t)}</small></span><em>inkl.</em></li>' for w, t in worte)
    return f'''<div class="bon__drucker" data-bon>
      <p class="bon__theke" aria-hidden="true"><span>Rezeption</span></p>
      <div class="bon__fach"><div class="bon__papier">
        <p class="bon__kopf">{kamm('bon__kamm')}<b>Hotel Monte-Moro</b><span>{e(D.HAUS['plz_ort'])}</span><span>Tel. {e(D.HAUS['tel'])}</span></p>
        <p class="bon__titel"><span>Ihr Aufenthalt</span><span>CHF</span></p><p class="bon__trenn" aria-hidden="true"></p>
        <ul class="bon__zeilen">{zeilen}</ul><p class="bon__trenn" aria-hidden="true"></p>
        <p class="bon__summe"><span>Total</span><b>inklusive</b></p><p class="bon__dank">Mehr erleben, weniger zahlen.</p>
        <svg class="bon__abriss" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{GRAT}"/></svg>
      </div></div>
    </div>'''


def karte_heft(alle=False):
    """Die Karte des Röstihüs als aufgeschlagenes Heft (Speisekarte vom 18.11.2024)."""
    namen = ''.join(f'<li><span>{e(n)}</span><i aria-hidden="true"></i><em>{e(p)}</em><small>{e(z)}</small></li>' for n, z, p in D.ROESTIS)
    cordon = ''.join(f'<li><span>{e(n)}</span><i aria-hidden="true"></i><em>{e(p)}</em><small>{e(z)}</small></li>' for n, z, p in D.CORDON)
    links = f'''<p class="buch__kopf">Röstihüs · Saas-Almagell</p><p class="buch__titel">Unsere Cordon bleus</p><ul class="buch__namen">{cordon}</ul>
        <p class="buch__titel buch__titel--klein">Zum Dessert</p><ul class="buch__namen"><li><span>{e(D.KOPF[0].split(' (')[0])}</span><i aria-hidden="true"></i><em>{e(D.KOPF[1])}</em><small>{e(D.KOPF[0].split(' (', 1)[1].rstrip(')'))}</small></li></ul>
        <p class="buch__titel buch__titel--klein">Im Stübli</p><ul class="buch__namen"><li><span>{e(D.RACLETTE[0].split(' mit ')[0])}</span><i aria-hidden="true"></i><em>{e(D.RACLETTE[1])}</em><small>mit {e(D.RACLETTE[0].split(' mit ', 1)[1])}</small></li></ul>'''
    # 23.10.2026: Gerichtnamen brechen nie um, Zusatz in die kleine Zeile (Wortlaut bleibt)
    if alle:
        weine = ''.join(f'<li><span>{e(n.replace("«Hotelwein» ", "Hotelwein · "))}</span><i aria-hidden="true"></i><em>{e(p)}</em><small>{e(h)} · {e(r)} · {e(m)}</small></li>' for n, h, r, m, p in D.HOTELWEINE)
        spritz = ''.join(f'<li><span>{e(n)}</span><i aria-hidden="true"></i><em>{e(p)}</em><small>{e(z)}</small></li>' for n, z, p in D.SPRITZ)
        links += f'<p class="buch__titel buch__titel--klein">Wein von Fabian</p><ul class="buch__namen">{weine}</ul><p class="buch__titel buch__titel--klein">Zum Apéro</p><ul class="buch__namen">{spritz}</ul>'
    return f'''<div class="buch" data-buch>
      <div class="buch__seite buch__seite--l">{links}</div>
      <div class="buch__seite buch__seite--r"><p class="buch__kopf">Karte vom 18.11.2024 · Fr.</p><p class="buch__titel">Best of Röstis</p><ul class="buch__namen">{namen}</ul></div>
    </div>'''


def seitenkopf(id_, ueber_, titel_, em, satz, bildkey, lage='50% 50%'):
    """Anfang einer Unterseite: ein grosses Foto, Titel und ein Satz, mit dem das kleine Kapitel beginnt."""
    return f'''<section class="seitenkopf" id="{id_}">
  <figure class="seitenkopf__bild">{bild(bildkey, sizes='100vw', vorn=True, lage=lage)}</figure>
  <div class="seitenkopf__text">{ueber(ueber_)}{titel(titel_, em=em, kl='d1', tag='h1')}<p class="leise" data-s>{e(satz)}</p></div>
</section>'''


# ================================================================ die Startseite: ein Tag in acht Kapiteln (DREHBUCH.md)
def k1_morgen():
    """Auftakt: die Sonne geht hinter dem Grat auf, das Haus steigt herauf, Himmel, Grat, Haus und Titel laufen beim Scrollen gegeneinander.
    Darunter die Gastgeber: der Empfang und das Dorf als zwei Ebenen, die Note des Personals zählt hoch."""
    noten = {n: w for n, w, v, c in D.NOTEN}
    return f'''<section class="kapitel k-morgen" id="morgen" aria-label="Morgen über Saas-Almagell">
  <div class="auf__buehne" data-auf>
    <div class="auf__himmel" aria-hidden="true" data-lauf=".55"><i class="auf__frueh"></i><i class="auf__tag"></i></div>
    <div class="auf__sonne" aria-hidden="true" data-lauf=".42"><i></i></div>
    <svg class="auf__grat auf__grat--fern" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true" data-lauf=".34"><path d="{GRAT_LINIE}"/></svg>
    <svg class="auf__grat auf__grat--nah" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true" data-lauf=".24"><path d="{GRAT_LINIE}"/></svg>
    <div class="auf__hauswrap" data-lauf=".1"><img class="auf__haus" src="assets/img/haus-frei-m.webp" srcset="assets/img/haus-frei-s.webp 900w, assets/img/haus-frei-m.webp 1440w, assets/img/haus-frei-l.webp 2400w" sizes="(max-width:700px) 180vw, 100vw" width="2400" height="1573" alt="Das Hotel Monte-Moro mit den Balkonen aus Lärche" fetchpriority="high" decoding="async"></div>
    <div class="auf__kopf" data-lauf="-.22">
      <p class="ueber">Hotel Monte-Moro · Saas-Almagell · Wallis</p>
      {titel('Bei uns scheint fast immer die Sonne.', em='die Sonne.', kl='d1', tag='h1')}
    </div>
    <div class="auf__fuss">{buchen_form()}</div>
  </div>
  <div class="gast">
    <div class="gast__text">
      <p class="ueber" data-steig>Ihre Gastgeber</p>
      {titel('Esther und Fabian Zurbriggen.', em='Zurbriggen.')}
      <p class="gast__satz" data-steig>Willkommen im Hotel Monte-Moro in Saas-Almagell. Das Hotel befindet sich an bester Lage: zwei Gehminuten zum Skigebiet, drei zur Busstation und drei ins Dorf.</p>
      <p class="gast__satz" data-steig>Bei schönem Wetter (bei uns scheint fast immer die Sonne) geniessen Sie unsere Sonnenterrasse direkt vor dem Haus. Und im hauseigenen Restaurant Röstihüs regionale und authentische Küche.</p>
      {zahl(noten['Personal'], 'Personal · Booking.com')}
    </div>
    <div class="gast__bilder komp">
      {ebene('empfang', 'gast__a', '.32', lage='40% 50%', s='(max-width:900px) 92vw, 46vw')}
      {ebene('tal-dorf', 'gast__b', '-.5', 'rechts', s='(max-width:900px) 56vw, 24vw')}
      {ebene('alpenrosen', 'gast__c', '.5', s='(max-width:900px) 40vw, 18vw')}
    </div>
  </div>
  <p class="auf__weiter" data-steig><span>Die Sonne steht schon über dem Balkon.</span></p>
</section>'''


def k2_zimmer():
    """Kapitel 2: das Zimmer, das sich öffnet. Zwei Läden aus Lärche gehen mit dem Scrollen auf; Balkon und Morgenlicht als Ebenen darüber, gegenläufig."""
    return kapitel('zimmer', 'k-zimmer', f'''
    <div class="zim">
      <div class="zim__kopf">{ueber('Aufwachen im Zimmer')}{titel('Schöne Hotelzimmer - schöne Ferien.', em='schöne Ferien.')}</div>
      <div class="zim__zahlen">{zahl('18', 'Zimmer')}{zahl('55', 'Betten')}</div>
      <div class="zim__bilder komp">
        {ebene('z-dach', 'zim__a', '.16', lage='50% 55%', s='(max-width:900px) 96vw, 60vw')}
        {ebene('z-licht', 'zim__c', '.62', 'rechts', s='(max-width:900px) 50vw, 30vw')}
        {ebene('balkon', 'zim__b', '-.46', lage='50% 60%', s='(max-width:900px) 60vw, 34vw')}
        {ebene('z-gelb', 'zim__d', '.34', s='(max-width:900px) 48vw, 26vw')}
        {ebene('z-wanne', 'zim__e', '-.3', 'rechts', s='(max-width:900px) 40vw, 20vw')}
      </div>
      <div class="zim__text">
        <p data-steig>{e(D.ZIMMER_TEXT)}</p>
        <p data-steig>{e(D.FAMILIE_TEXT)} {e(D.ALPENHOF_TEXT)} Dazu die Ferienwohnungen in den Häusern Apollo und Arizona.</p>
        <div class="kn-reihe" data-steig>{kn('Alle Zimmer und Ferienwohnungen', 'zimmer.html', 'kn--nacht')}</div>
      </div>
    </div>''', 'Aufwachen im Zimmer', weiter=('Unten ist das Frühstück gedeckt, und auf dem Bon steht schon alles.', None, None))


def k3_bon():
    """Kapitel 3: das Frühstück als zwei Ebenen, der Bon fliegt von rechts herein und landet schräg darauf; die Stempel «inkl.» setzen nacheinander auf,
    der Preis zählt hoch."""
    pr = {p[0] + p[1]: p[2] for p in D.PREISE}
    ag = D.ANREISE_GRATIS
    ab = pr['BudgetzimmerZimmer mit Frühstück']
    return kapitel('inbegriffen', 'k-bon', f'''
    <div class="bon2">
      <div class="bon2__kopf">{ueber('Frühstück und der Bon')}{titel('Mehr erleben, weniger zahlen.', em='weniger zahlen.')}</div>
      <div class="bon2__bilder komp">
        {ebene('fr-gross', 'bon2__a', None, 'satt', lage='50% 55%', s='(max-width:900px) 96vw, 42vw')}
        {ebene('speiseraum', 'bon2__b', None, 'satt', s='(max-width:900px) 60vw, 26vw')}
        {ebene('fr-detail', 'bon2__c', None, 'satt', s='(max-width:900px) 48vw, 22vw')}
        <div class="eb bon2__flug">{bon_flug()}</div>
      </div>
      <div class="drei">
        <div class="drei__s" data-steig><p class="drei__k">Zimmer mit Frühstück</p><p class="drei__z">ab CHF <i data-zahl="{ab.split('.')[0]}">{ab.split('.')[0]}</i>.{ab.split('.')[1]}</p><p class="drei__t">pro Person und Tag</p></div>
        <div class="drei__s" data-steig><p class="drei__k">Ab der 1. Übernachtung</p><p class="drei__z">inklusive</p><p class="drei__t">Bergbahnen und Postautos im Sommer und Herbst</p></div>
        <div class="drei__s" data-steig data-bis="{ag['bis']}"><p class="drei__k">Ab 2 Nächten</p><p class="drei__z">geschenkt</p><p class="drei__t">An- und Abreise mit dem öffentlichen Verkehr</p></div>
      </div>
      <p class="drei__bed" data-bis="{ag['bis']}" data-steig>{' · '.join(e(x.rstrip('.')) for x in ag['bedingungen'])}</p>
      <div class="kn-reihe kn-reihe--mitte" data-steig>{kn('Preise und gut zu wissen', 'preise.html', 'kn--linie')}</div>
    </div>''', 'Frühstück und der Bon', weiter=('Mit dem Bon in der Tasche sind es zwei Minuten bis zum Lift.', None, None))


def bon_flug():
    """Der Bon allein, ohne Drucker: fliegt herein (tiefe.js setzt .da), die Stempel setzen nacheinander auf."""
    worte = [('Postauto', D.INKLUSIVE[0]), ('Bergbahnen', D.INKLUSIVE[1]), ('Frühstück', D.INKLUSIVE[2]), ('Raclette', D.INKLUSIVE[3]), ('Kidsclub', D.INKLUSIVE[4]), ('Parkplatz', D.INKLUSIVE[5])]
    tipp = lambda w: ''.join(f'<i style="--c:{k}">{e(z)}</i>' for k, z in enumerate(w))  # Robert 20.10.2026 17:25: nicht aufstempeln, sondern ausfüllen
    zeilen = ''.join(f'<li><span><b>{e(w)}</b><small>{e(t)}</small></span><em style="--n:{i}" aria-label="inkl.">{tipp("inkl.")}</em></li>' for i, (w, t) in enumerate(worte))
    return f'''<div class="bon__papier bon__papier--flug" data-bonflug>
        <p class="bon__kopf">{kamm('bon__kamm')}<b>Hotel Monte-Moro</b><span>{e(D.HAUS['plz_ort'])}</span><span>Tel. {e(D.HAUS['tel'])}</span></p>
        <p class="bon__titel"><span>Ihr Aufenthalt</span><span>CHF</span></p><p class="bon__trenn" aria-hidden="true"></p>
        <ul class="bon__zeilen">{zeilen}</ul><p class="bon__trenn" aria-hidden="true"></p>
        <p class="bon__summe"><span>Total</span><b style="--n:6" aria-label="inklusive">{tipp("inklusive")}</b></p><p class="bon__dank">Mehr erleben, weniger zahlen.</p>
        <svg class="bon__abriss" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{GRAT}"/></svg>
      </div>'''


def k4_saastal():
    """Kapitel 4: zuerst der Flug ins Tal mit den Fussspuren zu Lift, Bus und Dorf; danach das Tal in drei Ebenen, gegenläufig, und drei Zahlen, die zählen."""
    w = D.SAASTAL['winter'][0]
    return kapitel('saastal', 'k-saastal', f'''
    {flug('tal', zeit=True)}
    <div class="tal">
      <div class="tal__bilder komp">
        {ebene('tal-sommer', 'tal__a', '.22', s='(max-width:900px) 96vw, 64vw')}
        {ebene('dorf-winter', 'tal__b', '-.5', 'rechts', lage='50% 60%', s='(max-width:900px) 60vw, 40vw')}
        {ebene('stausee', 'tal__c', '.66', s='(max-width:900px) 64vw, 36vw')}
        {ebene('skitour-hang', 'tal__d', '-.28', 'rechts', s='(max-width:900px) 46vw, 24vw')}
        {ebene('bergbach', 'tal__e', '.4', s='(max-width:900px) 40vw, 22vw')}
      </div>
      <div class="tal__zahlen">{zahl('250', 'Wanderwege im Sommer', 'über ', ' km')}{zahl('3500', 'Skifahren bis Saas-Fee', '', ' m')}{zahl(D.LAGE[0][0], 'zum Skigebiet Saas-Almagell', '', ' Min.')}</div>
      <div class="tal__text">
        <p data-steig>{e(D.SOMMER_SATZ.split(';')[0])}. Im Winter: {e(w[2])}.</p>
        <p data-steig>{e(D.INKLUSIVE[0])}. {e(D.LAGE[1][2])}.</p>
      </div>
    </div>''', 'Der Tag im Saastal', weiter=('Nach dem Lift: das Spa nebenan.', None, None), knopf=kn('Sommer und Winter im Saastal', 'saastal.html', 'kn--linie'))


def k5_spa():
    return kapitel('spa', 'k-spa', f'''
    <div class="kap__kopf">{ueber(D.SPA_TITEL)}{titel('Nach dem Lift: das Spa nebenan.', em='das Spa nebenan.')}</div>
    <div class="spa5__bilder komp">
      {ebene('spa-licht', 'spa5__a', None, 'satt', s='(max-width:900px) 92vw, 58vw')}
      {ebene('spa-holz', 'spa5__b', None, 'satt', s='(max-width:900px) 56vw, 30vw')}
      {ebene('f-wellness', 'spa5__c', None, 'satt', lage='50% 60%', s='(max-width:900px) 48vw, 24vw')}
      {ebene('spa-massage', 'spa5__d', None, 'satt', lage='50% 45%', s='(max-width:900px) 48vw, 26vw')}
    </div>
    <div class="spa5__zahlen">{zahl('1700', 'Spa im Sommer', '', ' m²')}{zahl('25', 'pro Person und Eintritt', 'CHF ', '.00')}{zahl('150', '7 Tage Abo pro Person', 'CHF ', '.00')}</div>
    <div class="mitte">
      <p data-s>{e(D.SPA_SATZ)}</p>
      <p class="mitte__leise" data-s>{e(D.SPA_INKL)}</p>
      <div class="kn-reihe" data-s>{kn('Das Spa nebenan', 'spa.html', 'kn--nacht')}</div>
    </div>''', 'Das Spa nebenan', weiter=('Am Abend leuchten vor dem Röstihüs die alten Gondeln.', None, None))


def k6_roestihues():
    return kapitel('roestihues', 'k-roesti', f'''
    <div class="kap__kopf">{ueber('Abend im Röstihüs')}{titel(D.TRADITION, em='die Tradition!')}</div>
    <div class="roe6__bilder komp">
      {ebene('gondel', 'roe6__a', None, 'satt', lage='50% 45%', s='(max-width:900px) 92vw, 50vw')}
      {ebene('roesti-raum', 'roe6__b', None, 'satt', s='(max-width:900px) 60vw, 34vw')}
      {ebene('roesti-orange', 'roe6__c', None, 'satt', s='(max-width:900px) 50vw, 26vw')}
      {ebene('roesti-tische', 'roe6__d', None, 'satt', s='(max-width:900px) 46vw, 22vw')}
    </div>
    <div class="kap__text"><p data-s>{e(D.ROESTI_SATZ)} {e(D.ROESTI_GETRAENKE.split('.')[1].strip())}.</p></div>
    {karte_heft()}
    <div class="kn-reihe kn-reihe--mitte" data-s>{anfrage('Tisch reservieren', 'Tisch im Röstihüs', 'kn--laerche', 'tisch')}{kn('Das Röstihüs und die ganze Karte', 'roestihues.html', 'kn--linie')}</div>''',
                   'Abend im Röstihüs', weiter=('Bis 21 Uhr ist der Kidsclub offen.', None, None))


def k7_kinder():
    """Kapitel 7 (Robert 18.10.2026: Bild und alles darunter «unspektakulär»): die Uhr bleibt; links drei Fotos des Hauses in Ebenen
    (Rodelbahn, Murmeltiere, Spielburg), die von unten an ihren Platz kommen; darunter die Kinderpreise als eine ruhige Zeile."""
    kinder = ''.join(f'<li><span>{e(a)}</span><b>{zaehlwerk(p_.split(".")[0])}<small>.{e(p_.split(".")[1])}</small></b></li>' for a, p_ in D.KINDER)
    return kapitel('kinder', 'k-kinder', f'''
    <div class="kinder__bilder komp">
      {ebene('kinder-rodel', 'kinder__a', None, 'satt', lage='50% 45%', s='(max-width:900px) 92vw, 46vw')}
      {ebene('murmeli', 'kinder__b', None, 'satt', lage='64% 50%', s='(max-width:900px) 56vw, 24vw')}
      {ebene('spielburg', 'kinder__c', None, 'satt', lage='50% 60%', s='(max-width:900px) 40vw, 18vw')}
    </div>
    <div class="kinder__text">
      {ueber('Die Kinder bis 21 Uhr · Kidsclub täglich Mo - Sa · inklusive')}
      <p class="kind__zeit" data-zaehl>{zaehlwerk('16:30')}<span class="kind__bis">bis</span>{zaehlwerk('21:00')}</p>
      <p class="kinder__satz" data-steig>{e(D.FAMILIE_TEXT)} {e(D.ROESTI_KINDER)}</p>
      <div class="kn-reihe" data-steig>{anfrage('Familienzimmer anfragen', 'Familienzimmer', 'kn--nacht')}{kn('Kinderpreise', 'preise.html#kinder', 'kn--linie')}</div>
    </div>
    <div class="kinder__preise" data-steig>
      <p class="ueber">{e(D.KINDER_SATZ)} · CHF</p>
      <ul class="zw-preise" data-zaehl>{kinder}</ul>
    </div>''', 'Die Kinder', weiter=('Später, im Stübli, steht der Wein auf dem Tisch, den Fabian selbst kreiert hat.', None, None))


def k8_wein():
    def karte(i, w, kl):
        n, h, r, m, p = w
        return f'<div class="wein wein--{kl}" style="--w:{i}">{glas(kl, "#6E1B2C" if i == 0 else "#7E2433")}<div class="wein__etikett"><p class="ueber">{"Prestige Silber" if i == 0 else "Prestige Gold"}</p><p class="wein__name">{e(n.replace("«Hotelwein» ", ""))}</p><p class="wein__h">{e(h)}</p><p class="wein__r">{e(r)} · {e(m)}</p><p class="wein__p">Fr. {e(p)}</p></div></div>'
    spritz = D.SPRITZ[0]
    return kapitel('wein', 'k-wein', f'''
    <div class="wein__bilder komp">
      {ebene('stuebli', 'wein__a', None, 'satt', lage='70% 50%', s='(max-width:900px) 84vw, 34vw')}
      {ebene('dorf-nacht', 'wein__c', None, 'satt', lage='50% 55%', s='(max-width:900px) 44vw, 20vw')}
      {ebene('raclette', 'wein__b', None, 'satt', lage='92% 50%', s='(max-width:900px) 50vw, 22vw')}
    </div>
    <div class="wein__rechts">
      {ueber('Der Wein von Fabian · Raclettestübli')}
      {titel('Wein von Fabian.', em='Fabian.')}
      <div class="wein__glaeser" data-glaeser>{karte(0, D.HOTELWEINE[0], 'silber')}{karte(1, D.HOTELWEINE[1], 'gold')}</div>
      <p class="wein__mehr" data-s>Halbpension: wöchentlicher Racletteabend im Stübli. Zum Apéro: {e(spritz[0])} ({e(spritz[1])}).</p>
    </div>''', 'Der Wein von Fabian')


def schluss():
    return f'''<section class="schluss" id="morgen-wieder" aria-label="Buchen und Anreise">{grat_oben()}
  <div class="schluss__innen">
    <figure class="schluss__bild" data-bilder>{bild('wolkenmeer-echt', sizes='(max-width:900px) 390vw, 100vw', lage='50% 42%')}
      <figcaption>{e(BILDER['wolkenmeer-echt'][1])}</figcaption>
      <p class="schluss__satz" data-zeilen>Und morgen scheint <em>die Sonne wieder.</em></p>
      <div class="schluss__unten">
        <div class="schluss__leiste">{buchen_form('leiste--nacht')}</div>
        <p class="schluss__anreise"><span><b>{e(D.ANREISE_ZUG_ZEIT.split('ca. ')[1])}</b> mit Zug und Postauto ab Visp</span><span><b>{e(D.ANREISE_AUTO_ZEIT.split('ca. ')[1])}</b> mit dem Auto ab Visp</span><a href="anreise.html">Anreise</a></p>
      </div></figure>
  </div>
</section>'''


def startseite():
    teile = [k1_morgen(), k2_zimmer(), k3_bon(), k4_saastal(), k5_spa(), k6_roestihues(), k7_kinder(), k8_wein(), schluss()]
    return (kopf('Hotel Monte-Moro · Saas-Almagell', 'Ein Tag im Hotel Monte-Moro in Saas-Almagell: Sonne am Morgen, Bergbahnen und Postautos inklusive, das Spa nebenan, Rösti im Röstihüs und der Wein von Fabian.')
            + '\n'.join(teile) + fuss())


# ================================================================ die Unterseiten, je ein kleines Kapitel mit Anfang und Ende
def kopf_tag(id_, ueber_, titel_, em, satz, bildkey, lage='50% 50%', abend=False):
    """Kopf der Unterseiten (Plan 19.10.2026, Robert «ja»): dieselbe Sprache wie der abgenommene Auftakt der Startseite. Himmel der Tageszeit,
    Zeichen in Gold, Titel gross in der Mitte, darunter das Foto in voller Farbe bis an die Unterkante des ersten Bildschirms."""
    return f'''<section class="sk2{" sk2--abend" if abend else ""}" id="{id_}">
  <div class="sk2__kopf">{kamm('sk2__kamm')}{ueber(ueber_)}{titel(titel_, em=em, kl='d1', tag='h1')}<p class="sk2__satz" data-s>{e(satz)}</p></div>
  <figure class="sk2__bild">{bild(bildkey, sizes='100vw', vorn=True, lage=lage)}</figure>
</section>'''


def galerie(id_, titel_, keys):
    """Alle Ansichten im Fenster (galerie.js); die Fotos liegen gehalten im Template und laden erst beim Öffnen."""
    figs = ''.join(f'<figure>{bild(k, sizes="(max-width:700px) 92vw, 30vw")}<figcaption>{e(BILDER[k][1])}</figcaption></figure>' for k in keys)
    return f'<template id="gal-{id_}" data-titel="{e(titel_)}">{figs}</template>'


def zimmeransicht(id_, titel_, keys, steck):
    """Zimmeransicht (Robert 24.10.2026: «statt alle Ansichten für jedes Zimmer noch eine Zimmeransicht … mit allen Infos die uns vorliegen»):
    über den ganzen Bildschirm, links alle Fotos dieser Zimmerart, rechts fest der Steckbrief. Fotos und Text liegen im Template und laden erst beim Öffnen
    (assets/js/zimmeransicht.js)."""
    figs = ''.join(f'<figure>{bild(k, sizes="(max-width:900px) 92vw, 58vw")}<figcaption>{e(BILDER[k][1])}</figcaption></figure>' for k in keys)
    return f'<template id="zi-{id_}" data-titel="{e(titel_)}"><div class="zi__bilder">{figs}</div><aside class="zi__steck">{steck}</aside></template>'


def steckbrief(teile, knoepfe):
    """teile: [(Titel, Inhalt)], Inhalt ist Text, eine Liste von Wörtern oder eine Liste von (Angabe, Wert)."""
    h = ''
    for t, inh in teile:
        if isinstance(inh, str):
            k = f'<p class="zi__satz">{e(inh)}</p>'
        elif inh and isinstance(inh[0], tuple):
            k = '<dl class="zi__zeilen">' + ''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in inh) + '</dl>'
        else:
            k = '<ul class="zi__liste">' + ''.join(f'<li>{e(x)}</li>' for x in inh) + '</ul>'
        h += f'<section class="zi__teil"><p class="zi__rubrik">{e(t)}</p>{k}</section>'
    return h + f'<div class="zi__knoepfe">{knoepfe}</div>'


def blatt(id_, art, keys, lagen, ueber_, name, satz, zeilen, knoepfe, alle, steck=None):
    """Eine Zimmerart wie ein Balkon der Fassade: vier Fotos des Hauses als Ebenen (art a oder b, gespiegelt mit «-r»), daneben Name, Satz des Hauses,
    Angaben als Zeilen und die Knöpfe; «Alle Ansichten» öffnet jedes Foto dieser Art im Fenster."""
    eb = ''.join(ebene(k, f'bl__{n}', None, 'satt', lage=l, s=('(max-width:900px) 94vw, 44vw' if n == 'a' else '(max-width:900px) 52vw, 24vw'))
                 for k, l, n in zip(keys, lagen, 'abcd'))
    z = ''.join(f'<li><span>{e(a)}</span><b>{e(b)}</b></li>' for a, b in zeilen)
    return f'''<div class="bl bl--{art}" id="{id_}">
      <div class="bl__bilder komp">{eb}</div>
      <div class="bl__text">{ueber(ueber_)}<p class="bl__name" data-s>{e(name)}</p><p class="bl__satz" data-s>{e(satz)}</p>
        <ul class="bl__zeilen" data-s>{z}</ul>
        <div class="kn-reihe" data-s>{knoepfe}{kn('Zimmeransicht', '#', 'kn--linie', tag='button', attr=f'data-zimmer="{id_}"') if steck else kn(f'Alle Ansichten ({len(alle)})', '#', 'kn--linie', tag='button', attr=f'data-galerie="{id_}"')}</div>
      </div>{zimmeransicht(id_, name, alle, steck) if steck else galerie(id_, name, alle)}
    </div>'''


def seite_zimmer():
    """Zimmer «Aufwachen im Monte-Moro» (Plan Unterseiten, Probe 1): jede Zimmerart ist ein Balkon des Hauses."""
    pr = {p[0] + p[1]: p[2] for p in D.PREISE}
    hotel = ['z-licht', 'z-sessel', 'z-abend', 'z-rot', 'z-neu', 'z-fenster', 'z-bogen', 'z-tv', 'z-gelb', 'z-balkon', 'z-bad', 'z-wanne']
    fam = ['z-familie', 'z-hell', 'z-twin', 'z-doppel', 'z-einzel']
    inhalt = kopf_tag('anfang', 'Zimmer · Residence Alpenhof · Ferienwohnungen', 'Aufwachen im Monte-Moro.', 'im Monte-Moro.', D.ZIMMER_TEXT, 'z-dach', '50% 58%')
    # Steckbriefe der Zimmeransicht (24.10.2026): nur Angaben des Hauses (Website, Preisliste, Booking-Eintrag des Hauses), nichts geschätzt
    ausstattung = ['Dusche/Bad', 'WC', 'Haarfön', 'TV', 'Safe', 'Balkon'] + D.BOOKING_ZIMMER
    preise = [(f'{a}, {b.replace("Zimmer mit ", "")}', f'CHF {c}') for a, b, c in D.PREISE] + [('Preise', 'pro Person / Tag')]
    zuschl = [(t, (p_ if '%' in p_ else f'CHF {p_}')) for t, p_ in D.ZUSCHLAEGE]
    buchen = kn('Zimmer buchen', D.HAUS['buchen'], 'kn--laerche', neu=True)
    st_hotel = steckbrief([('Im Zimmer', ausstattung), ('Zum Schutz unserer Gäste', 'Wir haben eine Brandmeldeanlage.'),
                           ('Preise', preise), ('Inklusive', D.INKLUSIVE), ('Gut zu wissen', zuschl + [('Bezahlung', D.EURO)]),
                           ('Im Haus', [('Zimmer', D.HAUS_ZAHLEN[0]), ('Betten', D.HAUS_ZAHLEN[1])])],
                          buchen + anfrage('Anfrage an die Rezeption', 'Hotelzimmer', 'kn--linie'))
    st_familie = steckbrief([('Familienzimmer', D.FAMILIE_TEXT), ('Residence Alpenhof', D.ALPENHOF_TEXT), ('Im Zimmer', ausstattung),
                             ('Preise', preise), (D.KINDER_SATZ, [(a, f'CHF {p_}') for a, p_ in D.KINDER] + [('Im eigenen Zimmer', D.KINDER_EIGEN.split(': ')[1])]),
                             ('Kidsclub', D.INKLUSIVE[4].split(': ')[1] + ', inklusive'), ('Inklusive', D.INKLUSIVE)],
                            buchen + anfrage('Familienzimmer anfragen', 'Familienzimmer', 'kn--linie'))
    st_apollo = steckbrief([('Haus Apollo', D.APOLLO), ('Auf einen Blick', [('Wohnung', 'im 4. Stock'), ('Lage', 'am Dorfeingang von Saas-Almagell'), ('Balkon', 'Südbalkon'),
                            ('Ausstattung', 'Fernseher, Geschirrspülmaschine, Kaffeemaschine'), ('Wäsche', 'Bett- und Frotteewäsche stehen zur Verfügung'), ('Parkplatz', 'direkt neben dem Haus')]),
                            ('Preis und freie Daten', 'auf Anfrage bei der Rezeption')],
                           anfrage('Ferienwohnung anfragen', 'Haus Apollo', 'kn--laerche'))
    st_arizona = steckbrief([('Haus Arizona', D.ARIZONA), ('Auf einen Blick', [('Wohnungen', '4½, 3½ und 2½ Zimmer'), ('Ausstattung', 'TV, Radio, Geschirrspülmaschine, Kaffeemaschine, Mikrowelle'),
                             ('Wäsche', 'Bett- und Frotteewäsche stehen zur Verfügung'), ('Parkplatz', 'direkt neben dem Haus')]), ('Preis und freie Daten', 'auf Anfrage bei der Rezeption')],
                            anfrage('Ferienwohnung anfragen', 'Haus Arizona', 'kn--laerche'))
    inhalt += kapitel('hotelzimmer', 'k-bl', f'''
    <div class="kap__kopf">{ueber('Hotelzimmer')}{titel('Jedes Zimmer mit Balkon.', em='mit Balkon.')}</div>
    {blatt('standard', 'a', ['z-licht', 'z-bogen', 'z-abend', 'z-wanne'], ['50% 50%', '50% 50%', '50% 50%', '50% 50%'],
           'Standardzimmer und Budgetzimmer', 'Hotelzimmer', D.ZIMMER_TEXT,
           [('Standardzimmer, Frühstück', 'CHF ' + pr['StandardzimmerZimmer mit Frühstück']), ('Standardzimmer, Halbpension (4-Gänge)', 'CHF ' + pr['StandardzimmerZimmer mit Halbpension (4-Gänge)']),
            ('Budgetzimmer, Frühstück', 'CHF ' + pr['BudgetzimmerZimmer mit Frühstück']), ('Budgetzimmer, Halbpension (4-Gänge)', 'CHF ' + pr['BudgetzimmerZimmer mit Halbpension (4-Gänge)']),
            ('Preise', 'pro Person / Tag')],
           kn('Zimmer buchen', D.HAUS['buchen'], 'kn--laerche', neu=True), hotel, steck=st_hotel)}
    <figure class="ausblick" data-bilder>{bild('balkon', sizes='100vw', lage='50% 62%')}<figcaption class="ausblick__satz" data-zeilen>Vom Balkon <em>ins Tal.</em></figcaption></figure>
    {blatt('familie', 'b-r', ['z-familie', 'z-hell', 'z-twin', 'z-einzel'], ['50% 50%', '50% 50%', '50% 50%', '50% 50%'],
           'Familienzimmer · Residence Alpenhof', 'Platz für die ganze Familie', D.FAMILIE_TEXT,
           [('Familienzimmer', '3 - 6 Personen'), ('Residence Alpenhof', '4 Gehminuten'), ('Frühstück und Abendessen', 'im Hotel Monte-Moro')],
           anfrage('Familienzimmer anfragen', 'Familienzimmer', 'kn--nacht') + kn('Kinderpreise', 'preise.html#kinder', 'kn--linie'), fam, steck=st_familie)}''', 'Hotelzimmer')
    inhalt += kapitel('ferienwohnungen', 'k-bl k-bl--wohn', f'''
    <div class="kap__kopf">{ueber('Ferienwohnungen')}{titel('Haus Apollo und Haus Arizona.', em='Haus Arizona.')}</div>
    {blatt('apollo', 'a', ['apollo-wohnen', 'apollo', 'apollo-kueche', 'apollo-haus'], ['50% 50%', '50% 50%', '50% 50%', '30% 50%'],
           'Ferienwohnung am Dorfeingang', 'Haus Apollo', D.APOLLO.split('. Die Wohnung')[0] + '.',
           [('Wohnung', 'eine Wohnung im 4. Stock'), ('Lage', 'am Dorfeingang, Ausblick auf das ganze Dorf'), ('Balkon', 'Südbalkon'),
            ('Ausstattung', 'Fernseher, Geschirrspülmaschine, Kaffeemaschine'), ('Wäsche, Parkplatz', 'Bett- und Frotteewäsche · Parkplatz neben dem Haus')],
           anfrage('Ferienwohnung anfragen', 'Haus Apollo', 'kn--nacht'), ['apollo-wohnen', 'apollo', 'apollo-kueche', 'apollo-haus'], steck=st_apollo)}
    {blatt('arizona', 'a-r', ['arizona-wohnen', 'arizona-holz', 'arizona', 'arizona-haus'], ['50% 50%', '50% 50%', '50% 50%', '90% 50%'],
           'Ferienwohnungen in Saas-Almagell', 'Haus Arizona', D.ARIZONA.split(' Die Wohnungen')[0],
           [('Wohnungen', '4½, 3½ und 2½-Zimmer'), ('Ausstattung', 'TV, Radio, Geschirrspülmaschine, Kaffeemaschine, Mikrowelle'),
            ('Wäsche, Parkplatz', 'Bett- und Frotteewäsche · Parkplatz neben dem Haus')],
           anfrage('Ferienwohnung anfragen', 'Haus Arizona', 'kn--nacht'), ['arizona-wohnen', 'arizona-holz', 'arizona', 'arizona-haus'], steck=st_arizona)}''',
                      'Ferienwohnungen', weiter=('Unten ist das Frühstück gedeckt.', 'preise.html', 'Was im Preis steckt'))
    return kopf('Zimmer und Ferienwohnungen · Hotel Monte-Moro', 'Zimmer, Familienzimmer, Residence Alpenhof und die Ferienwohnungen Apollo und Arizona des Hotel Monte-Moro in Saas-Almagell.', 'zimmer.html') + inhalt + fuss()


def seite_preise():
    preise = ''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td><td>CHF {e(c)}</td></tr>' for a, b, c in D.PREISE)
    z = ''.join(f'<tr><th>{e(t)}</th><td></td><td>{e(p)}</td></tr>' for t, p in D.ZUSCHLAEGE)
    k = ''.join(f'<tr><th>{e(a)}</th><td></td><td>CHF {e(p)}</td></tr>' for a, p in D.KINDER)
    ag = D.ANREISE_GRATIS
    inhalt = kopf_tag('anfang', 'Preise · was im Preis steckt', 'Alles schon dabei.', 'dabei.', D.BERGBAHN_SATZ, 'fr-gross')
    # Robert 20.10.2026 17:28: «Links super viel Leerraum und der Text unübersichtlich» · Preistafeln «viel geiler, schöner, animierter, besser gesetzt, besser zum Stil passend»
    # → links die Gratis-Anreise als geordnete Karte mit den Bedingungen des Hauses im Wortlaut plus zwei Fotos; die Preisliste als Aushang der Rezeption (Plan Unterseiten).
    marken = ['Wohnort', 'Aufenthalt', 'Buchung', 'Zeitraum']
    bed = ''.join(f'<li><span>{m}</span><b>{e(t)}</b></li>' for m, t in zip(marken, ag['bedingungen']))
    inhalt += kapitel('bon', 'k-bon k-bon--preise', f'''
    <div class="bon__links">{ueber('Der Bon der Rezeption')}{titel('Mehr erleben, weniger zahlen.', em='weniger zahlen.')}
      <div class="gr" data-steig data-bis="{ag['bis']}"><p class="gr__marke">Ab 2 Nächten · bis 31. Oktober 2026</p><p class="gr__titel">An- und Abreise <em>geschenkt.</em></p><p class="gr__unter">mit dem öffentlichen Verkehr</p><ul class="gr__zeilen">{bed}</ul></div>
    </div>
    {bon_html()}''', 'Der Bon')
    def zeile(t, p_):
        n = p_.split(' ')[0]
        g, _, d = n.partition('.')  # Schreibweise des Hauses (Punkt) bleibt; gezählt wird nur der Franken-Teil
        z = f'<i data-zahl="{g}">{g}</i>.{d}' + e(p_[len(n):]) if re.fullmatch(r'\d+\.\d\d', n) else e(p_)
        return f'<li><span>{e(t)}</span><i class="aus__punkte" aria-hidden="true"></i><b>{z}</b></li>'
    mat = {(a_, b_): c_ for a_, b_, c_ in D.PREISE}
    spalten = ['Zimmer mit Frühstück', 'Zimmer mit Halbpension (4-Gänge)']
    kopfz = ''.join(f'<th scope="col">{e(c_.replace("Zimmer mit ", ""))}</th>' for c_ in spalten)
    reihen = ''.join(f'<tr><th scope="row">{e(r_)}</th>' + ''.join(f'<td><small>CHF</small><i data-zahl="{mat[(r_, c_)].split(".")[0]}">{mat[(r_, c_)].split(".")[0]}</i>.{mat[(r_, c_)].split(".")[1]}</td>' for c_ in spalten) + '</tr>' for r_ in ('Budgetzimmer', 'Standardzimmer'))
    zus = ''.join(zeile(t, p_) for t, p_ in D.ZUSCHLAEGE)
    kin = ''.join(zeile(a_, 'CHF ' + p_ if False else p_) for a_, p_ in D.KINDER)
    inhalt += kapitel('preisliste', 'k-preise k-aus', f'''
    <div class="kap__kopf">{ueber('Preisliste des Hauses · CHF pro Person / Tag')}{titel('Gut zu wissen, bevor Sie buchen.', em='bevor Sie buchen.')}</div>
    <div class="aus__buehne">
      <div class="pola">{''.join(f'<figure class="pola__k pola__k--{i}" data-steig><div class="pola__f">{bild(k, sizes="(max-width:900px) 70vw, 24vw", vorn=True)}</div><figcaption>{e(BILDER[k][1])}</figcaption></figure>' for i, k in enumerate(('fr-tisch', 'speiseraum', 'fr-detail')))}</div>
      <div class="aus" data-steig>
        <div class="aus__kopf">{kamm('aus__kamm')}<p class="aus__haus">Hotel Monte-Moro · {e(D.HAUS['plz_ort'])}</p><p class="aus__titel">Preisliste</p><p class="aus__unter">pro Person und Tag · CHF</p></div>
        <table class="aus__matrix"><thead><tr><td></td>{kopfz}</tr></thead><tbody>{reihen}</tbody></table>
        <div class="aus__zwei">
          <div><p class="aus__rubrik">Zuschläge</p><ul class="aus__liste">{zus}</ul></div>
          <div id="kinder"><p class="aus__rubrik">{e(D.KINDER_SATZ)}</p><ul class="aus__liste">{kin}</ul></div>
        </div>
        <p class="aus__fuss">{e(D.KINDER_EIGEN)}. {e(D.EURO)} Hotelparkplatz inklusive.</p>
      </div>
    </div>
    <div class="kn-reihe kn-reihe--mitte" data-s>{kn('Zimmer buchen', D.HAUS['buchen'], 'kn--laerche', neu=True)}{anfrage('Frage zu den Preisen', 'Frage zu den Preisen', 'kn--linie')}</div>''',
                      'Preisliste', weiter=('Mit dem Bon in der Tasche: zwei Minuten bis zum Lift.', 'saastal.html', 'Der Tag im Saastal'))
    return kopf('Preise · Hotel Monte-Moro', 'Was im Preis des Hotel Monte-Moro steckt: Bergbahnen und Postautos, Frühstück, Raclette-Abend, Kidsclub, Parkplatz; Preisliste, Zuschläge, Kinderpreise.', 'preise.html') + inhalt + fuss()


def seite_saastal():
    def strecke(liste):
        out = ''
        for i in range(0, len(liste), 2):
            pa = liste[i:i + 2]
            if len(pa) == 2:
                out += paar(pa[0][0], pa[1][0])
            else:
                out += einzel(pa[0][0], 'einzel--breit', s='100vw')
            out += '<div class="saastal__namen">' + ''.join(f'<div data-s><p class="zim__t">{e(t)}</p><p>{e(s)}{(" · " + e(D.POSTAUTO)) if inkl else ""}</p></div>' for k, t, s, inkl in pa) + '</div>'
        return out
    wege, k = '', 0
    for m, ort, satz in D.LAGE:
        n = int(m) * 6
        wege += f'<li><b>{e(m)}</b><span class="spur" aria-hidden="true">{spuren_zeile(n, k)}</span><strong>{e(ort)}</strong><small>{e(satz)}</small></li>'
        k += n
    inhalt = kopf_tag('anfang', 'Saastal · Sommer und Winter', 'Zwei Minuten bis zum Lift.', 'bis zum Lift.', D.LAGE_SATZ + ' ' + D.BERGBAHN_SATZ, 'tal-sommer')
    inhalt += kapitel('wege', 'k-saastal', f'''<div class="kap__kopf">{ueber('Ab dem Haus · Gehminuten laut Haus')}{titel('Zu Fuss vom Haus.', em='vom Haus.')}</div><ol class="wege wege--gross" data-wege>{wege}</ol>''', 'Wege ab dem Haus')
    inhalt += kapitel('sommer', 'k-sommer', f'''<div class="kap__kopf">{ueber('Sommer')}{titel('Im Sommer ein herrliches Wanderparadies.', em='Wanderparadies.')}<p class="leise" data-s>{e(D.SOMMER_SATZ)}</p></div>{strecke(D.SAASTAL['sommer'])}{rahmen('see-blumen', 'alpenrosen', 'murmeltiere', 'rahmen--links')}''', 'Sommer im Saastal')
    inhalt += kapitel('winter', 'k-winter', f'''<div class="kap__kopf">{ueber('Winter')}{titel('Im Winter auf die Piste.', em='auf die Piste.')}</div>{strecke(D.SAASTAL['winter'])}{rahmen('dorf-fluss', 'gletscher', 'winterbach')}''', 'Winter im Saastal',
                      weiter=('Nach dem Lift: das Spa nebenan.', 'spa.html', 'Das Spa nebenan'))
    return kopf('Saastal · Hotel Monte-Moro', 'Sommer und Winter im Saastal ab dem Hotel Monte-Moro: zwei Minuten bis zum Lift, Bergbahnen und Postautos inklusive.', 'saastal.html') + inhalt + fuss()


def seite_spa():
    a = D.SPA_ANGEBOT.replace('Das Angebot reicht vom ', '').replace(' bis hin zum ', ', ').replace(' über ', ', ').rstrip('.')
    teile = [t.strip() for t in a.split(',') if t.strip()]
    angebot = ''.join(f'<li>{e(t[0].upper() + t[1:])}</li>' for t in teile)
    inhalt = kopf_tag('anfang', D.SPA_TITEL, 'Das Spa nebenan.', 'nebenan.', D.SPA_SATZ, 'spa-garten')
    inhalt += kapitel('angebot', 'k-spa', f'''
    <div class="kap__kopf">{ueber('Das Angebot')}{titel('Nach der Sonne die Wärme.', em='die Wärme.')}</div>
    {rahmen('spa-licht', 'spa-holz', 'f-wellness', lagen=('50% 50%', '50% 50%', '50% 60%'))}
    <div class="spa__unten"><ul class="spa__angebot" data-s>{angebot}</ul>
      <div class="spa__preise">{''.join(f'<p data-s><b>{e(p)}</b><span>{e(t)}{(" · " + e(x)) if x else ""}</span></p>' for t, p, x in D.SPA_TARIFE)}<p class="spa__inkl" data-s>{e(D.SPA_INKL)}</p>
      <div class="kn-reihe" data-s>{kn('Zum Spa des Partnerhotels', D.SPA_LINK, 'kn--nacht', neu=True)}</div></div></div>
    ''', 'Das Angebot', weiter=('Am Abend leuchten vor dem Röstihüs die alten Gondeln.', 'roestihues.html', 'Abend im Röstihüs'))
    return kopf('Spa nebenan · Hotel Monte-Moro', 'Das Spa im Partnerhotel Pirmin Zurbriggen nebenan, mit Tarifen für Gäste des Hotel Monte-Moro.', 'spa.html') + inhalt + fuss()


def zettel(titel_, posten, kl=''):
    """Ein Zettel der Karte, gesetzt wie der Bon der Rezeption (Papier, Abriss mit dem Grat des Logos)."""
    z = ''.join(f'<li><span>{e(n)}</span><em>{e(p)}</em>{f"<small>{e(t)}</small>" if t else ""}</li>' for n, t, p in posten)
    return (f'<div class="zt {kl}" data-s><div class="zt__papier"><p class="zt__kopf">{kamm("zt__kamm")}<span>Röstihüs · Saas-Almagell</span></p>'
            f'<p class="zt__titel">{e(titel_)}</p><ul class="zt__posten">{z}</ul>'
            f'<svg class="zt__abriss" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{GRAT}"/></svg></div></div>')


def seite_roestihues():
    """Röstihüs «Es lebe die Tradition!» (Plan Unterseiten, Probe 2): der Abend vor den geschmückten Gondeln, die Stube in Ebenen, die Karte als Zettel je Rubrik."""
    inhalt = kopf_tag('anfang', 'Restaurant Röstihüs · am Abend', 'Es lebe die Tradition!', 'die Tradition!', D.ROESTI_SATZ, 'gondel', '50% 42%', abend=True)
    inhalt += kapitel('stube', 'k-roesti k-bl', f'''
    <div class="kap__kopf">{ueber('Die Stube')}{titel('Regional und herzlich.', em='herzlich.')}</div>
    {blatt('stube-alle', 'a', ['roesti-raum', 'roesti-stube', 'roesti-tische', 'roesti-orange'], ['50% 50%', '55% 50%', '50% 50%', '50% 50%'],
           'Restaurant Röstihüs', 'Im Röstihüs', D.ROESTI_LUST,
           [('Röstis', f'{len(D.ROESTIS)} Sorten, ab Fr. 25.–'), ('Cordon bleus', f'{len(D.CORDON)} Sorten, ab Fr. 39.–'), ('Für die Kleinen', 'eine kleine Auswahl an Speisen')],
           anfrage('Einen Tisch, bitte', 'Tisch im Röstihüs', 'kn--laerche', 'tisch'),
           ['roesti-raum', 'roesti-stube', 'roesti-tische', 'roesti-orange', 'stube-tische', 'stuebli'])}''', 'Die Stube')
    # Robert 20.10.2026 17:31 zu den vier versetzten Zetteln: «Das kann man sich auch nochmal deutlich geiler und besser und schöner machen.»
    # → eine grosse Karte des Röstihüs in drei Spalten auf einer Höhe, Titel mit Messinglinie, Gerichte gross, Preise in der Titelschrift.
    def posten(liste):
        return ''.join(f'<li><p class="rk__z"><span>{e(n)}</span><i aria-hidden="true"></i><em>{e(p_)}</em></p>{f"<small>{e(t)}</small>" if t else ""}</li>' for n, t, p_ in liste)
    weine = [(n.replace('«Hotelwein» ', 'Hotelwein · '), f'{h} · {r} · {m}', p_) for n, h, r, m, p_ in D.HOTELWEINE] + list(D.SPRITZ)
    inhalt += kapitel('karte', 'k-zettel k-rk', f'''
    <div class="kap__kopf">{ueber('Karte vom 18.11.2024 · Fr.')}{titel('Heute Abend im Röstihüs.', em='im Röstihüs.')}</div>
    <div class="rk" data-steig>
      <div class="rk__kopf">{kamm('rk__kamm')}<p>Röstihüs · Saas-Almagell</p></div>
      <div class="rk__spalten">
        <div class="rk__sp"><p class="rk__titel">Best of Röstis</p><ul>{posten(D.ROESTIS)}</ul></div>
        <div class="rk__sp"><p class="rk__titel">Unsere Cordon bleus</p><ul>{posten(D.CORDON)}</ul>
          <p class="rk__titel rk__titel--zwei">Zum Dessert</p><ul>{posten([(D.KOPF[0].split(' (')[0], D.KOPF[0].split(' (')[1].rstrip(')') if ' (' in D.KOPF[0] else '', D.KOPF[1])])}</ul></div>
        <div class="rk__sp"><p class="rk__titel">Wein von Fabian</p><ul>{posten([(n.replace('«Hotelwein» ', ''), f'«Hotelwein» · {h} · {r} · {m}', p_) for n, h, r, m, p_ in D.HOTELWEINE])}</ul>
          <p class="rk__titel rk__titel--zwei">Zum Apéro</p><ul>{posten(list(D.SPRITZ))}</ul>
          <p class="rk__titel rk__titel--zwei">Im Stübli</p><ul>{posten([(D.RACLETTE[0].split(' mit ')[0], 'mit ' + D.RACLETTE[0].split(' mit ', 1)[1], D.RACLETTE[1])])}</ul></div>
      </div>
    </div>
    <div class="kn-reihe kn-reihe--mitte" data-s>{anfrage('Einen Tisch, bitte', 'Tisch im Röstihüs', 'kn--laerche', 'tisch')}{kn('Die ganze Karte (PDF)', 'assets/pdf/speisekarte.pdf', 'kn--linie', neu=True)}</div>''',
                      'Die Karte', weiter=('Später, im Stübli: der Wein von Fabian.', 'index.html#wein', 'Zum Wein von Fabian'))
    return kopf('Restaurant Röstihüs · Hotel Monte-Moro', 'Das Restaurant Röstihüs im Hotel Monte-Moro: elf Röstis, Cordon bleus, Raclette und der Hotelwein von Fabian.', 'roestihues.html') + inhalt + fuss()


def seite_anreise():
    ag = D.ANREISE_GRATIS
    halte = [('Visp', 'Zug bis hier, dann Postauto'), ('Stalden', 'Verzweigung Richtung Saastal'), ('Saas-Grund', 'umsteigen · Abzweigung Saas-Fee links'), ('Saas-Almagell', 'Hotel Monte-Moro')]
    strecke = ''.join(f'<li><i aria-hidden="true"></i><b>{e(n)}</b><small>{e(t)}</small></li>' for n, t in halte)
    inhalt = kopf_tag('anfang', 'Anreise · Kontakt', 'Die Abfahrt in Visp.', 'in Visp.', D.ANREISE_ZUG_ZEIT + ' ' + D.ANREISE_AUTO_ZEIT, 'haus-sommer-g', '50% 45%')
    inhalt += kapitel('weg', 'k-anreise k-anreise--flug', f'''
    {flug('anreise')}
    <div class="kap__kopf kap__kopf--tafel">{ueber('Abfahrt in Visp')}{titel('Die nächste Abfahrt.', em='Abfahrt.')}</div>
    {abfahrtstafel()}
    <div class="anreise__texte">
      <div data-s><p class="ueber">Mit dem Zug und dem Postauto</p><p>{e(D.ANREISE_ZUG)}</p><p class="zim__t">{e(D.ANREISE_ZUG_ZEIT)}</p></div>
      <div data-s><p class="ueber">Mit dem Auto</p><p>{e(D.ANREISE_AUTO)}</p><p class="zim__t">{e(D.ANREISE_AUTO_ZEIT)}</p></div>
      <div data-s data-bis="{ag['bis']}"><p class="ueber">Geschenkt</p><p><b>{e(ag['titel'])}</b> {' '.join(e(b) for b in ag['bedingungen'])}</p></div>
    </div>''', 'Der Weg')
    inhalt += kapitel('ankunft', 'k-ankunft', f'''
    {rahmen('haus-winter-g', 'empfang', 'dorf-nacht')}
    <div class="kap__text"><p class="zim__t" data-s>Ankunft: {e(D.HAUS['name'])}, {e(D.HAUS['plz_ort'])}.</p><p data-s>{e(D.PARK)}. Tel. <a href="tel:{D.HAUS['tel_href']}">{e(D.HAUS['tel'])}</a> · Fax {e(D.HAUS['fax'])}</p>
      <div class="kn-reihe" data-s>{kn('Zimmer buchen', D.HAUS['buchen'], 'kn--laerche', neu=True)}{anfrage('Anfrage an die Rezeption', 'Ihre Anfrage', 'kn--linie')}</div></div>''',
                      'Ankunft', weiter=('Und morgen scheint die Sonne wieder.', 'index.html', 'Zur Startseite'))
    return kopf('Anreise und Kontakt · Hotel Monte-Moro', 'Anreise zum Hotel Monte-Moro in Saas-Almagell mit Zug und Postauto oder mit dem Auto; Kontakt.', 'anreise.html') + inhalt + fuss()


# ---------------------------------------------------------------- Fuss: Fassung 19 «Eingelassen» (Robert 20.10.2026: «eingelassen.»), 1:1 aus _varianten/fuss-2026-10-20c/gen.py
# Wie die Leiste 18: der ganze Fuss liegt in einer hellen, eingelassenen Fläche, nur «Zimmer buchen» steht erhaben. Darin auf der Achse Marke, Kontakt,
# Wege und die vier Häuser der Familie; die Häuser schweben in einem Zug herein und heben sich beim Überfahren leicht (Robert 20.10.2026)
# Familienband seit 26.10.2026 wie auf allen Häusern in der Form «Vier Scheiben» (Robert, auf Wellness gewählt, _varianten/fuss-15b):
# erst die eingelassene Fläche des Hauses, darunter das Band, ganz unten die Rechtszeile (FAMILIEN-FOOTER.md; Aussehen familienband-scheiben.css/.js).
F3_SATZ = 'Bei uns scheint fast immer <em>die Sonne.</em>'
F3_WEGE = [('zimmer.html', 'Zimmer'), ('preise.html', 'Preise'), ('saastal.html', 'Saastal'), ('spa.html', 'Spa nebenan'), ('roestihues.html', 'Röstihüs'), ('anreise.html', 'Anreise')]
F3_FAM_SEITE = 'http://127.0.0.1:8961/'


def f3_img(k, g='m', sizes='(max-width:900px) 50vw, 25vw'):
    w, h = MASSE[k][:2]
    ss = f' srcset="assets/img/{k}-m.webp 900w, assets/img/{k}-l.webp 1440w, assets/img/{k}-x.webp 2200w" sizes="{sizes}"' if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'assets/img/{k}-x.webp')) else ''
    return f'<img src="assets/img/{k}-{g}.webp"{ss} alt="{e(BILDER[k][1])}" width="{w}" height="{h}" loading="lazy" decoding="async">'


def f3_marke():
    return (f'<div class="f3-marke f3-mitte" data-f3="steig">{wort("f3-wort")}<p class="f3-satz">{F3_SATZ}</p>'
            f'<a class="kn kn--laerche" href="{e(D.HAUS["buchen"])}" target="_blank" rel="noopener"><span>Zimmer buchen</span><i>{PF}</i></a></div>')


def f3_kontakt():
    H = D.HAUS
    return (f'<div class="f3-kt f3-kt--mitte">'
            f'<a class="f3-kt__e" href="tel:{H["tel_href"]}" data-f3="steig"><span class="ueber">Telefon</span><b>{e(H["tel"])}</b></a>'
            f'<a class="f3-kt__e" href="mailto:{e(H["mail"])}" data-anfrage="Ihre Anfrage" data-f3="steig"><span class="ueber">E-Mail</span><b>{e(H["mail"])}</b></a>'
            f'<div class="f3-kt__e" data-f3="steig"><span class="ueber">Gastgeber</span><b>Esther &amp; Fabian</b><small>{e(H["gastgeber"])}<br>{e(H["plz_ort"])} · Fax {e(H["fax"])}</small></div>'
            '</div>')


def f3_wege():
    return '<nav class="f3-wege f3-wege--mitte" aria-label="Fuss" data-f3="steig">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in F3_WEGE) + '</nav>'


def f3_familie():
    """Das Familienband unter der eingelassenen Fläche, mit allen Angaben der Vorlage (Name, Zusatz, Ort und Gastgeber, «Sie sind hier», «Zum Haus», Chalet ohne Link).
    Markup wie familienband(), nur mit den Fotos und dem roten Pinselstrich dieses Hauses; Form «Vier Scheiben» in familienband-scheiben.css."""
    li = ''
    for k, name, z, o, g, web, b in FAMILIENBAND_HAEUSER:
        ich = k == 'montemoro'
        inhalt = (f'<figure>{f3_img(b)}</figure><span class="fb__name">{e(name)}</span>' + (f'<span class="fb__zusatz">{e(z)}</span>' if z else '') + f'<span class="fb__ort">{e(o)} · {e(g)}</span>'
                  + ('<span class="fb__hier">Sie sind hier</span>' if ich else ('<span class="fb__weiter">Zum Haus</span>' if web else '')))
        li += f'<li class="fb__haus{" fb__haus--hier" if ich else ""}">' + (f'<a href="{e(web)}">{inhalt}</a>' if web and not ich else f'<div>{inhalt}</div>') + '</li>'
    kopf = f'<a class="fb__kopf" href="{F3_FAM_SEITE}"><img src="assets/zeichen/pinsel-rot.svg" alt="" width="40" height="37"><span>Familie Zurbriggen&nbsp;· seit&nbsp;1967</span></a>'
    return f'<section class="familienband" aria-label="Familie Zurbriggen">{kopf}<ul class="fb__haeuser">{li}</ul></section>'


def fuss():
    return f'''<footer class="fuss f3 f3-19" id="kontakt">{grat_oben()}
<div class="f3__in"><div class="f3-ein f3-fluss">{f3_marke()}{f3_kontakt()}{f3_wege()}</div>{f3_familie()}</div>
  <p class="studie"><span>Designstudie von Tasty Studios, nicht die offizielle Website des Hotel Monte-Moro.</span><span>Fotos: Hotel Monte-Moro (Website, Booking, Tripadvisor vom Haus), Schweiz Tourismus, Familie Zurbriggen · Schlussbild: Christoph Strässler, Wikimedia Commons, CC BY-SA 2.0</span><span><a href="impressum.html">Impressum und Bildnachweis</a> · <a href="datenschutz.html">Datenschutz</a></span></p>
</footer>
</main>
{chat_html()}
<script src="assets/js/bilder.js?v={V}" defer></script>
<script src="assets/js/montemoro.js?v={V}" defer></script>
<script src="assets/js/tiefe.js?v={V}" defer></script>
<script src="assets/js/rezeption-weg.js?v={V}" defer></script>
<script src="assets/js/anfrage.js?v={V}" defer></script>
<script src="assets/js/galerie.js?v={V}" defer></script>
<script src="assets/js/zimmeransicht.js?v={V}" defer></script>
<script src="assets/js/rezeption.js?v={V}" defer></script>
<script src="assets/js/fuss.js?v={V}" defer></script>
<script src="assets/js/familienband-scheiben.js?v={V}" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- Pflicht-Liste 9d (23.10.2026): Impressum, Datenschutz, 404, robots.txt, sitemap.xml
# Rechtstexte nur im Wortlaut des Hauses (_quelle/website/text/de__impressum.html.md, de__datenschutz.html.md, abgerufen 09.10.2026), nichts von uns geschrieben.
# Eigene Zeilen nur: Hinweis Designstudie und Bildnachweis (Herkunft aus inhalt/bilder.py).
IMPRESSUM = [
    ('Kontakt', ['Hotel & Restaurant Monte-Moro', 'Esther & Fabian Zurbriggen-Zurbriggen', 'CH-3905 Saas-Almagell',
                 f'Tel: {D.HAUS["tel"]}', f'Fax: {D.HAUS["fax"]}', f'Email: {D.HAUS["mail"]}']),
    ('Haftungsausschluss', ['Hotel Monte-Moro übernimmt keinerlei Gewähr hinsichtlich der inhaltlichen Richtigkeit, Genauigkeit, Aktualität, Zuverlässigkeit und Vollständigkeit der Informationen. Haftungsansprüche gegen Hotel Monte-Moro wegen Schäden materieller oder immaterieller Art, welche aus dem Zugriff oder der Nutzung bzw. Nichtnutzung der veröffentlichten Informationen, durch Missbrauch der Verbindung oder durch technische Störungen entstanden sind, werden ausgeschlossen. Alle Angebote sind unverbindlich. Hotel Monte-Moro behält es sich ausdrücklich vor, Teile der Seiten oder das gesamte Angebot ohne gesonderte Ankündigung zu verändern, zu ergänzen, zu löschen oder die Veröffentlichung zeitweise oder endgültig einzustellen.']),
    ('Haftung für Links', ['Verweise und Links auf Webseiten Dritter liegen ausserhalb unseres Verantwortungsbereichs. Es wird jegliche Verantwortung für solche Webseiten abgelehnt. Der Zugriff und die Nutzung solcher Webseiten erfolgen auf eigene Gefahr des Nutzers oder der Nutzerin.']),
    ('Urheberrechte', ['Die Urheber- und alle anderen Rechte an Inhalten, Bildern, Fotos oder anderen Dateien auf der Website gehören ausschliesslich Hotel Monte-Moro oder den speziell genannten Rechtsinhabern. Für die Reproduktion jeglicher Elemente ist die schriftliche Zustimmung der Urheberrechtsträger im Voraus einzuholen.']),
]
DATENSCHUTZ = [
    ('SSL-Verschlüsselung', ['Diese Seite nutzt aus Sicherheitsgründen und zum Schutz der Übertragung vertraulicher Inhalte, wie zum Beispiel Bestellungen oder Anfragen, die Sie an uns als Seitenbetreiber senden, eine SSL- beziehungsweise TLS-Verschlüsselung. Somit können Daten, die Sie an uns übermitteln, nicht von Dritten mitgelesen werden.']),
    ('Daten', ['Durch die Nutzung unserer Webseite werden die nachstehenden Bedingungen akzeptiert. Wenn Sie via Formular, Email, Telefon oder sozialer Medien Anfragen, Reservationen, Bestellungen tätigen, Newsletter abonnieren oder Informationsmaterial und andere Leistungen bei uns anfordern, benötigen wir von Ihnen persönliche Informationen (Name, Adresse, usw.). Falls die von Ihnen gewünschten Leistungen nur mit Hilfe von Dritten erbracht werden können (Kurtaxen, Bürgerpässe, Wintercard usw.), werden wir die Daten an die betreffenden Dienstleistungsträger weiterleiten, wozu Sie uns mit den Angaben Ihrer Daten automatisch ermächtigen. Ansonsten werden Ihre persönlichen Daten vertraulich behandelt und nur in anonymisierter Form selbst bearbeitet. Der Verkauf an Dritte wird ausdrücklich ausgeschlossen.']),
    ('Cookies', ['Cookies sind kleine Datenelemente, die eine Website an Ihren Browser senden kann, um Sie bei datenbankgestützten Systemen besser zu unterstützen. Sie haben jedoch die Möglichkeit, Ihren Browser so einzustellen, dass er Sie davon in Kenntnis setzt, wenn Sie ein Cookie erhalten oder diese automatisch ablehnt. Somit können Sie selbst entscheiden, ob Sie das akzeptieren wollen oder nicht. Durch die Nutzung unserer Webseite willigen Sie ein, dass wir Cookies zur Optimierung der Benutzerfreundlichkeit setzen.']),
    ('Google Analytics', ['Google Analytics ist ein Webanalysedienst. Google verwendet die erhobenen Daten, um nachzuverfolgen und zu untersuchen, wie diese Webseite genutzt wird, Berichte über ihre Aktivitäten zu verfassen und diese gemeinsam mit anderen Google-Diensten zu nutzen. Google kann die erhobenen Daten verwenden, um die Anzeigen seines eigenen Werbenetzwerks zu kontextualisieren und personalisieren. Erhobene personenbezogene Daten: Cookie und Nutzungsdaten Verarbeitungsort: Vereinigte Staaten',
                          ('Datenschutzerklärung', 'https://policies.google.com/privacy'), ('Google Analytics deaktivieren', 'https://tools.google.com/dlpage/gaoptout?hl=de')]),
    ('Google Webfonts', ['Um unsere Inhalte browserübergreifend korrekt und grafisch ansprechend darzustellen, verwenden wir auf dieser Website Scriptbibliotheken und Schriftbibliotheken. Google Webfonts werden zur Vermeidung mehrfachen Ladens in den Cache Ihres Browsers übertragen. Falls der Browser die Google Webfonts nicht unterstützt oder den Zugriff unterbindet, werden Inhalte in einer Standardschrift angezeigt. Der Aufruf von Scriptbibliotheken oder Schriftbibliotheken löst automatisch eine Verbindung zum Betreiber der Bibliothek aus. Dabei ist es theoretisch möglich, dass Betreiber entsprechender Bibliotheken Daten erheben. Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA',
                         ('Datenschutzerklärung', 'https://policies.google.com/privacy?hl=de')]),
    ('Google Maps', ['Wir verwenden Google Maps, um geographische Informationen visuell darzustellen. Bei der Nutzung von Google Maps werden von Google auch Daten über die Nutzung der Kartenfunktionen durch Besucher erhoben, verarbeitet und genutzt. Nähere Informationen über die Datenverarbeitung durch Google können Sie den Google-Datenschutzhinweisen entnehmen. Dort können Sie im Datenschutzcenter auch Ihre persönlichen Datenschutz-Einstellungen verändern.',
                     ('Datenschutzerklärung', 'https://www.google.com/intl/de_ch/help/terms_maps.html')]),
]
HERKUNFT = [('website/', 'Website des Hotel Monte-Moro'), ('extern/booking', 'Booking.com, Fotos vom Haus'), ('bearbeitet/gondel-booking', 'Booking.com, Fotos vom Haus'),
            ('extern/tripadvisor', 'Tripadvisor, Fotos vom Hotel'), ('extern/myswitzerland', 'Schweiz Tourismus'), ('../../Familie Zurbriggen', 'Fotos der Häuser der Familie Zurbriggen')]


def bildnachweis():
    benutzt = set()
    for n in SEITEN:
        if os.path.exists(n):
            benutzt |= set(re.findall(r'assets/img/([a-z0-9-]+?)-(?:s|m|l|x)\.webp', open(n, encoding='utf-8').read()))
    gruppen = {}
    for k in sorted(benutzt):
        if k not in BILDER:
            continue
        q = next((t for p, t in HERKUNFT if BILDER[k][0].startswith(p)), None)
        if q:
            gruppen[q] = gruppen.get(q, 0) + 1
    zeilen = ''.join(f'<li>{e(q)}</li>' for q in gruppen)
    return ('<h2 class="recht__h">Bildnachweis</h2><ul class="recht__liste">' + zeilen +
            '<li>Schlussbild «Valais under a sea of fog»: Christoph Strässler, <a href="https://commons.wikimedia.org/wiki/File:Valais_under_a_sea_of_fog.jpg" target="_blank" rel="noopener">Wikimedia Commons</a>, '
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/deed.de" target="_blank" rel="noopener">CC BY-SA 2.0</a>, zugeschnitten</li>'
            '<li>Auftakt: Foto des Hauses freigestellt, die Fichte links mit KI ergänzt</li>'
            '<li>Dorfkarte auf der Seite Anreise: <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© OpenStreetMap-Mitwirkende</a>, ODbL</li></ul>')


def recht_seite(datei, titel_, abschnitte, satz, nachweis=False):
    def teil(t):
        if isinstance(t, tuple):
            return f'<a href="{e(t[1])}" target="_blank" rel="noopener">{e(t[0])}</a>'
        return e(t)
    body = ''
    for h, teile in abschnitte:
        texte = [teil(t) for t in teile]
        if h == 'Kontakt':
            inhalt_ = '<p>' + '<br>'.join(texte) + '</p>'
        else:
            links = [x for t, x in zip(teile, texte) if isinstance(t, tuple)]
            inhalt_ = ''.join(f'<p>{x}</p>' for t, x in zip(teile, texte) if not isinstance(t, tuple)) + (f'<p class="recht__links">{" · ".join(links)}</p>' if links else '')
        body += f'<h2 class="recht__h">{e(h)}</h2>{inhalt_}'
    if nachweis:
        body += bildnachweis()
    body += ('<p class="recht__studie">Diese Seite ist eine Designstudie von Tasty Studios und nicht die offizielle Website des Hotel Monte-Moro. '
             'Die Texte oben stehen im Wortlaut der heutigen Seite des Hauses, abgerufen am 09.10.2026.</p>')
    inhalt = f'''<section class="recht" id="anfang" aria-label="{e(titel_)}">
  <div class="recht__kopf">{kamm('recht__kamm')}{ueber(satz)}{titel(titel_ + '.', em=None, kl='d2', tag='h1')}</div>
  <div class="recht__text">{body}</div>
</section>'''
    return kopf(f'{titel_} · Hotel Monte-Moro', f'{titel_} des Hotel Monte-Moro in Saas-Almagell, im Wortlaut des Hauses. Designstudie von Tasty Studios.') + inhalt + fuss()


def seite_impressum():
    return recht_seite('impressum.html', 'Impressum', IMPRESSUM, 'Hotel Monte-Moro · Saas-Almagell', nachweis=True)


def seite_datenschutz():
    return recht_seite('datenschutz.html', 'Datenschutz', DATENSCHUTZ, 'Hotel Monte-Moro · Saas-Almagell')


def seite_404():
    inhalt = f'''<section class="recht recht--404" id="anfang" aria-label="Seite nicht gefunden">
  <div class="recht__kopf">{kamm('recht__kamm')}{ueber('Hotel Monte-Moro · Saas-Almagell')}{titel('Diese Seite gibt es nicht.', em='nicht.', kl='d2', tag='h1')}
  <div class="kn-reihe kn-reihe--mitte" data-s>{kn('Zur Startseite', 'index.html', 'kn--laerche')}{kn('Zimmer buchen', D.HAUS['buchen'], 'kn--linie', neu=True)}</div></div>
</section>'''
    return kopf('Seite nicht gefunden · Hotel Monte-Moro', 'Diese Seite gibt es im Hotel Monte-Moro nicht. Zur Startseite mit Zimmern, Preisen, Saastal, Spa, Röstihüs und Anreise.') + inhalt + fuss()


def nebendateien():
    seiten = ['', 'zimmer.html', 'preise.html', 'saastal.html', 'spa.html', 'roestihues.html', 'anreise.html', 'impressum.html', 'datenschutz.html']
    open('robots.txt', 'w').write('User-agent: *\nDisallow: /\n# Designstudie: bleibt bis zur Freigabe ausserhalb der Suchmaschinen.\nSitemap: https://www.monte-moro.ch/sitemap.xml\n')
    open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                   + ''.join(f'  <url><loc>https://www.monte-moro.ch/{s}</loc></url>\n' for s in seiten) + '</urlset>\n')


from seiten import saastal as _saastal, spa as _spa, anreise as _anreise  # noqa: E402  eigene Dateien je Unterseite (20.10.2026)
SEITEN = {'index.html': startseite, 'zimmer.html': seite_zimmer, 'preise.html': seite_preise, 'saastal.html': _saastal.seite, 'spa.html': _spa.seite, 'roestihues.html': seite_roestihues, 'anreise.html': _anreise.seite,
          'datenschutz.html': seite_datenschutz, '404.html': seite_404}
SEITEN['impressum.html'] = seite_impressum   # zuletzt: der Bildnachweis liest die übrigen fertigen Seiten


if __name__ == '__main__':
    wissen()
    for name, f in SEITEN.items():
        open(name, 'w', encoding='utf-8').write(f())
        print('gebaut:', name, os.path.getsize(name) // 1024, 'KB')
    nebendateien()
    print('Familienband:', familienband_datei())
