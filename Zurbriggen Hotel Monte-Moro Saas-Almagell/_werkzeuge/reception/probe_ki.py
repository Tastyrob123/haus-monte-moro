"""Probe-Antworten statt Claude (Robert 16.10.2026: «lokal bis zur Kostenrunde», keine bezahlten KI-Aufrufe in Prüfläufen).

In der Rezeption des Hotel Monte-Moro ist das der Standard: python3 _werkzeuge/reception/server.py 9384 (ohne RECEPTION_KI=1).
Kopie aus dem Culinarium über Wild Side (08.11.2026), Inhalt des Hauses: Zimmer, Ferienwohnungen, Tisch im Röstihüs, Sie-Form, Schweizer Schreibung.
Dann ruft kein Teil der Rezeption und vom Chat die KI auf und kein Schlüssel wird gelesen. Jede Stelle, die sonst Claude fragt, bekommt
eine Antwort in genau der Form, die Claude liefern würde:
  Chat (gast.frage)        dieselbe Antwort wie die Rezeption im Chat der Website (gast/website_chat.py über assets/js/wissen.json); nennt der Gast
                           eine E-Mail oder Telefonnummer, ruft die Probe das Werkzeug «anfrage» auf (so entsteht wie echt eine Anfrage im Eingang);
                           ohne Antwort meldet sie «nicht belegt» (Lücke fürs Team), ehrlich und ohne Zahl.
  Brief (gast.anfrage)     «Betreff: …», Brief mit Anrede, offenen Stellen [in Klammern] und Gruss von Esther und Fabian, darunter «---» mit Punkten fürs Team.
                           Preise aus website/inhalt/daten.py (PREISE, INKLUSIVE), nie geraten.
  Übersetzen               JSON mit betreff, text und verlauf in gleicher Länge (ohne KI: der Wortlaut unverändert).
  Wissen einlesen          Werkzeug «eintraege» mit einem Eintrag je Material.
"""
import importlib.util, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
BEREICH = 'Das Haus'
_CHAT = None
_D = None


def _daten():
    """website/inhalt/daten.py, nur gelesen (Preise und Inklusive für die Probe-Briefe)."""
    global _D
    if _D is None:
        s = importlib.util.spec_from_file_location('mm_daten_probe', os.path.join(HIER, '..', '..', 'website', 'inhalt', 'daten.py'))
        _D = importlib.util.module_from_spec(s); s.loader.exec_module(_D)
    return _D


def _beleg(frage):
    """Antwort ohne KI wie die Rezeption im Chat der Website (gast/website_chat.py); None, wenn nicht ladbar."""
    global _CHAT
    try:
        if _CHAT is None:
            s = importlib.util.spec_from_file_location('website_chat_probe', os.path.join(HIER, 'gast', 'website_chat.py'))
            m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
            _CHAT = m
        return _CHAT.antworte(frage)
    except Exception:  # noqa: BLE001
        return None


def _text(koerper):
    """Alles, was der Aufruf an Text mitschickt (System und Nachrichten), für die Erkennung der Stelle."""
    s = koerper.get('system')
    sys_t = s if isinstance(s, str) else ' '.join(b.get('text', '') for b in (s or []) if isinstance(b, dict))
    msg = []
    for m in koerper.get('messages') or []:
        c = m.get('content')
        if isinstance(c, str):
            msg.append(c)
        else:
            msg += [b.get('text', '') for b in c or [] if isinstance(b, dict) and b.get('type') == 'text']
    return sys_t, msg


def _antwort(text='', werkzeug=None):
    inhalt = [{'type': 'text', 'text': text}] if text else []
    if werkzeug:
        inhalt.append({'type': 'tool_use', 'id': 'toolu_probe', 'name': werkzeug[0], 'input': werkzeug[1]})
    return {'content': inhalt, 'stop_reason': 'tool_use' if werkzeug else 'end_turn', 'usage': {'input_tokens': 0, 'output_tokens': 0}}


GRUSS = '\n\nHerzliche Grüsse aus Saas-Almagell\n\nEsther und Fabian Zurbriggen\nHotel Monte-Moro'


