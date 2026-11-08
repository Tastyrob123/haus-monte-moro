#!/usr/bin/env python3
"""Das Markenbuch · Hotel Monte-Moro, Saas-Almagell: die Hausregeln (buch.html, Stil in buch/buch.css, Druck in buch.js), gebaut aus livre.json,
dem Markenbuch der Station 05 (_kette/05-markenbauer/marke/markenbuch.html: Haltung, Zeichen, Farben, Schrift, Tapete, Bilder, Bausteine, Logo richtig
und falsch, Worte des Hauses) und den Hauswerten der Website (website/inhalt/daten.py, per ast gelesen). Aufbau wie die Hausregeln im Stamm (Titel,
Kapitel als Blätter, Fenster, Leiste mit «Als PDF sichern»), Inhalt und Kleid des Hauses. Fotos aus der Website (/assets/img), Zeichen aus dateien/ (bau.py).

   python3 _werkzeuge/livre/buch.py      (nach bau.py)"""
import ast, hashlib, html, json, os, re

e = html.escape
nb = lambda t: re.sub(r' (\S+)$', r'&nbsp;\1', e(t))   # nur das letzte Leerzeichen fest: kein Einzelwort in der letzten Zeile
HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))
L = json.load(open(os.path.join(HIER, 'livre.json'), encoding='utf-8'))
FOTO = {f['k']: f for f in L['fotos']}
FARBE = {f['k']: f for f in L['farben']}
S = 'monte-moro'


def daten(name):
    """Ein Wert aus website/inhalt/daten.py, ohne die Datei auszuführen."""
    baum = ast.parse(open(os.path.join(PROJEKT, 'website', 'inhalt', 'daten.py'), encoding='utf-8').read())
    for n in baum.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            if isinstance(n.value, ast.Call):
                return {k.arg: ast.literal_eval(k.value) for k in n.value.keywords}
            return ast.literal_eval(n.value)
    raise SystemExit(f'{name} fehlt in daten.py')


HAUS = daten('HAUS')


def _v(n):
    p = os.path.join(HIER, n)
    return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10] if os.path.exists(p) else '1'


def bild(k, alt=None, pos='50% 50%', gross=False, lazy=False):
    f = FOTO[k]
    st = [x for x in f['sw'] if x[0] <= 1500] or f['sw'][:1]
    srcset = ', '.join(f'{p} {w}w' for w, p in st)
    return (f'<img src="{f["fm"]}" srcset="{srcset}" sizes="{"100vw" if gross else "(max-width:900px) 100vw, 34vw"}" alt="{e(alt or f["t"]["de"])}"'
            f' width="{f["w"]}" height="{f["h"]}"{" loading=\"lazy\"" if lazy else ""} style="object-position:{pos}">')


def symbole():
    """Wortmarke und Bergkamm einmal als Symbol (Pfade aus dateien/, gebaut von bau.py aus dem Markenbuch), jede Verwendung über <use>, Farbe über color."""
    aus = []
    for form, sid in (('wortmarke', 'wm'), ('bergkamm', 'bk')):
        s = open(os.path.join(HIER, 'dateien', f'{S}-{form}-blau.svg'), encoding='utf-8').read()
        vb = re.search(r'viewBox="([^"]+)"', s).group(1)
        innen = re.search(r'</title>(.*)</svg>', s, flags=re.S).group(1)
        aus.append(f'<symbol id="{sid}" viewBox="{vb}" fill="currentColor">{innen}</symbol>')
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{"".join(aus)}</defs></svg>'


def marke(farbe, klasse='', label='Hotel Monte-Moro, Saas-Almagell'):
    return f'<svg class="wm {klasse}" viewBox="0 0 3483 1425" style="color:{FARBE[farbe]["h"]}" role="img" aria-label="{e(label)}"><use href="#wm"/></svg>'


def kamm(farbe, klasse=''):
    return f'<svg class="bk {klasse}" viewBox="0 0 3483 696" style="color:{FARBE[farbe]["h"]}" aria-hidden="true"><use href="#bk"/></svg>'


PFEIL = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9.5M8.5 4l4 4-4 4"/></svg>'
RUNTER = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v9M3.8 7 8 11.2 12.2 7M3 14h10"/></svg>'

