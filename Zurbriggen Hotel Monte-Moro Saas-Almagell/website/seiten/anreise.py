"""Unterseite anreise.html des Hotel Monte-Moro. Eigene Datei, damit ein eigener Chat sie neu bauen kann, ohne bau.py anzufassen
(Robert 20.10.2026 17:29–17:31 zu Saastal, Spa und Anreise: «nochmal neu machen, anders denken, besser machen … edel … einladen»).
Hilfsmittel kommen aus bau.py (import bau as B: B.kopf, B.kopf_tag, B.kapitel, B.bild, B.ebene, B.kn, B.anfrage, B.fuss, B.D, B.e …).
Eigenes CSS: assets/css/seite-anreise.css (wird auf allen Seiten geladen, also nur mit eigenen Klassen arbeiten, Vorsilbe «an-»).

Neubau 20.10.2026 abends (Robert 17:31): «Diese Abfahrtstafel gefällt mir nicht. Überlegt ihr was anderes dafür.» · zur Ankunft «deutlich besser und geiler».
Bleibt (Robert 18.10. 15:30): die Linie Visp–Stalden–Saas-Grund–Saas-Almagell mit Fussspuren und gezoomten Zielen, nur der Text darauf ist klarer gesetzt.
Der Faden der Seite: der Weg her, in drei Stücken.
  1. Die Linie ins Tal (Karte, Fussspuren von der Busstation bis vor das Haus).
  2. Zwei Wege ins Saastal: eine Platte aus zwei Hälften, die aneinander liegen. Links am Abend mit Zug und Postauto (Saas-Almagell bei Nacht,
     die Dauer, die letzten Verbindungen ab Visp gross gesetzt, darunter die geschenkte Anreise mit Ablaufdatum), rechts bei Tag mit dem Auto
     (das Tal, die Strecke als Linie mit den Abzweigungen im Wortlaut des Hauses, Parkplätze). Die Platte steigt als Ganzes von unten.
  3. Ankunft: das Haus im Schnee und der Empfang bündig nebeneinander, darunter wie ein Hausschild die Adresse, das Telefon, der Parkplatz;
     die Knöpfe mittig darunter. Kein Ticket, keine Tafel, kein Aufklappen, keine Kreise."""
import re


