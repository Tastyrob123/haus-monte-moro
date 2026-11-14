"""Die Rezeption (Team hinter dem Gäste-Chat) · Hotel Monte-Moro, Saas-Almagell (08.11.2026, Stamm Culinarium Hannover über Wild Side).
Das Hotel Monte-Moro mit Restaurant Röstihüs, Familie Zurbriggen, Gastgeber Esther und Fabian Zurbriggen: Zimmer mit Frühstück oder Halbpension,
Familienzimmer, Residence Alpenhof, Ferienwohnungen Haus Apollo und Haus Arizona, Tisch im Röstihüs. Alle Angaben aus website/inhalt/daten.py.

Zwei Dinge kommen herein:
  Eingang      Das Anfrage-Fenster der Website (assets/js/anfrage.js: Hotelzimmer, Familienzimmer, Haus Apollo, Haus Arizona, Tisch im Röstihüs, Frage zu den
               Preisen, Ihre Anfrage; Name, E-Mail oder Telefon, Tag, Uhrzeit, Personen, Nachricht) und Anfragen aus dem Chat, sobald ein Gast Name und
               Kontakt nennt (Zimmer, Ferienwohnung, Tisch im Röstihüs, Nachricht). Das Team bekommt dazu einen Antwortentwurf im Ton der Website (Sie,
               herzlich, ruhig), auf Grundlage dessen, was das Haus selbst schreibt (vorlagen/), ändert ihn und schickt ihn selbst. Hier wird nichts verschickt.
               Zu jeder Anfrage stehen Hinweise aus den Angaben des Hauses dabei: Einzelzimmerzuschlag, Kurzaufenthalt, Kinder, Hund, Familienzimmer bis
               6 Personen, Preise der Ferienwohnungen nicht veröffentlicht, Öffnungszeiten des Röstihüs nicht veröffentlicht, Allergien, Gratis-Anreise abgelaufen.
  Gefragt      Jede Frage mit Antwort. Wo der Chat keine Antwort hatte (Werkzeug «nicht_belegt»), trägt das Team sie einmal nach;
               ab dann antwortet der Chat damit (Block «NACHGETRAGEN VOM TEAM» in der Anweisung).

Speicher: Dateien unter daten/ (oder RECEPTION_DATEN), im selben Aufbau wie der Online-Speicher beim Carlton (Vercel Blob, _gast/fragen.js):
  fragen/JJJJ-MM-TT/<zeit>-<zufall>.json · anfragen/JJJJ-MM-TT/<zeit>-<zufall>.json · nachgetragen.json · status.json
Einträge älter als zwölf Monate werden gelöscht (Datenschutz; der Satz dazu steht auf der Website noch nicht, siehe LIEFERUNG.md).

Eingebunden von server.py: reception.einbinden(gast_modul) hängt sich an gast/gast.py, ohne die Datei zu ändern."""
import datetime, glob, hashlib, html, json, os, random, re, shutil, threading, time
try:   # «Das weiss der Chat» (16.10.2026, nur lokal): Berichtigungen und Ergänzungen des Teams am Wissen. Online fehlt die Datei: dann wie bisher.
    import gedaechtnis
