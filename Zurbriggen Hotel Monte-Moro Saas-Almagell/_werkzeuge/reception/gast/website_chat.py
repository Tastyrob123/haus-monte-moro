"""Die Rezeption im Chat der Website, in Python (08.11.2026): dieselbe Suche wie website/assets/js/rezeption.js über dieselben Fragen und Antworten
(website/assets/js/wissen.json), damit «Chat ausprobieren» und «Das wurde gefragt» genau so antworten wie der Chat auf der Website.
Worte der Frage gegen Frage und Antwort jedes Eintrags, seltene Worte zählen mehr; ein Themawort der Gastfrage (Spa, Hund, Röstis …) muss im Eintrag
vorkommen, sonst lieber an die Rezeption verweisen als falsch antworten. Einträge zu Angeboten, die abgelaufen sind (Gratis-Anreise bis 31.10.2026,
website/inhalt/daten.py ANREISE_GRATIS), nimmt die Rezeption nicht mehr: sonst böte sie etwas an, das es nicht mehr gibt.
antworte(frage) → {'text', 'belegt', 'fids', 'aktion'}; ohne Treffer belegt=False und der Weg zur Rezeption, ohne Zahl."""
import datetime, json, math, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HIER))), 'website')
STOP = set('der die das und oder ist sind ein eine einen einem einer im in am an auf aus bei mit für von zu zum zur den dem des wie was wer wo ich sie wir es kann können gibt gibt’s gibt es hat haben man mein meine ihr ihre ihren noch auch nicht nur sehr bitte monte moro hotel'.split())
NAH = {'pools': 'pool', 'hunde': 'hund', 'tier': 'hund', 'tiere': 'hund', 'parken': 'parkplatz', 'auto': 'parkplatz', 'mietwagen': 'parkplatz', 'kind': 'kinder', 'baby': 'kinder',
       'wohnung': 'ferienwohnung', 'bahn': 'zug', 'postauto': 'postauto zug', 'wellness': 'spa', 'sauna': 'spa', 'pool': 'spa', 'fliege': 'flughafen', 'flug': 'flughafen',
       'airport': 'flughafen', 'taxi': 'transfer', 'essen': 'restaurant', 'abendessen': 'restaurant', 'schwimmbad': 'pool', 'schwimmen': 'pool', 'hochzeit': 'hochzeiten',
       'anreise': 'check in', 'abreise': 'check out', 'einchecken': 'check in', 'auschecken': 'check out', 'oeffnet': 'geoeffnet oeffnungszeiten', 'offen': 'geoeffnet oeffnungszeiten',
       'massage': 'massage spa', 'auf': 'geoeffnet', 'darf': 'erlaubt', 'duerfen': 'erlaubt', 'heiraten': 'hochzeiten'}
THEMA = ['spa', 'roesti', 'raclet', 'fruehs', 'kinder', 'kidscl', 'hund', 'parkpl', 'wein', 'ferien', 'apollo', 'arizon', 'alpenh', 'kurtax', 'euro', 'zug', 'auto', 'bergba', 'postau', 'cordon']
_W = {}


def _norm(t):
    t = str(t).lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    return re.sub(r'[^a-z0-9 ]+', ' ', t)


def _worte(t):
    aus = []
    for w in _norm(t).split():
        if len(w) > 2 and w not in STOP:
            aus.append(w)
            aus += NAH.get(w, '').split()
    return [w[:6] if len(w) > 6 else w for w in aus]


def _abgelaufen():
    """Sätze abgelaufener Angebote (daten.py ANREISE_GRATIS), nach ihrem Enddatum."""
    try:
        s = open(os.path.join(WEB, 'inhalt', 'daten.py'), encoding='utf-8').read()
        m = re.search(r"ANREISE_GRATIS = dict\(titel='([^']+)', bis='(\d{4}-\d{2}-\d{2})'", s)
        if m and datetime.date.today().isoformat() > m.group(2):
            return [m.group(1)]
    except OSError:
        pass
    return []


def wissen():
    p = os.path.join(WEB, 'assets', 'js', 'wissen.json')
    t = os.path.getmtime(p)
    if _W.get('t') == t:
        return _W['d']
    d = json.load(open(p, encoding='utf-8'))
    raus = _abgelaufen()
    d['eintraege'] = [e for e in d['eintraege'] if not any(r in e['a'] for r in raus)]
    df = {}
    for i, e in enumerate(d['eintraege']):
        e['_q'], e['_a'], e['fid'] = _worte(e['q']), _worte(e['a']), 'w%02d' % i
        for w in set(e['_q'] + e['_a']):
            df[w] = df.get(w, 0) + 1
    n = len(d['eintraege'])
    idf = {w: math.log(1 + n / c) for w, c in df.items()}
    for w in ('wann', 'check'):   # Fragewort und «Check» allein tragen keine Antwort
        if w in idf:
            idf[w] *= 0.35
    d['_idf'] = idf
    _W.update(t=t, d=d)
    return d


