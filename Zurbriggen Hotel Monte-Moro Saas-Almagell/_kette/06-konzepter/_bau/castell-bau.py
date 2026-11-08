#!/usr/bin/env python3
"""Station 06 · Konzepter · Castell Son Claret. Baut das Konzept-Board (konzept.html) und konzept.json.

Stand der Rivage-Werkbank (Regel 13.5 Nr. 12): dieselbe Bauart wie das Markenbuch der Station 05 (Vorlage Le Livre des
Grand Beau-Rivage), darum werden marke.css und marke.js des Markenbuchs eingebunden und nicht neu geschrieben; eigenes
liegt nur in konzept.css (Szenen-Reihen, Vergleich nebeneinander). Fotos des Hauses kommen aus _quelle/ (grösste Fassung)
und werden für das Board auf 1600 px verkleinert nach bilder/. Nur transform und opacity, nativer Scroll.
   python3 bau.py   → konzept.html, konzept.css, konzept.json, bilder/"""
import html, json, os, re, sys

H = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(H))
M5 = os.path.join(PROJEKT, '_kette', '05-markenbauer')
sys.path.insert(0, M5)
import bau as B    # noqa: E402  Farben, Zeichen, Wortmarke, Ton, eigene Welt (Station 05)
import bau2 as B2  # noqa: E402  Bausteine des Markenbuchs: kopf, zeilen, kn, zeichen, wort, name

e = html.escape
F = B.F
PF = B2.PF
Q = os.path.join(PROJEKT, '_quelle', 'website', 'bilder')
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
}
FUNDUS = 'https://tasty-ui-fundus.vercel.app/'
FUNDUS_B = FUNDUS + 'bereiche.html#hotel-'

# ---------------------------------------------------------------- Fotos: Schlüssel → Datei in _quelle/website/bilder (grösste Fassung)
FOTOS = {
    'tor': 'castel_16904516770216_hotelcastellsonclaretcastell3.jpg',
    'luftbild': 'castel_16950055718775_ourfuture.jpg',
    'gartenachse': 'castel_16904517004277_hotelcastellsonclaretcastellsonclaretluxuryboutiquehotelmallorca4.jpg',
    'tramuntana': 'castel_16904517691593_hotelcastellsonclaretnaturetramuntanamountainscastellsonclaretmallorca3.jpg',
    'castell-aussen': 'castel_16904523570259_hotelcastellsonclaretcastellsuite06.jpg',
    'castell-turm': 'castel_1690452354901_hotelcastellsonclaretcastellsuite03.jpg',
    'innenhof': 'castel_16904524292665_hotelcastellsonclaretcastelldemisuite09.jpg',
    'garten-suite': 'castel_16904525170229_hotelcastellsonclaretcastellgardensuite11.jpg',
    'pool-suite': 'castel_16904525464573_hotelcastellsonclaretcastellpoolsuite02.jpg',
    'wasserturm': 'castel_16904526705363_hotelcastellsonclaretcastellwatertowerduplex08.jpg',
    'turm-suite': 'castel_16904526394165_hotelcastellsonclaretcastelltowersuite02.jpg',
    'olivera-terrasse': '1730x8_16904522395388_hotelcastellsonclaretrestaurantolivera28.jpg',
    'brot': '1730x8_16951071623696_castellsonclaretoliverarestaurant14.jpg',
    'huerto': '1730x8_1698151090616_castellsonclaretteam9.jpg',
    'bar-cocktail': 'castel_16904509648433_hotelcastellsonclaretbar18.jpg',
    'bar-theke': 'castel_16904509443858_hotelcastellsonclaretbar01.jpg',
    'allee-nacht': '1920x7_17283758706203_cscentrancenight.jpg',
    'hof-abend': 'castel_16904520805401_hotelcastellsonclaretrestaurantsaclastra26.jpg',
    'jordi': '2400x1_17702940101559_.jordicantchefsaclastracastellsonclaretmallorca.webp',
    'teller-1': 'castel_16904520767395_hotelcastellsonclaretrestaurantsaclastra20.jpg',
    'teller-2': 'castel_16904521021615_hotelcastellsonclaretrestaurantsaclastra41.jpg',
    'pool': 'castel_16904516775109_hotelcastellsonclaretcastell4.jpg',
    'innenpool': '2400x1_16904511291335_hotelcastellsonclaretspa13.jpg',
    'hammam': '1730x8_16904510913617_hotelcastellsonclaretspabalibeds03.jpg',
    'yoga': '1730x8_16904514278949_hotelcastellsonclaretyoga09.jpg',
    'behandlung': '2400x1_17431544561535_.spaoutdoor20242.webp',
    'classics': 'castel_16950033763477_castellsonclaretcastellclassics18.jpg',
    'hochzeit-allee': '1730x8_16904515412294_hotelcastellsonclaretweddings16.jpg',
    'tafel-nacht': '1730x8_16904515830971_hotelcastellsonclaretweddings42.jpg',
    'tafona': 'galler_202309180405440.Sa_Tafona_1_.jpg',
    'garten-gaeste': '1920x7_16904510420234_hotelcastellsonclaretevents36.jpg',
    'team': '2400x1_16950055754598_ourteam.jpg',
    'nacht': 'castel_16904517236025_hotelcastellsonclaretcscnight.jpg',
    'fassade': 'castel_16904516779903_hotelcastellsonclaretcastell5.jpg',
}
PLAN_PDF = os.path.join(PROJEKT, '_quelle', 'website', 'pdf', '16905351550762_Castell-Son-Claret-Map.pdf')
FONTENAY = os.path.join(PROJEKT, '_fontenay-und-castell', '_quelle', 'fontenay', 'website', 'bilder', 'local_The_Fontenay_Drohne.jpg')


def quelle(key):
    return '_quelle/website/bilder/' + FOTOS[key]


def bilder_bauen():
    """Alle Fotos des Boards nach bilder/<key>.jpg, höchstens 1600 px breit. Der Plan aus dem PDF des Hauses."""
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
    ziel = os.path.join(BILDER, 'plan.jpg')
    if not os.path.exists(ziel):   # der Lageplan des Hauses (PDF, 2020) als Bild für das Board
        os.system(f'pdftoppm -r 110 -png -f 1 -l 1 "{PLAN_PDF}" "{os.path.join(BILDER, "plan")}"')
        im = Image.open(os.path.join(BILDER, 'plan-1.png')).convert('RGB'); im.save(ziel, 'JPEG', quality=88, optimize=True); os.remove(os.path.join(BILDER, 'plan-1.png'))
    ziel = os.path.join(BILDER, 'fontenay.jpg')
    if not os.path.exists(ziel) and os.path.exists(FONTENAY):
        im = Image.open(FONTENAY).convert('RGB')
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(ziel, 'JPEG', quality=82, optimize=True)


def foto(key):
    return f'bilder/{key}.jpg'


# ---------------------------------------------------------------- Bausteine des Boards
def kachel(key, name, satz='', i=0, lage='50% 50%', kl='k3--karte', kerbe=True):
    kb = f'<figcaption class="kerbe">{e(name)}</figcaption>' if kerbe else ''
    return (f'<figure class="k3 {kl}" data-r="feder" style="--i:{i}"><div class="k3__b"><img src="{foto(key)}" alt="{e(name)}" loading="lazy" decoding="async" style="object-position:{lage}">{kb}</div>'
            f'{f"<p class={chr(34)}kb__s{chr(34)}>{satz}</p>" if satz else ""}</figure>')


def fenster(key, zeilen, unter, lage='50% 50%'):
    z = ''.join(f'<span class="z"><span>{"<em>" + x + "</em>" if i == len(zeilen) - 1 and len(zeilen) > 1 else x}</span></span>' for i, x in enumerate(zeilen))
    return f'''<section class="fenster" aria-label="{e(' '.join(zeilen))}">
  <div class="fenster__f">
    <div class="fenster__b"><img src="{foto(key)}" alt="" decoding="async" style="object-position:{lage}"></div>
    <div class="fenster__t"><p class="fenster__s">{z}</p><p class="fenster__u">{unter}</p></div>
  </div>
</section>'''


def wort(text):
    return f'<span class="mono">{e(text)}</span>'


