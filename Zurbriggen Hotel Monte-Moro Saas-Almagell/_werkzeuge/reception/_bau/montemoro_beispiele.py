#!/usr/bin/env python3
"""Beispiele für die Rezeption des Hotel Monte-Moro (08.11.2026, Muster _bau/culinarium_beispiele.py des Culinarium): schreibt gast_beispiele.json
(Anfragen im Eingang) und gast_beispiel_fragen.json («Das wurde gefragt»). Die Gäste sind erfunden (Vornamen und Namen wie im Stamm, Adressen
example.com, Telefonnummern mit 555), in der Oberfläche steht «Beispiel» dabei (Master E10, R20). Jede Angabe des Hauses in Antworten und Briefen
kommt aus website/inhalt/daten.py bzw. steht so in gast/gast_wissen.txt oder gast/gast_umgebung.txt; Preise, Zeiten, Leistungen sind nicht erfunden.
Die Antworten der deutschen Fragen sind genau die der Rezeption im Chat der Website (gast/website_chat.py über assets/js/wissen.json).
Zwei Fragen haben mit Absicht keine Antwort (Öffnungszeiten des Röstihüs, Check-in): das Haus veröffentlicht es nicht, Lücken zum Nachtragen.
Nie erfinden, das Team habe etwas nachgetragen (gast_beispiel_nachgetragen.json bleibt leer, die Oberfläche zeigt beschriftete Musterkarten).
Die Anfragen der Website haben genau die Zeilen, die reception.website_anfrage aus dem Anfrage-Fenster (assets/js/anfrage.js) macht.
Prüfung am Ende: jede Zahl der Antworten und Briefe steht im Wissen oder ist eine Angabe des erfundenen Gastes.
Aufruf: python3 _werkzeuge/reception/_bau/montemoro_beispiele.py"""
import importlib.util, json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, C)
from reception import DANKE, D, KONTAKT   # Dank an den Gast, Angaben des Hauses (website/inhalt/daten.py), Kontakt der Rezeption
s = importlib.util.spec_from_file_location('website_chat', os.path.join(C, 'gast', 'website_chat.py'))
W = importlib.util.module_from_spec(s); s.loader.exec_module(W)

P = {(k, a): v for k, a, v in D.PREISE}
ZF, ZF_ST = P[('Budgetzimmer', 'Zimmer mit Frühstück')], P[('Standardzimmer', 'Zimmer mit Frühstück')]
HP, HP_ST = P[('Budgetzimmer', 'Zimmer mit Halbpension (4-Gänge)')], P[('Standardzimmer', 'Zimmer mit Halbpension (4-Gänge)')]
ZU = dict(D.ZUSCHLAEGE)
KI = dict(D.KINDER)
SPA = {k: p for k, p, _ in D.SPA_TARIFE}
GRUSS = '\n\nHerzliche Grüsse aus Saas-Almagell\n\nEsther und Fabian Zurbriggen\nHotel Monte-Moro'


def web(seite, seite_name, formular, betreff, zeilen):
    n = '\n'.join([f'Betreff: {betreff}'] + zeilen)
    return {'web': True, 'an': KONTAKT, 'seite': seite, 'seite_name': seite_name, 'formular': formular, 'nachricht': n,
            'verlauf': [['user', f'Über ein Formular der Website (Seite {seite_name}): ' + n]]}


def chat(*z):
    return {'verlauf': [[('user' if i % 2 == 0 else 'assistant'), t] for i, t in enumerate(z)]}