except ImportError:
    gedaechtnis = None

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')   # die Website des Hauses (nur gelesen)
DATEN = os.environ.get('RECEPTION_DATEN') or os.environ.get('REZEPTION_DATEN') or os.path.join(HIER, 'daten')
def _name(teil='gaeste', standard='Anfragen & Chat'):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/montemoro.js › namen), nie fest im Code."""
    try:
        s = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'montemoro.js'), encoding='utf-8').read()
        m = re.search(r"namen:\s*\{([^}]*)\}", s)
        n = re.search(teil + r":\s*'([^']+)'", m.group(1)) if m else None
        return n.group(1) if n else standard
    except OSError:
        return standard


NAME = _name()
NAME_IM = ('im ' + NAME[4:]) if NAME.startswith('Das ') else ('in der ' + NAME[4:]) if NAME.startswith('Die ') else ('im ' + NAME[4:]) if NAME.startswith('Der ') else ('in ' + NAME)   # «in der Rezeption»

SCHLOSS = threading.Lock()
LOKAL = threading.local()


def _haus_daten():
    """website/inhalt/daten.py (nur gelesen): alle Angaben des Hauses an einer Stelle, für Hinweise und Kontakt."""
    import importlib.util
    try:
        s = importlib.util.spec_from_file_location('mm_daten_rezeption', os.path.join(WEB, 'inhalt', 'daten.py'))
        m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
        return m
    except (OSError, SyntaxError):
        return None


D = _haus_daten()
ARTEN = {'zimmer': 'Zimmer', 'wohnung': 'Ferienwohnung', 'tisch': 'Tisch im Röstihüs', 'nachricht': 'Nachricht'}   # Hotel mit Restaurant (08.11.2026)
# Kontakt des Hauses (daten.py HAUS, Impressum): Telefon und E-Mail der Rezeption; die Strasse ist nicht belegt (OFFEN) und steht nirgends.
MAIL = D.HAUS['mail'] if D else 'info@monte-moro.ch'
TEL = D.HAUS['tel'] if D else '+41 27 957 10 12'
KONTAKT = f'Telefon {TEL} · {MAIL}'
VORLAGE = {'zimmer': ('zimmer', KONTAKT), 'wohnung': ('wohnung', KONTAKT), 'tisch': ('tisch', KONTAKT), 'nachricht': ('', KONTAKT)}
VORLAGEN_DATEIEN = ('zimmer.txt', 'wohnung.txt', 'tisch.txt')
# Die «Abteilung» ist im Haus die Art der Arbeit (wer sich darum kümmert); alle Wege gehen an dieselbe Adresse der Rezeption.
ABTEILUNG_VON = {}
ART_ABTEILUNG = {'zimmer': 'Zimmer', 'wohnung': 'Ferienwohnungen', 'tisch': 'Röstihüs', 'nachricht': 'Nachrichten'}
FORMULARE = ('zimmer', 'tisch', 'allgemein')
# Allergien: das Anfrage-Fenster der Website hat kein Feld dafür; ein späteres Feld nimmt diese Namen (die 14 Allergene der Schweizer Verordnung, gekürzt).
ALLERGENE = {k: k for k in ('Gluten', 'Laktose', 'Ei', 'Fisch', 'Krebstiere', 'Erdnüsse', 'Nüsse', 'Soja', 'Sellerie', 'Senf', 'Sesam')}
TAG_NAME = {0: 'Montag', 1: 'Dienstag', 2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 6: 'Sonntag'}
FAMILIE_BIS = 6   # «Familienzimmer und Familienkombinationen - ideal für 3 - 6 Personen» (daten.py FAMILIE_TEXT)
SPRACHEN = ('de', 'en', 'fr')
# Themen für «Das wurde gefragt»: Wortlisten in den Sprachen der Gäste, erste passende gewinnt
THEMEN = [('Ferienwohnungen', r'ferienwohnung|wohnung|apollo|arizona|apartment|flat'),
          ('Kinder & Familie', r'kind|kidsclub|familie|baby|family|child|enfant'),
          ('Röstihüs', r'rösti|roesti|röstihüs|cordon|raclette|stübli|wein|essen|restaurant|tisch|allerg|vegan|vegetar|gluten|menu|dinner|food|table'),
          ('Spa', r'spa\b|wellness|sauna|schwimm|massage|pool|whirlpool'),
          ('Inklusive & Saastal', r'inklusive|inbegriffen|bergbahn|metro|wander|\bski|saastal|ausflug|sommer|winter|gratis|included|hiking'),
          ('Anreise & Lage', r'anreise|zug|postauto|\bauto\b|visp|park|bus\b|skigebiet|lift|weg\b|wo ist|adresse|strasse|train|where|arrive'),
          ('Zimmer & Preise', r'zimmer|preis|kost|chf|franken|halbpension|frühstück|einzel|zuschlag|kurtaxe|euro|bezahl|buchen|room|price|book'),
          ('Das Haus', r'hund|check|storno|esther|fabian|zurbriggen|haus\b|rezeption|dog|who')]
ABDECKEN = [(re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'), '[E-Mail]'), (re.compile(r'(?:\+|00)?\d[\d\s/().-]{7,}\d'), '[Nummer]')]

# ---------------------------------------------------------------- Dateien
def _pfad(*t):
    return os.path.join(DATEN, *t)

def _lies(p, standard):
    try:
        return json.load(open(p, encoding='utf-8'))
    except OSError:
        return standard
    except ValueError:              # beschädigt: die letzte gute Fassung nehmen
        try:
            return json.load(open(p + '.gut', encoding='utf-8'))
        except (OSError, ValueError):
            return standard

def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.neu'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        json.load(open(p, encoding='utf-8')); shutil.copy2(p, p + '.gut')   # nur eine lesbare Fassung wird zur Sicherung
    except (OSError, ValueError):
        pass
    os.replace(tmp, p)

def _neue_id(art):
    jetzt = datetime.datetime.now().astimezone()
    zeit = jetzt.isoformat(timespec='seconds')
    return zeit, f'{art}/{zeit[:10]}/{zeit.replace(":", "-").replace("+", "_")}-{random.randrange(36**6):06x}.json'

def _gueltig(id_, art):
    return bool(re.fullmatch(art + r'/\d{4}-\d{2}-\d{2}/[\w.-]+\.json', id_ or '')) and os.path.exists(_pfad(id_))

def _alle(art):
    l = []
    for f in sorted(glob.glob(_pfad(art, '*', '*.json')), reverse=True):
        d = _lies(f, None)
        if d:
            d['id'] = os.path.relpath(f, DATEN)
            l.append(d)
    return l

def aufraeumen():
    """Einträge älter als zwölf Monate löschen (ganze Tagesordner)."""
    grenze = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    n = 0
    for art in ('fragen', 'anfragen'):
        for o in glob.glob(_pfad(art, '*')):
            if os.path.basename(o) < grenze:
                shutil.rmtree(o, ignore_errors=True); n += 1
    return n


# ---------------------------------------------------------------- Ablegen (aus dem Chat)
def thema_von(text):
    t = (text or '').lower()
    for name, muster in THEMEN:
        if re.search(muster, t):
            return name
    return 'Weitere Fragen'

def lege_frage(daten):
    for muster, ersatz in ABDECKEN:
        daten['frage'] = muster.sub(ersatz, daten.get('frage', ''))
    zeit, id_ = _neue_id('fragen')
    e = {'zeit': zeit, 'frage': str(daten.get('frage', ''))[:600], 'antwort': str(daten.get('antwort', ''))[:2000], 'belegt': daten.get('belegt') is not False,
         'thema': str(daten.get('thema', ''))[:80], 'gruppe': thema_von(daten.get('frage', '')), 'sprache': str(daten.get('sprache', 'de'))[:2],
         'buchung': bool(daten.get('buchung')), 'mappe': bool(daten.get('mappe')), 'anfrage': daten.get('anfrage') or ''}
    if daten.get('beispiel'):
        e['beispiel'] = True; e['probe'] = True
    with SCHLOSS:
        _schreib(_pfad(id_), e)
    if random.random() < 0.05:
        aufraeumen()
    return id_

def lege_anfrage(eingabe, gespraech, sprache, verlauf):
    """Legt eine Anfrage ab. Kommt im selben Gespräch dieselbe Art noch einmal (Gast ergänzt Datum oder Personen), wird sie ergänzt, nicht verdoppelt."""
    art = eingabe.get('art') if eingabe.get('art') in ARTEN else 'nachricht'
    with SCHLOSS:
        for a in _alle('anfragen')[:80]:
            if a.get('gespraech') == gespraech and a.get('art') == art and a.get('status') != 'erledigt':
                for k in ('name', 'kontakt', 'datum', 'personen', 'anliegen'):
                    if eingabe.get(k) not in (None, ''):
                        a[k] = eingabe[k]
                a['verlauf'] = verlauf; a['entwurf'] = None; a['geaendert'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
                id_ = a.pop('id'); _schreib(_pfad(id_), a)
                return id_
        zeit, id_ = _neue_id('anfragen')
        _schreib(_pfad(id_), {'zeit': zeit, 'art': art, 'name': str(eingabe.get('name') or '')[:120], 'kontakt': str(eingabe.get('kontakt') or '')[:160],
                              'datum': str(eingabe.get('datum') or '')[:120], 'personen': eingabe.get('personen'), 'anliegen': str(eingabe.get('anliegen') or '')[:1200],
                              'sprache': sprache, 'gespraech': gespraech, 'verlauf': verlauf, 'status': 'neu', 'entwurf': None})
        return id_


# ---------------------------------------------------------------- Beispiele im Eingang
BEISPIEL_STAND = 4   # Monte-Moro: eigene Beispiele des Hauses ab Stand 4 (08.11.2026)   # 3: deutsche Lesefassungen der fremdsprachigen Briefe (16.10.2026) · 1: fünf Anfragen und neun Fragen (13./14.10.2026) · 2: zwölf Anfragen, 24 Fragen, drei Antworten des Teams, Entwürfe neu geschrieben (15.10.2026)


def _jetzt():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('Europe/Zurich'))
    except Exception:
        return datetime.datetime.now().astimezone()


def _zeit_vor(jetzt, vor):
    tage, h, m = vor
    z = (jetzt - datetime.timedelta(days=tage)).replace(hour=h, minute=m, second=0, microsecond=0)
    if z > jetzt:
        z -= datetime.timedelta(days=1)
    return z.isoformat(timespec='seconds')


def _stand(marke):
    """Welcher Beispiel-Stand liegt in diesem Datenordner: 0 = noch keiner, 1 = alte Marke ohne Stand."""
    if not os.path.exists(marke):
        return 0
    return int(_lies(marke, {}).get('stand') or 1)


def _quelle(e):
    """Kennung des Textstands, aus dem eine Lesefassung stammt: ändert das Team den Brief, ist die Übersetzung veraltet."""
    return hashlib.sha1(((e.get('betreff') or '') + '\n' + (e.get('text') or '')).encode('utf-8')).hexdigest()[:12]


UEBERSETZEN = """Du übersetzt für Esther und Fabian Zurbriggen (Hotel Monte-Moro mit Restaurant Röstihüs in Saas-Almagell) einen Antwortbrief an einen Gast und das Gespräch, das der Gast im Chat geführt hat, ins Deutsche.
Die Übersetzung ist nur zum Mitlesen für das Team und wird nie verschickt. Übersetze genau und vollständig, nichts weglassen, nichts hinzufügen,
Schweizer Schreibung wie die Website (ss statt ß, «Guillemets», Sie-Form). Stellen in eckigen Klammern bleiben in eckigen Klammern, übersetzt. Namen, Adressen, Zahlen und Preise bleiben, wie sie sind.
Antworte ausschliesslich mit JSON: {"betreff": "…", "text": "…", "verlauf": ["…", …]} – «verlauf» hat genau so viele Einträge wie im Eingang, in derselben Reihenfolge."""

def uebersetzen(id_):
    """Deutsche Lesefassung eines fremdsprachigen Briefs und seines Chat-Gesprächs (Robert 16.10.2026: «der Mitarbeiter … muss das auch nochmal kurz
    übersetzen können … sehen, wie das übersetzt aussieht, bevor er es abschickt»). Wird gespeichert und gilt, bis der Brief geändert wird."""
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {})
    e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('ÜBERSETZEN · Es gibt noch keinen Brief.')
    q = _quelle(e)
    if (e.get('deutsch') or {}).get('quelle') == q and a.get('verlauf_de'):
        return {'deutsch': e['deutsch'], 'verlauf_de': a['verlauf_de']}
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen.')
    verlauf = [v.get('text', '') for v in a.get('verlauf') or []]
    eingabe = json.dumps({'betreff': e.get('betreff', ''), 'text': e['text'], 'verlauf': verlauf}, ensure_ascii=False)
    antwort = _G._api({'model': _G.MODELL, 'max_tokens': 6000, 'system': UEBERSETZEN, 'messages': [{'role': 'user', 'content': eingabe}]})
    roh = ''.join(b.get('text', '') for b in antwort.get('content', []) if b.get('type') == 'text').strip()
    roh = re.sub(r'^```(?:json)?\s*|\s*```$', '', roh)
    try:
        d = json.loads(roh[roh.index('{'):roh.rindex('}') + 1])
    except (ValueError, json.JSONDecodeError):
        raise ValueError('ÜBERSETZEN · Die Übersetzung kam unvollständig zurück. Bitte noch einmal versuchen.')
    with SCHLOSS:
        a = _lies(_pfad(id_), {})
        a['entwurf']['deutsch'] = {'betreff': str(d.get('betreff') or ''), 'text': str(d.get('text') or ''), 'quelle': q}
        vd = d.get('verlauf') if isinstance(d.get('verlauf'), list) else []
        a['verlauf_de'] = [str(x) for x in vd][:len(verlauf)] if len(vd) == len(verlauf) else a.get('verlauf_de') or []
        _schreib(_pfad(id_), a)
    return {'deutsch': a['entwurf']['deutsch'], 'verlauf_de': a['verlauf_de']}


def beispiele():
    """Beispiel-Anfragen mit fertigem Entwurf (gast_beispiele.json), damit das Haus sieht, wie der Eingang arbeitet (Robert 13.10.2026, erweitert 15.10.2026).
    Je Datenordner merkt sich beispiele.json den Stand. Ein neuer Stand legt nur die neu hinzugekommenen Beispiele an und schreibt die Entwürfe der
    noch vorhandenen neu; gelöschte Beispiele kommen nicht wieder. Liegt beim ersten Mal schon eine echte Anfrage da, bleibt der Eingang wie er ist.
    Namen und Adressen sind erfunden (example.com), in der Oberfläche steht «Beispiel» dabei."""
    marke = _pfad('beispiele.json')
    if _stand(marke) >= BEISPIEL_STAND:
        return 0
    with SCHLOSS:
        stand = _stand(marke)
        if stand >= BEISPIEL_STAND:
            return 0
        alt = _lies(marke, {}).get('anzahl', 0) if stand else 0
        da = {a.get('gespraech'): a for a in _alle('anfragen') if a.get('beispiel')}
        if not stand and any(not a.get('beispiel') for a in _alle('anfragen')):
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        liste = _lies(os.path.join(HIER, 'gast_beispiele.json'), [])
        jetzt = _jetzt(); n_neu = 0
        for n, b in enumerate(liste, 1):
            nr, absender = VORLAGE.get(b['art'], VORLAGE['nachricht'])
            absender = b.get('an') or absender
            g = f'beispiel-{n}'
            if g in da and stand >= 2:   # schon auf Stand 2: nur die deutsche Lesefassung dazu, Text, Gestaltung und Status bleiben
                a = da[g]; id_ = a.pop('id')
                if b.get('deutsch') and a.get('entwurf'):
                    a['entwurf']['deutsch'] = dict(b['deutsch'], quelle=_quelle(a['entwurf']))
                if b.get('verlauf_de'):
                    a['verlauf_de'] = b['verlauf_de']
                _schreib(_pfad(id_), a)
                continue
            if g in da:   # noch vorhanden: Entwurf und Angaben auf den neuen Stand, Status des Teams bleibt
                a = da[g]; id_ = a.pop('id')
                a.update({'name': b['name'], 'kontakt': b['kontakt'], 'datum': b['datum'], 'personen': b['personen'], 'anliegen': b['anliegen'],
                          'verlauf': [{'rolle': r, 'text': t} for r, t in b['verlauf']]})
                a['entwurf'] = {'betreff': b['betreff'], 'text': b['text'], 'team': b['team'], 'vorlage': nr, 'absender': absender, 'zeit': a.get('zeit')}
                if b.get('deutsch'):
                    a['entwurf']['deutsch'] = dict(b['deutsch'], quelle=_quelle(a['entwurf']))
                if b.get('verlauf_de'):
                    a['verlauf_de'] = b['verlauf_de']
                _schreib(_pfad(id_), a)
                continue
            if n <= alt:  # gab es schon und wurde gelöscht
                continue
            zeit = _zeit_vor(jetzt, b['vor'])
            _schreib(_pfad('anfragen', zeit[:10], f"{zeit[11:19].replace(':', '-')}_{g}.json"),
                     {'zeit': zeit, 'art': b['art'], 'name': b['name'], 'kontakt': b['kontakt'], 'datum': b['datum'], 'personen': b['personen'], 'anliegen': b['anliegen'],
                      'sprache': b['sprache'], 'gespraech': g, 'verlauf': [{'rolle': r, 'text': t} for r, t in b['verlauf']], 'status': b['status'], 'beispiel': True, **{k: b[k] for k in ('an', 'abteilung', 'seite', 'seite_name', 'web', 'nachricht', 'formular', 'allergene', 'uhrzeit', 'platz') if b.get(k)},
                      'entwurf': (dict({'betreff': b['betreff'], 'text': b['text'], 'team': b['team'], 'vorlage': nr, 'absender': absender, 'zeit': zeit},
                                       **({'deutsch': dict(b['deutsch'], quelle=_quelle(b))} if b.get('deutsch') else {})) if b.get('text') else None),   # Anfragen ohne Brief: den schreibt der Assistent auf Knopfdruck (Probe ohne KI: probe_ki.py)
                      **({'verlauf_de': b['verlauf_de']} if b.get('verlauf_de') else {})})
            n_neu += 1
        _schreib(marke, {'angelegt': jetzt.isoformat(timespec='seconds'), 'anzahl': len(liste), 'stand': BEISPIEL_STAND})
        return n_neu


def beispiel_fragen():
    """Beispiel-Fragen für «Das wurde gefragt» (gast_beispiel_fragen.json, Robert 14.10.2026: «Beispielfragen einsetzen in der Rezeption», erweitert 15.10.2026)
    und Beispiel-Antworten des Teams (gast_beispiel_nachgetragen.json). Stand wie bei beispiele(): ein neuer Stand legt nur Neues an.
    Die Antworten der Fragen stehen so im Wissen des Chats (Website und Unterlagen des Hauses); einige Fragen haben mit Absicht keine Antwort
    (Lücken zum Nachtragen). Die nachgetragenen Beispiele gehen nicht ins Wissen des Chats. In der Oberfläche steht «Beispiel» dabei."""
    marke = _pfad('beispiele_fragen.json')
    if _stand(marke) >= BEISPIEL_STAND:
        return 0
    with SCHLOSS:
        stand = _stand(marke)
        if stand >= BEISPIEL_STAND:
            return 0
        alt = _lies(marke, {}).get('anzahl', 0) if stand else 0
        jetzt = _jetzt()
        if not stand and glob.glob(_pfad('fragen', '*', '*.json')):
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        if stand and not alt:   # damals lag schon eine echte Frage da: auch jetzt keine Beispiele dazwischen
            _schreib(marke, {'angelegt': '', 'anzahl': 0, 'stand': BEISPIEL_STAND})
            return 0
        liste = _lies(os.path.join(HIER, 'gast_beispiel_fragen.json'), [])
        n_neu = 0
        for n, b in enumerate(liste, 1):
            if n <= alt:
                continue
            zeit = _zeit_vor(jetzt, b['vor'])
            _schreib(_pfad('fragen', zeit[:10], f"{zeit[11:19].replace(':', '-')}_beispiel-{n}.json"),
                     {'zeit': zeit, 'frage': b['frage'], 'antwort': b['antwort'], 'belegt': bool(b.get('belegt', True)), 'thema': b.get('thema', ''),
                      'gruppe': thema_von(b['frage']), 'sprache': b['sprache'], 'buchung': bool(b.get('buchung')), 'mappe': False, 'anfrage': '', 'beispiel': True})
            n_neu += 1
        ng = nachgetragen()
        if not any(str(x.get('nid', '')).startswith('beispiel-') for x in ng):
            for n, b in enumerate(_lies(os.path.join(HIER, 'gast_beispiel_nachgetragen.json'), []), 1):
                ng.append({'nid': f'beispiel-{n}', 'frage': b['frage'], 'antwort': b['antwort'], 'zeit': _zeit_vor(jetzt, b['vor']), 'quelle': '', 'beispiel': True})
            _schreib(_pfad('nachgetragen.json'), ng)
        _schreib(marke, {'angelegt': jetzt.isoformat(timespec='seconds'), 'anzahl': len(liste), 'stand': BEISPIEL_STAND})
        return n_neu


# ---------------------------------------------------------------- Nachgetragen vom Team
def nachgetragen():
    return _lies(_pfad('nachgetragen.json'), [])

def wissen_block():
    l = [x for x in nachgetragen() if (x.get('antwort') or '').strip() and not x.get('beispiel')]   # Beispiele sind erfunden, der Chat sagt sie nicht
    if not l:
        return ''
    return ('\n\nNACHGETRAGEN VOM TEAM (gilt wie WISSEN; das Team des Hauses hat diese Antworten selbst geschrieben, nachdem Gäste danach gefragt hatten):\n'
            + '\n'.join(f'Frage: {x["frage"]}\nAntwort des Hauses: {x["antwort"]}' for x in l))


# ---------------------------------------------------------------- Anbindung an _gast/gast.py
ZUSATZ = f"""

