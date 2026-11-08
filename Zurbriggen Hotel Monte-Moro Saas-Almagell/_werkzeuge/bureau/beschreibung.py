#!/usr/bin/env python3
"""Beschreibung des Hotel Monte-Moro für den Schreibtisch des Stamms (Das Schaufenster · Website pflegen), 08.11.2026.
Vorlage: dieselbe Datei des Stamms der sieben Werkzeuge (Beschreibung eines Hauses für den Schreibtisch), Hauswerte des Monte-Moro.
   python3 _werkzeuge/bureau/beschreibung.py          schreibt beide Dateien neu und legt die Probe-Kopie an, falls sie fehlt
   python3 _werkzeuge/bureau/beschreibung.py --pruef  zeigt nur, was geschrieben würde
Der Server des Schaufensters (serve.py) ruft anlegen() beim Start selbst auf; die beiden Dateien entstehen so auch auf einem frischen Rechner.

Schreibt (Master Werkzeug-Bau 4.2 L17/L18):
  _Werkzeuge/haeuser/montemoro/haus.json                 Kennung, Name, Welt, Quelle
  _Werkzeuge/werkzeuge/website/haeuser/montemoro.json    Seiten, Bereiche, Listen des Hauses, Angaben, gesperrte Karten-Stellen
Nichts wird abgetippt: Seiten aus dem Menü der gebauten Website, Telefon, E-Mail und Ort aus dem Fuss von index.html,
Fotos der Bereiche nur, wenn sie auf der Seite stehen. Die Website selbst (website/) wird nur gelesen, nie geschrieben."""
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
WEB = PROJEKT / 'website'
STAMM = PROJEKT.parent / '_Werkzeuge'
HAUS = 'montemoro'
FOTO_SEITE = {'impressum.html': 'empfang', 'datenschutz.html': 'empfang'}   # Seiten ohne eigenes Foto: Bild für Google-Texte und Listen (Fotos der Website)
# Zeiten und Preise: Muster des Stamms (api.py › ZAHL), dazu wie das Hotel schreibt: «CHF 90.00», «25.–», «7 dl», «ca. 45 Min.», «2400m», «50 %».
# Jeder Treffer braucht eine Ziffer: eine Beschriftung wie «CHF» allein (Kopf des Bons) ist keine Angabe (Master 4.2 L15).
ZAHL = (r'((?:CHF|Fr\.|€|\bEUR)\s?\d|\b\d+\s?\.\d{2}\b|\d\s?(?:CHF|Uhr)\b|\b\d+\.–|\d+\s?(Minuten|Min\.|m²|m2|Personen|Pers\.|Nächte?|Nacht|Betten|Zimmer|Plätze|Gänge|Jahre|dl|km|m ü\. M\.|M\.ü\.M\.|%)'
        r'|\b\d{3,4}\s?m\b|\d{1,2}[.:]\d{2}\s?(?:[–-]|bis)\s?\d{1,2}[.:]\d{2}|\d{1,2}[.:]\d{2}\s?Uhr|\b\d{1,2} bis \d{1,2} Uhr)')


def lies(name):
    return (WEB / name).read_text(encoding='utf-8')


def name(teil):
    """Name eines Werkzeugs aus der einen Stelle (kleid/montemoro.js › namen), nie fest geschrieben."""
    js = (PROJEKT / '_werkzeuge' / 'oberflaeche' / 'kleid' / 'montemoro.js').read_text(encoding='utf-8')
    m = re.search(r"namen:\s*\{([^}]*)\}", js)
    n = dict(re.findall(r"(\w+):\s*'([^']*)'", m.group(1))) if m else {}
    return n.get(teil) or teil


def seiten():
    """Jede Seite, die das Menü der Website nennt, dazu Impressum und Datenschutz aus dem Fuss. 404.html gehört nicht dazu."""
    start = lies('index.html')
    menue = re.search(r'<nav class="kopf__nav"[^>]*>.*?</nav>', start, re.S)
    if not menue:
        sys.exit('Das Menü (nav.kopf__nav) steht nicht mehr in website/index.html: Beschreibung nicht geschrieben.')
    namen = ['index.html'] + [d for d in re.findall(r'href="([a-z-]+\.html)"', menue.group(0)) if d != 'index.html']
    namen += [d for d in re.findall(r'href="((?:impressum|datenschutz)\.html)"', start) if d not in namen]
    for d in namen:
        if not (WEB / d).is_file():
            sys.exit(f'{d} steht im Menü, liegt aber nicht in website/.')
    return list(dict.fromkeys(namen))