A = [
    dict(vor=[0, 9, 12], art='zimmer', status='neu', abteilung='Zimmer', name='Anna Meier', kontakt='anna.meier@example.com', datum='', personen=None, sprache='de',
         anliegen='Familienzimmer: Wir möchten vom 26. bis 30. Dezember 2026 mit zwei Kindern (5 und 9 Jahre) kommen, gern mit Halbpension.', betreff='', text='', team='',
         **web('/zimmer.html', 'Zimmer', 'zimmer', 'Familienzimmer', ['Ihre Nachricht: Wir möchten vom 26. bis 30. Dezember 2026 mit zwei Kindern (5 und 9 Jahre) kommen, gern mit Halbpension.'])),
    dict(vor=[1, 20, 5], art='zimmer', status='gelesen', abteilung='Zimmer', name='Thomas Gerber', kontakt='+41 79 555 01 23',
         datum='14. bis 16. Januar 2027', personen=2, sprache='de',
         anliegen='Zimmer für zwei Erwachsene mit Halbpension, 2 Nächte im Januar; der Hund Bruno kommt mit.',
         betreff='Ihr Wochenende im Januar mit Bruno',
         text=('Guten Tag Thomas Gerber,\n\nherzlichen Dank für Ihre Anfrage. Wir freuen uns, Sie und Bruno vom 14. bis 16. Januar bei uns in Saas-Almagell zu begrüssen; '
               'ob das Zimmer für diese Tage frei ist, prüfen wir gern für Sie [Zimmer prüfen].\n\n'
               f'Ein Zimmer mit Halbpension (4 Gänge) kostet bei uns ab CHF {HP} pro Person und Tag; für einen Aufenthalt von 1 bis 3 Nächten kommt ein Zuschlag von CHF {ZU["Zuschlag für 1 - 3 Übernachtungen / pro Tag"]} pro Tag dazu. '
               f'Für Bruno rechnen wir CHF {ZU["Hund pro Tag ohne Futter"]} pro Tag ohne Futter [Preis für den Hund].\n\n'
               'Das Postauto im ganzen Saastal ist im Preis inbegriffen, und an einem Abend der Woche ist Racletteabend im Stübli.' + GRUSS),
         team=('Grundlage: Preise (Halbpension, Zuschläge, Hund), Inklusive.\n'
               'Offen: freies Zimmer, Preis für den Hund innerhalb CHF 7.00 bis 10.00, Budget- oder Standardzimmer.'),
         **chat('Grüezi, wir möchten im Januar zwei Nächte zu zweit kommen, vom 14. bis 16. Januar, mit Halbpension. Dürfen wir unseren Hund mitnehmen?',
                f'Ja, Ihr Hund ist bei uns willkommen; laut Preisliste kostet er CHF {ZU["Hund pro Tag ohne Futter"]} pro Tag ohne Futter. Möchten Sie, dass ich Ihre Anfrage an die Rezeption weitergebe? Dann brauche ich Ihren Namen und eine E-Mail-Adresse oder Telefonnummer.',
                'Thomas Gerber, +41 79 555 01 23. Der Hund heisst Bruno.',
                DANKE['de'])),
    dict(vor=[1, 11, 30], art='tisch', status='neu', abteilung='Röstihüs', name='Claudia Imboden', kontakt='claudia.imboden@example.com', datum='Sa, 14. November 2026',
         uhrzeit='19:00 Uhr', personen=4, sprache='de', anliegen='Tisch im Röstihüs: Wir freuen uns auf Röstis. Eine von uns isst kein Gluten.', betreff='', text='', team='',
         **web('/roestihues.html', 'Röstihüs', 'tisch', 'Tisch im Röstihüs', ['Tag: Sa, 14. November 2026', 'Uhrzeit: 19:00 Uhr', 'Personen: 4', 'Ihre Nachricht: Wir freuen uns auf Röstis. Eine von uns isst kein Gluten.'])),
    dict(vor=[2, 18, 45], art='wohnung', status='gelesen', abteilung='Ferienwohnungen', name='Markus Brunner', kontakt='markus.brunner@example.com', datum='', personen=None, sprache='de',
         anliegen='Haus Arizona: Wir sind zu fünft und suchen vom 1. bis 8. August 2027 eine 3½-Zimmer-Wohnung.',
         betreff='Ihre Ferienwohnung im Haus Arizona',
         text=('Guten Tag Markus Brunner,\n\nherzlichen Dank für Ihre Anfrage und Ihr Interesse an unseren Ferienwohnungen. Gern schauen wir, ob für Sie fünf vom 1. bis 8. August eine 3½-Zimmer-Wohnung im Haus Arizona frei ist [Wohnung prüfen].\n\n'
               'Die Wohnungen sind komfortabel eingerichtet, mit TV, Radio, Geschirrspülmaschine, Kaffeemaschine und Mikrowelle; Bett- und Frotteewäsche stehen Ihnen zur Verfügung, und der Parkplatz liegt direkt neben dem Haus.\n\n'
               'Den Preis für Ihre Woche nennen wir Ihnen gern persönlich [Preis der Wohnung]. Im Sommer sind bei uns alle Bergbahnen im Saastal ausser der Metro Alpin inklusive.' + GRUSS),
         team='Grundlage: Zimmer und Ferienwohnungen (Haus Arizona), Inklusive.\nOffen: Preis der Wohnung (nicht veröffentlicht), freie Wohnung, ob die Bergbahnen auch für Gäste der Ferienwohnungen gelten.',
         **web('/zimmer.html', 'Zimmer', 'zimmer', 'Haus Arizona', ['Ihre Nachricht: Wir sind zu fünft und suchen vom 1. bis 8. August 2027 eine 3½-Zimmer-Wohnung.'])),
    dict(vor=[3, 14, 10], art='nachricht', status='erledigt', abteilung='Nachrichten', name='Sabine Lehner', kontakt='sabine.lehner@example.com', datum='', personen=None, sprache='de',
         anliegen='Fragt, was das Spa im Partnerhotel kostet und ob Bademäntel dabei sind.',
         betreff='Das Spa im Partnerhotel',
         text=('Guten Tag Sabine Lehner,\n\nschön, dass Sie sich nach einem Tag am Berg etwas Gutes tun möchten. Unsere Gäste nutzen das ausgezeichnete Spa im Partnerhotel Pirmin Zurbriggen gleich nebenan.\n\n'
               f'Der Eintritt kostet {SPA["pro Person und Eintritt"]} pro Person, das 7-Tage-Abo {SPA["7 Tage Abo pro Person"]} pro Person. Bademantel, Schuhe und Handtücher stehen Ihnen zur Verfügung.' + GRUSS),
         team='Grundlage: Spa (Tarife, «Bademantel, Schuhe, Handtücher stehen zur Verfügung»).\nOffen: nichts.',
         **chat('Was kostet das Spa nebenan, und muss ich einen Bademantel mitbringen?',
                f'Das Spa im Partnerhotel kostet {SPA["pro Person und Eintritt"]} pro Person und Eintritt, das 7-Tage-Abo {SPA["7 Tage Abo pro Person"]}. Bademantel, Schuhe und Handtücher stehen zur Verfügung. Möchten Sie der Rezeption noch etwas schreiben? Dann brauche ich Ihren Namen und eine E-Mail-Adresse.',
                'Sabine Lehner, sabine.lehner@example.com. Danke, das war schon alles.',
                DANKE['de'])),
    dict(vor=[5, 21, 15], art='zimmer', status='gelesen', abteilung='Zimmer', name='James Whitfield', kontakt='james.whitfield@example.com', datum='February, 3 nights', personen=1, sprache='en',
         anliegen='Single room for 3 nights in February, for skiing.',
         betreff='Your skiing days in Saas-Almagell',
         text=('Dear James Whitfield,\n\nthank you very much for your enquiry. We would be delighted to welcome you for three nights in February [Zimmer prüfen]; the ski area of Saas-Almagell is just two minutes on foot from the hotel.\n\n'
               f'A room with breakfast starts at CHF {ZF} per person and day, with half board (4 courses) at CHF {HP}. For a single room we add {ZU["Einzelzimmerzuschlag"]}, and for stays of 1 to 3 nights CHF {ZU["Zuschlag für 1 - 3 Übernachtungen / pro Tag"]} per day.\n\n'
               'Please let us know your dates of arrival and departure, and whether you would like breakfast or half board.\n\nWarm regards from Saas-Almagell\n\nEsther und Fabian Zurbriggen\nHotel Monte-Moro'),
         team='Grundlage: Preise (Zimmer, Einzelzimmerzuschlag, Zuschlag 1 bis 3 Nächte), Lage (2 Gehminuten zum Skigebiet).\nOffen: genaue Daten, freies Zimmer.',
         deutsch={'betreff': 'Ihre Skitage in Saas-Almagell',
                  'text': ('Guten Tag James Whitfield,\n\nherzlichen Dank für Ihre Anfrage. Wir freuen uns, Sie im Februar für drei Nächte zu begrüssen [Zimmer prüfen]; das Skigebiet Saas-Almagell liegt nur zwei Gehminuten vom Hotel.\n\n'
                           f'Ein Zimmer mit Frühstück kostet ab CHF {ZF} pro Person und Tag, mit Halbpension (4 Gänge) ab CHF {HP}. Für ein Einzelzimmer kommen {ZU["Einzelzimmerzuschlag"]} dazu, für 1 bis 3 Nächte CHF {ZU["Zuschlag für 1 - 3 Übernachtungen / pro Tag"]} pro Tag.\n\n'
                           'Bitte nennen Sie uns Anreise und Abreise und ob Sie Frühstück oder Halbpension wünschen.' + GRUSS)},
         verlauf_de=['Guten Tag, ich möchte im Februar drei Nächte zum Skifahren kommen, allein. Haben Sie ein Einzelzimmer?',
                     'Gern gebe ich Ihre Anfrage an die Rezeption weiter. Wie ist Ihr Name, und wie erreicht Sie das Haus?',
                     'James Whitfield, james.whitfield@example.com',
                     DANKE['de']],
         **chat('Hello, I would like to come for three nights of skiing in February, on my own. Do you have a single room?',
                'I will gladly pass your request on to our reception. What is your name, and how can the hotel reach you?',
                'James Whitfield, james.whitfield@example.com',
                DANKE['en'])),
    dict(vor=[6, 10, 20], art='nachricht', status='neu', abteilung='Nachrichten', name='Peter Schmid', kontakt='+41 76 555 44 33', datum='', personen=None, sprache='de',
         anliegen='Frage zu den Preisen: Gilt die Gratis-Anreise mit dem Zug auch im Dezember noch?', betreff='', text='', team='',
         **web('/preise.html', 'Preise', 'allgemein', 'Frage zu den Preisen', ['Ihre Nachricht: Gilt die Gratis-Anreise mit dem Zug auch im Dezember noch?'])),
]