def szene(s, nr, flaeche_klasse):
    """Eine Szene als Blatt: Kopf (Nummer, Titel, Satz), Fotos, Bauzeile, darunter der Unterschied nebeneinander."""
    bilder = ''.join(kachel(k, n, i=i % 3, lage=l) for i, (k, n, l) in enumerate(s['fotos']))
    alt = ''
    if s.get('alternativen'):
        alt = '<p class="sz__alt"><b>Weitere Kandidaten</b> ' + ' · '.join(f'<span class="mono">{e(a)}</span>' for a in s['alternativen']) + '</p>'
    baust = e(s['baustein']) + (' <em>neu</em>' if s['quelle'] == 'neu' else ' <em>Fundus</em>')
    skizze = f'<div class="sz__z"><b>Skizze</b><p>{e(s["skizze"])}</p></div>' if s.get('skizze') else ''
    bisher = ''.join(f'<li><a href="{e(LIVE.get(h, "#"))}{e(s["bisher_anker"].get(h, ""))}" target="_blank" rel="noopener"><b>{e(h)}</b></a><span>{e(t)}</span></li>' for h, t in s['bisher'].items())
    fl = {'hell': 'Hell (Kalk)', 'creme': 'Hell (Sandstein)', 'tapete': 'Hell mit Tapete', 'dunkel': 'Nacht mit Tapete', 'foto': 'Foto, Mittag'}[s['flaeche']]
    return f'''<section class="ab blatt {flaeche_klasse} sz" id="s-{s['teil']}">
  <div class="in">
    <header class="mk" data-r="kopf">
      <div><p class="mk__kap"><b>Szene {nr:02d} · {e(s['teil'])}</b><i></i></p><h2 class="mk__t">{B2.zeilen(s['titel'])}</h2></div>
      <p class="mk__lead">{e(s['satz'])}{' <span class="vonmir">von mir</span>' if s.get('vonmir') else ''}</p>
    </header>
    <div class="sz__fotos sz__fotos--{min(len(s['fotos']), 4)}" data-g>{bilder}</div>
    {alt}
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
GESCHICHTE = ('Die Startseite ist ein Gang über das Gut, vom Tor im Mittag bis zum Castell bei Nacht: Tor, Plan des Guts, die Häuser, in denen man wohnt, '
              'der Tisch im Garten, Sa Clastra mit seinen Winden, das Wasser, die Feste, das Angebot, das Tor bei Nacht. '
              'Hell wie der Tag auf dem Gut; dunkel nur dort, wo das Haus es selbst ist.')

BISHER_AUFTAKT = {
    'Carlton-Europe': 'Türflügel, die sich öffnen; Navy, Gold, Wortmarke mittig über dem Haus; Buchungsleiste unten.',
    'Grand Beau-Rivage': 'Hero mittig über der Aare: Zeichen in Gold über dem Namen, Ortszeile «Interlaken · seit 1874», Buchungsleiste als Platte.',
    'Hotel Seiler au Lac': 'Dunst statt Vorhang, Wortmarke in Gold, Eck-Knöpfe, Seefoto.',
    'Waldhotel Doldenhorn': 'Block unten links, Auszeichnungs-Laufband direkt darunter.',
    'Landgasthof Ruedihus': 'Holzhaus von 1753 als Profil, Satz «Heute Abend Ihr Tisch, heute Nacht Ihr Bett».',
    'Berghotel Gasterntal': 'Hof hinter dem Titel «Herzlich willkommen», Berghütte, kein Tor.',
    'Salt & Silver': 'Hafen bei Nacht, Vorhang mit Zeichen, Antonio-Versalien, Kursblatt.',
}
ANKER_START = {h: 'index.html#oben' for h in BISHER_AUFTAKT}
ANKER_START.update({'Carlton-Europe': '#oben', 'Waldhotel Doldenhorn': '#ankunft', 'Landgasthof Ruedihus': '#ankunft', 'Berghotel Gasterntal': '#ankunft', 'Salt & Silver': '#'})

SZENEN = [
    dict(teil='auftakt', titel=['Der Name steht', 'im Tor.'],
         satz='«Es gibt Orte, die man einfach nicht beschreiben kann.»',
         fotos=[('tor', 'Das Tor mit den zwei Pfeilern, Mittag', '50% 55%'), ('luftbild', 'Das Gut von oben, Galatzó im Rücken', '50% 50%'), ('gartenachse', 'Die Gartenachse zum Castell', '50% 50%')],
         bilder=[quelle('tor')], alternativen=[quelle('luftbild'), quelle('gartenachse')],
         baustein='Auftakt «Name im Tor»', quelle='neu',
         skizze='Das Tor-Foto ganz, in Farbe, ein Bildschirm hoch. Die Wortmarke in Bar-Gold steht in der Öffnung zwischen den zwei Pfeilern, auf dem Weg, nicht über dem Haus. Darunter die Ortszeile «Es Capdellà · Mallorca» in Montserrat gesperrt und der eine Satz des Hauses. Unten die Buchungsleiste als Sandstein-Platte mit Kuhlen. Leiste oben als Creme-Insel über dem Foto. Der Baumeister zeigt 20 bis 50 Fassungen des Tor-Bildes, Robert wählt.',
         bewegung='Wortmarke rollt aus dem Schlitz, Ortszeile und Satz kommen gestaffelt, die Platte schwebt von unten. Kein Vorhang, kein Tor-Effekt, kein Film.',
         flaeche='foto',
         unterschied='Das Tor steht im Foto, nichts öffnet sich. Der Name sitzt in der Toröffnung, unten auf dem Weg, nicht mittig über dem Haus und nicht in einer Ecke. Hell im Mittag statt Nacht, Dunst oder Hafen.',
         bisher=BISHER_AUFTAKT, bisher_anker=ANKER_START),
    dict(teil='gut', titel=['Ein Landgut,', 'seit 1450.'],
         satz='«Possessiones gibt es auf Mallorca seit dem Mittelalter. Sie sind autarke ländliche Zentren.»',
         fotos=[('luftbild', '132 Hektar am Fuß des Galatzó', '50% 40%'), ('plan', 'Lageplan des Hauses (PDF, 2020)', '50% 50%'), ('fassade', 'Das Castell im Mittag', '50% 30%')],
         bilder=[quelle('luftbild'), '_quelle/website/pdf/16905351550762_Castell-Son-Claret-Map.pdf', quelle('fassade')],
         baustein='Der Plan des Guts', quelle='neu',
         skizze='Eine Nacht-Platte mit Tapete, darauf der Plan des Anwesens aus dem Lageplan des Hauses, neu gezeichnet in feinen Linien in Bar-Gold: Allee, Tor, Castell, Innenhof, Olivera, Garten mit Wasserbecken, Häuser 3 bis 10, Wasserturm, Tennisplatz, Castell Park. Die Orte stehen als Wörter in Fahkwang am Plan. Wer einen Ort antippt, bekommt rechts in der Kachel das Foto des Orts, das deckend von unten heraufkommt. Darunter eine Hotelkarten-Zeile: 1450 in Aufzeichnungen · 132 Hektar · 43 Zimmer und Suiten · Hotel seit Mai 2013. Handy: Plan oben, die Orte als Band darunter.',
         bewegung='Die Linien des Plans erscheinen gestaffelt über die Deckkraft, die Ortswörter schweben herein, das Foto kommt deckend von unten. Nur ein Element in Bewegung.',
         flaeche='hell',
         unterschied='Kein Willkommensgruss und kein Rundgang durch Räume: Der zweite Abschnitt ist der Plan eines 132-Hektar-Guts, eine Infografik, die etwas Wahres zeigt und zu jedem Ort der Seite führt. Keines der bisherigen Häuser hat einen Plan seines Geländes.',
         bisher={'Carlton-Europe': '«Das Vintage Hotel» mit Fotos, danach «Zwei Häuser, ein Hotel» auf Creme mit Tapete.',
                 'Grand Beau-Rivage': '«Halle»: dunkler Abschnitt, Rundgang durch die Räume, Portier.',
                 'Hotel Seiler au Lac': '«Der Tag beginnt auf dem Balkon», danach die Uhr «Ein Tag am See».',
                 'Waldhotel Doldenhorn': '«Herzlich willkommen» hell, dann die Wahl «Worauf freuen Sie sich?».',
                 'Landgasthof Ruedihus': '«Das Ruedihus, unsere Dependance», dann die Frage «Was führt Sie zu uns?» auf Holz.',
                 'Berghotel Gasterntal': '«Im wildromantischen Gasterntal» als Laube, dann «Was Sie hier nicht finden».'},
         bisher_anker={'Carlton-Europe': '#willkommen', 'Grand Beau-Rivage': '#halle', 'Hotel Seiler au Lac': '#balkon', 'Waldhotel Doldenhorn': '#willkommen', 'Landgasthof Ruedihus': '#ankommen', 'Berghotel Gasterntal': '#haus'}),
    dict(teil='fenster-galatzo', titel=['Fenster', 'Der Galatzó im Rücken.'],
         satz='Der Galatzó im Rücken, der Garten vor der Tür.', vonmir=True,
         fotos=[('tramuntana', 'Die Tramuntana vom Gut aus', '50% 50%')],
         bilder=[quelle('tramuntana')],
         baustein='Fenster', quelle='fundus',
         bewegung='Das Bild steht, die Seite zieht darüber, der Satz rollt zeilenweise herein, sobald ein Drittel frei ist. Erstes von drei Fenstern.',
         flaeche='foto',
         unterschied='Das Fenster zeigt den Berg, nicht das Haus; es ist der Wendepunkt vom Ankommen zum Wohnen. Drei Fenster je Startseite: Galatzó, Allee bei Nacht, Castell Classics.',
         bisher={'Grand Beau-Rivage': 'Fünf Fenster, das erste «Ankommen mit Stil» nach der Halle.', 'Carlton-Europe': 'Erstes Fenster «Was bedeutet Vintage?» nach «Zwei Häuser».', 'Landgasthof Ruedihus': 'Fenster mit Zitaten des Hauses, 7 % gegenläufig.', 'Hotel Seiler au Lac': '«Die Schiffe halten vor dem Haus.»'},
         bisher_anker={'Grand Beau-Rivage': '#zimmer', 'Carlton-Europe': '#zimmer', 'Landgasthof Ruedihus': '#frage', 'Hotel Seiler au Lac': '#tag'}),
    dict(teil='zimmer', titel=['Wo auf dem Gut', 'Sie wohnen.'],
         satz='Fünf Orte, elf Kategorien, 43 Zimmer und Suiten.', vonmir=True,
         fotos=[('castell-turm', 'Im Castell: Deluxe Double, Terrace Deluxe, Turm-Suite', '50% 40%'), ('innenhof', 'Am Innenhof und im Gebäude neben dem Castell: Estate Double, Estate Courtyard, Demi Suite, Terrace Demi Suite, Castell Suite', '50% 50%'),
                ('garten-suite', 'Im Garten: Garden Suite', '50% 50%'), ('pool-suite', 'Mit eigenem Pool: Pool Suite', '50% 50%')],
         bilder=[quelle('castell-turm'), quelle('innenhof'), quelle('garten-suite'), quelle('pool-suite'), quelle('wasserturm')],
         baustein='Bildwand der Häuser mit Fach', quelle='neu',
         skizze='Fünf Fotos der Gebäude als Ziegelverband: zwei oben, drei unten, je Reihe exakt gleich hoch, randlos, runde Ecken. Nur das grösste trägt die Einkerbung. Jedes Haus heisst nach seinem Ort: Im Castell · Am Innenhof · Im Garten · Mit eigenem Pool · Im Wasserturm. Unter der Wand ein Fach: Es zeigt die Kategorien des angetippten Hauses als Kacheln mit grossem Foto, Name in der Einkerbung, m² und Personen als Hotelkarten-Zeile, Knopf «Zimmer ansehen». Gewählt ist das Haus, dessen Foto hell bleibt; die anderen werden leicht dunkler. Beim Öffnen ist das Castell gewählt. Die Zuordnung der Kategorien kommt aus den Zimmertexten des Hauses (Deluxe Double: Castell, Erdgeschoss bis zweite Etage · Turm-Suite: die Türme, erster Stock · Castell Suite: Erdgeschoss im Gebäude neben dem Castell · Terrace Demi Suite: erste Etage dort · Estate: Blick auf den Innenhof · Garden Suite: im Garten · Pool Suite: eigener Garten mit Pool · Wasserturm-Duplex).',
         bewegung='Die Wand kommt als Ganzes (scale .965 → 1), die Fotos zoomen in ihren Rahmen. Beim Antippen öffnet sich das Fach, die Kacheln schweben nacheinander von unten.',
         flaeche='creme',
         unterschied='Zimmer nach Orten, nicht nach Kategorien: Die erste Ebene sind die Gebäude des Guts, die Kategorien liegen eine Ebene tiefer im Fach. Kein Haus zeigt Zimmer so.',
         bisher={'Grand Beau-Rivage': 'Reihe von 3D-Kacheln je Kategorie mit Namensfeld, Knopf mittig.', 'Carlton-Europe': 'Kacheln «Süsse Träume», danach das Kissen-Band.',
                 'Waldhotel Doldenhorn': 'Helle Kacheln von Economy bis Junior Suite.', 'Landgasthof Ruedihus': 'Gerahmte Fotos mit den Namen der Stuben («Geborgenheit und Freude teilen»).',
                 'Berghotel Gasterntal': 'Polaroids paarweise, nach dem Fenster «Die Zimmer».', 'Hotel Seiler au Lac': 'Die Zimmer stecken im Abschnitt «Der Tag beginnt auf dem Balkon».'},
         bisher_anker={'Grand Beau-Rivage': '#zimmer', 'Carlton-Europe': '#zimmer', 'Waldhotel Doldenhorn': '#zimmer', 'Landgasthof Ruedihus': '#zimmer', 'Berghotel Gasterntal': '#zimmer', 'Hotel Seiler au Lac': '#balkon'}),
    dict(teil='tisch', titel=['Vom Garten', 'auf den Tisch.'],
         satz='«Hausgemachte Brote, frischer Fisch aus dem Mittelmeer, Bergprodukte und Olivenöl von unserem Anwesen.»',
         fotos=[('olivera-terrasse', 'Olivera, die Terrasse am Mittag', '50% 50%'), ('brot', 'Die eigene Bäckerei', '50% 50%'), ('huerto', 'Der Garten mit ESMENT', '50% 50%'), ('bar-cocktail', 'Castell Bar im Kutscherhaus', '50% 50%')],
         bilder=[quelle('olivera-terrasse'), quelle('brot'), quelle('huerto'), quelle('bar-cocktail'), quelle('bar-theke')],
         baustein='Lage eines Hauses, darunter drei Kacheln', quelle='fundus',
         bewegung='Das Olivera-Foto über die volle Breite schwebt herauf, die helle Tafel mit den Zeiten (8.00–10.30, 13.00–15.30, 19.00–21.30 Uhr) liegt darüber. Die drei Kacheln kommen gestaffelt, pulsieren einmal, zoomen in den Rahmen.',
         flaeche='tapete',
         unterschied='Der Tisch wird vom Garten her erzählt: Brot, Öl, Gemüse, Kräuter kommen vom Gut, deshalb stehen Bäckerei und Garten neben dem Restaurant. Sa Clastra bekommt eine eigene, dunkle Szene.',
         bisher={'Grand Beau-Rivage': '«Restaurants & Bar» als Kacheln auf Papier.', 'Carlton-Europe': '«Im Haus» dunkel mit Wechsel hell/dunkel über drei Abschnitte.',
                 'Waldhotel Doldenhorn': '«Gemeinsam geniessen und verweilen» dunkel mit Tannen.', 'Landgasthof Ruedihus': '«Kommen Sie herein»: Stuben, Rahmen hängen sich auf.',
                 'Hotel Seiler au Lac': '«Zwei Tische am See» auf Creme.', 'Berghotel Gasterntal': 'Karte als Laube.'},
         bisher_anker={'Grand Beau-Rivage': '#tafel', 'Carlton-Europe': '#im-haus', 'Waldhotel Doldenhorn': '#kueche', 'Landgasthof Ruedihus': '#stuben', 'Hotel Seiler au Lac': '#tische', 'Berghotel Gasterntal': '#karte'}),
    dict(teil='fenster-allee', titel=['Fenster', 'Die Allee bei Nacht.'],
         satz='«Wind und Erinnerung.»',
         fotos=[('allee-nacht', 'Die Palmenallee zum Castell bei Nacht', '50% 45%')],
         bilder=[quelle('allee-nacht')],
         baustein='Fenster', quelle='fundus',
         bewegung='Wie das erste Fenster. Der Satz ist der Name des Menüs von Sa Clastra; die Seite wird hier zum ersten Mal dunkel.',
         flaeche='foto',
         unterschied='Das zweite Fenster ist die Naht von Tag zu Nacht. Danach kommt der einzige dunkle Abschnitt der Startseite.',
         bisher={'Grand Beau-Rivage': '«Während das Kaminfeuer knistert» vor den Restaurants.', 'Carlton-Europe': '«Vom Zimmer hinaus in die Berge».'},
         bisher_anker={'Grand Beau-Rivage': '#tafel', 'Carlton-Europe': '#anlass'}),
    dict(teil='saclastra', titel=['Sa Clastra:', 'acht Winde, ein Menü.'],
         satz='«Mallorca trägt die Handschrift seiner Winde.»',
         fotos=[('hof-abend', 'Der Hof von Sa Clastra am Abend', '50% 50%'), ('jordi', 'Jordi Cantó', '50% 30%'), ('teller-1', 'Ein Gang aus «Wind und Erinnerung»', '50% 50%'), ('teller-2', 'Gamba de Sóller', '50% 50%')],
         bilder=[quelle('hof-abend'), quelle('jordi'), quelle('teller-1'), quelle('teller-2'), '_quelle/website/pdf/17424632450264_Rosa_20de_20los_20vientos_20-_20GER.pdf', '_quelle/video/hotel-kanal/youtube_a7RZRKnFlKc_Restaurante Sa Clastra ｜ Los vientos de Mallorca.mp4'],
         baustein='Die Windrose', quelle='neu',
         skizze='Auf Nacht mit Tapete steht die Windrose des Hauses in Bar-Gold, aus der Karte «Rosa de los vientos» gezeichnet. Um sie herum die acht Winde als Wörter mit ihrer Zeit, wie das Haus sie druckt: Tramuntana 1200 v. Chr. – 123 v. Chr. · Gregal 800 v. Chr. – 146 v. Chr. · Llevant 1229 – heute · Xaloc 902 – 1229 · Migjorn 455 – 534 · Garbí moderne Zeiten · Ponent 123 v. Chr. – 476 · Mistral 534 – 800. Wer einen Wind antippt, dreht die Rose zu ihm (nur die Rose bewegt sich), Name und Zeit wechseln kurz und hart. Rechts daneben der Hof am Abend als 3D-Kachel, darunter Jordi Cantó mit Einkerbung und der Film «Los vientos de Mallorca» als Standbild mit Start per Klick. Knöpfe: «Tisch reservieren» (CoverManager bleibt), «Das Menü».',
         bewegung='Die Rose dreht sich beim Hereinkommen einmal in ihre Lage (transform), die Winde schweben gestaffelt herein. Beim Antippen dreht nur die Rose.',
         flaeche='dunkel',
         unterschied='Der einzige dunkle Abschnitt der Startseite gehört dem einen Restaurant mit Stern. Das bewegte Element ist die Windrose des Hauses, keine Kachel und kein Band. Kein bisheriges Haus hat ein Zeichen des Hauses als Bedienelement in der Mitte eines Abschnitts.',
         bisher={'Grand Beau-Rivage': 'Restaurants als Kacheln, der dunkle Abschnitt ist die Halle und das Bad.', 'Carlton-Europe': 'Drei dunkle/helle Abschnitte «Im Haus», «Wellness», «Dach».',
                 'Landgasthof Ruedihus': 'Kompass der Herkunft (Lieferanten) als Infografik.', 'Salt & Silver': 'Kursblatt mit Fahrt, Vorhang mit Zeichen.', 'Hotel Seiler au Lac': 'Fahrplan-Tafel «Vor der Tür» auf Holz.'},
         bisher_anker={'Grand Beau-Rivage': '#halle', 'Carlton-Europe': '#im-haus', 'Landgasthof Ruedihus': '#rund', 'Salt & Silver': '#', 'Hotel Seiler au Lac': '#tuer'}),
    dict(teil='wasser', titel=['Das Wasser', 'des Guts.'],
         satz='Vom Aljub zum Pool: Bellesa de Claret.', vonmir=True,
         fotos=[('pool', 'Der Pool an der Steinmauer', '50% 50%'), ('yoga', 'Yoga auf dem Wasserbecken', '50% 50%'), ('hammam', 'Der Hammam', '50% 50%'), ('innenpool', 'Der Innenpool', '50% 50%')],
         bilder=[quelle('pool'), quelle('yoga'), quelle('hammam'), quelle('innenpool'), quelle('behandlung')],
         baustein='Band zum Blättern', quelle='fundus',
         bewegung='Fünf hohe Karten, nativer Seitwärts-Scroll, Pfeile und Laufbalken, erste Karte mit Abstand zum Rand. Die Karten schweben beim ersten Hereinkommen gestaffelt von unten.',
         flaeche='hell',
         unterschied='Das Band trägt die Orte des Wassers auf dem Gut (Pool an der Mauer, Innenpool, Hammam, Yoga auf dem Becken, Behandlung im Garten), nicht Packages oder Kissen. Spa heisst hier Wasser, weil die Possessió vom Wasser der Zisternen lebte.',
         bisher={'Grand Beau-Rivage': '«Bad» als Wand-Abschnitt auf Nacht; das Band gehört den Angeboten.', 'Carlton-Europe': '«Wellness-Park» hell; das Band gehört den Kissen.',
                 'Waldhotel Doldenhorn': '«Anspannung lösen» auf Stahlblau.', 'Berghotel Gasterntal': '«Sauna in der alten Käserei».'},
         bisher_anker={'Grand Beau-Rivage': '#bad', 'Carlton-Europe': '#wellness-park', 'Waldhotel Doldenhorn': '#spa', 'Berghotel Gasterntal': '#sauna'}),
    dict(teil='fenster-classics', titel=['Fenster', 'Castell Classics.'],
         satz='«Jedes Jahr ist das Castell Son Claret Gastgeber der Castell Classics.»',
         fotos=[('classics', 'Konzert vor dem Castell', '50% 50%')],
         bilder=[quelle('classics')],
         baustein='Fenster', quelle='fundus',
         bewegung='Wie die anderen Fenster. Drittes und letztes Fenster.',
         flaeche='foto',
         unterschied='Das dritte Fenster ist ein Konzertabend, ein Ereignis, kein Raum und kein Ausblick.',
         bisher={'Grand Beau-Rivage': '«Ein besonderes Juwel im Herzen des Hauses» vor dem Salon.', 'Carlton-Europe': '«Die wohl schönste Dachterrasse von Interlaken».'},
         bisher_anker={'Grand Beau-Rivage': '#salon', 'Carlton-Europe': '#pakete'}),
    dict(teil='feiern', titel=['Feste', 'auf dem Gut.'],
         satz='Hochzeiten unter Palmen, Tagungen in der Ölmühle.', vonmir=True,
         fotos=[('hochzeit-allee', 'Hochzeit auf der Allee', '50% 50%'), ('tafel-nacht', 'Die Tafel unter Palmen', '50% 50%'), ('tafona', 'Sa Tafona, die alte Ölmühle', '50% 50%'), ('garten-gaeste', 'Gäste im Garten', '50% 50%')],
         bilder=[quelle('hochzeit-allee'), quelle('tafel-nacht'), quelle('tafona'), quelle('garten-gaeste')],
         baustein='Ziegelverband aus vier (Bildgruppe)', quelle='fundus',
         bewegung='Die vier Bilder kommen als Einheit, nur das grösste trägt die Einkerbung. Klick auf ein kleines Bild: es fährt an die Stelle des grossen.',
         flaeche='tapete',
         unterschied='Keine Wahl «Wofür kommen Sie?» und keine Säle als Bühne: Die Feste sind Orte des Guts (Allee, Tafel unter Palmen, Ölmühle, Garten). Die Zahlen der Räume (Sa Tafona 70 m², 45 Personen · Boardroom 30 m², 10 · Garten 4.400 m², 150) stehen auf der Unterseite mit dem Anfrage-Rechner.',
         bisher={'Grand Beau-Rivage': '«Feiern & Tagen» auf Creme, Säle als Bühne, Anfrage-Rechner.', 'Carlton-Europe': '«Wofür kommen Sie?» als Wahl, Packages & Events auf Navy.',
                 'Waldhotel Doldenhorn': '«Feste und Seminare» hell.', 'Berghotel Gasterntal': '«Feiern Sie Ihren besonderen Anlass» hell.'},
         bisher_anker={'Grand Beau-Rivage': '#saal', 'Carlton-Europe': '#anlass', 'Waldhotel Doldenhorn': '#feste', 'Berghotel Gasterntal': '#feste'}),
    dict(teil='angebote', titel=['Direkt gebucht,', '5 € für das Meer.'],
         satz='«Für jede Online-Reservierung spenden wir 5 € an die Marilles Stiftung.»',
         fotos=[('fassade', 'Das Castell im Mittag', '50% 30%'), ('teller-1', 'Michelin-Stern-Erlebnis', '50% 50%'), ('yoga', 'Wellness-Tag', '50% 50%')],
         bilder=['_quelle/website/bilder/offers_*.jpg (je Angebot, Zuordnung in herkunft.json)'],
         baustein='Platte und Kuhle', quelle='fundus',
         bewegung='Drei helle Platten auf Nacht mit Tapete kommen deckend von unten; Foto oben, Name, Leistungen mit Haarlinien, Knopf. Darunter die Marilles-Zeile als Platte mit Kuhle.',
         flaeche='dunkel',
         unterschied='Die Angebote stehen unter dem Grund, direkt zu buchen (5 € ans Meer). Platten statt Band, drei sichtbar, der Rest auf der Unterseite; jeder Buchen-Knopf öffnet sein Angebot (Befund 3.1).',
         bisher={'Grand Beau-Rivage': 'Angebote als Band zum Blättern auf Nacht.', 'Carlton-Europe': '«Packages & Events» auf Navy mit Tapete.', 'Hotel Seiler au Lac': '«Zuerst, was Sie bekommen» auf Nacht.', 'Waldhotel Doldenhorn': '«Gourmet-Aufenthalt» auf Stahlblau (Zimmerseite).'},
         bisher_anker={'Grand Beau-Rivage': '#angebote', 'Carlton-Europe': '#pakete', 'Hotel Seiler au Lac': '#angebote', 'Waldhotel Doldenhorn': 'zimmer.html#gourmet'}),
    dict(teil='gaeste', titel=['Was Gäste', 'und Prüfer sagen.'],
         satz='Booking.com 8,7 von 10 aus 133 Bewertungen · Michelin-Stern für Sa Clastra · The Leading Hotels of the World · EarthCheck seit 2023.',
         fotos=[('team', 'Das Team des Hauses', '50% 40%')],
         bilder=[quelle('team'), '_quelle/website/bilder/250x25_17283056162201_michelinstarxcastellsonclaret.jpg', '_quelle/website/bilder/250x25_16987525962146_theleadinghotelsoftheworld250.png', '_quelle/website/bilder/250x25_17283056155606_earthcheckxcastellsonclaret.jpg'],
         baustein='Zeile zwischen Goldlinien, Siegel als Originaldateien', quelle='fundus',
         bewegung='Die Note steht gross in Fahkwang und zählt nicht hoch. Die drei Siegel schweben gestaffelt herein. Das Teamfoto daneben als 3D-Kachel.',
         flaeche='creme',
         unterschied='Eine Note und drei Siegel, dazu das Team: Robert wollte beim Carlton keine hochzählenden Zahlen, beim Rivage zählen sie. Hier stehen sie still, und das Team steht daneben («Viele Mitarbeitende sind seit der Eröffnung dabei»).',
         bisher={'Grand Beau-Rivage': '«Was Gäste am Haus schätzen»: Noten zählen hoch zwischen Goldlinien.', 'Carlton-Europe': '«Lassen Sie die Seele baumeln»: Auszeichnungen als vier Felder.', 'Waldhotel Doldenhorn': 'Auszeichnungs-Laufband direkt unter dem Auftakt.', 'Landgasthof Ruedihus': '«So sehen es die Gäste» auf Holz.'},
         bisher_anker={'Grand Beau-Rivage': '#gaeste', 'Carlton-Europe': '#pakete', 'Waldhotel Doldenhorn': '#ankunft', 'Landgasthof Ruedihus': '#gaeste'}),
    dict(teil='nacht', titel=['Das Castell', 'bei Nacht.'],
         satz='Castell Son Claret · Ctra. Capdellà-Galilea Km 1,7 · 07196 Es Capdellà.',
         fotos=[('nacht', 'Das Castell mit dem Wasserbecken bei Nacht', '50% 50%')],
         bilder=[quelle('nacht')],
         baustein='Nachtbild volle Breite, zweite Buchungsleiste, Anreise als Platte', quelle='fundus',
         bewegung='Das Nachtbild schwebt herauf, darüber die Buchungsleiste als Sandstein-Platte, daneben die Anreise-Platte mit Adresse. Lädt ein, verabschiedet nicht.',
         flaeche='foto',
         unterschied='Der Bogen schliesst sich: Tor im Mittag am Anfang, Castell bei Nacht am Ende. Kein «Herzlich willkommen» als Schluss, keine Karte des Ortes, keine «Gute Nacht».',
         bisher={'Grand Beau-Rivage': '«Herzlich willkommen im Grand Beau-Rivage» als Abschied auf Nacht.', 'Hotel Seiler au Lac': '«Gute Nacht am See».', 'Carlton-Europe': 'Schluss mit Karte.', 'Waldhotel Doldenhorn': '«Wir freuen uns, Sie bald willkommen zu heissen».'},
         bisher_anker={'Grand Beau-Rivage': '#abschied', 'Hotel Seiler au Lac': '#schluss', 'Carlton-Europe': '#pakete', 'Waldhotel Doldenhorn': '#buchen'}),
    dict(teil='fuss', titel=['Der Fuss', 'mit dem Schwesterhaus.'],
         satz='«The Luxury of being Yourself.»',
         fotos=[('fontenay', 'The Fontenay, Hamburg (Schwesterhaus)', '50% 50%')],
         bilder=['_fontenay-und-castell/_quelle/fontenay/website/bilder/local_The_Fontenay_Drohne.jpg'],
         baustein='Fuss mit Tapete, Kontaktfeld, Linkspalten, Siegel, Karte des Schwesterhauses', quelle='fundus',
         bewegung='Ruhig. Die Wortmarke baut sich einmal auf, die Spalten kommen gestaffelt.',
         flaeche='dunkel',
         unterschied='The Fontenay steht als Karte mit Foto im Fuss, nicht als Satz (Befund 7.6). Darunter die Zeile «Designstudie von Tasty Studios, nicht die offizielle Website».',
         bisher={'Grand Beau-Rivage': 'Fuss für zwei Häuser (Seiler au Lac als Karte).', 'Waldhotel Doldenhorn': 'Fuss der Hotelfamilie mit vier Häusern als Karten.', 'Carlton-Europe': 'Eigener Fuss mit Inschrift und Breitbild.'},
         bisher_anker={'Grand Beau-Rivage': '#abschied', 'Waldhotel Doldenhorn': '#buchen', 'Carlton-Europe': '#pakete'}),
]

UNTERSEITEN = [
    ('zimmer.html', 'Zimmer und Suiten', '12 Seiten je Sprache', 'Seitenkopf mit dem Castell · Register der fünf Orte · je Kategorie Bildgruppe (1 gross + 2 klein) mit Text daneben, abwechselnd · Hotelkarten-Zeile m²/Personen aus den Zimmertexten · Knopf «Zimmer buchen» in die richtige Kategorie (Profitroom, RoomID stimmt heute) · Haustier-Regel einmal, eindeutig · «Gut zu wissen» (Check-in ab 15.00, Check-out bis 12.00) · Ausklang-Zeile', 'Seitenkopf · Bildgruppe · Einkerbung · Platte und Kuhle · Auswahl im Hausstil'),
    ('sa-clastra.html', 'Sa Clastra', '3 Seiten + 9 PDFs', 'Kopf: der Hof am Abend · die Windrose gross · das Menü «Wind und Erinnerung» als Seite, acht Winde mit Zeit und Gängen aus den September-Karten (lange und kurze Fassung), nicht nur als PDF (Befund 4.1) · Film «Los vientos de Mallorca» · Jordi Cantó · Weinkarte vom 03.10.2026 · Reservieren (CoverManager bleibt) · Saison (offen: genaue Daten)', 'Windrose (neu) · Karte als Erlebnis · 3D-Kachel · Film im Bild'),
    ('olivera.html', 'Olivera', '4 Seiten + 12 PDFs', 'Kopf: die Terrasse · Zeiten · Mittag, Abend und Pool-Bar als Daten aus den September-Karten (eine Quelle für Seite, La Carte und PDF; Befund 4.2) · Degustationsmenü «Wurzeln & Avantgarde» · die Bäckerei · Reservieren', 'Lage eines Hauses · Karte als Daten · Bogen-Karte'),
    ('castell-bar.html', 'Castell Bar', 'heute nur PDF (Bild)', 'Das Kutscherhaus, die Theke, die Kräuter aus dem Garten · die Karte 2025 neu als Daten gesetzt (das PDF ist ein Bild ohne Text: offen, Wortlaut aus dem Bild) · Mosaik-Zeichen in Gold', 'Lage eines Hauses · Karte als Daten'),
    ('spa.html', 'Bellesa de Claret', '3 Seiten, Preislisten heute nicht ladbar', 'Kopf: Yoga auf dem Wasser · Innenpool, Hammam, Behandlungen aus dem Garten als Zeilen mit Preis (48 Preise aus dem Spa-Menü; Befund 5.1) · Zeiten 8.00–20.00, Behandlungen 10.00–19.30 · Buchung (Spalopia bleibt, Sprache richtig) · Yoga-Retreat', 'Seitenkopf · Band zum Blättern · Weinkarten-Zeile'),
    ('feiern.html', 'Feiern und Tagen', '7 Seiten + 5 Kits', 'Hochzeiten auf der Allee, Tafel unter Palmen · Sa Tafona 70 m² / 45, Boardroom 30 m² / 10, Gärten 4.400 m² / 150 · Anfrage-Rechner und Formular in einem Abschnitt, Anfrage an events@ (Befund 6.3) · Wedding Kit 2026 in der Sprache der Seite (Befund 6.1) · Castell Classics mit Programm (offen: 2026)', 'Bildgruppe · Anfrage-Rechner (3a) · Platte und Kuhle'),
    ('angebote.html', 'Angebote, Gutscheine, Treue, Day Pass', '13 Seiten + zwei Shops', 'Alle Angebote als Platten, jeder Knopf öffnet sein Angebot (OfferID; Befund 3.1) · eine Saison, einmal gepflegt (offen: welche Winterpause gilt) · Gutscheine an einem Ort, dann in den zuständigen Shop (Befund 3.4) · Treueprogramm 10/15/20 % · Day Pass 150 € p. P., 300 und 350 € je Paar, ab 600 € für vier, buchbar im Tischsystem (offen) · Marilles-Zeile', 'Platte und Kuhle · Billett nicht (Carlton/Rivage) · Gutschein online (3a)'),
    ('gut.html', 'Das Gut', '2 Seiten (Über uns, Nachhaltigkeit)', 'Possessió seit 1450, bis zu 80 Menschen, Tafona, Keller, Aljubs · das Team als Gruppenfoto · ESMENT, Marilles, EarthCheck, Kühne-Stiftung · Castell Classics · The Fontenay als Schwesterhaus (Befund 7.6) · Geschichte an echten Stücken (offen: Archivbilder)', 'Plan des Guts (neu) · Grosse Zahlen (nur hier) · 3D-Kachel'),
    ('region.html', 'Mallorca vom Gut aus', '16 Ausflugsseiten + Strandführer + Blog', 'Ausflüge als Kacheln mit grossem Foto: Strandführer, Wandern zum Galatzó (PDFs), Husky Rides, Boot, Weinprobe, Palma, Beach Club, E-Bike, Radfahren · je Ausflug eine Seite in der Sprache der Seite (Befund 8.2) · kein Wetter', '3D-Kachel · Band zum Blättern'),
    ('vor-ihrer-anreise.html', 'Vor Ihrer Anreise', 'neu (Gäste-Funktion 3a)', 'Zimmermappe für gebuchte Gäste: Ankunftszeit, Tisch in Olivera oder Sa Clastra, Day Pass, Yoga, alles an die Rezeption · Rezeption im Chat', 'Meldeschein-Karte · Rezeption im Chat'),
    ('kontakt.html', 'Anreise und Kontakt', '2 Kontaktseiten', 'Adresse, Karte, Weg von Palma und vom Flughafen (offen: welche Zahl gilt, Befund 10.3) · eine Nummer, eine Adresse (offen: 620 oder 629, Befund 10.2) · Formular als heller Briefbogen · häufige Fragen', 'Billett nicht · Briefbogen (Rivage) · Auswahl im Hausstil'),
    ('faq.html', 'Fragen und Antworten', '1 Seite, 285 Fragen', 'Nach Themen gegliedert, als Fragen ausgezeichnet, aufklappbar, für Google hinterlegt (Befund 9.2)', 'Gut zu wissen'),
    ('journal.html', 'Journal', 'Blog mit 1 sichtbaren Beitrag', 'Strandführer, Castell Classics als Rückblick (Salzburg, Staatsoper Hamburg), Platz für Garten, Bäckerei, Öl (Befund 7.3)', 'Ansichtskarte · Bildgruppe'),
    ('impressum.html · datenschutz.html', 'Rechtstexte', 'Aviso Legal, Datenschutz', 'Wortlaut des Hauses (Aviso Legal, Privacy Policy), Kopf übersetzt · AGB und Widerruf: offen (nicht gefunden) · 404-Seite mit Wegen zu Zimmern, Restaurants, Kontakt (Befund 9.8)', 'Blatt rechts, Inhaltsfeld links'),
    ('es/ · en/ · fr/', 'Sprachen', 'heute es, de, en, fr', 'Station 15a: mindestens die vier Sprachen von heute, Reihenfolge nach den Gäste-Sprachen (offen in sprachen.json); Sprachwechsel an derselben Stelle', '–'),
]

GESTRICHEN = [
    ('Türflügel oder Tor-Effekt im Auftakt', 'Robert: kein Vorhang, kein Tor, keine Türflügel, «überall bitte». Das Tor bleibt ein Foto.'),
    ('Die acht Winde als Kapitelstruktur der ganzen Startseite', 'Kapitelzeilen sind auf der Website verboten, und die Winde gehören Sa Clastra. Sie tragen nur diesen einen Abschnitt.'),
    ('Ein eigenes Band mit grossen Zahlen auf der Startseite', 'Carlton, Grand Beau-Rivage und Ruedihus haben es schon. Die Zahlen des Guts stehen als Hotelkarten-Zeile unter dem Plan, gross zählen sie nur auf der Unterseite «Das Gut».'),
    ('Das Startvideo (23 MB) als Auftakt', 'Befund 1.1. Filme nur stumm, im Bild, als Standbild bis geladen: der Winde-Film in Sa Clastra.'),
    ('Wetter beim Buchen oder auf der Region-Seite', 'Robert hat es aus allen Seiten gestrichen.'),
    ('Instagram-Wand auf der Startseite', 'Ohne Anmeldung sind nur zwölf Beiträge erreichbar; die heutige Seite zeigt sie als Fremdbaustein.'),
    ('Treppenreihe (versetzte Fotos) für die Feste', 'Kacheln auf verschiedener Höhe hat Robert abgelehnt.'),
    ('Hochzählende Bewertungen', 'Das hat das Grand Beau-Rivage; beim Carlton wollte Robert es nicht. Hier stehen die Zahlen still.'),
    ('Bühne mit Abzügen (Polaroids)', 'Salt & Silver und Ruedihus haben sie, Gasterntal die Paare. Das Castell nimmt die Bildwand und den Ziegelverband.'),
    ('«Herzlich willkommen» als zweiter Abschnitt', 'Doldenhorn und Gasterntal beginnen so. Das Castell begrüsst mit dem Plan des Guts.'),
    ('Farbwelt B «Oliv und Messing»', 'Robert hat am 15.10.2026 Welt A «Stein und Nacht» gewählt. Kein Grün als Fläche.'),
    ('Wahl «Wofür kommen Sie?» / «Worauf freuen Sie sich?»', 'Carlton, Doldenhorn und Ruedihus haben eine Wahl im zweiten oder dritten Abschnitt. Beim Castell führt der Plan zu den Orten.'),
    ('Ticket / Billett', 'Vorerst nur Carlton und Grand Beau-Rivage (Robert 15.10.2026). Angaben stehen auf Platten mit Kuhle.'),
]

OFFEN = [
    ('Prompt-Datei des Hauses mit Denkanstössen (Abschnitt 4) liegt nicht vor; der erste Moment ist ohne sie entworfen', 'Projektordner Castell Son Claret, kein «Prompt — Castell Son Claret.md»'),
    ('Terrace Deluxe: laut Zimmertext «im Hauptgebäude und im Garten», auf der Bildwand dem Castell zugeordnet', '_quelle/website/text/de__suiten-zimmer__terrace-deluxe.md'),
    ('Siegel (Michelin, Leading Hotels, EarthCheck) liegen nur in 250 px vor; Druckqualität fehlt', '_quelle/website/bilder/250x25_*'),
    ('Castell Classics: Programm 2026 steht auf keiner Seite', 'Potenzialanalyse 7.3'),
    ('Saison von Sa Clastra und Winterpause des Hauses: zwei Angaben auf der Seite', 'Potenzialanalyse 3.2; fakten.json › saison_winterpause'),
    ('Anreise-Zahlen (Flughafen 32 oder 34 km, Palma 25 oder 30 Minuten) und die gültige Telefonnummer', 'Potenzialanalyse 10.2, 10.3; fakten.json › telefon, anreise'),
    ('Gästesätze für die Szene «Was Gäste sagen»: keine Bewertungstexte im Material (TripAdvisor und Google nicht abgelesen)', '_quelle/extern/portale; notizen.md'),
    ('Foto des Fontenay für die Schwesterhaus-Karte im Fuss: Herkunft und Rechte prüfen', '_fontenay-und-castell/_quelle/fontenay/website/bilder/local_The_Fontenay_Drohne.jpg (herkunft.json)'),
    ('Karte der Castell Bar liegt nur als Bild-PDF vor; Wortlaut muss aus dem Bild gelesen werden', '_quelle/website/pdf/17544796039099_CASTELL_20BAR_202025_20_284_29.pdf'),
    ('Archivbilder des Guts (vor 2013) für die Geschichte: keine im Material', '_quelle/website/bilder, extern/wikipedia-commons'),
]


# ---------------------------------------------------------------- die Seite
def seite():
    flaechen = {'hell': 'papier', 'creme': 'creme tapete-h', 'tapete': 'creme tapete-h', 'dunkel': 'marine tapete', 'foto': 'papier'}
    szenen_html = ''
    nr = 0
    for s in SZENEN:
        if s['teil'].startswith('fenster'):
            szenen_html += fenster(s['fotos'][0][0], s['titel'][1:], s['satz'] + (' <span class="vonmir">von mir</span>' if s.get('vonmir') else ''), s['fotos'][0][2])
            nr += 1
            szenen_html += szene(s, nr, 'papier')
        else:
            nr += 1
            szenen_html += szene(s, nr, flaechen[s['flaeche']])
    lauf = ''.join(f'<a href="#s-{s["teil"]}" data-r style="--i:{i}"><i class="fl fl--{s["flaeche"]}"></i><b>{i + 1:02d}</b><span>{e(s["titel"][0] + " " + s["titel"][1])}</span></a>' for i, s in enumerate(SZENEN))
    unter_html = ''.join(f'<li data-r style="--i:{i % 4}"><div class="us__k"><b>{e(n)}</b><small class="mono">{e(d)}</small><small>{e(h)}</small></div><div class="us__t"><p>{e(t)}</p><p class="us__b"><span>Bausteine</span> {e(b)}</p></div></li>' for i, (d, n, h, t, b) in enumerate(UNTERSEITEN))
    gestr_html = ''.join(f'<li data-r style="--i:{i % 4}"><b>{e(w)}</b><span>{e(g)}</span></li>' for i, (w, g) in enumerate(GESTRICHEN))
    offen_html = ''.join(f'<li data-r style="--i:{i % 4}"><b>{e(p)}</b><span class="mono">{e(w)}</span></li>' for i, (p, w) in enumerate(OFFEN))
    haeuser = ''.join(f'<li style="--i:{i}"><b><a href="{e(LIVE[h])}" target="_blank" rel="noopener">{e(h)}</a></b><span>{e(t)}</span></li>' for i, (h, t) in enumerate(B.EIGENE_WELT['unterschied_zu'].items()))
    v_css = int(os.path.getmtime(os.path.join(M5, 'marke', 'marke.css')))
    v_js = int(os.path.getmtime(os.path.join(M5, 'marke', 'marke.js')))
    GOLD = '<linearGradient id="tgold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F3E8CC"/><stop offset=".34" stop-color="#DCC68F"/><stop offset=".52" stop-color="#C0A062"/><stop offset=".62" stop-color="#8F7445"/><stop offset=".8" stop-color="#D2B97F"/><stop offset="1" stop-color="#EBDCB1"/></linearGradient>'
    defs = B.sym_defs().replace('</defs>', GOLD + '</defs>')
    KAP = [('geschichte', 'Geschichte'), ('s-auftakt', 'Startseite'), ('unterseiten', 'Unterseiten'), ('nummer10', 'Nummer 10'), ('gestrichen', 'Gestrichen'), ('offen', 'Offen')]
    nav = ''.join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAP)
    index = ''.join(f'<a href="#{k}" data-r style="--i:{i}"><span>{e(n)}</span></a>' for i, (k, n) in enumerate(KAP))
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Konzept-Board · Castell Son Claret</title>
<meta name="description" content="Die Geschichte der neuen Website des Castell Son Claret: jede Szene mit echten Fotos, Baustein, Bewegung, Fläche und dem Unterschied zu allen bisherigen Häusern. Intern, Station 06 der Kette.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['Nacht']}">
<link rel="preload" href="{MARKE}/schriften/fahkwang-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{MARKE}/schriften/montserrat-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{MARKE}/marke.css?v={v_css}">
<link rel="stylesheet" href="konzept.css?v={int(os.path.getmtime(os.path.join(H, 'konzept.css')))}">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
{defs}

<nav class="leiste" aria-label="Konzept-Board">
  <a class="leiste__m" href="#oben">{B2.zeichen()}<span><b>Konzept-Board</b><small>Station 06 · Castell Son Claret</small></span></a>
  <div class="leiste__k">{nav}</div>
  <a class="glanz" href="{MARKE}/markenbuch.html" target="_blank" rel="noopener">Markenbuch{PF}</a>
</nav>

<main>
<section class="titel tapete" id="oben">
  <div class="titel__in">
    <p class="titel__kap" data-r="hero" style="--i:0"><i></i><b>Konzept-Board · Oktober 2026 · intern</b><i></i></p>
    <div class="titel__z" data-r="zeichen">{B2.zeichen('', 'Die drei Türme').replace('fill="currentColor"', 'fill="url(#tgold) #C0A062"')}</div>
    <h1 class="titel__w" data-r="maske"><span class="z"><span>{B2.name().replace('fill="currentColor"', 'fill="url(#tgold) #C0A062"')}</span></span></h1>
    <p class="titel__ort" data-r="hero" style="--i:2">Es Capdellà <span class="raute"></span> ein Gang über das Gut</p>
    <p class="titel__lead" data-r="hero" style="--i:3">{e(GESCHICHTE)}</p>
    <div class="knr knr--mitte" data-r="hero" style="--i:4">{B2.kn('Die Szenen', '#s-auftakt')}{B2.kn('Markenbuch', MARKE + '/markenbuch.html', 'kn--linie', neu=True)}</div>
  </div>
  <nav class="index" aria-label="Inhalt" data-g>{index}</nav>
  <span class="titel__runter" aria-hidden="true"><i></i></span>
</section>

<section class="ab blatt papier" id="geschichte">
  <div class="in">
    {B2.kopf('Die Geschichte', ['Vom Tor im Mittag', 'bis zum Castell bei Nacht.'], 'Die Startseite erzählt einen Aufenthalt als Gang über das Gut, in der Reihenfolge, in der ein Gast das Anwesen erlebt: durch das Tor, auf den Plan des Guts, zu den Häusern, in denen man wohnt, an den Tisch im Garten, am Abend in den Hof von Sa Clastra, ans Wasser, zu den Festen, zum Angebot und zurück zum Castell bei Nacht. Hell wie der Tag auf dem Gut; dunkel nur dort, wo das Haus es selbst ist. Vierzehn Szenen, drei Fenster, ein dunkler Abschnitt. Farbwelt A «Stein und Nacht».')}
    <div class="drei" data-g>
      {kachel('tor', 'Mittag: das Tor.', 'Hell, Sandstein, die Wortmarke in der Toröffnung.', 0, '50% 55%')}
      {kachel('luftbild', 'Das Gut: der Plan.', 'Orte statt Kategorien: Castell, Innenhof, Garten, Pool, Wasserturm, Hof, Tafona.', 1, '50% 45%')}
      {kachel('allee-nacht', 'Nacht: Sa Clastra.', 'Die eine dunkle Fläche mit der Windrose, dann das Castell bei Nacht.', 2, '50% 45%')}
    </div>
    <div class="lauf-szenen" data-g>{lauf}</div>
  </div>
</section>

{szenen_html}

<section class="ab blatt creme tapete-h" id="unterseiten">
  <div class="in">
    {B2.kopf('Unterseiten', ['Alles, was das Haus', 'heute hat, neu gedacht.'], 'Aus der Seitenliste der Station 02: 302 Seiten in vier Sprachen, davon je Sprache rund 75. Neu geordnet nach Orten und Anliegen, jede Seite mit Seitenkopf in der Sprache des Auftakts, kürzeren Szenen, ein bis zwei Fenstern, Ausklang-Zeile. Buchungsmasken bleiben (Profitroom, CoverManager, Spalopia), kein Klick führt mehr ins alte Design. Was fehlt, kommt dazu: Vor Ihrer Anreise, Rezeption im Chat, 404, AGB und Widerruf (offen).')}
    <ul class="us" data-g>{unter_html}</ul>
  </div>
</section>

<section class="ab blatt marine tapete" id="nummer10">
  <div class="in">
    {B2.kopf('Projekt Nummer 10', ['Womit es sich von jedem', 'bisherigen Haus unterscheidet.'], 'Vor dieser Station wurden die Startseiten und Zimmerseiten aller bisherigen Häuser gelesen (Abschnittsfolge aus dem Code, UI-Fundus «Bereiche»). Oben steht bei jeder Szene der Unterschied nebeneinander; hier je Haus in einem Satz. Gleich dürfen Knöpfe, Kacheln, Tapete, Hereinschweben sein; eigen sind Aufbau, Zimmer-Darstellung, tragende Bausteine, Bewegung und Rhythmus.')}
    <ul class="unter" data-g>
      <li style="--i:0"><b>Castell Son Claret</b><span>Gang über das Gut: Tor im Mittag · Plan des Guts · Bildwand der Häuser mit Fach · Tisch vom Garten her · Windrose als bewegtes Element im einzigen dunklen Abschnitt · Wasser als Band · Feste als Ziegelverband · Platten für Angebote · stille Note und Team · Castell bei Nacht. Drei Fenster: Berg, Allee, Konzert.</span></li>
      {haeuser}
    </ul>
    <div class="knr knr--mitte" data-r>{B2.kn('UI-Fundus: Hotel bauen', FUNDUS_B + 'auftakt', neu=True)}{B2.kn('Markenbuch, eigene Welt', MARKE + '/markenbuch.html#welt', 'kn--linie', neu=True)}</div>
  </div>
</section>

<section class="ab blatt papier" id="gestrichen">
  <div class="in">
    {B2.kopf('Gestrichen', ['Überlegt', 'und verworfen.'], 'Damit kein anderer Chat es wieder aufmacht: Was es auf dieser Website nicht gibt, und warum.')}
    <ul class="gs" data-g>{gestr_html}</ul>
  </div>
</section>

<section class="ab blatt creme tapete-h" id="offen">
  <div class="in">
    {B2.kopf('Offen', ['Was nicht belegt ist,', 'bleibt offen.'], 'Zehn Punkte, jeder mit Fundstelle. Sie stehen auch in stand.json und auf der Karte. Dazu gelten weiter die offenen Punkte der Stationen 03 und 05 (Telefon, Saison, Zimmerkategorien, Schrift der Wortmarke, Herkunft der Rosette).')}
    <ul class="gs gs--rot" data-g>{offen_html}</ul>
  </div>
</section>

<section class="ab blatt marine tapete schluss" id="ende">
  <div class="in">
    <div class="ende" data-r="ende">
      <span class="strich strich--gross">{B2.zeichen()}</span>
      <p class="ende__w">{B2.name()}</p>
      <p class="ende__s">Konzept-Board Castell Son Claret · Station 06 der Kette · intern, geht nie an den Kunden · Tasty Studios, Oktober 2026. Nächste Station: der Baumeister baut Szene für Szene, Robert bestätigt je Abschnitt.</p>
      <div class="knr knr--mitte">{B2.kn('Markenbuch', MARKE + '/markenbuch.html', neu=True)}{B2.kn('Die Probe', MARKE + '/probe.html', 'kn--linie', neu=True)}{B2.kn('Potentialanalyse', 'https://castell-son-claret-analyse.vercel.app', 'kn--linie', neu=True)}</div>
    </div>
  </div>
</section>
</main>
<script src="{MARKE}/marke.js?v={v_js}" defer></script>
</body>
</html>
'''


