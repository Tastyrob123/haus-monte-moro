"""Der Chat des Hotel Monte-Moro, Saas-Almagell (Hotel mit Restaurant Röstihüs, Gastgeber Esther und Fabian Zurbriggen).
Kopie aus dem Culinarium Hannover über Wild Side (08.11.2026), Zimmer, Ferienwohnungen und Röstihüs statt Bar.
Auf der Website antwortet die Rezeption im Chat heute ohne KI aus assets/js/wissen.json; in der Rezeption läuft dieser Chat unter «Chat ausprobieren»
(Python ohne Zusatzpakete, ohne RECEPTION_KI=1 mit Probe-Antworten aus probe_ki.py).

Eingang (POST, JSON):
  {"messages":[{"role":"user"|"assistant","content":"…"}], "mappe":bool, "sprache":"de|en|fr", "heute":"YYYY-MM-DD"}   Gästechat
  {"modus":"anfrage", "mail":"…", "hinweis":"…"}                                                                     Antwort-Entwurf auf eine Anfrage
Wissen: gast_wissen.txt (Angaben der Seiten des Hauses) und gast_umgebung.txt (Kontakt, Lage, was das Haus nicht veröffentlicht). Ohne Orte in gast_haus.json
holt der Chat kein Wetter (am Rechner nichts aus dem Netz). Der Chat antwortet nur daraus.
Schlüssel: nur mit RECEPTION_KI=1 und ANTHROPIC_API_KEY in der Umgebung (server.py). Schutz gegen Missbrauch: Grenzen je Besucher und je Tag (siehe GRENZEN),
nur Aufrufe von der eigenen Seite."""
from http.server import BaseHTTPRequestHandler
import collections, datetime, json, os, re, threading, time, urllib.request, urllib.error

HIER = os.path.dirname(os.path.abspath(__file__))
def _lies(n):
    try:
        return open(os.path.join(HIER, n), encoding='utf-8').read()
    except OSError:
        return ''
WISSEN = _lies('gast_wissen.txt')
TAL = _lies('gast_umgebung.txt')
# Das Haus (gast_haus.json daneben, aus website/inhalt/daten.py, _bau/montemoro_wissen.py). Ohne die Datei startet der Chat nicht mit fremden Werten:
# Vorfall 10.10.2026 (Carlton-Hundepreise als Antwort im Gasterntal), deshalb stehen hier keine Werte und kein Muster eines anderen Hauses mehr.
HAUS = {'name': 'Hotel Monte-Moro', 'ort': 'Saas-Almagell', 'tel': '', 'mail': '', 'kontakt': '', 'adresse': '', 'zeiten': '', 'fahrplan': '', 'kategorien': [], 'orte': [],
        'art': 'Hotel mit Restaurant Röstihüs', 'ruhetage': '', 'reservation_name': 'Zimmer buchen'}
try:
    HAUS.update(json.loads(_lies('gast_haus.json') or '{}'))
except ValueError:
    pass
