"""Hotel Monte-Moro, Saas-Almagell: Inhalt der Werkbank («Alles auf einen Blick») und ihrer Beigaben.   Werkzeug: _Werkbank-Kit/ (unverändert)

Werkbank Kern Monte-Moro, 08.11.2026 (Auftrag Oberchef, _werkzeuge/AUFTRAG-GEMEINSAM.md; Roberts Deal: «kopieren, umkleiden, Hauswerte eintragen, nichts neu erfinden»).
Aufbau, Wege und Funktionen aus dem Stamm der Werkbänke, unverändert. Kleid aus der Website (website/assets/css/montemoro.css :root) und dem Markenbuch
(_kette/05-markenbauer/marke/): Nacht #0A2A4A, Nachtblau #0D3F6F, Tiefnacht #071B2E, Logo-Blau #115595; Lärche #C67144 als Akzent (in Titeln nur das letzte Wort),
Lärche tief #9A4F2B auf Hell, Messing #B39867 nur für feine Linien; Papier #F5F2EE, Fassade #E7E1DC, Creme #EFE9E1; Fjalla One für Titel (eine Stärke),
Instrument Sans zum Lesen, DM Mono gesperrt für Etiketten und Zahlen; der Bergkamm aus dem Logo als Zeichen, das ganze Logo als Wortmarke.
Fakten nur aus website/inhalt/daten.py, den Seiten der Website, _kette/03-sammler/fakten.json, _kette/04-analyst/potential.json; was in OFFEN steht, erscheint nicht.

Eigenes Revier: website/_werkbank/ ist der Projektordner des Kits (ROOT), die Website liegt eine Ebene höher (WEB) und wird nur gelesen;
assets/ ist ein Verweis auf website/assets (nur gelesen). Serviert von website/_werkbank/serve.py auf Port 9388 (zuerst das Revier, sonst die Website).
Ton: Hotel in der Schweiz, Sie-Form an Esther und Fabian Zurbriggen, Schweizer Schreibung (ss, «Guillemets»). Kein Preis für Roberts Arbeit in der Werkbank."""
import json
import os
import re as _re
import shutil
import sys
import glob as _glob
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # = website/_werkbank (Projektordner des Kits)
WEB = os.path.dirname(ROOT)                                          # = website/ (nur gelesen)
PROJ = os.path.dirname(WEB)
KLEID = os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid')
sys.path.insert(0, os.path.join(WEB, 'inhalt'))
import daten as D  # noqa: E402  (Hauswerte, nur gelesen)

_GROESSE = {'s': 480, 'm': 900, 'l': 1440, 'x': 2200}


def bild(key, hoechstens=2400):
    """Grösste Fassung eines Fotos der Website bis «hoechstens» Pixel Breite (assets/img/<key>-<s|m|l|x>.webp) als voller Pfad für K.hausbild."""
    da = [(b, s) for s, b in _GROESSE.items() if b <= hoechstens and os.path.exists(os.path.join(WEB, 'assets', 'img', f'{key}-{s}.webp'))]
    if not da:
        raise FileNotFoundError(f'Bild {key} fehlt in website/assets/img')
    return os.path.join(WEB, 'assets', 'img', f'{key}-{max(da)[1]}.webp')


NAME = 'Hotel Monte-Moro'
KURZ = 'montemoro'
LEISTE = ''          # das Zeichen steht in der Leiste schon (keine doppelten Logos, Kriterium 14)
HAUSART = 'hotel'
PORT = 9388
DOMAIN = 'monte-moro.ch'
HEUTE_URL = 'https://www.monte-moro.ch/de/'
ANREDE = 'Für Esther und Fabian Zurbriggen'
RECHTE = 'dem Hotel Monte-Moro, der Familie Zurbriggen und den jeweiligen Fotografen.'
START_MS = 4200
WAHL = 'body > section, body > header, main > section'
ADRESSE = f'{D.HAUS["name"]} · {D.HAUS["plz_ort"]}'   # eine Strasse ist nicht belegt (daten.OFFEN)
PREIS_AB = D.PREISE[0][2]                              # Budgetzimmer mit Frühstück, pro Person / Tag

# ---------- Farben: die der Website (website/assets/css/montemoro.css :root) ----------
# Im Kit heisst der Akzent «gold»: hier die Lärche der Balkone. «messing» bleibt Messing (feine Linien), «rot» die Lärche tief (Betonung auf Hell).
FARBEN = dict(nacht='#0a2a4a', tief='#071b2e', navy='#0d3f6f', blau='#115595', papier='#f5f2ee', creme='#efe9e1', weiss='#f5f2ee',
              gold='#c67144', messing='#b39867', taupe='#4a5d70', tinte='#13263a', punkt='#c67144', rot='#9a4f2b')
SCHRIFT = dict(titel=('Fjalla One', 'FjallaOne-400.woff2'), titel_folge="'Arial Narrow',sans-serif", ersatz="local('Arial Narrow')", druckgewicht=400)
SCHRIFT_MEHR = []
DRUCKQUELLEN = []   # feste Druckschnitte legt _werkbank/druckschrift.py an (Werkbank Papier)
DRUCKSCHRIFT = [('Fjalla One', 400, 'FjallaOne-Regular.ttf'), ('Fjalla One', 500, 'FjallaOne-Regular.ttf'), ('Fjalla One', 700, 'FjallaOne-Regular.ttf')]
# Die Webschriften der Website unter den Namen, die der Kit erwartet (werkbank/fonts)
_WF = os.path.join(ROOT, 'werkbank', 'fonts')
os.makedirs(_WF, exist_ok=True)
for _f in ('FjallaOne-400.woff2', 'InstrumentSans-normal-400_600.woff2', 'DMMono-normal-400.woff2'):
    if os.path.exists(os.path.join(WEB, 'assets', 'fonts', _f)):
        shutil.copy2(os.path.join(WEB, 'assets', 'fonts', _f), os.path.join(_WF, _f))
# Muster: die Tapete des Markenbuchs (Grate in feinen Linien, website/assets/zeichen/tapete-*.svg), ohne eigene Grundfläche, damit sie auf jeder Fläche liegt
_EI = os.path.join(ROOT, 'werkbank', 'eigen')
os.makedirs(_EI, exist_ok=True)
for _q, _z in (('tapete-dunkel.svg', 'tapete-dunkel.svg'), ('tapete-hell.svg', 'tapete-hell.svg')):
    _t = open(os.path.join(WEB, 'assets', 'zeichen', _q), encoding='utf-8').read()
    open(os.path.join(_EI, _z), 'w', encoding='utf-8').write(_re.sub(r'<rect width="480" height="480" fill="#[0-9A-Fa-f]{6}"/>', '', _t, count=1))
MUSTER = 'url(/werkbank/eigen/tapete-dunkel.svg)'
MUSTER_B = '240px'
MUSTER_DRUCK = '18mm'
# Das Zeichen: der Bergkamm aus dem Logo (Kleid der Werkzeuge), unverändert übernommen, nie nachgezeichnet. Breit (viewBox 3483 × 696).
_ZC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen', 'zeichen-haus.svg')
os.makedirs(os.path.dirname(_ZC), exist_ok=True)
open(_ZC, 'w', encoding='utf-8').write(open(os.path.join(KLEID, 'montemoro-zeichen.svg'), encoding='utf-8').read())
ZEICHEN = K.svg_innen(_ZC)
ZEICHEN = (ZEICHEN[0], _re.sub(r'\s+fill="(?:#000|#000000|black)"', '', ZEICHEN[1]))   # Farbe über currentColor


def _wortmarke():
    """Das ganze Logo «Monte Moro / Saas-Almagell» aus _werkzeuge/oberflaeche/kleid/montemoro-marke.svg (Symbol «wm»)."""
    s = open(os.path.join(KLEID, 'montemoro-marke.svg'), encoding='utf-8').read()
    m = _re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, _re.S)
    vb = ' '.join(str(float(x)).rstrip('0').rstrip('.') for x in m.group(1).split())
    return vb, _re.sub(r'\s+fill="currentColor"', '', _re.sub(r'\s*\n\s*', ' ', m.group(2))).strip()


