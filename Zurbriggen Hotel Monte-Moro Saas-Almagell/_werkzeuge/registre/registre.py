#!/usr/bin/env python3
"""Die Besucherliste (Le Registre) · Hotel Monte-Moro, Saas-Almagell (Tasty Studios, 08.11.2026, Werkzeug 6): das Haus sieht, wer seine Website besucht.
Je Besuch: Land und Ort, Tag und Uhrzeit, Gerät, Sprache des Browsers, woher der Gast kam, welche Seiten er in welcher Reihenfolge ansah, wie lange
jede Seite sichtbar war und ob er ein Zimmer anfragte (Fenster «Anfrage» der Website), auf «Zimmer buchen» ging (Buchung bei seekda), einen Tisch im
Röstihüs anfragte, das Haus anrief oder anschrieb, den Chat der Rezeption öffnete oder zur Familie Zurbriggen weiterging (Spa nebenan, Familienband).
Nie ein Name, nie eine Adresse der Verbindung, kein Cookie.

Stamm: die Besucherliste der Häuser (28.10.2026, von Robert abgenommen); Aufbau, Funktionen und Wege unverändert.
Angepasst an das Hotel Monte-Moro mit Restaurant Röstihüs (Familie Zurbriggen, Gastgeber Esther und Fabian Zurbriggen): Seiten der Website (Zimmer, Preise,
Saastal, Spa nebenan, Röstihüs, Anreise), Wege des Hauses (Anfrage-Fenster, «Zimmer buchen» bei seekda, Tisch im Röstihüs, Telefon, E-Mail, Chat der Rezeption,
Familie Zurbriggen), Herkunftsnamen und Beispielorte für ein Hotel im Saastal, Uhrzeit Europe/Zurich, Sprache = Sprache des Browsers (die Website gibt es auf Deutsch).
Eigener Zähl-Schlüssel und eigener Speicher, getrennt von jedem anderen Haus (Werkzeug-Master 3, Robert 17.10.2026).

Der Browser schickt je Seite eine Zeile an /api/registre (assets/messung.js der Website, Quelle vorschlag/messung.js):
    r1 <seitenaufruf> <datei> <sprache> <geraet> <sekunden> <ereignisse|-> <herkunft|->
Einmal beim Öffnen (0 Sekunden), bei jedem gezählten Klick und beim Verlassen (sichtbare Sekunden und die Klicks).

Damit die Seiten eines Besuchs zusammenfinden, bildet der Server je Tag ein Kürzel aus Tag + Adresse der Verbindung + Browser-Kennung
(HMAC mit geheimem Schlüssel). Die Adresse selbst wird nie gespeichert; weil der Tag im Kürzel steckt, erkennt der nächste Tag
denselben Gast nicht wieder. Land und Ort nennt der Anbieter aus der Verbindung. Nach AUFBEWAHREN Tagen wird gelöscht.

Speicher: je Tag (Kalendertag in Saas-Almagell, Europe/Zurich) eine Datei, lokal _daten/<tag>.json.
Vorführ-Betrieb (Master Lernprotokoll 14.10.2026, Robert: «Da sollen Probewerte angezeigt werden. Für den Kunden»): die Abfrage antwortet
jedem mit Beispielwerten, als Beispiel beschriftet. Echte Werte nur mit Schlüssel (siehe server.py).

  python3 registre.py                  Stand der letzten 30 Tage (echt, lokal)
  python3 registre.py beispiel         dasselbe mit Beispielwerten
  python3 registre.py ablage           schreibt beispiel/7.json, 30.json, 90.json (falls das Werkzeug ohne Server-Teil läuft)
  python3 registre.py aufraeumen       löscht Tagesdateien älter als AUFBEWAHREN Tage
  python3 registre.py seiten           seiten.json und seiten-bilder.json neu aus der Website (nach neuen Seiten)
  python3 registre.py leeren           Zählung lokal leeren (alter Ordner bleibt als _daten.vor-leeren)"""
import collections, datetime, hashlib, hmac, json, os, random, re, sys, threading, time

HIER = os.path.dirname(os.path.abspath(__file__))
ORDNER = os.environ.get('REGISTRE_ORDNER') or os.path.join(HIER, '_daten')   # Prüfläufe zählen in einen eigenen Ordner
GEHEIM = (os.environ.get('REGISTRE_GEHEIM') or 'montemoro-saas-almagell-nur-lokal').encode('utf-8')
# Klicks, die zählen (messung.js): Zimmer-Anfrage begonnen und abgeschickt, «Zimmer buchen», Tisch im Röstihüs begonnen und abgeschickt,
# Telefon, E-Mail-Adresse, Chat der Rezeption, weiter zur Familie Zurbriggen
EREIGNISSE = ('fenster', 'buchung', 'booking', 'tisch', 'anfrage', 'anruf', 'mail', 'chat', 'route')
# Bedeutung beim Hotel Monte-Moro (Schlüssel wie in allen Häusern, damit La Maison, Prüfläufe und Ablage gleich lesen; Master G14):
#   fenster = Zimmer-Anfrage begonnen (Fenster «Anfrage» der Website für ein Zimmer, das Familienzimmer, Haus Apollo, Haus Arizona oder eine Frage zu den Preisen geöffnet)
#   buchung = Zimmer angefragt (dasselbe Fenster zeigt sein «Danke.»; in der Vorschau der Website geht nichts an das Haus)
#   booking = «Zimmer buchen» angeklickt (weiter zur Buchung bei seekda, HAUS.buchen in website/inhalt/daten.py)
#   tisch = Tisch-Anfrage begonnen (Fenster «Tisch im Röstihüs» geöffnet)
#   anfrage = Tisch im Röstihüs angefragt (das Fenster zeigt sein «Danke.»)
#   anruf = Telefon des Hauses (+41 27 957 10 12) · mail = E-Mail-Adresse des Hauses angeklickt (info@monte-moro.ch, öffnet das Fenster «Ihre Anfrage»)
#   chat = Chat der Rezeption geöffnet (Knopf unten rechts auf jeder Seite)
#   route = weiter zur Familie Zurbriggen (Spa nebenan im Wellness & Spa Pirmin Zurbriggen, Familienband im Fuss jeder Seite)
ZUR_BUCHUNG = {'buchung', 'booking'}   # «zur Buchung»: Zimmer angefragt oder weiter zu «Zimmer buchen»
SPRACHEN = ('de', 'en', 'fr', 'it', 'nl', 'es', 'pt', 'zh', 'ja', 'ko', 'ar', 'xx')   # Sprache des Browsers; xx = eine andere
GERAETE = ('handy', 'tablet', 'rechner')
PAUSE = 30 * 60        # nach einer halben Stunde ohne neue Seite beginnt ein neuer Besuch
LANG = 30 * 60         # länger als eine halbe Stunde sichtbar zählt eine Seite nicht
MAX_TAG = 4000         # Seitenaufrufe je Tag; darüber wird nichts mehr angenommen (Schutz vor Unfug)
AUFBEWAHREN = 400      # Tage; ältere Tagesdateien löscht aufraeumen() (Datenschutz: nicht länger als nötig)
AUTOMAT = re.compile(r'bot|crawl|spider|slurp|headless|lighthouse|preview|monitor|uptime|curl|wget|python|scrapy|facebookexternalhit|whatsapp|telegram|vercel', re.I)
_SCHLOSS = threading.Lock()