MUSTER_CARLTON = ''
REGELN_MEHR = f'''- Sprache: Schreibt der Gast Englisch, Französisch oder eine andere Sprache, antwortest du vollständig in seiner Sprache, auch die Punkte. Nur bei deutschen Fragen deutsch.
- Du bist ein KI-Assistent, kein Mensch. Wenn jemand fragt, sag das.
- Bleib beim {HAUS['name']}, seinen Zimmern und Ferienwohnungen, Preisen, dem Röstihüs, dem Spa im Partnerhotel, {HAUS['ort']}, dem Saastal und dem Weg dorthin. Zu anderen Themen freundlich zurück zum Haus.
- Persönliche Daten (Kreditkarten, Ausweise, Zugänge) nimmst du nicht entgegen; dafür ist die Rezeption da.
- Schreibe immer zuerst deine Antwort an den Gast, dann erst ein Werkzeug.
- Widersprechen sich die Seiten der Website und eine ältere Unterlage, gilt die Website.
- Sagt eine Seite «auf Anfrage» oder nennt keinen Preis, nennst du auch keinen.'''   # 15.10.2026: vorher standen diese Regeln versehentlich im Muster
MUSTER = HAUS.get('muster') or MUSTER_CARLTON
MODELL = 'claude-sonnet-5-5'   # Robert 10.10.2026: alle Häuser auf Sonnet 5.5 (Haiku 4.5 irrte bei Öffnungstagen und erfand Ausflüge; davor Opus 5.5).
MODELL = HAUS.get('modell') or MODELL   # je Haus umstellbar (gast_haus.json)
GRENZE = 1000 if 'haiku' in MODELL else 4000   # Sonnet denkt vor der Antwort mit; mit 1000 brach die Antwort mitten im Satz ab (10.10.2026)
TEL = HAUS['tel']
MAIL = HAUS['mail']
KONTAKT = HAUS.get('kontakt') or ' oder '.join(x for x in (TEL, MAIL) if x)   # Monte-Moro: die Rezeption am Telefon oder per E-Mail
HOECHSTENS_NACHRICHTEN = 12   # nur die letzten Beiträge reisen mit
HOECHSTENS_ZEICHEN = 600      # je Frage
# Grenzen gegen Missbrauch: je Besucher (IP) und gesamt je Tag. Darüber antwortet die Rezeption freundlich mit der Telefonnummer.
GRENZEN = {'besucher_10min': 20, 'besucher_tag': 80, 'gesamt_tag': 2000, 'anfrage_tag': 60}
SPRACHE = {'de': 'Deutsch, Schweizer Schreibung (ss statt ß, «Guillemets»), immer «Sie»', 'en': 'Englisch (britische Schreibung)', 'fr': 'Französisch (vouvoiement)'}

ANWEISUNG = f"""Du bist die Rezeption im Chat des {HAUS['name']} in {HAUS['ort']} ({HAUS['art']}) und beantwortest Fragen der Gäste im Chatfenster der Website.

Regeln:
- Antworte nur mit dem, was in WISSEN oder TALWISSEN steht. WISSEN sind die Angaben der Seiten des Hauses (Startseite, Zimmer, Preise, Röstihüs, Spa, Saastal, Anreise) und die Fragen und Antworten der Website; TALWISSEN sind Kontakt, Lage und was das Haus nicht veröffentlicht. Erfinde nichts dazu, auch keine Preise, Zeiten, freien Zimmer oder Regeln.
- Steht die Antwort nirgends, sag das offen: Esther und Fabian beantworten das gern persönlich, {KONTAKT}. Nenne dann keine Zahl und keine Zeit. Rufe dann zusätzlich das Werkzeug nicht_belegt auf.
- Was das Haus nicht veröffentlicht (Öffnungszeiten des Röstihüs, Strasse, Storno, Preise der Ferienwohnungen, Check-in und Check-out), beantwortest du nie mit einer Zahl, sondern mit dem Weg zur Rezeption. Die Gratis-Anreise mit dem öffentlichen Verkehr ist abgelaufen; biete sie nie an.
- Zimmer buchen: Du prüfst nichts selbst und sagst nie, ein Zimmer sei frei. Rufe das Werkzeug reservieren auf, sobald der Gast ein Zimmer buchen oder anfragen will; der Weg ist «Zimmer buchen» auf der Website, per Telefon oder E-Mail. Für einen Tisch im Röstihüs: Telefon {TEL} oder TheFork.
- Form (wichtig, der Gast liest auf dem Handy): Erst EIN kurzer Satz mit der direkten Antwort. Wenn es mehrere Angaben gibt (Preise, Zeiten, Ablauf), danach höchstens vier Punkte, jeder auf einer eigenen Zeile, beginnend mit «- », im Muster «Stichwort: Angabe». Kein Absatz länger als zwei Sätze. Nur, was gefragt ist; Zusätzliches höchstens als ein kurzer Satz am Schluss.
- Ton wie die Website: immer «Sie», herzlich, ruhig, wie eine gute Rezeption in den Bergen. Jeder Satz wertet den Aufenthalt auf (der einzelne Gast, die Familie, der Berg, das Röstihüs); nie Menge, nie Abfertigung. Nie «gute Frage», «gerne doch», «leider» am Satzanfang oder andere Floskeln. Keine Emojis, kein Fettdruck, keine Überschriften, keine Gedankenstriche. Preise wie die Website: CHF 90.00, im Röstihüs Fr. 25.–.
- Nichts Ungefragtes: Fragt jemand nach dem Weg, kein Wort zum Preis. Fragt jemand nach dem Röstihüs, nichts zum Spa.
{REGELN_MEHR}

So sehen gute Antworten aus (nur die FORM übernehmen; Zahlen und Angaben stammen immer aus WISSEN dieses Hauses, nie aus den Mustern):
{MUSTER}

WISSEN:
{WISSEN}

TALWISSEN:
{TAL or '(keins)'}"""

