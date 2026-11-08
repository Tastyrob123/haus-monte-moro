#!/usr/bin/env python3
"""Das Kartenbrett · Hotel Monte-Moro, Saas-Almagell: liest die Karten und Preislisten des Hauses aus der Website (08.11.2026, C26 in der Form des Hauses).
Vorlage: karten_lesen.py des Stamms (dort je Abend eine Menükarte).

Nichts wird abgetippt. website/inhalt/daten.py wird als Text gelesen (ast, nie importiert) und geschrieben nach _daten/quelle/<karte>.json:
  · roestihues   Die Röstihüs-Karte: elf Röstis («Best of Röstis»), fünf Cordon bleus, Monte-Moro-Kopf, Raclette im Stübli (ROESTIS, CORDON, KOPF, RACLETTE);
                 Rubriken, Beilagen und Herkunft des Fleisches wörtlich aus der Speisekarte des Hauses (speisekarte.pdf, Stand 18.11.2024). Zwei Seiten.
  · wein-apero   Wein und Apéro: die zwei Hotelweine «von Fabian selber kreiert» (HOTELWEINE) und die Spritz der Speisekarte (darunter SPRITZ)
  · preisliste   Die Preisliste: Zimmer mit Frühstück und mit Halbpension (4-Gänge), was inklusive ist (PREISE, INKLUSIVE, EURO)
  · zuschlaege   Zuschläge und Kinder: Kurtaxe, Einzelzimmer, kurze Aufenthalte, Hund, Kinder im Zimmer der Eltern (ZUSCHLAEGE, KINDER, KINDER_SATZ, KINDER_EIGEN)
  · spa          Spa im Partnerhotel Pirmin Zurbriggen: Eintritt und 7 Tage Abo (SPA_TARIFE, SPA_SATZ, SPA_ANGEBOT, SPA_INKL)
Zwei Prüfwege, bricht bei jeder Abweichung ab:
  1. Wort für Wort: jedes Wort jeder Karte (Titel, Zeilen, Rubriken, Namen, Beschreibungen, Preise, Hinweise) steht in daten.py, in der Speisekarte
     (_daten/beleg/speisekarte-2024-11-18.txt, pdftotext der Speisekarte) oder auf der gebauten Website (roestihues.html, preise.html, spa.html).
  2. Gegen Speisekarte und Website: jeder Name mit seinem Preis steht so in der Speisekarte (Restaurant) bzw. auf preise.html / spa.html (Hotel).
Was das Haus nicht veröffentlicht (OFFEN in daten.py: Öffnungszeiten des Röstihüs …), steht auf keiner Karte.

    python3 _werkzeuge/carte/karten_lesen.py         schreibt _daten/quelle/ und prüft
"""
import ast, html, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')
QD = os.path.join(HIER, '_daten', 'quelle')
BELEG = os.path.join(HIER, '_daten', 'beleg', 'speisekarte-2024-11-18.txt')
PDF = os.path.join(os.path.dirname(os.path.dirname(HIER)), '_quelle', 'website', 'pdf', 'speisekarte.pdf')
SEITEN = ('roestihues.html', 'preise.html', 'spa.html')


class Fehler(Exception):
    pass


def daten():
    """Alle Zuweisungen NAME = … aus website/inhalt/daten.py als Werte (ohne die Datei auszuführen)."""
    p = os.path.join(WEB, 'inhalt', 'daten.py')
    text = open(p, encoding='utf-8').read()
    d = {}
    for k in ast.parse(text).body:
        if isinstance(k, ast.Assign) and len(k.targets) == 1 and isinstance(k.targets[0], ast.Name):
            v = k.value
            try:
                if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == 'dict' and not v.args:   # HAUS = dict(name=…, …)
                    d[k.targets[0].id] = {kw.arg: ast.literal_eval(kw.value) for kw in v.keywords}
                else:
                    d[k.targets[0].id] = ast.literal_eval(v)
            except ValueError:
                pass
    d['_text'] = text
    return d