def _brief(letzte):
    D = _daten()
    feld = lambda k: (re.search(k + r':\s*(.+)', letzte) or [None, ''])[1].strip()
    wer = feld('Name') or 'Gast'
    art, datum, pers = feld('Art'), feld('Datum'), feld('Personen')
    allerg, hinw = feld(r'Allergien \(Formular\)'), feld('Hinweise')
    datum = '' if datum == 'nicht genannt' else datum
    pers = '' if pers == 'nicht genannt' else pers
    p = {(k, a): v for k, a, v in D.PREISE}
    ab_zf, ab_hp = p[('Budgetzimmer', 'Zimmer mit Frühstück')], p[('Budgetzimmer', 'Zimmer mit Halbpension (4-Gänge)')]
    satz_al = (f'Ihre Angaben zu Allergien ({allerg}) geben wir an unsere Küche weiter [Küche fragen].\n\n' if allerg and allerg != 'keine angegeben' else '')
    satz_ki = ('Für Ihre Kinder ist der Kidsclub täglich von Montag bis Samstag, 16:30 bis 21:00 Uhr, offen und im Preis inbegriffen.\n\n'
               if re.search(r'kind|kidsclub', letzte, re.I) else '')
    anrede = f'Guten Tag {wer},\n\n'
    if art == 'Tisch im Röstihüs':
        wann = f' am {datum}' if datum else ''
        return (f'Betreff: Ihr Tisch im Röstihüs\n\n{anrede}herzlichen Dank für Ihre Reservierung. Wir freuen uns, Sie{wann} im Röstihüs zu begrüssen'
                + (f', {pers} Personen' if pers else '') + ' [Tisch prüfen].\n\n'
                'Auf unserer Karte stehen elf Röstis und fünf Cordon bleus, dazu Walliser Weine und der Hotelwein, den Fabian selbst kreiert hat.\n\n'
                f'{satz_al}{satz_ki}Damit wir Ihren Tisch in Ruhe vorbereiten können:\n- an welchem Tag\n- um welche Uhrzeit\n- für wie viele Personen'
                + GRUSS + '\n---\nGrundlage: Röstihüs (Website)\nOffen: freier Tisch, Öffnungszeiten (nicht veröffentlicht)')
    if art == 'Ferienwohnung':
        return (f'Betreff: Ihre Ferienwohnung in Saas-Almagell\n\n{anrede}herzlichen Dank für Ihre Anfrage und Ihr Interesse an unseren Ferienwohnungen.\n\n'
                'Im Haus Apollo am Dorfeingang wohnen Sie im 4. Stock mit Ausblick auf das ganze Dorf; im Haus Arizona gibt es 4½-, 3½- und 2½-Zimmer-Wohnungen. '
                'Bett- und Frotteewäsche stehen Ihnen zur Verfügung, der Parkplatz liegt direkt neben dem Haus.\n\n'
                'Den Preis für Ihren Aufenthalt nennen wir Ihnen gern persönlich [Preis der Wohnung], sobald wir wissen, welche Wohnung frei ist [Wohnung prüfen].\n\n'
                f'{satz_ki}Damit wir Ihnen ein genaues Angebot machen können:\n- Anreise und Abreise\n- wie viele Erwachsene und Kinder\n- Haus Apollo oder Haus Arizona'
                + GRUSS + '\n---\nGrundlage: Zimmer und Ferienwohnungen (Website)\nOffen: Preis der Wohnung (nicht veröffentlicht), freie Wohnung')
    if art == 'Zimmer':
        wann = f' für {datum}' if datum else ''
        return (f'Betreff: Ihr Aufenthalt im Hotel Monte-Moro\n\n{anrede}herzlichen Dank für Ihre Anfrage und Ihr Interesse an unserem Haus in Saas-Almagell.\n\n'
                f'Gern schauen wir{wann}, welches Zimmer für Sie frei ist [Zimmer prüfen]. Ein Zimmer mit Frühstück kostet bei uns ab CHF {ab_zf} pro Person und Tag, '
                f'mit Halbpension (4 Gänge) ab CHF {ab_hp}. Inklusive sind die Postautos im ganzen Saastal und im Sommer alle Bergbahnen im Saastal (ohne Metro Alpin).\n\n'
                f'{satz_ki}{satz_al}Damit wir Ihnen ein genaues Angebot machen können:\n- Anreise und Abreise\n- wie viele Erwachsene und Kinder (mit Alter)\n- Zimmer mit Frühstück oder mit Halbpension'
                + GRUSS + '\n---\nGrundlage: Preise (Website)\nOffen: freies Zimmer, Zeitraum, Anzahl Gäste' + (f'\nHinweise: {hinw}' if hinw and hinw != 'keine' else ''))
    return (f'Betreff: Ihre Nachricht an das Hotel Monte-Moro\n\n{anrede}herzlichen Dank für Ihre Nachricht.\n\n'
            'Gern beantworten wir Ihre Frage persönlich [Antwort des Teams].\n\n'
            f'{satz_al}Für alles Weitere erreichen Sie uns jederzeit an der Rezeption.' + GRUSS + '\n---\nGrundlage: Kontakt (Website)\nOffen: Antwort auf die Frage')


