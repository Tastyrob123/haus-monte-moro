#!/usr/bin/env python3
"""werkbank/ki.html «KI und Ihre Daten» und werkbank/karte.html + PDF «Ein Vorschlag.» (Stamm, 21.10.2026, Vorlage sb_ki.py des Stamm).

Robert 20.10.2026: «… dass unten auch noch das Angebot ist, dieser ganzen KI-Sache, dieser KI-Seite» (Vorbild ki_seite.py des Vorbild der Werkbänke,
nur gelesen; hier eigene, kürzere Fassung im Kleid des Stamms). Verlinkt aus Gang IV der Karte «Ein Vorschlag.» (sb_angebot.py).

Nur Belegtes:
  · Vier Stellen und «ohne KI»: reception/gast/gast.py (Chat und Antwort-Entwurf, Wissen nur aus Seiten und Unterlagen), reception/reception.js
    («Hier wird nichts verschickt»), imprimerie/api/entwurf.py (ohne KI die passendste fertige Vorlage), livre/livre.py («Gespeichert wird nichts»,
    Messung ohne KI gegen die Palette).
  · Anbieter: privacy.anthropic.com, Artikel «Is my data used for model training?» (kommerzielle Produkte, API), gelesen am 20.10.2026.
  · Gästefragen aus dem Chat gehen mit der Antwort ins Werkzeug für die Gäste (gast.py → /api/fragen), damit das Team sieht, was gefragt wurde.
Läuft am Ende von haus.nach_bau(): bau()."""
import html, os, re, subprocess

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
WB = os.path.join(ROOT, 'werkbank')
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'