# Seiten des Hotel Monte-Moro nach Art (die Seiten aus bau.py der Website; Namen der Gruppen wie in allen Häusern, Inhalt aus diesem Haus)
KARTE = ('preise.html',)                       # Preise: Zimmer mit Frühstück und Halbpension, Inklusive, Zuschläge, Kinder (die «Karten» dieses Hauses)
ABEND = ('zimmer.html',)                       # Zimmer und Ferienwohnungen: hier wird ein Zimmer, das Familienzimmer oder eine Wohnung angefragt
ESSEN = ('roestihues.html',)                   # Restaurant Röstihüs: Röstis, Cordon bleus, Hotelweine, Tisch anfragen
ERLEBEN = ('saastal.html', 'spa.html')         # Saastal (Sommer und Winter), Spa nebenan im Partnerhotel
FESTE = ()                                     # keine eigene Seite für Feste oder Gutscheine
WEG = ('anreise.html',)                        # Anreise und Kontakt: Zug und Postauto, Auto, Telefon, E-Mail


class Konflikt(Exception):
    pass


def jetzt():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('Europe/Zurich'))
    except Exception:  # noqa: BLE001  ohne Zeitzonen-Daten: Uhr des Rechners
        return datetime.datetime.now()


def art_von(datei):
    if datei == 'index.html': return 'start'
    if datei in KARTE: return 'karte'
    if datei in ABEND: return 'abend'
    if datei in ESSEN: return 'essen'
    if datei in ERLEBEN: return 'erleben'
    if datei in FESTE: return 'feste'
    if datei in WEG: return 'weg'
    return 'sonst'


# ---- Speicher: lokal je Tag eine Datei. Ein Online-Teil ersetzt nur diese drei Funktionen.
def _lies(tag):
    try:
        with open(os.path.join(ORDNER, tag + '.json'), encoding='utf-8') as f:
            d = json.load(f)
        return (d if isinstance(d, dict) else {}), None
    except (OSError, ValueError):
        return {}, None


def _schreib(tag, d, marke):
    os.makedirs(ORDNER, exist_ok=True)
    p = os.path.join(ORDNER, tag + '.json')
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
    os.replace(p + '.neu', p)


def _tage_lesen(tage):
    return {t: _lies(t)[0] for t in tage}


# ---- Annehmen
def _kuerzel(tag, ip, ua):
    return hmac.new(GEHEIM, f'{tag}|{ip}|{ua}'.encode('utf-8', 'replace'), hashlib.sha256).hexdigest()[:10]


def _wort(s, n=60):
    return re.sub(r'[^\w\s\-’\'.()]', '', str(s or ''), flags=re.U).strip()[:n]


def melde(roh, ip='', ua='', land='', ort='', region=''):
    """Eine Zeile des Browsers. Angenommen wird nur, was genau dem Muster entspricht; alles andere fällt weg."""
    if not roh or len(roh) > 300 or AUTOMAT.search(ua or '') or not (ua or '').strip():
        return False
    try:
        t = roh.decode('ascii').strip().split(' ')
    except (UnicodeDecodeError, AttributeError):
        return False
    if len(t) != 8 or t[0] != 'r1':
        return False
    _, pv, datei, sp, geraet, sek, ereignisse, her = t
    if not (re.fullmatch(r'[a-z0-9]{4,8}', pv) and re.fullmatch(r'[a-z0-9-]{1,60}\.html', datei) and sp in SPRACHEN and geraet in GERAETE
            and re.fullmatch(r'\d{1,5}', sek) and (her == '-' or re.fullmatch(r'[a-z0-9.-]{3,60}', her))):
        return False
    e = [] if ereignisse == '-' else ereignisse.split(',')
    if any(x not in EREIGNISSE for x in e) or len(e) > len(EREIGNISSE):
        return False
    sek = min(int(sek), LANG)
    n = jetzt()
    tag, uhr = n.date().isoformat(), n.strftime('%H:%M:%S')
    kz = _kuerzel(tag, ip, ua)
    land = re.sub(r'[^A-Z]', '', (land or '').upper())[:2]
    for versuch in range(7):
        with _SCHLOSS:
            d, marke = _lies(tag)
            b = d.setdefault('b', {})
            if sum(len(x.get('a') or []) for x in b.values()) >= MAX_TAG:
                return False
            g = b.get(kz)
            if g is None:
                g = b[kz] = {'l': land, 'o': _wort(ort), 'r': _wort(region, 12), 'g': geraet, 'h': '' if her == '-' else her, 'a': []}
            alt = next((x for x in g['a'] if x.get('k') == pv), None)
            if alt is None:
                if len(g['a']) >= 400:
                    return False
                g['a'].append({'k': pv, 'z': uhr, 's': datei, 'sp': sp, 'sek': sek, 'e': sorted(set(e))})
            else:
                alt['sek'] = max(int(alt.get('sek') or 0), sek)
                alt['e'] = sorted(set(alt.get('e') or []) | set(e))
            try:
                _schreib(tag, d, marke)
                return True
            except Konflikt:
                pass
        time.sleep(0.05 + random.random() * 0.3 * (versuch + 1))
    return False


