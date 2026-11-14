#!/usr/bin/env python3
"""Karten & Preislisten · Hotel Monte-Moro, Saas-Almagell — setzt die Karten und Preislisten des Hauses neu, im Satz des Hauses (08.11.2026, Vorlage:
satz_bau.py des Stamms).

Grundlage ist die Machart des Hauses (Fehlerbuch 10a: das Original ist die Grundlage, nie schwächer): die Karte des Röstihüs auf der Website
(roestihues.html, Abschnitt «Die Karte», website/assets/css/bewegung.css .rk) und die Preisliste (preise.html): ein Blatt Papier mit doppelter
Messing-Linie, oben der Bergkamm bzw. das Logo, Rubriken in Fjalla One mittig mit kurzer Messing-Linie darunter, je Eintrag der Name in
Fjalla One, eine gepunktete Linie, rechts der Preis in Lärche tief, die Beschreibung klein darunter. Dazu unten die Nacht mit der Grat-Kante
(der Bergkamm der Website, .grat-oben) und darin die Adresse. Farben und Schriften aus dem Markenbuch (Nacht, Lärche, Messing, Papier;
Fjalla One, Instrument Sans, DM Mono), nie fett, nie kursiv; Lärche im Titel nur im letzten Wort.

Nichts ist abgetippt: jede Rubrik, jeder Name, jede Beschreibung, jeder Preis kommt aus _daten/quelle/<karte>.json (karten_lesen.py, gegen
daten.py, Speisekarte und Website geprüft). Typografisch anders (der Wortlaut bleibt): Trennstrich «|» als « · » wie auf der Website.
Gesperrte Versalien höchstens .08em (pdftotext, Abschnitt 9).

Aus dem Satz liest einlesen.py die Karte als Baum; satz/satz.js setzt daraus Zeichen für Zeichen dasselbe HTML (Vorschau, PDF, Werkbank).

    python3 _werkzeuge/carte/satz_bau.py          setzt alle Karten nach satz/u-<karte>.html, die Zeichen nach satz/zeichen.json
"""
import html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
QD = os.path.join(HIER, '_daten', 'quelle')
SATZ = os.path.join(HIER, 'satz')
KLEID = os.path.join(HIER, '..', 'oberflaeche', 'kleid')
NAME = 'Hotel Monte-Moro'
e = lambda t: html.escape(t, quote=False)