def wie_website(frage):
    a = W.antworte(frage)
    return dict(frage=frage, antwort=a['text'], belegt=a['belegt'], thema=a.get('thema', ''))


F = [
    dict(vor=[0, 10, 20], sprache='de', buchung=False, **wie_website('Was ist im Preis inbegriffen?')),
    dict(vor=[0, 8, 55], sprache='de', buchung=True, **wie_website('Was kostet ein Zimmer?')),
    dict(vor=[1, 19, 5], sprache='de', **wie_website('Gibt es einen Kidsclub für Kinder?')),
    dict(vor=[1, 13, 40], sprache='de', **wie_website('Wann hat das Röstihüs am Abend offen?')),
    dict(vor=[2, 17, 25], sprache='de', **wie_website('Sind Hunde erlaubt?')),
    dict(vor=[2, 9, 10], sprache='de', **wie_website('Wie komme ich mit dem Zug und Postauto zu Ihnen?')),
    dict(vor=[3, 12, 30], sprache='de', **wie_website('Ab wann können wir am Anreisetag ins Zimmer, gibt es einen Check-in?')),
    dict(vor=[3, 15, 45], sprache='en', belegt=True, thema='', frage='Are the cable cars included in summer?',
         antwort='Yes, in summer all cable cars in the Saastal are included, except the Metro Alpin; the post buses in the whole Saastal are included in summer and winter.'),
    dict(vor=[4, 11, 0], sprache='de', **wie_website('Was kostet das Spa im Partnerhotel?')),
    dict(vor=[4, 18, 20], sprache='de', **wie_website('Kann ich in Euro bezahlen?')),
]
for f in F:
    f.setdefault('thema', ''); f.setdefault('buchung', False)