def speisekarte():
    """Text der Speisekarte. Liegt das Kundenmaterial da (Zweig quelle), wird der Beleg im Revier aus der PDF erneuert und muss gleich bleiben."""
    if os.path.exists(PDF):
        import subprocess
        neu = subprocess.run(['pdftotext', PDF, '-'], capture_output=True, text=True).stdout
        alt = open(BELEG, encoding='utf-8').read() if os.path.exists(BELEG) else ''
        if alt and alt != neu:
            raise Fehler('Die Speisekarte im Kundenmaterial ist eine andere als der Beleg (_daten/beleg/): bitte prüfen, dann den Beleg erneuern')
        if not alt:
            os.makedirs(os.path.dirname(BELEG), exist_ok=True)
            open(BELEG, 'w', encoding='utf-8').write(neu)
    return open(BELEG, encoding='utf-8').read()


def spritz(sk):
    """Die Spritz der Speisekarte (Rubrik «Prosecco»): «Hugo Spritz: Prosecco, Holundersirup  Fr. 12.–» → (Name, Zutaten, Preis)"""
    aus = []
    for z in sk.splitlines():
        m = re.match(r'^(.+? Spritz): (.+?)\s+Fr\. (\d+\.–)\s*$', z.strip())
        if m:
            aus.append((m.group(1), m.group(2).strip(), m.group(3)))
    return aus


def chf(p):
    """Preis des Hotels wie auf der Website («CHF 90.00»); Prozent bleibt («50 %»)"""
    return p if '%' in p else 'CHF ' + p


def satzzeichen(t):
    """Nur die Typografie, der Wortlaut bleibt: «Mozzarella , Salami» → «Mozzarella, Salami», «Syrah,Merlot» → «Syrah, Merlot»"""
    return re.sub(r'\s+/\s+', ', ', re.sub(r',(?=[^\s\d])', ', ', re.sub(r'\s+,', ',', t)))   # «Übernachtungen / pro Tag» → «Übernachtungen, pro Tag» (Trenner des Hauses)


def eintraege(e):
    return [dict(name=satzzeichen(n), zutaten=satzzeichen(z), preis=p) for n, z, p in e]


def karte(ziel, name, unter, gruppe, foto, titel, datum, mit, rubriken, quelle, hinweis='', fuss=''):
    """rubriken: [(Titel, [(Name, Beschreibung, Preis)], Seite)]; Seite 0 oder 1 (Karten mit zwei Seiten)"""
    return dict(ziel=ziel, art='satz', key=ziel, name=name, unter=unter, gruppe=gruppe, ab='', plakat='', foto=foto, titel=titel, datum=datum, mit=mit,
                rubriken=[dict(titel=t, seite=s, eintraege=eintraege(e)) for t, e, s in rubriken], hinweis=hinweis, quelle=quelle, fuss=fuss)


