#!/usr/bin/env python3
"""Station 06 · Konzepter · Hotel Monte-Moro, Saas-Almagell (Familie Zurbriggen), 17./18.10.2026.

Baut das Konzept-Board (konzept.html) und konzept.json. Bauart wie das bestätigte Board des Castell Son Claret
(_bau/castell-bau.py): Stand der Rivage-Werkbank über marke.css und marke.js des Markenbuchs der Station 05 (bestätigt,
Farbwelt A, Fjalla One, Grat), eigenes nur in konzept.css. Fotos des Hauses aus _quelle/ (grösste Fassung), für das Board
auf 1600 px nach bilder/. Keine Einkerbungen (Robert 18.10.2026): Bildnamen stehen im Foto auf weichem Schatten.
   python3 _bau/bau.py   → konzept.html, konzept.css, konzept.json, bilder/"""
import html, json, os, re, sys

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # _kette/06-konzepter
PROJEKT = os.path.dirname(os.path.dirname(H))
M5 = os.path.join(PROJEKT, '_kette', '05-markenbauer', '_bau')
sys.path.insert(0, M5)
import bau as B    # noqa: E402  Farben, Zeichen, Wortmarke, Ton, eigene Welt (Station 05)
import bau2 as B2  # noqa: E402  Bausteine des Markenbuchs: kopf, zeilen, kn, zeichen, wort

e = html.escape
F = B.F
PF = B2.PF
Q = os.path.join(PROJEKT, '_quelle')
BILDER = os.path.join(H, 'bilder')
MARKE = '../05-markenbauer/marke'
LIVE = {
    'Carlton-Europe': 'https://carlton-europe-entwurf.vercel.app/',
    'Grand Beau-Rivage': 'http://127.0.0.1:8940/',
    'Hotel Seiler au Lac': 'http://localhost:8921/',
    'Waldhotel Doldenhorn': 'https://waldhotel-doldenhorn-entwurf.vercel.app/',
    'Landgasthof Ruedihus': 'https://landgasthof-ruedihus-entwurf.vercel.app/',
    'Berghotel Gasterntal': 'https://berghotel-gasterntal-entwurf.vercel.app/',
    'Salt & Silver': 'https://salt-and-silver-studie.vercel.app/',
    'Tasty Grand Hotel': 'https://tasty-grand-hotel.vercel.app/',
    'Castell Son Claret': '',
}
FUNDUS = 'https://tasty-ui-fundus.vercel.app/'
FUNDUS_B = FUNDUS + 'bereiche.html#hotel-'

# ---------------------------------------------------------------- Fotos: Schlüssel → Datei in _quelle (grösste Fassung)
FOTOS = {
    'fassade-sommer': 'extern/myswitzerland/myswitzerland-00072098_m.jpg',
    'fassade-winter': 'extern/myswitzerland/myswitzerland-00072097_m.jpg',
    'haus-schnee': 'extern/booking/booking-609882154.jpg',
    'balkon': 'website/bilder/aktuel_hotel-monte-moro-saas-almagell-balkon.jpg',
    'gondel': 'extern/booking/booking-609882092.jpg',
    'reception': 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291892278-reception.jpg',
    'fruehstueck': 'extern/tripadvisor/vom-hotel/tripadvisor-2018-02-17-303351039-fruhstucksbuffet.jpg',
    'zimmer-dach': 'extern/booking/booking-28633464.jpg',
    'zimmer': 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291892318-doppelzimmer.jpg',
    'zimmer-rot': 'extern/booking/booking-28199274.jpg',
    'apollo': 'website/bilder/apollo_2.jpg',
    'apollo-haus': 'website/bilder/apollo_1.jpg',
    'arizona': 'website/bilder/arizon_11.jpg',
    'saecke': 'website/bilder/restau_3.jpg',
    'stube': 'website/bilder/restau_restaurant.jpg',
    'stube-weit': 'website/bilder/restau_4.jpg',
    'stube-bar': 'website/bilder/restau_8.jpg',
    'raclettestuebli': 'extern/tripadvisor/vom-hotel/tripadvisor-2017-11-29-291892107-raclettestubli.jpg',
    'raclette': 'extern/myswitzerland/myswitzerland-00072104_m.jpg',
    'spa': 'website/bilder/wellne_wellness.jpg',
    'spa-pool': 'website/bilder/wellne_3.jpg',
    'spa-sauna': 'website/bilder/wellne_2.jpg',
    'sommer': 'website/bilder/sommer_1.jpg',
    'sommer-see': 'website/bilder/ausflu_1.jpg',
    'winter': 'website/bilder/winter_2.jpg',
    'winter-tour': 'website/bilder/winter_4.jpg',
    'winter-dorf': 'website/bilder/winter_1.jpg',
}
KARTE_PDF = os.path.join(Q, 'website', 'pdf', 'speisekarte.pdf')


def quelle(key):
    return '_quelle/' + FOTOS[key]


def bilder_bauen():
    from PIL import Image
    os.makedirs(BILDER, exist_ok=True)
    for key, datei in FOTOS.items():
        ziel = os.path.join(BILDER, key + '.jpg')
        if os.path.exists(ziel):
            continue
        im = Image.open(os.path.join(Q, datei)).convert('RGB')
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(ziel, 'JPEG', quality=84, optimize=True, progressive=True)
    ziel = os.path.join(BILDER, 'karte.jpg')
    if not os.path.exists(ziel):   # die Rösti-Seite der Karte (Seite 4 des PDFs, Stand 18.11.2024)
        os.system(f'pdftoppm -r 110 -png -f 4 -l 4 "{KARTE_PDF}" "{os.path.join(BILDER, "karte")}"')
        roh = [n for n in os.listdir(BILDER) if n.startswith('karte-') and n.endswith('.png')][0]
        im = Image.open(os.path.join(BILDER, roh)).convert('RGB'); im.save(ziel, 'JPEG', quality=86, optimize=True); os.remove(os.path.join(BILDER, roh))


def foto(key):
    return f'bilder/{key}.jpg'


# ---------------------------------------------------------------- Bausteine des Boards
def kachel(key, name, satz='', i=0, lage='50% 50%', kl='k3--karte'):
    return (f'<figure class="k3 {kl}" data-r="feder" style="--i:{i}"><div class="k3__b"><img src="{foto(key)}" alt="{e(name)}" loading="lazy" decoding="async" style="object-position:{lage}">'
            f'<figcaption class="kerbe">{e(name)}</figcaption></div>'
            f'{f"<p class={chr(34)}kb__s{chr(34)}>{satz}</p>" if satz else ""}</figure>')


def grat(farbe):
    return f'<svg class="grat-naht" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT_PFAD}" fill="{farbe}"/></svg>'


FARBE_KLASSE = {'papier': 'var(--papier)', 'creme tapete-h': 'var(--creme)', 'marine tapete': 'var(--marine)'}


def fenster(key, zeilen, unter, lage='50% 50%'):
    z = ''.join(f'<span class="z"><span>{"<em>" + x + "</em>" if i == len(zeilen) - 1 and len(zeilen) > 1 else x}</span></span>' for i, x in enumerate(zeilen))
    return f'''<section class="fenster" aria-label="{e(' '.join(zeilen))}">
  <div class="fenster__f">
    <div class="fenster__b"><img src="{foto(key)}" alt="" decoding="async" style="object-position:{lage}"></div>
    <div class="fenster__t"><p class="fenster__s">{z}</p><p class="fenster__u">{unter}</p></div>
  </div>
</section>'''