# ANFRAGE: Grundfassung; die Rezeption setzt beim Einbinden ihre eigene (reception.ANFRAGE_GBR) ein.
ANFRAGE = f"""Du schreibst im Namen von Esther und Fabian Zurbriggen, {HAUS['name']} in {HAUS['ort']}, den Entwurf einer Antwort an einen Gast (Zimmer, Ferienwohnung, Tisch im Röstihüs, Nachricht).

Regeln:
- Alles, was du an Preisen, Zeiten, Zimmern und Leistungen nennst, steht wörtlich in WISSEN. Erfinde nichts.
- Freie Zimmer und Tische kannst du nicht prüfen: setz dafür [Zimmer prüfen] bzw. [Tisch prüfen].
- Was in der Anfrage fehlt (Anreise, Abreise, Gäste, Zimmerart), erfragst du freundlich am Ende, in einer kurzen Liste.
- Was das Team selbst entscheiden muss, markierst du in eckigen Klammern, zum Beispiel [Preis bestätigen].
- Ton der Website: Sie, herzlich, ruhig, keine Werbesprache, keine Emojis, kein Fettdruck. Kurze Absätze. Schweizer Schreibung (ss statt ß).
- Sprache: die Sprache der Anfrage.
- Form: Zeile 1 «Betreff: …», dann Leerzeile, dann die Antwort mit Anrede und Gruss «Herzliche Grüsse aus Saas-Almagell» und darunter «Esther und Fabian Zurbriggen», «{HAUS['name']}».
- Nach der Antwort eine Zeile «---» und darunter für das Team, nicht für den Gast: «Grundlage:» mit den Seiten, aus denen die Angaben stammen, und «Offen:» mit dem, was das Team vor dem Senden klären muss.

WISSEN:
{WISSEN}"""

WERKZEUGE = [{
    'name': 'reservieren',
    'description': 'Zeigt dem Gast im Chat den Weg zu «Zimmer buchen» auf der Website (Buchungsfenster des Hauses; dazu Telefon und E-Mail). Aufrufen, sobald der Gast ein Zimmer buchen oder anfragen will. Eintragen, was der Gast schon genannt hat, den Rest null lassen.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False,
                     'required': ['datum', 'uhrzeit', 'personen'],
                     'properties': {'datum': {'type': ['string', 'null'], 'description': 'Anreise und Abreise, wie der Gast sie nennt, oder null'},
                                    'uhrzeit': {'type': ['string', 'null'], 'description': 'Zimmerart (Budgetzimmer, Standardzimmer, Familienzimmer, Ferienwohnung) oder null'},
                                    'personen': {'type': ['integer', 'null'], 'description': 'Anzahl Gäste oder null'}}}},
    {
    'name': 'nicht_belegt',
    'description': 'Vermerk für das Haus: Die Frage des Gastes liess sich aus WISSEN und TALWISSEN nicht beantworten. Das Team sieht diese Fragen in seinem Werkzeug und trägt die Antwort nach.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False, 'required': ['thema'],
                     'properties': {'thema': {'type': 'string', 'description': 'Worum es ging, in zwei bis vier Wörtern auf Deutsch, z. B. «Check-in-Zeit»'}}}}]
MAPPE = """

Zusatz: Der Gast wohnt bereits im Haus. Antworte wie die Rezeption vor Ort (was heute im Röstihüs ist, wann der Kidsclub offen hat), nicht wie für jemanden, der erst buchen will."""

