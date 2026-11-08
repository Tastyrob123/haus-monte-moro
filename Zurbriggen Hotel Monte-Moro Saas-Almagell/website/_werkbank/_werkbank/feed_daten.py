"""Instagram-Feed des Hotels Monte-Moro als Idee (Werkbank Papier, 08.11.2026). Bauart aus dem Feed der Vorlage
(Kit feed.py mit REGEL 'bogen', feed_bogen.py), Konzept eigen für dieses Haus (Master 5a, Regel 10a; Gegenprobe in feed-bestand.md).

Das Profil heute: @hotelmonte_moro, «Hotel Monte Moro | Restaurant Röstihüs | Saas-Almagell», 19 Beiträge, 173 Follower, 1 gefolgt
(_quelle/extern/ig/profil.txt). Neuester eigener Beitrag: 21.09.2026. Im Profil der Werkbank stehen die zehn eigenen Beiträge mit Bild aus
_quelle/extern/ig/ (herkunft.json, nur Konto hotelmonte_moro) unter den neuen (feed_leicht.py).

Konzept «Am Grat»: Das Haus erzählt sich in drei Kapiteln, je ein Panorama des Saastals über eine ganze Reihe (drei Beiträge ergeben ein Bild,
wie die Grat-Kante der Website die Fotos oben fasst): Sommer im Tal, Winter auf den Gletschern, der Stausee Mattmark. Dazwischen je zwei
Reihen aus dem Haus: Zimmer, Frühstück, Röstihüs, Stübli, Empfang, und je Reihe genau eine Tafel mit einem Satz der Website
(«Mehr erleben, weniger zahlen.», «Bei uns scheint fast immer die Sonne.», «Zwei Minuten bis zum Lift.», «Es lebe die Tradition!»,
«Wein von Fabian.», «Willkommen im Monte-Moro.») und einmal der Bon der Rezeption mit allem, was inklusive ist. Der Platz der Tafel wandert.
30 Beiträge, nur Fotos der Website (website/assets/img, keine Gästefotos, nichts Erzeugtes, nichts, was schon gepostet ist: feed_bestand.py).
Kleid: Nacht und Papier, Lärche nur im Bergkamm und im letzten Wort, Messing als feine Linie; Fjalla One, Instrument Sans, DM Mono.
Texte zu den Beiträgen: Tasty Studios, nur mit Fakten aus website/inhalt/daten.py; Sie-Ansprache, Schweizer Schreibung."""
import os
import feed_bogen

_HIER = os.path.dirname(os.path.abspath(__file__))
_WB = os.path.dirname(_HIER)
_WEB = os.path.dirname(_WB)
_HAUS = os.path.dirname(_WEB)


def quelle(key):
    """Grösste Fassung des Fotos der Website (website/assets/img/<key>-<x|l|m|s>.webp)."""
    for a in ('x', 'l', 'm', 's'):
        p = os.path.join(_WEB, 'assets', 'img', f'{key}-{a}.webp')
        if os.path.exists(p):
            return p
    raise FileNotFoundError(key)


# Zeichen und Wortmarke als Bild je Farbe (aus dem Kleid, unverändert; die Tafeln werden über Dateien gesetzt)
_FEED = os.path.join(_WB, 'feed')
os.makedirs(_FEED, exist_ok=True)
_KLEID = os.path.join(_HAUS, '_werkzeuge', 'oberflaeche', 'kleid')
_Z = open(os.path.join(_KLEID, 'montemoro-zeichen.svg'), encoding='utf-8').read()
_M = open(os.path.join(_KLEID, 'montemoro-marke.svg'), encoding='utf-8').read()
for _n, _f in (('laerche', '#C67144'), ('papier', '#F5F2EE')):
    open(os.path.join(_FEED, f'zeichen-{_n}.svg'), 'w', encoding='utf-8').write(_Z.replace('<svg ', f'<svg color="{_f}" ', 1))