def konzept_json():
    seiten = [{'seite': 'index.html', 'titel': 'Startseite: ein Gang über das Gut',
               'szenen': [{k: s[k] for k in ('teil',)} | {
                   'titel': ' '.join(s['titel']), 'satz': s['satz'] + (' (von mir)' if s.get('vonmir') else ''), 'bilder': s['bilder'], 'baustein': s['baustein'], 'quelle': s['quelle'],
                   'skizze': s.get('skizze', ''), 'bewegung': s['bewegung'], 'flaeche': s['flaeche'], 'unterschied': s['unterschied'], 'bisher': s['bisher'],
                   'bisher_links': {h: LIVE.get(h, '') + a for h, a in s['bisher_anker'].items()}} for s in SZENEN]}]
    for datei, name, heute, text, bausteine in UNTERSEITEN:
        seiten.append({'seite': datei, 'titel': name, 'heute': heute, 'szenen': [{'teil': re.sub(r'[^a-z0-9]+', '-', datei.split('.')[0].lower()).strip('-') or 'seite', 'titel': name, 'satz': text, 'baustein': bausteine, 'quelle': 'fundus' if 'neu' not in bausteine else 'neu'}]})
    return {'haus': 'Castell Son Claret', 'stand': '2026-10-15', 'geschichte': GESCHICHTE, 'farbwelt': 'A «Stein und Nacht»', 'seiten': seiten,
            'gestrichen': [{'was': w, 'grund': g} for w, g in GESTRICHEN], 'offen': [{'punkt': p, 'wo': w} for p, w in OFFEN], 'familie_machart': None,
            'quellen': ['_kette/02-spaeher/seitenliste.json', '_kette/03-sammler/fakten.json', '_kette/05-markenbauer/marke.json',
                        '_fontenay-und-castell/Website-Potenzialanalyse — Castell Son Claret.md', '_fontenay-und-castell/Markenanalyse — The Fontenay & Castell Son Claret.md',
                        '_quelle/website/text/de__*.md', '_quelle/website/pdf/16905351550762_Castell-Son-Claret-Map.pdf', '_quelle/website/pdf/17424632450264_Rosa_20de_20los_20vientos_20-_20GER.pdf']}


if __name__ == '__main__':
    bilder_bauen()
    open(os.path.join(H, 'konzept.html'), 'w', encoding='utf-8').write(seite())
    json.dump(konzept_json(), open(os.path.join(H, 'konzept.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('gebaut: konzept.html, konzept.json, bilder/')