# ---------------------------------------------------------------- Wetter (Open-Meteo, frei, ohne Schlüssel), 30 Minuten gemerkt
WMO = {0: 'klar', 1: 'überwiegend klar', 2: 'teils bewölkt', 3: 'bedeckt', 45: 'Nebel', 48: 'Raureifnebel', 51: 'leichter Niesel', 53: 'Niesel', 55: 'starker Niesel',
       61: 'leichter Regen', 63: 'Regen', 65: 'starker Regen', 66: 'gefrierender Regen', 67: 'gefrierender Regen', 71: 'leichter Schneefall', 73: 'Schneefall', 75: 'starker Schneefall',
       77: 'Schneegriesel', 80: 'Regenschauer', 81: 'Regenschauer', 82: 'heftige Regenschauer', 85: 'Schneeschauer', 86: 'starke Schneeschauer', 95: 'Gewitter', 96: 'Gewitter mit Hagel', 99: 'Gewitter mit Hagel'}
ORTE = [tuple(o) for o in HAUS['orte']]
_WETTER = {'zeit': 0, 'text': ''}

def wetter():
    if time.time() - _WETTER['zeit'] < 1800 and _WETTER['text']:
        return _WETTER['text']
    zeilen = []
    try:
        for name, la, lo in ORTE:
            u = (f'https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&current=temperature_2m,weather_code'
                 '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunset&timezone=Europe%2FZurich&forecast_days=3')
            with urllib.request.urlopen(u, timeout=4) as r:
                d = json.load(r)
            c, t = d['current'], d['daily']
            zeilen.append(f"{name}: jetzt {c['temperature_2m']:.0f} °C, {WMO.get(c['weather_code'], 'unbekannt')}. " + ' · '.join(
                f"{tag}: {WMO.get(w, '?')}, {lo_:.0f} bis {hi:.0f} °C, Regen {p} %, Sonnenuntergang {s[-5:]}"
                for tag, w, lo_, hi, p, s in zip(t['time'], t['weather_code'], t['temperature_2m_min'], t['temperature_2m_max'], t['precipitation_probability_max'], t['sunset'])))
        _WETTER.update(zeit=time.time(), text='Vorhersage Open-Meteo, abgerufen ' + datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))).strftime('%d.%m.%Y %H:%M') + '\n' + '\n'.join(zeilen))
    except Exception:  # noqa: BLE001  ohne Wetter antwortet die Rezeption trotzdem
        pass
    return _WETTER['text'] or '(kein Wetter: das Haus nennt keins)'

# ---------------------------------------------------------------- Grenzen je Besucher und Tag (im Speicher der laufenden Funktion)
SCHLOSS = threading.Lock()
BESUCHER = collections.defaultdict(list)
TAG = {'tag': '', 'n': 0, 'anfrage': 0}

def erlaubt(ip, art='gast'):
    jetzt, heute = time.time(), time.strftime('%Y-%m-%d')
    with SCHLOSS:
        if TAG['tag'] != heute:
            TAG.update(tag=heute, n=0, anfrage=0); BESUCHER.clear()
        if art == 'anfrage':
            if TAG['anfrage'] >= GRENZEN['anfrage_tag']:
                return False
            TAG['anfrage'] += 1
            return True
        z = [t for t in BESUCHER[ip] if jetzt - t < 86400]
        if len(z) >= GRENZEN['besucher_tag'] or len([t for t in z if jetzt - t < 600]) >= GRENZEN['besucher_10min'] or TAG['n'] >= GRENZEN['gesamt_tag']:
            BESUCHER[ip] = z
            return False
        z.append(jetzt); BESUCHER[ip] = z; TAG['n'] += 1
        return True