for _n, _f in (('papier', '#F5F2EE'), ('blau', '#115595')):
    _s = _M.replace('<svg xmlns="http://www.w3.org/2000/svg"', f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" color="{_f}" fill="{_f}"', 1)
    if '<use' not in _s:
        _s = _s.replace('</svg>', '<use href="#wm" xlink:href="#wm" width="3483" height="1425"/></svg>')
    open(os.path.join(_FEED, f'marke-{_n}.svg'), 'w', encoding='utf-8').write(_s)
for _alt in ('marke-rot.svg', 'marke-creme.svg', 'marke-nacht.svg'):   # Zeichen eines anderen Hauses
    if os.path.exists(os.path.join(_FEED, _alt)):
        os.remove(os.path.join(_FEED, _alt))

PROFIL = {'name': 'hotelmonte_moro', 'titel': 'Hotel Monte Moro | Restaurant Röstihüs | Saas‑Almagell', 'art': 'Hotel',
          'bio': ['Hotel und Restaurant Röstihüs in Saas-Almagell, Wallis', 'Mehr erleben, weniger zahlen.', 'Ihre Gastgeber Esther und Fabian Zurbriggen'],
          'link': 'monte-moro.ch',
          'zahlen': {'beitraege': '19', 'follower': '173', 'gefolgt': '1'}, 'stand': 'Profil laut Instagram'}
HIGHLIGHTS = [('Zimmer', quelle('z-dach'), .5), ('Röstihüs', quelle('roesti-tische'), .5), ('Saastal', quelle('mattmark'), .5),
              ('Frühstück', quelle('fruehstueck'), .5), ('Spa', quelle('spa-garten'), .5)]
TON = (.99, 1.03, 1.0, 1.0)
REGEL = 'bogen'
SEITE = dict(
    titel=['Am', 'Grat.'],
    text1='Ihr Feed bleibt, wie er ist. Darauf bauen die nächsten 30 Beiträge auf: drei Kapitel, je mit einem Panorama des Saastals über eine ganze Reihe, '
          'dem Sommer im Tal, dem Winter auf den Gletschern und dem Stausee Mattmark. Dazwischen das Haus, das Röstihüs, das Stübli und je eine Tafel mit einem Satz Ihrer Website.',
    text2='Kein Foto, das schon auf Ihrem Profil steht, kommt noch einmal vor. Mit dem Schalter sehen Sie Ihren Feed heute und mit den nächsten 30; die Nummern zeigen die Reihenfolge zum Posten.',
    aufbau='Drei Panoramen über je eine Reihe, dazwischen Haus und Röstihüs, je Reihe eine Tafel',
    texte='Ideen von mir, die Sätze auf den Tafeln stammen von Ihrer Website',
    bilder='Ihre eigenen Fotos von der Website, die noch nie gepostet wurden')

_F = "url('../assets/fonts/{}') format('woff2')"
BOGEN_CSS = (
    f"@font-face{{font-family:'Fjalla One';src:{_F.format('FjallaOne-400.woff2')};font-weight:400}}"
    f"@font-face{{font-family:'Instrument Sans';src:{_F.format('InstrumentSans-normal-400_600.woff2')};font-weight:400 600}}"
    f"@font-face{{font-family:'DM Mono';src:{_F.format('DMMono-normal-400.woff2')};font-weight:400}}"
    '.st{--nacht:#0A2A4A;--nachtblau:#0D3F6F;--papier:#F5F2EE;--creme:#EFE9E1;--laerche:#C67144;--laerche-t:#9A4F2B;--messing:#B39867;--tinte:#13263A;--grau:#4A5D70}'
    '.n,.w,.b{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:170px 130px}'
    '.n{background:radial-gradient(120% 90% at 50% 0%,#0D3F6F 0%,#0A2A4A 64%);color:var(--papier)}'
    '.w{background:var(--papier);color:var(--nacht)}'
    '.zk{position:absolute;top:168px;left:50%;width:150px;height:auto;transform:translateX(-50%)}'
    '.ki{font:400 24px/1.3 "DM Mono",monospace;letter-spacing:.22em;text-transform:uppercase;color:var(--messing);margin:0 0 40px}'
    '.w .ki{color:var(--laerche-t)}'
    '.ti{font:400 132px/1.02 "Fjalla One",sans-serif;margin:0;text-wrap:balance}'
    '.ti em{font-style:normal;color:var(--laerche)}.w .ti em{color:var(--laerche-t)}'
    '.li{width:110px;height:2px;background:var(--messing);margin:56px auto 0}'
    '.sa{margin:44px 0 0;max-width:720px;font:400 38px/1.45 "Instrument Sans",sans-serif;text-wrap:balance;opacity:.9}'
    '.fu{position:absolute;bottom:150px;left:150px;right:150px;margin:0;font:400 22px/1.3 "DM Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--messing)}'
    '.w .fu{color:var(--grau)}'
    '.wm{position:absolute;bottom:140px;left:50%;width:260px;height:auto;transform:translateX(-50%)}'
    # der Bon der Rezeption: Papier auf der Nacht, unten gezackt
    '.b{background:radial-gradient(120% 90% at 50% 0%,#0D3F6F 0%,#0A2A4A 64%);padding:0}'
    '.bon{position:relative;width:640px;padding:70px 64px 90px;background:var(--papier);color:var(--nacht);text-align:left;'
    'clip-path:polygon(0 0,100% 0,100% calc(100% - 24px),95% 100%,90% calc(100% - 24px),85% 100%,80% calc(100% - 24px),75% 100%,70% calc(100% - 24px),65% 100%,60% calc(100% - 24px),55% 100%,50% calc(100% - 24px),45% 100%,40% calc(100% - 24px),35% 100%,30% calc(100% - 24px),25% 100%,20% calc(100% - 24px),15% 100%,10% calc(100% - 24px),5% 100%,0 calc(100% - 24px))}'
    '.bon .ki{text-align:center;color:var(--grau);margin-bottom:26px}'
    '.bon .bt{font:400 70px/1 "Fjalla One",sans-serif;text-align:center;margin:0 0 30px}'
    '.bon ul{list-style:none;margin:0;padding:0}'
    '.bon li{display:flex;justify-content:space-between;align-items:baseline;padding:16px 0;border-bottom:2px dashed #D6CCC1;font:400 40px/1.1 "Fjalla One",sans-serif}'
    '.bon li span{font:400 22px/1 "DM Mono",monospace;letter-spacing:.14em;color:var(--laerche-t)}'
    '.bon .to{display:flex;justify-content:space-between;align-items:baseline;padding-top:22px;font:400 50px/1 "Fjalla One",sans-serif}'
    '.bon .to span{font:400 26px/1 "DM Mono",monospace;letter-spacing:.14em;color:var(--laerche-t)}'
)


def tafel(titel, satz='', fuss='', ton='n', kicker='', marke=False):
    """Satz des Hauses auf Nacht (n) oder Papier (w), oben der Bergkamm in Lärche, unten wahlweise die Wortmarke."""
    zk = '<img class="zk" src="zeichen-laerche.svg" alt="">'
    wm = f'<img class="wm" src="marke-{"papier" if ton == "n" else "blau"}.svg" alt="">' if marke else ''
    return (f'<div class="{ton}">{zk}' + (f'<p class="ki">{kicker}</p>' if kicker else '') + f'<p class="ti">{titel}</p><i class="li"></i>'
            + (f'<p class="sa">{satz}</p>' if satz else '') + (f'<p class="fu">{fuss}</p>' if fuss else '') + wm + '</div>')


def bon():
    posten = ''.join(f'<li>{k}<span>INKL.</span></li>' for k in ('Postauto', 'Bergbahnen', 'Frühstück', 'Raclette', 'Kidsclub', 'Parkplatz'))
    return (f'<div class="b"><div class="bon"><p class="ki">Der Bon der Rezeption</p><p class="bt">Ihr Aufenthalt</p><ul>{posten}</ul>'
            f'<div class="to">Total<span>INKLUSIVE</span></div></div></div>')


F = lambda key, fx=.5, fy=.5: dict(art='foto', bild=quelle(key), fx=fx, fy=fy)
T = lambda html: dict(art='html', html=html)

# Raster von oben (neuester Beitrag) nach unten; Reihe, Spalte, Breite, Stück, Texte (ein Text je gedecktem Feld)
STUECKE = [
    (0, 0, 3, F('tal-sommer', .5, .5), ['Das Saastal im Sommer: über 250 km Wanderwege, vom einfachen Spaziergang bis zum Viertausender.',
                                         'Mittendrin liegt Saas-Almagell. Das Postauto im ganzen Saastal ist bei uns im Zimmerpreis inklusive.',
                                         'Im Sommer auch alle Bergbahnen im Saastal, ausser der Metro Alpin. Mehr erleben, weniger zahlen.']),
    (1, 0, 1, F('haus-sommer-g', .5, .5), ['Das Hotel Monte-Moro im Sommer, mit den Balkonen aus Lärche und der Sonnenterrasse vor dem Haus.']),
    (1, 1, 1, T(tafel('Mehr erleben, <em>weniger zahlen.</em>', 'Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag.', 'Hotel Monte-Moro · Saas-Almagell')),
     ['Mehr erleben, weniger zahlen. Zimmer mit Frühstück ab CHF 90.00 pro Person und Tag, Postauto und im Sommer die Bergbahnen inklusive.']),
    (1, 2, 1, F('roesti-raum', .45, .5), ['Das Röstihüs. Unsere Gäste sagen, hier gebe es die wohl besten Röstis und Cordon bleus der Region.']),
    (2, 0, 1, T(bon()), ['Der Bon der Rezeption: Postauto, Bergbahnen im Sommer, Frühstücksbuffet, Racletteabend mit Halbpension, Kidsclub und Parkplatz. Alles schon dabei.']),
    (2, 1, 1, F('fr-tisch', .5, .5), ['Unten ist das Frühstück gedeckt. Das Buffet gehört zu jedem Zimmer.']),
    (2, 2, 1, F('balkon', .5, .5), ['Die Sonne steht schon über dem Balkon. Alle Zimmer im Monte-Moro haben einen.']),
    (3, 0, 1, F('alpenrosen', .62, .5), ['Alpenrosen über dem Saastal. Im Sommer ein herrliches Wanderparadies.']),
    (3, 1, 1, F('murmeltiere', .5, .5), ['Murmeltiere im Saastal, gleich neben den Wanderwegen.']),
    (3, 2, 1, T(tafel('Bei uns scheint fast immer <em>die Sonne.</em>', 'Bei schönem Wetter auf der Sonnenterrasse direkt vor dem Haus.', '', 'w')),
     ['Bei uns scheint fast immer die Sonne. Dann sitzen Sie auf der Sonnenterrasse direkt vor dem Haus.']),
    (4, 0, 3, F('gletscher', .5, .5), ['Winter im Saastal: Skifahren bis auf 3500 m in Saas-Fee.',
                                       'Saas-Grund bis 3200 m, Saas-Almagell bis 2400 m. Drei Skigebiete in einem Tal.',
                                       'Alle 30 Minuten bringt Sie ein Bus ins Skigebiet Saas-Grund oder Saas-Fee, das Postauto ist inklusive.']),
    (5, 0, 1, F('haus-winter-g', .5, .5), ['Das Monte-Moro im frischen Schnee.']),
    (5, 1, 1, T(tafel('Zwei Minuten <em>bis zum Lift.</em>', 'Zwei Gehminuten zum Skigebiet, drei zur Busstation, drei ins Dorf.', 'Ab dem Haus · Gehminuten laut Haus')),
     ['Zwei Gehminuten zum Skigebiet Saas-Almagell, drei zur Busstation, drei ins Dorf. Das Hotel liegt an bester Lage.']),
    (5, 2, 1, F('dorf-winter', .55, .5), ['Saas-Almagell im Winter. Einkaufen, Bankomat und Tourismusbüro sind drei Gehminuten entfernt.']),
    (6, 0, 1, T(tafel('Es lebe <em>die Tradition!</em>', 'Elf Röstis und fünf Cordon bleus auf der Karte des Röstihüs.', 'Restaurant Röstihüs', 'w')),
     ['Es lebe die Tradition! Die Rösti Tschug Tschug wird mit Calvados flambiert, die Rösti Saastal kommt mit Spiegelei.']),
    (6, 1, 1, F('stuebli', .4, .5), ['Das Stübli. Einmal in der Woche ist hier Racletteabend für alle mit Halbpension.']),
    (6, 2, 1, F('z-hell', .5, .5), ['Schöne Hotelzimmer, schöne Ferien. Alle mit Dusche oder Bad, Safe und Balkon.']),
    (7, 0, 1, F('empfang', .55, .5), ['Der Empfang, an der Wand der Bergkamm des Hauses. Willkommen.']),
    (7, 1, 1, F('see-blumen', .5, .6), ['Blumen am Mattmarksee. Ein Tagesausflug im Saastal, mit dem Postauto inklusive.']),
    (7, 2, 1, T(tafel('Wein <em>von Fabian.</em>', 'Zwei Hotelweine, von Fabian selbst kreiert.', 'Im Röstihüs')),
     ['Wein von Fabian: zwei Hotelweine, die Fabian selbst kreiert hat. Im Röstihüs zur Rösti oder zum Cordon bleu.']),
    (8, 0, 3, F('stausee', .5, .5), ['Der Stausee Mattmark.', 'Ein Tagesausflug aus dem Saastal, wie ihn das Haus empfiehlt.', 'Und am Abend zurück ins Röstihüs.']),
    (9, 0, 1, F('wasserfall', .55, .5), ['Ein Wasserfall im Saastal. In der Alpin Gorge geht es mit einem Bergführer durch eine Gebirgsbachschlucht.']),
    (9, 1, 1, T(tafel('Willkommen <em>im Monte-Moro.</em>', 'Ihre Gastgeber Esther und Fabian Zurbriggen.', '', 'w', '', True)),
     ['Willkommen im Monte-Moro. Ihre Gastgeber Esther und Fabian Zurbriggen.']),
    (9, 2, 1, F('fr-detail', .5, .5), ['Konfitüren und Brot am Buffet. Guten Morgen aus Saas-Almagell.']),
]

BOGEN = []
for _r, _c, _w, _st, _texte in STUECKE:
    _kurz = os.path.basename(_st['bild']).rsplit('-', 1)[0] if _st['art'] == 'foto' else f'tafel{_r}{_c}'
    BOGEN.append(dict(id=f'{_r + 1:02d}{_c + 1}-{_kurz}', r=_r, c=_c, w=_w, h=1, texte=_texte, **_st))
P = feed_bogen.p_liste(BOGEN)
assert len(P) == 30, len(P)
BISHER = 19   # Beiträge auf @hotelmonte_moro heute (profil.txt); im Profil der Werkbank stehen die zehn eigenen mit Bild unter den neuen
PROFIL['zahlen']['beitraege'] = str(len(P) + BISHER)
IG_BESTAND = ['../../_quelle/extern/ig/ig-*.jpg']   # alle Bilder aus dem Instagram-Material (auch die des Partnerhotels) für den Abgleich
BESTAND_AUSNAHMEN = ()
BESTAND_KANDIDATEN = []