def api(koerper):
    sys_t, msg = _text(koerper)
    werkzeuge = [w.get('name') for w in koerper.get('tools') or []]
    letzte = msg[-1] if msg else ''
    if 'eintraege' in werkzeuge:                                    # Wissen einlesen (gedaechtnis._auszug)
        m = re.search(r'BEREICH DES TEAMS: (.+)', letzte)
        bereich = (m.group(1).strip() if m else '') or BEREICH
        roh = ' '.join(msg)
        stueck = re.sub(r'\s+', ' ', roh.split('TEXT DES TEAMS:', 1)[-1] if 'TEXT DES TEAMS:' in roh else roh)[-220:].strip()
        return _antwort(werkzeug=('eintraege', {'grund': 'Aus dem Dokument übernommen', 'eintraege': [
            {'bereich': bereich, 'titel': (' '.join(stueck.split()[:6]) or 'Neuer Eintrag'), 'text': stueck, 'gueltig_bis': None}]}))
    if sys_t.startswith('Du übersetzt'):                             # reception.uebersetzen
        try:
            d = json.loads(letzte)
        except ValueError:
            d = {}
        return _antwort(json.dumps({'betreff': str(d.get('betreff', '')), 'text': str(d.get('text', '')),   # ohne KI: der Wortlaut des Gastes unverändert, ohne Probe-Beschriftung (Tor K23, 30.10.2026)
                                    'verlauf': [str(v) for v in d.get('verlauf') or []]}, ensure_ascii=False))
    if 'ANFRAGE:' in letzte:                                         # gast.anfrage (Brief)
        return _antwort(_brief(letzte))
    # Chat (gast.frage, auch der zweite Schritt nach dem Weg zu «Zimmer buchen»)
    if any(isinstance(m.get('content'), list) and any(b.get('type') == 'tool_result' for b in m['content']) for m in koerper.get('messages') or []):
        return _antwort('OK')
    frage = letzte.strip()
    kontakt = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+|00)\d[\d\s]{7,}\d', frage)
    if kontakt and 'anfrage' in werkzeuge:
        name = re.search(r'(?:ich bin|ich heisse|mein name ist|name:|my name is|je suis)\s+([A-ZÄÖÜ][\w-]+(?:\s+[A-ZÄÖÜ][\w-]+)?)', frage, re.I) \
            or re.match(r'\s*([A-ZÄÖÜ][a-zäöüé-]+\s+[A-ZÄÖÜ][a-zäöüé-]+)\s*,', frage)
        pers = re.search(r'(\d{1,3})\s*(?:personen|gäste|erwachsene|persons|people|personnes)', frage, re.I)
        art = ('wohnung' if re.search(r'ferienwohnung|wohnung|apollo|arizona|apartment', frage, re.I)
               else 'tisch' if re.search(r'tisch|röstihüs|roestihues|raclette|abendessen|essen|table|restaurant', frage, re.I)
               else 'zimmer' if re.search(r'zimmer|nacht|nächte|übernacht|buchen|halbpension|frühstück|aufenthalt|room|night|stay', frage, re.I) else 'nachricht')
        return _antwort('Herzlichen Dank, Ihre Anfrage liegt jetzt bei der Rezeption. Esther und Fabian melden sich persönlich bei Ihnen.',
                        ('anfrage', {'art': art, 'name': name.group(1) if name else 'Gast', 'kontakt': kontakt.group(0), 'datum': None,
                                     'personen': int(pers.group(1)) if pers else None, 'anliegen': frage[:300]}))
    if 'lücke' in frage.lower() or 'luecke' in frage.lower():
        return _antwort('Dazu steht nichts in meinen Unterlagen. Esther und Fabian beantworten Ihre Frage gern persönlich.', ('nicht_belegt', {'thema': frage[:80]}))
    if 'reservieren' in werkzeuge and re.search(r'zimmer (buchen|frei|reservier)|buchen|übernachten|book a room|a room for', frage, re.I):   # wie echt: der Weg zu «Zimmer buchen» unter der Antwort
        p = {(k, a): v for k, a, v in _daten().PREISE}
        return _antwort('Mit «Zimmer buchen» auf der Website geht es am schnellsten; die Rezeption ist auch am Telefon und per E-Mail für Sie da.\n'
                        f"- Mit Frühstück: ab CHF {p[('Budgetzimmer', 'Zimmer mit Frühstück')]} pro Person und Tag\n"
                        f"- Mit Halbpension: ab CHF {p[('Budgetzimmer', 'Zimmer mit Halbpension (4-Gänge)')]} pro Person und Tag",
                        ('reservieren', {'datum': None, 'uhrzeit': None, 'personen': None}))
    b = _beleg(frage)
    if b and b.get('belegt'):
        return _antwort(b['text'])
    text = (b or {}).get('text') or 'Dazu steht nichts in meinen Unterlagen. Esther und Fabian beantworten Ihre Frage gern persönlich.'
    return _antwort(text, ('nicht_belegt', {'thema': (b or {}).get('thema') or frage[:80]}))