def angaben():
    h = lies('index.html')
    kt = re.search(r'<div class="f3-kt f3-kt--mitte">.*?</div>\s*</div>', h, re.S)
    b = kt.group(0) if kt else ''
    tel = re.search(r'href="tel:(\+\d+)"[^>]*>.*?<b>([^<]+)</b>', b, re.S)
    mail = re.search(r'href="mailto:([^"]+)"', b)
    ort = re.search(r'<br>(CH-\d{4} [^<·]+?)\s*·', b)
    if not (tel and mail and ort):
        sys.exit('Telefon, E-Mail oder Ort stehen nicht mehr im Fuss von index.html: Beschreibung nicht geschrieben.')
    q = 'website/index.html (gebaut aus website/bau.py › f3_kontakt(), inhalt/daten.py › HAUS)'
    return [{'key': 'telefon', 'label': 'Telefon des Hotels', 'art': 'telefon', 'wert': tel.group(2).strip(), 'link': 'tel:' + tel.group(1), 'quelle': q},
            {'key': 'mail', 'label': 'E-Mail des Hotels', 'art': 'mail', 'wert': mail.group(1).strip(), 'link': 'mailto:' + mail.group(1).strip(), 'quelle': q},
            {'key': 'ort', 'label': 'PLZ und Ort', 'art': 'text', 'wert': ort.group(1).strip(), 'quelle': q}]


def foto_da(key, dateien):
    """Ein Foto gilt nur, wenn es auf einer der Seiten des Bereichs steht (sonst bliebe die Kachel ohne Bild)."""
    return any(re.search(rf'assets/img/{re.escape(key)}-[smlx]\.webp', lies(d)) for d in dateien)