Anfragen an die Rezeption (Werkzeug anfrage):
- Möchte ein Gast ein Zimmer oder eine Ferienwohnung anfragen, einen Tisch im Röstihüs reservieren oder Esther und Fabian etwas schreiben, bietest du an, es an die Rezeption weiterzugeben. Dafür brauchst du den Namen und eine E-Mail-Adresse oder Telefonnummer; frag in einem Satz danach.
- Sobald Name und Kontakt genannt sind, rufst du das Werkzeug anfrage auf, mit allem, was der Gast gesagt hat (Anreise, Abreise, Gäste, Kinder mit Alter, Zimmerart, Halbpension, Hund, Wünsche). Ohne Kontakt rufst du es nicht auf.
- Deine Antwort dazu: ein Satz, dass die Anfrage jetzt bei der Rezeption liegt und Esther und Fabian sich persönlich melden. Sag nie, dass ein Zimmer oder Tisch reserviert, bestätigt oder frei ist.
- Zum Buchen allein ist «Zimmer buchen» auf der Website der schnellste Weg, für einen Tisch das Telefon ({TEL}) oder TheFork; die Anfrage im Chat ist ein Angebot zusätzlich, wenn der Gast Fragen oder Wünsche hat. Nenne nie ein Datum, einen Preis oder eine Zeit, der nicht in WISSEN steht; Preise der Ferienwohnungen und die Öffnungszeiten des Röstihüs stehen nicht drin.
- Allergien und Unverträglichkeiten: Die Website sagt dazu nichts. Nimm sie immer in die Anfrage auf und sag, dass die Küche des Röstihüs es mit dem Gast klärt. Ob ein Gericht frei davon ist, sagst du nie."""

WERKZEUG = {
    'name': 'anfrage',
    'description': 'Gibt eine Anfrage des Gastes an die Rezeption des Hotel Monte-Moro weiter (Zimmer, Ferienwohnung im Haus Apollo oder Arizona, Tisch im Röstihüs, Nachricht). Nur aufrufen, wenn Name und E-Mail oder Telefon genannt sind.',
    'strict': True,
    'input_schema': {'type': 'object', 'additionalProperties': False, 'required': ['art', 'name', 'kontakt', 'datum', 'personen', 'anliegen'],
                     'properties': {'art': {'type': 'string', 'enum': list(ARTEN)},
                                    'name': {'type': 'string', 'description': 'Name, wie der Gast ihn nennt'},
                                    'kontakt': {'type': 'string', 'description': 'E-Mail-Adresse oder Telefonnummer, wörtlich'},
                                    'datum': {'type': ['string', 'null'], 'description': 'Anreise und Abreise bzw. Tag des Tisches, wie der Gast sie nennt, oder null'},
                                    'personen': {'type': ['integer', 'null'], 'description': 'Anzahl Gäste (Erwachsene und Kinder zusammen) oder null'},
                                    'anliegen': {'type': 'string', 'description': 'Worum es geht, in ein bis drei Sätzen auf Deutsch, mit allen Wünschen des Gastes; Zimmerart, Kinder mit Alter, Hund und Allergien immer ausdrücklich'}}}}

DANKE = {'de': 'Herzlichen Dank. Ihre Anfrage liegt jetzt bei der Rezeption des Hotel Monte-Moro; Esther und Fabian melden sich persönlich bei Ihnen.',
         'en': 'Thank you very much. Your request is now with the reception of Hotel Monte-Moro; Esther and Fabian will get back to you personally.',
         'fr': 'Merci beaucoup. Votre demande est maintenant à la réception de l’Hotel Monte-Moro ; Esther et Fabian vous répondront personnellement.'}

ANFRAGE_GBR = f"""Du schreibst im Namen von Esther und Fabian Zurbriggen den Entwurf einer Antwort an einen Gast des Hotel Monte-Moro in Saas-Almagell (Wallis, Schweiz): ein Hotel mit 3 Sternen, 18 Zimmern und dem Restaurant Röstihüs, geführt von der Familie Zurbriggen. Satz des Hauses: «Mehr erleben, weniger zahlen.» Zimmer mit Frühstück oder Halbpension (4 Gänge, mit wöchentlichem Racletteabend im Stübli), Familienzimmer, Zimmer in der Residence Alpenhof, Ferienwohnungen im Haus Apollo und im Haus Arizona; inklusive Postautos im ganzen Saastal und im Sommer aller Bergbahnen ausser Metro Alpin; Kidsclub Mo - Sa 16:30 bis 21:00 Uhr; das Spa im Partnerhotel Pirmin Zurbriggen. Der Gast hat über das Anfrage-Fenster der Website oder im Chat geschrieben (Zimmer, Ferienwohnung, Tisch im Röstihüs, Nachricht).