GRENZE_TEXT = {'de': f'Sie haben in kurzer Zeit sehr viele Fragen gestellt. Damit jeder Gast eine Antwort bekommt, mache ich hier kurz Pause. Die Rezeption ist direkt für Sie da: {TEL} oder {MAIL}.',
               'en': f'You have asked a great many questions in a short time. So that every guest gets an answer, I will pause here for a moment. Our reception is happy to help directly: {TEL} or {MAIL}.',
               'fr': f'Vous avez posé beaucoup de questions en peu de temps. Pour que chaque client reçoive une réponse, je fais une petite pause. La réception vous aide volontiers : {TEL} ou {MAIL}.'}
NICHTS = {'de': f'Dazu kann ich hier nichts sagen. Esther und Fabian helfen Ihnen gern persönlich weiter: {TEL} oder {MAIL}.',
          'en': f'I am afraid I cannot help with that here. Esther and Fabian will gladly assist you personally: {TEL} or {MAIL}.',
          'fr': f'Je ne peux malheureusement pas vous renseigner ici. Esther et Fabian vous aident volontiers personnellement : {TEL} ou {MAIL}.'}

def _api(koerper):
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages', data=json.dumps(koerper).encode('utf-8'), method='POST',
        headers={'content-type': 'application/json', 'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01',
                 'anthropic-workspace-id': os.environ.get('ANTHROPIC_WORKSPACE_ID', '')})   # Nutzer-Schlüssel brauchen den Arbeitsbereich dazu
    with urllib.request.urlopen(req, timeout=55) as r:
        return json.load(r)