KAP = [('haltung', 'Haltung'), ('zeichen', 'Zeichen'), ('farben', 'Farben'), ('schrift', 'Schrift'), ('form', 'Bausteine'),
       ('bilder', 'Bilder'), ('logo', 'Richtig und falsch'), ('ton', 'Ton')]


def kopf(nr, etikett, titel, lead):
    a, b = titel
    return (f'<header class="mk"><p class="mk__kap" data-r><span>{nr:02d}</span><b>{e(etikett)}</b><i></i></p>'
            f'<h2 class="mk__t" data-t>{e((a + " " + b).rsplit(" ", 1)[0])}&nbsp;<em>{e((a + " " + b).rsplit(" ", 1)[1])}</em></h2><p class="mk__lead" data-r>{lead}</p></header>')


def faecher():
    out = []
    for g in L['gruppen']:
        fs = [f for f in L['farben'] if f['g'] == g['k']]
        knoepfe = ''.join(
            f'<div class="fa" role="button" tabindex="0" data-r data-hex="{f["h"]}" style="--c:{f["h"]}" aria-label="{e(f["n"])} {f["h"]} kopieren">'
            f'<span class="fa__f"><span class="fa__ok">kopiert</span></span><span class="fa__n"><b>{nb(f["n"])}</b><small>{e(f["r"])}</small><code>{f["h"]}</code></span></div>'
            for f in fs)
        out.append(f'<div class="fg"><div class="fg__t" data-r><h3>{e(g["n"])}</h3><p>{e(g["s"])}</p></div><div class="fg__f">{knoepfe}</div></div>')
    return ''.join(out)


