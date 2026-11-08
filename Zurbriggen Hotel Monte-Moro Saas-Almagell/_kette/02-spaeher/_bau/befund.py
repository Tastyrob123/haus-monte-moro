#!/usr/bin/env python3
"""Befund Station 2 (Späher) als Seite im Stand der Werkbank: Hotel Monte-Moro, Saas-Almagell.
Aufbau mit dem Werkbank-Kit (kern.py, werkbank.css, werkbank.js), Haken in _werkbank/haus.py.
Inhalt: ../befund.md, ../einordnung.json, ../../stand.json (offene Punkte). Fotos: nur echte Bilder der Häuser aus _quelle.
Aufruf: python3 befund.py   →  ../befund.html"""
import json, os, sys, html
HIER = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], HIER]
sys.path.insert(0, os.path.expanduser('~/Desktop/Website-Projekte/_Werkbank-Kit'))
import kern as K  # noqa: E402

e = html.escape
PAKET = os.path.dirname(HIER)
Q = os.path.expanduser('~/Desktop/Website-Projekte/Familie Zurbriggen/_quelle/')
MM = Q + 'monte-moro/'
IMG = os.path.join(HIER, 'img')
os.makedirs(IMG, exist_ok=True)
HEUTE = 'https://www.monte-moro.ch/de/'

