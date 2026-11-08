"""Unterseite spa.html des Hotel Monte-Moro. Eigene Datei, damit ein eigener Chat sie neu bauen kann, ohne bau.py anzufassen
(Robert 20.10.2026 17:29–17:31 zu Saastal, Spa und Anreise: «nochmal neu machen, anders denken, besser machen … edel … einladen»).
Hilfsmittel kommen aus bau.py (import bau as B: B.kopf, B.kopf_tag, B.kapitel, B.bild, B.ebene, B.kn, B.anfrage, B.fuss, B.D, B.e …).
Eigenes CSS: assets/css/seite-spa.css (wird auf allen Seiten geladen, also nur mit eigenen Klassen arbeiten).

Neubau 20.10.2026 abends (Robert zur Bildgruppe: «kann man mit den Bildern auch anders arbeiten»; zur Liste mit Tarifen: «schöner, übersichtlicher»;
zu allen Unterseiten: «edel … Jedes Element soll seinen Platz haben, einladen»). Die Stunde nach dem Lift in drei Schritten:
  1 Der Weg hinüber: das Haus des Partnerhotels und die Liege im Bademantel, aneinander; darunter, was bereitliegt (Bademantel · Schuhe · Handtücher).
  2 Das Angebot als Folge der Räume: Bad, Sauna, Massage als ein Band aneinanderliegender Fotos, unter jedem Raum, was dazugehört.
  3 Der Eintritt: Ruheraum mit Leuchter über einer Platte in Nachtblau, Tarife als eine Zeile, Zahlen zählen ab 80 %, ein Glanzstreif läuft einmal darüber.
Sicherung der vorigen Fassung: _sicherung/spa-2026-10-20/."""

ZAEHL = '''<script>(function(){var z=[].slice.call(document.querySelectorAll('[data-spazahl]'));
if(!z.length||matchMedia('(prefers-reduced-motion: reduce)').matches||/[?&]nomotion/.test(location.search)||!('IntersectionObserver' in window))return;
z.forEach(function(el){el.__n=+el.dataset.spazahl;el.__v=Math.round(el.__n*.8);el.style.display='inline-block';el.style.minWidth=String(el.__n).length+'ch';el.style.textAlign='right';
if(el.getBoundingClientRect().top>innerHeight)el.textContent=el.__v;});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);var el=e.target,t0=0;
(function s(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/900);el.textContent=Math.round(el.__v+(el.__n-el.__v)*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(s);})(performance.now());});},{rootMargin:'0px 0px -12% 0px'});
z.forEach(function(el){io.observe(el);});})();</script>'''


def seite():
    import bau as B
    D, e = B.D, B.e

    def fo(key, kl='', lage='50% 50%', s='(max-width:860px) 100vw, 40vw', alt=None):
        return f'<figure class="fo {kl}" data-r="satt">{B.bild(key, sizes=s, lage=lage, alt=alt)}</figure>'

    # Das Angebot im Wortlaut des Hauses, in seine elf Teile zerlegt und den Räumen zugeordnet
    a = D.SPA_ANGEBOT.replace('Das Angebot reicht vom ', '').replace(' bis hin zum ', ', ').replace(' über ', ', ').rstrip('.')
    t = [x.strip() for x in a.split(',') if x.strip()]
    assert len(t) == 11, t
    t = [x[0].upper() + x[1:] for x in t]
    raeume = [('bad', 'Das Bad', fo('spa-wasser', lage='100% 50%', s='(max-width:860px) 100vw, 30vw', alt=B.BILDER['spa-bad'][1]), [t[0], t[1], t[4], t[5]]),
              ('sauna', 'Die Saunen', fo('spa-holz', lage='55% 50%', s='(max-width:860px) 100vw, 44vw'), [t[2], t[3], t[6]]),
              ('pflege', 'Pflege und Fitness', fo('spa-massage', lage='50% 40%', s='(max-width:860px) 100vw, 26vw'), [t[8], t[10], t[9], t[7]])]
    folge = ''.join(f'<div class="spr__raum spr__raum--{k}">{f}<div class="spr__text" data-steig><p class="spr__name">{e(n)}</p>'
                    f'<ul>{"".join(f"<li>{e(x)}</li>" for x in li)}</ul></div></div>' for k, n, f, li in raeume)

    bereit = D.SPA_INKL.replace(' stehen zur Verfügung.', '')
    dinge = [x.strip() for x in bereit.split(',')]
    assert len(dinge) == 3, dinge

    def tarif(t_, preis, zusatz):
        wert = preis.replace('CHF ', '').split('.')[0]
        return (f'<div class="spt__tarif"><p class="spt__preis"><span>CHF </span><i data-spazahl="{e(wert)}">{e(wert)}</i><span>.00</span></p>'
                f'<p class="spt__was">{e(t_)}</p>{f"<p class=spt__zusatz>{e(zusatz)}</p>" if zusatz else ""}</div>')

    inhalt = B.kopf_tag('anfang', 'Spa nebenan · ' + D.SPA_TITEL, 'Entspannung pur, gleich nebenan.', 'gleich nebenan.', D.SPA_SATZ, 'spa-garten', '50% 55%')
    inhalt += B.kapitel('hinueber', 'k-spw', f'''
    <div class="kap__kopf spa-mitte">{B.ueber('Der Weg hinüber')}{B.titel('Nebenan ist alles bereit.', em='alles bereit.')}</div>
    <div class="spw__bilder">{fo('f-wellness', 'spw__haus', '50% 72%', '(max-width:860px) 100vw, 60vw')}{fo('spa-wasser', 'spw__liege', '27% 50%', '(max-width:860px) 100vw, 34vw', 'Ruheliege im Bademantel im Spa des Partnerhotels')}</div>
    <div class="spw__bereit" data-steig><p class="spw__dinge">{"".join(f"<span>{e(d)}</span>" for d in dinge)}</p><p class="spw__satz">stehen zur Verfügung</p></div>''', 'Der Weg hinüber')
    inhalt += B.kapitel('angebot', 'k-spr', f'''
    <div class="kap__kopf spa-mitte">{B.ueber('Das Angebot')}{B.titel('Vom Schwimmbad bis zum Beautysalon.', em='Beautysalon.')}</div>
    <div class="spr">{folge}</div>''', 'Das Angebot')
    inhalt += B.kapitel('eintritt', 'k-spt', f'''
    <div class="kap__kopf spa-mitte">{B.ueber('Der Eintritt')}{B.titel('Ein Tag oder die ganze Woche.', em='die ganze Woche.')}</div>
    <div class="spt" data-steig>{fo('spa-licht', 'spt__bild', '50% 45%', '(max-width:860px) 100vw, 1040px')}
      <div class="spt__platte"><div class="spt__zeile">{"".join(tarif(*x) for x in D.SPA_TARIFE)}</div>
        <div class="kn-reihe kn-reihe--mitte">{B.kn('Zum Spa des Partnerhotels', D.SPA_LINK, 'kn--laerche', neu=True)}</div></div>
    </div>{ZAEHL}''', 'Der Eintritt', weiter=('Am Abend leuchten vor dem Röstihüs die alten Gondeln.', 'roestihues.html', 'Abend im Röstihüs'))
    return B.kopf('Spa nebenan · Hotel Monte-Moro', 'Das Spa im Partnerhotel Pirmin Zurbriggen nebenan, mit Tarifen für Gäste des Hotel Monte-Moro.', 'spa.html') + inhalt + B.fuss()