def suche(frage):
    d = wissen(); idf = d['_idf']; f = _worte(frage); treffer = []
    if not f:
        return []
    for e in d['eintraege']:
        if any(w in THEMA and w not in e['_q'] and w not in e['_a'] for w in f):
            continue
        s = infrage = 0.0
        for w in f:
            g = idf.get(w, 1)
            if w in e['_q']:
                s += 2.2 * g; infrage += g
            elif w in e['_a']:
                s += g
        if infrage >= 1.5:
            for w in e['_q']:
                if w not in f and idf.get(w, 1) > 3:
                    s -= 0.5 * idf.get(w, 1)
            treffer.append((s / math.sqrt(4 + len(e['_q'])), e))
    treffer.sort(key=lambda x: -x[0])
    return treffer


# Was das Haus nicht veröffentlicht (daten.py OFFEN, fakten.json): vor der Suche abgefangen, damit nie eine Antwort mit fremden Zahlen kommt
# (die Suche der Website antwortete auf «Wann hat das Röstihüs offen?» mit der Röstikarte). Ehrlich, ohne Zahl, als Lücke fürs Team.
OFFEN = [(r'(oeffnungszeit|geoeffnet|offen|ruhetag|wann.*(auf|zu)\b)', r'roesti|restaurant|stuebli|essen|kueche', 'Öffnungszeiten des Röstihüs',
          'Die Öffnungszeiten des Röstihüs erfahren Sie gern direkt bei uns an der Rezeption'),
         (r'check ?in|check ?out|einchecken|auschecken|ankunftszeit|bis wann.*zimmer|ab wann.*zimmer', '', 'Check-in und Check-out',
          'Wann Ihr Zimmer bereit ist und bis wann Sie es am Abreisetag nutzen, sagen Ihnen Esther und Fabian gern persönlich'),
         (r'storn|annull|rueckt|geschaeftsbeding|\bagb\b', '', 'Storno und Geschäftsbedingungen',
          'Zu Storno und Geschäftsbedingungen geben Ihnen Esther und Fabian gern persönlich Auskunft'),
         (r'(preis|kost|teuer|chf|franken)', r'ferienwohn|apollo|arizona|wohnung', 'Preis der Ferienwohnungen',
          'Die Preise der Ferienwohnungen im Haus Apollo und im Haus Arizona nennen Ihnen Esther und Fabian gern persönlich'),
         (r'strasse|hausnummer|navi|adresse', '', 'Strasse des Hauses',
          'Sie finden uns im Hotel Monte-Moro, CH-3905 Saas-Almagell; den genauen Weg beschreibt Ihnen die Rezeption gern'),
         (r'allerg|unvertraeg|gluten|laktos|zoeliak|vegan|nuss|nuess', '', 'Allergien und Unverträglichkeiten',
          'Ob ein Gericht des Röstihüs für Sie passt, klärt die Küche gern persönlich mit Ihnen')]


def antworte(frage, sprache='de'):
    d = wissen(); n = _norm(frage)
    if re.search(r'gratis|geschenkt|kostenlos|umsonst', n) and re.search(r'anreis|abreis|zug|bahn|oev|oeffentlich', n):
        return {'text': 'Die An- und Abreise mit dem öffentlichen Verkehr war für Buchungen bis 31. Oktober 2026 geschenkt; dieses Angebot läuft nicht mehr. '
                        'Inklusive bleibt die Benutzung der Postautos im ganzen Saastal (Sommer/Winter).', 'belegt': True, 'fids': [], 'aktion': '', 'quelle': 'Preise'}
    for muster, auch, thema, satz in OFFEN:
        if re.search(muster, n) and (not auch or re.search(auch, n)):
            return {'text': f"{satz}: {d['telefon']} oder {d['mail']}.", 'belegt': False, 'fids': [], 'aktion': '', 'thema': thema}
    t = suche(frage)
    if t and t[0][0] > 1.1:
        e = t[0][1]
        return {'text': e['a'], 'belegt': True, 'fids': [e['fid']], 'aktion': '', 'quelle': e['k'], 'frage_haus': e['q']}
    return {'text': f"Dazu steht in unseren Antworten nichts Genaues. Esther und Fabian helfen Ihnen gern persönlich weiter: {d['telefon']} oder {d['mail']}.",
            'belegt': False, 'fids': [], 'aktion': ''}