# ---- Auswerten
# Herkunftsnamen des Hotel Monte-Moro (Master G08): Suchmaschinen und Google Maps, die Portale, auf denen das Haus steht (Booking.com, Tripadvisor,
# Schweiz Tourismus myswitzerland.com; _kette/03-sammler/fakten.json › noten, social), die Ferienregion Saas-Fee/Saastal (saas-fee.ch), Wallis (valais.ch),
# Instagram (@hotelmonte_moro) und Facebook, die Häuser der Familie Zurbriggen (Wellness & Spa Pirmin Zurbriggen). Eine eigene Adresse der neuen Website
# steht noch nicht fest (nichts online): kommt sie, Zeile dazu.
HERKUNFT = (('google.', 'Google'), ('bing.', 'Bing'), ('duckduckgo.', 'DuckDuckGo'), ('ecosia.', 'Ecosia'), ('yahoo.', 'Yahoo'),
            ('booking.', 'Booking.com'), ('tripadvisor.', 'Tripadvisor'), ('holidaycheck.', 'HolidayCheck'), ('myswitzerland.', 'Schweiz Tourismus'),
            ('saas-fee.', 'Saas-Fee/Saastal'), ('valais.', 'Wallis'), ('wellnesshotel-zurbriggen.', 'Wellness & Spa Pirmin Zurbriggen'),
            ('instagram.', 'Instagram'), ('facebook.', 'Facebook'), ('youtube.', 'YouTube'), ('sbb.', 'SBB'),
            ('chatgpt.', 'ChatGPT'), ('perplexity.', 'Perplexity'))


def herkunft(h):
    if not h:
        return 'Direkt aufgerufen'
    for stueck, name in HERKUNFT:
        if stueck in h:
            return name
    return h[4:] if h.startswith('www.') else h


def _sek(z):
    h, m, s = (int(x) for x in z.split(':'))
    return h * 3600 + m * 60 + s


def besuche_aus(tage_inhalt):
    """Alle Besuche aus den Tagesdateien: je Gast und Tag die Seiten nach Uhrzeit, getrennt, wo eine halbe Stunde Pause lag."""
    aus = []
    for tag in sorted(tage_inhalt):
        for g in ((tage_inhalt[tag] or {}).get('b') or {}).values():
            a = sorted((x for x in (g.get('a') or []) if isinstance(x, dict) and x.get('z') and x.get('s')), key=lambda x: x['z'])
            teil = []
            for x in a:
                if teil and _sek(x['z']) - (_sek(teil[-1]['z']) + int(teil[-1].get('sek') or 0)) > PAUSE:
                    aus.append(_besuch(tag, g, teil)); teil = []
                teil.append(x)
            if teil:
                aus.append(_besuch(tag, g, teil))
    return aus


def _besuch(tag, g, a):
    e = set(y for x in a for y in (x.get('e') or []))
    return {'tag': tag, 'z': a[0]['z'][:5], 'zs': a[0]['z'][:8], 'l': g.get('l') or '', 'o': g.get('o') or '', 'r': g.get('r') or '', 'g': g.get('g') or 'rechner',
            'sp': a[0].get('sp') or 'de', 'h': herkunft(g.get('h') or ''), 'dauer': sum(int(x.get('sek') or 0) for x in a), 'seiten': len(a),
            'buchung': bool(e & ZUR_BUCHUNG), 'anfrage': bool(e & {'fenster', 'tisch'}), 'kontakt': bool(e & {'anruf', 'mail'}), 'chat': 'chat' in e,
            'route': 'route' in e,
            'weg': [{'z': x['z'][:5], 's': x['s'], 'sp': x.get('sp') or 'de', 'sek': int(x.get('sek') or 0), 'e': x.get('e') or []} for x in a]}


def _anteil(z, n):
    return round(min(100.0, 100.0 * z / n), 1) if n else None


def _rang(zaehler, n=12):
    return [{'k': k, 'n': v} for k, v in sorted(zaehler.items(), key=lambda x: (-x[1], str(x[0])))[:n]]


def _kurz(B):
    mit_zeit = [b['dauer'] for b in B if b['dauer'] > 0]
    seiten = sum(b['seiten'] for b in B)
    return {'besuche': len(B), 'seiten': seiten, 'buchung': sum(1 for b in B if b['buchung']), 'anfrage': sum(1 for b in B if b['anfrage']),
            'kontakt': sum(1 for b in B if b['kontakt']), 'route': sum(1 for b in B if b['route']),
            'dauer_mittel': round(sum(mit_zeit) / len(mit_zeit)) if mit_zeit else None,
            'seiten_je_besuch': round(seiten / len(B), 1) if B else None,
            'laender': len({b['l'] for b in B if b['l'] and b['l'] != '??'})}


def platz_bis(weg):
    """Stelle der Seite im Weg eines Besuchs, auf der er zur Buchung kam (Zimmer angefragt oder «Zimmer buchen»), sonst -1. Damit «Von welcher Seite zur Buchung»
    und «Startseite zur Buchung» etwas sagen, zählt jede Seite, die der Besuch bis dahin ansah (Pseudo-Ereignis «platz», Name wie in allen Häusern; Master G16)."""
    return next((i for i, x in enumerate(weg) if ZUR_BUCHUNG & set(x.get('e') or [])), -1)