def beschreibung():
    s = seiten()
    rechts = [d for d in s if d in ('impressum.html', 'datenschutz.html')]
    karten = name('karten')
    im_karten = 'im ' + karten.split(' ', 1)[1] if karten.startswith('Das ') else karten
    website = [
        ('start', 'Startseite', 'Der erste Eindruck: das Haus in Saas-Almagell, die Zimmer, was im Preis dabei ist, das Saastal, das Spa nebenan, das Röstihüs und der Kidsclub.', ['index.html'], 'haus-winter-g'),
        ('zimmer', 'Zimmer', 'Hotelzimmer, Familienzimmer, die Residence Alpenhof und die Ferienwohnungen in den Häusern Apollo und Arizona.', ['zimmer.html'], 'z-dach'),
        ('preise', 'Preise', 'Zimmer mit Frühstück oder Halbpension, was inklusive ist, die Zuschläge und die Preise für Kinder.', ['preise.html'], 'fr-gross'),
        ('saastal', 'Saastal', 'Sommer und Winter im Saastal: Wandern, Skifahren, Ausflüge, Bergbahnen und Postauto.', ['saastal.html'], 'tal-sommer'),
        ('spa', 'Spa nebenan', 'Das Spa im Partnerhotel Pirmin Zurbriggen: was es bietet und was der Eintritt kostet.', ['spa.html'], 'spa-garten'),
        ('roestihues', 'Röstihüs', f'Das Restaurant des Hauses mit Stube und Sonnenterrasse. Die Karte selbst pflegen Sie {im_karten}.', ['roestihues.html'], 'gondel'),
        ('anreise', 'Anreise', 'Mit Zug und Postauto oder mit dem Auto ab Visp, die Ankunft im Dorf und der Kontakt.', ['anreise.html'], 'empfang'),
        ('recht', 'Rechtliches', 'Impressum und Datenschutz im Wortlaut des Hauses.', rechts, 'empfang'),
    ]
    fehlt = set(s) - {d for w in website for d in w[3]}
    if fehlt:
        sys.exit('Seiten ohne Bereich: ' + ', '.join(sorted(fehlt)))
    for k, n, t, sei, f in website:
        if not foto_da(f, sei if k != 'recht' else ['index.html', 'anreise.html']):
            sys.exit(f'Foto «{f}» des Bereichs {n} steht auf keiner seiner Seiten.')
    return {
        '_lies_mich': 'Beschreibung des Hauses für das Werkzeug «website» (Das Schaufenster · Website pflegen). Hotel Monte-Moro mit Restaurant Röstihüs, '
                      'Saas-Almagell (Familie Zurbriggen), nur Deutsch. Jeder Text, jede Zahl, jedes Foto wird aus den gebauten Seiten gelesen '
                      '(website/ des Projekts, nie geschrieben). Läuft im Rahmen des Hauses: http://127.0.0.1:9382/_werkzeuge/bureau/ '
                      '(Zurbriggen Hotel Monte-Moro Saas-Almagell/_werkzeuge/bureau/). Geschrieben von _werkzeuge/bureau/beschreibung.py, nie von Hand ändern.',
        'seiten': [dict({'datei': d}, **({'foto': FOTO_SEITE[d]} if d in FOTO_SEITE else {})) for d in s],
        'sprachen': [],
        'kopie': {'unter': 'website', 'ordner': ['assets']},
        # Die Karte des Röstihüs (Röstis, Cordon bleus, Hotelweine, Spritz, Dessert, Raclette) kommt aus dem Kartenbrett: hier gesperrt, mit Weg dorthin
        'gesperrt': [{'wahl': '#karte .rk, #roestihues .buch, #wein .wein__glaeser, #stube .bl__zeilen', 'werkzeug': 'karten'}],
        # Was das Haus nicht mehr zeigt oder doppelt führt und nie hier geändert wird: die Gratis-Anreise (abgelaufen am 31.10.2026, die Seite blendet sie
        # über data-bis aus), Zeichen der Familie (Pinselstrich), das Familienband (gehört der Familie, nicht diesem Haus) und das Fenster der Rezeption
        # (Gäste-Chat: seine Texte pflegt die Rezeption, nicht die Website); das Zählwerk (Ziffernwalzen 0–9 einer Uhrzeit, nur Zierde)
        'auslassen': ['[data-bis]', '.familienband', 'img[src$=".svg"]', 'section.chat', '.zaehlwerk'],
        'vorschau': {'ohne_skripte': ['assets/js/rezeption.js'], 'zusatz_css': '.fenster{overflow:clip}@media (hover:none){[data-ws-e],img[data-ws-b]{cursor:pointer}}'},
        'bild_groessen': r'-(?:s|m|l|x|\d{3,4}w?)$',
        # Listen des Hauses (Gruppe «Das Haus»): Ansichten auf dieselben Stellen der Seiten, kein zweites Datenmodell. Ein Eintrag lässt sich ändern
        # und ausblenden, nicht neu anlegen (das bleibt dem Bau der Website). Packages, Säle, Unterlagen, Stellen hat das Haus auf der Website nicht.
        'bereiche': {
            **{k: {'an': False} for k in ('packages', 'saele', 'unterlagen', 'stellen')},
            'zimmer': {'name': 'Zimmer und Wohnungen',
                       'satz': 'Hotelzimmer, Familienzimmer mit der Residence Alpenhof und die Ferienwohnungen Apollo und Arizona, je mit Name, Text, Angaben und Fotos.',
                       'quellen': [{'seite': 'zimmer.html', 'jedes': '#hotelzimmer div.bl, #ferienwohnungen div.bl', 'felder': [
                           {'key': 'name', 'label': 'Name', 'art': 'text', 'wo': 'p.bl__name', 'titel': True},
                           {'key': 'ueber', 'label': 'Zeile darüber', 'art': 'text', 'wo': '.bl__text p.ueber'},
                           {'key': 'satz', 'label': 'Text', 'art': 'lang', 'wo': 'p.bl__satz'},
                           {'key': 'zeilen', 'label': 'Angaben und Preise', 'art': 'liste', 'wo': 'ul.bl__zeilen li'},
                           {'key': 'bilder', 'label': 'Fotos', 'art': 'bilder', 'wo': '.bl__bilder'}]}]},
            'preisstufen': {'name': 'Preisliste',
                            'satz': 'Jede Zeile der Preisliste: Zimmer mit Frühstück oder Halbpension, Zuschläge und Kinderpreise, in CHF pro Person und Tag.',
                            'quellen': [{'seite': 'preise.html', 'jedes': '#preisliste .aus__matrix tbody tr', 'felder': [
                                            {'key': 'name', 'label': 'Zimmer', 'art': 'text', 'wo': 'th', 'titel': True},
                                            {'key': 'preise', 'label': 'Frühstück · Halbpension', 'art': 'liste', 'wo': 'td'}]},
                                        {'seite': 'preise.html', 'jedes': '#preisliste .aus__liste li', 'felder': [
                                            {'key': 'name', 'label': 'Bezeichnung', 'art': 'text', 'wo': 'span', 'titel': True},
                                            {'key': 'preis', 'label': 'Preis', 'art': 'zahl', 'wo': 'b'}]}]},
            'inklusive': {'name': 'Inklusive',
                          'satz': 'Was im Preis dabei ist, Zeile für Zeile wie auf dem Bon der Rezeption: Postauto, Bergbahnen, Frühstück, Racletteabend, Kidsclub, Parkplatz.',
                          'quellen': [{'seite': 'preise.html', 'jedes': '#bon .bon__zeilen li', 'felder': [
                              {'key': 'name', 'label': 'Was', 'art': 'text', 'wo': 'b', 'titel': True},
                              {'key': 'text', 'label': 'Im Wortlaut des Hauses', 'art': 'text', 'wo': 'small'},
                              {'key': 'zusatz', 'label': 'Rechts auf dem Bon', 'art': 'text', 'wo': 'em'}]}]},
        },
        'zahlen': {'muster': ZAHL},
        'kleid': {},
        'website': [{'key': k, 'name': n, 'satz': t, 'seiten': sei, 'foto': f} for k, n, t, sei, f in website],
        'angaben': angaben(),
        'google': {'an': True},
        'hochladen': {'an': True, 'ordner': 'assets/img'},
        'funktionen': ['leiste_klar'],
        'anleitung': '/_werkzeuge/bureau/anleitung.html',
    }