def seite():
    import bau as B
    D, e = B.D, B.e
    zug_zeit = D.ANREISE_ZUG_ZEIT.split('ca. ')[1]          # «45 Min.»
    auto_zeit = D.ANREISE_AUTO_ZEIT.split('ca. ')[1]        # «40 Min.»

    # ---------------------------------------------------------------- Kopf: unverändert, nur der Satz sagt jetzt, welche Zeit zu welchem Weg gehört
    inhalt = B.kopf_tag('anfang', 'Anreise · Kontakt', 'Die Abfahrt in Visp.', 'in Visp.',
                        f'Ab Visp ca. {zug_zeit} mit Zug und Postauto, ca. {auto_zeit} mit dem Auto.', 'dorf-weiss', '50% 58%')
    # Robert 20.10.2026 18:29 zum Streifen mit dem angeschnittenen Haus: «sieht kacke aus als Motiv von diesem Streifenbild» → das Dorf im Schnee als Landschaft

    # ---------------------------------------------------------------- 1. die Linie ins Tal (bleibt), Text auf der Karte klarer
    flug = B.flug('anreise')
    # Robert 24.10.2026: statt der zweiten Fussspur (Busstation bis Haus) eine gezeichnete Dorfkarte mit dem Weg (seiten/dorfkarte.py, OpenStreetMap)
    from seiten import dorfkarte
    a = flug.index('<g class="flug__detail">'); b = flug.index('<g class="ort ort--haus"', a)
    flug = flug[:a] + '<g class="flug__detail">' + dorfkarte.karte(e) + '</g>\n        ' + flug[b:]
    flug = re.sub(r'<p class="leise">.*?</p>',
                  f'<p class="leise an-flug__zeit"><span><b>ca. {e(zug_zeit)}</b> mit Zug und Postauto</span><span><b>ca. {e(auto_zeit)}</b> mit dem Auto</span></p>',
                  flug, count=1, flags=re.S)
    # Z2 20.10.2026 18:05: der Schluss des Flugs war fast leer und die Karte «Bis vor das Haus» wirkte blass → Foto in die Karte (zu Fuss bis vor das Haus),
    # beide Karten deckend (Auftritt über die Klasse .nah der Karte, CSS), Strecke kürzer, weniger Luft danach.
    zwei = '<div class="flug__text flug__text--2" data-flugzwei>'
    assert zwei in flug
    # am Handy liegt das Foto oben in der Bühne (die Karte unten bleibt frei, damit die Fussspuren zu sehen sind), am Laptop oben in der Karte
    flug = flug.replace(zwei, f'<figure class="an-flug__oben">{B.bild("winterweg", sizes="100vw", lage="50% 62%")}</figure>'
                        + zwei + f'<figure class="an-flug__bild">{B.bild("winterweg", sizes="460px", lage="50% 60%")}</figure>', 1)
    inhalt += B.kapitel('weg', 'k-anreise k-anreise--flug an-k-flug', flug, 'Der Weg ins Saastal')

    # ---------------------------------------------------------------- 2. zwei Wege ins Saastal
    def dauer(zeit):
        z = zeit.split(' ')[0]
        return f'<p class="an-dauer"><small>ca.</small><b><i data-zahl="{e(z)}">{e(z)}</i></b><small>Min. ab Visp</small></p>'

    # Verbindungen ab Visp, Wortlaut D.ANREISE_ZUG: «stündliche Verbindungen bis 20.10 Uhr ab Visp [bis Saas-Grund 22.40 ab Visp, sowie Freitag und Samstag um 23.40 Uhr]»
    abfahrten = [('Stündlich bis', '20.10', 'Uhr ab Visp'), ('Bis Saas-Grund', '22.40', 'Uhr ab Visp'), ('Freitag und Samstag', '23.40', 'Uhr bis Saas-Grund')]
    ab = ''.join(f'<li><span>{e(a)}</span><b>{e(t)}</b><small>{e(w)}</small></li>' for a, t, w in abfahrten)
    zug_satz = D.ANREISE_ZUG.split(' Es bestehen')[0]                       # «Wenn Sie mit dem Zug anreisen, … umsteigen.»
    umsteigen = D.ANREISE_ZUG.split(']. ')[1]                                 # «In Saas-Grund müssen Sie umsteigen.»
    ag = D.ANREISE_GRATIS
    gratis = (f'<div class="an-gratis" data-bis="{e(ag["bis"])}"><p class="an-gratis__wort">geschenkt</p>'
              f'<div><p class="an-gratis__titel">{e(ag["titel"])}</p><p class="an-gratis__bed">{" ".join(e(b) for b in ag["bedingungen"])}</p></div></div>')

    # Strecke mit dem Auto, Wortlaut D.ANREISE_AUTO in vier Stücken
    strecke = [('Visp', 'Von Visp aus fahren Sie durchs Vispertal.'), ('Stalden', 'Bei der Verzweigung in Stalden Richtung Saastal.'),
               ('Saas-Grund', 'Bei der Abzweigung nach Saas-Fee halten Sie sich links.'), ('Saas-Almagell', 'Ihr Reiseziel, der Ferienort Saas-Almagell.')]
    st = ''.join(f'<li{" class=an-strecke__ziel" if i == len(strecke) - 1 else ""}><b>{e(o)}</b><small>{e(t)}</small></li>' for i, (o, t) in enumerate(strecke))

    inhalt += B.kapitel('zwei-wege', 'k-anreise an-k-wege', f'''
    <div class="kap__kopf an-mitte">{B.ueber('Mit dem Zug und dem Postauto · mit dem Auto')}{B.titel('Zwei Wege ins Saastal.', em='ins Saastal.')}</div>
    <div class="an-wege" data-steig>
      <section class="an-weg an-weg--zug" aria-label="Mit Zug und Postauto">
        <figure class="an-weg__bild" data-bilder>{B.bild('dorf-nacht', sizes='(max-width:900px) 100vw, 680px', lage='50% 62%')}<figcaption>{e(B.BILDER['dorf-nacht'][1])}</figcaption></figure>
        <div class="an-weg__text">
          <p class="ueber">Mit Zug und Postauto</p>
          {dauer(zug_zeit)}
          <p class="an-weg__satz">{e(zug_satz)} {e(umsteigen)}</p>
          <p class="an-ab__kopf">Verbindungen ab Visp</p><ol class="an-ab">{ab}</ol>
          {gratis}
        </div>
      </section>
      <section class="an-weg an-weg--auto" aria-label="Mit dem Auto">
        <figure class="an-weg__bild" data-bilder>{B.bild('tal-dorf', sizes='(max-width:900px) 100vw, 600px', lage='50% 55%')}<figcaption>{e(B.BILDER['tal-dorf'][1])}</figcaption></figure>
        <div class="an-weg__text">
          <p class="ueber">Mit dem Auto</p>
          {dauer(auto_zeit)}
          <ol class="an-strecke" aria-label="Strecke ab Visp">{st}</ol>
          <div class="an-gratis an-gratis--park"><p class="an-gratis__wort">inklusive</p><div><p class="an-gratis__titel">{e(D.INKLUSIVE[5])}</p><p class="an-gratis__bed">{e(D.PARK)}.</p></div></div>
        </div>
      </section>
    </div>''', 'Zwei Wege ins Saastal')

    # ---------------------------------------------------------------- 3. Ankunft
    H = D.HAUS
    inhalt += B.kapitel('ankunft', 'k-ankunft an-k-ankunft', f'''
    <div class="kap__kopf an-mitte">{B.ueber('Ankunft')}{B.titel('Willkommen im Monte-Moro.', em='im Monte-Moro.')}<p class="leise" data-s>{e(D.LAGE_SATZ)}</p></div>
    <div class="an-ankunft" data-steig>
      <div class="an-ankunft__bilder">
        <figure class="an-ankunft__haus" data-bilder>{B.bild('haus-winter-b', sizes='(max-width:900px) 100vw, 790px', lage='50% 45%')}<figcaption>{e(B.BILDER['haus-winter-b'][1])}</figcaption></figure>
        <figure class="an-ankunft__empfang" data-bilder>{B.bild('empfang', sizes='(max-width:900px) 100vw, 490px', lage='40% 50%')}<figcaption>{e(B.BILDER['empfang'][1])}</figcaption></figure>
      </div>
      <div class="an-schild">
        {B.kamm('an-schild__kamm')}
        <div class="an-schild__f"><p class="ueber">Adresse</p><p class="an-schild__gross">{e(H['name'])}</p><p class="an-schild__klein">{e(H['plz_ort'])}</p></div>
        <div class="an-schild__f"><p class="ueber">Telefon</p><p class="an-schild__gross"><a href="tel:{e(H['tel_href'])}">{e(H['tel'])}</a></p><p class="an-schild__klein">Fax {e(H['fax'])}</p></div>
        <div class="an-schild__f"><p class="ueber">E-Mail</p><p class="an-schild__gross"><a href="mailto:{e(H['mail'])}" data-anfrage="Ihre Anfrage">{e(H['mail'])}</a></p><p class="an-schild__klein">{e(H['gastgeber'])}</p></div>
      </div>
    </div>
    <div class="kn-reihe kn-reihe--mitte" data-s>{B.kn('Zimmer buchen', H['buchen'], 'kn--laerche', neu=True)}{B.anfrage('Anfrage an die Rezeption', 'Ihre Anfrage', 'kn--linie')}</div>''',
                        'Ankunft', weiter=('Und morgen scheint die Sonne wieder.', 'index.html', 'Zur Startseite'))

    return (B.kopf('Anreise und Kontakt · Hotel Monte-Moro', 'Anreise zum Hotel Monte-Moro in Saas-Almagell mit Zug und Postauto oder mit dem Auto; Kontakt.', 'anreise.html')
            + inhalt + B.fuss())