def pruefen():
    """Jede Zahl in Antworten und Briefen steht im Wissen (Angaben des Hauses) oder ist eine Angabe des erfundenen Gastes; zwei Fragen ohne Antwort."""
    w = ''.join(open(os.path.join(C, 'gast', n), encoding='utf-8').read() for n in ('gast_wissen.txt', 'gast_umgebung.txt'))
    erlaubt = {'14', '16', '2027', '2026', '1', '8', '26', '30', '5', '9', '3', '4', '79', '555', '01', '23', '76', '44', '33', '41', '2', '19', '00', '7'}   # Tage, Personen, Alter und Nummern der erfundenen Gäste
    fehler = []
    for x in [a.get('text', '') + ' ' + a.get('betreff', '') + ' ' + a.get('team', '') for a in A] + [f['antwort'] for f in F]:
        for z in re.findall(r'\d+(?:[.,]\d+)?', x.replace('+41 27 957 10 12', '')):
            if z not in w and z not in erlaubt:
                fehler.append(z)
    if fehler:
        sys.exit('PRUEF · Zahlen ohne Beleg: ' + ', '.join(sorted(set(fehler))))
    if sum(1 for f in F if not f['belegt']) != 2:
        sys.exit('PRUEF · Es sollen genau zwei Fragen ohne Antwort sein: ' + ', '.join(f['frage'] for f in F if not f['belegt']))
    if re.search(r'geschenkt|gratis', ' '.join(a.get('text', '') for a in A), re.I):
        sys.exit('PRUEF · ein Brief bietet die abgelaufene Gratis-Anreise an.')


if __name__ == '__main__':
    pruefen()
    json.dump(A, open(os.path.join(C, 'gast_beispiele.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(F, open(os.path.join(C, 'gast_beispiel_fragen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([], open(os.path.join(C, 'gast_beispiel_nachgetragen.json'), 'w', encoding='utf-8'))
    print(len(A), 'Anfragen,', len(F), 'Fragen (davon', sum(1 for f in F if not f['belegt']), 'ohne Antwort)')