def frage(messages, mappe=False, heute='', sprache='de'):
    verlauf = []
    for m in messages[-HOECHSTENS_NACHRICHTEN:]:
        rolle = 'assistant' if m.get('role') == 'assistant' else 'user'
        inhalt = str(m.get('content', ''))[:HOECHSTENS_ZEICHEN].strip()
        if not inhalt:
            continue
        if verlauf and verlauf[-1]['role'] == rolle:   # zwei gleiche Rollen nacheinander nimmt die API nicht
            verlauf[-1]['content'] += '\n' + inhalt
        else:
            verlauf.append({'role': rolle, 'content': inhalt})
    if not verlauf or verlauf[0]['role'] != 'user':
        verlauf.insert(0, {'role': 'user', 'content': 'Hallo'})
    if verlauf[-1]['role'] != 'user':
        verlauf.append({'role': 'user', 'content': 'Mach bitte weiter.'})
    sp = sprache if sprache in SPRACHE else 'de'
    # Sprache der letzten Frage erkennen: Haiku antwortete auf englische Fragen sonst deutsch (10.10.2026)
    letzte = verlauf[-1]['content'].lower()
    worte = set(re.findall(r"[a-zäöüéèàç']+", letzte))
    if len(worte & {'the', 'is', 'are', 'do', 'does', 'can', 'we', 'you', 'there', 'what', 'how', 'when', 'where', 'our', 'my', 'have', 'bring', 'serve'}) >= 2: sp = 'en'
    elif len(worte & {'le', 'la', 'les', 'est', 'vous', 'nous', 'avez', 'quel', 'quelle', 'pour', 'chien', 'peut', 'comment', 'où', 'je', 'une', 'des'}) >= 2: sp = 'fr'
    antwort = _api({
        'model': MODELL, 'max_tokens': GRENZE, 'tools': WERKZEUGE,
        'system': [{'type': 'text', 'text': ANWEISUNG, 'cache_control': {'type': 'ephemeral'}},
                   {'type': 'text', 'text': (MAPPE if mappe else '') + f'\n\nWETTER:\n{wetter()}\n\nHeute ist {heute or time.strftime("%Y-%m-%d")}. Antworte auf {SPRACHE[sp]}.'}],
        'messages': verlauf})
    if antwort.get('stop_reason') == 'refusal':
        return {'text': NICHTS[sp], 'belegt': False, 'thema': 'abgelehnt'}
    text = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    werk = {b.get('name'): b.get('input') for b in antwort.get('content', []) if b.get('type') == 'tool_use'}
    maske, lucke = werk.get('reservieren'), werk.get('nicht_belegt')
    # Ruft die Rezeption die Buchungsmaske auf, endet ihr Text dort. Fragte der Gast dazu noch etwas (Spa, Essen, Anreise), blieb das
    # unbeantwortet oder endete mit einem Doppelpunkt (10.10.2026). Darum ein zweiter, kurzer Schritt: die Rezeption sieht die Maske
    # als erledigt und ergänzt nur, was noch offen ist. Der Zwischenspeicher macht den zweiten Schritt billig.
    if maske and antwort.get('stop_reason') == 'tool_use':
        try:
            erg = _api({
                'model': MODELL, 'max_tokens': GRENZE, 'tools': WERKZEUGE,
                'system': [{'type': 'text', 'text': ANWEISUNG, 'cache_control': {'type': 'ephemeral'}},
                           {'type': 'text', 'text': (MAPPE if mappe else '') + f'\n\nWETTER:\n{wetter()}\n\nHeute ist {heute or time.strftime("%Y-%m-%d")}. Antworte auf {SPRACHE[sp]}.'}],
                'messages': verlauf + [{'role': 'assistant', 'content': antwort['content']},
                                       {'role': 'user', 'content': [{'type': 'tool_result', 'tool_use_id': b['id'],
                                        'content': 'Der Weg zu «Zimmer buchen» steht jetzt unter deiner Antwort. Ist eine Frage des Gastes (ausser freie Zimmer) noch nicht beantwortet, '
                                                   'beantworte sie jetzt als höchstens fünf Punkte «- Stichwort: Angabe», nur mit Angaben, die so in WISSEN stehen, in der Sie-Form. Keine Einleitung, keine Überschrift, kein Fettdruck, keine Frage am Schluss, die Maske nicht erwähnen. Ist alles beantwortet, antworte nur mit OK.'}
                                        for b in antwort['content'] if b.get('type') == 'tool_use']}]})
            mehr = ''.join(x.get('text', '') for x in erg.get('content', []) if x.get('type') == 'text').strip()
            if mehr and erg.get('stop_reason') != 'refusal' and mehr.rstrip('.').upper() != 'OK':
                text = (text + '\n' + mehr).strip()
        except Exception:  # noqa: BLE001
            pass
        if text.endswith(':'):   # nichts nachgekommen: den angefangenen Satz nicht stehen lassen
            text = text.rsplit('\n', 1)[0].strip() if '\n' in text else ''
    if not text:
        text = ({'de': 'Mit «Zimmer buchen» auf der Website geht es am schnellsten; die Rezeption ist auch am Telefon und per E-Mail für Sie da.', 'en': 'The quickest way is «Zimmer buchen» on our website; our reception is also there for you by phone and email.',
                 'fr': 'Le plus simple : « Zimmer buchen » sur notre site ; la réception est aussi joignable par téléphone et par e-mail.'} if maske else NICHTS)[sp]
    n = antwort.get('usage', {})
    return {'text': text, 'maske': maske, 'belegt': not lucke, 'thema': (lucke or {}).get('thema', ''),
            'tokens': {'ein': n.get('input_tokens'), 'cache': n.get('cache_read_input_tokens'), 'aus': n.get('output_tokens')}}


def anfrage(mail, hinweis=''):
    antwort = _api({
        'model': MODELL, 'max_tokens': 3000 if 'haiku' in MODELL else 7000,   # Sonnet denkt mit: mit 3000 brach der Entwurf mitten in der Liste ab (10.10.2026)
       
        'system': [{'type': 'text', 'text': ANFRAGE, 'cache_control': {'type': 'ephemeral'}},
                   {'type': 'text', 'text': f'Heute ist {time.strftime("%Y-%m-%d")}.'}],
        'messages': [{'role': 'user', 'content': 'ANFRAGE:\n' + mail[:12000] + ('\n\nHINWEIS DES TEAMS:\n' + hinweis[:2000] if hinweis.strip() else '')}]})
    if antwort.get('stop_reason') == 'refusal':
        return {'text': '', 'fehler': 'Diese Anfrage lässt sich nicht automatisch beantworten. Bitte selbst schreiben.'}
    text = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    mail_teil, _, team = text.partition('\n---')
    m = re.match(r'\s*Betreff:\s*(.+)\n', mail_teil)
    return {'betreff': m.group(1).strip() if m else '', 'text': (mail_teil[m.end():] if m else mail_teil).strip(), 'team': team.strip()}


