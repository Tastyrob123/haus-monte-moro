"""Unterseite saastal.html des Hotel Monte-Moro: «Der Tag im Saastal» (Neubau 20.10.2026 abends).
Robert 20.10.2026 17:29–17:31 zur alten Seite: «Da kann man sicher noch eine schöne Animation einbauen» (Zu Fuss vom Haus) · «Das muss richtig geil sein,
man muss richtig Lust haben auf Ausflüge» · «Alles nochmal neu machen, anders denken, besser machen. Es muss wirklich edel sein. Jedes Element soll
irgendwie so seinen Platz haben, einladen.» Plan Unterseiten: die Fussspuren gehen vom Haus zu den Zielen, Sommer und Winter als zwei Hälften desselben Tals.

Drehbuch: (1) Kopf wie gehabt (kopf_tag). (2) «Zu Fuss vom Haus»: das Haus als grosses Foto, aus ihm läuft die Spur nach der Uhr zum Lift, zur Busstation
und in den Dorfkern; an jedem Ziel steigt die Minutenzahl auf, sobald die Spur ankommt. (3) «Sommer und Winter»: das Tal in zwei Hälften, links der helle
Sommer, rechts der Winter in Nachtblau, oben je ein eigener Grat. Auf der Naht läuft die Spur weiter, ein Schritt im Sommer, einer im Winter; an ihr
liegen die Ziele beider Jahreszeiten, versetzt, die Fotos des Hauses aneinander. (4) Überleitung ins Spa.
Eine Bewegungsidee: die Spur. Sonst nur die Handschrift des Hauses: Rahmen steigen deckend von unten (tiefe.js, .fo[data-r]), Fotos zoomen im Rahmen,
Zahlen zählen ab 80 %. Alle Fakten und Sätze aus inhalt/daten.py, alle Fotos aus inhalt/bilder.py. Eigenes CSS: assets/css/seite-saastal.css (Klassen st-…)."""