def seite():
    h = FARBE
    titel = f'''<section class="titel" id="oben">
  <div class="titel__in">
    <div class="titel__wm" data-r>{marke("papier")}</div>
    <div class="titel__t">
      <p class="etikett" data-r>Die Hausregeln · Markenbuch, Oktober 2026</p>
      <h1 data-t>Mehr erleben, weniger <em>zahlen.</em></h1>
      <p class="titel__ort" data-r>Hotel Monte-Moro <i></i> Restaurant Röstihüs <i></i> <span class="ort-z">Saas-Almagell <i></i> Saastal <i></i> Wallis</span></p>
      <p class="titel__lead" data-r>Alles, was das Haus erkennbar macht, an einem Ort: der Bergkamm und die Wortmarke, die Farben und ihre Rollen, die Schriften, das Medaillon als Tapete, die Bausteine, die Bilder und der Ton. Damit jedes neue Stück, ob Karte, Aushang oder Beitrag, aussieht wie aus einem Guss.</p>
      <p class="titel__kn" data-r><a class="kn kn--laerche" href="#haltung"><span>Lesen</span><i>{RUNTER}</i></a></p>
    </div>
  </div>
  <nav class="index" aria-label="Inhalt" data-r>{"".join(f'<a href="#{k}"><span>{i + 1:02d}</span>{e(n)}</a>' for i, (k, n) in enumerate(KAP))}</nav>
</section>'''

    haltung = f'''<section class="blatt hell" id="haltung"><div class="in">
  {kopf(1, 'Haltung', ('Hell, direkt', 'und herzlich.'), '«Mehr erleben, weniger zahlen.» Der Satz steht ganz oben auf der Startseite des Hauses, und er beschreibt es: drei Sterne, 18 Zimmer, die Postautos im ganzen Saastal inbegriffen, im Sommer auch die Bergbahnen, das Spa des Partnerhotels offen, im Röstihüs elf Röstis mit Namen. Die Gestaltung ist hell, direkt und herzlich, so wie das Haus mit seinen Gästen redet.')}
  <div class="drei">
    <article class="k3" data-r><div class="k3__b">{bild('haus-sommer-g', None, '50% 40%')}</div>
      <div class="k3__n"><small>Licht</small><b>Hell wie die Fassade.</b><p>Papier und Fassade tragen den Lesetext. Dunkel wird die Seite am Abend, im Blau des Logos.</p></div></article>
    <article class="k3" data-r><div class="k3__b">{bild('roesti-raum', None, '50% 50%')}</div>
      <div class="k3__n"><small>Röstihüs</small><b>Das Haus mit Gesicht.</b><p>Kartoffelsäcke mit Gesichtern, Röstis mit Namen, Hotelweine, die Fabian selber kreiert hat: gezeigt wird, was es nur hier gibt.</p></div></article>
    <article class="k3" data-r><div class="k3__b">{bild('gondel', None, '50% 50%')}</div>
      <div class="k3__n"><small>Ton</small><b>Ehrlich gerechnet.</b><p>Was inbegriffen ist, steht vorn und als Liste, ohne grosse Worte. Das Haus siezt seine Gäste.</p></div></article>
  </div>
</div></section>'''

    fenster = lambda k, satz, unter, pos='50% 50%': f'''<section class="fenster" data-z aria-label="{e(satz)}"><div class="fenster__f">
  <div class="fenster__b">{bild(k, None, pos, True, False)}</div>
  <div class="fenster__t"><p class="fenster__s" data-t>{e(satz)}</p><p class="fenster__u" data-r>{e(unter)}</p></div></div></section>'''

    nein = lambda klasse, text: f'<figure class="nein nein--{klasse}"><div>{marke("blau")}</div><figcaption>{nb(text)}</figcaption></figure>'
    zeichen = f'''<section class="blatt dunkel" id="zeichen"><div class="in">
  {kopf(2, 'Zeichen und Name', ('Zwei Gipfel', 'und Ihr Name.'), 'Das Logo ist eine Datei von der heutigen Seite des Hauses (logo.png, 1161 auf 475 Pixel): zwei Gipfel als «MM», darunter «Monte Moro» und «Saas-Almagell». Für Farben und grosse Drucke liegt ein genauer Zug der Datei bei, der die Form nicht verändert. Aus den Gipfeln kommen der Bergkamm, das Medaillon und der Grat.')}
  <div class="lockups">
    <figure class="lock lock--papier" data-r><div>{marke("blau")}</div><figcaption><b>Logo-Blau auf Papier</b><small>die Hauptform · {h["blau"]["h"]}</small></figcaption></figure>
    <figure class="lock lock--nacht" data-r><div>{marke("papier")}</div><figcaption><b>Papier auf Nacht</b><small>auf dunklen Flächen · {h["papier"]["h"]}</small></figcaption></figure>
    <figure class="lock lock--nacht" data-r><div>{marke("laerche")}</div><figcaption><b>Lärche auf Nacht</b><small>wo es warm sein darf · {h["laerche"]["h"]}</small></figcaption></figure>
  </div>
  <div class="regeln">
    <div class="regel" data-r><div class="regel__f"><span class="schutz">{marke("papier")}</span></div><h3>Schutzraum</h3><p>Rundum bleibt so viel Luft, wie das «o» in «Moro» hoch ist. Kein Text, kein Bildrand, keine Linie ragt hinein.</p></div>
    <div class="regel" data-r><div class="regel__f klein"><span>{kamm("papier")}<small>48 px</small></span><span>{marke("papier")}<small>150 px</small></span></div><h3>Kleinste Grösse</h3><p>Die ganze Wortmarke ab 150 Pixel oder 40 Millimeter Breite, darunter ist «Saas-Almagell» nicht mehr lesbar. Kleiner steht nur der Bergkamm, ab 48 Pixel oder 15 Millimeter.</p></div>
    <div class="regel regel--breit" data-r><div class="regel__f neine">{nein('zerr', 'Nicht verzerren')}{nein('dreh', 'Nicht drehen')}{nein('farbe', 'Nicht umfärben')}{nein('schatten', 'Keine Schatten')}</div><h3>Was das Zeichen nicht&nbsp;darf</h3><p>Es steht gerade, in Logo-Blau, Nacht, Papier oder Lärche, ohne Schatten und ohne Rahmen. Auf Fotos nur dort, wo die Fläche ruhig ist. Das Medaillon, der Bergkamm im Kreis, ist Siegel und Tapete, nie Ersatz für die Wortmarke.</p></div>
  </div>
</div></section>'''

    farben = f'''<section class="blatt hell" id="farben"><div class="in">
  {kopf(3, 'Farben', ('Papier, Nacht', 'und Lärche.'), 'Die Farben kommen aus dem Haus: aus der Logo-Datei, aus der Fassade in der Sonne und aus den Balkonen aus Lärche. Jede steht genau so in der Gestaltung der Website (Farbwelt A «Bergnacht und Lärche», von Robert am 18. Oktober 2026 gewählt). Ein Klick auf eine Farbe kopiert ihren Wert.')}
  {faecher()}
  <div class="satzreihe" data-r><p><b>Hell ist der Normalzustand.</b> Papier und Fassade tragen den Lesetext, dunkel wird es am Abend.</p><p><b>Lärche betont.</b> Den Hauptknopf und das letzte Wort im Titel, nie den Lesetext. Messing nur als feine Linie.</p><p><b>Nie rein.</b> Kein reines Schwarz, kein reines Weiss: Nacht und Papier tragen alles.</p></div>
</div></section>'''

    schrift = f'''<section class="blatt dunkel" id="schrift"><div class="in">
  {kopf(4, 'Schrift', ('Die Schrift', 'aus der Wortmarke.'), '«Monte Moro» steht im Logo in einer schmalen, kräftigen Groteske. Die Titelschrift nimmt diese Haltung auf: Fjalla One, gross und klein geschrieben wie die Wortmarke. Instrument Sans hält lange Texte lesbar, DM Mono steht bei Zeiten, Preisen, Adressen und auf den Knöpfen. Alle sind frei lizenziert und liegen als Dateien bei der Website.')}
  <div class="proben">
    <div class="probe probe--titel" data-r><small>Titel · Fjalla One 400</small><p class="p1">Mehr erleben, weniger zahlen.</p><p class="abc">Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz Ää Öö Üü 0123456789</p></div>
    <div class="probe" data-r><small>Lesetext · Instrument Sans 400 · 17,5 px · Zeilenabstand 1,7</small><p class="p2">{e(daten("RESTAURANT"))} {e(daten("SONNE"))}</p></div>
    <div class="probe" data-r><small>Kleine Angaben · DM Mono 400 · Versalien · 0,16 bis 0,24 em</small><p class="p3">Restaurant Röstihüs · Saas-Almagell</p><p class="p4"><span>Tel.</span><b>{e(HAUS["tel"])}</b><span>Ort</span><b>{e(HAUS["plz_ort"])}</b></p></div>
  </div>
</div></section>'''

    form = f'''<section class="blatt hell" id="form"><div class="in">
  {kopf(5, 'Bausteine', ('Knöpfe, Grat', 'und Tapete.'), 'Die kleinen Teile, die überall wiederkehren. Jeder Knopf hat Tiefe und einen runden Knauf mit Pfeil und gibt nach, wenn man ihn drückt. Wo eine helle Fläche in eine dunkle übergeht, endet sie nicht gerade, sondern als Grat, gezogen nach den Gipfeln des Logos. Die Tapete ist das Medaillon in einem Rautengitter: zart, Ton in Ton, im Wechsel mit glatten Flächen.')}
  <div class="formen">
    <figure class="form-b" data-r>{bild('empfang', None, '50% 50%')}<figcaption>Der Bergkamm an der Wand beim Empfang</figcaption></figure>
    <div class="form-d" data-r>
      <div class="platte platte--grat"><small>Der Grat</small><b>Jede Naht zwischen zwei Flächen endet als Bergkamm, nie an Kacheln oder Bildern.</b><div class="tapeten"><span class="tap tap--hell">Tapete auf Papier</span><span class="tap tap--dunkel">Tapete auf Nacht</span></div></div>
      <div class="kn-reihe"><span class="kn kn--laerche"><span>Zimmer anfragen</span><i>{PFEIL}</i></span><span class="kn kn--nacht"><span>Zur Karte</span><i>{PFEIL}</i></span></div>
      <p class="form-s"><b>Lärche mit hellem Knauf</b> ist der Hauptweg, einmal je Fläche. <b>Nacht</b> und <b>Papier</b> sind jeder Nebenweg. Schrift in DM Mono, gesperrt, in Versalien; der Knopf sagt ruhig, was passiert.</p>
    </div>
  </div>
  <div class="nicht" data-r><h3>Nicht bei uns</h3><p>Ausgeschnittene Ecken, Pillen-Reihen, Sticker, Siegel als Schmuck, Leuchtschrift, Verläufe im Logo. Der Name eines Bildes steht unten links im Foto, auf einem weichen Schatten.</p></div>
</div></section>'''

    mosaik = [('haus-winter-b', '50% 50%'), ('z-dach', '50% 50%'), ('stuebli', '50% 50%'), ('fr-tisch', '50% 50%'), ('balkon', '50% 60%')]
    bilder = f'''<section class="blatt dunkel" id="bilder"><div class="in">
  {kopf(6, 'Bilder', ('Ihr Haus,', 'in echtem Licht.'), 'Gezeigt wird, was der Gast vorfindet: das Haus im Schnee, die Zimmer unter dem Dach, das Raclettestübli, das Frühstück, der Blick vom Balkon. Die Fotos stammen von der Seite des Hauses, von Schweiz Tourismus, Booking.com und Tripadvisor, jeweils vom Haus selbst; mit KI neu gerechnet werden nur Licht und Schärfe, nie der Inhalt.')}
  <div class="mosaik">{"".join(f'<figure data-r>{bild(k, None, p)}</figure>' for k, p in mosaik)}</div>
  <ul class="regel-liste" data-r><li><b>Fotos aus dem Haus.</b> Jedes Bild zeigt das Monte-Moro oder das Röstihüs, Bilder der Region nur mit bekannter Herkunft.</li><li><b>Warm bleibt warm.</b> Licht und Weiss werden ausgeglichen, das Holz bleibt Holz.</li><li><b>Der Name im Bild.</b> Unten links, in Fjalla One, auf einem weichen Schatten im Foto.</li><li><b>Mit KI neu gerechnet</b> nur mit diesem Hinweis; frei lizenzierte Fotos nur mit Fotograf und Lizenz.</li></ul>
</div></section>'''

    ja = [('papier', 'Das Original', 'Die Datei des Hauses in Logo-Blau, überall dort, wo die Fläche hell ist.', 'blau'),
          ('nacht', 'Auf Nacht', 'Auf dunkler Fläche in Papier, aus dem Vektor gezogen, Form unverändert.', 'papier'),
          ('papier', 'Der Bergkamm allein', 'Die zwei Gipfel stehen allein in Leisten, über Überschriften und an der Wand, wie beim Empfang.', 'kamm'),
          ('nacht', 'In Lärche', 'Auf Nacht darf das Zeichen in Lärche stehen.', 'laerche')]
    nein2 = [('zerr', 'Gestreckt', 'Die Proportion bleibt. Nie breiter oder höher gezogen.'),
             ('farbe', 'Umgefärbt', 'Nur Logo-Blau, Nacht, Papier und Lärche. Kein Grün, kein Verlauf.'),
             ('schatten', 'Mit Schatten und Glanz', 'Kein Schatten, kein Leuchten, kein Relief. Die Wortmarke liegt flach.'),
             ('dreh', 'Gedreht', 'Die Wortmarke steht immer waagrecht und ganz.')]
    logo = f'''<section class="blatt creme2" id="logo"><div class="in">
  {kopf(7, 'Logo richtig und falsch', ('Eingesetzt,', 'nie verändert.'), 'Die Wortmarke und der Bergkamm sind Dateien aus dem Haus. Sie werden eingesetzt, nie nachgezeichnet und nie neu gesetzt, auch nicht in Fjalla One. Bergkamm und Name werden nie auseinandergenommen und neu gestellt.')}
  <div class="rf"><h3 class="rf__t rf__t--ja" data-r>Richtig</h3><div class="vier">{"".join(f'<article class="k4 k4--ja" data-r><div class="k4__f k4__f--{g}">{kamm("blau") if was == "kamm" else marke(was)}</div><b>{e(t)}</b><p>{e(s)}</p></article>' for g, t, s, was in ja)}</div></div>
  <div class="rf"><h3 class="rf__t rf__t--nein" data-r>Falsch</h3><div class="vier">{"".join(f'<article class="k4 k4--nein nein--{k}" data-r><div class="k4__f k4__f--papier">{marke("blau")}</div><b>{e(t)}</b><p>{e(s)}</p></article>' for k, t, s in nein2)}</div></div>
</div></section>'''

    worte = L['ton']['eigene_worte']
    ton = f'''<section class="blatt dunkel" id="ton"><div class="in">
  {kopf(8, 'Ton', ('Sie, ehrlich,', 'ohne grosse Worte.'), 'Das Haus siezt seine Gäste. Es schreibt hell, direkt und herzlich, in Schweizer Schreibung, und macht sich nicht grösser, als es ist. Lieber eine echte Angabe (was inbegriffen ist, wie viele Röstis, wann der Kidsclub offen hat) als ein Adjektiv.')}
  <div class="zwei">
    <div class="ton ton--ja" data-r><h3>So klingt das Haus</h3><ul>{"".join(f'<li>«{e(w.rstrip("."))}»</li>' for w in worte)}</ul></div>
    <div class="ton ton--nein" data-r><h3>So nicht</h3><ul><li><s>Gönn dir eine Auszeit</s><span>Sie-Form, wie auf der Website</span></li><li><s>Luxus-Refugium der Extraklasse</s><span>Ein familiäres Haus mit drei Sternen</span></li><li><s>Jetzt buchen!</s><span>Zimmer anfragen</span></li><li><s>Atemberaubende, unvergessliche Momente</s><span>Bei uns scheint fast immer die Sonne.</span></li></ul></div>
  </div>
</div></section>'''

    fuss = f'''<footer class="fuss"><div class="in">
  <div class="fuss__wm">{marke("papier")}</div>
  <div class="fuss__t"><p class="etikett">Die Hausregeln · Stand Oktober 2026</p><p class="fuss__a">{e(HAUS["name"])} mit Restaurant Röstihüs<br>{e(HAUS["plz_ort"])}</p>
    <dl class="fuss__z"><div><dt>Telefon</dt><dd>{e(HAUS["tel"])}</dd></div><div><dt>E-Mail</dt><dd>{e(HAUS["mail"])}</dd></div></dl>
    <p class="fuss__l"><a href="./">Zurück zum Markenbuch</a></p></div>
</div></footer>'''

    leiste = f'''<nav class="leiste" aria-label="Die Hausregeln">
  <a class="leiste__m" href="./" title="Zurück zum Markenbuch">{kamm("laerche", "leiste__wm")}<span><b>Die Hausregeln</b><small>Zurück zum Markenbuch</small></span></a>
  <div class="leiste__k">{"".join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAP)}</div>
  <button class="kn kn--laerche kn--leiste" type="button" id="bu-pdf"><span>Als PDF sichern</span><i>{RUNTER}</i></button>
</nav>'''

    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Die Hausregeln · Hotel Monte-Moro, Saas-Almagell</title>