def lesen():
    q, sk = daten(), speisekarte()
    H = q['HAUS']
    fuss_r = f'Restaurant Röstihüs · {H["name"]} · {H["plz_ort"]} · Tel. {H["tel"]} · {H["mail"]}'
    fuss_h = f'{H["name"]} · {H["plz_ort"]} · Tel. {H["tel"]} · {H["mail"]}'
    aus = {}
    # Röstihüs: Rubriken wie die Speisekarte («Best of Röstis», «Unsere Cordon bleus») und die Website («Zum Dessert», «Im Stübli»)
    kopf_n, kopf_z = re.match(r'^(.+?) \((.+)\)$', q['KOPF'][0]).groups()          # «Monte-Moro-Kopf (Eiweissschaum mit Schoko und Eis)»
    rac_n, rac_z = re.match(r'^(.+?) (mit .+)$', q['RACLETTE'][0]).groups()          # «Raclette gross mit Pellkartoffeln»
    beilagen = next(z.strip() for z in sk.splitlines() if z.startswith('Beilagen:'))
    fleisch = {m.group(1): m.group(0) for z in sk.splitlines() for m in [re.match(r'^(Schwein|Kalb|Poulet): .+$', z.strip())] if m}
    herkunft = 'Herkunft Fleisch: ' + ' · '.join(fleisch[k] for k in ('Schwein', 'Kalb', 'Poulet'))
    aus['roestihues'] = karte('roestihues', 'Die Röstihüs-Karte', 'Röstis und Cordon bleus', 'Restaurant Röstihüs', 'roesti-orange',
                              'Restaurant Röstihüs', q['TRADITION'], '',
                              [('Best of Röstis', q['ROESTIS'], 0), ('Unsere Cordon bleus', q['CORDON'], 1),
                               ('Zum Dessert', [(kopf_n, kopf_z, q['KOPF'][1])], 1), ('Im Stübli', [(rac_n, rac_z, q['RACLETTE'][1])], 1)],
                              'website/inhalt/daten.py ROESTIS, CORDON, KOPF, RACLETTE; Rubriken, Beilagen und Herkunft aus der Speisekarte (speisekarte.pdf, Stand 18.11.2024)',
                              hinweis=beilagen + '. ' + herkunft + '.', fuss=fuss_r)
    weine = [(n.replace('«Hotelwein» ', ''), f'{w} | {t.rstrip(", ")} | {g}', p) for n, w, t, g, p in q['HOTELWEINE']]
    aus['wein-apero'] = karte('wein-apero', 'Wein und Apéro', 'Hotelwein und Spritz', 'Restaurant Röstihüs', 'stuebli',
                              'Wein von Fabian', 'Restaurant Röstihüs · Saas-Almagell', q['ROESTI_GETRAENKE'].split('. ')[0] + '.',
                              [('«Hotelwein»', weine, 0), ('Zum Apéro', spritz(sk), 0)],
                              'website/inhalt/daten.py HOTELWEINE, SPRITZ, ROESTI_GETRAENKE; die übrigen Spritz aus der Speisekarte (Stand 18.11.2024)', fuss=fuss_r)
    zimmer = {}
    for art, was, p in q['PREISE']:
        zimmer.setdefault(was, []).append((art, '', chf(p)))
    aus['preisliste'] = karte('preisliste', 'Die Preisliste', 'Zimmer und Inklusive', 'Hotel Monte-Moro', 'fruehstueck',
                              'Preisliste des Hauses', 'pro Person und Tag · CHF', H['satz'],
                              [(was, e, 0) for was, e in zimmer.items()] + [('Inklusive', [(x, '', 'inkl.') for x in q['INKLUSIVE']], 0)],
                              'website/inhalt/daten.py PREISE, INKLUSIVE, EURO, HAUS satz (Seite preise.html)', hinweis=q['EURO'], fuss=fuss_h)
    k_titel, k_zusatz = re.match(r'^(.+?) \((.+?)\) (.+)$', q['KINDER_SATZ']).groups()[0], ' '.join(re.match(r'^(.+?) \((.+?)\) (.+)$', q['KINDER_SATZ']).groups()[1:])
    aus['zuschlaege'] = karte('zuschlaege', 'Zuschläge und Kinder', 'Kurtaxe, Kinder, Hund', 'Hotel Monte-Moro', 'kinder-rodel',
                              'Zuschläge und Kinder', 'Preisliste · CHF', '',
                              [('Zuschläge', [(n, '', chf(p)) for n, p in q['ZUSCHLAEGE']], 0),
                               (k_titel, [(n, '', chf(p)) for n, p in q['KINDER']], 0)],
                              'website/inhalt/daten.py ZUSCHLAEGE, KINDER, KINDER_SATZ, KINDER_EIGEN, EURO (Seite preise.html)',
                              hinweis=f'Kinderzuschläge: {k_zusatz}. {q["KINDER_EIGEN"]}. {q["EURO"]}', fuss=fuss_h)
    aus['spa'] = karte('spa', 'Spa im Partnerhotel', 'Hotel Pirmin Zurbriggen', 'Hotel Monte-Moro', 'spa-licht',
                       'Spa im Partnerhotel', 'Hotel Pirmin Zurbriggen · Saas-Almagell', q['SPA_SATZ'].split('. ', 1)[1],
                       [('Der Eintritt', [(n[0].upper() + n[1:], z, p) for n, p, z in q['SPA_TARIFE']], 0)],
                       'website/inhalt/daten.py SPA_TARIFE, SPA_SATZ, SPA_ANGEBOT, SPA_INKL (Seite spa.html)',
                       hinweis=q['SPA_ANGEBOT'] + ' ' + q['SPA_INKL'], fuss=fuss_h)
    pruefe(aus, q, sk)
    return aus


WORT = re.compile(r'[0-9A-Za-zÄÖÜäöüœéèêàâçÉÈÀ]+')


def _seite(f):
    t = open(os.path.join(WEB, f), encoding='utf-8').read()
    t = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))