STAND = '8. November 2026'
_ZVB = __import__('re').search(r'viewBox="([^"]+)"', open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..', '..', '_werkzeuge', 'oberflaeche', 'kleid', 'montemoro-zeichen.svg'), encoding='utf-8').read()).group(1)   # viewBox des Bergkamms
HZ = f'<svg class="ki-hz" viewBox="{_ZVB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg>'
CLAUDE = '<svg class="ki-claude" viewBox="0 0 24 24" role="img" aria-label="Claude"><path fill="currentColor" d="' + open(os.path.join(W, 'ki_claude_pfad.txt'), encoding='utf-8').read().strip() + '"/></svg>'
KOSTEN_OFFEN = 'Nach Verbrauch über Ihr eigenes Konto. Den Betrag je Aufruf messe ich beim ersten Lauf mit Ihrem Konto und trage ihn hier ein.'

# Aufbau: Auftakt → Zahlen → drei Stellen (Gerät + helle Karte) → Sorge → Fenster → Daten → Ohne KI → In Ihrer Hand.
# Kosten stehen nur hier, nicht auf der Karte «Ein Vorschlag.»; ein Betrag ist nicht belegt und steht darum nirgends.
AUFTAKT = ('Wo die KI hilft.', 'Und wo Ihre Daten bleiben.',
           'In zwei Werkzeugen des Monte-Moro hilft an drei Stellen KI mit, jedes Mal Claude, das Sprachmodell von Anthropic. Für jede Stelle steht hier, was sie macht, welche Daten wohin gehen und was ohne KI bleibt. Im Entwurf antworten alle drei mit beschrifteten Proben; die KI arbeitet erst über Ihr eigenes Konto.')
ZAHLEN = [('3', 'Stellen nutzen KI, alles andere arbeitet ohne.'), ('0', 'Ihrer Daten gehen ins Training des Modells.'),
          ('30', 'Tage, dann löscht der Anbieter jede Eingabe.'), ('12', 'Monate bewahren Sie Anfragen auf, dann sind sie weg.')]
BLICK = ('Was es kostet', ['Die KI läuft über ein eigenes Konto des Hotels beim Anbieter. Sie zahlen dort direkt nach Verbrauch; ich richte das Konto ein und setze eine Obergrenze je Monat.',
                           'Die Werkzeuge, die Vorlagen, das Markenbuch und alles Übrige laufen ohne KI.'])
STELLEN_KOPF = ('Drei Stellen,', 'genau beschrieben.', 'Was die KI dort tut, was dabei zum Anbieter geht, was Sie aufbewahren und was ohne sie bleibt.')
REIHEN = ('Was sie tut', 'Was zum Anbieter geht', 'Was gespeichert wird', 'Ohne KI')
import rh_werkzeuge as _WK
_N = _WK.NAMEN
STELLEN = [  # Name, Werkzeug, Bildschirm (ansichten/Werkzeuge), tut, an, gespeichert, ohne
    ('Die Rezeption im Chat', _N['reception'], 'reception',
     'Beantwortet Fragen von Gästen zu Zimmern, Preisen, Inklusive, Anreise, Kidsclub, Spa und Röstihüs, nur aus Ihren Seiten und Karten. Im Entwurf steht er auf jeder Seite unten rechts zum Ausprobieren.',
     'Fragen und Antworten des Gesprächs. Name und Kontakt nur, wenn ein Gast selbst etwas anfragt.',
     'Fragen und Antworten in der Rezeption, damit Sie sehen, was Gäste wissen wollen; nach zwölf Monaten gelöscht.',
     'Die Seiten Zimmer, Preise und Anreise und das Fenster für Anfragen stehen wie gewohnt da.'),
    ('Antwort auf eine Anfrage', _N['reception'], 'reception-2',
     'Schreibt Ihnen einen Antwortentwurf auf eine Zimmeranfrage, eine Frage oder einen Tischwunsch, im Ton des Hauses.',
     'Die Anfrage mit Name, Kontakt und Anliegen.',
     'Anfragen in der Rezeption, nach zwölf Monaten gelöscht, auf Wunsch des Gastes sofort.',
     'Eingang und Anfragen lassen sich bedienen. Die Antwort schreiben Sie dann selbst. Verschickt wird ohnehin nur, was jemand abschickt.'),
    ('Eine Markenprüfung', _N['livre'], 'livre',
     'Prüft einen fremden Entwurf, etwa eine Anzeige oder einen Prospekt von aussen, gegen Farben, Logo und Schrift des Monte-Moro.',
     'Die ersten zwei Seiten der Datei als Bild.',
     'Nichts.',
     'Fotos, Dateien und die Messung der Farben laufen weiter. Nur die schriftliche Beurteilung fehlt.')]
SORGE = ('Und wenn die KI Gästen etwas Falsches sagt?',
         'Die Frage ist richtig. Die KI darf nur wiedergeben, was Sie selbst veröffentlicht haben, und muss sagen, wenn sie etwas nicht weiss; dann nennt sie Ihren Kontakt. '
         'Ein Fehler lässt sich bei einer KI nie ganz ausschliessen. Verbindlich ist, was Sie sagen.')
FENSTER = ('Die KI macht den Entwurf.', 'Abgeschickt wird von Ihnen.', 'Jede Antwort an einen Gast geht erst hinaus, wenn jemand aus Ihrem Team sie selbst verschickt.')
DATEN_KOPF = ('Was mit Ihren Daten', 'geschieht.', 'Der Anbieter des Sprachmodells ist Anthropic. Was er zusagt, steht in seinen Geschäftsbedingungen; was Sie aufbewahren, bestimmen Sie.')
ANBIETER = ('Claude', 'Sprachmodell von Anthropic PBC, San Francisco')
DATEN = [('Nicht zum Lernen', 'Anthropic nutzt, was über Ihr Konto läuft, nicht zum Training seiner Modelle.'),
         ('Nach 30 Tagen gelöscht', 'Eingaben und Antworten löscht Anthropic innerhalb von 30 Tagen. Länger nur bei Verstössen gegen seine Nutzungsregeln oder wenn ein Gesetz es verlangt.'),
         ('Ihr eigener Speicher', 'Was Sie aufbewahren, liegt in der Rezeption, nur mit Zugang lesbar, und wird nach zwölf Monaten gelöscht.'),
         ('Menschen verschicken', 'Die KI verschickt keine Mails und bucht nichts. Jede Antwort per Mail geht von Ihnen hinaus.'),
         ('Gebucht wird woanders', 'Zimmer laufen wie heute über Ihr Buchungsfenster, Tische über die Anfrage. Karten- und Zahlungsdaten gehören nicht in den Chat.'),
         ('Abschaltbar', 'Jede der drei Stellen lässt sich einzeln abschalten, das Werkzeug arbeitet weiter.')]
OHNE_KOPF = ('Läuft auch', 'ohne KI.', 'Fällt die KI aus, ist die Grenze des Monats erreicht oder schalten Sie sie ab, arbeiten alle Werkzeuge weiter. Es fehlt nur, was die KI schreibt.')
HAND_KOPF = ('Sie entscheiden,', 'wie weit sie geht.')
HAND = [('Das Konto', 'läuft auf das Hotel Monte-Moro. Beim Anbieter sehen Sie jeden Aufruf.'),
        ('Die Obergrenze', 'setze ich je Monat. Ist sie erreicht, laufen die Werkzeuge bis zum nächsten Monat ohne KI weiter.'),
        ('Der Schalter', 'liegt bei Ihnen. Auf Ihren Wunsch schalte ich die KI ab, die Werkzeuge laufen weiter wie beschrieben.')]
OFFEN = ('Was Sie noch festlegen', 'Ihre Datenschutzerklärung bekommt vor dem Start einen Abschnitt zum Chat. Zwei Punkte entscheiden Sie: die Grundlage für die Übermittlung in die USA und wie lange Anfragen aufbewahrt werden.')
QUELLEN = [('Anthropic: Training mit Daten', 'https://privacy.anthropic.com/en/articles/7996868-is-my-data-used-for-model-training'),
           ('Anthropic: Aufbewahrung', 'https://privacy.anthropic.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data')]
NAV = ('<nav aria-label="Kapitel"><a href="#ki-blick">KI</a><a href="#ki-zahlen">In Zahlen</a><a href="#ki-stellen">Drei Stellen</a><a href="#ki-daten">Ihre Daten</a>'
       '<a href="#ki-ohne">Ohne KI</a><a href="#ki-hand">In Ihrer Hand</a><a href="index.html#sag-vorschlag">Zurück zum Angebot</a></nav>')


def titel(z1, z2, cls='t2', tag='h2'):
    return f'<{tag} class="{cls} zt"><span class="z"><span>{e(z1)}</span></span><span class="z"><span><em>{e(z2)}</em></span></span></{tag}>'


def kopf_mitte(z1, z2, lauf):
    return f'<header class="ki-kopf"><div data-a="auf">{HZ}</div>{titel(z1, z2)}<p class="ki-lauf" data-a="worte">{e(lauf)}</p></header>'


def geraete():
    """Laptop mit dem echten Bildschirm je Stelle (Gehäuse der Werkbank, objekte_bau.laptop), nach werkbank/img/ki-geraet-<n>.webp."""
    import objekte_bau as OB
    os.makedirs(os.path.join(WB, 'img'), exist_ok=True)
    for _n, _w, b, *_x in STELLEN:
        q = os.path.join(W, 'ansichten', 'Werkzeuge', b + '.jpg')
        if os.path.exists(q):
            im = OB.laptop(q); im.thumbnail((1600, 1600)); im.save(os.path.join(WB, 'img', f'ki-geraet-{b}.webp'), quality=82)


def hauptteil():
    zahlen = ''.join(f'<div class="ki-zahl" data-a="auf" style="--i:{i}"><p class="ki-zahl__n"><span data-z="{z}">{z}</span></p><p class="ki-zahl__t">{e(t)}</p></div>' for i, (z, t) in enumerate(ZAHLEN))
    kosten = ''.join(f'<li class="mn-p"><p class="mn-p__z"><b>{e(n)}</b><i></i><span>{e(w)}</span></p><p class="mn-p__s">{e(KOSTEN_OFFEN)}</p></li>' for n, w, *_x in STELLEN)
    stellen = ''
    for i, (n, w, b, tut, an, sp, ohne) in enumerate(STELLEN):
        reihen = ''.join(f'<div class="ki-k__r"><dt>{e(REIHEN[j])}</dt><dd>{e(x)}</dd></div>' for j, x in enumerate((tut, an, sp)))
        stellen += (f'<article class="ki-st{" ki-st--um" if i % 2 else ""}"><figure class="ki-geraet" data-a="kipp"><img src="img/ki-geraet-{b}.webp" alt="{e(w)} am Laptop: {e(n)}" loading="lazy" decoding="async"></figure>'
                    f'<div class="ag-blatt ki-k" data-a="heben"><h3 class="ki-k__t">{e(n)}</h3><p class="ki-k__preis">{e(w)}</p><dl>{reihen}</dl>'
                    f'<div class="ki-k__ohne"><p class="ki-k__ohne-t">{e(REIHEN[3])}</p><p>{e(ohne)}</p></div></div></article>')
    daten = ''.join(f'<div class="ki-d" data-a="heben"><span class="ki-siegel" aria-hidden="true"><i></i></span><h3>{e(t)}</h3><p>{e(s)}</p></div>' for t, s in DATEN)
    ohne = ''.join(f'<div class="ki-o" data-a="kipp" style="--i:{i}"><h3>{e(s[0])}</h3><p>{e(s[6])}</p></div>' for i, s in enumerate(STELLEN))
    hand = ''.join(f'<p class="ki-h" data-a="auf" style="--i:{i}"><b>{e(t)}</b>{e(s)}</p>' for i, (t, s) in enumerate(HAND))
    quellen = ''.join(f'<li><a href="{q}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, q in QUELLEN)
    f1, f2, fs = FENSTER
    return f'''
<section class="fl fl--nacht tapete-leicht ki ki-auftakt" id="ki-blick">
  <div class="in"><div data-a="auf">{HZ}</div>{titel(AUFTAKT[0], AUFTAKT[1], 't1', 'h1')}<p class="ki-lauf" data-a="worte">{e(AUFTAKT[2])}</p></div>
</section>
<section class="fl fl--navy tapete blatt ki" id="ki-zahlen">
  <div class="in">
    <div class="ki-zahlen">{zahlen}</div>
  </div>
</section>
<section class="fl fl--navy tapete blatt ki" id="ki-stellen">
  <div class="in">{kopf_mitte(*STELLEN_KOPF)}<div class="ki-stellen">{stellen}</div>
    <div class="ag-blatt ki-offen ki-sorge" data-a="heben"><h3 class="ki-k__t">{e(SORGE[0])}</h3><p>{e(SORGE[1])}</p></div></div>
</section>
<section class="wfen" id="ki-fenster" aria-label="{e(f1)} {e(f2)}">
  <div class="wfen__f">
    <img src="eigen/fen-fenster-tisch-1800.webp" srcset="eigen/fen-fenster-tisch-1200.webp 1200w, eigen/fen-fenster-tisch-1800.webp 1800w, eigen/fen-fenster-tisch-2400.webp 2400w" sizes="100vw" alt="Blick vom Balkon des Hotel Monte-Moro ins Tal" loading="lazy" decoding="async">
    <div class="wfen__in"><svg class="wfen__z" viewBox="{_ZVB}" fill="currentColor" aria-hidden="true"><use href="#hz"/></svg><h2 class="wfen__t"><span>{e(f1)}</span><span><em>{e(f2)}</em></span></h2><p class="wfen__k">{e(fs)}</p></div>
  </div>
</section>
<section class="fl fl--papier tapete-hell blatt ki" id="ki-daten">
  <div class="in">{kopf_mitte(*DATEN_KOPF)}
    <div class="ki-anbieter" data-a="auf">{CLAUDE}<p><b>{e(ANBIETER[0])}</b><span>{e(ANBIETER[1])}</span></p></div>
    <div class="ki-daten">{daten}</div></div>
</section>
<section class="fl fl--creme tapete-hell blatt ki" id="ki-ohne">
  <div class="in">{kopf_mitte(*OHNE_KOPF)}<div class="ki-ohne">{ohne}</div></div>
</section>
<section class="fl fl--nacht tapete-leicht blatt ki" id="ki-hand">
  <div class="in">
    <div class="ki-hand">
      <figure class="ki-hand__b" data-a="kipp"><img src="img/ki-team.webp" alt="Der Empfang des Hotel Monte-Moro mit dem Bergkamm" loading="lazy" decoding="async"></figure>
      <div class="ki-hand__t"><div data-a="auf">{HZ}</div>{titel(*HAND_KOPF)}{hand}</div>
    </div>
    <div class="ag-blatt ki-offen" data-a="heben"><h3 class="ki-k__t">{e(OFFEN[0])}</h3><p>{e(OFFEN[1])}</p>
      <p class="ki-knoepfe"><a class="kn kn--klein" href="../datenschutz.html" target="_blank" rel="noopener">Datenschutz auf der neuen Seite<i>{PF}</i></a>
      <a class="kn kn--klein" href="index.html#sag-vorschlag">Zurück zum Angebot<i>{PF}</i></a></p>
      <p class="ki-quellen">Angaben des Anbieters, gelesen am {STAND}:</p><ul class="ki-quellen__l">{quellen}</ul></div>
  </div>
</section>
<script>
(function () {{ var f = document.getElementById('ki-fenster'); if (!f) return; if (!('IntersectionObserver' in window)) {{ f.classList.add('da'); return; }}
  f.classList.add('weg'); new IntersectionObserver(function (es) {{ f.classList.toggle('weg', !es[0].isIntersecting); }}).observe(f);
  new IntersectionObserver(function (es, o) {{ if (es[0].isIntersecting) {{ o.disconnect(); f.classList.add('da'); }} }}, {{ threshold: 0.35 }}).observe(f); }})();
</script>
'''


def ki_seite(t):
    geraete()
    from PIL import Image
    import haus as _H
    q = _H.bild('rezeption', 1440)
    if os.path.exists(q):
        Image.open(q).convert('RGB').save(os.path.join(WB, 'img', 'ki-team.webp'), quality=82)
    m0, m1 = t.find('<main id="oben">'), t.find('</main>')
    kopf = t[:m0]
    kopf = re.sub(r'<title>.*?</title>', '<title>KI und Ihre Daten · Hotel Monte-Moro</title>', kopf, count=1, flags=re.S)
    kopf = re.sub(r'<nav aria-label="Kapitel">.*?</nav>', NAV, kopf, count=1, flags=re.S)
    import sb_farbe as SF
    kopf = kopf.replace('</head>', SF.ohne_fett(SF.faerbe(open(os.path.join(W, 'sb_ki.css'), encoding='utf-8').read())) + '\n<style>.ki-claude{color:#d97757!important}</style>\n</head>', 1)
    return kopf + '<main id="oben">' + hauptteil() + t[m1:]


def _kopf(t, titel):
    css = ''.join(re.findall(r'<link rel="stylesheet" href="[^"]*(?:werkbank|kapitel)\.css[^"]*">', t))
    fonts = ''.join(re.findall(r'<link rel="preload"[^>]*font[^>]*>', t))
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)} · Hotel Monte-Moro</title>
<meta name="robots" content="noindex, nofollow">
{fonts}
{css}'''


def karte_seite(t):
    m = re.search(r'<article class="mn".*?</article>', t, re.S)
    if not m:
        return None
    karte = m.group(0).replace('<article class="mn" data-a="heben">', '<article class="mn da">')
    return _kopf(t, 'Ein Vorschlag') + '''