Regeln:
- Grundlage ist, wo vorhanden, die VORLAGE: was das Haus selbst schreibt (Zimmer: Preise, Inklusive, Zuschläge, Kinder; Ferienwohnung: Haus Apollo und Haus Arizona; Tisch: das Röstihüs). Übernimm daraus den Inhalt und die Haltung, nicht Satz für Satz. Was für die Antwort fehlt (Anreise, Abreise, Erwachsene und Kinder mit Alter, Zimmerart, Frühstück oder Halbpension; beim Tisch Tag, Uhrzeit, Personen), erfragst du freundlich am Ende, in einer kurzen Liste. Gibt es keine Vorlage, gilt nur der Ton.
- Alles, was du an Preisen, Zeiten, Zimmern und Leistungen nennst, steht wörtlich in WISSEN. Erfinde nichts. Freie Zimmer und Tische kannst du nicht prüfen: setz dafür [Zimmer prüfen], [Wohnung prüfen] bzw. [Tisch prüfen]. Preise der Ferienwohnungen stehen nicht auf der Website: [Preis der Wohnung]. Öffnungszeiten des Röstihüs stehen nicht auf der Website: nenne keine. Storno- und Geschäftsbedingungen stehen nicht auf der Website: [Bedingungen]. Die Gratis-Anreise mit dem öffentlichen Verkehr ist abgelaufen: biete sie nie an. Was das Team entscheiden muss, steht in eckigen Klammern, kurz und in normaler Schreibung. Das Werkzeug zeigt diese Stellen als offene Felder im Brief.
- Allergien und Unverträglichkeiten: Nennt der Gast eine Allergie, nenne sie ausdrücklich und schreib, dass die Küche des Röstihüs es mit dem Gast abstimmt [Küche fragen]. Sag nie von dir aus, ein Gericht sei frei davon.
- Ton der Website: Sie, herzlich, ruhig und persönlich, wie Gastgeber in den Bergen schreiben. Jeder Satz macht den Aufenthalt wertvoller: der einzelne Gast, die Familie, die Sonne über dem Saastal, das Röstihüs, der Wein, den Fabian selbst kreiert hat. Nie Masse, nie Abfertigung, keine Stückzahlen als Pointe. Keine Werbesprache (nicht «Highlight», «Genuss pur», «unvergesslich»), keine Emojis, kein Fettdruck. Kurze Absätze. Schweizer Schreibung: ss statt ß, «Guillemets», Preise wie die Website (CHF 90.00, im Röstihüs Fr. 25.–).
- Anrede «Guten Tag [Vorname Nachname],» bzw. in der Sprache des Gastes, Gruss «Herzliche Grüsse aus Saas-Almagell».
- Sprache: die Sprache des Gastes (steht bei der Anfrage).
- Form: Zeile 1 «Betreff: …» (persönlich, mit Zeitraum oder Anlass), dann Leerzeile, dann die Antwort mit Anrede und Gruss, darunter zwei Zeilen: «Esther und Fabian Zurbriggen» und «Hotel Monte-Moro». Adresse, Telefon und E-Mail stehen schon im Briefkopf, nicht wiederholen.
- Nach der Antwort eine Zeile «---» und darunter für das Team, nicht für den Gast: «Grundlage:» mit den Seiten, aus denen die Angaben stammen, und «Offen:» mit dem, was das Team vor dem Senden klären muss.