def pruefe(aus, q, sk):
    """1. Wort für Wort gegen daten.py, Speisekarte und Website; 2. Name und Preis gegen Speisekarte bzw. Website; 3. nichts aus OFFEN."""
    try:
        web = {f: _seite(f) for f in SEITEN}
    except OSError:
        raise Fehler('website/roestihues.html, preise.html oder spa.html fehlt (Website erst bauen)')
    quelle = set(w.lower() for w in WORT.findall(q['_text'] + ' ' + sk + ' ' + ' '.join(web.values())))
    sk1 = re.sub(r'\s+', ' ', sk)
    fehl = []
    for z, d in aus.items():
        texte = [d['name'], d['unter'], d['gruppe'], d['titel'], d['datum'], d['mit'], d['hinweis'], d['fuss']]
        for r in d['rubriken']:
            texte.append(r['titel'])
            for x in r['eintraege']:
                texte += [x['name'], x['zutaten'], x['preis']]
                if d['gruppe'] == 'Restaurant Röstihüs':
                    n = x['name']
                    if not re.search(re.escape(n) + r'.{0,160}?Fr\. ' + re.escape(x['preis']), sk1) and not (n + ' ' + x['zutaten']).split(' (')[0] in sk1:
                        fehl.append(f'{z}: «{n} {x["preis"]}» steht so nicht in der Speisekarte')
                elif x['preis'] != 'inkl.':
                    zahl = x['preis'].replace('CHF ', '')
                    vorne, _, hinten = zahl.partition('.')
                    seite = web['spa.html' if z == 'spa' else 'preise.html']
                    namen = {x['name'], x['name'].lower(), x['name'].replace(', ', ' / ')}   # satzzeichen(): «… / pro Tag» der Website
                    if not any(n in seite or n in seite.lower() for n in namen) or not re.search(re.escape(vorne) + r' ?\.' + re.escape(hinten) if hinten else re.escape(zahl), seite):
                        fehl.append(f'{z}: «{x["name"]} {x["preis"]}» steht so nicht auf der Website')
        for t in texte:
            for w in WORT.findall(t):
                if w.lower() not in quelle:
                    fehl.append(f'{z}: Wort «{w}» nicht in der Quelle')
        alles = ' '.join(texte).lower()
        for o, _ in q['OFFEN']:
            if 'öffnungszeit' in alles or 'ruhetag' in alles:
                fehl.append(f'{z}: nennt etwas aus OFFEN ({o})')
                break
    for n, z, p in q['SPRITZ']:
        if not any(x['name'] == n and x['zutaten'] == z and x['preis'] == p for x in aus['wein-apero']['rubriken'][1]['eintraege']):
            fehl.append(f'wein-apero: «{n}» aus daten.py SPRITZ fehlt')
    if len(aus['roestihues']['rubriken'][0]['eintraege']) != 11 or len(aus['roestihues']['rubriken'][1]['eintraege']) != 5:
        fehl.append('roestihues: nicht elf Röstis und fünf Cordon bleus')
    if fehl:
        raise Fehler('Prüfung gegen die Quelle: ' + '; '.join(fehl[:12]))
    return True


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


if __name__ == '__main__':
    try:
        aus = lesen()
    except Fehler as e:
        sys.exit('ABBRUCH · ' + str(e))
    for f in os.listdir(QD):
        if f.endswith('.json') and f[:-5] not in aus and f != 'pruefung.json':
            os.remove(os.path.join(QD, f))
    bericht = {}
    for z, d in aus.items():
        _schreib(os.path.join(QD, z + '.json'), d)
        n = sum(len(r['eintraege']) for r in d['rubriken'])
        bericht[z] = dict(name=d['name'], eintraege=n, preise=sum(1 for r in d['rubriken'] for x in r['eintraege'] if x['preis']))
        print(f'{z}: {d["name"]} · {n} Einträge')
    _schreib(os.path.join(QD, 'pruefung.json'), dict(geprueft='Wort für Wort gegen website/inhalt/daten.py, die Speisekarte (Stand 18.11.2024) und die Website '
                                                  '(roestihues.html, preise.html, spa.html); Restaurant: Name und Preis gegen die Speisekarte; Hotel: Name und Preis gegen preise.html bzw. spa.html',
                                                  karten=bericht))
    print('Prüfung: gleich')