WORT = _wortmarke()
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer', einzahl='Untersetzer')

SEITEN = [   # alle Seiten, die ein Gast als Seite wahrnimmt, dazu das Rechtliche (Sätze nur aus dem, was auf der Seite steht)
    ('index.html', 'Startseite', 8, 'Das Haus in der Sonne, die Zimmer, was im Preis steckt, das Saastal ab dem Haus, das Spa nebenan, das Röstihüs, die Kinder und der Wein von Fabian.', ''),
    ('zimmer.html', 'Zimmer', 5, 'Die Hotelzimmer mit Balkon, jede Zimmerart mit ihren Fotos zum Öffnen, die Familienzimmer und die Ferienwohnungen Haus Apollo und Haus Arizona.', ''),
    ('preise.html', 'Preise', 3, 'Was im Preis steckt, die Zimmer mit Frühstück und Halbpension, Zuschläge, Kinder und was man vor dem Buchen wissen will.', ''),
    ('roestihues.html', 'Röstihüs', 3, 'Die Stube des Röstihüs, regional und herzlich, und die Karte mit Röstis, Cordon bleus und den Hotelweinen.', ''),
    ('spa.html', 'Spa', 4, 'Das Spa im Partnerhotel Pirmin Zurbriggen: der Weg hinüber, was es dort gibt und was der Eintritt kostet.', ''),
    ('saastal.html', 'Saastal', 4, 'Zu Fuss vom Haus zum Lift, zum Bus und ins Dorf, das Saastal im Sommer und im Winter.', ''),
    ('anreise.html', 'Anreise', 4, 'Mit Zug und Postauto über Visp oder mit dem Auto durchs Vispertal bis vor das Haus.', ''),
    ('impressum.html', 'Rechtliches', 1, 'Impressum und Datenschutz.', 'recht'),
]
LANG = {'Startseite': 'Startseite', 'Rechtliches': 'Impressum und\u00a0Datenschutz'}   # «und Datenschutz» bleibt zusammen (Tor: Einzelwort)
KURZNAME = {}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import namen_fall as _nf  # noqa: E402