<style>
html,body{margin:0;background:var(--nacht,#0a2a4a)}
body{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;padding:clamp(20px,4vw,64px) 16px}
.mn{opacity:1!important;transform:none!important;transition:none!important}
.mn-pdf{display:none!important}
@page{margin:0}
@media print{html,body{background:#f5f2ee;padding:0;display:block}.mn{width:100%;max-width:none;border-radius:0;box-shadow:none;padding:14mm 18mm;zoom:.86}.mn-ki{display:none!important}.mn-gang,.mn-l li,.mn-p{break-inside:avoid}}
</style>
</head>
<body>
''' + karte + '\n</body>\n</html>\n'


PDF_JS = r'''
const path = require('path');
let PW; try { PW = require('playwright'); } catch (e) { PW = require('/opt/node-tools/node_modules/playwright'); }
const { chromium } = PW;
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('http://127.0.0.1:9388/werkbank/karte.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
  // feste TrueType-Schnitte für den Druck (variable Schriften landen sonst als «Type 3» in der PDF, Apple-Vorschau zeichnet sie weich)
  await p.addStyleTag({ content: "@font-face{font-family:'TDruck';src:url(/_werkbank/fonts/FjallaOne-Regular.ttf)}" +
    "@font-face{font-family:'IDruck';font-weight:400;src:url(/_werkbank/fonts/InstrumentSans-Regular.ttf)}@font-face{font-family:'IDruck';font-weight:500;src:url(/_werkbank/fonts/InstrumentSans-Medium.ttf)}@font-face{font-family:'IDruck';font-weight:600 900;src:url(/_werkbank/fonts/InstrumentSans-SemiBold.ttf)}" +
    "@font-face{font-family:'MDruck';src:url(/_werkbank/fonts/DMMono-Regular.ttf)}:root{--serif:'TDruck','Arial Narrow',sans-serif!important;--sans:'IDruck',Arial,sans-serif!important;--mono:'MDruck',monospace!important}" +
    "body,body *{font-family:'IDruck',Arial,sans-serif}h1,h2,h3,h4,.mn-titel,[class*=mn-] b{font-family:'TDruck','Arial Narrow',sans-serif}.mn-haus,.mn-gang,.mn-gang span,.mn-ende span{font-family:'MDruck',monospace}" });
  await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(800);
  await p.pdf({ path: process.argv[2], format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); console.log('PDF', process.argv[2]); })();
'''


def bau():
    idx = os.path.join(WB, 'index.html')
    if not os.path.exists(idx):
        return
    t = open(idx, encoding='utf-8').read()
    open(os.path.join(WB, 'ki.html'), 'w', encoding='utf-8').write(ki_seite(t))
    k = karte_seite(t)
    if k:
        open(os.path.join(WB, 'karte.html'), 'w', encoding='utf-8').write(k)
        js = os.path.join(W, '_karte_pdf.js'); open(js, 'w', encoding='utf-8').write(PDF_JS)
        import sb_angebot as SA
        r = subprocess.run(['node', js, os.path.join(WB, SA.PDF_NAME)], capture_output=True, text=True, timeout=120)
        print(r.stdout.strip() or ('PDF nicht gebaut: ' + r.stderr[-300:]))


if __name__ == '__main__':
    bau()