def szene(s, nr, flaeche_klasse):
    bilder = ''.join(kachel(k, n, i=i % 3, lage=l) for i, (k, n, l) in enumerate(s['fotos']))
    baust = e(s['baustein']) + (' <em>neu</em>' if s['quelle'] == 'neu' else ' <em>Fundus</em>')
    skizze = f'<div class="sz__z"><b>Skizze</b><p>{e(s["skizze"])}</p></div>' if s.get('skizze') else ''
    bisher = ''.join(f'<li><a href="{e(LIVE.get(h) or "#")}{e(s["bisher_anker"].get(h, "") if LIVE.get(h) else "")}" target="_blank" rel="noopener"><b>{e(h)}</b></a><span>{e(t)}</span></li>' for h, t in s['bisher'].items())
    fl = {'hell': 'Hell (Papier)', 'creme': 'Hell (Fassade)', 'tapete': 'Hell mit Tapete', 'dunkel': 'Nacht mit Tapete', 'foto': 'Foto über die volle Breite'}[s['flaeche']]
    return f'''<section class="ab blatt {flaeche_klasse} sz" id="s-{s['teil']}">
  {grat(FARBE_KLASSE[flaeche_klasse])}
  <div class="in">
    <header class="mk" data-r="kopf">
      <div><p class="mk__kap"><b>Szene {nr:02d} · {e(s['teil'])}</b><i></i></p><h2 class="mk__t">{B2.zeilen(s['titel'])}</h2></div>
      <p class="mk__lead">{e(s['satz'])}{' <span class="vonmir">von mir</span>' if s.get('vonmir') else ''}</p>
    </header>
    <div class="sz__fotos sz__fotos--{min(len(s['fotos']), 4)}" data-g>{bilder}</div>
    <div class="sz__bau" data-g>
      <div data-r style="--i:0"><small>Baustein</small><b>{baust}</b>{skizze}</div>
      <div data-r style="--i:1"><small>Bewegung</small><p>{e(s['bewegung'])}</p></div>
      <div data-r style="--i:2"><small>Fläche</small><p><i class="fl fl--{s['flaeche']}"></i>{e(fl)}</p></div>
      <div data-r style="--i:3"><small>Bilder</small><p>{'<br>'.join(f'<span class="mono">{e(q)}</span>' for q in s['bilder'])}</p></div>
    </div>
    <div class="nb" data-g>
      <div class="nb__a" data-r style="--i:0"><p class="mk__kap"><b>Dieses Haus</b><i></i></p><p class="nb__t">{e(s['unterschied'])}</p></div>
      <div class="nb__b" data-r style="--i:1"><p class="mk__kap"><b>Bisherige Häuser</b><i></i></p><ul class="nb__l">{bisher}</ul></div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- Inhalt: die Geschichte und die Szenen der Startseite
GESCHICHTE = ('Die Startseite rechnet für den Gast, so wie das Haus es tut: Sie beginnt mit der Fassade in der Jahreszeit, in der man bucht, '
              'zeigt auf einem Bon, was alles schon im Preis steckt, misst den Weg zum Lift in Minuten, gibt die Zimmer als Schlüssel vom Brett, '
              'führt am Abend an der Gondel vorbei ins Röstihüs mit seinen elf Röstis, ins Stübli zu Raclette und Fabians Wein, über den kurzen Weg ins Spa nebenan '
              'und hinaus ins Saastal. Hell und direkt am Tag, dunkel wie der Himmel über dem Dorf am Abend; jede Naht ist ein Bergkamm.')

BISHER_AUFTAKT = {
    'Carlton-Europe': 'Türflügel, die sich öffnen; Navy, Gold, Wortmarke mittig über dem Haus; Buchungsleiste unten.',
    'Grand Beau-Rivage': 'Hero mittig über der Aare: Zeichen in Gold über dem Namen, Ortszeile «Interlaken · seit 1874», Buchungsleiste als Platte.',
    'Hotel Seiler au Lac': 'Dunst statt Vorhang, Wortmarke in Gold, Eck-Knöpfe, Seefoto.',
    'Waldhotel Doldenhorn': 'Block unten links, Auszeichnungs-Laufband direkt darunter.',
    'Landgasthof Ruedihus': 'Holzhaus von 1753 als Profil, Satz «Heute Abend Ihr Tisch, heute Nacht Ihr Bett».',
    'Berghotel Gasterntal': 'Hof hinter dem Titel «Herzlich willkommen», Berghütte.',
    'Salt & Silver': 'Hafen bei Nacht, Vorhang mit Zeichen, Antonio-Versalien, Kursblatt.',
    'Castell Son Claret': 'Das Tor im Mittag, der Name steht in der Toröffnung auf dem Weg.',
}
ANKER_START = {h: 'index.html#oben' for h in BISHER_AUFTAKT}
ANKER_START.update({'Carlton-Europe': '#oben', 'Waldhotel Doldenhorn': '#ankunft', 'Landgasthof Ruedihus': '#ankunft', 'Berghotel Gasterntal': '#ankunft', 'Salt & Silver': '#'})

INKLUSIVE = ['Benutzung Postautos im ganzen Saastal (Sommer/Winter)', 'Benutzung aller Bergbahnen im Saastal (ohne Metro Alpin) (Sommer)', 'ZF und HP: Frühstücksbuffet',
             'Halbpension: wöchentlicher Racletteabend', 'Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr', 'Hotelparkplatz']

SZENEN = [
    dict(teil='auftakt', titel=['Mehr erleben,', 'weniger zahlen.'],
         satz='«Mehr erleben, weniger zahlen. Gratis an- und abreisen.»',
         fotos=[('fassade-sommer', 'Das Haus im Sommer', '50% 40%'), ('fassade-winter', 'Das Haus im Winter', '50% 45%')],
         bilder=[quelle('fassade-sommer'), quelle('fassade-winter')],
         baustein='Auftakt «Das Haus in seiner Jahreszeit»', quelle='neu',
         skizze='Die Fassade über die volle Breite, ein Bildschirm hoch: von Mai bis Oktober das Sommerfoto, ab November das Winterfoto (beide vom Haus, Schweiz Tourismus, 3734 px); der Stichtag kommt aus der Werkbank, damit im Winter nie mehr der Sommer begrüsst (Potentialanalyse, Punkt 01). Die Wortmarke in Papier steht im Himmel über dem Dach, nie über den Balkonen. Darunter die Ortszeile «Saas-Almagell · Saastal · Wallis» und der Satz des Hauses. Unten die Buchungsleiste als helle Platte mit Kuhlen (Anreise, Abreise, Personen), sie übergibt an das Buchungsfenster von seekda. Die Fläche endet unten nicht gerade, sondern als Grat.',
         bewegung='Die Wortmarke rollt aus dem Schlitz, Ortszeile und Satz kommen gestaffelt, die Platte schwebt von unten; der Grat am unteren Rand zieht sich einmal von links nach rechts. Kein Vorhang, keine Tür, kein Film.',
         flaeche='foto',
         unterschied='Das Haus in der Jahreszeit, in der man bucht: Sommer oder Winter nach Stichtag, die Wortmarke im Himmel, die Fläche endet als Bergkamm. Kein Tor, keine Tür, kein Dunst, keine Nacht.',
         bisher=BISHER_AUFTAKT, bisher_anker=ANKER_START),
    dict(teil='inbegriffen', titel=['Was im Preis', 'schon drin ist.'],
         satz='«Bergbahnen und Postautos im Sommer und Herbst ab der 1. Übernachtung inklusive!»',
         fotos=[('gondel', 'Die Gondel vor dem Haus', '50% 50%'), ('fruehstueck', 'Das Frühstücksbuffet', '50% 50%'), ('raclette', 'Raclette, einmal die Woche', '75% 50%')],
         bilder=[quelle('gondel'), quelle('fruehstueck'), quelle('raclette'), '_quelle/website/text/de__hotel__preise.html.md («Inklusive»)', '_quelle/website/text/de.md (Gratis-Anreise, Bedingungen)'],
         baustein='Der Bon', quelle='neu',
         skizze='Eine Quittung auf Papier, oben und unten mit gezackter Abrisskante wie der Grat, daneben drei Fotos. Kopfzeile: «Zimmer mit Frühstück ab CHF 90.00 pro Person / Tag (Budgetzimmer)». Darunter die Zeilen wörtlich aus der Preisliste «Inklusive»: ' + ' · '.join(INKLUSIVE) + '; dazu «An- und Abreise mit dem öffentlichen Verkehr (ab 2 Nächten) geschenkt!» mit den Bedingungen des Hauses (Wohnsitz Schweiz, direkt gebucht, Zeitraum 1. Mai bis 31. Oktober 2026). Rechts steht je Zeile «inklusive» statt eines Preises. Unten ein Stempel mit dem Satz des Hauses und der Knopf «Zimmer buchen». Aktionen haben ein Datum und laufen über die Werkbank ab.',
         bewegung='Der Bon schiebt sich wie aus der Kasse von oben heraus, die Zeilen erscheinen nacheinander mit Haken. Nur der Bon bewegt sich, die Fotos stehen.',
         flaeche='tapete',
         unterschied='Kein bisheriges Haus zeigt, was im Preis steckt. Beim Monte-Moro ist das der tragende Baustein: eine Quittung, auf der alles «inklusive» steht. Das Haus rechnet für seine Gäste, die Seite rechnet mit.',
         bisher={'Carlton-Europe': '«Das Vintage Hotel» mit Fotos, danach «Zwei Häuser, ein Hotel» auf Creme.', 'Grand Beau-Rivage': '«Halle»: dunkler Abschnitt, Rundgang durch die Räume.',
                 'Hotel Seiler au Lac': '«Zuerst, was Sie bekommen» als Angebote auf Nacht.', 'Waldhotel Doldenhorn': '«Herzlich willkommen», dann die Wahl «Worauf freuen Sie sich?».',
                 'Landgasthof Ruedihus': '«Das Ruedihus, unsere Dependance», dann «Was führt Sie zu uns?».', 'Castell Son Claret': 'Der Plan des Guts als Infografik.'},
         bisher_anker={'Carlton-Europe': '#willkommen', 'Grand Beau-Rivage': '#halle', 'Hotel Seiler au Lac': '#angebote', 'Waldhotel Doldenhorn': '#willkommen', 'Landgasthof Ruedihus': '#ankommen'}),
    dict(teil='lage', titel=['Zwei Minuten', 'bis zum Lift.'],
         satz='«2 Gehminuten vom Skigebiet Saas-Almagell · 3 Gehminuten von der Busstation · 3 Gehminuten zum Dorfkern»',
         fotos=[('winter-dorf', 'Saas-Almagell im Winter', '50% 50%'), ('winter', 'Winter im Saastal', '50% 50%')],
         bilder=[quelle('winter-dorf'), quelle('winter'), '_quelle/website/text/de.md («Zentrale Lage»)'],
         baustein='Die Gehminuten-Linie', quelle='neu',
         skizze='Eine Linie vom Haus nach rechts, flach gezogen wie der Grat, mit drei Halten: Skigebiet 2 · Busstation 3 · Dorfkern 3, die Minuten gross in Fjalla One. Unter jedem Halt der Zusatz des Hauses in kleiner Schrift («Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee», «Einkaufsmöglichkeiten, Bankomat, Tourismusbüro usw.»). Dahinter das Dorf im Winter. Am Handy steht die Linie senkrecht.',
         bewegung='Die Linie zieht sich von links nach rechts (scaleX), die drei Halte springen nacheinander auf. Die Zahlen zählen nicht hoch.',
         flaeche='hell',
         unterschied='Keine Karte und kein Plan: Die Lage ist ein Weg in Minuten, so wie das Haus sie selbst angibt.',
         bisher={'Castell Son Claret': 'Plan des Guts, Orte als Wörter am Plan.', 'Landgasthof Ruedihus': 'Kompass der Herkunft (Lieferanten) als Infografik.',
                 'Hotel Seiler au Lac': 'Fahrplan-Tafel «Vor der Tür» auf Holz.', 'Carlton-Europe': 'Schluss mit Karte.'},
         bisher_anker={'Landgasthof Ruedihus': '#rund', 'Hotel Seiler au Lac': '#tuer', 'Carlton-Europe': '#pakete'}),
    dict(teil='fenster-sonne', titel=['Fenster', 'Bei uns scheint', 'fast immer die Sonne.'],
         satz='Restaurant Röstihüs, monte-moro.ch.',
         fotos=[('balkon', 'Blick vom Balkon ins Tal', '50% 50%')],
         bilder=[quelle('balkon')],
         baustein='Fenster', quelle='fundus',
         bewegung='Das Bild steht, die Seite zieht darüber, der Satz rollt zeilenweise herein. Erstes von zwei Fenstern, der Wendepunkt vom Ankommen zum Wohnen.',
         flaeche='foto',
         unterschied='Der Satz kommt vom Haus selbst (Restaurantseite), das Bild vom eigenen Balkon. Zwei Fenster je Startseite: Sonne am Tag, Gondel am Abend.',
         bisher={'Grand Beau-Rivage': 'Fünf Fenster, das erste «Ankommen mit Stil» nach der Halle.', 'Carlton-Europe': 'Erstes Fenster «Was bedeutet Vintage?».', 'Castell Son Claret': 'Drei Fenster: Galatzó, Allee bei Nacht, Konzert.'},
         bisher_anker={'Grand Beau-Rivage': '#zimmer', 'Carlton-Europe': '#zimmer'}),
    dict(teil='zimmer', titel=['Schöne Hotelzimmer,', 'schöne Ferien.'],
         satz='«Schöne Hotelzimmer - schöne Ferien»',
         fotos=[('reception', 'Das Schlüsselbrett an der Rezeption', '80% 40%'), ('zimmer-dach', 'Zimmer unter dem Dach', '50% 50%'), ('apollo', 'Haus Apollo', '50% 50%'), ('arizona', 'Haus Arizona', '50% 50%')],
         bilder=[quelle('reception'), quelle('zimmer-dach'), quelle('zimmer'), quelle('apollo'), quelle('arizona'), '_quelle/website/text/de__hotel__zimmer.html.md', '_quelle/website/text/de__hotel__preise.html.md'],
         baustein='Das Schlüsselbrett', quelle='neu',
         skizze='Das Schlüsselbrett der Rezeption als Bedienelement: je Wohnart ein Schlüssel mit Anhänger in Fjalla One: Budgetzimmer · Standardzimmer · Familienzimmer (3 bis 6 Personen) · Residence Alpenhof (4 Gehminuten) · Haus Apollo · Haus Arizona. Wer einen Schlüssel nimmt, sieht daneben die grosse Kachel: Foto, Text des Hauses, Preis wo belegt (Budgetzimmer CHF 90.00, Standardzimmer CHF 100.00 pro Person und Tag mit Frühstück; Halbpension CHF 120.00 und 130.00), Grösse wo belegt (Doppelzimmer 18 m² im Buchungsfenster), Knopf in die richtige Kategorie bei seekda. Erweiterung (Robert 18.10.2026): Zimmer-Finder im Buchen-Fenster: drei Fragen (wie viele, wann, was ist wichtig), danach das passende Zimmer mit dem echten Preis für genau diese Tage aus seekda (Zugang offen; ohne Zugang zeigt der Finder die passenden Zimmer und den Weg zur Buchung). Die Ferienwohnungen Apollo und Arizona stehen im Vergleich nebeneinander (Zimmerzahl, Balkon, Ausstattung) mit Anfragefenster im Hausstil (Preise und Grössen offen). Beim Öffnen hängt der Standardzimmer-Schlüssel schon in der Hand.',
         bewegung='Der gewählte Schlüssel hebt sich und schwingt einmal um seine Öse aus (rotate), die Kachel kommt deckend von unten, das Foto zoomt in seinen Rahmen.',
         flaeche='creme',
         unterschied='Zimmer und Ferienwohnungen als Schlüssel am Brett der eigenen Rezeption, gleichrangig nebeneinander, nicht als Kachelreihe, Bildwand oder Polaroids.',
         bisher={'Grand Beau-Rivage': 'Reihe von 3D-Kacheln je Kategorie mit Namensfeld.', 'Carlton-Europe': 'Kacheln «Süsse Träume», danach das Kissen-Band.',
                 'Waldhotel Doldenhorn': 'Helle Kacheln von Economy bis Junior Suite.', 'Landgasthof Ruedihus': 'Gerahmte Fotos mit den Namen der Stuben.',
                 'Berghotel Gasterntal': 'Polaroids paarweise, nach dem Fenster «Die Zimmer».', 'Castell Son Claret': 'Bildwand der Häuser mit Fach (Zimmer nach Orten).'},
         bisher_anker={'Grand Beau-Rivage': '#zimmer', 'Carlton-Europe': '#zimmer', 'Waldhotel Doldenhorn': '#zimmer', 'Landgasthof Ruedihus': '#zimmer', 'Berghotel Gasterntal': '#zimmer'}),
    dict(teil='kinder', titel=['Von halb fünf bis neun:', 'der Kidsclub.'],
         satz='«Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr» (Preisliste, «Inklusive»)',
         fotos=[('zimmer-rot', 'Ein Zimmer im Haus', '50% 50%'), ('fruehstueck', 'Das Frühstücksbuffet', '50% 50%')],
         bilder=[quelle('zimmer-rot'), quelle('fruehstueck'), '_quelle/website/text/de__hotel__preise.html.md («Inklusive», «Kinderzuschläge»)', '_quelle/website/text/de__hotel__zimmer.html.md (Familienzimmer)'],
         baustein='Familien-Platte: Kidsclub, Familienzimmer, Kinder im Zimmer der Eltern', quelle='neu',
         skizze='Ein eigener Platz für Familien (Erweiterung, Robert 18.10.2026: «yes hinzufügen alles»): Links gross die Uhrzeit des Kidsclubs, Mo bis Sa 16:30 bis 21:00 Uhr, inklusive. Rechts die Familienzimmer und Familienkombinationen für 3 bis 6 Personen und die Kinderzuschläge im Zimmer der Eltern wörtlich aus der Preisliste (pro Kind und Tag inklusiv Halbpension: bis 5 Jahre 50.00, 6 Jahre 60.00, 7 Jahre 70.00, 8 Jahre 80.00, 9 - 16 Jahre 90.00 CHF), Knopf «Familienzimmer anfragen». Fotos vom Kidsclub: offen (keine im Material); bis dahin trägt das Bild eines Zimmers.',
         bewegung='Die Uhrzeit steht still, die zwei Platten kommen nebeneinander deckend von unten, die Fotos zoomen in ihren Rahmen.',
         flaeche='hell',
         unterschied='Familien bekommen einen eigenen Platz mit Uhrzeit und Kinderpreisen, nicht nur ein Wort im Kleingedruckten.',
         bisher={'Carlton-Europe': 'Familien kommen in den Zimmer-Kacheln vor, kein eigener Abschnitt.', 'Grand Beau-Rivage': 'Kein Familienabschnitt auf der Startseite.',
                 'Waldhotel Doldenhorn': 'Familienzimmer als Kachel unter den Zimmern.', 'Castell Son Claret': 'Haus ohne Kinderangebot auf der Startseite.'},
         bisher_anker={'Carlton-Europe': '#zimmer', 'Waldhotel Doldenhorn': '#zimmer'}),
    dict(teil='fenster-gondel', titel=['Fenster', 'Der Abend', 'vor dem Haus.'],
         satz='«Es lebe die Tradition!»',
         fotos=[('gondel', 'Die geschmückte Gondel am Haus', '50% 45%')],
         bilder=[quelle('gondel')],
         baustein='Fenster', quelle='fundus',
         bewegung='Wie das erste Fenster. Hier wird die Seite zum ersten Mal dunkel; dahinter liegt das Röstihüs.',
         flaeche='foto',
         unterschied='Das zweite Fenster ist die Naht vom Tag zum Abend: die Gondel mit den Lichtern vor der Tür, nicht ein Saal oder eine Allee.',
         bisher={'Grand Beau-Rivage': '«Während das Kaminfeuer knistert» vor den Restaurants.', 'Castell Son Claret': 'Die Allee bei Nacht vor Sa Clastra.'},
         bisher_anker={'Grand Beau-Rivage': '#tafel'}),
    dict(teil='roestihues', titel=['Elf Röstis,', 'jede mit Namen.'],
         satz='«Im hauseigenen Restaurant Röstihüs verwöhnen wir Sie gerne mit Schweizer Spezialitäten, die mit Liebe, Herz und den besten regionalen Produkten zubereitet werden.»',
         fotos=[('karte', 'Die Rösti-Seite der Karte', '50% 0%'), ('saecke', 'Die Säcke vor dem Röstihüs', '50% 30%'), ('stube', 'Die Stube', '50% 50%')],
         bilder=['_quelle/website/pdf/speisekarte.pdf (Seite 4, Stand 18.11.2024)', quelle('saecke'), quelle('stube'), quelle('stube-weit')],
         baustein='Karte auf Papier, Laufzeile der Röstis', quelle='fundus',
         skizze='Auf Nacht mit Tapete liegt die Rösti-Seite als Blatt Papier, gesetzt aus der Karte vom 18.11.2024: elf Röstis mit Zutaten und Preis (Rösti Albert Fr. 25.– bis Rösti Indian Style Fr. 32.–), die Zahl kommt aus der Karte, nicht von der heutigen Startseite. Daneben die Säcke vor der Tür und die Stube. Unten läuft die Zeile mit den Namen: Albert · Dracula · Macugnaga · Exotic Palma · Tschug Tschug · Gartu · Saastal · Diavolo · Schmugglerrösti · Olma · Indian Style. Knöpfe «Tisch reservieren» und «Die ganze Karte». Erweiterung (Robert 18.10.2026): Der Tisch wird in einem Fenster im Stil des Hauses reserviert, mit der Karte daneben (elf Röstis, fünf Cordon Bleus), statt im fremden Fenster von TheFork; Telefon bleibt. Öffnungszeiten und Ruhetage: offen.',
         bewegung='Das Blatt kommt leicht gedreht von unten und legt sich gerade, die Fotos zoomen in ihren Rahmen, die Laufzeile läuft ruhig.',
         flaeche='dunkel',
         unterschied='Die Startseite zeigt eine echte Karte mit Preisen statt Restaurant-Kacheln, und die Namen der Röstis sind der Takt des Abschnitts.',
         bisher={'Grand Beau-Rivage': '«Restaurants & Bar» als Kacheln auf Papier.', 'Carlton-Europe': '«Im Haus» dunkel, Wechsel hell/dunkel über drei Abschnitte.',
                 'Waldhotel Doldenhorn': '«Gemeinsam geniessen und verweilen» dunkel mit Tannen.', 'Landgasthof Ruedihus': '«Kommen Sie herein»: Stuben, Rahmen hängen sich auf.',
                 'Berghotel Gasterntal': 'Karte als Laube.', 'Castell Son Claret': 'Sa Clastra mit der Windrose als bewegtem Element.'},
         bisher_anker={'Grand Beau-Rivage': '#tafel', 'Carlton-Europe': '#im-haus', 'Waldhotel Doldenhorn': '#kueche', 'Landgasthof Ruedihus': '#stuben', 'Berghotel Gasterntal': '#karte'}),
    dict(teil='stuebli', titel=['Raclette im Stübli,', 'Wein von Fabian.'],
         satz='«Hotelwein» Cuvee Special, Fils Maye, Prestige Silber «(wurde von Fabian selber kreiert)», laut Weinkarte des Hauses.',
         fotos=[('raclettestuebli', 'Das Raclettestübli', '75% 50%'), ('raclette', 'Raclette', '75% 50%'), ('stube-bar', 'Die Bar des Röstihüs', '50% 50%')],
         bilder=[quelle('raclettestuebli'), quelle('raclette'), quelle('stube-bar'), '_quelle/website/pdf/speisekarte.pdf (Weinkarte, Nr. 7 und 8)', '_quelle/website/text/de__restaurant.html.md (Spritz)'],
         baustein='Bildgruppe (1 gross, 2 klein) mit Weinkarten-Zeile', quelle='fundus',
         skizze='Das Raclettestübli mit den Butzenscheiben gross, daneben Raclette und die Bar. Darunter zwei Zeilen wie in der Weinkarte: die zwei Hotelweine (Cuvee Special und Cuvee Special Eichenfass, Fils Maye), dazu Zurbriggen Spritz und Antrona Spritz mit den Zutaten des Hauses. Ein Satz zum wöchentlichen Racletteabend für Halbpensionsgäste. Erweiterung (Robert 18.10.2026): «Fabians Hauswein»: Neben den zwei Cuvees auf Wunsch sein Lied «Wallis Baby» (Kanal Fabian Zurbriggen, mit Szenen im Röstihüs) als Film im Bild mit Start per Klick, nie als Hintergrund, und nur mit Fabians Ja (offen).',
         bewegung='Die Gruppe schwebt als Einheit herauf, das grosse Bild zoomt in seinen Rahmen, die Zeilen kommen nacheinander.',
         flaeche='tapete',
         unterschied='Wein als Geschichte des Gastgebers (Fabian kreiert die Hotelweine) und Raclette als Abend des Hauses, nicht Weinkeller, Bar-Kachel oder Kursblatt.',
         bisher={'Carlton-Europe': 'Weinkeller als eigene Welt.', 'Grand Beau-Rivage': 'Bar als Kachel unter «Restaurants & Bar».', 'Castell Son Claret': 'Castell Bar im Kutscherhaus als Kachel unter Olivera.',
                 'Salt & Silver': 'Kursblatt mit Fahrt.'},
         bisher_anker={'Carlton-Europe': '#im-haus', 'Grand Beau-Rivage': '#tafel'}),
    dict(teil='spa', titel=['Das Spa', 'gleich nebenan.'],
         satz='«Erleben Sie Entspannung pur im ausgezeichneten Spa vom Hotel Pirmin Zurbriggen****S.»',
         fotos=[('spa', 'Ruheraum im Partnerhotel', '50% 50%'), ('spa-pool', 'Schwimmbad im Partnerhotel', '75% 50%'), ('spa-sauna', 'Sauna im Partnerhotel', '50% 50%')],
         bilder=[quelle('spa'), quelle('spa-pool'), quelle('spa-sauna'), '_quelle/website/text/de__hotel__wellness.html.md'],
         baustein='Platte und Kuhle', quelle='fundus',
         skizze='Eine helle Platte auf Nacht: links das Monte-Moro, rechts das Wellness & Spa Pirmin Zurbriggen, dazwischen der Weg. In der Kuhle die Tarife für Hotelgäste wörtlich: CHF 25.00 pro Person und Eintritt, 7 Tage Abo CHF 150.00 pro Person; Bademantel, Schuhe, Handtücher stehen zur Verfügung. Keine Grösse des Spas (drei Angaben auf der heutigen Seite). Knopf «Zum Spa nebenan» auf die Seite des Partnerhotels.',
         bewegung='Die Platte schwebt deckend von unten, die drei Fotos kommen gestaffelt und zoomen in ihren Rahmen.',
         flaeche='dunkel',
         unterschied='Das Spa gehört dem Familienhaus nebenan: Die Seite zeigt den Weg und den Preis für Hotelgäste, keine eigene Wellness-Welt.',
         bisher={'Grand Beau-Rivage': '«Bad» als Wand-Abschnitt auf Nacht.', 'Carlton-Europe': '«Wellness-Park» hell.', 'Waldhotel Doldenhorn': '«Anspannung lösen» auf Stahlblau.',
                 'Berghotel Gasterntal': '«Sauna in der alten Käserei».', 'Castell Son Claret': 'Das Wasser des Guts als Band zum Blättern.'},
         bisher_anker={'Grand Beau-Rivage': '#bad', 'Carlton-Europe': '#wellness-park', 'Waldhotel Doldenhorn': '#spa', 'Berghotel Gasterntal': '#sauna'}),
    dict(teil='saastal', titel=['Im Sommer', 'ein herrliches Wanderparadies.'],
         satz='«Im Sommer ein herrliches Wanderparadies. Ueber 250 km Wanderwege …» (Seite «Aktivitäten im Sommer»)',
         fotos=[('sommer', 'Saastal im Sommer', '50% 50%'), ('sommer-see', 'Von der Seite «Ausflüge»', '50% 50%'), ('winter-tour', 'Skitour', '50% 50%')],
         bilder=[quelle('sommer'), quelle('sommer-see'), quelle('winter'), quelle('winter-tour'), '_quelle/website/text/de__region__sommer.html.md', '_quelle/website/text/de__region__winter.html.md', '_quelle/website/text/de__region__ausfluege.html.md'],
         baustein='Band zum Blättern', quelle='fundus',
         skizze='Hohe Karten je Aktivität und Ausflug aus den Seiten Sommer, Winter und Ausflüge des Hauses (Wandern, Alpin Gorge, Winterwanderwege, Schneeschuhlaufen, Mattmark, Saas-Fee mit Metro Alpin, Zermatt, Glacier-Express …). Auf jeder Karte ein kleiner Vermerk aus dem Bon, ob Postauto oder Bergbahn inbegriffen sind (Metro Alpin: offen). Umschalter Sommer · Winter oben, voreingestellt nach dem Stichtag des Auftakts.',
         bewegung='Nativer Seitwärts-Scroll mit Pfeilen und Laufbalken, die Karten schweben beim ersten Hereinkommen gestaffelt von unten.',
         flaeche='hell',
         unterschied='Die Region wird vom Inbegriffenen her erzählt: Jede Karte sagt, ob die Fahrt schon bezahlt ist. Sommer und Winter folgen dem Stichtag.',
         bisher={'Castell Son Claret': 'Das Wasser als Band; die Region nur auf der Unterseite als Kacheln.', 'Grand Beau-Rivage': 'Band zum Blättern für die Angebote.',
                 'Carlton-Europe': 'Band für die Kissen.', 'Berghotel Gasterntal': '«Was Sie hier nicht finden».'},
         bisher_anker={'Grand Beau-Rivage': '#angebote', 'Carlton-Europe': '#zimmer'}),
    dict(teil='gaeste', titel=['Was Gäste', 'am Haus schätzen.'],
         satz='Google 4,5 von 5 aus 121 Bewertungen · Booking.com 8,3 von 10 aus 94, Personal 9,0 und Lage 9,0 · Stand 17.10.2026.',
         fotos=[('reception', 'Die Rezeption', '40% 50%')],
         bilder=[quelle('reception'), '_kette/02-spaeher/befund.md («Noten»)'],
         baustein='Noten als Zeilen auf dem Bon', quelle='neu',
         skizze='Der Bon kommt ein zweites Mal, kurz: Zeilen statt Sterne, «Personal 9,0 · Lage 9,0 · Sauberkeit 8,8 · Google 4,5 von 5», mit Datum. Kein TripAdvisor (3,9, Stand 09.10.). Gästesätze: offen (keine Texte im Material).',
         bewegung='Die Zahlen stehen still, die Zeilen erscheinen nacheinander.',
         flaeche='creme',
         unterschied='Die Noten stehen auf derselben Quittung wie die Leistungen, still und mit Datum.',
         bisher={'Grand Beau-Rivage': 'Noten zählen hoch zwischen Goldlinien.', 'Carlton-Europe': 'Auszeichnungen als vier Felder.', 'Waldhotel Doldenhorn': 'Auszeichnungs-Laufband unter dem Auftakt.',
                 'Landgasthof Ruedihus': '«So sehen es die Gäste» auf Holz.', 'Castell Son Claret': 'Stille Note, drei Siegel und das Team.'},
         bisher_anker={'Grand Beau-Rivage': '#gaeste', 'Carlton-Europe': '#pakete', 'Waldhotel Doldenhorn': '#ankunft', 'Landgasthof Ruedihus': '#gaeste'}),
    dict(teil='gut-zu-wissen', titel=['Gut zu wissen,', 'bevor Sie buchen.'],
         satz='Alles aus der Preisliste an einer Stelle, wörtlich, nichts gerundet.',
         fotos=[('reception', 'Die Rezeption', '40% 50%')],
         bilder=[quelle('reception'), '_quelle/website/text/de__hotel__preise.html.md («Zuschläge»)'],
         baustein='Platte und Kuhle, Zeilen wie auf dem Bon', quelle='fundus',
         skizze='Erweiterung (Robert 18.10.2026): eine helle Platte mit Kuhlen vor der zweiten Buchungsleiste. Zeilen wörtlich aus der Preisliste: Kurtaxen Erwachsene pro Tag (Winter) 4.50, (Sommer) 7.00; Kinder (6 - 16 Jahre) pro Tag (Winter) 2.25, (Sommer) 3.50 · Einzelzimmerzuschlag 50 % · Zuschlag für 1 - 3 Übernachtungen / pro Tag 5.00 · Kinderzuschläge im Zimmer der Eltern · Hund pro Tag ohne Futter 7.00 - 10.00 · Bezahlung in Euro möglich, Rückgeld in Franken · Hotelparkplatz inklusive. Storno- und Geschäftsbedingungen: offen (stehen auf keiner Seite). Dieselben Zeilen stehen im Buchen-Fenster.',
         bewegung='Die Platte schwebt deckend von unten, die Zeilen erscheinen nacheinander.',
         flaeche='creme',
         unterschied='Das Kleingedruckte steht vor dem Buchen gross und an einer Stelle, statt in der Preisliste versteckt.',
         bisher={'Castell Son Claret': '«Gut zu wissen» nur auf der Zimmerseite (Check-in, Check-out).', 'Carlton-Europe': 'Zimmermappe für gebuchte Gäste, keine Konditionen auf der Startseite.',
                 'Grand Beau-Rivage': 'Keine Konditionen auf der Startseite.'},
         bisher_anker={'Carlton-Europe': '#zimmer'}),
    dict(teil='anreise', titel=['Mit dem Zug bis Visp,', 'dann im Postauto.'],
         satz='«Zeitdauer Visp - Saas-Almagell ca. 45 Min.» (Zug und Postauto) · «ca. 40 Min.» (Auto)',
         fotos=[('fassade-winter', 'Das Haus im Winter', '50% 45%')],
         bilder=[quelle('fassade-winter'), '_quelle/website/text/de__hotel__anreise.html.md'],
         baustein='Bild über die volle Breite, zweite Buchungsleiste, Anreise als Platte', quelle='fundus',
         skizze='Das Haus im Winter über die volle Breite, darüber die zweite Buchungsleiste als Platte und daneben die Anreise-Platte: Zug bis Visp, Postauto mit Umsteigen in Saas-Grund (ca. 45 Min.), Auto ab Visp (ca. 40 Min.), dazu die Gratis-Anreise aus dem Bon. Erweiterung (Robert 18.10.2026): «Mit dem Zug anreisen, Ticket inklusive»: für Gäste aus der Schweiz ab zwei Nächten bei direkter Buchung, Zeitraum 1. Mai bis 31. Oktober 2026 (ob es 2027 weiterläuft: offen), mit dem Weg bis vor die Tür und den Verbindungen des Hauses (stündlich bis 20.10 Uhr ab Visp). Adresse: nur «CH-3905 Saas-Almagell» wie im Impressum, die Strasse ist offen.',
         bewegung='Das Bild schwebt herauf, die zwei Platten kommen nebeneinander von unten.',
         flaeche='foto',
         unterschied='Der Bogen schliesst sich über das Jahr: Sommerfassade am Anfang (im Winter umgekehrt), die andere Jahreszeit am Schluss, mit dem Weg hierher statt eines Abschieds.',
         bisher={'Grand Beau-Rivage': '«Herzlich willkommen im Grand Beau-Rivage» als Abschied auf Nacht.', 'Hotel Seiler au Lac': '«Gute Nacht am See».',
                 'Waldhotel Doldenhorn': '«Wir freuen uns, Sie bald willkommen zu heissen».', 'Castell Son Claret': 'Das Castell bei Nacht, zweite Buchungsleiste, Anreise als Platte.'},
         bisher_anker={'Grand Beau-Rivage': '#abschied', 'Hotel Seiler au Lac': '#schluss', 'Waldhotel Doldenhorn': '#buchen'}),
    dict(teil='haus-finder', titel=['Welches Haus der Familie', 'zu Ihnen passt.'],
         satz='Drei Fragen, dann das passende Haus der Familie Zurbriggen.',
         fotos=[('fassade-sommer', 'Hotel Monte-Moro', '50% 40%'), ('spa', 'Wellness & Spa Pirmin Zurbriggen', '50% 50%')],
         bilder=[quelle('fassade-sommer'), quelle('spa'), 'Familie Zurbriggen/erweiterungen/index.html (Preise ab je Haus)'],
         baustein='Haus-Finder der Familie', quelle='neu',
         skizze='Erweiterung für alle drei Häuser (Robert 18.10.2026): drei Fragen als Auswahl im Hausstil: Mit wem kommen Sie? · Was ist Ihnen wichtig (Preis, Spa, Gourmet)? · Saastal oder Zermatt? Danach eine Karte mit dem passenden Haus der Familie, Foto, Preis ab wie belegt (Monte-Moro CHF 90.00 mit Frühstück, Wellness & Spa CHF 175 mit Halbpension, Suitenhotel Zermatt Suiten von 23 bis 145 m²) und Knopf «Zum Haus». Der Gast bleibt in der Familie, statt zu einem Portal zu wechseln. Derselbe Finder steht auf den Seiten aller drei Häuser, je in deren Kleid.',
         bewegung='Die Fragen erscheinen nacheinander, die Antwortkarte kommt deckend von unten. Nur ein Element bewegt sich.',
         flaeche='tapete',
         unterschied='Kein bisheriges Haus führt den Gast zu einem anderen Haus derselben Familie, das zu ihm besser passt.',
         bisher={'Waldhotel Doldenhorn': 'Die Häuser der Familie Maeder nur als Karten im Fuss.', 'Carlton-Europe': '«Wofür kommen Sie?» als Wahl innerhalb des eigenen Hauses.',
                 'Grand Beau-Rivage': 'Seiler au Lac als Karte im Fuss.'},
         bisher_anker={'Waldhotel Doldenhorn': '#buchen', 'Carlton-Europe': '#anlass', 'Grand Beau-Rivage': '#abschied'}),
    dict(teil='fuss', titel=['Der Fuss', 'der Familie Zurbriggen.'],
         satz='«Hotel Monte-Moro, Esther und Fabian Zurbriggen-Zurbriggen» (Impressum)',
         fotos=[('fassade-sommer', 'Hotel Monte-Moro', '50% 40%'), ('spa', 'Wellness & Spa Pirmin Zurbriggen', '50% 50%')],
         bilder=[quelle('fassade-sommer'), '_kette/02-spaeher/befund.md («Familie und weitere Häuser»)'],
         baustein='Fuss der Hotelfamilie mit Karten', quelle='fundus',
         skizze='Der Satz des Hauses gross, die Wortmarke, darunter die Häuser der Familie als Karten mit Foto und «Zum Haus», nach Gastgebern geordnet: Esther und Fabian (Wellness & Spa Pirmin Zurbriggen, Loft-Suite Hotel, Hotel Monte-Moro), Moni und Pirmin (Suitenhotel Zurbriggen, Zermatt), Heidi und Damian (Chalet Rustica). Aufbau bei allen Häusern der Familie gleich, Farben, Muster und Zeichen je Haus (Master 2.8). Darunter Kontaktfeld, Linkspalten, Rechtstexte, der Verweis auf die neue Familienseite zurbriggen.ch (eigener Auftrag, hier nur der Link) und die Zeile «Designstudie von Tasty Studios, nicht die offizielle Website».',
         bewegung='Ruhig. Die Wortmarke baut sich einmal auf, die Karten kommen gestaffelt.',
         flaeche='dunkel',
         unterschied='Erstes Haus der Familie Zurbriggen in der Kette: Der Fuss legt den gemeinsamen Aufbau für alle Häuser der Familie fest.',
         bisher={'Waldhotel Doldenhorn': 'Fuss der Hotelfamilie Maeder mit vier Häusern als Karten.', 'Grand Beau-Rivage': 'Fuss für zwei Häuser (Seiler au Lac als Karte).', 'Castell Son Claret': 'Fuss mit dem Schwesterhaus The Fontenay als Karte.'},
         bisher_anker={'Waldhotel Doldenhorn': '#buchen', 'Grand Beau-Rivage': '#abschied'}),
]

UNTERSEITEN = [
    ('zimmer.html', 'Zimmer', 'je Sprache 1 Seite, eine Bildreihe und zwei Absätze', 'Seitenkopf mit dem Zimmer unter dem Dach · das Schlüsselbrett gross · je Zimmerart eine Bildgruppe mit Text, Preis aus der Preisliste, Belegung und Grösse, wo belegt · Familienzimmer und Familienkombinationen 3 bis 6 Personen · Residence Alpenhof mit Lage · «Gut zu wissen» (Euro möglich, Rückgeld in Franken) · Knopf in die richtige Kategorie bei seekda', 'Schlüsselbrett (neu) · Bildgruppe · Platte und Kuhle'),
    ('ferienwohnungen.html', 'Ferienwohnungen Apollo und Arizona', '2 Seiten je Sprache, ohne Preis und Anfrage', 'Haus Apollo (4. Stock, Dorfeingang, Südbalkon) und Haus Arizona (4½, 3½ und 2½ Zimmer) im Vergleich nebeneinander (Zimmerzahl, Balkon, Ausstattung; Erweiterung Robert 18.10.2026) · je Wohnung Fotos und Text des Hauses · Anfragefenster im Hausstil direkt auf der Seite (Potentialanalyse Punkt 02) · Preise und Grössen offen', 'Bildgruppe · Anfrage im Hausstil (3a) · Auswahl im Hausstil'),
    ('preise.html', 'Preise', '1 Seite je Sprache, Tabelle', 'Die ganze Preisliste als Bon: Zimmer mit Frühstück und Halbpension, Zuschläge, Kurtaxen, Kinder, Hund, wörtlich und vollständig, nichts gerundet · gross und lesbar am Handy (Potentialanalyse Punkt 04) · Saisonzeiten der Preise: offen', 'Der Bon (neu) · Platte und Kuhle'),
    ('roestihues.html', 'Restaurant Röstihüs', '1 Seite je Sprache + Karte als PDF (deutsch, französisch)', 'Kopf: die Säcke vor der Tür · Tisch reservieren im Hausstil mit der Karte daneben (statt TheFork-Fenster) · die Karte als Daten (Speisen, Röstis, Cordon Bleus, Weine, Getränke) aus dem PDF vom 18.11.2024, eine Quelle für Seite, La Carte und PDF · Hotelweine von Fabian · Spritz des Hauses · Kinderauswahl · Sonnenterrasse · Tisch reservieren (TheFork, Telefon) · Öffnungszeiten: offen', 'Karte auf Papier · Karte als Daten · Bogen-Karte (nur hier)'),
    ('angebote.html', 'Aktuelles und Angebote', '1 Seite «Aktuelles», ohne Datum', 'Gratis-Anreise mit Bedingungen und Zeitraum · Top Winterzauber (CHF 999.00) mit Saison (offen) · jede Aktion mit Datum, läuft über die Werkbank ab (Potentialanalyse Punkt 01)', 'Platte und Kuhle · Der Bon'),
    ('wellness.html', 'Spa im Partnerhotel', '1 Seite je Sprache', 'Der Weg nebenan · Angebot des Spas wörtlich · Tarife für Hotelgäste · Knopf zum Partnerhotel · keine Spa-Grösse (Potentialanalyse Punkt 08)', 'Platte und Kuhle · Bildgruppe'),
    ('saastal.html', 'Saastal: Sommer, Winter, Ausflüge', '3 Seiten je Sprache, Text und Bildreihe', 'Sommer und Winter als Umschalter, Ausflüge als Kacheln mit grossem Foto, je Karte Vermerk Postauto/Bergbahn inbegriffen (Metro Alpin offen) · kein Wetter, kein Schneebericht', 'Band zum Blättern · 3D-Kachel'),
    ('anreise.html', 'Anreise', '1 Seite je Sprache', 'Zug bis Visp, Postauto mit Umsteigen in Saas-Grund (ca. 45 Min.) · Auto (ca. 40 Min.) · Gratis-Anreise · Adresse wie im Impressum, Strasse offen', 'Platte und Kuhle · Gehminuten-Linie'),
    ('vor-ihrer-anreise.html', 'Vor Ihrer Anreise', 'neu (Gäste-Funktion 3a)', 'Für gebuchte Gäste: Ankunftszeit, Tisch im Röstihüs, Spa-Eintritt nebenan, Kidsclub, alles an die Rezeption · Rezeption im Chat', 'Meldeschein-Karte · Rezeption im Chat'),
    ('familien.html', 'Familien', 'neu (Erweiterung, Robert 18.10.2026)', 'Kidsclub Mo bis Sa 16:30 bis 21:00 Uhr · Familienzimmer und Familienkombinationen 3 bis 6 Personen · Kinderzuschläge im Zimmer der Eltern wörtlich · Ferienwohnungen für Familien · Fotos vom Kidsclub offen', 'Familien-Platte (neu) · Bildgruppe'),
    ('kontakt.html', 'Kontakt', '1 Formular je Sprache', 'Telefon, E-Mail, Formular als heller Briefbogen im Hausstil · häufige Fragen', 'Briefbogen · Auswahl im Hausstil'),
    ('buchen.html', 'Buchen', 'seekda eingebettet', 'Das Buchungsfenster von seekda bleibt, die Seite darum im neuen Kleid; kein Weg mehr ins alte Design · davor der Zimmer-Finder mit Live-Preis (Zugang offen) und «Gut zu wissen» (Kurtaxe, Zuschläge, Euro, Parkplatz; Storno offen)', 'Zimmer-Finder (3a) · Platte und Kuhle'),
    ('impressum.html · datenschutz.html', 'Rechtstexte', 'Impressum, Datenschutz (EN und FR deutsch)', 'Wortlaut des Hauses, Kopf übersetzt · AGB, Widerruf und Storno: offen (nirgends gefunden, Potentialanalyse Punkt 09) · 404-Seite mit Wegen zu Zimmern, Röstihüs, Kontakt', 'Blatt rechts, Inhaltsfeld links'),
    ('en/ · fr/', 'Sprachen', 'heute de, en, fr', 'Station 15a: Deutsch, Französisch, Englisch (Booking: 46 deutsch, 29 französisch); jede Seite ganz in jeder Sprache, auch Datenschutz EN/FR (heute deutsch); die Seite öffnet in der Sprache des Browsers; Karte und Rechtstexte in allen Sprachen (Potentialanalyse Punkt 12)', '–'),
]

GESTRICHEN = [
    ('Einkerbungen für Bildnamen, Zahlen oder Gruss', 'Robert 18.10.2026: «Keine Einkerbungen benutzen bei den neuen Projekten.» Bildnamen stehen im Foto auf weichem Schatten.'),
    ('Farbwelt B «Logo-Blau und Butzenglas»', 'Robert hat am 18.10.2026 Welt A «Bergnacht und Lärche» gewählt («Und Farbe A»).'),
    ('Tür, Tor oder Vorhang im Auftakt', 'Robert: kein Vorhang, kein Tor, keine Türflügel. Das Haus steht im Foto.'),
    ('Ein Band mit grossen Zahlen auf der Startseite', 'Carlton, Grand Beau-Rivage und Ruedihus haben es; die Minuten stehen auf der Gehminuten-Linie, die Preise auf dem Bon.'),
    ('Hochzählende Bewertungen', 'Das hat das Grand Beau-Rivage; hier stehen die Noten still auf dem Bon.'),
    ('TripAdvisor-Note', '3,9 von 5, Nr. 8 von 8 in Saas-Almagell (09.10.2026): gehört nicht auf die Seite (Prompt des Hauses).'),
    ('Gäste-Videos von YouTube', 'Nie auf die Seite (Prompt des Hauses). Fabians eigener Film «Wallis Baby» kommt ins Stübli (Robert 18.10.2026), im Bild mit Start per Klick, nie als Hintergrund, nur mit Fabians Ja.'),
    ('Wetter und Schneebericht', 'Robert hat Wetter aus allen Seiten gestrichen; die heutige Unterseite «Wetter / Schneebericht» entfällt.'),
    ('Spa-Grösse in m²', 'Drei verschiedene Angaben auf der heutigen Seite (Potentialanalyse Punkt 08); das Spa wird mit seinem Angebot beschrieben.'),
    ('«12 Röstis und 7 Cordon Bleus» von der heutigen Startseite', 'Die Karte gilt: elf Röstis, fünf Cordon Bleus (Potentialanalyse Punkt 06).'),
    ('Geschichte des Hauses als eigener Abschnitt', 'Nicht belegt (Station 03, offen); nichts dazu erfinden.'),
    ('Eigentum der Resort Monte Moro AG', 'Nicht auf die Seite; die Gastgeber stehen wie im Impressum.'),
    ('«Herzlich willkommen» als zweiter Abschnitt, Wahl «Wofür kommen Sie?»', 'Doldenhorn, Gasterntal, Carlton und Ruedihus haben es. Das Monte-Moro beginnt mit dem Bon.'),
    ('Polaroids, Bühne mit Abzügen, Bildwand mit Fach', 'Salt & Silver, Ruedihus, Gasterntal und Castell haben sie. Das Monte-Moro nimmt das Schlüsselbrett.'),
    ('Ticket / Billett', 'Vorerst nur Carlton und Grand Beau-Rivage (Robert 15.10.2026).'),
]

OFFEN = [
    ('Öffnungszeiten und Ruhetage des Röstihüs stehen nirgends', 'Station 03 › offen; alle 49 Seiten, Schweiz Tourismus, Google'),
    ('Preise und Grössen der Ferienwohnungen Apollo und Arizona fehlen', 'de/ferienwohnungen/apollo.html, arizona.html, Preisliste'),
    ('Saisonzeiten der Preise und Saison der Pauschale «Top Winterzauber» fehlen', 'de/hotel/preise.html, de/hotel/aktuelles.html'),
    ('Zimmergrössen ausser Doppelzimmer (18 m², Buchungsfenster) nicht belegt', 'de/hotel/zimmer.html, seekda'),
    ('Metro Alpin inbegriffen oder nicht: zwei Angaben', 'Preisliste «ohne Metro Alpin» gegen Schweiz Tourismus «auch»'),
    ('Strasse des Hauses: Talstrasse 129, Furusandstrasse 12 oder 10', 'fakten.json › adresse; auf der Seite nur «CH-3905 Saas-Almagell»'),
    ('Herkunft der Region-Fotos (sommer_*, winter_*, ausflu_*) unbekannt: liegen auf der Seite des Hauses, Fotograf nicht genannt', '_quelle/website/herkunft.json'),
    ('Gästesätze für die Szene «Was Gäste schätzen»: keine Bewertungstexte im Material', 'Booking, Google, TripAdvisor nicht als Text abgelesen'),
    ('Fotos der anderen Familienhäuser für den Fuss: aus deren Paketen zu übernehmen (Wellness, Loft-Suite, Zermatt laufen eigene Stationen; Chalet Rustica nicht in der Kette)', '../Familie Zurbriggen/_quelle/'),
    ('AGB, Widerruf und Stornobedingungen nicht vorhanden', 'alle Seiten DE/EN/FR; seekda nicht bis zur Buchung durchgeklickt'),
    ('Fotos vom Kidsclub (Erweiterung): keine im Material', '_quelle/website/bilder, booking, tripadvisor'),
    ('Zugang zu seekda für den Zimmer-Finder mit Live-Preis (Erweiterung)', 'Buchungsfenster de/buchen.html'),
    ('Wohin Anfragen aus der Rezeption im Chat gehen (Erweiterung)', 'vom Haus zu klären'),
    ('Ja von Fabian, dass «Wallis Baby» auf der Seite läuft (Erweiterung)', '_quelle/video/familie/youtube_gbSFcYqELPA_Wallis Baby.mp4'),
    ('Ob die Gratis-Anreise mit dem Zug 2027 weiterläuft (Erweiterung)', 'de.md: Zeitraum 1. Mai bis 31. Oktober 2026'),
    ('Neue Familienseite zurbriggen.ch: eigener Auftrag, Ja der Familie zur Umstellung offen', 'Familie Zurbriggen/erweiterungen/index.html'),
]


# ---------------------------------------------------------------- Erweiterungen (Robert 18.10.2026: «yes hinzufügen alles», Übersicht Familie Zurbriggen/erweiterungen/)
ERWEITERUNGEN = [
    # (für, was, wo im Board, Grundlage, vom Haus offen)
    ('Alle drei Häuser', 'Haus-Finder der Familie', 'Szene «haus-finder» vor dem Fuss', 'Preise ab: Monte-Moro CHF 90 mit Frühstück, Wellness CHF 175 mit Halbpension, Zermatt Suiten 23 bis 145 m²', 'nichts'),
    ('Alle drei Häuser', 'Rezeption im Chat auf jeder Seite', 'auf jeder Seite unten rechts; «Vor Ihrer Anreise»', 'läuft auf vier Maeder-Häusern und Salt & Silver; antwortet aus den Fakten des Hauses in jeder Sprache der Seite', 'wohin Anfragen aus dem Chat gehen'),
    ('Alle drei Häuser', 'Zimmer-Finder mit Live-Preis', 'Szene «zimmer», Unterseite «Buchen»', 'erprobt am Carlton (Master 3a); Buchungssystem seekda', 'Zugang zu seekda; ohne Zugang die passenden Zimmer und der Weg zur Buchung'),
    ('Alle drei Häuser', 'Jede Sprache ganz', 'Sprachen (Station 15a)', 'Datenschutz auf EN und FR heute deutsch; Seite öffnet in der Sprache des Browsers', 'nichts'),
    ('Alle drei Häuser', 'Verweis auf die neue Familienseite zurbriggen.ch', 'Fuss', 'eigener Auftrag, hier nur der Link', 'Ja der Familie zur Umstellung'),
    ('Monte-Moro', 'Kidsclub mit eigenem Platz', 'Szene «kinder», Unterseite «Familien»', 'Preisliste «Inklusive»: Mo bis Sa 16:30 bis 21:00 Uhr; Kinderzuschläge', 'Fotos vom Kidsclub'),
    ('Monte-Moro', '«Gut zu wissen» vor dem Buchen', 'Szene «gut-zu-wissen», Buchen-Fenster', 'Preisliste: Kurtaxen 4.50/7.00, Kinder 2.25/3.50, Einzelzimmer 50 %, 1 - 3 Nächte 5.00 pro Tag, Hund, Euro', 'Storno- und Geschäftsbedingungen'),
    ('Monte-Moro', 'Tisch im Röstihüs im Hausstil reservieren', 'Szene «roestihues», Unterseite «Röstihüs»', 'heute TheFork; Karte DE und FR vom 18.11.2024', 'Öffnungszeiten und Ruhetage'),
    ('Monte-Moro', 'Mit dem Zug anreisen, Ticket inklusive', 'Szene «anreise», Unterseite «Anreise»', 'Gratis-Anreise 1. Mai bis 31. Oktober 2026; Zug bis Visp, Postauto über Saas-Grund', 'ob das Angebot 2027 weiterläuft'),
    ('Monte-Moro', 'Fabians Hauswein mit «Wallis Baby»', 'Szene «stuebli»', 'Weinkarte Nr. 7 und 8; Film auf Fabians eigenem Kanal', 'Ja von Fabian zum Film'),
    ('Monte-Moro', 'Ferienwohnungen im Vergleich', 'Szene «zimmer», Unterseite «Ferienwohnungen»', 'Haus Apollo (4. Stock, Südbalkon), Haus Arizona (2½ bis 4½ Zimmer)', 'Grössen und Preise der Wohnungen'),
]

# ---------------------------------------------------------------- CSS des Boards: Vorlage Castell, Töne dieses Hauses
def css():
    s = open(os.path.join(H, '_bau', 'castell-konzept.css'), encoding='utf-8').read()
    for a, b in (('rgba(87,87,86', 'rgba(10,42,74'), ('rgba(192,160,98', 'rgba(198,113,68'), ('rgba(12,31,65', 'rgba(10,42,74'), ('rgba(138,43,43', 'rgba(155,44,34'),
                 ('#E4DBCC', F['Fassade']), ('#F6F4EE', '#F8F6F3'), ('#ECEAE4', F['Papier']), ('#9B9382', F['Lärche tief']), ('#8a2b2b', '#9b2c22'), ('#0C1F41', F['Nacht'])):
        s = s.replace(a, b)
    s = re.sub(r'/\*[^*]*Castell[^*]*\*/', '', s, count=1)
    s = '/* Konzept-Board Hotel Monte-Moro · Station 06 · eigenes zum Markenbuch (marke.css): Szenen-Reihen, Vergleich nebeneinander. Vorlage: Board Castell Son Claret. */\n' + s
    s += '\n/* Monte-Moro: Fjalla One hat nur eine Stärke */\nhtml{font-synthesis:none}\n'
    open(os.path.join(H, 'konzept.css'), 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- die Seite
def seite():
    flaechen = {'hell': 'papier', 'creme': 'creme tapete-h', 'tapete': 'creme tapete-h', 'dunkel': 'marine tapete', 'foto': 'papier'}
    szenen_html = ''
    nr = 0
    for s in SZENEN:
        nr += 1
        if s['teil'].startswith('fenster'):
            szenen_html += fenster(s['fotos'][0][0], s['titel'][1:], s['satz'] + (' <span class="vonmir">von mir</span>' if s.get('vonmir') else ''), s['fotos'][0][2])
            szenen_html += szene(s, nr, 'papier')
        else:
            szenen_html += szene(s, nr, flaechen[s['flaeche']])
    lauf = ''.join(f'<a href="#s-{s["teil"]}" data-r style="--i:{i}"><i class="fl fl--{s["flaeche"]}"></i><b>{i + 1:02d}</b><span>{e(" ".join(s["titel"][1:] if s["teil"].startswith("fenster") else s["titel"]))}</span></a>' for i, s in enumerate(SZENEN))
    unter_html = ''.join(f'<li data-r style="--i:{i % 4}"><div class="us__k"><b>{e(n)}</b><small class="mono">{e(d)}</small><small>{e(h)}</small></div><div class="us__t"><p>{e(t)}</p><p class="us__b"><span>Bausteine</span> {e(b)}</p></div></li>' for i, (d, n, h, t, b) in enumerate(UNTERSEITEN))
    gestr_html = ''.join(f'<li data-r style="--i:{i % 4}"><b>{e(w)}</b><span>{e(g)}</span></li>' for i, (w, g) in enumerate(GESTRICHEN))
    erw_html = ''.join(f'<li data-r style="--i:{i % 4}"><div class="us__k"><b>{e(w)}</b><small class="mono">{e(f)}</small><small>{e(wo)}</small></div><div class="us__t"><p>{e(g)}</p><p class="us__b"><span>Vom Haus offen</span> {e(o)}</p></div></li>' for i, (f, w, wo, g, o) in enumerate(ERWEITERUNGEN))
    offen_html = ''.join(f'<li data-r style="--i:{i % 4}"><b>{e(p)}</b><span class="mono">{e(w)}</span></li>' for i, (p, w) in enumerate(OFFEN))
    haeuser = ''.join(f'<li style="--i:{i}"><b>{(f"<a href={chr(34)}{e(LIVE[h])}{chr(34)} target={chr(34)}_blank{chr(34)} rel={chr(34)}noopener{chr(34)}>{e(h)}</a>") if LIVE.get(h) else e(h)}</b><span>{e(t)}</span></li>' for i, (h, t) in enumerate(B.EIGENE_WELT['unterschied_zu'].items()))
    v_css = int(os.path.getmtime(os.path.join(H, '..', '05-markenbauer', 'marke', 'marke.css')))
    v_js = int(os.path.getmtime(os.path.join(H, '..', '05-markenbauer', 'marke', 'marke.js')))
    GOLD = '<linearGradient id="tgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3CDB2"/><stop offset=".34" stop-color="#E09A70"/><stop offset=".52" stop-color="#C67144"/><stop offset=".64" stop-color="#8A4626"/><stop offset=".82" stop-color="#D98E62"/><stop offset="1" stop-color="#F1C6A8"/></linearGradient>'
    defs = B.sym_defs().replace('</defs>', GOLD + '</defs>')
    KAP = [('geschichte', 'Geschichte'), ('s-auftakt', 'Startseite'), ('unterseiten', 'Unterseiten'), ('erweiterungen', 'Erweiterungen'), ('nummer10', 'Nummer 10'), ('gestrichen', 'Gestrichen'), ('offen', 'Offen')]
    nav = ''.join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAP)
    index = ''.join(f'<a href="#{k}" data-r style="--i:{i}"><span>{e(n)}</span></a>' for i, (k, n) in enumerate(KAP))
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Konzept-Board · Hotel Monte-Moro</title>
<meta name="description" content="Die Geschichte der neuen Website des Hotel Monte-Moro: jede Szene mit echten Fotos, Baustein, Bewegung, Fläche und dem Unterschied zu allen bisherigen Häusern. Intern, Station 06 der Kette.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['Nacht']}">
<link rel="icon" href="{MARKE}/zeichen/medaillon-blau.svg" type="image/svg+xml">
<link rel="preload" href="{MARKE}/schriften/FjallaOne-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{MARKE}/schriften/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{MARKE}/marke.css?v={v_css}">
<link rel="stylesheet" href="konzept.css?v={int(os.path.getmtime(os.path.join(H, 'konzept.css')))}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{defs}

<nav class="leiste" aria-label="Konzept-Board">
  <a class="leiste__m" href="#oben">{B2.zeichen()}<span><b>Konzept-Board</b><small>Station 06 · Hotel Monte-Moro</small></span></a>
  <div class="leiste__k">{nav}</div>
  <a class="glanz" href="{MARKE}/markenbuch.html" target="_blank" rel="noopener">Markenbuch{PF}</a>
</nav>

<main>
<section class="titel tapete" id="oben">
  <div class="titel__in">
    <p class="titel__kap" data-r="hero" style="--i:0"><i></i><b>Konzept-Board · Oktober 2026 · intern</b><i></i></p>
    <div class="titel__z" data-r="zeichen">{B2.medaillon('', 'url(#tgold)').replace('<svg ', '<svg style="width:clamp(84px,9vw,132px);height:auto" ')}</div>
    <h1 class="titel__w" data-r="maske"><span class="z"><span>{B2.wort().replace('fill="currentColor"', 'fill="#F5F2EE"')}</span></span></h1>
    <p class="titel__ort" data-r="hero" style="--i:2"><span style="white-space:nowrap">Saas-Almagell</span> <span class="raute"></span> was im Preis steckt</p>
    <p class="titel__lead" data-r="hero" style="--i:3">{e(GESCHICHTE)}</p>
    <div class="knr knr--mitte" data-r="hero" style="--i:4">{B2.kn('Die Szenen', '#s-auftakt')}{B2.kn('Markenbuch', MARKE + '/markenbuch.html', 'kn--linie', neu=True)}</div>
  </div>
  <nav class="index" aria-label="Inhalt" data-g>{index}</nav>
  <span class="titel__runter" aria-hidden="true"><i></i></span>
</section>

<section class="ab blatt papier" id="geschichte">
  {grat('var(--papier)')}
  <div class="in">
    {B2.kopf('Die Geschichte', ['Ein Haus, das', 'für seine Gäste rechnet.'], 'Die Startseite erzählt einen Aufenthalt so, wie das Monte-Moro ihn anbietet: Erst sieht man das Haus in seiner Jahreszeit, dann auf einem Bon, was alles schon bezahlt ist, dann wie nah der Lift ist. Man nimmt den Schlüssel vom Brett, geht am Abend an der Gondel vorbei ins Röstihüs, ins Stübli zu Raclette und Fabians Wein, über den kurzen Weg ins Spa nebenan und am nächsten Tag hinaus ins Saastal. Für Familien hat der Kidsclub seinen eigenen Platz, vor dem Buchen steht alles Kleingedruckte an einer Stelle, und ein Haus-Finder führt zum passenden Haus der Familie. Am Schluss der Weg hierher und die Familie. ' + f'{len(SZENEN)} Szenen, zwei Fenster, { {2: "zwei", 3: "drei", 4: "vier"}[sum(1 for x in SZENEN if x["flaeche"] == "dunkel")] } dunkle Flächen; jede Naht ist ein Bergkamm. Farbwelt A «Bergnacht und Lärche», Titel in Fjalla One.')}
    <div class="drei" data-g>
      {kachel('fassade-sommer', 'Tag: das Haus in der Sonne.', 'Hell und direkt, die Wortmarke im Himmel, darunter der Bon.', 0, '50% 40%')}
      {kachel('reception', 'Der Schlüssel vom Brett.', 'Zimmer und Ferienwohnungen gleichrangig, als Schlüssel der eigenen Rezeption.', 1, '80% 40%')}
      {kachel('saecke', 'Abend: das Röstihüs.', 'Die Karte auf Papier, elf Röstis mit Namen, dunkel wie der Himmel über dem Dorf.', 2, '50% 30%')}
    </div>
    <div class="lauf-szenen" data-g>{lauf}</div>
  </div>
</section>

{szenen_html}

<section class="ab blatt creme tapete-h" id="unterseiten">
  {grat('var(--creme)')}
  <div class="in">
    {B2.kopf('Unterseiten', ['Alles, was das Haus', 'heute hat, neu gedacht.'], 'Aus der Seitenliste der Station 02: 49 Seiten in drei Sprachen, je Sprache rund 16. Neu geordnet nach Anliegen, jede Seite mit Seitenkopf, kürzeren Szenen, einem Fenster und Ausklang-Zeile. Das Buchungsfenster von seekda und die Tischreservation bleiben, kein Klick führt mehr ins alte Design. Was fehlt, kommt dazu: Preise lesbar am Handy, Ferienwohnungen mit Anfrage, Vor Ihrer Anreise, 404; AGB und Storno sind offen. Wetter und Schneebericht entfallen.')}
    <ul class="us" data-g>{unter_html}</ul>
  </div>
</section>

<section class="ab blatt papier" id="erweiterungen">
  {grat('var(--papier)')}
  <div class="in">
    {B2.kopf('Erweiterungen', ['Was der Seite', 'mehr Substanz gibt.'], 'Robert hat am 18.10.2026 alle Erweiterungen aus der Übersicht der Familie Zurbriggen freigegeben («yes hinzufügen alles»). Jede steht oben als Szene oder unten als Unterseite; hier je Erweiterung, wo sie sitzt, worauf sie steht und was vom Haus noch fehlt. Was fehlt, bleibt offen, nichts wird dazu erfunden.')}
    <ul class="us" data-g>{erw_html}</ul>
  </div>
</section>

<section class="ab blatt marine tapete" id="nummer10">
  {grat('var(--marine)')}
  <div class="in">
    {B2.kopf('Projekt Nummer 10', ['Womit es sich von jedem', 'bisherigen Haus unterscheidet.'], 'Vor dieser Station wurden die Boards und Startseiten der bisherigen Häuser gelesen (Castell Son Claret aus dem Archiv, UI-Fundus «Bereiche», Abschnittsfolgen). Bei jeder Szene steht oben der Unterschied nebeneinander; hier je Haus in einem Satz, dazu die zwei Häuser der Familie, die parallel laufen. Gleich dürfen Knöpfe, Kacheln, Tapete und Hereinschweben sein; eigen sind Aufbau, Zimmer-Darstellung, tragende Bausteine, Bewegung und Rhythmus.')}
    <ul class="unter" data-g>
      <li style="--i:0"><b>Hotel Monte-Moro</b><span>Ein Haus, das rechnet: Fassade in ihrer Jahreszeit · der Bon mit allem Inbegriffenen · Gehminuten-Linie · Schlüsselbrett für Zimmer und Ferienwohnungen · Gondel am Abend · Karte auf Papier mit elf Röstis · Stübli und Fabians Wein · Spa nebenan als Platte · Saastal vom Inbegriffenen her · Kidsclub mit eigenem Platz · Noten auf dem Bon · «Gut zu wissen» vor dem Buchen · Anreise in der anderen Jahreszeit, Ticket inklusive · Haus-Finder der Familie · Fuss der Familie Zurbriggen. Zwei Fenster, Bergkamm an jeder Naht.</span></li>
      {haeuser}
    </ul>
    <div class="knr knr--mitte" data-r>{B2.kn('UI-Fundus: Hotel bauen', FUNDUS_B + 'auftakt', neu=True)}{B2.kn('Markenbuch, eigene Welt', MARKE + '/markenbuch.html#welt', 'kn--linie', neu=True)}</div>
  </div>
</section>

<section class="ab blatt papier" id="gestrichen">
  {grat('var(--papier)')}
  <div class="in">
    {B2.kopf('Gestrichen', ['Überlegt', 'und verworfen.'], 'Damit kein anderer Chat es wieder aufmacht: Was es auf dieser Website nicht gibt, und warum.')}
    <ul class="gs" data-g>{gestr_html}</ul>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="offen">
  {grat('var(--creme)')}
  <div class="in">
    {B2.kopf('Offen', ['Was nicht belegt ist,', 'bleibt offen.'], f'{len(OFFEN)} Punkte, jeder mit Fundstelle. Sie stehen auch in stand.json und auf der Karte. Dazu gelten weiter die offenen Punkte der Stationen 03 bis 05.')}
    <ul class="gs gs--rot" data-g>{offen_html}</ul>
  </div>
</section>

<section class="ab blatt marine tapete schluss" id="ende">
  {grat('var(--marine)')}
  <div class="in">
    <div class="ende" data-r="ende">
      <span class="strich strich--gross">{B2.zeichen()}</span>
      <p class="ende__w">{B2.wort()}</p>
      <p class="ende__s">Konzept-Board Hotel Monte-Moro · Station 06 der Kette · intern, geht nie an den Kunden · Tasty Studios, Oktober 2026. Nächste Station: der Baumeister baut Szene für Szene, Robert bestätigt je Abschnitt.</p>
      <div class="knr knr--mitte">{B2.kn('Markenbuch', MARKE + '/markenbuch.html', neu=True)}{B2.kn('Die Probe', MARKE + '/probe.html', 'kn--linie', neu=True)}{B2.kn('Potentialanalyse', '../04-analyst/potential/', 'kn--linie', neu=True)}</div>
    </div>
  </div>
</section>
</main>
<script src="{MARKE}/marke.js?v={v_js}" defer></script>
</body>
</html>
'''