def seite():
    import bau as B
    D, e = B.D, B.e

    def tritte(n, k0=0, kl='st-tr'):
        """n Fussabdrücke, der k-te erscheint nach k Schritten (--k)."""
        return ''.join(f'<i class="{kl}" style="--k:{k0 + i}"></i>' for i in range(n))

    def foto(key, kl='', s='(max-width:900px) 92vw, 40vw', lage='50% 50%'):
        """Ein Rahmen mit einem Foto: steigt deckend von unten, das Foto zoomt darin (tiefe.js)."""
        return f'<figure class="fo st-f {kl}" data-r="">{B.bild(key, sizes=s, lage=lage)}</figure>'

    def stapel(keys, kl='', s='(max-width:900px) 92vw, 40vw', lagen=None):
        """Mehrere Panoramen des Hauses aneinander in einem Rahmen; die Gruppe kommt in einem Zug."""
        lagen = lagen or ['50% 50%'] * len(keys)
        z = ''.join(f'<span class="st-z st-z--{i}">{B.bild(k, sizes=s, lage=l)}</span>' for i, (k, l) in enumerate(zip(keys, lagen)))
        return f'<div class="fo st-stapel {kl}" data-r="">{z}</div>'

    def zahl(wert, nach=''):
        return f'<b class="st-zahl"><i data-stz="{e(wert)}">{e(wert)}</i>{e(nach)}</b>'

    def ziel(bilder, titel_, satz='', extra='', kl=''):
        t = f'<p class="st-ziel__t">{e(titel_)}</p>' + (f'<p class="st-ziel__s">{satz}</p>' if satz else '') + extra
        return f'<article class="st-ziel {kl}">{bilder}<div class="st-ziel__text" data-s>{t}</div></article>'

    inkl = f'<p class="st-inkl">{e(D.POSTAUTO)}</p>'

    # ---------------------------------------------------------------- 1 Kopf
    inhalt = B.kopf_tag('anfang', 'Saastal · Sommer und Winter', 'Zwei Minuten bis zum Lift.', 'bis zum Lift.',
                        D.LAGE_SATZ + ' ' + D.BERGBAHN_SATZ, 'tal-sommer')

    # ---------------------------------------------------------------- 2 Zu Fuss vom Haus: die Spur läuft nach der Uhr vom Haus zu den drei Zielen
    SCHRITT = .085                       # Sekunden je Abdruck
    teile, k = '', 0
    for i, (m, ort, satz) in enumerate(D.LAGE):
        n = 5 + int(m) * 2               # mehr Gehminuten, mehr Schritte
        teile += f'<div class="st-weg__stueck" aria-hidden="true">{tritte(n, k)}</div>'
        k += n
        t = k * SCHRITT
        teile += (f'<div class="st-halt" style="--t:{t:.2f}s"><p class="st-halt__min">{zahl(m)}<small>Min.</small></p><i class="st-halt__marke" aria-hidden="true"></i>'
                  f'<p class="st-halt__ort">{e(ort)}</p><p class="st-halt__satz">{e(satz)}</p></div>')
    inhalt += f'''<section class="kapitel st-fuss" id="wege" aria-label="Zu Fuss vom Haus">{B.grat_oben()}
  <div class="kapitel__innen">
    <div class="st-fuss__buehne">
      {foto('haus-sommer-g', 'st-fuss__haus', '(max-width:900px) 92vw, 38vw', '42% 50%')}
      <div class="st-fuss__rechts">
        <div class="st-fuss__kopf">{B.ueber('Ab dem Haus · Gehminuten laut Haus')}{B.titel('Zu Fuss vom Haus.', em='vom Haus.')}<p class="leise" data-s>{e(D.PARK)}.</p></div>
        <div class="st-weg" data-stlauf>{teile}</div>
      </div>
    </div>
  </div>
</section>'''

    # ---------------------------------------------------------------- 3 Sommer und Winter: zwei Hälften, die Spur auf der Naht
    so, wi = {x[0]: x for x in D.SAASTAL['sommer']}, {x[0]: x for x in D.SAASTAL['winter']}
    rest = D.SOMMER_SATZ.split('; ', 1)[1]
    rest = rest[0].upper() + rest[1:]
    ausfluege = '<p class="st-orte">' + ' <span class="st-orte__tr" aria-hidden="true">/</span> '.join(f'<span>{e(o)}</span>' for o in so['stausee'][2].split(', ')) + '</p>'
    hoehen = ''.join(f'<li><span>{e(o)}</span>{zahl(h, " m")}</li>' for o, h in B.re.findall(r'(\S+) (\d+)m', wi['skitour'][2]))
    S = '(max-width:900px) 92vw, 42vw'
    sommer = f'''<div class="st-haelfte st-haelfte--sommer">
      <div class="st-haelfte__kopf">{B.ueber('Sommer')}{B.titel('Im Sommer ein herrliches Wanderparadies.', em='Wanderparadies.')}<p class="leise" data-s>{e(rest)}</p></div>
      {ziel(stapel(['mattmark', 'alpenrosen', 'murmeltiere'], 'st-stapel--drei', S), so['mattmark'][1], '', f'<p class="st-gross">über {zahl("250", " km")}<span>Wanderwege</span></p>' + inkl, 'st-ziel--erst')}
      {ziel(foto('wasserfall', 'st-f--hoch', S, '50% 50%'), so['wasserfall'][1], e(so['wasserfall'][2]))}
      {ziel(stapel(['bach', 'bergbach'], '', S), so['bach'][1], e(so['bach'][2]))}
      {ziel(foto('blumen', 'st-f--breit', S), so['blumen'][1], e(so['blumen'][2]))}
      {ziel(stapel(['stausee', 'see-blumen'], '', S), so['stausee'][1], '', ausfluege, 'st-ziel--orte')}
    </div>'''
    winter = f'''<div class="st-haelfte st-haelfte--winter">
      <div class="st-haelfte__kopf">{B.ueber('Winter')}{B.titel('Im Winter auf die Piste.', em='auf die Piste.')}<ul class="st-hoehen" data-s>{hoehen}</ul></div>
      {ziel(stapel(['skitour', 'skitour-hang'], '', S, ['50% 40%', '50% 50%']), wi['skitour'][1], e(D.LAGE[0][0] + ' ' + D.LAGE[0][2]), '', 'st-ziel--erst')}
      {ziel(foto('huette', 'st-f--hoch', S, '58% 50%'), wi['huette'][1], e(wi['huette'][2][0].upper() + wi['huette'][2][1:]), inkl)}
      {ziel(stapel(['winterweg', 'winterbach'], '', S), wi['winterweg'][1], e(wi['winterweg'][2][0].upper() + wi['winterweg'][2][1:]))}
      {ziel(stapel(['metro', 'gletscher'], '', S, ['50% 45%', '50% 50%']), wi['metro'][1], e(wi['metro'][2]))}
      {ziel(foto('dorf-fluss', 'st-f--hoch', S, '50% 60%'), 'Saas-Almagell', e(D.INKLUSIVE[0]), '', 'st-schluss')}
    </div>'''
    naht = '<div class="st-naht" aria-hidden="true">' + ''.join(f'<div class="st-naht__stueck" data-stlauf>{tritte(12, 0, "st-tr st-tr--naht")}</div>' for _ in range(7)) + '</div>'
    inhalt += f'''<section class="st-tal" id="sommer-winter" aria-label="Sommer und Winter im Saastal">
  <svg class="st-tal__grat st-tal__grat--l" viewBox="0 0 500 60" preserveAspectRatio="none" aria-hidden="true"><path d="{B.GRAT.replace('L1000 26 L1000 60 Z', '').split(' L540')[0]} L500 41 L500 60 Z"/></svg>
  <svg class="st-tal__grat st-tal__grat--r" viewBox="500 0 500 60" preserveAspectRatio="none" aria-hidden="true"><path d="M500 60 L500 41 L540{B.GRAT.split(' L540', 1)[1]}"/></svg>
  <div class="st-tal__innen">{sommer}{naht}{winter}</div>
</section>'''

    # ---------------------------------------------------------------- 4 Überleitung ins Spa
    inhalt += B.kapitel('weiter', 'st-ende', '', 'Weiter zum Spa', weiter=('Nach dem Lift: das Spa nebenan.', 'spa.html', 'Das Spa nebenan'))

    # ---------------------------------------------------------------- Bewegung der Spur (nur diese Seite)
    inhalt += '''<script>
(function () {
  var D = document, $$ = function (s) { return [].slice.call(D.querySelectorAll(s)); };
  var ruhig = matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]nomotion/.test(location.search);
  var zahlen = $$('[data-stz]');
  function zaehle(el) {
    var n = parseFloat(el.dataset.stz), v0 = Math.max(1, Math.round(n * .8)), t0 = 0;
    if (v0 >= n) { el.textContent = el.dataset.stz; return; }
    (function s(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 900); el.textContent = String(Math.round(v0 + (n - v0) * (1 - Math.pow(1 - k, 3)))); if (k < 1) requestAnimationFrame(s); })(performance.now());
  }
  zahlen.forEach(function (el) { el.style.minWidth = el.dataset.stz.length + 'ch'; });
  if (ruhig || !('IntersectionObserver' in window)) { $$('[data-stlauf]').forEach(function (el) { el.classList.add('da'); }); return; }
  zahlen.forEach(function (el) { if (el.getBoundingClientRect().top > innerHeight) el.textContent = String(Math.max(1, Math.round(parseFloat(el.dataset.stz) * .8))); });
  /* die Spur läuft, sobald ihr Stück den unteren Rand berührt; die Ziele am Weg steigen, wenn sie ankommt */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return; io.unobserve(e.target); var w = e.target; w.classList.add('da');
      $$('[data-stlauf].da .st-halt').forEach(function (h) { if (h.__z) return; h.__z = 1; var t = parseFloat(getComputedStyle(h).getPropertyValue('--t')) || 0; var z = h.querySelector('[data-stz]'); if (z) setTimeout(function () { zaehle(z); }, t * 1000 + 250); });
    });
  }, { rootMargin: '0px 0px -12% 0px' });
  $$('[data-stlauf]').forEach(function (el) { io.observe(el); });
  var zio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { zio.unobserve(e.target); zaehle(e.target); } }); }, { rootMargin: '0px 0px -14% 0px' });
  zahlen.forEach(function (el) { if (!el.closest('.st-halt')) zio.observe(el); });
})();
</script>'''
    return (B.kopf('Saastal · Hotel Monte-Moro', 'Sommer und Winter im Saastal ab dem Hotel Monte-Moro: zwei Minuten bis zum Lift, Bergbahnen und Postautos inklusive.', 'saastal.html')
            + inhalt + B.fuss())