def haus():
    try:
        welt = json.loads((PROJEKT / '_kette/05-markenbauer/marke.json').read_text(encoding='utf-8')).get('welt') or 'grand'
    except (OSError, ValueError):
        welt = 'grand'
    return {'kennung': HAUS, 'name': 'Monte-Moro', 'welt': welt, 'quelle': str(PROJEKT),
            'hinweis': 'Hotel Monte-Moro mit Restaurant Röstihüs, Saas-Almagell (Familie Zurbriggen, Gastgeber Esther und Fabian Zurbriggen). Nur Deutsch. '
                       'Angelegt 08.11.2026 vom Bau-Agenten Schaufenster mit _werkzeuge/bureau/beschreibung.py. Die Quelle wird nur gelesen, nie beschrieben.'}


def schreib(p, d):
    neu = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
    if p.is_file() and p.read_text(encoding='utf-8') == neu:
        return f'{p.name}: unverändert'
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(neu, encoding='utf-8')
    tmp.replace(p)
    return f'{p.name}: geschrieben'


def anlegen():
    """Beide Dateien schreiben (nur wenn anders) und die Probe-Kopie anlegen, falls sie fehlt."""
    b, h = beschreibung(), haus()
    aus = [schreib(STAMM / 'haeuser' / HAUS / 'haus.json', h), schreib(STAMM / 'werkzeuge/website/haeuser' / f'{HAUS}.json', b)]
    aus.append(subprocess.run([sys.executable, str(STAMM / 'werkzeuge/website/probe.py'), HAUS], capture_output=True, text=True).stdout.strip())
    return aus


if __name__ == '__main__':
    if '--pruef' in sys.argv:
        print(json.dumps({'haus': haus(), 'beschreibung': beschreibung()}, ensure_ascii=False, indent=1))
        sys.exit()
    print('\n'.join(anlegen()))