def konzept_json():
    seiten = [{'seite': 'index.html', 'titel': 'Startseite: ein Haus, das für seine Gäste rechnet',
               'szenen': [{'teil': s['teil'], 'titel': ' '.join(s['titel']), 'satz': s['satz'] + (' (von mir)' if s.get('vonmir') else ''), 'bilder': s['bilder'], 'baustein': s['baustein'], 'quelle': s['quelle'],
                           'skizze': s.get('skizze', ''), 'bewegung': s['bewegung'], 'flaeche': {'creme': 'hell', 'tapete': 'tapete', 'foto': 'hell'}.get(s['flaeche'], s['flaeche']), 'flaeche_genau': s['flaeche'],
                           'unterschied': s['unterschied'], 'bisher': s['bisher'],
                           'bisher_links': {h: (LIVE.get(h, '') + a) if LIVE.get(h) else '' for h, a in s['bisher_anker'].items()}} for s in SZENEN]}]
    for datei, name, heute, text, bausteine in UNTERSEITEN:
        seiten.append({'seite': datei, 'titel': name, 'heute': heute, 'szenen': [{'teil': re.sub(r'[^a-z0-9]+', '-', datei.split('.')[0].lower()).strip('-') or 'seite', 'titel': name, 'satz': text, 'baustein': bausteine, 'quelle': 'neu' if 'neu' in bausteine else 'fundus'}]})
    return {'haus': 'Hotel Monte-Moro', 'stand': '2026-10-18', 'geschichte': GESCHICHTE, 'farbwelt': 'A «Bergnacht und Lärche» (Robert 18.10.2026)', 'schrift': 'Fjalla One (Robert 18.10.2026)',
            'linie': 'Bergkamm an jeder Naht (Robert 18.10.2026)', 'seiten': seiten,
            'erweiterungen': [{'fuer': f, 'was': w, 'wo': wo, 'grundlage': g, 'vom_haus_offen': o, 'wort': 'Robert 18.10.2026: «yes hinzufügen alles»'} for f, w, wo, g, o in ERWEITERUNGEN],
            'gestrichen': [{'was': w, 'grund': g} for w, g in GESTRICHEN], 'offen': [{'punkt': p, 'wo': w} for p, w in OFFEN], 'familie_machart': None,
            'quellen': ['_kette/02-spaeher/seitenliste.json', '_kette/02-spaeher/befund.md', '_kette/03-sammler/fakten.json', '_kette/04-analyst/potential.json', '_kette/05-markenbauer/marke.json',
                        'Prompt — Hotel Monte-Moro, Saas-Almagell.md (Abschnitt 4)', '_quelle/website/text/de*.md', '_quelle/website/pdf/speisekarte.pdf',
                        '_Archiv/Castell Son Claret/_kette/06-konzepter/konzept.json (bisherige Häuser)']}


if __name__ == '__main__':
    bilder_bauen()
    css()
    open(os.path.join(H, 'konzept.html'), 'w', encoding='utf-8').write(seite())
    json.dump(konzept_json(), open(os.path.join(H, 'konzept.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('gebaut: konzept.html, konzept.css, konzept.json, bilder/')