ABDECKEN = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'), '[E-Mail]'), (re.compile(r'(?:\+|00)?\d[\d\s/().-]{7,}\d'), '[Nummer]')]

def merke(host, daten):
    """Frage und Antwort an den Speicher fürs Studio (fragen.js). Mail-Adressen und Nummern der Gäste werden vorher abgedeckt.
    Scheitert das, bleibt die Antwort an den Gast davon unberührt."""
    geheim = os.environ.get('GAST_GEHEIM')
    if not geheim or not host:
        return
    for muster, ersatz in ABDECKEN:
        daten['frage'] = muster.sub(ersatz, daten.get('frage', ''))
    try:
        req = urllib.request.Request(f'https://{host}/api/fragen', data=json.dumps(daten).encode('utf-8'), method='POST',
                                     headers={'content-type': 'application/json', 'x-gast-geheim': geheim})
        urllib.request.urlopen(req, timeout=4).close()
    except Exception:  # noqa: BLE001
        pass


class handler(BaseHTTPRequestHandler):
    def _sende(self, code, daten):
        roh = json.dumps(daten, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(roh)))
        self.end_headers()
        self.wfile.write(roh)

    def _ip(self):
        return (self.headers.get('x-forwarded-for') or self.client_address[0] or '').split(',')[0].strip()

    def do_GET(self):
        self._sende(200, {'ok': True, 'modell': MODELL, 'wissen_zeichen': len(WISSEN), 'tal_zeichen': len(TAL), 'wetter': wetter()[:80]})

    def do_POST(self):
        try:
            host = (self.headers.get('host') or '').split(':')[0]
            herkunft = self.headers.get('origin') or self.headers.get('referer') or ''
            if herkunft and host and f'//{host}' not in herkunft:   # nur Aufrufe von der eigenen Seite
                return self._sende(403, {'fehler': 'nicht erlaubt'})
            n = int(self.headers.get('Content-Length') or 0)
            if n > 40000:
                return self._sende(413, {'fehler': 'zu lang'})
            daten = json.loads(self.rfile.read(n) or b'{}')
            if daten.get('modus') == 'anfrage':
                mail = str(daten.get('mail') or '').strip()
                if len(mail) < 20:
                    return self._sende(400, {'fehler': 'Bitte die Anfrage einfügen.'})
                if not erlaubt(self._ip(), 'anfrage'):
                    return self._sende(429, {'fehler': 'Für heute sind genug Entwürfe geschrieben. Morgen geht es weiter.'})
                return self._sende(200, anfrage(mail, str(daten.get('hinweis') or '')))
            messages = daten.get('messages') or []
            if not isinstance(messages, list):
                return self._sende(400, {'fehler': 'messages fehlt'})
            sp = str(daten.get('sprache') or 'de')[:2]
            sp = sp if sp in SPRACHE else 'de'
            if not erlaubt(self._ip()):
                return self._sende(200, {'text': GRENZE_TEXT[sp], 'grenze': True})
            a = frage(messages, mappe=bool(daten.get('mappe')), heute=str(daten.get('heute', ''))[:10], sprache=sp)
            letzte = next((str(m.get('content', '')) for m in reversed(messages) if m.get('role') == 'user'), '')
            merke(host, {'frage': letzte[:HOECHSTENS_ZEICHEN], 'antwort': a['text'][:2000], 'belegt': a.get('belegt', True), 'thema': a.get('thema', ''),
                         'mappe': bool(daten.get('mappe')), 'sprache': sp, 'buchung': bool(a.get('maske'))})
            self._sende(200, a)
        except urllib.error.HTTPError as e:
            self._sende(502, {'fehler': 'api', 'status': e.code, 'text': e.read().decode('utf-8', 'replace')[:400]})
        except Exception as e:  # noqa: BLE001
            self._sende(500, {'fehler': type(e).__name__, 'text': str(e)[:300]})

    def log_message(self, *a):   # Vercel schreibt die Zugriffe selbst
        pass