<meta name="description" content="Die Hausregeln des Hotel Monte-Moro: Haltung, Wortmarke und Bergkamm, Farben und ihre Rollen, Schriften, Bausteine, Bilder, Logo richtig und falsch, Ton.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{h['nacht']['h']}">
<link rel="icon" href="/assets/oberflaeche/kleid/montemoro-zeichen.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/FjallaOne-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/InstrumentSans-normal-400_600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="buch/buch.css?v={_v('buch/buch.css')}">
</head>
<body>
{symbole()}
{leiste}
<main>
{titel}
{haltung}
{fenster('haus-sommer', 'Bei uns scheint fast immer die Sonne.', 'Hotel Monte-Moro, auf der Seite des Röstihüs.', '50% 40%')}
{zeichen}
{farben}
{schrift}
{form}
{bilder}
{logo}
{fenster('stube-tische', 'Es lebe die Tradition!', 'Restaurant Röstihüs, Saas-Almagell.', '50% 50%')}
{ton}
</main>
{fuss}
<div class="meldung" id="meldung" aria-live="polite"></div>
<script src="buch.js?v={_v('buch.js')}"></script>
</body>
</html>
'''


if __name__ == '__main__':
    open(os.path.join(HIER, 'buch.html'), 'w', encoding='utf-8').write(seite())
    print('buch.html geschrieben')