def _werkzeugname(teil):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/montemoro.js › namen), nie fest geschrieben."""
    k = open(os.path.join(KLEID, 'montemoro.js'), encoding='utf-8').read()
    return dict(_re.findall(r"(\w+):\s*'([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', k).group(1)))[teil]


# ---------- Unterlagen: die Karte des Röstihüs (gesetzt mit dem Kartenbrett, PDFs in unterlagen/pdf; Texte überschreibt papier_haus.json) ----------
SATZ_FUSS = ADRESSE
UNTERLAGEN = dict(
    pflege=('Karten selbst ändern', 'http://127.0.0.1:9383/_werkzeuge/carte/'),
    text='Die Karte des Röstihüs, neu gesetzt neben den Seiten, wie sie heute auf dem Tisch liegen: die Röstis, die Cordon bleus, der Wein von Fabian und der Apéro.',
    seite_text='Die Karte des Röstihüs, neu gesetzt im Kleid der neuen Seite. Links das Blatt von heute, rechts die Idee. Jede neue Karte schreiben Sie ' + _nf.in_(_werkzeugname('karten')) + '.',
    knopf2=('Das Röstihüs auf der Website', '../roestihues.html'))
FAECHER = [(_z, _n) for _z, _n in (('roestihues', 'Röstihüs'), ('wein-apero', 'Weinkarte')) if os.path.exists(os.path.join(ROOT, 'unterlagen', 'pdf', _z + '.pdf'))]

# ---------- Auftakt, Brief ----------
AUFTAKT = dict(
    titel=['Mehr erleben', 'im Saastal.'],
    text='Die neue Website des Hotel Monte-Moro, so wie sie werden könnte. Dazu sieben Werkzeuge, mit denen Sie Zimmer, Preise, die Karte des Röstihüs und die Anfragen Ihrer Gäste selbst führen, und Ideen für Papier und Instagram.',
    abzuege=[(bild('roesti-stube'), 'Im Röstihüs'), (bild('z-dach'), 'Ein Zimmer unter dem Dach'), (bild('gondel'), 'Die Gondeln vor dem Röstihüs')])
BRIEF = dict(
    art='kurz',
    bild=bild('haus-sommer-g'), schnitt=2.0, lage=(.5, .55), bild_alt='Das Hotel Monte-Moro im Sommer, mit den Balkonen aus Lärche und der Sonnenterrasse',
    schild=('Hotel Monte-Moro', 'Saas-Almagell · Saastal'), ort='Tasty Studios',
    absaetze=[
        f'Wer bei Ihnen wohnt, bekommt mehr, als der Preis vermuten lässt: ein Zimmer mit Balkon und Frühstück ab CHF {PREIS_AB}, dazu die Postautos im ganzen Saastal und im Sommer die Bergbahnen. Abends wartet das Röstihüs, und einmal in der Woche ist im Stübli Racletteabend. Die neue Seite soll das zeigen, bevor ein Gast zum ersten Mal ankommt.',
        'Heute steht das Monte-Moro auf monte-moro.ch, auf Booking.com und bei Google. Zimmer, Preise, Röstihüs und Spa verteilen sich dort auf viele Seiten; manches steht erst im Buchungsfenster oder in einer Druckdatei. Die neue Seite stellt alles an einen Ort: die Zimmer mit allem, was inbegriffen ist, die Preise, das Röstihüs, das Spa nebenan, das Saastal und den Weg zu Ihnen.',
        'Um die Seite herum liegt, was Sie im Alltag brauchen: die Karte des Röstihüs neu gesetzt, Ideen für Papier und Instagram und sieben Werkzeuge, in denen Sie Zimmer, Preise, Karte und Anfragen selbst führen. Alles hier lässt sich anklicken und ausprobieren. Ich freue mich über ein Gespräch darüber, wie daraus Ihre Website werden kann.'],
    schluss=f'<q>{D.HAUS["satz"]}</q> <small>Hotel Monte-Moro</small>',
    abzuege=[])
GABEN = dict(seite='{n} Seiten.', unterlagen='Ihre Karte.', papier='{d} Drucksachen und {e} Untersetzer.', feed='{n} Beiträge.', gaeste='Für Ihre Gäste.', studio='')
GABEN_BILDER = dict(seite=(bild('haus-sommer'), (.5, .5)), unterlagen=(bild('roesti-tische'), (.5, .5)), papier=(bild('stube-holz'), (.5, .3)), material=(bild('fr-tisch'), (.5, .5)), gaeste=(bild('empfang'), (.5, .5)))
LAUFWORTE = ['Hotel Monte-Moro', '<b>Saas-Almagell</b>', D.HAUS['satz'], 'Röstihüs', '<b>Saastal</b>', 'Familie Zurbriggen']
REIHENFOLGE = ['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'papier', 'material', 'dazu', 'schluss']   # der Feed kommt als eigene Bühne (feed_buehne.py)

# ---------- Website: Ideen (Aufnahmen _werkbank/sb_ideen.js → ansichten/Ideen), Vergleich (sb_heute.py → ansichten/Vorher) ----------
IDEEN = [   # (Aufnahme, Titel, Satz, Ausschnitt): jeder Satz nur aus dem, was auf der Aufnahme zu sehen ist
    ('Ideen/start', 'Bei uns scheint fast immer die Sonne.', 'Das Haus mit seinen Balkonen aus Lärche über den ganzen Schirm, darüber der Satz der Startseite; Anreise, Abreise und Gäste wählt man gleich im ersten Bild.', '50% 50%'),
    ('Ideen/zimmer', 'Schöne Hotelzimmer, schöne Ferien.', 'Gleich nach dem Auftakt die Zimmer: 18 Zimmer und 55 Betten als grosse Ziffern, daneben Fotos unter dem Dach und am Bett.', '50% 50%'),
    ('Ideen/bon', 'Mehr erleben, weniger zahlen.', 'Was im Preis steckt, steht wie auf einem Bon des Hauses: Postauto, Bergbahnen, Frühstück, Raclette, Kidsclub und Parkplatz, jede Zeile «inkl.».', '50% 50%'),
    ('Ideen/saastal', 'Zwei Minuten bis zum Lift.', 'Ein Plan vom Haus zum Skigebiet, zur Busstation und in den Dorfkern, jede Strecke in Gehminuten.', '50% 50%'),
    ('Ideen/spa', 'Nach dem Lift: das Spa nebenan.', 'Ruheraum und Sauna im Partnerhotel Pirmin Zurbriggen, gross in Fotos, die man nacheinander betritt.', '50% 50%'),
    ('Ideen/roesti', 'Es lebe die Tradition!', 'Die Stube des Röstihüs und die beleuchteten Gondeln vor dem Haus, auf der Nacht wie ein Abend im Dorf.', '50% 50%'),
    ('Ideen/kinder', 'Die Kinder bis 21 Uhr.', 'Die Zeiten des Kidsclubs, 16:30 bis 21:00, als grosse Ziffern neben Rodelbahn, Murmeltier und Spielburg.', '50% 50%'),
    ('Ideen/wein', 'Wein von Fabian.', 'Die zwei Hotelweine als Gläser mit Namen, Winzer und Preis, daneben das Stübli mit seinen Butzenscheiben.', '50% 50%'),
    ('Ideen/schluss', 'Und morgen scheint die Sonne wieder.', 'Am Ende der Seite noch einmal das Buchen über dem Nebelmeer, darunter die Anreise in Minuten.', '50% 50%'),
    ('Ideen/preise', 'Gut zu wissen, bevor Sie buchen.', 'Die ganze Preisliste auf einem Blatt: Zimmer mit Frühstück und Halbpension, Zuschläge, Kurtaxe und Kinder nach Alter.', '50% 50%'),
    ('Ideen/karte', 'Heute Abend im Röstihüs.', 'Die Karte als Blatt auf dem Tisch: Röstis, Cordon bleus, das Dessert und der Wein von Fabian, jede Zeile mit ihrem Preis.', '50% 50%'),
    ('Ideen/anreise', 'Visp, Stalden, Saas-Grund, Saas-Almagell.', 'Die Anreise als Weg durchs Tal, von Visp bis vor das Haus, mit der Zeit für Zug und Postauto und für das Auto.', '50% 50%'),
]
VORHER = [   # «heute» ist die Aufnahme der heutigen Startseite durch den Analysten (17.10.2026, _kette/04-analyst/_bau/stellen/d8.1.png), «neu» die neue Seite
    ('startseite', 'Startseite', 'Die Startseite, einmal neu.',
     ['Heute beginnt monte-moro.ch mit dem Logo, einem Bild der Rezeption und zwei grünen Geschenk-Kacheln. Neu steht das Haus in der Sonne über den ganzen Schirm, und Anreise, Abreise und Gäste stehen gleich im ersten Bild.',
      'Was das Haus ausmacht, steht in einem Satz, bevor die Seite erzählt: Bei Ihnen scheint fast immer die Sonne, und im Preis steckt mehr, als man denkt.',
      'Zimmer, Preise, Röstihüs, Spa, Saastal und Anreise haben je ihre eigene Seite.'], 'index.html'),
]
VERGLEICH_TEXT = 'Links, wie monte-moro.ch heute beginnt, rechts die neue Seite. Den Griff schieben Sie hin und her, daneben steht, was neu ist.'


def gefuege(z):
    n = [
        ['fotos', 0, 0, 'Ihre Fotos', 'Haus, Zimmer, Stube, Tal', 'ein', 'Ihre Fotos', 'Die Aufnahmen Ihrer Seite, von Schweiz Tourismus und von Booking.com: das Haus im Sommer und Winter, die Zimmer, das Röstihüs, das Saastal.', ['Haus', 'Zimmer', 'Tal']],
        ['preise', 0, 1, 'Ihre Preisliste', 'Zimmer und Zuschläge', 'ein', 'Ihre Preisliste', 'Zimmer mit Frühstück und Halbpension, Kurtaxe, Einzelzimmer, Kinder nach Alter und der Hund pro Tag.', ['Preise', 'Kinder']],
        ['karte', 0, 2, 'Ihre Karte', 'Röstihüs', 'ein', 'Ihre Karte', 'Elf Röstis, fünf Cordon bleus, die zwei Hotelweine von Fabian, Spritz und der Monte-Moro-Kopf.', ['Röstis', 'Weine']],
        ['texte', 0, 3, 'Ihre Worte', 'aus Ihrer Seite', 'ein', 'Ihre Worte', '«Mehr erleben, weniger zahlen.», «Es lebe die Tradition!», «Bei uns scheint fast immer die Sonne»: Ihre Sätze tragen die neue Seite.', ['Sätze']],
        ['zeichen', 0, 4, 'Ihr Logo', 'Bergkamm und Name', 'ein', 'Ihr Logo', 'Der Bergkamm und der Name Monte Moro aus Ihrem Logo, nachgezogen, in jeder Grösse scharf.', ['Bergkamm']],
        ['inklusive', 0, 5, 'Was inbegriffen ist', 'Postauto, Bergbahnen', 'ein', 'Was inbegriffen ist', 'Postautos im ganzen Saastal, im Sommer alle Bergbahnen ausser der Metro Alpin, Frühstücksbuffet, Racletteabend, Kidsclub und Parkplatz.', []],
        ['bildwelt', 1, 0, 'Bildwelt', 'jedes Foto mit festem Platz', '', 'Bildwelt', 'Jedes Foto liegt in mehreren Grössen vor, für den Rechner und fürs Handy, und sitzt mit seinem Ausschnitt fest.', ['Ausschnitt', 'Grössen']],
        ['daten', 1, 1, 'Preise und Zeiten', 'eine Stelle', '', 'Preise und Zeiten', 'Jeder Preis, jede Zeit und jede Angabe zum Haus steht einmal; jede Seite liest von dort.', ['Preise', 'Zeiten']],
        ['buchen', 1, 2, 'Buchen bei Ihnen', 'über Ihr Buchungsfenster', '', 'Buchen bei Ihnen', 'Anreise, Abreise und Gäste wählt der Gast auf der Seite; gebucht wird wie heute in Ihrem eigenen Buchungsfenster.', []],
        ['muster', 1, 3, 'Nacht und Lärche', 'wie das Haus', '', 'Farben und Form', 'Das Blau des Logos als Nacht, die Lärche der Balkone als Akzent, die Fassade als Papier und der Grat der Berge als Kante über den Bildern.', ['Farben', 'Grat']],
        ['zimmerarten', 1, 4, 'Die Zimmerarten', 'jede zum Öffnen', '', 'Die Zimmerarten', 'Jede Zimmerart öffnet sich mit allen Fotos, der Ausstattung, den Preisen und dem, was inbegriffen ist.', []],
        ['familie', 1, 5, 'Familie Zurbriggen', 'die Häuser der Familie', '', 'Familie Zurbriggen', 'Am Ende jeder Seite die Häuser der Familie, vom Wellness & Spa Pirmin Zurbriggen bis Zermatt.', []],
        ['start', 2, 0, 'Startseite', 'fast immer Sonne', 'seite', 'Startseite', 'Vom Haus in der Sonne über die Zimmer und was inbegriffen ist zum Saastal, zum Spa, zum Röstihüs, zu den Kindern und zum Wein von Fabian.', ['Sonne', 'Bon']],
        ['zimmer', 2, 1, 'Zimmer', 'mit Balkon', 'seite', 'Zimmer', 'Die Hotelzimmer, die Familienzimmer und die Ferienwohnungen Haus Apollo und Haus Arizona.', []],
        ['preisseite', 2, 2, 'Preise', 'alles schon dabei', 'seite', 'Preise', 'Was im Preis steckt, die Preisliste und was man vor dem Buchen wissen will.', []],
        ['roesti', 2, 3, 'Röstihüs', 'es lebe die Tradition', 'seite', 'Röstihüs', 'Die Stube und die Karte mit Röstis, Cordon bleus und Hotelweinen.', []],
        ['tal', 2, 4, 'Spa, Saastal, Anreise', 'rund ums Haus', 'seite', 'Spa, Saastal, Anreise', 'Das Spa nebenan, das Tal im Sommer und im Winter und der Weg über Visp.', []],
        ['anfrage', 3, 0, 'Anfragen', 'im Fenster', 'sys', 'Anfragen', 'Zimmer, Familienzimmer, Ferienwohnung oder Tisch im Röstihüs: Die Anfrage öffnet sich auf der Seite und kommt im Werkzeug an, nie als Mail.', []],
        ['chat', 3, 1, 'Fragen an die Rezeption', 'im Chat', 'sys', 'Fragen an die Rezeption', 'Ein Gast fragt nach Hund, Anreise oder Kidsclub; die Antwort kommt nur aus dem, was auf Ihren Seiten steht.', []],
        ['pdf', 3, 2, 'Karte als PDF', 'zum Teilen', 'sys', 'Karte als PDF', 'Die Karte des Röstihüs liegt zusätzlich als PDF bereit.', []],
        ['studio', 3, 3, 'Sieben Werkzeuge', 'für Sie', 'sys', 'Sieben Werkzeuge', 'Mit ihnen tragen Sie Zimmer, Preise, Karte und Texte selbst ein; jede Änderung wartet als Entwurf.', ['Preise', 'Karte']],
    ]
    k = [['fotos', 'bildwelt'], ['fotos', 'zimmerarten'], ['preise', 'daten'], ['karte', 'pdf'], ['karte', 'roesti'], ['texte', 'start'], ['zeichen', 'muster'], ['inklusive', 'daten'],
         ['bildwelt', 'start'], ['bildwelt', 'zimmer'], ['daten', 'preisseite'], ['daten', 'start'], ['buchen', 'start'], ['buchen', 'zimmer'], ['zimmerarten', 'zimmer'], ['familie', 'tal'],
         ['zimmer', 'anfrage'], ['roesti', 'anfrage'], ['start', 'chat'], ['studio', 'preisseite'], ['studio', 'roesti'], ['studio', 'start']]
    return {'sp': ['Von Ihnen', 'Daraus gemacht', 'Die Seiten', 'Im Hintergrund'], 'fx': [0.118, 0.372, 0.628, 0.882], 'n': n, 'k': k,
            'tour': ['fotos', 'preise', 'karte', 'anfrage', 'chat', 'studio'], 'fuss': 'Folgen Sie einer Linie: Sie führt von dem, was von Ihnen kommt, zur Seite',
            'start': ['Übersicht', 'Von Ihnen zur Seite', 'Tippen Sie eine Kachel an, dann leuchtet ihr Weg. Oder starten Sie den Rundgang.']}


# ---------- Für Ihre Gäste (Gäste-Funktionen der Website, Aufnahmen sb_ideen.js → ansichten/Gaeste) ----------
GAESTE = [
    ('buchen', 'Ein Zimmer buchen', 'Anreise, Abreise und Gäste stehen gleich im ersten Bild der Startseite; «Zimmer buchen» führt in Ihr Buchungsfenster.', '50% 50%'),
    ('zimmer', 'Jede Zimmerart zum Öffnen', 'Ein Klick öffnet die Zimmerart über den ganzen Schirm: alle Fotos, die Ausstattung, die Preise und was inbegriffen ist.', '50% 0'),
    ('anfrage', 'Anfragen ohne Mailprogramm', 'Zimmer, Familienzimmer, Ferienwohnung oder Tisch im Röstihüs: Die Anfrage öffnet sich auf der Seite. Im Entwurf wird nichts verschickt.', '50% 50%'),
    ('chat', 'Fragen an die Rezeption', 'Unten rechts auf jeder Seite: Fragen zu Preisen, Hund, Anreise oder Kidsclub, beantwortet aus dem, was auf Ihren Seiten steht.', '50% 50%'),
    ('inklusive', 'Was inbegriffen ist', 'Postauto, Bergbahnen im Sommer, Frühstück, Racletteabend, Kidsclub und Parkplatz auf einen Blick.', '50% 50%'),
    ('anreise', 'Der Weg zu Ihnen', 'Mit Zug und Postauto über Visp oder mit dem Auto durchs Vispertal, beide Wege mit ihrer Zeit.', '50% 50%'),
]
GAESTE_TEL = []
GAESTE_KNOEPFE = [('Zimmer ansehen', '../zimmer.html'), ('Die Preise', '../preise.html'), ('Die Anreise', '../anreise.html')]
GAESTE_LINK = '../zimmer.html'
GABEN['gaeste'] = 'Buchen, die Zimmerarten, Anfragen, die Rezeption im Chat, was inbegriffen ist und der Weg.'

# ---------- Handschrift (marke_werkbank.py) ----------
HANDSCHRIFT = dict(
    text='Ihr Haus hat schon, was eine Marke braucht: den Bergkamm im Logo, das Blau des Namens und die Lärche der Balkone. Die Seite nimmt das auf.',
    marke_etik='Logo', marke_text='Der Bergkamm und der Name kommen aus Ihrem Logo und bleiben in jeder Grösse scharf: Logo-Blau auf Hell, Papier auf der Nacht, nie neu gesetzt.',
    schriften=[], farben=[], farben_etik='aus Logo, Fassade und Fotos',
    muster_etik='Die Tapete',
    muster_text='Auf ruhigen Flächen liegt eine Tapete aus feinen Graten, Ton in Ton, dazu über jedem grossen Bild die Kante eines Bergkamms. Man findet beides auf der Seite und auf den Drucksachen.',
    knopf_text='Diese Knöpfe darf man drücken.', knoepfe=('Ausprobieren', 'Noch einmal'))

# ---------- Feed, Papier, Dateien (Texte der Papier-Seiten: papier_haus.json über mit_papier, Werkbank Papier) ----------
FEED = dict(art='bogen', bogen=[1, 2, 3, 4, 5, 6, 7, 8, 9], bogen_zeile='Die ersten drei Reihen',
            text1='', text2='Tippen Sie auf den Bildschirm, dann scrollen Sie durch den Feed wie am Handy.', kacheln=[])
PAPIER = dict(
    etik_text='Zum Bier im Röstihüs gehört ein Untersetzer: zwölf Ideen mit dem Bergkamm, der Lärche der Balkone und den Sätzen des Hauses.',
    druck_text='Von der Karte im Röstihüs bis zum Willkommensbrief im Zimmer, dazu <a href="../sticker/index.html" target="_blank" rel="noopener">Sticker</a> und <a href="../beigaben/index.html" target="_blank" rel="noopener">Beigaben</a>.',
    orte_e=[(3, 6, 28, -3), (36, 6, 28, 2), (69, 6, 28, -2), (3, 54, 28, 2), (36, 54, 28, -3), (69, 54, 28, 3)],
    orte_d=[('pw-roestihues-best-of-roestis', 3, 16, 29, -3, 0), ('pw-aushang-inklusive', 35.5, 16, 29, 2, 0), ('pw-willkommensbrief', 68, 16, 29, -2, 0)])   # Stücke der Hausdruckerei (papier_haus.json)
PAPIER_SEITE = dict(breit=set(), formen=set(), auslage=[], karton={}, titel={}, schatten=set(), flaeche=['fl--papier', 'fl--nacht tapete-leicht', 'fl--papier', 'fl--creme'],
                    etik_titel=('Untersetzer', 'fürs Röstihüs.'), etik_text='', etik_kap='Die Untersetzer', etik_kopf=['Zwölf', 'Untersetzer.'], etik_kopftext='', druck_text='', etik_auslage=[])
MATERIAL = dict(
    text='Was für den Entwurf neu entstanden ist, liegt sortiert in einem Ordner: die Karte als PDF, die Drucksachen, die Untersetzer, die Sticker, die Beigaben, die Postkarten, die Beiträge für Instagram und Ihr Logo als Datei.',
    streu=[(bild('fr-detail'), 'Konfitüren und Brot am Buffet', -4, '-0.05'), (bild('roesti-bar'), 'Die Bar des Röstihüs', 3, '0.04'), (bild('alpenrosen'), 'Alpenrosen über dem Saastal', -2, '-0.07'),
           (bild('z-balkon'), 'Die Balkontür', 4, '0.05'), (bild('stuebli'), 'Das Raclettestübli', -3, '-0.04')],
    druck_satz='Von der Karte am Tisch bis zum Willkommensbrief im Zimmer.',
    zeichen=[('Ihr Logo', '../../../_werkzeuge/oberflaeche/kleid/montemoro-marke.svg', 'Hotel Monte-Moro Logo.svg')],
    zeichen_satz='Ihr Logo als Zeichnung, die in jeder Grösse scharf bleibt.',
    auslage=[])
AUSBLICK = dict(text='Ein paar Dinge fehlen noch.', gross=('', '', ''), punkte=[], studio='')
SCHLUSS = dict(bild=bild('wolkenmeer'))
KAPITEL = {
    'vergleich': dict(text=VERGLEICH_TEXT),
    'ideen': dict(text='Hinter jeder Stelle der Seite steht ein Gedanke. Zwölf davon sind hier aufgenommen, so wie die Seite heute aussieht.'),
    'gefuege': dict(text='Links, was von Ihnen kommt, in der Mitte, was daraus geworden ist, rechts die Seiten und was im Hintergrund mitläuft.'),
    'seiten': dict(text='Eine Seite aussuchen, mit den Pfeilen weiterblättern. Rechts dieselbe Stelle am Handy, mit «Öffnen» sind Sie auf der echten Seite.'),
    'unterlagen': dict(text=UNTERLAGEN['text']),
    'gaeste': dict(text='Wer zu Ihnen kommen will, möchte vorher wissen, wie das Zimmer aussieht, was inbegriffen ist und wie er hinfindet. Auf der neuen Seite steht das an einem Ort, und jede Frage hat einen Weg zu Ihnen.'),
    'papier': dict(text='Für das Monte-Moro ist einiges entstanden: Drucksachen von der Karte im Röstihüs bis zum Willkommensbrief im Zimmer, Untersetzer fürs Röstihüs, Mails an Ihre Gäste, Postkarten und Sticker.'),
    'material': dict(text='Wer eine Datei braucht, findet sie hier: die Karte als PDF, jede Drucksache, jeden Untersetzer und Ihr Logo in voller Schärfe.'),
    'geprueft': dict(text='Bevor etwas davon zu Ihnen kommt, wird es geöffnet, gelesen und gedrückt: am Handy wie am Rechner, jeder Preis gegen Ihre Angaben, jedes Werkzeug in jedem Schritt. Das Blatt fasst es zusammen, der Bericht erzählt es ganz.'),
    'schluss': dict(text='Sagen Sie mir offen, was Ihnen am Entwurf gefällt und was nicht. Ändern lässt sich alles.'),
}
MEINS = ['Der Brief und alle Sätze der Werkbank', 'Titel und Sätze zu den Ideen, zum Gefüge, zu den Drucksachen und Untersetzern', 'Texte zu den Beiträgen des Feeds']

# ---------- Geprüft (nur Belegtes; Werkzeuge aus ihren Lieferungen) ----------
import datetime as _dt
GEPRUEFT = [
    ('Die Website', 'seite', ['Alle Seiten am Handy und am Rechner: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
                              'In vier Breiten angesehen, vom Handy bis zum grossen Bildschirm.',
                              'Jede Angabe kommt aus einer Stelle mit Quelle: Preise, Zuschläge, Inklusive, Zeiten des Kidsclubs und die Anreise.']),
    ('Die Karte', 'karte', ['Jede Zeile der Karte aus Ihrer Speisekarte gelesen, nicht abgetippt.',
                            'Was nur Sie klären können, steht gesondert in der Liste der offenen Punkte.']),
    ('Die Werkzeuge', 'schloss', ['Jedes der sieben Werkzeuge in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, nur mit erfundenen Gästen.',
                                  'Kein Werkzeug verschickt etwas von selbst, keines öffnet ein Mailprogramm.']),
]
GEPRUEFT_PUNKTE = [
    ('Die Website', 'Jede Seite am Handy und am Rechner, in vier Breiten. Nichts rutscht zur Seite, kein Bild fehlt.'),
    ('Die Preise', 'Gelesen aus Ihrer Preisliste und Ihrer Karte, nicht abgeschrieben. Jeder Preis steht so, wie Sie ihn heute nennen.'),
    ('Die Werkzeuge', 'Jedes der sieben in seinem eigenen Durchgang bedient, mit erfundenen Gästen. Keines schickt von sich aus eine Nachricht.'),
    ('Ihre Daten', 'Gäste bekommen keine Cookies. Was sie anfragen, landet bei Ihnen, und im Entwurf nie beim echten Hotel.'),
]
GEPRUEFT_TRIO = [(bild('empfang'), 1.6, (.5, .5), 'Am Empfang'), (bild('stube'), 1.6, (.5, .5), 'Im Röstihüs'), (bild('haus-winter'), 1.6, (.5, .5), 'Das Haus im Winter')]
GEPRUEFT_OFFEN = 'Ein paar Fragen können nur Sie beantworten: welche Strasse im Impressum steht, wer an welchem Foto die Rechte hat und wer welches Werkzeug bekommt.'
GEPRUEFT_EIN = 'Hier steht in einfachen Worten, was an Website, Karte und Werkzeugen angesehen und ausprobiert wurde, und was danach noch bei Ihnen liegt.'
GEPRUEFT_NAV = ['Website', 'Karte', 'Werkzeuge', 'Daten', 'Offen']
PRUEF_WERKZEUGE = []   # Zahl der geprüften Zustände je Werkzeug aus den Lieferungen (wird nachgetragen, sobald alle sieben fertig gemeldet sind)
try:
    PRUEF_WERKZEUGE = [tuple(x) for x in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pruef_werkzeuge.json'), encoding='utf-8'))]
except (FileNotFoundError, ValueError):
    pass
GEPRUEFT_MEHR = [
    ('Die Website', 'seite', 'Neun Seiten: sieben für Ihre Gäste von der Startseite bis zur Anreise, dazu Impressum und Datenschutz.', [
        'Jede Seite geöffnet, auf dem Handy und auf dem Rechner. Nichts verrutscht zur Seite, kein Bild fehlt, kein Skript bricht ab.',
        'In vier Breiten angesehen, von 390 bis 1440 Pixel. Beim Laden springt nichts.',
        'Preise, Zuschläge, Inklusive, Kidsclub und Anreise stehen an genau einer Stelle, mit ihrer Quelle, und jede Seite liest von dort.']),
    ('Die Karte', 'karte', 'Die Karte des Röstihüs: Röstis, Cordon bleus, Hotelweine, Spritz und Dessert.', [
        'Gelesen aus Ihrer Speisekarte vom November 2024, nicht abgeschrieben.',
        'Neu gesetzt im Kleid der neuen Seite, die Schriften fest eingebettet.']),
    ('Die sieben Werkzeuge', 'schloss', 'Die Werkzeuge, mit denen Sie Zimmer, Preise, Karte, Marke und Anfragen selbst führen.', [
        'Jedes Werkzeug in seinem eigenen Durchgang gebaut und Schritt für Schritt bedient, mit erfundenen Gästen und Zahlen.',
        'Kein Werkzeug schickt etwas von sich aus und keines öffnet ein Mailprogramm. Antworten an Gäste bleiben als Entwurf im Werkzeug, bis jemand sie selbst verschickt.',
        'Jedes Werkzeug ging durch die Prüfung in vier Breiten (1440, 1280, 1000 und 390 Pixel): Start, jeder Reiter, jedes Fenster'
        + (': ' + ', '.join(f'{_werkzeugname(t)} {n}' for t, n in PRUEF_WERKZEUGE) if PRUEF_WERKZEUGE else '') + '. Gefunden wurde dabei nichts, das offen geblieben ist.']),
    ('Ihre Daten und die Ihrer Gäste', 'schild', 'Was gespeichert wird und was nicht.', [
        'Gäste bekommen keine Cookies. Im Entwurf werden keine Besuche gezählt; ' + _nf.klein(_werkzeugname('besuche')) + ' zeigt erfundene Zahlen.',
        'Anfragen für Zimmer und Tisch laufen im Entwurf nur zur Probe; nichts davon erreicht das echte Hotel.',
        'Suchmaschinen sehen den Entwurf nicht, bis Sie ihn freigeben.']),
    ('Was offen bleibt', 'auge', 'Das können nur Sie entscheiden.', [
        'Welche Strasse im Impressum und bei Google stehen soll.',
        'Wer an welchem Foto die Rechte hat.',
        'Im Entwurf öffnen sich die Werkzeuge ohne Anmeldung. Zum Start bekommt jede Person ihren eigenen Zugang.'])]
PRUEFDATUM = _dt.date(2026, 11, 8)
STEMPEL_TEXT = f'GEPRÜFT · MONTE-MORO · {PRUEFDATUM:%d.%m.%Y} ·'
GEPRUEFT_BILD = bild('empfang')

# ================================================================ Bausteine (Kit unverändert, eigene Module in _werkbank/)
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
EIGENE, EIGENE_BILDER, FLAECHE = [], [], {}
CSS = ''
_WB = os.path.join(ROOT, 'werkbank')

import brief_blatt as _bb  # noqa: E402
brief_abschnitt = _bb.abschnitt(globals())
EIGENE_BILDER += _bb.bilder(BRIEF)
CSS += _bb.CSS
import kopf_mitte as _km  # noqa: E402
import auftakt_kacheln as _ak  # noqa: E402
CSS += _km.CSS + _ak.CSS
FLAECHE.update(brief='fl--papier tapete-hell', vergleich='fl--nacht tapete-leicht', ideen='fl--blau tapete-leicht', gefuege='fl--nacht tapete-leicht',
               seiten='fl--papier tapete-hell', gaeste='fl--navy tapete', unterlagen='fl--tief tapete-leicht', papier='fl--navy tapete', material='fl--papier tapete-hell',
               feed='fl--nacht tapete-leicht', geprueft='fl--navy tapete')
CSS += '''
/* ---------- Leichte Tapete: die Grate des Markenbuchs auf jeder dunklen Fläche ---------- */
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(10,42,74,.25)}
.fl--blau.tapete-leicht{--tl:rgba(17,85,149,.2)}
.fl--tief.tapete-leicht{--tl:rgba(7,27,46,.25)}
.tapete-hell{background-image:url(/werkbank/eigen/tapete-hell.svg);background-size:240px auto;background-position:50% 0}
/* ---------- Titel wie auf der Website: Fjalla One, eine Stärke, normale Schreibung, Betonung nur über die Farbe, nie fett, nie kursiv ---------- */
.zt,.t1,.t2,.t3,.wfen__t,.ins-t h3,.rgw .wfa__texte h3,.sbf-text h3,.hs2-ww+small{font-weight:400!important}
.zt{text-transform:none;letter-spacing:0}
.zt em,em{font-style:normal}
.kap--k .kap__geist{display:none}.kap--z span,.kap--k>span{font-family:var(--mono)!important;font-weight:400!important;font-size:12px!important;letter-spacing:.2em;text-transform:uppercase}
.wfen__t{text-transform:none;letter-spacing:0}
h2,h3,.wege__t,.gb-blatt header h3,.rgw .wfa__texte h3,.fbz__n{font-weight:400!important}
b,strong{font-weight:500}
.gb-blatt header h3{font-family:var(--serif);text-transform:uppercase;letter-spacing:.08em}
.wf .wege__t{font-family:var(--serif);text-transform:none;letter-spacing:0;font-size:clamp(2rem,3.6vw,3.4rem)!important;line-height:1.1}
/* Schrift mittig in den Ziffern des Registers und der Befunde (DM Mono) */
.rgc-p{padding:8px 10px 6px!important;font-family:var(--mono)!important;font-size:.82rem!important;letter-spacing:0!important}
.rgc-p[data-i="3"]{padding-left:9.4px!important;padding-right:10.6px!important}   /* «IV»: das V steht in DM Mono 0,6 px weiter rechts (Tor 08.11.) */
.ins-m{padding:8px 16px!important}
@supports (interpolate-size:allow-keywords){.ins-m>.tm{position:relative;top:.7px}}   /* DM Mono in Chromium 0,7 px zu hoch (Tor 08.11.) */
.ins-m .tm-l,.sbf-z .tm-l{letter-spacing:0}
.sbf-z{padding:7px 9px!important;letter-spacing:0!important}
@supports (interpolate-size:allow-keywords){.sbf-b .sbf-z{padding-top:7.7px!important;padding-bottom:6.3px!important}}   /* DM Mono in Chromium 0,7 px zu hoch (Tor 08.11.) */
@media(max-width:600px){.auftakt__fuss .runter i{display:none}.auftakt__fuss .runter{gap:0}}   /* am Handy alle Zeilen auf einer Kante */
/* Das Zeichen (Bergkamm) steht in der Lärche, auf Hell in Lärche tief; es ist breit, darum nur über die Höhe bemessen */
svg:has(> use[href="#hz"]){color:var(--gold);fill:currentColor}
.fl--papier svg:has(> use[href="#hz"]),.fl--creme svg:has(> use[href="#hz"]){color:var(--rot)}
.kap__z{width:auto!important;height:clamp(18px,1.8vw,26px)!important;aspect-ratio:3483/696}
/* Fjalla One nur für Titel (Kleid der Website): Lauftext der Bausteine in Instrument Sans, Zahlen und kleine Zeilen in DM Mono */
.ins-hinweis,.ins-t__s,.rh-livre p,.sag-opt,.vt-erg small,.vt-feld__l span,.vt-gegen__satz,.vt-gr span,.vt-r__lead,.vt-r__t>p,.vt-r__u,.wfen__k,.wzs__z li,.punkte i,.werte span,.bfk-bed span,.vt-gegen__z{font-family:var(--sans)!important}
.hs2-her figcaption,.gb-f figcaption,.fb-p figcaption,.mn-haus,.sag-reg a,.vt-erg span,.vt-feld__w em,.vt-feld__w input,.abzug span{font-family:var(--mono)!important;font-style:normal!important}
.vt-r__lead{font-size:clamp(1.12rem,1.3vw,1.36rem)!important}
.fl--papier .zt em,.fl--creme .zt em,.fl--papier h2 em,.fl--creme h2 em,.fl--papier .t1 em,.fl--papier .t2 em,.fl--creme .t2 em{color:var(--rot)!important}
/* Knöpfe wie .kn der Website: Hauptweg Lärche mit weissem Knauf, Nebenweg Nacht (montemoro.css .kn--laerche, .kn--nacht) */
.kn,.hell .kn,.fl .kn,.pk .kn,.wf .kn,.fl--papier .kn,.fl--creme .kn,.pk--hell .kn{--o:#d3845a!important;--m:#c67144!important;--u:#ae5e34!important;--t:#ffffff!important;--licht:rgba(255,255,255,.3)!important;--kante:rgba(0,0,0,.22)!important;--tf:rgba(90,40,15,.45)!important;--ko:#ffffff!important;--ku:#efe9e1!important;--kt:#0a2a4a!important;--klicht:rgba(255,255,255,.95)!important}
.kn--linie,.hell .kn--linie,.fl .kn--linie,.pk .kn--linie,.wf .kn--linie,.kn--nacht{--o:#15466f!important;--m:#0d3f6f!important;--u:#0a2a4a!important;--t:#ffffff!important;--licht:rgba(255,255,255,.18)!important;--kante:rgba(0,0,0,.35)!important;--tf:rgba(3,10,16,.5)!important;--ko:#ffffff!important;--ku:#efe9e1!important;--kt:#0a2a4a!important;--klicht:rgba(255,255,255,.95)!important}
/* Auf der Lärche-Karte der Drucksachen der Knopf in Nacht (nie zwei grosse Flächen in voller Akzentfarbe, Kriterium 25) */
.pk--hell .kn{--o:#15466f!important;--m:#0d3f6f!important;--u:#0a2a4a!important;--tf:rgba(3,10,16,.5)!important}
/* Etiketten des Hauses: DM Mono, gesperrt, Versalien (wie die kleinen Zeilen der Website) */
.rz{font-family:var(--mono);font-weight:400;letter-spacing:.18em;text-transform:uppercase}
'''

import marke_werkbank as _mw  # noqa: E402
EIGENE.append(_mw.abschnitt(globals())); EIGENE_BILDER += _mw.BILDER; CSS += _mw.CSS
FLAECHE['handschrift'] = 'fl--navy tapete'
import mails_reihe as _mr  # noqa: E402
CSS += _mr.CSS
EIGENE_BILDER += _mr.BILDER   # die Mails als dritte Karte im Papier (wb_kapitel.papier_mails)
import feed_buehne as _fb  # noqa: E402
_FEED_DA = os.path.exists(os.path.join(ROOT, 'feed', 'feed.json'))
if _fb.BEREIT and _FEED_DA:
    EIGENE.append(_fb.abschnitt(globals())); EIGENE_BILDER += _fb.BILDER; CSS += _fb.CSS
import fenster_ausblick as _fa  # noqa: E402
CSS += _fa.CSS
import geprueft_blatt as _gb  # noqa: E402
geprueft_abschnitt = _gb.abschnitt(globals())
_AN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ansichten')
for _i, _q in enumerate([os.path.join(_AN, 'Rechner', 'Startseite.jpg'), (sorted(_glob.glob(os.path.join(ROOT, 'unterlagen', 'img', 'n-*.webp'))) or [''])[0],
                         os.path.join(_AN, 'Werkzeuge', 'bureau.jpg'), os.path.join(_AN, 'Gaeste', 'anfrage.jpg')]):
    if _q and os.path.exists(_q):
        EIGENE_BILDER.append((f'gp-{_i}', _q, 320, dict(q=80, schnitt=4 / 3, lage=(.5, 0))))
CSS += _gb.CSS

import fuss_faecher as _ff  # noqa: E402
if _ff.BEREIT:
    wege_abschnitt = _ff.abschnitt
    CSS += _ff.CSS
CSS += '''
/* Dateien: Fotos ohne Polaroid-Rand und ohne Bildzeile, ungleich gross, ohne Drehung */
#material .streu .abzug{padding:0!important;background:none!important;border-radius:clamp(10px,1vw,14px);overflow:hidden;--r:0deg!important;--r0:0deg!important;box-shadow:0 30px 40px -26px rgba(7,27,46,.6),0 10px 16px -10px rgba(7,27,46,.35)!important}
#material .streu .abzug span{display:none!important}
#material .streu .abzug img{display:block;width:100%;height:100%;object-fit:cover;border-radius:0!important}
@media(min-width:760px){#material .streu{align-items:center}#material .streu .abzug:nth-child(3){transform:scale(1.18);z-index:2}#material .streu .abzug:nth-child(2),#material .streu .abzug:nth-child(4){transform:scale(1.04);z-index:1}}
/* Flüssigkeit (Regel 55): Abschnitte ausserhalb des Blicks werden nicht gezeichnet. Ausgenommen der Brief (überstehendes Blatt). */
@supports (content-visibility:auto){main>section.fl:not(#brief):not(#gefuege):not(.bfs):not(.ki){content-visibility:auto;contain-intrinsic-size:auto 1400px}}   /* Befund und KI-Seite sind kurz: immer gezeichnet (Oberflächen-Prüfung Punkt 3) */
html.cv-alle main>section.fl:not(#brief){content-visibility:visible}
@media(min-width:760px){.vh-wahl>:first-child,#seiten .wahl>:first-child{margin-left:auto}.vh-wahl>:last-child,#seiten .wahl>:last-child{margin-right:auto}}
@media(max-width:480px){.kn{max-width:100%;height:auto;min-height:54px;padding-top:9px;padding-bottom:9px;white-space:normal;line-height:1.35;text-align:left}.kn i{flex:none}.kn-reihe{max-width:100%}}
.schluss .zt,.schluss .lauf p,.schluss .kap span{text-shadow:0 1px 2px rgba(7,27,46,.9),0 2px 16px rgba(7,27,46,.8),0 0 42px rgba(7,27,46,.55)}
'''


CV_JS = ("<script id=\"cv-hoehen\">(function(){var d=document.documentElement;function alle(){d.classList.add('cv-alle');requestAnimationFrame(function(){requestAnimationFrame(function(){d.classList.remove('cv-alle')})})}"
         "/* einmal alles zeichnen, damit jede Fläche ihre echte Höhe kennt: Sprungmarken landen genau (content-visibility) */"
         "if(document.readyState==='complete')setTimeout(alle,300);else addEventListener('load',function(){setTimeout(alle,300)});"
         "addEventListener('resize',function(){clearTimeout(alle.t);alle.t=setTimeout(alle,400)})})();</script>")
BRETT_HILFE = ("<script id=\"brett-hilfe\">(function(){var b=document.getElementById('brett'),k=document.getElementById('brett-noch');if(!b||!k||!('IntersectionObserver' in window))return;"
               "new IntersectionObserver(function(E,o){if(!E[0].isIntersecting)return;o.disconnect();setTimeout(function(){if(/\\bvor\\b/.test(b.className))k.click()},700)},{rootMargin:'0px 0px -35% 0px'}).observe(b)})();</script>")


def nach_bau():
    """Nach jedem Bau des Kits: Eigenes nach werkbank/eigen, Nacharbeit der Bausteine, Kapitel, Ruhe, Farben, Schweizer Schreibung."""
    import re as _re, shutil as _sh
    from PIL import Image as _I
    q, z = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen'), os.path.join(_WB, 'eigen')
    os.makedirs(z, exist_ok=True)
    sig = _I.open(os.path.join(q, 'unterschrift-robert.webp')).convert('RGBA')
    r, g, b = (int(FARBEN['tinte'][i:i + 2], 16) for i in (1, 3, 5))
    _I.merge('RGBA', (*_I.new('RGB', sig.size, (r, g, b)).split(), sig.getchannel('A'))).save(os.path.join(z, 'unterschrift.webp'), 'WEBP', quality=90)
    _fa.fenster_bilder()
    for f in os.listdir(q):
        if f.startswith('fen-'):
            _sh.copy2(os.path.join(q, f), os.path.join(z, f))
    if _fb.BEREIT and _FEED_DA:
        _fb.bilder()
    if _ff.BEREIT:
        _ff.bilder()
    seite = os.path.join(_WB, 'index.html')
    _ak.anwenden(seite)
    _mw.anwenden(seite)
    _fa.anwenden(seite)
    _km.anwenden(seite)
    import fluss_werkbank as _fw
    _fw.anwenden(seite)
    import wb_kapitel as _kp
    _kp.anwenden(seite)
    # Nichts läuft mit dem Scrollen mit (Regel 55)
    t = open(seite, encoding='utf-8').read()
    t = _re.sub(r'\sdata-(?:drift|zug)="[^"]*"', '', t)
    ruhe = ('<style id="sb-ruhe">.bf .bf-blatt[data-a="heben"],.bf .bf-blatt[data-a="heben"].da{animation:none!important}.kap__geist{animation:none!important}'
            '.kn:hover,.kn:active,.rund:hover,.rund:active,.wahl button:active,.vh-wahl button:active,.bn button:hover,.bn button:active,.glanz:active,.ins-r:hover,.ins-r:active,.wf__pf:hover,.wf__pf:active,.rgc-p:hover,.rgc-p:active,.sbf-z:hover{transform:none!important;translate:none!important;scale:none!important}'
            '.kn{overflow:hidden}.ins-reiter,.fb__reiter{padding-top:10px!important;padding-bottom:26px!important;margin-top:-10px!important;margin-bottom:-26px!important}'
            '.wahl,.vh-wahl{padding-top:8px!important;padding-bottom:26px!important;margin-top:-8px!important;margin-bottom:-12px!important}'
            '.wfen .wfen__t{font-size:clamp(24px,3.6vw,54px)!important;line-height:1.14!important}.wfen .wfen__k{font-size:clamp(15px,1.36vw,19px)!important}'
            '#papier img.frei{filter:none!important;box-shadow:none!important}</style>')
    if 'id="sb-ruhe"' not in t:
        t = t.replace('</head>', ruhe + '</head>', 1)
    if 'id="ins-mitte-js"' not in t:   # Reiter der Werkzeuge: Text in .tm, letzter Buchstabe in .tm-l ohne Sperrung (wie knopf_mitte.js)
        t = t.replace('</body>', "<script id=\"ins-mitte-js\">(function(){function m(){document.querySelectorAll('.ins-m').forEach(function(k){var t=k.firstChild;"
                      "if(!t||t.nodeType!==3||!t.textContent.trim())return;var x=t.textContent.replace(/\\s+$/,'');var s=document.createElement('span');s.className='tm';"
                      "s.textContent=x.slice(0,-1);var l=document.createElement('span');l.className='tm-l';l.textContent=x.slice(-1);s.appendChild(l);k.replaceChild(s,t)})}"
                      "m();addEventListener('load',m)})();</script></body>", 1)
    if 'id="brett-hilfe"' not in t:
        t = t.replace('</body>', BRETT_HILFE + '</body>', 1)
    if 'id="cv-hoehen"' not in t:
        t = t.replace('</body>', CV_JS + '</body>', 1)
    import sb_skripte as _sk
    for _id, _js in (('rh-vorladen', _sk.VORLADEN_JS), ('rh-frueh', _sk.FRUEH_JS), ('rh-zurueck', _sk.WB_JS), ('rh-karussell', _sk.KARUSSELL_JS)):
        if f'id="{_id}"' not in t:
            t = t.replace('</body>', _js + '\n</body>', 1)
    open(seite, 'w', encoding='utf-8').write(t)
    import kartenzug as _kz   # Bildkarussells heissen «kartenzug», nicht «band» (Nachtrag 09.11.2026, Prüfpunkt 6)
    _kz.anwenden(_WB)
    import feed_leicht as _fl
    if _fb.BEREIT and _FEED_DA:
        _fl.mach()
    import sb_farbe
    sb_farbe.anwenden()
    # Das Zeichen (Bergkamm) als Datei: in Lärche für die Karte «Ein Vorschlag.» (als <img> wäre currentColor schwarz), schwarz als Maske für Schmuck im CSS
    vb, innen = ZEICHEN
    open(os.path.join(_WB, 'eigen', 'zeichen-kerze.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{FARBEN["gold"]}">{innen}</svg>')
    open(os.path.join(_WB, 'eigen', 'zeichen-c.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="#000">{innen}</svg>')
    _ft = os.path.join(ROOT, 'feed', '_tafeln.html')
    if os.path.exists(_ft):
        _s = open(_ft, encoding='utf-8').read()
        if 'noindex' not in _s:   # nach <head> bzw. nach dem Doctype, nie davor (sonst Quirks-Modus)
            if '<head>' in _s:
                _s = _s.replace('<head>', '<head><meta name="robots" content="noindex, nofollow">', 1)
            elif _s.lower().startswith('<!doctype html>'):
                _s = _s[:15] + '<meta name="robots" content="noindex, nofollow">' + _s[15:]
            open(_ft, 'w', encoding='utf-8').write(_s)
    import sb_ki   # Seite «KI und Ihre Daten», Karte «Ein Vorschlag.» allein und als PDF
    sb_ki.bau()
    import du_gang   # zuletzt: Schweizer Schreibung (ss), Sie-Form, Reste der Vorlage
    du_gang.anwenden()
    import nur_bewegung   # bewegt nur transform/opacity, Glanzkante dreht statt neu zu malen, Karte kommt herein
    nur_bewegung.anwenden(ROOT)
    import zeile_ganz   # kein Einzelwort allein in der letzten Titelzeile
    zeile_ganz.anwenden(ROOT)
    import text_mitte   # Schrift optisch mittig in den Knöpfen aller Werkbank-Seiten
    text_mitte.anwenden(ROOT)
    import bild_mass   # Bilder in der gezeigten Grösse
    bild_mass.anwenden(ROOT)
    try:   # Knopfschrift in Chromium und WebKit gleich mittig (Baustein von Werkbank Papier, papier_nach.knopf_mitte, nach text_mitte)
        import papier_nach as _pn
        for _s in ('werkbank/index.html', 'werkbank/ki.html', 'werkbank/karte.html', 'werkbank/impressum.html', 'werkbank/geprueft/index.html', 'befund/index.html'):
            if os.path.exists(os.path.join(ROOT, _s)):
                _pn.knopf_mitte(os.path.join(ROOT, _s))
    except Exception as _f:
        print('knopf_mitte nicht gesetzt:', _f)
    import kleid_haus   # zuletzt: Kleid des Monte-Moro über alle Seiten des Kerns (Leiste, Zeichen, Reste der Vorlage)
    kleid_haus.anwenden(ROOT)
    import importlib.util as _iu   # Zurück im Browser landet auf der alten Höhe, auf jeder Seite der Werkbank (Robert 1.11.2026); die eigene Fassung, nicht die des Kits
    _sp = _iu.spec_from_file_location('rs_haus', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ruecksprung.py'))
    _rs = _iu.module_from_spec(_sp); _sp.loader.exec_module(_rs)
    _rs.anwenden(ROOT)


TITEL_NEU = {   # eigene Überschriften des Monte-Moro (Werkbank-Regel 14)
    ('Schön, dass Sie', 'hereinschauen.'): ('Liebe Frau Zurbriggen,', 'lieber Herr Zurbriggen'),
    ('Ihre Website,', 'Seite für Seite.'): ('Heute und', 'morgen.'),
    ('Die Ideen', 'hinter der Seite.'): ('Zwölf Stellen,', 'zwölf Gedanken.'),
    ('Wie alles', 'zusammenhängt.'): ('Was hinter', 'dem Haus steht.'),
    ('Alle Seiten zum', 'Durchblättern.'): ('Vom Zimmer', 'bis zur Anreise.'),
    ('Vorschläge für', 'Ihre Gäste.'): ('Bevor der Gast', 'ankommt.'),
    ('Ihre Unterlagen,', 'im selben Stil.'): ('Ihre Karten,', 'neu gesetzt.'),   # alle Karten des Hauses (Robert 09.11.2026)
    ('Ein paar Ideen', 'für Papier.'): ('Für Tisch', 'und Zimmer.'),
    ('Ein Feed', 'für Instagram.'): ('Ein Feed', 'am Grat.'),
    ('Alles liegt für', 'Sie bereit.'): ('Alle Dateien', 'an einem Ort.'),
    ('Alles geprüft,', 'bevor Sie es sehen.'): ('Ausprobiert,', 'Stück für Stück.'),
}
TEXT_NEU = [   # Sätze des Kits, die fürs Haus nicht stimmen (wb_kapitel.eigene_titel ersetzt sie wörtlich)
    ('Links Ihre Seite, wie sie heute ist, rechts der Entwurf. Schieben Sie den Griff hin und her, daneben steht, was neu ist.', VERGLEICH_TEXT),
]
KAP_NAME_NEU = {'Guten Tag': 'Ein Brief', 'Register': 'Inhalt', 'Zum Schluss': 'Bis bald'}


# Farben und Schnitte schon in H.CSS setzen: baut ein anderer Schritt mit dem Kit (K.gestaltung), stehen so trotzdem die Töne des Hauses
import sb_farbe as _sf  # noqa: E402
CSS = _sf.ohne_fett(_sf.faerbe(CSS))

# Unterlagen «Heute und als Idee»: das Foto der Karte hat das Format des Blatts daneben, beide Seiten gleich hoch.
CSS_SEITEN = '''
.upaar{align-items:center}
.ublatt--alt .ublatt__b{aspect-ratio:1/1.414!important}
.ublatt--alt .ublatt__b img{width:100%;height:100%;object-fit:cover}
'''

# Texte der Papier-Seiten (Werkbank Papier, _werkbank/papier_haus.json): dieselben Werte auch auf der Startseite
try:
    import mit_papier as _mp  # noqa: E402
    _mp.anwenden(sys.modules[__name__])
except Exception as _f:   # ohne Papier-Werte baut der Kern mit den eigenen
    print('mit_papier nicht angewendet:', _f)