def werte_aus(summe):
    """Die neun Werte der Ansicht «Zur Buchung» aus den gezählten Aufrufen und Klicks (summe(ereignis, art, geraet)). Eine Rechnung für Dienst und Ablage.
    Hotel Monte-Moro: «zur Buchung» = Zimmer angefragt oder weiter zu «Zimmer buchen» (seekda). Ohne nächsten Schritt = Zimmer-Anfrage begonnen, aber nicht
    abgeschickt (je Öffnen gezählt, nie unter null). Die Schlüssel bleiben wie in allen Häusern, die Bedeutung steht oben bei EREIGNISSE."""
    def wert(z, n, **mehr):
        return dict(zahl=z, von=n, anteil=_anteil(z, n), **mehr)
    auf = summe('seite')
    return {
        'start': wert(summe('platz', 'start'), summe('seite', 'start')),   # Aufrufe der Startseite in Besuchen, die danach zur Buchung kamen
        'karte': wert(summe('platz', 'karte'), summe('seite', 'karte')),   # dasselbe für «Preise»
        'booking': wert(summe('booking'), summe('buchung') + summe('booking'), anfrage=summe('buchung')),   # «Zimmer buchen» unter allen Wegen zur Buchung, dazu angefragte Zimmer
        'abbruch': wert(max(0, summe('fenster') - summe('buchung')), summe('fenster')),
        'tisch': wert(summe('tisch'), auf, abend=summe('tisch', 'essen')),   # Tisch-Anfrage begonnen, davon auf «Röstihüs»
        'anfrage': wert(summe('anfrage'), auf, start=summe('anfrage', 'essen')),   # Tisch im Röstihüs angefragt, davon auf «Röstihüs»
        'kontakt': wert(summe('anruf') + summe('mail'), auf, anruf=summe('anruf'), mail=summe('mail')),
        'chat': wert(summe('chat'), auf, dc=summe('chat', 'start')),   # Chat der Rezeption geöffnet, davon auf der Startseite
        'route': wert(summe('route'), auf, weg=summe('route', 'erleben')),   # weiter zur Familie Zurbriggen, davon auf «Saastal» oder «Spa nebenan»
    }


def stand(tage=30, beispiel=False, ablage=False):
    """Alles, was die Besucherliste zeigt, für die letzten Tage (heute eingeschlossen) und zum Vergleich den gleich langen Zeitraum davor.
    Nichts geschätzt: wo nichts gemessen ist, steht None."""
    try:
        tage = max(1, min(366, int(tage)))
    except (TypeError, ValueError):
        tage = 30
    bis = jetzt().date()
    von = bis - datetime.timedelta(days=tage - 1)
    liste = [(von + datetime.timedelta(days=i)).isoformat() for i in range(tage)]
    vorher_liste = [(von - datetime.timedelta(days=tage - i)).isoformat() for i in range(tage)]
    inhalt = _beispiel(vorher_liste + liste, voll=ablage) if beispiel else _tage_lesen(vorher_liste + liste)
    alle = besuche_aus(inhalt)
    hier = set(liste)
    B = [b for b in alle if b['tag'] in hier]
    V = [b for b in alle if b['tag'] not in hier]

    je_tag = {t: {'tag': t, 'besuche': 0, 'seiten': 0, 'buchung': 0} for t in liste}
    vor_tag = {t: 0 for t in vorher_liste}
    laender, orte, sprachen, geraete, her, stunden = (collections.Counter() for _ in range(6))
    raster = [[0] * 24 for _ in range(7)]
    land_tag = collections.defaultdict(collections.Counter)
    seiten = {}
    S = collections.Counter()
    for b in V:
        vor_tag[b['tag']] += 1
    for b in B:
        je_tag[b['tag']]['besuche'] += 1
        je_tag[b['tag']]['seiten'] += b['seiten']
        je_tag[b['tag']]['buchung'] += 1 if b['buchung'] else 0
        laender[b['l'] or '??'] += 1
        land_tag[b['l'] or '??'][b['tag']] += 1
        if b['o']:
            orte[(b['o'], b['l'])] += 1
        sprachen[b['sp']] += 1
        geraete[b['g']] += 1
        her[b['h']] += 1
        h = int(b['z'][:2])
        stunden[h] += 1
        raster[datetime.date.fromisoformat(b['tag']).weekday()][h] += 1
        pb = platz_bis(b['weg'])
        for i, x in enumerate(b['weg']):
            s = seiten.setdefault(x['s'], {'s': x['s'], 'n': 0, 'sek': 0, 'gemessen': 0, 'buchung': 0})
            s['n'] += 1
            if x['sek'] > 0:
                s['sek'] += x['sek']; s['gemessen'] += 1
            a = art_von(x['s'])
            S[('seite', a, b['g'])] += 1
            if i <= pb:   # diese Seite lag auf dem Weg zum Tisch
                s['buchung'] += 1
                S[('platz', a, b['g'])] += 1
            for e in x['e']:
                S[(e, a, b['g'])] += 1

    def summe(ereignis, art=None, geraet=None):
        return sum(n for (e, a, g), n in S.items() if e == ereignis and art in (None, a) and geraet in (None, g))

    heute = bis.isoformat()
    mit_daten = [t for t in liste if je_tag[t]['besuche']]
    k, kv = _kurz(B), _kurz(V)
    # Woche für Woche (Montag bis Sonntag), damit der Verlauf auch bei 90 Tagen lesbar bleibt
    wochen = collections.OrderedDict()
    for t in liste:
        d = datetime.date.fromisoformat(t)
        mo = (d - datetime.timedelta(days=d.weekday())).isoformat()
        w = wochen.setdefault(mo, {'von': t, 'bis': t, 'tage': 0, 'besuche': 0, 'buchung': 0})
        w['bis'] = t; w['tage'] += 1; w['besuche'] += je_tag[t]['besuche']; w['buchung'] += je_tag[t]['buchung']
    top = [x['k'] for x in _rang(laender, 5) if x['k'] != '??'][:4]
    aus = {
        'tage': tage, 'von': von.isoformat(), 'bis': heute, 'seit': mit_daten[0] if mit_daten else None, 'leer': not B, 'beispiel': bool(beispiel),
        'summe': dict(k, heute=je_tag[heute]['besuche']),
        'vorher': dict(kv, von=vorher_liste[0], bis=vorher_liste[-1]),
        'je_tag': [je_tag[t] for t in liste],
        'vor_tag': [vor_tag[t] for t in vorher_liste],
        'wochen': list(wochen.values()),
        'land_verlauf': [{'k': l, 'n': [land_tag[l].get(t, 0) for t in liste]} for l in top],
        'stunden': [stunden.get(h, 0) for h in range(24)],
        'raster': raster,
        'laender': _rang(laender, 20),
        'orte': [{'k': o[0], 'l': o[1], 'n': n} for o, n in sorted(orte.items(), key=lambda x: (-x[1], x[0]))[:20]],
        'sprachen': _rang(sprachen), 'geraete': _rang(geraete), 'herkunft': _rang(her, 14),
        'seiten': sorted(({'s': s['s'], 'n': s['n'], 'sek': round(s['sek'] / s['gemessen']) if s['gemessen'] else None, 'buchung': s['buchung']} for s in seiten.values()),
                         key=lambda x: (-x['n'], x['s'])),
        'werte': werte_aus(summe),
        'besuche': sorted(B, key=lambda b: (b['tag'], b['zs']), reverse=True)[:400 + (je_tag[heute]['besuche'] if ablage else 0)],   # Ablage: heute ganz dazu, registre.js kürzt
    }
    if ablage:   # was registre.js braucht, um abgelegte Beispielwerte genau auf «heute bis jetzt» zu kürzen (Carlton, Prüfung 16.10.2026)
        mz = [b['dauer'] for b in B if b['dauer'] > 0]
        aus['roh'] = {'dauer': [sum(mz), len(mz)], 'seiten_sek': {s['s']: [s['sek'], s['gemessen']] for s in seiten.values()},
                      'S': [[e, a, g, n] for (e, a, g), n in sorted(S.items())], 'laender': _rang(laender, 999), 'herkunft': _rang(her, 999),
                      'orte': [{'k': o[0], 'l': o[1], 'n': n} for o, n in sorted(orte.items(), key=lambda x: (-x[1], x[0]))],
                      'land_tag': {l: [land_tag[l].get(t, 0) for t in liste] for l in land_tag}, 'heute_voll': True}
    return aus