def _svg(datei, kl, symbol=None):
    """Logo (montemoro-marke.svg #wm) bzw. Bergkamm (montemoro-zeichen.svg) als eigenes svg, unverändert, nur als Ganzes eingesetzt."""
    s = open(os.path.join(KLEID, datei), encoding='utf-8').read()
    if symbol:
        m = re.search(r'<symbol id="%s" viewBox="([^"]+)">(.*?)</symbol>' % symbol, s, re.S)
        vb, innen = m.group(1), m.group(2)
    else:
        m = re.search(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>', s, re.S)
        vb, innen = m.group(1), m.group(2)
    innen = re.sub(r'\s+', ' ', innen.strip())
    return f'<svg class="{kl}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="currentColor">{innen}</svg>'


WM = _svg('montemoro-marke.svg', 'mm-wm', 'wm')
KAMM = _svg('montemoro-zeichen.svg', 'mm-kamm')


def q(kid):
    return json.load(open(os.path.join(QD, kid + '.json'), encoding='utf-8'))


def zeile(t):
    """Beschreibung: Trennstrich « | » als « · » wie auf der Website; der Wortlaut bleibt. Vor «·» ein geschütztes Leerzeichen: der Punkt
    beginnt nie eine Zeile."""
    return punkt(re.sub(r'\s*\|\s*', ' · ', t.strip()))


def punkt(t):
    return t.replace(' · ', '\xa0· ')


# ---------------------------------------------------------------- Bausteine
def eintrag(x):
    innen = f'<p class="sb-n">{e(x["name"])}</p>'
    if x['preis']:
        innen += f'<p class="sb-mp">{e(x["preis"])}</p>'
    if x['zutaten']:
        innen += f'<p class="sb-dr">{e(zeile(x["zutaten"]))}</p>'
    return f'<div class="sb-m">{innen}</div>'


def rubrik(r, i=0):
    ohne = '' if any(x['zutaten'] for x in r['eintraege']) else ' sb-r--knapp'
    return f'<section class="sb-r sb-r{i}{ohne}"><p class="sb-h">{e(r["titel"])}</p>' + ''.join(eintrag(x) for x in r['eintraege']) + '</section>'


def band(d):
    """Titel der Karte: das letzte Wort in Lärche (wie die Titel der Website); der Wortlaut bleibt."""
    t = d['titel']
    if ' ' in t:
        vorn, letzt = t.rsplit(' ', 1)
        return f'<h2 class="sb-band"><span class="sb-b1">{e(vorn)}</span> <span class="sb-b2">{e(letzt)}</span></h2>'
    return f'<h2 class="sb-band"><span class="sb-b2">{e(t)}</span></h2>'


def oben(d):
    return (f'<div class="sb-oben"><span class="uz sb-zeichen">{WM}</span>'
            f'{band(d)}<p class="sb-datum">{e(d["datum"])}</p>'
            + (f'<p class="sb-mit">{e(d["mit"])}</p>' if d.get('mit') else '') + '</div>')


def oben_weiter():
    """Zweite Seite: nur der Bergkamm (wie der Kopf der Karte auf der Website)."""
    return f'<div class="sb-oben sb-oben--weiter"><span class="uz sb-zeichen">{KAMM}</span></div>'


def unten(d):
    return f'<div class="sb-unten"><p class="sb-hinweis">{e(punkt(d["hinweis"]))}</p></div>' if d.get('hinweis') else ''


def blatt(inhalt, d, mx='1.6'):
    """Ein Blatt A4 hoch: Papier mit doppelter Messing-Linie, unten die Nacht mit der Grat-Kante und der Adresse."""
    return (f'<section data-max="{mx}" class="blatt mm" data-b="210" data-h="297" style="width:210mm;height:297mm">'
            f'<div class="inhalt">{inhalt}</div><footer class="ufuss2">{e(punkt(d.get("fuss") or NAME))}</footer></section>')


def doc(titel, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{e(titel)} · {e(NAME)}</title>\n'
            f'<link rel="stylesheet" href="satz.css"><style>@page{{size:210mm 297mm;margin:0}}</style></head><body>' + ''.join(seiten) + '</body></html>')


def karte(kid):
    d = q(kid)
    n = max(r.get('seite', 0) for r in d['rubriken']) + 1
    seiten = []
    for s in range(n):
        rub = [(i, r) for i, r in enumerate(d['rubriken']) if r.get('seite', 0) == s]
        menue = '<div class="sb-menue">' + ''.join(rubrik(r, i) for i, r in rub) + '</div>'
        kopf = oben(d) if s == 0 else oben_weiter()
        seiten.append(blatt(f'<div class="sb-quer">{kopf}{menue}{unten(d) if s == n - 1 else ""}</div>', d))
    return doc(d['name'], seiten)


def zeichen():
    """Feste Teile für satz.js: Logo, Bergkamm, Fusszeile."""
    return dict(ZEICHEN=KAMM, BLATT='<i></i>', FUSS=NAME, HAUS=NAME, WORTMARKE=WM)


def _schreib(p, t):
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        f.write(t)
    os.replace(p + '.neu', p)


if __name__ == '__main__':
    os.makedirs(SATZ, exist_ok=True)
    for f in os.listdir(SATZ):
        if f.startswith('u-') and f.endswith('.html'):
            os.remove(os.path.join(SATZ, f))
    for f in sorted(os.listdir(QD)):
        kid = f[:-5]
        if not f.endswith('.json') or kid in ('abend', 'pruefung'):
            continue
        _schreib(os.path.join(SATZ, f'u-{kid}.html'), karte(kid))
        print('gesetzt:', f'satz/u-{kid}.html')
    with open(os.path.join(SATZ, 'zeichen.json'), 'w', encoding='utf-8') as f:
        json.dump(zeichen(), f, ensure_ascii=False)
    print('Zeichen: satz/zeichen.json')