WISSEN:
"""

_G = None

def einbinden(g):
    """Hängt La Réception an das geladene Modul _gast/gast.py: Werkzeug «anfrage», Wissen des Teams, Ablage statt Online-Speicher."""
    global _G
    _G = g
    os.makedirs(DATEN, exist_ok=True)
    g.WERKZEUGE = [w for w in g.WERKZEUGE if w.get('name') != 'anfrage'] + [WERKZEUG]
    if gedaechtnis:
        gedaechtnis._G = g
    basis = g.ANWEISUNG
    g.ANFRAGE = ANFRAGE_GBR + g.WISSEN
    roh_api, roh_frage, roh_ip = g._api, g.frage, g.handler._ip

    def api(koerper):
        a = roh_api(koerper)
        for b in a.get('content', []):
            if b.get('type') == 'tool_use' and b.get('name') == 'anfrage':
                LOKAL.anfrage = b.get('input') or {}
        return a

    def ip(self):
        LOKAL.ip = roh_ip(self)
        # «Chat ausprobieren» in La Réception lädt die Website mit ?probe=1: Fragen und Anfragen daraus gelten als Beispiel (Robert 16.10.2026)
        LOKAL.probe = 'probe=1' in (self.headers.get('referer') or self.headers.get('Referer') or '') or self.headers.get('X-Reception-Probe') == '1'
        return LOKAL.ip

    def frage(messages, mappe=False, heute='', sprache='de'):
        LOKAL.anfrage = None
        g.ANWEISUNG = (gedaechtnis.anweisung(basis) if gedaechtnis else basis) + ZUSATZ + wissen_block()   # vom Team Berichtigtes, Ergänztes und Nachgetragenes gilt ab der nächsten Frage
        a = roh_frage(messages, mappe=mappe, heute=heute, sprache=sprache)
        e = getattr(LOKAL, 'anfrage', None)
        LOKAL.anfrage = None
        if e and (e.get('kontakt') or '').strip():
            erste = next((str(m.get('content', '')) for m in messages if m.get('role') == 'user'), '')
            gespraech = hashlib.sha1((getattr(LOKAL, 'ip', '') + '|' + erste[:300]).encode('utf-8')).hexdigest()[:16]
            sp = sprache if sprache in SPRACHEN else 'de'
            if re.search(r"\b(the|is|are|could|would|we|our|table|room|please)\b", (messages[-1].get('content') or '').lower()) and sp == 'de':
                sp = 'en'
            if a.get('text') in g.NICHTS.values() or not a.get('text'):   # Text endete am Werkzeug: kurzer Dank statt «dazu kann ich nichts sagen»
                a['text'] = DANKE.get(sp, DANKE['en'])
            verlauf = [{'rolle': m.get('role'), 'text': str(m.get('content', ''))[:600]} for m in messages[-8:]] + [{'rolle': 'assistant', 'text': a.get('text', '')[:1200]}]
            LOKAL.letzte = lege_anfrage(e, gespraech, sp, verlauf)
            if getattr(LOKAL, 'probe', False) and LOKAL.letzte:
                with SCHLOSS:
                    x = _lies(_pfad(LOKAL.letzte), {})
                    if x:
                        x['beispiel'] = True; x['probe'] = True; _schreib(_pfad(LOKAL.letzte), x)
        return a

    def merke(host, daten):
        if getattr(LOKAL, 'probe', False):   # Tor 3 G1 (30.10.2026): Proben des Teams («Chat ausprobieren», ?probe=1) kommen nicht unter die Gästefragen
            return
        try:
            lege_frage(dict(daten, anfrage=getattr(LOKAL, 'letzte', None) or '', beispiel=bool(getattr(LOKAL, 'probe', False))))
        except Exception:  # noqa: BLE001  die Antwort an den Gast bleibt davon unberührt
            pass

    roh_erlaubt = g.erlaubt
    PROBEN = {'tag': '', 'n': 0}

    def erlaubt(ip_, art='gast'):
        """Proben des Teams («Chat ausprobieren», Prüfläufe) zählen nicht gegen die Grenzen der Gäste, haben aber eine eigene: 400 am Tag (Carlton 17.10.2026)."""
        if getattr(LOKAL, 'probe', False) and art == 'gast':
            heute = time.strftime('%Y-%m-%d')
            with SCHLOSS:
                if PROBEN['tag'] != heute:
                    PROBEN.update(tag=heute, n=0)
                PROBEN['n'] += 1
                return PROBEN['n'] <= 400
        return roh_erlaubt(ip_, art)

    g._api, g.frage, g.merke, g.handler._ip, g.erlaubt = api, frage, merke, ip, erlaubt
    # Die Frage im Protokoll soll wissen, ob daraus eine Anfrage wurde: do_POST ruft frage(), dann merke(); dazwischen merkt sich LOKAL.letzte die Kennung.
    roh_post = g.handler.do_POST

    def do_post(self):
        LOKAL.letzte = None; LOKAL.probe = False
        return roh_post(self)
    g.handler.do_POST = do_post
    return g


# ---------------------------------------------------------------- Entwurf
def vorlage_text(art, sprache):
    """Die Fragen des Hauses aus seinem eigenen Mail-Link (vorlagen/<nr>.txt, Deutsch); ohne Vorlage leer. Der Assistent schreibt in der Sprache des Gastes."""
    nr, absender = VORLAGE.get(art, VORLAGE['nachricht'])
    if not nr:
        return '', absender, 'de', ''
    try:
        t = open(os.path.join(HIER, 'vorlagen', nr + '.txt'), encoding='utf-8').read().strip()
    except OSError:
        return nr, absender, 'de', ''
    return nr, absender, 'de', t


def _daten_aus(text):
    """Alle Daten aus den Angaben («Fr, 20. November 2026 bis So, 22. November 2026», «20.11.2026 – 22.11.2026», «2026-11-20»), in der Reihenfolge."""
    t = str(text or '')
    mon = {m: i for i, m in enumerate(('januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember'), 1)}
    l = []
    for m in re.finditer(r'(\d{4})-(\d{2})-(\d{2})|(\d{1,2})\.(\d{1,2})\.(\d{4})|(\d{1,2})\.\s*([A-Za-zÄÖÜäöü]+)\s+(\d{4})', t):
        try:
            if m[1]:
                l.append(datetime.date(int(m[1]), int(m[2]), int(m[3])))
            elif m[4]:
                l.append(datetime.date(int(m[6]), int(m[5]), int(m[4])))
            elif m[8].lower() in mon:
                l.append(datetime.date(int(m[9]), mon[m[8].lower()], int(m[7])))
        except ValueError:
            continue
    return l


def _datum_aus(text):
    l = _daten_aus(text)
    return l[0] if l else None


def _chf(w):
    return w if '%' in w else 'CHF ' + w


def hinweise(a):
    """Hinweise fürs Team zu einer Anfrage, nur aus Angaben des Hauses gerechnet (website/inhalt/daten.py; nicht gespeichert, bei jedem Lesen neu):
    Einzelzimmerzuschlag bei einer Person, Zuschlag für 1 bis 3 Übernachtungen, Kinder im Zimmer der Eltern (Zuschläge nach Alter, Kidsclub), Hund,
    Familienzimmer bis 6 Personen, Preise der Ferienwohnungen und Öffnungszeiten des Röstihüs nicht veröffentlicht, Allergien (Küche fragen),
    Gratis-Anreise abgelaufen."""
    h = []
    art = a.get('art')
    zu = dict(D.ZUSCHLAEGE) if D else {}
    try:
        p = int(a.get('personen') or 0)
    except (TypeError, ValueError):
        p = 0
    text = ' '.join(str(a.get(k) or '') for k in ('anliegen', 'nachricht', 'datum'))
    text = re.sub(r'(?:Ihre Nachricht|Betreff|Tag|Uhrzeit|Personen)\s*:', ' ', text)   # Feldnamen des Anfrage-Fensters zählen nicht, nur was der Gast schreibt
    if art in ('zimmer', 'wohnung'):
        ds = _daten_aus(a.get('datum'))
        naechte = (ds[1] - ds[0]).days if len(ds) >= 2 and ds[1] > ds[0] else 0
        m = re.search(r'(\d{1,2})\s*(?:nächte|nacht|übernachtung|nights?)', text, re.I)
        naechte = naechte or (int(m.group(1)) if m else 0)
        if art == 'zimmer' and p == 1:
            h.append({'art': 'einzel', 'text': 'Eine Person: Einzelzimmerzuschlag ' + _chf(zu.get('Einzelzimmerzuschlag', '50 %'))})
        if art == 'zimmer' and 1 <= naechte <= 3:
            h.append({'art': 'kurz', 'text': f'{naechte} {"Nacht" if naechte == 1 else "Nächte"}: Zuschlag für 1 - 3 Übernachtungen ' + _chf(zu.get('Zuschlag für 1 - 3 Übernachtungen / pro Tag', '5.00')) + ' pro Tag'})
        if p > FAMILIE_BIS:
            h.append({'art': 'gruppe', 'text': f'{p} Gäste: Familienzimmer sind ideal für 3 bis {FAMILIE_BIS} Personen; mehrere Zimmer oder Wohnungen klären'})
        if re.search(r'kind|kinder|tochter|sohn|baby|jahre alt|\bj\.\b|child|kids', text, re.I):
            k = ' · '.join(f'{x} {_chf(y)}' for x, y in (D.KINDER if D else []))
            h.append({'art': 'kinder', 'text': 'Mit Kindern: im Zimmer der Eltern pro Kind und Tag mit Halbpension ' + k + '; Kidsclub Mo - Sa 16:30 bis 21:00 Uhr inklusive'})
        if art == 'wohnung':
            h.append({'art': 'preis', 'text': 'Preise der Ferienwohnungen stehen nicht auf der Website: persönlich nennen'})
    if re.search(r'\bhund|hündin|\bdog\b|\bchien', text, re.I):
        h.append({'art': 'hund', 'text': 'Mit Hund: ' + _chf(zu.get('Hund pro Tag ohne Futter', '7.00 - 10.00')) + ' pro Tag ohne Futter'})
    if art == 'tisch':
        d = _datum_aus(a.get('datum'))
        h.append({'art': 'oeffnung', 'text': (f'{TAG_NAME[d.weekday()]}: ' if d else '') + 'Öffnungszeiten des Röstihüs sind nicht veröffentlicht, Tisch an der Rezeption prüfen'})
    al = [ALLERGENE.get(x, x) for x in (a.get('allergene') or []) if isinstance(x, str)]
    frei = re.findall(r'allerg\w*|unverträglich\w*|verträgt keine?\b|zöliak\w*|gluten\w*|laktose\w*|nuss\w*|nüsse|vegetar\w*|vegan\w*', text, re.I)
    if al:
        h.append({'art': 'allergie', 'text': 'Allergien und Wünsche: ' + ', '.join(al) + ' (Küche des Röstihüs fragen)'})
    elif frei:
        h.append({'art': 'allergie', 'text': 'Allergie oder Wunsch zum Essen im Text: die Website sagt dazu nichts, die Küche des Röstihüs fragen'})
    if re.search(r'gratis|geschenkt|kostenlos', text, re.I) and re.search(r'anreis|abreis|zug|bahn|öv|öffentlich', text, re.I) and D and datetime.date.today().isoformat() > D.ANREISE_GRATIS['bis']:
        h.append({'art': 'gratis', 'text': 'Gratis-Anreise mit dem öffentlichen Verkehr galt bis 31.10.2026: nicht mehr anbieten'})
    return h

def entwurf(id_, hinweis=''):
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    if _G is None:
        raise ValueError('CHAT · Der Assistent ist noch nicht geladen. Einmal eine Frage im Chat stellen oder server.py neu starten.')
    a = _lies(_pfad(id_), {})
    nr, absender, sp_v, vorlage = vorlage_text(a.get('art'), a.get('sprache', 'de'))
    absender = KONTAKT   # der Brief nennt die Wege des Hauses: Telefon und E-Mail der Rezeption
    gast = '\n'.join(f"{'Gast' if v.get('rolle') == 'user' else 'Chat des Hauses'}: {v.get('text', '')}" for v in a.get('verlauf') or [])
    mail = (f"Art: {ARTEN.get(a.get('art'), a.get('art'))}\nAbteilung: {a.get('abteilung') or ART_ABTEILUNG.get(a.get('art'), 'Nachrichten')}\nName: {a.get('name')}\nKontakt: {a.get('kontakt')}\nDatum: {a.get('datum') or 'nicht genannt'}\n"
            f"Personen: {a.get('personen') or 'nicht genannt'}\nAnliegen: {a.get('anliegen')}\nSprache des Gastes: {a.get('sprache')}\n\nGESPRÄCH IM CHAT:\n{gast}\n\n"
            f"Allergien (Formular): {', '.join(ALLERGENE.get(x, x) for x in a.get('allergene') or []) or 'keine angegeben'}\nHinweise: {'; '.join(x['text'] for x in hinweise(a)) or 'keine'}\n\n"
            f"VORLAGE DES HAUSES ({nr or 'keine'}, Sprache {sp_v}):\n{vorlage or '(keine: nur der Ton des Hauses)'}")
    _G.ANFRAGE = ANFRAGE_GBR + (gedaechtnis.wissen_text(_G.WISSEN) if gedaechtnis else _G.WISSEN) + wissen_block()   # derselbe Stand wie im Chat
    r = _G.anfrage(mail, hinweis)
    if r.get('fehler'):
        raise ValueError('ENTWURF · ' + r['fehler'])
    entwurf_neu = {'betreff': r.get('betreff', ''), 'text': r.get('text', ''), 'team': r.get('team', ''), 'vorlage': nr, 'absender': absender,
                   'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds')}
    with SCHLOSS:
        # frisch lesen: während der Assistent schrieb (Sekunden), kann das Team die Anfrage geändert haben (Status, Notiz, Betreff);
        # vorher überschrieb der alte Stand von oben diese Änderungen (17.10.2026)
        a = _lies(_pfad(id_), a)
        entwurf_neu['fassung'] = ((a.get('entwurf') or {}).get('fassung', 0) or 0) + 1
        a['entwurf'] = entwurf_neu
        if a.get('status') == 'neu':
            a['status'] = 'gelesen'
        _schreib(_pfad(id_), a)
    return a['entwurf']


# ---------------------------------------------------------------- Schnittstelle für La Réception (/reception/api/<was>)
def ueberblick():
    an = _alle('anfragen'); fr = _alle('fragen'); ng = nachgetragen()
    erledigt = set(_lies(_pfad('status.json'), {}).get('fragen_erledigt', []))
    luecken = [f for f in fr if not f.get('belegt') and f['id'] not in erledigt]
    return {'anfragen_neu': sum(1 for a in an if a.get('status') == 'neu'), 'anfragen_offen': sum(1 for a in an if a.get('status') != 'erledigt'),
            'anfragen_gesamt': len(an), 'fragen_gesamt': len(fr), 'ohne_antwort': len(luecken), 'nachgetragen_gesamt': len(ng),
            'letzte_frage': fr[0]['zeit'] if fr else '', 'speicher': os.path.relpath(DATEN, WEB)}

# ---------------------------------------------------------------- Anfrage-Fenster der Website (08.11.2026)
# Das Anfrage-Fenster der Website (website/assets/js/anfrage.js) schickt «Anfrage senden» als POST /api/anfragen. Auf dem Server der Rezeption landet
# das gleich im Eingang (server.py → website_anfrage). Auf dem Vorschau-Server der Website (website/serve.py, Port 8947) legt es die Anfrage in
# website/_dienste/anfragen.jsonl ab; die Rezeption holt sie dort ab (nur lesen, an der Website wird nichts geschrieben) und merkt sich in status.json,
# welche Zeilen sie schon übernommen hat, damit jede Anfrage genau einmal in den Eingang kommt. RECEPTION_ONLINE=aus schaltet das Abholen ab
# (Prüfläufe mit Wegwerf-Daten holen nur mit ausdrücklichem RECEPTION_ONLINE ab, sonst nähmen sie echte Anfragen in ihre Wegwerf-Daten mit).
ONLINE_API = os.environ.get('RECEPTION_ONLINE') or ('aus' if os.environ.get('RECEPTION_DATEN') else os.path.join(WEB, '_dienste', 'anfragen.jsonl'))
ONLINE_STAND = {'zeit': '', 'neu': 0, 'fehler': ''}
_ONLINE_SCHLOSS = threading.Lock()
SEITEN_NAME = {'/': 'Startseite', '/index.html': 'Startseite', '/zimmer.html': 'Zimmer', '/preise.html': 'Preise', '/roestihues.html': 'Röstihüs', '/spa.html': 'Spa',
               '/saastal.html': 'Saastal', '/anreise.html': 'Anreise', '/impressum.html': 'Impressum', '/datenschutz.html': 'Datenschutz'}


def website_anfrage(d):
    """Eine Anfrage im Format des Anfrage-Fensters der Website (assets/js/anfrage.js: betreff, art, tag, zeit, personen, nachricht, name, kontakt,
    seite, zeitpunkt) in die Felder des Eingangs übersetzen und ablegen. Die Art kommt aus dem Betreff, den die Website setzt (data-anfrage)."""
    b = re.sub(r'\s+', ' ', str(d.get('betreff') or '')).strip()[:120]
    art = ('tisch' if d.get('art') == 'tisch' or 'Tisch' in b else 'wohnung' if re.search(r'Apollo|Arizona|Ferienwohnung', b)
           else 'zimmer' if re.search(r'zimmer', b, re.I) else 'nachricht')
    tag, zeit = str(d.get('tag') or '')[:10], str(d.get('zeit') or '')[:5]
    datum = ''
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', tag):
        t = datetime.date.fromisoformat(tag)
        datum = f"{TAG_NAME[t.weekday()][:2]}, {t.day}. {('Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember')[t.month - 1]} {t.year}"
    text = str(d.get('nachricht') or '').strip()[:4000]
    zeilen = [f'Betreff: {b or "Ihre Anfrage"}'] + ([f'Tag: {datum}'] if datum else []) + ([f'Uhrzeit: {zeit} Uhr'] if zeit else []) \
        + ([f"Personen: {d.get('personen')}"] if str(d.get('personen') or '').strip() else []) + [f'Ihre Nachricht: {text}' if text else 'Ihre Nachricht: –']
    seite = str(d.get('seite') or '')[:160]
    return post('formular', {'art': art, 'name': d.get('name'), 'kontakt': d.get('kontakt'), 'datum': datum, 'uhrzeit': f'{zeit} Uhr' if zeit else '',
                             'personen': d.get('personen') or None, 'anliegen': (b + (': ' + text if text else ''))[:300], 'nachricht': '\n'.join(zeilen),
                             'seite': seite, 'seite_name': SEITEN_NAME.get(seite.split('#')[0].split('?')[0], ''), 'formular': 'tisch' if art == 'tisch' else 'zimmer' if art in ('zimmer', 'wohnung') else 'allgemein',
                             'website': d.get('website') or '', 'probe': d.get('probe') is True, 'online_id': d.get('online_id') or '', 'zeit': d.get('zeitpunkt') or ''})


def online_abholen():
    """Holt die Anfragen ab, die das Anfrage-Fenster auf dem Vorschau-Server der Website abgelegt hat (website/_dienste/anfragen.jsonl, nur lesen);
    jede Zeile kommt genau einmal in den Eingang (Kennung aus dem Inhalt, gemerkt in status.json)."""
    if ONLINE_API == 'aus' or not _ONLINE_SCHLOSS.acquire(blocking=False):
        return 0
    try:
        if not os.path.exists(ONLINE_API):
            ONLINE_STAND.update(zeit=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), neu=0, fehler='')
            return 0
        schon = set(_lies(_pfad('status.json'), {}).get('website_zeilen', []))
        neu = 0
        for z in open(ONLINE_API, encoding='utf-8').read().splitlines():
            if not z.strip():
                continue
            oid = 'website/' + hashlib.sha1(z.encode('utf-8')).hexdigest()[:16]
            if oid in schon:
                continue
            try:
                website_anfrage({**json.loads(z), 'online_id': oid})
            except (ValueError, TypeError) as e:   # nimmt die Rezeption nicht an (kein Kontakt): Zeile bleibt liegen, Stand zeigt es
                ONLINE_STAND['fehler'] = f'{oid}: {e}'
            else:
                neu += 1
            schon.add(oid)
            with SCHLOSS:
                s = _lies(_pfad('status.json'), {}); s['website_zeilen'] = sorted(schon)[-5000:]; _schreib(_pfad('status.json'), s)
        ONLINE_STAND.update(zeit=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), neu=neu)
        return neu
    except Exception as e:  # noqa: BLE001 (Datei besetzt, beschädigt): beim nächsten Mal wieder
        ONLINE_STAND['fehler'] = type(e).__name__ + ': ' + str(e)[:160]
        return 0
    finally:
        _ONLINE_SCHLOSS.release()


def get(was, q=None):
    if was.startswith('wissen') and gedaechtnis:
        return {**gedaechtnis.get(was, q), 'nachgetragen': nachgetragen()} if was == 'wissen' else gedaechtnis.get(was, q)
    beispiele(); beispiel_fragen()
    if was == 'ueberblick':
        return ueberblick()
    if was == 'anfragen':
        an = _alle('anfragen')
        for a in an:
            a['hinweise'] = hinweise(a)
            a['allergene_lang'] = [ALLERGENE.get(x, x) for x in a.get('allergene') or [] if isinstance(x, str)]
        return {'anfragen': an, **ueberblick()}
    if was == 'fragen':
        erledigt = set(_lies(_pfad('status.json'), {}).get('fragen_erledigt', []))
        fr = _alle('fragen')
        for f in fr:
            f['erledigt'] = f['id'] in erledigt
            f['gruppe'] = thema_von(f.get('frage'))
        return {'fragen': fr, 'nachgetragen': nachgetragen(), **ueberblick()}
    if was == 'vorlage':
        nr, absender, sp, t = vorlage_text((q or {}).get('art', ['nachricht'])[0], (q or {}).get('sprache', ['de'])[0])
        return {'vorlage': nr, 'absender': absender, 'sprache': sp, 'text': t}
    raise ValueError('ANFRAGE · Unbekannte Ansicht.')

def brief_pdf(id_, port):
    """Der Brief einer Anfrage als A4-PDF: Chromium setzt brief-pdf.html (brief_pdf.js, Playwright wie in La Carte). Gibt (Bytes, Dateiname) zurück."""
    import subprocess, tempfile
    if not _gueltig(id_, 'anfragen'):
        raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
    a = _lies(_pfad(id_), {}); e = a.get('entwurf') or {}
    if not e.get('text'):
        raise ValueError('BRIEF · Zu dieser Anfrage gibt es noch keinen Brief.')
    daten = {'name': a.get('name') or '', 'kontakt': a.get('kontakt') or '', 'absender': e.get('absender') or KONTAKT,
             'betreff': e.get('betreff') or '', 'text': e.get('text') or '', 'gestalt': e.get('gestalt') or {}}
    node = shutil.which('node') or next((x for x in ('/opt/homebrew/bin/node', '/usr/local/bin/node') if os.path.exists(x)), None)
    if not node:
        raise ValueError('PDF · node ist nicht installiert (wird für das PDF gebraucht).')
    with tempfile.TemporaryDirectory() as t:
        quelle, ziel = os.path.join(t, 'brief.json'), os.path.join(t, 'brief.pdf')
        with open(quelle, 'w', encoding='utf-8') as f:
            json.dump(daten, f, ensure_ascii=False)
        try:
            r = subprocess.run([node, os.path.join(HIER, 'brief_pdf.js'), str(port), quelle, ziel], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise ValueError('PDF · Das PDF liess sich nicht setzen (Zeitüberschreitung).')
        if r.returncode != 0 or not os.path.exists(ziel):
            raise ValueError('PDF · Das PDF liess sich nicht setzen. Ist Playwright installiert? ' + (r.stderr or '')[-160:])
        roh = open(ziel, 'rb').read()
    wer = re.sub(r'[\\/:*?"<>|\n\r]+', ' ', a.get('name') or 'Gast').strip()[:60] or 'Gast'
    return roh, f'Hotel Monte-Moro – {wer} – {datetime.date.today().strftime("%d.%m.%Y")}.pdf'


def post(was, d):
    if was.startswith('wissen') and gedaechtnis:
        return gedaechtnis.post(was, d)
    beispiele(); beispiel_fragen()
    if was == 'uebersetzen':
        return {**uebersetzen(d.get('id')), **ueberblick()}
    if was == 'entwurf':
        return {'entwurf': entwurf(d.get('id'), str(d.get('hinweis') or '')[:2000]), **ueberblick()}
    if was == 'anfrage':            # Status, Notiz oder geänderter Entwurf des Teams
        id_ = d.get('id')
        if not _gueltig(id_, 'anfragen'):
            raise ValueError('ANFRAGE · Diese Anfrage gibt es nicht mehr.')
        with SCHLOSS:
            a = _lies(_pfad(id_), {})
            aendert = a.get('entwurf') and (isinstance(d.get('entwurf_text'), str) or isinstance(d.get('gestalt'), dict))
            if aendert and isinstance(d.get('fassung'), int) and d['fassung'] != a['entwurf'].get('fassung', 0):
                raise ValueError('KONFLIKT · Dieser Brief wurde inzwischen in einem anderen Fenster geändert. Ihre Eingabe ist noch hier; bitte kopieren, neu laden und wieder einsetzen.')
            if aendert:
                a['entwurf']['fassung'] = a['entwurf'].get('fassung', 0) + 1
            if d.get('status') in ('neu', 'gelesen', 'erledigt'):
                a['status'] = d['status']
            if isinstance(d.get('entwurf_text'), str) and a.get('entwurf'):
                if 'original' not in a['entwurf']:
                    a['entwurf']['original'] = {'text': a['entwurf'].get('text') or '', 'betreff': a['entwurf'].get('betreff') or ''}
                a['entwurf']['text'] = d['entwurf_text'][:12000]
                if isinstance(d.get('betreff'), str):
                    a['entwurf']['betreff'] = d['betreff'][:300]
                a['entwurf']['geaendert'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            if isinstance(d.get('gestalt'), dict) and a.get('entwurf') and len(json.dumps(d['gestalt'])) < 20000:   # Anordnung des Briefs (verschoben, Grösse, Bündigkeit, Kopftexte)
                a['entwurf']['gestalt'] = d['gestalt']
            _schreib(_pfad(id_), a)
        return {'ok': True, 'fassung': (a.get('entwurf') or {}).get('fassung', 0), **ueberblick()}
    if was == 'formular':           # Anfrage-Fenster der Website (assets/js/anfrage.js über website_anfrage): landet im Eingang, nicht in einem Mailfach (Rivage E12, Schlössli, Schäfli, Monte-Moro 08.11.2026)
        if d.get('website'):        # Feld, das Menschen nicht sehen: nur Maschinen füllen es aus
            return {'ok': True}
        name, kontakt = str(d.get('name') or '').strip()[:120], str(d.get('kontakt') or '').strip()[:160]
        if not kontakt:
            raise ValueError('FORMULAR · Bitte E-Mail oder Telefon angeben, damit das Haus antworten kann.')
        if not re.fullmatch(r'[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]{2,}|\+?[\d\s/().-]{7,24}', kontakt):
            raise ValueError('FORMULAR · Bitte eine gültige E-Mail-Adresse oder Telefonnummer angeben.')
        art = d.get('art') if d.get('art') in ARTEN else 'nachricht'
        sp = d.get('sprache') if d.get('sprache') in SPRACHEN else 'de'
        try:
            pers = max(1, min(200, int(d.get('personen'))))   # das Anfrage-Fenster nimmt 1 bis 40 Personen (anfrage.js)
        except (TypeError, ValueError):
            pers = None
        anliegen = str(d.get('anliegen') or '').strip()[:300]
        nachricht = str(d.get('nachricht') or '').strip()[:6000]   # Angaben des Formulars + Nachricht des Gastes (bis 1'200) + Wünsche ohne Grenze: 1'200 schnitt still ab (Prüfung 17.10.2026); die Anfrage selbst bleibt unter 12 kB
        an = KONTAKT
        allergene = [x for x in (d.get('allergene') or []) if x in ALLERGENE][:len(ALLERGENE)] if isinstance(d.get('allergene'), list) else []
        seite = str(d.get('seite') or '')[:160]
        seite = re.sub(r'[^\w./?#=&%-]', '', seite) if seite.startswith('/') else ''   # Weg der Seite (mit ? und #), nur harmlose Zeichen
        seite_name = re.sub(r'[<>]', '', str(d.get('seite_name') or ''))[:80]
        formular = d.get('formular') if d.get('formular') in FORMULARE else 'allgemein'
        text = nachricht or anliegen
        id_ = lege_anfrage({'art': art, 'name': name, 'kontakt': kontakt, 'datum': str(d.get('datum') or '')[:120], 'personen': pers, 'anliegen': anliegen or text[:200]},
                           'formular-' + hashlib.sha1(f'{time.time()}{random.random()}'.encode()).hexdigest()[:12], sp,
                           [{'rolle': 'user', 'text': f'Über ein Formular der Website (Seite {seite_name or seite or "unbekannt"}): ' + text}])
        with SCHLOSS:
            x = _lies(_pfad(id_), {})
            x.update({'web': True, 'an': an, 'abteilung': ART_ABTEILUNG.get(art, 'Nachrichten'), 'seite': seite, 'seite_name': seite_name, 'formular': formular,
                      'nachricht': nachricht, 'allergene': allergene, 'uhrzeit': str(d.get('uhrzeit') or '')[:20], 'platz': str(d.get('platz') or '')[:60], 'hund': d.get('hund') is True})
            if d.get('probe') is True:
                x['probe'] = True
            if d.get('online_id'):   # vom Vorschau-Server der Website abgeholt (online_abholen): Zeit des Gastes und Kennung der Zeile
                x['online_id'] = str(d['online_id'])[:120]
                try:
                    x['zeit'] = datetime.datetime.fromisoformat(str(d.get('zeit'))).astimezone().isoformat(timespec='seconds')
                except ValueError:
                    pass
            _schreib(_pfad(id_), x)
        return {'ok': True, 'danke': DANKE.get(sp, DANKE['de'])}
    if was == 'weg':                # Anfrage oder Frage löschen (Wunsch des Gastes, Test)
        id_ = d.get('id', '')
        art = id_.split('/')[0]
        if art not in ('anfragen', 'fragen') or not _gueltig(id_, art):
            raise ValueError('ANFRAGE · Dieser Eintrag existiert nicht.')
        with SCHLOSS:
            os.remove(_pfad(id_))
            for rest in ('.gut', '.neu'):
                try:
                    os.remove(_pfad(id_) + rest)
                except OSError:
                    pass
        return {'ok': True, **ueberblick()}
    if was == 'frage':              # Frage erledigt / wieder offen
        id_ = d.get('id')
        if not _gueltig(id_, 'fragen'):
            raise ValueError('FRAGE · Diese Frage gibt es nicht mehr.')
        with SCHLOSS:
            s = _lies(_pfad('status.json'), {}); l = [x for x in s.get('fragen_erledigt', []) if x != id_]
            if d.get('erledigt'):
                l.append(id_)
            s['fragen_erledigt'] = l[-5000:]
            _schreib(_pfad('status.json'), s)
        return {'ok': True, **ueberblick()}
    if was == 'nachtragen':         # Antwort des Teams auf eine Frage ohne Antwort
        frage_ = str(d.get('frage') or '').strip()[:400]; antwort = str(d.get('antwort') or '').strip()[:2000]
        if len(frage_) < 3 or len(antwort) < 3:
            raise ValueError('EINGABE · Bitte Frage und Antwort ausfüllen.')
        with SCHLOSS:
            l = nachgetragen()
            nid = d.get('nid') or ('n' + str(int(time.time() * 1000)))
            alt = next((x for x in l if x.get('nid') == nid), None)
            eintrag = {'nid': nid, 'frage': frage_, 'antwort': antwort, 'zeit': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                       'quelle': d.get('quelle') or (alt or {}).get('quelle') or ''}
            l = [x for x in l if x.get('nid') != nid] + [eintrag]
            _schreib(_pfad('nachgetragen.json'), l)
            if d.get('quelle') and _gueltig(d['quelle'], 'fragen'):
                s = _lies(_pfad('status.json'), {}); fe = set(s.get('fragen_erledigt', [])); fe.add(d['quelle'])
                s['fragen_erledigt'] = sorted(fe)[-5000:]; _schreib(_pfad('status.json'), s)
        return {'ok': True, 'eintrag': eintrag, **ueberblick()}
    if was == 'nachtragen_weg':
        with SCHLOSS:
            _schreib(_pfad('nachgetragen.json'), [x for x in nachgetragen() if x.get('nid') != d.get('nid')])
        return {'ok': True, **ueberblick()}
    raise ValueError('ANFRAGE · Unbekannter Auftrag.')