# ---- Beispielwerte: erfunden, damit das Haus sieht, wie die Besucherliste mit Besuchen aussieht. Immer als Beispiel gekennzeichnet.
# Orte und Herkunft passend zu einem Hotel im Saastal: die meisten Besuche aus der Deutschschweiz (Zürich, Bern, Basel, Luzern …) und aus dem Wallis,
# dazu die Romandie und das Tessin, Süddeutschland und das übrige Deutschland, Norditalien über den Monte-Moro-Pass, wenige von weiter her.
# Gefunden über Google, Booking.com, Schweiz Tourismus, die Ferienregion Saas-Fee/Saastal und Instagram; oft am Rechner (Ferien plant man in Ruhe),
# gesucht am Abend und am Sonntag, wenn Ferien geplant werden. Keine echten Zahlen des Hauses.
def _beispiel(liste, voll=False):
    jt = jetzt()
    heute, jetzt_sek = jt.date(), jt.hour * 3600 + jt.minute * 60 + jt.second
    orte = [('CH', 'Zürich', 'ZH', 'de', 12), ('CH', 'Zürich', 'ZH', 'en', 2), ('CH', 'Bern', 'BE', 'de', 7), ('CH', 'Basel', 'BS', 'de', 5),
            ('CH', 'Luzern', 'LU', 'de', 4), ('CH', 'Winterthur', 'ZH', 'de', 3), ('CH', 'St. Gallen', 'SG', 'de', 3), ('CH', 'Aarau', 'AG', 'de', 2),
            ('CH', 'Baden', 'AG', 'de', 2), ('CH', 'Thun', 'BE', 'de', 2), ('CH', 'Zug', 'ZG', 'de', 2), ('CH', 'Solothurn', 'SO', 'de', 1),
            ('CH', 'Chur', 'GR', 'de', 1), ('CH', 'Schaffhausen', 'SH', 'de', 1), ('CH', 'Visp', 'VS', 'de', 3), ('CH', 'Brig-Glis', 'VS', 'de', 2),
            ('CH', 'Naters', 'VS', 'de', 1), ('CH', 'Sion', 'VS', 'fr', 1), ('CH', 'Genf', 'GE', 'fr', 2), ('CH', 'Lausanne', 'VD', 'fr', 2),
            ('CH', 'Lugano', 'TI', 'it', 1), ('DE', 'München', 'BY', 'de', 3), ('DE', 'Stuttgart', 'BW', 'de', 3), ('DE', 'Freiburg im Breisgau', 'BW', 'de', 2),
            ('DE', 'Frankfurt am Main', 'HE', 'de', 2), ('DE', 'Köln', 'NW', 'de', 2), ('DE', 'Karlsruhe', 'BW', 'de', 1), ('DE', 'Konstanz', 'BW', 'de', 1),
            ('DE', 'Nürnberg', 'BY', 'de', 1), ('DE', 'Hamburg', 'HH', 'de', 1), ('DE', 'Berlin', 'BE', 'de', 1), ('IT', 'Mailand', '25', 'it', 2),
            ('IT', 'Domodossola', '21', 'it', 1), ('IT', 'Macugnaga', '21', 'it', 1), ('NL', 'Amsterdam', 'NH', 'nl', 2), ('NL', 'Utrecht', 'UT', 'nl', 1),
            ('BE', 'Antwerpen', 'VAN', 'nl', 1), ('FR', 'Lyon', 'ARA', 'fr', 1), ('AT', 'Wien', '9', 'de', 1), ('GB', 'London', 'ENG', 'en', 1),
            ('US', 'New York', 'NY', 'en', 1)]
    her = [('', 24), ('www.google.ch', 22), ('www.google.com', 5), ('www.google.de', 6), ('www.booking.com', 8), ('www.myswitzerland.com', 5),
           ('www.saas-fee.ch', 5), ('www.tripadvisor.ch', 3), ('www.instagram.com', 4), ('l.instagram.com', 2), ('www.facebook.com', 2),
           ('www.holidaycheck.de', 1), ('www.valais.ch', 1), ('www.wellnesshotel-zurbriggen.ch', 2), ('www.bing.com', 2), ('duckduckgo.com', 1),
           ('chatgpt.com', 1), ('www.sbb.ch', 1)]
    seiten = ['zimmer.html', 'preise.html', 'saastal.html', 'spa.html', 'roestihues.html', 'anreise.html']
    selten = ['impressum.html', 'datenschutz.html']
    gew = lambda l: z.choices(l, weights=[x[-1] for x in l])[0]   # z ist der Zufall des jeweiligen Tages
    aus = {}
    for tag in liste:
        d = datetime.date.fromisoformat(tag)
        z = random.Random('montemoro-saas-almagell-' + tag)   # je Tag fest: derselbe Tag zeigt in 7, 30 und 90 Tagen dieselben Besuche
        wt, alter = d.weekday(), (heute - d).days
        n = int(15 * (1 - alter / 300) * (1.05, 1.0, 1.0, 0.95, 0.9, 0.95, 1.2)[wt] * z.uniform(0.75, 1.25))
        b = {}
        for j in range(n):
            land, ort, region, sp, _ = gew(orte)
            geraet = z.choices(GERAETE, weights=(58, 9, 33))[0]
            t = beginn = int(min(23.9, z.triangular(0.0, 24.0, 19.5)) * 3600)
            weg = ['index.html'] if z.random() < 0.55 else [z.choices(['zimmer.html', 'preise.html', 'roestihues.html', 'saastal.html', 'anreise.html', 'spa.html'],
                                                                       weights=(30, 22, 18, 16, 8, 6))[0]]
            for _ in range(z.choices(range(0, 7), weights=(20, 22, 20, 15, 11, 7, 5))[0]):
                neu = z.choice(seiten) if z.random() < 0.94 else z.choice(selten)
                if neu != weg[-1]:   # dieselbe Seite nie zweimal hintereinander
                    weg.append(neu)
            a = []
            for i, s in enumerate(weg):
                art = art_von(s)
                sek = int(z.triangular(6, 150, 28)) + (int(z.uniform(30, 140)) if art in ('karte', 'abend', 'essen') else 0)
                e = []
                r = z.random()
                if art == 'abend':                                                           # Zimmer und Ferienwohnungen
                    if r < 0.28:
                        e = ['fenster'] + (['buchung'] if z.random() < 0.4 else [])          # Zimmer-Anfrage begonnen, abgeschickt
                    elif r < 0.46:
                        e = ['booking']                                                      # «Zimmer buchen» (seekda)
                    elif r < 0.50:
                        e = ['chat']                                                         # Chat der Rezeption
                elif art == 'karte':                                                         # Preise
                    if r < 0.14:
                        e = ['fenster'] + (['buchung'] if z.random() < 0.35 else [])        # Frage zu den Preisen
                    elif r < 0.30:
                        e = ['booking']
                    elif r < 0.34:
                        e = ['mail']
                elif art == 'essen':                                                         # Röstihüs
                    if r < 0.20:
                        e = ['tisch'] + (['anfrage'] if z.random() < 0.45 else [])           # Tisch im Röstihüs begonnen, angefragt
                    elif r < 0.25:
                        e = ['anruf']
                elif art == 'weg':                                                           # Anreise und Kontakt
                    if r < 0.12:
                        e = ['anruf']
                    elif r < 0.20:
                        e = ['mail']
                    elif r < 0.26:
                        e = ['booking']
                elif s == 'spa.html':
                    if r < 0.18:
                        e = ['route']                                                        # weiter zum Wellness & Spa Pirmin Zurbriggen
                    elif r < 0.24:
                        e = ['booking']
                elif s == 'saastal.html':
                    if r < 0.05:
                        e = ['route']
                    elif r < 0.10:
                        e = ['booking']
                elif art == 'start':
                    if r < 0.09:
                        e = ['booking']
                    elif r < 0.14:
                        e = ['chat']
                    elif r < 0.17:
                        e = ['route']                                                        # Familienband im Fuss
                    elif r < 0.20:
                        e = ['fenster'] + (['buchung'] if z.random() < 0.3 else [])         # Familienzimmer anfragen
                elif r < 0.02:
                    e = ['anruf']
                a.append({'k': 'b%03d%02d' % (j, len(a)), 'z': '%02d:%02d:%02d' % (t // 3600 % 24, t // 60 % 60, t % 60), 's': s, 'sp': sp, 'sek': sek, 'e': sorted(set(e))})
                t += sek + z.randint(1, 4)
                if t >= 24 * 3600 - 5 or ZUR_BUCHUNG & set(e):
                    break
            h = gew(her)[0]
            # heute nur bis jetzt; erst nach dem ganzen Besuch weggelassen, damit der Zufall der folgenden Besuche gleich bleibt
            # (die Ablage nimmt den ganzen Tag, registre.js kürzt beim Anzeigen genau gleich, Carlton-Prüfung 16.10.2026)
            if alter == 0 and beginn > jetzt_sek and not voll:
                continue
            b['bsp%04d' % j] = {'l': land, 'o': ort, 'r': region, 'g': geraet, 'h': h, 'a': a}
        aus[tag] = {'b': b}
    return aus


def ausfuhr(tage=30):
    """Alle Besuche der letzten Tage (heute eingeschlossen), neueste zuerst, ohne Obergrenze: für «Als Tabelle sichern» (Datenexport, Master 9d Punkt 21).
    Dieselben Angaben wie im Werkzeug, kein Kürzel, keine Adresse."""
    try:
        tage = max(1, min(AUFBEWAHREN, int(tage)))
    except (TypeError, ValueError):
        tage = 30
    bis = jetzt().date()
    liste = [(bis - datetime.timedelta(days=tage - 1 - i)).isoformat() for i in range(tage)]
    B = besuche_aus(_tage_lesen(liste))
    return {'tage': tage, 'von': liste[0], 'bis': liste[-1], 'besuche': sorted(B, key=lambda b: (b['tag'], b['zs']), reverse=True)}


def ablage_heute(tage=30, heute=None, uhr=None):
    """Die abgelegten Beispielwerte (beispiel/<tage>.json), auf heute geschoben und auf die jetzige Uhrzeit in Saas-Almagell (Europe/Zurich) gekürzt.
    Dieselbe Rechnung wie registre.js (ablageLaden, kuerzen), damit die Besucherliste und das Hotelbüro dieselben Beispielzahlen zeigen.
    Fehlt die Datei: Beispielwerte frisch gerechnet (stand)."""
    try:
        tage = int(tage)
    except (TypeError, ValueError):
        tage = 30
    p = os.path.join(HIER, 'beispiel', f'{tage}.json')
    if tage not in (7, 30, 90) or not os.path.exists(p):
        return stand(tage, beispiel=True)
    d = json.load(open(p, encoding='utf-8'))
    n = jetzt()
    heute = heute or n.date().isoformat()
    uhr = uhr or n.strftime('%H:%M:%S')
    um = (datetime.date.fromisoformat(heute) - datetime.date.fromisoformat(d['bis'])).days
    sch = lambda t: (datetime.date.fromisoformat(t) + datetime.timedelta(days=um)).isoformat()
    if um:
        for k in ('von', 'bis', 'seit'):
            if d.get(k):
                d[k] = sch(d[k])
        d['vorher']['von'], d['vorher']['bis'] = sch(d['vorher']['von']), sch(d['vorher']['bis'])
        for t in d['je_tag']:
            t['tag'] = sch(t['tag'])
        for b in d['besuche']:
            b['tag'] = sch(b['tag'])
        r7 = list(d['raster'])
        d['raster'] = [r7[(w - um) % 7] for w in range(7)]
    R = d.pop('roh', None)
    if R and R.get('heute_voll'):
        _kuerzen(d, R, uhr)
    wochen = collections.OrderedDict()
    for t in d['je_tag']:
        dd = datetime.date.fromisoformat(t['tag'])
        mo = (dd - datetime.timedelta(days=dd.weekday())).isoformat()
        w = wochen.setdefault(mo, {'von': t['tag'], 'bis': t['tag'], 'tage': 0, 'besuche': 0, 'buchung': 0})
        w['bis'] = t['tag']; w['tage'] += 1; w['besuche'] += t['besuche']; w['buchung'] += t['buchung']
    d['wochen'] = list(wochen.values())
    return d


def _kuerzen(d, R, uhr):
    u, L, heute = d['summe'], len(d['je_tag']) - 1, d['bis']
    weg = [b for b in d['besuche'] if b['tag'] == heute and (b.get('zs') or b['z'] + ':00') > uhr]
    if not weg:
        d['besuche'] = d['besuche'][:400]
        return

    def minus(liste, k, l=None):
        for x in liste:
            if x['k'] == k and (l is None or x.get('l') == l):
                x['n'] -= 1
                return
    SS = collections.Counter({(e, a, g): z for e, a, g, z in R['S']})
    wtag = datetime.date.fromisoformat(heute).weekday()
    for b in weg:
        u['besuche'] -= 1; u['seiten'] -= b['seiten']; u['heute'] -= 1
        u['buchung'] -= 1 if b['buchung'] else 0; u['anfrage'] -= 1 if b['anfrage'] else 0; u['kontakt'] -= 1 if b['kontakt'] else 0; u['route'] -= 1 if b.get('route') else 0
        if b['dauer'] > 0:
            R['dauer'][0] -= b['dauer']; R['dauer'][1] -= 1
        t = d['je_tag'][L]; t['besuche'] -= 1; t['seiten'] -= b['seiten']; t['buchung'] -= 1 if b['buchung'] else 0
        l = b['l'] or '??'
        minus(R['laender'], l)
        if l in R['land_tag']:
            R['land_tag'][l][L] -= 1
        if b['o']:
            minus(R['orte'], b['o'], b['l'])
        minus(d['sprachen'], b['sp']); minus(d['geraete'], b['g']); minus(R['herkunft'], b['h'])
        h = int(b['z'][:2]); d['stunden'][h] -= 1; d['raster'][wtag][h] -= 1
        pb = platz_bis(b['weg'])
        for i, x in enumerate(b['weg']):
            for s in d['seiten']:
                if s['s'] == x['s']:
                    s['n'] -= 1; s['buchung'] -= 1 if i <= pb else 0
                    break
            if x['sek'] > 0 and x['s'] in R['seiten_sek']:
                R['seiten_sek'][x['s']][0] -= x['sek']; R['seiten_sek'][x['s']][1] -= 1
            a = art_von(x['s'])
            for e in ['seite'] + list(x['e']) + (['platz'] if i <= pb else []):
                SS[(e, a, b['g'])] -= 1
    ids = {id(b) for b in weg}
    d['besuche'] = [b for b in d['besuche'] if id(b) not in ids][:400]
    u['dauer_mittel'] = round(R['dauer'][0] / R['dauer'][1]) if R['dauer'][1] else None
    u['seiten_je_besuch'] = round(u['seiten'] / u['besuche'], 1) if u['besuche'] else None
    u['laender'] = len([x for x in R['laender'] if x['n'] > 0 and x['k'] not in ('??', '')])
    rang = lambda l, n: sorted((x for x in l if x['n'] > 0), key=lambda x: (-x['n'], str(x['k'])))[:n]
    d['laender'], d['herkunft'] = rang(R['laender'], 20), rang(R['herkunft'], 14)
    d['sprachen'], d['geraete'] = rang(d['sprachen'], 12), rang(d['geraete'], 12)
    d['orte'] = sorted((x for x in R['orte'] if x['n'] > 0), key=lambda x: (-x['n'], x['k'], x['l']))[:20]
    for s in d['seiten']:
        q = R['seiten_sek'].get(s['s'])
        s['sek'] = round(q[0] / q[1]) if q and q[1] else None
    d['seiten'] = sorted((s for s in d['seiten'] if s['n'] > 0), key=lambda x: (-x['n'], x['s']))
    top = [x['k'] for x in rang(R['laender'], 5) if x['k'] != '??'][:4]
    d['land_verlauf'] = [{'k': k, 'n': R['land_tag'].get(k) or [0] * (L + 1)} for k in top]

    def summe(e, a=None, g=None):
        return sum(z for (e2, a2, g2), z in SS.items() if e2 == e and a in (None, a2) and g in (None, g2))
    d['werte'] = werte_aus(summe)
    mit = [t['tag'] for t in d['je_tag'] if t['besuche']]
    d['seit'], d['leer'] = (mit[0] if mit else None), not u['besuche']


def ablage():
    """beispiel/<tage>.json: dieselben Beispielwerte als Dateien, für ein Werkzeug ohne Server-Teil (registre.js verschiebt die Tage auf heute)."""
    p = os.path.join(HIER, 'beispiel')
    os.makedirs(p, exist_ok=True)
    for t in (7, 30, 90):
        json.dump(stand(t, beispiel=True, ablage=True), open(os.path.join(p, f'{t}.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return p


# Seiten ohne eigenes Foto im Inhalt bekommen je ein anderes Foto des Hauses (Schlüssel aus BILDER in website/inhalt/bilder.py), nie dasselbe zweimal
ERSATZ = ('haus-winter-g', 'dorf-schnee', 'stube-holz', 'speiseraum')
# Fotos der anderen Häuser der Familie (f-…, fam-…) und das gerechnete Nebelmeer (…-ki) taugen nicht als Bild einer Seite des Monte-Moro
KEIN_SEITENBILD = re.compile(r'^(f|fam)-|-ki$')


def seiten_namen():
    """seiten.json: Datei → Name der Seite, so wie die Website sie selbst nennt: die Namen der Leiste der Startseite (nav: Zimmer, Preise, Saastal,
    Spa, Röstihüs, Anreise) und Impressum/Datenschutz aus ihrem Fuss; die Startseite heisst «Startseite». Nichts abgetippt.
    seiten-bilder.json: je Seite das erste Foto in ihrem Inhalt (nicht der Fuss, der auf jeder Seite gleich ist), das noch keine andere Seite trägt
    (Fehlerbuch 10a, Robert 19.10.2026: jede Liste zeigt zu jedem Eintrag sein Bild; nie ein Foto doppelt). Kleinste Fassung -s.webp (480 px) aus
    website/assets/img/ (Bildregister BILDER in website/inhalt/bilder.py); Fotos der anderen Häuser der Familie ausgenommen."""
    import html
    wurzel = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')   # die Website liegt in website/ neben _werkzeuge/
    start = open(os.path.join(wurzel, 'index.html'), encoding='utf-8').read()
    namen = {'index.html': 'Startseite'}
    fuss = start[start.find('<footer'):] if '<footer' in start else ''
    teile = [m.group(1) for m in re.finditer(r'<nav[^>]*>(.*?)</nav>', start, re.S)] + [fuss]
    for teil in teile:
        for datei, name in re.findall(r'<a [^>]*?href="([a-z0-9-]+\.html)"[^>]*>(.*?)</a>', teil, re.S):
            name = html.unescape(re.sub(r'<[^>]+>', '', name)).strip()
            if name and datei != 'index.html' and os.path.exists(os.path.join(wurzel, datei)):
                namen.setdefault(datei, name)
    p = os.path.join(HIER, 'seiten.json')
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        json.dump(namen, f, ensure_ascii=False, indent=1)
    os.replace(p + '.neu', p)
    bilder = {}
    da = lambda b: os.path.exists(os.path.join(wurzel, 'assets', 'img', b + '-s.webp'))
    for n in namen:
        try:
            h = open(os.path.join(wurzel, n), encoding='utf-8').read()
        except OSError:
            continue
        h = h[:h.find('<footer')] if '<footer' in h else h
        for b in dict.fromkeys(re.findall(r'assets/img/([A-Za-z0-9_-]+?)-[smlx]\.webp', h)):
            if not KEIN_SEITENBILD.search(b) and 'assets/img/' + b + '-s.webp' not in bilder.values() and da(b):
                bilder[n] = 'assets/img/' + b + '-s.webp'
                break
        else:   # Seite ohne eigenes Foto im Inhalt (Impressum, Datenschutz): das nächste freie Foto des Hauses aus ERSATZ, nie eins doppelt
            frei = [x for x in ERSATZ if 'assets/img/' + x + '-s.webp' not in bilder.values() and da(x)]
            if frei:
                bilder[n] = 'assets/img/' + frei[0] + '-s.webp'
    with open(os.path.join(HIER, 'seiten-bilder.json'), 'w', encoding='utf-8') as f:
        json.dump(bilder, f, ensure_ascii=False, indent=1)
    return namen


def leeren():
    """Zählung lokal leeren: der bisherige Ordner bleibt als <ordner>.vor-leeren liegen (eine Fassung zurück)."""
    import shutil
    with _SCHLOSS:
        if os.path.isdir(ORDNER):
            ziel = ORDNER + '.vor-leeren'
            shutil.rmtree(ziel, ignore_errors=True)
            os.replace(ORDNER, ziel)
        os.makedirs(ORDNER, exist_ok=True)


def aufraeumen():
    grenze = (jetzt().date() - datetime.timedelta(days=AUFBEWAHREN)).isoformat()
    weg = 0
    if os.path.isdir(ORDNER):
        for f in os.listdir(ORDNER):
            if re.fullmatch(r'\d{4}-\d\d-\d\d\.json', f) and f[:10] < grenze:
                os.remove(os.path.join(ORDNER, f)); weg += 1
    return weg


if __name__ == '__main__':
    was = sys.argv[1] if len(sys.argv) > 1 else ''
    if was == 'ablage':
        print('Beispielwerte abgelegt:', ablage())
    elif was == 'seiten':
        print(len(seiten_namen()), 'Seiten →', os.path.join(HIER, 'seiten.json'))
    elif was == 'leeren':
        leeren(); print('Zählung geleert:', ORDNER)
    elif was == 'aufraeumen':
        print(aufraeumen(), 'Tagesdateien gelöscht (älter als', AUFBEWAHREN, 'Tage)')
    else:
        d = stand(30, beispiel=(was == 'beispiel'))
        d['besuche'] = d['besuche'][:3]
        print(json.dumps({k: d[k] for k in ('tage', 'von', 'bis', 'beispiel', 'summe', 'vorher', 'besuche')}, ensure_ascii=False, indent=1))