BILDER = {
    'haus': (MM + 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291891853-hotel-restaurant-monte.jpg', 2000, 'Das Hotel Monte-Moro im Winter'),
    'sommer': (MM + 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291891830-hotel-restaurant-monte.jpg', 1400, 'Das Hotel Monte-Moro im Sommer'),
    'stube': (MM + 'website/bilder/restau_restaurant.jpg', 1280, 'Die Stube des Röstihüs'),
    'raclette': (MM + 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291892107-raclettestubli.jpg', 1200, 'Das Raclettestübli'),
    'zimmer': (MM + 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291892318-doppelzimmer.jpg', 1100, 'Ein Doppelzimmer'),
    'balkon': (MM + 'website/bilder/aktuel_hotel-monte-moro-saas-almagell-balkon.jpg', 1100, 'Blick vom Balkon ins Tal'),
    'fruehstueck': (MM + 'extern/tripadvisor/vom-hotel/tripadvisor-2018-02-17-303351039-fruhstucksbuffet.jpg', 1100, 'Das Frühstücksbuffet'),
    'wellness': (Q + 'saas-almagell/extern/myswitzerland/myswitzerland-00044124_m.jpg', 900, 'Wellness & Spa Pirmin Zurbriggen'),
    'loft': (Q + 'loft-suite/website/bilder/zimmer-2692-98629.jpg', 900, 'Loft-Suite Hotel'),
    'zermatt': (Q + 'zermatt/extern/booking/booking-19385120.jpg', 900, 'Suitenhotel Zurbriggen, Zermatt'),
    'rustica': (Q + 'chalet-rustica/spiegel/rustica/bilder/nr5wohngross.jpg', 700, 'Chalet Rustica'),
}
DUNKEL = {'haus': (.5, .62), 'stube': (.12, .45)}   # das Dunkel steckt im Bild, nichts Durchscheinendes darüber
M = {}
for k, (q, b, alt) in BILDER.items():
    M[k] = (K.webp(q, os.path.join(IMG, k + '.webp'), b, dunkel=DUNKEL.get(k)), alt)


def bild(k, klasse='', lazy=True):
    (w, h), alt = M[k]
    st = f' style="background-image:url({K.VORAB[k]})"' if k in K.VORAB else ''
    return f'<img src="_bau/img/{k}.webp" width="{w}" height="{h}" alt="{e(alt)}"{" loading=lazy decoding=async" if lazy else ""} class="ld {klasse}"{st}>'


def abzug(k, unter, klasse='', r=0, i=0):
    return f'<div class="abzug {klasse}" data-a="schweb" style="--r:{r}deg;--r0:{r * 3}deg;--i:{i}">{bild(k)}<span>{e(unter)}</span></div>'


stand = json.load(open(os.path.join(PAKET, 'stand.json'), encoding='utf-8'))
offen = stand.get('offen', [])
ein = json.load(open(os.path.join(PAKET, 'einordnung.json'), encoding='utf-8'))

PF, HZ, kap, titel, kn = K.PF, K.HZ, K.kap, K.titel, K.kn


def kopf(nr, name, zeilen, text=''):
    return K.kopf(nr, name, zeilen, text) if text else f'<div class="kopfzeile"><div>{kap(nr, name)}{titel(zeilen)}</div></div>'


# ---------------------------------------------------------------- Inhalt (alles aus befund.md, Quellen dort)
STAND_ZEILEN = [
    ('Technik', 'Joomla, Bauteile der Reihe 3, Aufbau aus Tabellen.', 'Quelltext der Startseite, 17.10.2026'),
    ('Wer dahinter steht', 'Vorlage «zerone» von der zerone computer gmbh in Brig-Glis, angelegt am 04.04.2019. Ein laufender Betreuungsvertrag ist nicht belegt. Server bei Webland.', 'templateDetails.xml der Seite, zerone.ch, Namensserver, 17.10.2026'),
    ('Bilder', '88 Bilder, die grössten 1280 px breit. Zimmer, Stube und Haus sind eigene Fotos, die Bilder der Region tragen keine Herkunft, die Wellness-Bilder zeigen das Partnerhotel.', '_quelle/monte-moro/website/bilder'),
    ('Handy', 'Eigene Anordnung mit Menüknopf, der Massstab ist fest auf 0,8 gestellt.', 'Aufnahmen in _qa, Quelltext'),
    ('Ladezeit', 'Startseite 4,5 bis 5,3 Sekunden am Rechner, 2,0 MB, davon 1,65 MB Bilder. Am Handy 3,6 Sekunden. Gemessen ungedrosselt aus Koh Phangan.', '_qa/messung.json, 17.10.2026'),
    ('Sprachen', 'Deutsch, Englisch, Französisch mit je 16 bis 17 Seiten. Der Datenschutz bleibt in allen drei Sprachen deutsch. Speisekarte deutsch und französisch.', '_qa/live, 49 Seiten'),
    ('Buchung', 'Zimmer über einen eingebetteten Shop von seekda, Tische über TheFork oder Telefon, Anfragen über ein Formular.', 'monte-moro.ch/de/buchen.html'),
    ('Rechtstexte', 'Impressum und Datenschutz vorhanden. AGB, Widerruf und Stornobedingungen nicht gefunden.', '_qa/live/text'),
    ('Social', 'Instagram @hotelmonte_moro (173 Follower, 19 Beiträge am 09.10.2026) und Facebook. Newsletter nur als Auswahl im Kontaktformular.', 'Fuss jeder Seite'),
    ('Auszeichnungen', 'Keine eigene. Die Restaurantseite nennt 14 Gault-Millau-Punkte für den Küchenchef des Partnerhotels, Stand nicht geprüft.', 'monte-moro.ch/de/restaurant.html'),
]
AUFFAELLIG = [
    'Die Gratis-Anreise gilt für Buchungen «vom 1. Mai bis 31. Oktober 2026» und steht in zwei Wochen nicht mehr.',
    'Die Pauschale «Top Winterzauber» (CHF 999.00, sieben Nächte) nennt weder Saison noch Jahr.',
    'Das Spa des Partnerhotels steht mit 1700 m² im Sommer, 1000 m² im Winter und an anderer Stelle mit 1100 m² da.',
    'Der Routenplaner der Seite führt zur Talstrasse 129, Google nennt die Furusandstrasse 12.',
    'Im Browser heisst die Startseite «Aktuelles», die Seite Aktuelles «Akuelles».',
]
FEHLT = [
    ('Die Geschichte', 'Kein Wort dazu, seit wann es das Monte-Moro gibt und wer es führt, ausser dem Impressum.'),
    ('Die Zimmer', 'Eine Bildreihe und zwei Absätze. Keine Kategorie mit Grösse, Bild und Preis. Die Preisliste kennt Budget- und Standardzimmer, die Zimmerseite nicht.'),
    ('Die Wohnungen', 'Apollo und Arizona ohne Preis, ohne Grösse, ohne eigenen Buchungsweg.'),
    ('Das Röstihüs', 'Keine Öffnungszeiten, keine Ruhetage. Die Karte gibt es nur als PDF.'),
    ('Die Gäste', 'Bewertungen werden nirgends gezeigt, obwohl Personal und Lage auf Booking bei 9,0 stehen.'),
    ('Das Kleingedruckte', 'Keine AGB, keine Stornobedingungen.'),
]
FAMILIE = [
    ('wellness', 'Wellness & Spa Pirmin Zurbriggen', 'Furrusandstrasse 16, Saas-Almagell', 'Esther und Fabian Zurbriggen', 'https://www.wellnesshotel-zurbriggen.ch'),
    ('loft', 'Loft-Suite Hotel', 'Saas-Almagell', 'Esther und Fabian Zurbriggen', 'https://www.loftsuite.ch'),
    ('zermatt', 'Suitenhotel Zurbriggen', 'Schluhmattstrasse 68, Zermatt', 'Moni und Pirmin Zurbriggen', 'https://zurbriggen.ch/zermatt'),
    ('rustica', 'Chalet Rustica', 'Saas-Almagell', 'Heidi und Damian Andenmatten-Zurbriggen', 'http://www.chalet-rustica.ch'),
]
NOTEN = [
    ('4,5', 'von 5', 'Google', '121 Bewertungen · 17.10.2026'),
    ('8,3', 'von 10', 'Booking.com', '94 Bewertungen · 17.10.2026'),
    ('3,9', 'von 5', 'TripAdvisor', '17 Bewertungen · Stand 09.10.2026'),
]
TEILNOTEN = [('Personal', '9,0'), ('Lage', '9,0'), ('Sauberkeit', '8,8'), ('Komfort', '8,7'), ('Preis-Leistung', '8,6'), ('Ausstattung', '8,0')]
SPRACHEN = [('Deutsch', 46), ('Französisch', 29), ('Niederländisch', 6), ('Italienisch', 3), ('Englisch', 2), ('Rumänisch', 2), ('Weitere sechs', 6)]

# ---------------------------------------------------------------- Abschnitte
T = []
T.append(f'''
<section class="auftakt bf-auftakt">
  {bild('haus', 'bf-auftakt__bild', lazy=False)}
  <div class="in bf-auftakt__in">
    <div class="auftakt__t">
      <p class="gruss" data-a="auf">Station 2 · Der Späher · 17.10.2026</p>
      {titel(['Hotel Monte-Moro,', 'gelesen.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:1600ms">Das Haus mit dem Röstihüs in Saas-Almagell, drei Sterne, 18 Zimmer, Gastgeber laut Impressum Esther und Fabian Zurbriggen. Was die heutige Seite zeigt, was ihr fehlt und ob es weitergeht.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:6">{kn('Heutige Seite öffnen', HEUTE, neu=True)}{kn('Zur Empfehlung', '#empfehlung', 'kn--linie')}</div>
    </div>
    <aside class="bf-urteil" data-a="kipp" style="--i:4">{HZ}<small>Bestätigt am 17.10.2026</small><b>Passt, gehört zur Familie</b><p>Studie als Teil der Familie Zurbriggen. Die Familie steht über den Sternen. Hinter der Seite steht zerone aus Brig-Glis, kein Hindernis.</p></aside>
  </div>
  <div class="in auftakt__fuss mono" data-a="auf" style="--i:9"><span class="runter"><i></i>Einfach nach unten scrollen</span><span>Stand 17.10.2026</span><span>Robert Reff · Tasty Studios</span></div>
</section>''')

T.append(f'''
<section class="fl fl--papier blatt" id="haus">
  <div class="in bf-zwei">
    <div>
      {kap(1, 'Das Haus in Kürze')}
      {titel(['Drei Sterne,', 'ein Röstihüs.'])}
      <div class="lauf">
        <p data-a="auf" style="--i:1">Hotel und Restaurant in Saas-Almagell, 18 Zimmer, 55 Betten, drei Sterne. So steht es bei Schweiz Tourismus, Booking und Google.</p>
        <p data-a="auf" style="--i:2">Dazu gehören das Restaurant Röstihüs, die Ferienwohnungen in den Häusern Apollo und Arizona und weitere Zimmer in der Residence Alpenhof, vier Gehminuten entfernt.</p>
        <p data-a="auf" style="--i:3">Im Impressum steht «Hotel Monte-Moro, Esther und Fabian Zurbriggen-Zurbriggen». Telefon +41 27 957 10 12, info@monte-moro.ch.</p>
      </div>
    </div>
    <div class="bf-stapel">
      {abzug('sommer', 'Das Haus im Sommer', 'bf-a1', -2.2, 1)}
      {abzug('zimmer', 'Ein Doppelzimmer', 'bf-a2', 2.6, 2)}
      {abzug('balkon', 'Vom Balkon ins Tal', 'bf-a3', -1.2, 3)}
    </div>
  </div>
</section>''')

zeilen = ''.join(f'<div class="bf-z" data-a="auf" style="--i:{min(i, 6)}"><b>{e(a)}</b><p>{e(b)}</p><small class="mono">{e(c)}</small></div>' for i, (a, b, c) in enumerate(STAND_ZEILEN))
T.append(f'''
<section class="fl fl--navy tapete blatt" id="seite">
  <div class="in">
    {kopf(2, 'Die heutige Seite', ['Was monte-moro.ch', 'heute zeigt.'], 'Alle 49 Seiten in drei Sprachen am 17.10.2026 neu abgerufen. Inhaltlich ist alles wie am 09.10.2026. Die Seite selbst sehen Sie über den Knopf, nicht als Bild.')}
    <div class="bf-zeilen">{zeilen}</div>
    <div class="bf-platten">
      <div class="bf-platte" data-a="kipp" style="--i:1">{HZ}<h3>Was die Seite gut macht</h3><p>Sie sagt klar, was im Preis steckt: Bergbahnen und Postautos inklusive, Gratis-Anreise mit dem öffentlichen Verkehr, das Spa nebenan mit Preis je Eintritt. Die Preisliste ist offen und vollständig, bis zum Hund pro Tag. Die Lage steht in Gehminuten auf der Startseite.</p></div>
      <div class="bf-platte" data-a="kipp" style="--i:2">{HZ}<h3>Was auffällt</h3><ul>{''.join(f'<li>{e(x)}</li>' for x in AUFFAELLIG)}</ul></div>
    </div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(30px,3.4vw,48px)">{kn('Heutige Seite öffnen', HEUTE, neu=True)}</div>
  </div>
</section>''')

T.append(f'''
<section class="bf-fenster" aria-label="Die Stube des Röstihüs">
  {bild('stube', 'bf-fenster__b')}
  <p class="bf-fenster__s" data-a="auf">«Es lebe die Tradition!» <small>Startseite des Hauses, Abschnitt Röstihüs</small></p>
</section>''')

T.append(f'''
<section class="fl fl--papier blatt" id="fehlt">
  <div class="in">
    {kopf(3, 'Was fehlt', ['Was ein Gast', 'nicht findet.'])}
    <div class="bf-fehlt">{''.join(f'<div class="bf-f" data-a="auf" style="--i:{i}"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(FEHLT))}</div>
  </div>
</section>''')

T.append(f'''
<section class="fl fl--nacht blatt" id="ausmacht">
  <div class="in bf-zwei bf-zwei--um">
    <div class="bf-stapel">
      {abzug('raclette', 'Das Raclettestübli', 'bf-a1', 2, 1)}
      {abzug('fruehstueck', 'Frühstücksbuffet', 'bf-a2', -2.4, 2)}
    </div>
    <div>
      {kap(4, 'Was das Haus ausmacht')}
      {titel(['Mehr erleben,', 'weniger zahlen.'])}
      <div class="lauf">
        <p data-a="auf" style="--i:1">So sagt es das Haus selbst. Bergbahnen und Postautos sind im Sommer und Herbst ab der ersten Nacht inbegriffen, das Skigebiet liegt zwei Gehminuten entfernt, die Busstation drei.</p>
        <p data-a="auf" style="--i:2">Im Röstihüs gibt es nach eigener Angabe 12 Röstis und 7 Cordon Bleus, Walliser Wein, Appenzeller Bier und eine Sonnenterrasse vor dem Haus. Halbpension heisst einmal die Woche Raclette, Kinder haben ihren Club von Montag bis Samstag, 16:30 bis 21:00 Uhr.</p>
        <p data-a="auf" style="--i:3">Wer mehr will, geht nebenan ins Spa des Partnerhotels Pirmin Zurbriggen: CHF 25 je Eintritt, sieben Tage CHF 150.</p>
      </div>
    </div>
  </div>
</section>''')

karten = ''.join(f'''<a class="bf-haus" href="{u}" target="_blank" rel="noopener" data-a="kipp" style="--i:{i}"><span class="bf-haus__b">{bild(k)}</span><span class="bf-haus__t"><b>{e(n)}</b><small>{e(o)}</small><small>{e(g)}</small></span><i>{PF}</i></a>''' for i, (k, n, o, g, u) in enumerate(FAMILIE))
T.append(f'''
<section class="fl fl--creme blatt" id="familie">
  <div class="in">
    {kopf(5, 'Familie und weitere Häuser', ['Die anderen Häuser', 'der Familie.'], 'Gleiche Telefonnummer, gleiche Gastgeber im Impressum, «Partnerhotel» auf der Startseite. Gebaut ist von keinem dieser Häuser schon etwas; die drei anderen laufen heute parallel durch Station 2.')}
    <div class="bf-haeuser">{karten}</div>
    <div class="bf-rot" data-a="auf"><b>Wem das Monte-Moro gehört, ist nicht belegt.</b><p>Im Handelsregister steht die Resort Monte Moro AG (CHE-167.073.174), gegründet am 22.08.2022 an der Talstrasse 129, Zweck «Betrieb von Hotels und Gastrobetrieben». Einziges Mitglied des Verwaltungsrats ist laut SHAB vom 19.09.2022 Oliver Wachs aus Zürich. Seit März 2026 sitzt die Firma an der Furusandstrasse 10. Die Familie Zurbriggen steht dort nicht, das Impressum nennt weiter Esther und Fabian. Ob die AG das Hotel betreibt, ob es verpachtet oder verkauft ist, bleibt offen.</p><small class="mono">Zefix, Abruf 17.10.2026</small></div>
  </div>
</section>''')

noten = ''.join(f'<div class="bf-note" data-a="kipp" style="--i:{i}"><b>{a}</b><small>{e(b)}</small><h3>{e(c)}</h3><p class="mono">{e(d)}</p></div>' for i, (a, b, c, d) in enumerate(NOTEN))
T.append(f'''
<section class="fl fl--navy tapete blatt" id="noten">
  <div class="in">
    {kopf(6, 'Noten', ['Wie Gäste', 'es sehen.'], 'Nur abgelesen. TripAdvisor liess sich heute nicht öffnen, dort gilt der Stand vom 09.10.2026.')}
    <div class="bf-noten">{noten}</div>
    <div class="bf-platten">
      <div class="bf-platte" data-a="kipp" style="--i:1">{HZ}<h3>Booking im Einzelnen</h3><ul class="bf-liste">{''.join(f'<li><span>{e(a)}</span><b>{b}</b></li>' for a, b in TEILNOTEN)}</ul></div>
      <div class="bf-platte" data-a="kipp" style="--i:2">{HZ}<h3>In welcher Sprache Gäste schreiben</h3><ul class="bf-liste">{''.join(f'<li><span>{e(a)}</span><b>{b}</b></li>' for a, b in SPRACHEN)}</ul><p class="mono">Booking, 94 Bewertungen, 17.10.2026</p></div>
    </div>
  </div>
</section>''')

ZERONE_PUNKTE = [
    ('Die Firma', 'Zerone Computer GmbH, Brig-Glis, im Handelsregister seit 1999, Gesellschafter Marc und Daniel Burgener aus Saas-Grund. Programmierung, Fernwartung, Webdesign, Drucksachen. Dieselbe Vorlage tragen vier Hotels in Saas-Fee: La Gorge, Boutique Lodge Spycher, Belmont, Ambiente.', 'Handelsregister Oberwallis, zerone.ch, Quelltext der Seiten'),
    ('Gebaut und geändert', 'zerone baut die Seite mindestens seit Mai 2014 (Web-Archiv). Die heutige Fassung ist von 2019, Joomla 3, für das es seit Februar 2025 keine Sicherheits-Updates mehr gibt. Zuletzt geändert im Mai 2026.', 'web.archive.org, templateDetails.xml, Dateidaten des Servers'),
    ('Preise', 'Nicht öffentlich. «Die aktuellen Preise können bei zerone computer gmbh erfragt werden.» Abgerechnet wird jährlich im Voraus.', 'AGB Ziffer 2a, 2c, 2d'),
    ('Vertrag laut AGB', 'Ein Kalenderjahr, verlängert sich von selbst. Kündigung bis spätestens 15. November. Keine Rückvergütung. Nach Vertragsende werden alle Daten gelöscht, die Sicherung ist Sache des Kunden.', 'AGB «Internet Services», Stand August 2018, Ziffer 3 und 4'),
    ('Nutzungsrechte', 'Die Adresse wird auf den Namen des Kunden registriert. Am Hosting erhält das Haus nur ein Nutzungsrecht, die Rechte bleiben beim Anbieter. Ob zerone Vorlage, Code und Datenbank herausgibt, steht nirgends.', 'AGB Ziffer 5e und 8a, templateDetails.xml'),
    ('Ungeprüft', 'Der tatsächliche Vertrag der Familie mit zerone: Preis, Umfang, Pflege, Laufzeit. Im Gespräch zu klären, keine Tatsache über das Haus.', 'nicht öffentlich'),
]
BESSER = [
    ('Joomla 3 ohne Sicherheits-Updates', 'statischer Bau ohne Joomla und ohne Datenbank hinter der Seite'),
    ('Tabellen-Aufbau, Handy-Massstab fest auf 0,8', 'für das Handy zuerst gebaut, flüssig auch auf schwachen Geräten'),
    ('2 MB auf der Startseite, Bilder höchstens 1280 px', 'Bilder in voller Quellbreite, leicht ausgeliefert'),
    ('Datenschutz nur deutsch, keine AGB', 'alle Rechtstexte im Wortlaut, Sprachwechsel an derselben Stelle'),
    ('Daten werden bei Kündigung gelöscht', 'Seite, Server, Adresse und Zugänge auf das Haus, alles zum Mitnehmen'),
    ('eine Seite als Einzelstück', 'Werkbank mit Karten, Rezeption im Chat, Drucksachen, Besucherbuch'),
]
T.append(f'''
<section class="fl fl--papier blatt" id="zerone">
  <div class="in">
    {kopf(7, 'Wer hinter der heutigen Seite steht', ['zerone aus Brig-Glis,', 'kein Hindernis.'], 'Abgerufen am 17.10.2026. Die Buchung über seekda bleibt, wo sie ist. Alles mit Beleg im Befund als Text.')}
    <div class="bf-zeilen bf-zeilen--hell">{''.join(f'<div class="bf-z" data-a="auf" style="--i:{min(i, 5)}"><b>{e(a)}</b><p>{e(b)}</p><small class="mono">{e(c)}</small></div>' for i, (a, b, c) in enumerate(ZERONE_PUNKTE))}</div>
    <div class="bf-vgl" data-a="auf"><div class="bf-vgl__k"><span>Heute bei zerone</span><span>Mit uns</span></div>{''.join(f'<div class="bf-vgl__z"><p>{e(a)}</p><p>{e(b)}</p></div>' for a, b in BESSER)}</div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(30px,3.4vw,48px)">{kn('AGB von zerone', 'https://www.zerone.ch/agb/agb.pdf', neu=True)}{kn('Handelsregister', 'https://vo.chregister.ch/cr-portal/auszug/auszug.xhtml?uid=CHE-105.348.623', 'kn--linie', neu=True)}</div>
  </div>
</section>''')

offen_html = ''.join(f'<li><b>{e(o["punkt"])}</b><small>{e(o["wo"])}</small></li>' for o in offen) or '<li><b>Keine</b></li>'
T.append(f'''
<section class="schluss" id="empfehlung">
  {bild('haus', 'schluss__b')}
  <div class="in">
    {kap(8, 'Empfehlung')}
    {titel(['Passt, gehört', 'zur Familie.'], 'h2', 't1')}
    <div class="lauf">
      <p data-a="worte">Art: Studie, ungefragt, als Teil der Familie Zurbriggen. Die Seite ist sichtbar älter als das Haus, die Geschichte ist unerzählt, echtes Material liegt bereit, ein Relaunch ist nicht zu sehen.</p>
    </div>
    <div class="bf-platten bf-platten--hell">
      <div class="bf-platte" data-a="kipp" style="--i:1"><h3>Drei Sterne</h3><p>Kein Luxushotel, und trotzdem dabei: Die Familie steht über den Sternen (Robert 17.10.2026). Auf der Familienseite steht es weiter unten.</p></div>
      <div class="bf-platte" data-a="kipp" style="--i:2"><h3>Eigentum nicht öffentlich</h3><p>Das Register führt eine eigene AG mit einem Verwaltungsrat ausserhalb der Familie. Impressum, Karte und Filme 2026 zeigen Esther und Fabian; so stehen sie auch auf jeder Seite.</p></div>
    </div>
    <div class="bf-offen" data-a="auf"><h3>Offen</h3><ul>{offen_html}</ul></div>
    <div class="kn-reihe" data-a="auf">{kn('Heutige Seite öffnen', HEUTE, neu=True)}{kn('Befund als Text', 'befund.md', 'kn--linie', neu=True)}</div>
  </div>
</section>''')

CSS = '''
.bf-auftakt{position:relative;min-height:100svh;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;color:var(--weiss);background:var(--nacht)}
.bf-auftakt__bild{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background-size:cover}
.bf-auftakt__in{position:relative;display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,.65fr);gap:clamp(28px,5vw,90px);align-items:end;padding-top:20vh}
.bf-auftakt .auftakt__fuss{position:relative}
.bf-urteil{background:var(--papier);color:var(--tinte);border-radius:var(--rund);padding:clamp(24px,2.6vw,38px);box-shadow:0 30px 60px -30px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.7)}
.bf-urteil .hz{width:46px;height:auto;color:var(--messing);display:block;margin-bottom:14px}
.bf-urteil small{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--taupe)}
.bf-urteil b{display:block;font-family:var(--serif);font-weight:500;font-size:clamp(24px,2.2vw,32px);line-height:1.12;margin:8px 0 10px}
.bf-urteil p{margin:0;font-size:15px;line-height:1.55}
.bf-zwei{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(30px,6vw,110px);align-items:center}
.bf-stapel{position:relative;min-height:clamp(380px,40vw,560px)}
.bf-stapel .abzug{position:absolute;width:62%}
.bf-a1{left:0;top:0}.bf-a2{right:0;top:22%}.bf-a3{left:14%;bottom:0;width:52%!important}
.bf-zeilen{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;border-radius:var(--rund);overflow:hidden;margin-top:clamp(30px,3.6vw,52px)}
.bf-z{background:rgba(255,255,255,.045);padding:clamp(18px,2vw,28px) clamp(20px,2.2vw,32px);box-shadow:inset 0 1px 0 rgba(255,255,255,.05)}
.bf-z b{font-family:var(--serif);font-weight:500;font-size:clamp(19px,1.6vw,23px);color:var(--gold)}
.bf-z p{margin:8px 0 10px;line-height:1.6;color:rgba(253,250,244,.88)}
.bf-z small{font-size:11px;letter-spacing:.06em;color:rgba(253,250,244,.5)}
.bf-platten{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(18px,2vw,28px);margin-top:clamp(24px,2.6vw,38px)}
.bf-platte{background:var(--papier);color:var(--tinte);border-radius:var(--rund);padding:clamp(24px,2.6vw,38px);box-shadow:inset 0 2px 10px rgba(21,32,46,.10),0 24px 50px -32px rgba(0,0,0,.55)}
.bf-platte .hz{width:40px;height:auto;color:var(--messing);display:block;margin-bottom:12px}
.bf-platte h3{font-family:var(--serif);font-weight:500;font-size:clamp(22px,1.9vw,28px);margin:0 0 10px}
.bf-platte p,.bf-platte li{line-height:1.6;font-size:15.5px}
.bf-platte ul{margin:0;padding-left:1.1em}
.bf-platte li+li{margin-top:6px}
.bf-liste{list-style:none;padding:0!important}
.bf-liste li{display:flex;justify-content:space-between;border-bottom:1px solid rgba(21,32,46,.12);padding:7px 0;margin:0!important}
.bf-liste b{font-family:var(--serif);font-weight:500;font-size:18px}
.bf-platte p.mono{font-size:11px;letter-spacing:.06em;color:var(--taupe);margin:12px 0 0}
.bf-fenster{position:relative;height:min(78vh,720px);overflow:hidden;background:var(--nacht)}
.bf-fenster__b{width:100%;height:100%;object-fit:cover}
.bf-fenster__s{position:absolute;left:var(--rand);bottom:clamp(28px,5vw,70px);margin:0;max-width:640px;background:var(--papier);color:var(--tinte);border-radius:var(--rund);padding:22px 30px;font-family:var(--serif);font-size:clamp(24px,2.4vw,34px);line-height:1.2}
.bf-fenster__s small{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--taupe);margin-top:8px}
.bf-fehlt{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,1.8vw,26px);margin-top:clamp(30px,3.4vw,50px)}
.bf-f{background:var(--weiss);border-radius:var(--rund);padding:clamp(22px,2.2vw,32px);box-shadow:inset 0 2px 10px rgba(21,32,46,.07),0 1px 0 rgba(255,255,255,.8)}
.bf-f h3{font-family:var(--serif);font-weight:500;font-size:clamp(21px,1.8vw,26px);margin:0 0 8px;color:var(--navy)}
.bf-f p{margin:0;line-height:1.6}
.bf-zwei--um{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.fl--nacht .lauf p{color:rgba(253,250,244,.86)}
.bf-haeuser{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(14px,1.6vw,24px);margin-top:clamp(30px,3.4vw,50px)}
.bf-haus{position:relative;display:block;background:var(--weiss);border-radius:var(--rund);overflow:hidden;color:var(--tinte);text-decoration:none;box-shadow:0 24px 50px -34px rgba(21,32,46,.5)}
.bf-haus__b{display:block;aspect-ratio:4/3;overflow:hidden}
.bf-haus__b img{width:100%;height:100%;object-fit:cover;transition:transform .9s var(--e1)}
.bf-haus:hover .bf-haus__b img{transform:scale(1.04)}
.bf-haus__t{display:block;padding:18px 20px 22px}
.bf-haus__t b{display:block;font-family:var(--serif);font-weight:500;font-size:20px;line-height:1.2;margin-bottom:6px}
.bf-haus__t small{display:block;font-size:13.5px;line-height:1.5;color:#55606d}
.bf-haus>i{position:absolute;top:14px;right:14px;width:34px;height:34px;border-radius:50%;background:var(--papier);display:grid;place-items:center}
.bf-haus>i svg{width:14px;height:14px;fill:none;stroke:var(--tinte);stroke-width:1.6}
.bf-rot{margin-top:clamp(26px,3vw,42px);border-radius:var(--rund);background:var(--weiss);border-left:5px solid var(--rot);padding:clamp(22px,2.4vw,34px) clamp(24px,2.6vw,38px)}
.bf-rot b{font-family:var(--serif);font-weight:500;font-size:clamp(21px,1.8vw,26px);color:var(--rot)}
.bf-rot p{margin:10px 0;line-height:1.65;max-width:78ch}
.bf-rot small{font-size:11px;letter-spacing:.06em;color:var(--taupe)}
.bf-noten{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,1.8vw,26px);margin-top:clamp(30px,3.4vw,50px)}
.bf-note{border-radius:var(--rund);background:rgba(255,255,255,.05);padding:clamp(26px,2.8vw,40px);text-align:center;box-shadow:inset 0 1px 0 rgba(255,255,255,.07)}
.bf-note>b{font-family:var(--serif);font-weight:500;font-size:clamp(64px,7vw,104px);line-height:1;color:var(--gold)}
.bf-note>small{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:rgba(253,250,244,.6);margin-top:6px}
.bf-note h3{font-family:var(--serif);font-weight:500;font-size:24px;margin:16px 0 4px;color:var(--weiss)}
.bf-note p{margin:0;font-size:12px;letter-spacing:.05em;color:rgba(253,250,244,.6)}
.bf-platten--hell .bf-platte{background:rgba(246,241,231,.95)}
.bf-offen{margin-top:clamp(24px,2.6vw,38px);background:var(--papier);color:var(--tinte);border-radius:var(--rund);padding:clamp(22px,2.4vw,34px) clamp(24px,2.6vw,38px);border-left:5px solid var(--rot);text-align:left}
.bf-offen h3{font-family:var(--serif);font-weight:500;font-size:24px;margin:0 0 10px;color:var(--rot)}
.bf-offen ul{margin:0;padding-left:1.1em}
.bf-offen li{line-height:1.55;margin:8px 0}
.bf-offen li b{font-weight:500;color:var(--rot)}
.bf-offen li small{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:var(--taupe)}
.schluss .bf-platten{text-align:left}
.bf-zeilen--hell .bf-z{background:var(--weiss);box-shadow:inset 0 2px 10px rgba(21,32,46,.06)}
.bf-zeilen--hell .bf-z b{color:var(--navy)}
.bf-zeilen--hell .bf-z p{color:var(--tinte)}
.bf-zeilen--hell .bf-z small{color:var(--taupe)}
.bf-vgl{margin-top:clamp(24px,2.6vw,38px);border-radius:var(--rund);overflow:hidden;background:var(--navy);color:var(--weiss)}
.bf-vgl__k,.bf-vgl__z{display:grid;grid-template-columns:1fr 1fr}
.bf-vgl__k span{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);padding:18px 24px 10px}
.bf-vgl__z p{margin:0;padding:14px 24px;border-top:1px solid rgba(255,255,255,.08);line-height:1.55}
.bf-vgl__z p:first-child{color:rgba(253,250,244,.62)}
.bf-vgl__z p:last-child{background:rgba(207,162,108,.10)}
@media (max-width:560px){.bf-vgl__z p,.bf-vgl__k span{padding:12px 14px;font-size:14px}}
@media (max-width:900px){
 .bf-auftakt__in,.bf-zwei,.bf-zeilen,.bf-platten,.bf-noten{grid-template-columns:1fr}
 .bf-fehlt{grid-template-columns:1fr 1fr}.bf-haeuser{grid-template-columns:1fr 1fr}
 .bf-stapel{min-height:clamp(320px,90vw,520px)}
}
@media (max-width:560px){.bf-fehlt,.bf-haeuser{grid-template-columns:1fr}.bf-fenster__s{right:var(--rand)}}
'''

nav = ''.join(f'<a href="#{a}">{b}</a>' for a, b in (('haus', 'Das Haus'), ('seite', 'Heutige Seite'), ('fehlt', 'Was fehlt'), ('ausmacht', 'Was es ausmacht'), ('familie', 'Familie'), ('noten', 'Noten'), ('zerone', 'Wer dahinter steht'), ('empfehlung', 'Empfehlung')))
seite = f'''<!doctype html>
<html lang="de-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Befund · Hotel Monte-Moro</title>
<meta name="description" content="Station 2 der Kette: Befund zur heutigen Website des Hotel Monte-Moro, Saas-Almagell, mit Empfehlung.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{K.H.FARBEN['nacht']}">
<link rel="preload" href="_bau/werkbank/fonts/{K.H.SCHRIFT['titel'][1]}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="_bau/werkbank/werkbank.css?v={K.v('werkbank.css')}">
<style>{CSS}</style>
</head>
<body class="haus-{K.H.KURZ}">
{K.sprite()}
<div class="gang-linie" aria-hidden="true"></div>
<header class="leiste"><div class="insel">
  <a class="insel__m" href="#oben">{HZ}<span>Befund</span></a>
  <nav aria-label="Abschnitte">{nav}</nav>
  <a class="glanz" href="{HEUTE}" target="_blank" rel="noopener">Heutige Seite{PF}</a>
</div></header>
<main id="oben">
{''.join(T)}
</main>
<footer class="fuss fuss--kurz"><div class="in">
  <div><b>Befund zum Entwurf</b><p>Kette, Station 2, Späher. Interne Arbeitsseite von Robert Reff, Tasty Studios, nicht die offizielle Website des Hauses. Fotos gehören {K.H.RECHTE}</p></div>
  <div class="r mono"><span>Stand 17.10.2026</span></div>
</div></footer>
<script src="_bau/werkbank/werkbank.js?v={K.v('werkbank.js')}"></script>
</body>
</html>
'''
K.gestaltung()
open(os.path.join(PAKET, 'befund.html'), 'w', encoding='utf-8').write(seite)
print('geschrieben', os.path.join(PAKET, 'befund.html'), len(seite))
