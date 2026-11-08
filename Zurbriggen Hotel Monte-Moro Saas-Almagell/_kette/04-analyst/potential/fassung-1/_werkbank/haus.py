"""Hotel Monte-Moro, Saas-Almagell · Potentialanalyse (Station 4 der Kette, 17.10.2026): Haken für das Werkbank-Kit.

Aufbau wie die Analyse des Castell Son Claret (Fassung 7, `_Archiv/Castell Son Claret/_kette/04-analyst/potential/_werkbank/haus.py`),
Farben und Zeichen vom Haus: Blau des Logos (#115595, allgem_logo.png) und der Seite (#005794, #6bb1de, template.css),
Lärche der Balkone als warmer Akzent (Fassade, Schweiz Tourismus 00072098), Schnee und Fassade als helle Flächen.
Station 5 (Markenbuch) steht noch aus: die Farbwelt ist abgeleitet, nicht bestätigt (offen in stand.json).
Zeichen: der Bergkamm aus dem Logo (potrace), Wortmarke: das ganze Logo. Titelschrift Young Serif (Ersatz, bis Station 5 die Schrift festlegt)."""
import os, re
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKE = os.path.join(ROOT, '..', '_bau', 'marke')
NAME = 'Hotel Monte-Moro'
KURZ = 'monte-moro'
LEISTE = ''
PORT = 8978
DOMAIN = 'monte-moro.ch'
HEUTE_URL = 'https://www.monte-moro.ch/de/'
RECHTE = 'dem Hotel Monte-Moro und den jeweiligen Fotografen.'

FARBEN = dict(nacht='#0B2A4C', tief='#071F39', navy='#115595', blau='#1E68AE', papier='#F1EFEA', creme='#E7E2D9', weiss='#FFFFFF',
              gold='#C98A5A', messing='#A8603C', taupe='#A8603C', tinte='#0B2A4C', punkt='#C98A5A', rot='#B5442C')
SAND = '#E3D3C2'

SCHRIFT = dict(titel=('Young Serif', 'YoungSerif.woff2'), titel_folge="Georgia,'Times New Roman',serif",
               ersatz="local('Georgia');size-adjust:104%", druckgewicht=400)
SCHRIFT_MEHR = []
DRUCKQUELLEN = []
DRUCKSCHRIFT = []

MUSTER = 'url(muster.webp)'
MUSTER_B = '560px'
MUSTER_BILD = 'bilder/tapete-dunkel.webp'


def _ohne_fill(vb_innen):
    vb, innen = vb_innen
    innen = re.sub(r'\s+fill="#[0-9a-fA-F]{3,6}"', '', innen)
    return vb, innen


ZEICHEN = _ohne_fill(K.svg_innen(os.path.join(MARKE, 'zeichen.svg')))   # der Bergkamm aus dem Logo
WORT = _ohne_fill(K.svg_innen(os.path.join(MARKE, 'wort.svg')))         # das ganze Logo mit «Saas-Almagell»

ETIKETTEN = dict(ordner='kofferetiketten', name='Kofferaufkleber', einzahl='Kofferaufkleber')
SEITEN = []

CSS = '''
/* ---------- Hotel Monte-Moro, Potentialanalyse: Platten mit Kuhle, hell und dunkel (nach Grand Beau-Rivage _gbr.css) ---------- */
:root{
  --platte-h:linear-gradient(180deg,#ffffff,#F1EFEA 58%,#DDD6CA);--platte-h-s:inset 0 1px 0 #fff,inset 0 0 0 1px rgba(11,42,76,.14),0 1.5px 0 #C9BFAF,0 38px 50px -32px rgba(11,42,76,.45);
  --kuhle-h:linear-gradient(180deg,#D9D1C4,#E8E4DC 42%,#EFEDE8);--kuhle-h-s:inset 0 3px 7px -1px rgba(11,42,76,.2),inset 0 1px 0 rgba(11,42,76,.12),inset 0 0 0 1px rgba(11,42,76,.1),0 1px 0 #fff;
  --platte-d:linear-gradient(180deg,#1E68AE,#115595 46%,#0C3F72);--platte-d-s:inset 0 1px 0 rgba(255,255,255,.12),inset 0 0 0 1px rgba(201,138,90,.3),0 2px 0 #04172C,0 40px 50px -32px rgba(0,0,0,.7);
  --kuhle-d:linear-gradient(180deg,#061A31,#0A2340 34%,#0B2543);--kuhle-d-s:inset 0 3px 6px -1px rgba(0,4,16,.62),inset 0 1px 0 rgba(0,4,16,.55),inset 0 0 0 1px rgba(0,4,16,.3),0 1px 0 rgba(255,255,255,.08);
  --sand:#E3D3C2;
}
.tapete-hell{background-image:url(tapete-hell.webp);background-size:560px auto;background-position:50% 0}
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(11,42,76,.42)}
.platte{border-radius:clamp(22px,2.4vw,34px);background:var(--platte-h);box-shadow:var(--platte-h-s);color:var(--tinte)}
.kuhle{border-radius:clamp(16px,1.6vw,22px);background:var(--kuhle-h);box-shadow:var(--kuhle-h-s)}
.fl--nacht .platte,.fl--navy .platte,.fl--tief .platte,.dunkel .platte{background:var(--platte-d);box-shadow:var(--platte-d-s);color:#fff}
.fl--nacht .kuhle,.fl--navy .kuhle,.fl--tief .kuhle,.dunkel .kuhle{background:var(--kuhle-d);box-shadow:var(--kuhle-d-s)}
.rot{color:var(--rot)}

/* ---------- Abschnittsköpfe mittig, Zeichen des Hauses in Gold darüber (GBR kopf_mitte.py) ---------- */
.kap--z{flex-direction:column;justify-content:center;gap:clamp(16px,1.6vw,24px);text-align:center;margin-bottom:clamp(18px,2vw,30px);color:var(--gold)}
.fl--papier .kap--z,.fl--creme .kap--z{color:var(--gold)}
.kap__z{display:block;width:clamp(64px,7vw,104px);height:auto;flex:none;fill:currentColor}
.kap--z span{font-family:var(--mono);font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;color:rgba(11,42,76,.82)}
.fl--navy .kap--z span,.fl--nacht .kap--z span,.schluss .kap--z span{color:var(--gold)}
.kap--z~.zt{font-size:clamp(2.2rem,5.4vw,5.8rem);line-height:1.04;text-align:center}
.kopfzeile--mitte{display:block;text-align:center;margin-bottom:clamp(52px,6vw,96px)}
.kopfzeile--mitte .zt .z>span{margin-inline:auto}
.kopfzeile--mitte .lauf{max-width:62ch;margin:clamp(20px,2.3vw,34px) auto 0;padding-bottom:0}
.fl>.in>.kopfzeile--mitte:first-child{padding-top:clamp(8px,1.4vw,24px)}

/* ---------- Fenster: Foto fest hinter den Nachbarn, Satz des Hauses (GBR fenster_ausblick.py) ---------- */
.wfen{position:relative;min-height:min(84vh,800px);margin-top:calc(var(--rund)*-1);color:#fff}
.wfen::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--nacht)}
.wfen__f{position:absolute;left:0;right:0;top:-100vh;top:-100lvh;bottom:-100vh;bottom:-100lvh;pointer-events:none}
.wfen__f>img{position:sticky;top:0;z-index:-1;display:block;width:100%;height:100vh;height:100lvh;object-fit:cover;margin-bottom:-100vh;margin-bottom:-100lvh}
.wfen__in{position:sticky;top:50%;z-index:-1;transform:translateY(-50%);padding:0 var(--rand);text-align:center}
.wfen.weg .wfen__in{visibility:hidden}
.wfen__z{display:block;width:clamp(64px,7vw,104px);height:auto;margin:0 auto clamp(18px,2vw,30px);color:var(--gold);fill:currentColor}
.wfen__t{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,4.2vw,4.4rem);line-height:1.1;color:#fff;text-wrap:balance;max-width:24ch;margin-inline:auto;
  text-shadow:0 .02em .04em rgba(3,10,16,.82),0 .06em .16em rgba(3,10,16,.7),0 .14em .42em rgba(3,10,16,.5)}
.wfen__t span{display:block}
.wfen__t em{font-style:normal;color:var(--gold)}
.wfen__k{margin:clamp(16px,1.8vw,26px) auto 0;max-width:44ch;font-family:var(--mono);font-size:12.5px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.86);text-shadow:0 1px 2px rgba(3,10,16,.92),0 2px 10px rgba(3,10,16,.78)}
.wfen__z,.wfen__t span,.wfen__k{opacity:0;transform:translateY(34px);transition:opacity 1.3s var(--e1),transform 1.7s var(--e1)}
.wfen__t span:nth-child(1){transition-delay:.12s}.wfen__t span:nth-child(2){transition-delay:.24s}.wfen__k{transition-delay:.42s}
.wfen.da .wfen__z,.wfen.da .wfen__t span,.wfen.da .wfen__k{opacity:1;transform:none}
.wfen+.fl{border-radius:var(--rund) var(--rund) 0 0}
.fl.vor-fenster{border-radius:0 0 var(--rund) var(--rund);padding-bottom:var(--abschnitt)}
@media(max-width:860px){.wfen{min-height:62svh}}
@media (prefers-reduced-motion:reduce){.wfen__z,.wfen__t span,.wfen__k{opacity:1;transform:none;transition:none}}

/* ---------- Auftakt «titelblatt»: Inhaltsverzeichnis als Blatt, zwei Abzüge ---------- */
.auftakt--titelblatt{background:var(--nacht)}
.auftakt--titelblatt::after{content:'';position:absolute;inset:0;z-index:0;background:linear-gradient(180deg,rgba(11,42,76,.25),rgba(11,42,76,.1) 40%,rgba(11,42,76,.78) 100%);pointer-events:none}
.tb__inhalt a small{color:rgba(11,42,76,.72)}
.tb__inhalt a b{font-weight:400}
.auftakt .in.tb__kopf{color:rgba(255,255,255,.86)}
.auftakt .in.tb__kopf span{font-family:var(--mono);letter-spacing:.16em;text-transform:uppercase;font-size:12px}
.auftakt h1 em{color:var(--gold)}
.auftakt .lauf{color:rgba(255,255,255,.9)}
.auftakt .stand{margin-top:clamp(20px,2.4vw,34px);font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}

/* ---------- Hero wie das Markenbuch der Station 5: Nacht mit Tapete, Zeichen und Wortmarke in Gold, alles mittig ---------- */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:clamp(110px,14vh,170px) var(--rand) clamp(60px,8vh,100px);background-color:var(--nacht);color:#fff;text-align:center;overflow:clip}
.hero__in{display:flex;flex-direction:column;align-items:center;max-width:1100px;margin:0 auto}
.hero__kap{display:flex;align-items:center;gap:18px;font-family:var(--mono);font-size:12.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold)}
.hero__kap i{width:clamp(28px,4vw,64px);height:1px;background:currentColor;opacity:.6}
.hero__z{margin:clamp(30px,4vw,54px) 0 clamp(22px,2.6vw,36px)}
.hero__z svg{width:clamp(72px,8vw,120px);height:auto;display:block}
[data-a="zeichen"]{opacity:0;transform:scale(.62) rotate(-14deg);transition:opacity 1.2s var(--e2),transform 2.2s var(--feder);transition-delay:calc(var(--i,0)*140ms)}
[data-a="zeichen"].da{opacity:1;transform:none}
.hero__w{margin-top:clamp(34px,4.4vw,60px)}
.hero__w svg{width:min(520px,76vw);height:auto;display:block}
@media(max-width:600px){.hero__kap{letter-spacing:.18em;font-size:11.5px}.hero__kap i{display:none}.hero__ort{letter-spacing:.3em}}
.hero__ort{display:flex;align-items:center;gap:16px;margin-top:clamp(18px,2vw,30px);font-family:var(--mono);font-size:12.5px;letter-spacing:.42em;text-transform:uppercase;color:var(--gold)}
.hero__ort i{width:clamp(24px,3vw,48px);height:1px;background:currentColor;opacity:.6}
.hero__t{margin-top:clamp(34px,4.4vw,64px);font-size:clamp(2.6rem,6vw,6.4rem);color:#fff}
.hero__t .z>span{margin-inline:auto}
.hero__t em{color:var(--gold)}
.hero__lead{max-width:640px;margin:clamp(24px,2.8vw,40px) 0 0;font-size:clamp(1.06rem,1.24vw,1.24rem);line-height:1.72;color:rgba(255,255,255,.86)}
.hero .kn-reihe{margin-top:clamp(28px,3vw,44px)}
.hero__runter{position:absolute;left:50%;bottom:0;width:1px;height:clamp(44px,6vw,80px);margin-left:-.5px;background:rgba(201,138,90,.22);overflow:hidden}
.hero__runter::after{content:'';position:absolute;left:0;top:0;width:100%;height:50%;background:var(--gold);animation:heroRunter 2.6s var(--e2) infinite}
@keyframes heroRunter{0%{transform:translateY(-100%)}60%{transform:translateY(100%)}100%{transform:translateY(200%)}}
.hero+.fl{border-radius:var(--rund) var(--rund) 0 0}
@media (prefers-reduced-motion:reduce){.hero__runter::after{animation:none}[data-a="zeichen"]{opacity:1;transform:none}}

/* ---------- Pult je Bereich: Pfeil-Knäufe, Zähler, Zeichen je Punkt (Robert 15.10.2026: «mit Pfeilen, Zeichen, Symbolen», nicht ans Scrollen gekoppelt) ---------- */
.pult{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:clamp(10px,1.6vw,24px);padding:clamp(10px,1.2vw,16px) clamp(10px,1.4vw,20px);margin-bottom:clamp(16px,1.8vw,24px);outline:none}
.pult:focus-visible{box-shadow:var(--platte-h-s),0 0 0 2px var(--gold)}
.pult__m{display:flex;flex-direction:column;align-items:center;gap:8px;min-width:0}
.pult__zahl{display:flex;align-items:baseline;gap:14px;font-family:var(--mono);font-size:12px;letter-spacing:.17em;text-transform:uppercase;color:rgba(11,42,76,.8)}
.pult__zahl b{font-weight:400;color:var(--messing)}
.pult__zahl span{font-family:var(--serif);font-size:1.15rem;letter-spacing:0;text-transform:none;color:var(--tinte)}
.fl--navy .pult__zahl,.fl--nacht .pult__zahl{color:rgba(255,255,255,.8)} .fl--navy .pult__zahl b,.fl--nacht .pult__zahl b{color:var(--gold)} .fl--navy .pult__zahl span,.fl--nacht .pult__zahl span{color:#fff}
.pult__reihe{display:flex;gap:clamp(4px,.7vw,10px);max-width:100%;overflow-x:auto;scrollbar-width:none;padding:4px 6px;scroll-snap-type:x proximity}
.pult__reihe::-webkit-scrollbar{display:none}
.pult__reihe button{flex:none;display:flex;flex-direction:column;align-items:center;gap:6px;padding:4px 6px 2px;border-radius:14px;color:var(--tinte);scroll-snap-align:center;transition:transform .45s var(--e2)}
.pult__reihe button:hover{transform:translateY(-2px)}
.pult__reihe button i{width:clamp(42px,3.4vw,50px);height:clamp(42px,3.4vw,50px);border-radius:50%;display:grid;place-items:center;background:var(--kuhle-h);box-shadow:var(--kuhle-h-s);color:var(--tinte);transition:transform .5s var(--e3)}
.pult__reihe button svg{width:21px;height:21px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.pult__reihe button b{font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.1em;color:rgba(11,42,76,.72)}
.pult__reihe button[aria-pressed="true"] i{background:linear-gradient(180deg,#1E68AE,#115595 50%,#0C3F72);color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.24),inset 0 -2px 0 rgba(0,0,0,.45),0 10px 16px -10px rgba(11,42,76,.7);transform:scale(1.08)}
.pult__reihe button[aria-pressed="true"] b{color:var(--tinte)}
.fl--navy .pult__reihe button i,.fl--nacht .pult__reihe button i{background:var(--kuhle-d);box-shadow:var(--kuhle-d-s);color:#fff}
.fl--navy .pult__reihe button b,.fl--nacht .pult__reihe button b{color:rgba(255,255,255,.7)}
.fl--navy .pult__reihe button[aria-pressed="true"] i,.fl--nacht .pult__reihe button[aria-pressed="true"] i{background:linear-gradient(180deg,#F6E6D6,#C98A5A 55%,#8E4E2C);color:var(--nacht);box-shadow:inset 0 1px 0 rgba(255,255,255,.7),inset 0 -2px 0 rgba(0,0,0,.35),0 10px 16px -10px rgba(0,0,0,.7)}
.fl--navy .pult__reihe button[aria-pressed="true"] b,.fl--nacht .pult__reihe button[aria-pressed="true"] b{color:#fff}
.pult .rund{width:52px;height:52px}
.pult .rund[disabled]{opacity:.35}
.fl--navy .pult .rund,.fl--nacht .pult .rund{color:var(--tinte);background:linear-gradient(180deg,#F6E6D6,#E3D3C2);box-shadow:inset 0 1px 0 rgba(255,255,255,.9),inset 0 -3px 0 rgba(110,60,30,.38),0 14px 22px -12px rgba(0,0,0,.6)}
@media(max-width:700px){.pult{grid-template-columns:auto minmax(0,1fr) auto;gap:8px;padding:10px}.pult .rund{width:44px;height:44px}.pult__zahl{gap:10px;font-size:11px}.pult__zahl span{font-size:1rem}.pult__reihe button i{width:40px;height:40px}}
.blaetter{touch-action:pan-y}
/* zwei Karten am Ende des Bereichs: Was hier stimmt, Ohne uns zu beheben */
.bereich__ende{display:grid;gap:clamp(14px,1.8vw,24px);margin-top:clamp(18px,2.2vw,30px)}
@media(min-width:960px){.bereich__ende{grid-template-columns:1fr 1fr}.bereich__ende--eins{grid-template-columns:minmax(0,1fr)}}
.bereich__karte .pb__text{padding:clamp(22px,2.6vw,34px) clamp(18px,2.4vw,34px) clamp(20px,2.4vw,30px)}
.pb__ko--mitte{justify-content:center;font-size:1.3rem;margin-bottom:16px}
.bereich__karte p{font-size:.98rem;line-height:1.62}
.bereich__karte .pb__text{text-align:left}
.bereich__karte .pb__ko--mitte{justify-content:center}
.pb__text ul{justify-items:start;max-width:none}
.pb__text li{margin-inline:0;max-width:none}
/* ---------- Auftakt nach dem Muster der Rivage-Werkbank (Master 5b Punkt 1): grosses echtes Foto, Wortmarke scharf, Titel in Fahkwang, drei Fotos als 3D-Kacheln, ein Knopf ---------- */
.hero2{position:relative;min-height:100svh;display:flex;flex-direction:column;padding:clamp(96px,12vh,150px) var(--rand) calc(clamp(26px,4vh,48px) + var(--rund));color:#fff;background:var(--nacht);overflow:clip}
.hero2__bild{position:absolute;inset:0;z-index:0;width:100%;height:100%;object-fit:cover;object-position:50% 62%}
.hero2::after{content:'';position:absolute;inset:0;z-index:0;background:linear-gradient(180deg,rgba(11,42,76,.3) 0%,rgba(11,42,76,.05) 32%,rgba(11,42,76,.55) 72%,rgba(11,42,76,.9) 100%);pointer-events:none}
.hero2>.in{position:relative;z-index:1;width:100%}
.hero2__kopf{display:flex;justify-content:space-between;align-items:center;gap:20px;padding-bottom:16px;border-bottom:1px solid rgba(201,138,90,.5);font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.88)}
.hero2__wort{width:clamp(150px,14vw,210px);height:auto;flex:none;color:#fff;filter:drop-shadow(0 2px 6px rgba(3,10,16,.55))}
.hero2__in{display:grid;gap:clamp(34px,5vw,70px);align-items:end;margin-top:auto;padding-top:clamp(40px,6vh,80px)}
@media(min-width:1080px){.hero2__in{grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr)}}
.hero2__t .gruss{font-family:var(--serif);font-size:clamp(1.08rem,1.3vw,1.34rem);color:var(--gold);margin-bottom:clamp(16px,2vw,28px);display:flex;align-items:center;gap:16px}
.hero2__t .gruss::before{content:'';width:clamp(40px,5vw,84px);height:1px;background:currentColor;opacity:.75}
.hero2__t h1{font-size:clamp(3rem,6vw,6.6rem);text-shadow:0 .03em .08em rgba(3,10,16,.6)}
.hero2__t h1 em{color:var(--gold)}
.hero2__t .lauf{margin-top:clamp(20px,2.4vw,34px);max-width:44ch;color:rgba(255,255,255,.92);text-shadow:0 1px 3px rgba(3,10,16,.6)}
.hero2__t .kn-reihe{margin-top:clamp(26px,3vw,42px);justify-content:flex-start}
.hero2__k{position:relative;aspect-ratio:1/.78;width:100%;max-width:760px;justify-self:end}
.hk{position:absolute;border-radius:clamp(16px,1.6vw,24px);padding:7px;background:linear-gradient(180deg,rgba(255,255,255,.2),rgba(255,255,255,.06));box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 0 0 1px rgba(201,138,90,.4),0 50px 70px -40px rgba(0,0,0,.95);will-change:transform}
.hk img{display:block;width:100%;height:100%;object-fit:cover;border-radius:clamp(11px,1.1vw,17px);aspect-ratio:4/3}
.hk--1{left:0;top:9%;width:58%;--r:-3deg;--r0:-9deg;z-index:1}
.hk--2{right:0;top:0;width:40%;--r:4deg;--r0:11deg;z-index:2}
.hk--2 img{aspect-ratio:1}
.hk--3{right:5%;bottom:0;width:48%;--r:-2deg;--r0:-7deg;z-index:3}
.hk--3 img{aspect-ratio:3/2}
.hero2__fuss{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px 30px;margin-top:clamp(40px,6vh,76px);padding-top:16px;border-top:1px solid rgba(201,138,90,.4);font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.78)}
.hero2__fuss .runter{color:var(--gold)}
.hero2+.fl{border-radius:var(--rund) var(--rund) 0 0}
@media(max-width:1079px){.hero2__k{max-width:560px;justify-self:center;margin-top:10px}}
@media(max-width:600px){.hero2__kopf span{display:none}.hero2__wort{width:150px}.hero2__k{aspect-ratio:1/.9}.hk--1{width:62%}.hk--2{width:42%}.hk--3{width:50%}.hero2__fuss span:nth-child(3){display:none}}
/* ---------- Brief ---------- */
.schild small{color:rgba(11,42,76,.8);font-size:11.5px}
.zk__t b{color:var(--messing)}
.bf-ich .gastgeber__t{color:rgba(11,42,76,.88)}
.schild{background:var(--papier);color:var(--tinte)}
.werte span{color:var(--tinte)}

/* ---------- Auf einen Blick: vier Zahlen auf Fotos (gabe) ---------- */
.gabe b.odo{color:var(--gold)}
.gabe{min-height:clamp(340px,30vw,440px)}
.gabe__d{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,42,76,.18),rgba(11,42,76,.82) 100%)}
.gabe h3{font-size:1.5rem}
.blick__u{display:grid;gap:clamp(14px,1.8vw,24px);margin-top:clamp(28px,3.2vw,48px);align-items:start}
@media(min-width:1000px){.blick__u{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}}
.blick__u .platte{padding:clamp(22px,2.6vw,36px)}
.blick__u h3{font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2vw,2rem);line-height:1.14;margin-bottom:12px}
.blick__u p{color:rgba(255,255,255,.84);line-height:1.62}
.blick__u p+p{margin-top:.9em}
.luecken{display:grid;gap:10px;margin-top:14px}
.luecken li{position:relative;padding:12px 16px 12px 42px;border-radius:14px;background:var(--kuhle-d);box-shadow:var(--kuhle-d-s);line-height:1.5;color:rgba(255,255,255,.88);font-size:.98rem}
.luecken li::before{content:'';position:absolute;left:18px;top:19px;width:9px;height:9px;border-radius:50%;background:var(--rot);box-shadow:0 0 0 3px rgba(138,43,43,.28)}
.luecken li small{display:block;margin-top:4px;font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#E9A2A2}
details.methode{margin-top:14px;border-radius:14px;background:var(--kuhle-d);box-shadow:var(--kuhle-d-s);color:rgba(255,255,255,.86)}
details.methode summary{cursor:pointer;list-style:none;padding:14px 18px;font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);display:flex;justify-content:space-between;align-items:center}
details.methode summary::-webkit-details-marker{display:none}
details.methode summary i{width:10px;height:10px;border-right:1.4px solid currentColor;border-bottom:1.4px solid currentColor;transform:rotate(45deg);transition:transform .4s var(--e2)}
details.methode[open] summary i{transform:rotate(-135deg)}
details.methode .methode__t{padding:0 18px 18px;line-height:1.62;font-size:.98rem}
details.methode .methode__t p+p{margin-top:.8em}

/* ---------- Was zuerst zählt: fünf Platten mit Kuhle ---------- */
.zuerst{display:grid;gap:clamp(12px,1.4vw,20px);grid-template-columns:repeat(5,minmax(0,1fr))}
@media(max-width:1180px){.zuerst{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.zuerst{grid-template-columns:1fr}}
.zk{display:flex;flex-direction:column;padding:9px;text-decoration:none;transition:transform .55s var(--e2)}
.zk:hover{transform:translateY(-4px)}
.zk .kuhle{flex:1;display:flex;flex-direction:column;gap:10px;padding:22px 20px 20px}
.zk__z{font-family:var(--serif);font-weight:500;font-size:clamp(2.6rem,3.6vw,3.9rem);line-height:.95;color:var(--nacht);letter-spacing:-.01em;white-space:nowrap}
.zk__s{font-size:.95rem;line-height:1.5;color:rgba(11,42,76,.9)}
.zk__t{margin-top:auto;padding-top:14px;border-top:1px solid rgba(11,42,76,.16);font-family:var(--serif);font-size:1.08rem;line-height:1.25;color:var(--tinte)}
.zk__t b{font-weight:400;color:var(--taupe);margin-right:6px}
.zk__f{display:flex;justify-content:space-between;align-items:center;padding:12px 10px 4px 14px;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:rgba(11,42,76,.8)}
.knauf{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:#fff;background:linear-gradient(180deg,#1E68AE,#115595 50%,#0C3F72);box-shadow:inset 0 1px 0 rgba(255,255,255,.24),inset 0 -2px 0 rgba(0,0,0,.45),0 8px 12px -8px rgba(11,42,76,.7);transition:transform .5s var(--e2)}
.knauf svg{width:12px;height:12px;stroke:currentColor;fill:none;stroke-width:1.4}
.zk:hover .knauf{transform:translate(2px,-2px)}

/* ---------- Zehn Bereiche: Kacheln mit Namensfeld und Einkerbung ---------- */
.bereiche10{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:clamp(12px,1.4vw,22px)}
@media(max-width:1100px){.bereiche10{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:620px){.bereiche10{grid-template-columns:repeat(2,minmax(0,1fr))}}
.bk10{display:block;padding:8px;text-decoration:none;color:var(--tinte);transition:transform .55s var(--e2)}
.bk10:hover{transform:translateY(-4px)}
.bk10__b{position:relative;display:block;aspect-ratio:4/5;border-radius:clamp(14px,1.5vw,20px);overflow:hidden;background:var(--tief)}
.bk10__b img{width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--e2)}
.bk10:hover .bk10__b img{transform:scale(1.05)}
.kerbe{--f:#F1EFEA;--e:16px;position:absolute;z-index:2;left:-1px;bottom:-1px;display:block;padding:9px 14px 5px 12px;border-radius:0 var(--e) 0 0;background:var(--f);color:var(--navy);font-family:var(--serif);font-size:1.5rem;line-height:1}
.kerbe::before,.kerbe::after{content:'';position:absolute;width:var(--e);height:var(--e);background:radial-gradient(circle at 100% 0,transparent calc(var(--e) - .5px),var(--f) var(--e))}
.kerbe::before{left:0;bottom:100%}.kerbe::after{left:100%;bottom:0}
.bk10__n{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 6px 6px 10px}
.bk10__n b{font-family:var(--serif);font-weight:400;font-size:1.06rem;line-height:1.18}
.bk10__n small{display:block;margin-top:3px;font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(11,42,76,.78)}
.bk10 .knauf{flex:none;width:32px;height:32px}

/* ---------- Je Bereich eine Bühne: grosses Foto als Kachel, Wahl der Punkte, Blatt auf einer Platte ---------- */
.kf{display:block;padding:9px;margin-bottom:clamp(26px,3vw,44px)}
.kf__b{position:relative;border-radius:clamp(16px,1.8vw,26px);overflow:hidden;aspect-ratio:21/9;background:var(--tief)}
.kf__b img{width:100%;height:100%;object-fit:cover;object-position:var(--op,50% 50%)}
.kf .kerbe{font-size:clamp(1.5rem,2vw,2.1rem);padding:12px 20px 8px 16px}
.fl--navy .kf .kerbe,.fl--nacht .kf .kerbe{--f:#0B2A4C;color:var(--gold)}
@media(max-width:700px){.kf__b{aspect-ratio:4/3}}
.wahl{margin-bottom:clamp(18px,2vw,28px)}
@media(min-width:1000px){.wahl{flex-wrap:wrap;overflow:visible;margin-left:0;margin-right:0;padding-left:0;padding-right:0;row-gap:10px}}
.wahl button{display:inline-flex;align-items:center;gap:12px;height:48px}
.wahl button b{font-family:var(--serif);font-weight:400;font-size:15px;letter-spacing:0;text-transform:none;opacity:.9}
.wahl button em{font-style:normal;opacity:.6;letter-spacing:.08em;font-size:10.5px}
.wahl button.wahl--x{opacity:.86}
.blatt-p{display:none}
.blatt-p.an{display:block}
.pb{padding:clamp(10px,1.1vw,14px)}
.pb__band{display:grid;grid-template-columns:auto 1px minmax(0,1fr);gap:clamp(18px,2.6vw,38px);align-items:center;padding:clamp(20px,2.4vw,32px) clamp(22px,2.8vw,40px)}
.pb__z{font-family:var(--serif);font-weight:500;font-size:clamp(56px,6.4vw,100px);line-height:.95;letter-spacing:-.02em;color:var(--nacht);white-space:nowrap}
.pb__z.s3{font-size:clamp(46px,5vw,78px)}.pb__z.s4{font-size:clamp(38px,4vw,62px)}
@media(max-width:700px){.pb__band{grid-template-columns:1fr;gap:12px;padding:22px 20px}.pb__strich{display:none}.pb__z{font-size:clamp(48px,14vw,64px)}.pb__z.s3,.pb__z.s4{font-size:clamp(36px,10vw,48px)}}
.fl--navy .pb__z,.fl--nacht .pb__z{color:var(--gold)}
.pb__strich{align-self:stretch;width:1px;background:rgba(11,42,76,.22)}
.fl--navy .pb__strich,.fl--nacht .pb__strich{background:rgba(201,138,90,.3)}
.pb__nr{margin:0 0 6px;font-family:var(--mono);font-size:12px;letter-spacing:.17em;text-transform:uppercase;color:rgba(11,42,76,.8)}
.fl--navy .pb__nr,.fl--nacht .pb__nr{color:var(--gold)}
.pb__satz{margin:0;font-family:var(--serif);font-size:clamp(1.1rem,1.5vw,1.45rem);line-height:1.38;color:var(--tinte)}
.fl--navy .pb__satz,.fl--nacht .pb__satz{color:rgba(255,255,255,.92)}
.pb__k{padding:clamp(22px,2.8vw,40px) clamp(16px,2.2vw,32px) clamp(10px,1.4vw,18px)}
.pb__k h3{font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2.2vw,2.2rem);line-height:1.16;max-width:30ch}
.pb__kurz{margin-top:clamp(14px,1.6vw,22px);font-size:clamp(1.06rem,1.22vw,1.22rem);line-height:1.66;max-width:68ch;color:rgba(11,42,76,.92)}
.fl--navy .pb__kurz,.fl--nacht .pb__kurz{color:rgba(255,255,255,.86)}
.pb__zwei{display:grid;gap:clamp(12px,1.4vw,20px);margin-top:clamp(20px,2.4vw,32px)}
@media(min-width:900px){.pb__zwei{grid-template-columns:1fr 1fr}}
.pb__zwei .kuhle{padding:20px 22px 18px;font-size:.98rem;line-height:1.62;color:rgba(11,42,76,.92)}
.fl--navy .pb__zwei .kuhle,.fl--nacht .pb__zwei .kuhle{color:rgba(255,255,255,.86)}
.pb__zwei p+p{margin-top:.75em}
.pb__ko{display:flex;align-items:center;gap:10px;margin-bottom:10px;font-family:var(--serif);font-size:1.08rem;color:var(--tinte)}
.fl--navy .pb__ko,.fl--nacht .pb__ko{color:#fff}
.pb__ko svg{width:20px;height:auto;color:var(--gold);fill:currentColor;flex:none}
.pb__ko i{width:16px;height:16px;flex:none;display:grid;place-items:center}
.pb__ko i svg{width:16px;height:16px;fill:none;stroke:var(--gold);stroke-width:1.6}
.pb__nach{margin-top:clamp(18px,2vw,28px);padding-top:16px;border-top:1px solid rgba(11,42,76,.16)}
.fl--navy .pb__nach,.fl--nacht .pb__nach{border-color:rgba(201,138,90,.26)}
.pb__nach .etik{margin-bottom:10px;color:rgba(11,42,76,.8);justify-content:center}
.fl--navy .pb__nach .etik,.fl--nacht .pb__nach .etik{color:var(--gold)}
.pb__nach p{font-size:.98rem;line-height:1.6;color:rgba(11,42,76,.88);max-width:78ch}
.fl--navy .pb__nach p,.fl--nacht .pb__nach p{color:rgba(255,255,255,.82)}
.pb__ziele{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.pb__f{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:center;margin-top:clamp(20px,2.4vw,30px)}
.pb__f .kn-reihe{gap:10px}
.pb__text{padding:clamp(22px,2.8vw,40px) clamp(16px,2.2vw,32px) clamp(18px,2vw,30px)}
.pb__text h3{font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2.2vw,2.2rem);line-height:1.16;margin-bottom:clamp(14px,1.6vw,22px)}
.pb__text p,.pb__text li{font-size:1.02rem;line-height:1.66;color:rgba(11,42,76,.92);max-width:72ch}
.fl--navy .pb__text p,.fl--nacht .pb__text p,.fl--navy .pb__text li,.fl--nacht .pb__text li{color:rgba(255,255,255,.86)}
.pb__text p+p{margin-top:.9em}
.pb__text p b{font-weight:400;color:var(--tinte)}
.fl--navy .pb__text p b,.fl--nacht .pb__text p b{color:#fff}
.pb__text ul{display:grid;gap:10px}
.pb__text li{position:relative;padding-left:24px}
.pb__text li::before{content:'';position:absolute;left:2px;top:.62em;width:12px;height:7px;border-left:1.5px solid var(--gold);border-bottom:1.5px solid var(--gold);transform:rotate(-45deg)}
.pb a:not(.kn){color:inherit;text-decoration:underline;text-decoration-color:rgba(201,138,90,.6);text-underline-offset:3px}
code{font-family:var(--mono);font-size:.86em;letter-spacing:0;text-transform:none;opacity:.92}
/* Auftritt beim Wechsel eines Punktes: Band und Kacheln steigen federleicht herein */
.blatt-p .steig{opacity:0;transform:translateY(34px);transition:opacity .9s var(--e1),transform 1.25s var(--e1);transition-delay:calc(var(--i,0)*90ms)}
.blatt-p.an.da .steig{opacity:1;transform:none}

/* ---------- Auftritte wie im Markenbuch (Station 5): Hochschweben mit Feder, einmal pulsierend, Foto zoomt in seinem Rahmen; nur transform und opacity ---------- */
:root{--feder:cubic-bezier(.28,1.42,.42,1)}
[data-a="feder"]{opacity:0;transform:translate3d(0,clamp(80px,9vw,140px),0) scale(.93);transform-origin:50% 100%;transition:transform 2.1s var(--feder),opacity 1s var(--e2);transition-delay:calc(var(--vz,0ms) + var(--i,0)*140ms)}
[data-a="feder"].da{opacity:1;transform:none}
.js [data-a="feder"] .zb img{transform:scale(1.14);transition:transform 2.6s var(--e1);transition-delay:calc(var(--vz,0ms) + var(--i,0)*140ms)}
.js [data-a="feder"].da .zb img{transform:none}
.js .gabe[data-a="feder"] .gabe__b{transform:scale(1.16)}
.js .gabe[data-a="feder"].da .gabe__b{transform:scale(1.04);transition:transform 2.6s var(--e1)}
.js .gabe[data-a="feder"].da:hover .gabe__b{transform:scale(1.1);transition:transform 1.6s var(--e2)}
.blatt-p .steig{opacity:0;transform:translate3d(0,clamp(40px,5vw,70px),0) scale(.97);transform-origin:50% 100%;transition:opacity .9s var(--e2),transform 1.7s var(--feder);transition-delay:calc(var(--i,0)*110ms)}
.blatt-p.an.da .steig{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){[data-a="feder"],.blatt-p .steig,.js [data-a="feder"] .zb img,.js .gabe[data-a="feder"] .gabe__b{opacity:1!important;transform:none!important;transition:none!important}}
/* ---------- Genauer nachlesen: Fenster über der Seite ---------- */
dialog.genau{border:0;padding:0;margin:auto;width:min(860px,calc(100vw - 32px));max-height:calc(100vh - 48px);border-radius:clamp(20px,2.2vw,30px);background:var(--papier);color:var(--tinte);box-shadow:0 60px 120px -40px #000}
dialog.genau::backdrop{background:rgba(6,14,30,.78);backdrop-filter:none}
.genau__in{padding:clamp(24px,3vw,44px)}
.genau__kopf{display:flex;align-items:flex-start;gap:16px;justify-content:space-between;margin-bottom:clamp(18px,2vw,28px);padding-bottom:16px;border-bottom:1px solid rgba(11,42,76,.16)}
.genau__kopf small{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--taupe);margin-bottom:8px}
.genau__kopf h4{font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2vw,2rem);line-height:1.16;margin:0}
.genau__zu{flex:none;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;color:#fff;background:linear-gradient(180deg,#1E68AE,#115595 50%,#0C3F72);box-shadow:inset 0 1px 0 rgba(255,255,255,.24),inset 0 -2px 0 rgba(0,0,0,.45);cursor:pointer}
.genau__zu svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.5}
.genau__t p{font-size:1.02rem;line-height:1.68;color:rgba(11,42,76,.92)}
.genau__t p+p{margin-top:.9em}
.genau__t b.lead{font-weight:400;color:var(--tinte);font-family:var(--serif);font-size:1.12em}
.genau__t .warum{margin-top:clamp(18px,2vw,26px);padding:18px 20px;border-radius:16px;background:var(--kuhle-h);box-shadow:var(--kuhle-h-s)}
.genau__t a{color:inherit;text-decoration:underline;text-decoration-color:rgba(201,138,90,.6);text-underline-offset:3px;overflow-wrap:anywhere}

/* ---------- Lesbarkeit: Lauftext kräftiger, Fuss heller ---------- */
.fl--papier .lauf,.fl--creme .lauf{color:rgba(11,42,76,.9)}
.lauf{color:rgba(255,255,255,.9)}
.fl--papier .lauf,.fl--creme .lauf,.lauf{font-size:clamp(1.1rem,1.26vw,1.28rem);line-height:1.7}
.fuss{color:rgba(255,255,255,.84)}
.fuss p{color:rgba(255,255,255,.8);max-width:62ch}
.fuss .r a{color:#fff}
/* ---------- Knöpfe mittig, Blatt-Inhalt an Kante oder Mitte ---------- */
.pb__k h3{margin-inline:auto;text-align:center;max-width:26ch}
.pb__kurz{margin-inline:auto;text-align:center;max-width:66ch}
.pb__nach{text-align:center}
.pb__nach p{margin-inline:auto}
.pb__ziele{justify-content:center}
.pb__f{justify-content:center}
.pb__f .kn-reihe{justify-content:center}
.pb__text{text-align:center}
.pb__text p,.pb__text li{margin-inline:auto;text-align:left}
.pb__text h3{text-align:center}
.pb__text ul{max-width:72ch;margin-inline:auto}
.auftakt .kn-reihe,.schluss .kn-reihe{justify-content:center}
.brief .gastgeber{margin-inline:auto}
/* ---------- Schluss ---------- */
.schluss .in{text-align:center}
.schluss .lauf{margin-inline:auto}
.schluss .gruss-u{justify-content:center}
.schluss .kap--z~.zt{font-size:clamp(2rem,4.6vw,5rem)}
.schluss .kap--z span{color:rgba(255,255,255,.86);text-shadow:0 1px 2px rgba(3,10,16,.9)}
.schluss .kap--z{position:relative;z-index:1}
.schluss .gruss-u__b{box-shadow:0 0 0 2px var(--gold),0 18px 30px -16px rgba(0,0,0,.8)}
.schluss__d{position:fixed;inset:0;background:linear-gradient(180deg,rgba(11,42,76,.3),rgba(11,42,76,.62))}
@media(max-width:900px){.schluss__d{position:absolute}}
.fuss .siegel{display:flex;align-items:center;gap:14px;margin-bottom:18px;color:var(--gold)}
.fuss .siegel svg{height:22px;width:auto;fill:currentColor}
.fuss .siegel b{margin:0;font-size:1.1rem;color:#fff}

/* ================= Fassung 4b (Robert 15.10.2026 abends): Bilder stehen immer, Buchstaben steigen, Miniaturen, Abschnitte im Wechsel ================= */
/* Bilder: nie versteckt bis zum Ladeereignis (Safari meldete es nicht, Fotos blieben leer); das kleine Vorschaubild liegt dahinter */
.js img.ld:not(.da),img.ld{opacity:1}
.js img.ld.da{animation:none}
/* Ohne Skript steht alles da */
:root:not(.js) :is([data-a],.steig,.wfen__z,.wfen__t span,.wfen__k,.z>span,.kap[data-a] i,.hk){opacity:1!important;transform:none!important}
:root:not(.js) .blatt-p.an .steig{opacity:1!important;transform:none!important}
/* Buchstaben steigen einzeln aus der Zeile, federnd, gestaffelt (Markenbuch Carlton) */
.wo{display:inline-block;white-space:nowrap}
.js .zt.bst .z>span{transform:none!important;transition:none}
.js .zt.bst .bu{display:inline-block;opacity:0;transform:translate3d(0,.95em,0) rotate(5deg);transform-origin:0 100%;transition:opacity .7s var(--e2),transform 1.35s var(--feder);transition-delay:calc(var(--k)*24ms + 60ms)}
.js .zt.bst.da .bu{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .zt.bst .bu{opacity:1;transform:none;transition:none}}
/* Zeichen über den Köpfen dreht und federt herein */
.js .kap--z[data-a] .kap__z{transform:scale(.62) rotate(-14deg);opacity:0;transition:opacity 1.1s var(--e2),transform 2.1s var(--feder)}
.js .kap--z[data-a].da .kap__z{transform:none;opacity:1}
/* Bilder: Hochschweben mit Feder und Zoom im Rahmen auch für die Werte im Brief und die Zahlenkarten */
.js .werte [data-a="feder"] .zb img,.js .brief__haus[data-a="feder"] img{transform:scale(1.14);transition:transform 2.6s var(--e1)}
.js .werte [data-a="feder"].da .zb img,.js .brief__haus[data-a="feder"].da img{transform:none}
/* Miniatur im Band jedes zweiten Punktes */
.pb__band--mini{grid-template-columns:auto 1px minmax(0,1fr) auto}
.pb__mini{display:block;width:clamp(120px,11vw,176px);aspect-ratio:4/3;border-radius:14px;overflow:hidden;background:var(--tief);box-shadow:0 0 0 5px #fff,0 0 0 6px rgba(11,42,76,.12),0 22px 30px -16px rgba(11,42,76,.55);transform:rotate(2.5deg);margin:6px 6px 6px 0}
.pb__mini img{display:block;width:100%;height:100%;object-fit:cover;transform:scale(1.2);transition:transform 2.4s var(--e1) .25s}
.blatt-p.an.da .pb__mini img{transform:none}
.fl--navy .pb__mini,.fl--nacht .pb__mini{box-shadow:0 0 0 5px #F6E6D6,0 22px 30px -16px rgba(0,0,0,.7)}
@media(max-width:700px){.pb__band--mini{grid-template-columns:1fr}.pb__mini{width:58%;justify-self:start;margin-top:4px}}
/* Abschnitte im Wechsel: Kopf mittig, Kopf neben dem Foto (links oder rechts), Foto zuerst und Kopf darunter */
.kap--links{align-items:flex-start;text-align:left}
.kseite{display:grid;gap:clamp(30px,4.6vw,84px);align-items:center;margin-bottom:clamp(40px,5vw,80px)}
@media(min-width:1000px){.kseite{grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr)}.kseite--r{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)}.kseite--r .kseite__t{order:2}}
.kseite .kf{margin-bottom:0}
.kf--hoch .kf__b{aspect-ratio:4/3}
.kseite .kap--z~.zt,.kbild .kap--z~.zt{text-align:left;font-size:clamp(2.2rem,4.4vw,4.8rem)}
.kseite .zt .z>span,.kbild .zt .z>span{margin-inline:0}
.kseite .lauf,.kbild .lauf{margin-top:clamp(18px,2vw,30px);max-width:52ch}
.kbild{display:grid;gap:clamp(20px,3vw,60px);align-items:end;margin-bottom:clamp(40px,5vw,72px)}
@media(min-width:1000px){.kbild{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}.kbild .lauf{margin-top:0;padding-bottom:.4em}}
/* Übergang zum nächsten Bereich: leise Zeile, kein Knopf */
.uebergang{display:flex;align-items:center;justify-content:center;gap:16px;margin:clamp(40px,5vw,72px) auto 0;width:fit-content;max-width:100%;padding:12px 10px 12px 26px;border-radius:999px;color:var(--tinte);text-decoration:none;box-shadow:inset 0 0 0 1px rgba(11,42,76,.14);transition:transform .5s var(--e2)}
.uebergang:hover{transform:translateY(-2px)}
.uebergang span{font-family:var(--mono);font-size:12px;letter-spacing:.17em;text-transform:uppercase;color:var(--messing)}
.uebergang b{font-family:var(--serif);font-weight:500;font-size:clamp(1.1rem,1.4vw,1.35rem)}
.fl--navy .uebergang,.fl--nacht .uebergang{color:#fff;box-shadow:inset 0 0 0 1px rgba(201,138,90,.4)}
.fl--navy .uebergang span,.fl--nacht .uebergang span{color:var(--gold)}

/* ein Punkt ohne Gastszene: die eine Kuhle mittig, keine halbe leere Fläche */
@media(min-width:900px){.pb__zwei--eins{grid-template-columns:minmax(0,1fr);max-width:780px;margin-inline:auto}}
.pult__zahl b{white-space:nowrap}
@media(max-width:700px){.pult__zahl{flex-direction:column;align-items:center;gap:2px;text-align:center}}

/* ================= Fassung 5 (Robert 16.10.2026): Bilder auf den Blättern, mehr Farbe und Glanz, Zahl kleiner, Überblick ohne Leere, «Zuerst» und Bereiche grösser ================= */
/* Band jedes Punktes: Foto links, Nacht mit Tapete rechts, Zahl in Gold, Glanzkante */
.pb__band{position:relative;overflow:hidden;display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);gap:0;padding:0;border-radius:clamp(18px,1.8vw,24px);
  background:#0B2A4C var(--muster) 50% 0/420px auto;box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 0 0 1px rgba(201,138,90,.38),0 30px 44px -30px rgba(11,42,76,.6);color:#fff}
.pb__band--mini{grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr) auto;align-items:center}
.pb__foto{position:relative;display:block;min-height:clamp(210px,18vw,280px);overflow:hidden;background:var(--tief)}
.pb__foto img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.14);transition:transform 2.4s var(--e1) .1s}
.blatt-p.an.da .pb__foto img{transform:none}
.pb__inhalt{position:relative;display:flex;flex-direction:column;justify-content:center;gap:10px;padding:clamp(22px,2.6vw,38px) clamp(22px,2.8vw,44px);overflow:hidden}
.pb__inhalt::after{content:'';position:absolute;top:-20%;bottom:-20%;left:0;width:30%;background:linear-gradient(100deg,transparent,rgba(246,230,214,.2) 50%,transparent);transform:translate3d(-170%,0,0) skewX(-16deg);pointer-events:none}
.blatt-p.an.da .pb__inhalt::after{transform:translate3d(460%,0,0) skewX(-16deg);transition:transform 1.9s var(--e1) 2.7s}
.pb__band .pb__nr,.fl--navy .pb__band .pb__nr{margin:0;color:var(--gold)}
.pb__band .pb__z,.fl--navy .pb__band .pb__z,.fl--nacht .pb__band .pb__z{font-size:clamp(40px,4vw,62px);line-height:1;font-weight:500;color:#E2B48C;letter-spacing:-.01em}
.pb__band .pb__z.s3,.pb__band .pb__z.s4{font-size:clamp(34px,3.3vw,52px)}
.pb__linie{display:block;width:52px;height:1px;background:linear-gradient(90deg,var(--gold),rgba(201,138,90,0))}
.pb__band .pb__satz,.fl--navy .pb__band .pb__satz{color:rgba(255,255,255,.94)}
.pb__band .pb__mini{margin:0 clamp(18px,2vw,28px) 0 0}
/* auf dunklen Bereichen ist das Band hell (Sandstein), damit sich hell und dunkel abwechseln */
.fl--navy .pb__band,.fl--nacht .pb__band{background:linear-gradient(135deg,#F7F5F0,#E7E2D9 70%,#E3D3C2);box-shadow:inset 0 1px 0 #fff,inset 0 0 0 1px rgba(168,96,60,.35),0 30px 44px -30px rgba(0,0,0,.7);color:var(--tinte)}
.fl--navy .pb__band .pb__z,.fl--nacht .pb__band .pb__z{color:var(--nacht)}
.fl--navy .pb__band .pb__nr,.fl--nacht .pb__band .pb__nr{color:var(--messing)}
.fl--navy .pb__band .pb__satz,.fl--nacht .pb__band .pb__satz{color:var(--tinte)}
.fl--navy .pb__inhalt::after,.fl--nacht .pb__inhalt::after{background:linear-gradient(100deg,transparent,rgba(255,255,255,.55) 50%,transparent)}
@media(max-width:700px){.pb__band,.pb__band--mini{grid-template-columns:1fr}.pb__foto{min-height:0;aspect-ratio:16/10}.pb__band .pb__mini{display:none}}
/* «Was wir tun würden» in der Gegenfarbe: dunkel auf hellen Bereichen, hell auf dunklen */
.pb__zwei .kuhle.kuhle--tun{background:linear-gradient(180deg,#115595,#0C3F72 60%,#0B2A4C);box-shadow:inset 0 1px 0 rgba(255,255,255,.14),inset 0 0 0 1px rgba(201,138,90,.3),0 24px 34px -24px rgba(11,42,76,.6);color:rgba(255,255,255,.9)}
.pb__zwei .kuhle--tun .pb__ko{color:#fff}
.pb__zwei .kuhle--tun .pb__ko i svg{stroke:var(--gold)}
.fl--navy .pb__zwei .kuhle.kuhle--tun,.fl--nacht .pb__zwei .kuhle.kuhle--tun{background:linear-gradient(180deg,#F7F5F0,#E7E2D9);box-shadow:inset 0 1px 0 #fff,inset 0 0 0 1px rgba(168,96,60,.3);color:rgba(11,42,76,.9)}
.fl--navy .pb__zwei .kuhle--tun .pb__ko,.fl--nacht .pb__zwei .kuhle--tun .pb__ko{color:var(--tinte)}

/* Überblick: links unter «So lesen Sie» ein Foto, das bis zur Höhe der rechten Platte reicht */
.blick__u{align-items:stretch}
.blick__l{display:flex;flex-direction:column;gap:clamp(14px,1.8vw,24px)}
.blick__foto{flex:1;display:flex;padding:9px;min-height:clamp(260px,24vw,380px)}
.blick__foto .kf__b{position:relative;flex:1;display:block;border-radius:clamp(14px,1.5vw,20px);overflow:hidden;background:var(--tief)}
.blick__foto .kf__b img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.blick__foto .kerbe{--f:#115595;color:var(--gold);font-size:1.25rem}

/* Was zuerst zählt: ein grosses Blatt links, vier daneben; je Punkt sein Foto mit Nummer in der Kerbe */
.zuerst{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr) minmax(0,1fr);gap:clamp(14px,1.6vw,22px)}
.zk{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:9px;padding:9px}
.zk:first-child{grid-row:span 2;grid-template-columns:1fr;grid-template-rows:1fr auto}
.zk__b{position:relative;display:block;border-radius:clamp(13px,1.3vw,18px);overflow:hidden;min-height:clamp(170px,14vw,220px);background:var(--tief)}
.zk:first-child .zk__b{min-height:clamp(300px,26vw,420px)}
.zk__b img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.zk__b .kerbe{font-size:clamp(1.1rem,1.3vw,1.4rem);padding:8px 14px 5px 12px}
.zk .kuhle{display:flex;flex-direction:column;gap:8px;padding:18px 18px 12px}
.zk__z{font-size:clamp(1.9rem,2.4vw,2.6rem)}
.zk:first-child .zk__z{font-size:clamp(2.6rem,3.6vw,3.8rem)}
.zk__s{font-size:.92rem}
.zk__t{padding-top:10px;font-size:1rem}
.zk:first-child .zk__t{font-size:1.2rem}
.zk__f{margin-top:auto;padding:8px 0 0}
@media(max-width:1100px){.zuerst{grid-template-columns:repeat(2,minmax(0,1fr))}.zk:first-child{grid-column:1/-1;grid-row:auto;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);grid-template-rows:auto}.zk{grid-template-columns:1fr}.zk__b{aspect-ratio:16/10;min-height:0}}
@media(max-width:700px){.zuerst{grid-template-columns:1fr}.zk:first-child{grid-template-columns:1fr}.zk:first-child .zk__b{min-height:0;aspect-ratio:16/10}}

/* Zehn Bereiche grösser: zwei grosse, drei kleinere, im Wechsel */
.bereiche10{grid-template-columns:repeat(6,minmax(0,1fr));gap:clamp(14px,1.6vw,24px)}
.bk10:nth-child(5n+1),.bk10:nth-child(5n+2){grid-column:span 3}
.bk10:nth-child(5n+3),.bk10:nth-child(5n+4),.bk10:nth-child(5n+5){grid-column:span 2}
.bk10__b{aspect-ratio:4/3}
.bk10:nth-child(5n+1) .bk10__b,.bk10:nth-child(5n+2) .bk10__b{aspect-ratio:16/10}
.bk10__n{padding:16px 8px 8px 12px}
.bk10__n b{font-size:clamp(1.15rem,1.4vw,1.5rem)}
.bereiche10 .kerbe{font-size:clamp(1.6rem,2vw,2.2rem)}
.bk10 .knauf{width:38px;height:38px}
@media(max-width:1100px){.bereiche10{grid-template-columns:repeat(2,minmax(0,1fr))}.bk10:nth-child(n){grid-column:auto}.bk10:nth-child(1),.bk10:nth-child(10){grid-column:1/-1}.bk10__b,.bk10:nth-child(n) .bk10__b{aspect-ratio:4/3}.bk10:nth-child(1) .bk10__b,.bk10:nth-child(10) .bk10__b{aspect-ratio:16/10}}
@media(max-width:560px){.bk10__n b{font-size:1rem}.bk10 .knauf{width:30px;height:30px}}

.blick__u .blick__foto{padding:9px}
/* kleine «Zuerst»-Karten: Foto oben, Text darunter, damit nichts gequetscht wird */
@media(min-width:1101px){.zk:not(:first-child){grid-template-columns:1fr;grid-template-rows:auto 1fr}.zk:not(:first-child) .zk__b{min-height:0;aspect-ratio:16/8}.zk:not(:first-child) .zk__s{display:none}.zk:not(:first-child) .zk__t{padding-top:6px;border-top:0}}

/* ================= Fassung 6 (Robert 16.10.2026: «zu lang, zu gross, zu unübersichtlich … die Informationen in den Fokus»): Vorspann ein Drittel, Bereiche kompakt, alles auf die Punkte ================= */
.f6 .kopfzeile--mitte{margin-bottom:clamp(28px,3.4vw,52px)}
.f6.fl{padding-top:clamp(56px,6.6vw,104px)}
.f6.blatt{padding-bottom:calc(clamp(56px,6.6vw,104px) + var(--rund))}
/* Guten Tag: Text und Gastgeber links, Zahlen und Lesehilfe rechts */
.brief6{display:grid;gap:clamp(18px,2.4vw,36px);align-items:start}
@media(min-width:1000px){.brief6{grid-template-columns:minmax(0,1fr) minmax(0,.92fr)}}
.brief6 .gastgeber{margin-top:clamp(18px,2vw,28px)}
.brief6__r{padding:clamp(18px,2.2vw,30px)}
.zahlen4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:clamp(16px,1.8vw,24px)}
.z4{display:flex;flex-direction:column;gap:2px;padding:16px 18px 14px}
.z4 b{font-family:var(--serif);font-weight:500;font-size:clamp(1.9rem,2.5vw,2.7rem);line-height:1;color:var(--nacht);letter-spacing:-.01em}
.z4 span{margin-top:6px;font-family:var(--serif);font-size:1.02rem;color:var(--tinte)}
.z4 small{font-size:.86rem;line-height:1.4;color:rgba(11,42,76,.72)}
.brief6__r h3{font-family:var(--serif);font-weight:400;font-size:clamp(1.3rem,1.6vw,1.6rem);line-height:1.16;margin:0 0 8px}
.brief6__r>p{font-size:.98rem;line-height:1.62;color:rgba(11,42,76,.9)}
.brief6 details.methode{background:var(--kuhle-h);box-shadow:var(--kuhle-h-s);color:rgba(11,42,76,.9);margin-top:12px}
.brief6 details.methode summary{color:var(--messing)}
@media(max-width:520px){.zahlen4{grid-template-columns:1fr 1fr;gap:8px}.z4{padding:12px 12px 10px}.z4 b{font-size:1.7rem}}
/* Register: Was zuerst zählt (fünf Zeilen) und Zehn Bereiche (zwei Spalten), je Zeile ein kleines Foto, Zahl, Titel, Knauf */
.reg{display:grid;gap:clamp(14px,1.8vw,24px);align-items:stretch}
@media(min-width:1000px){.reg{grid-template-columns:minmax(0,1fr) minmax(0,1.15fr)}}
.reg__p{padding:clamp(14px,1.6vw,22px)}
.reg__p .pb__ko--mitte{margin-bottom:12px}
.reg__p .pb__ko--mitte svg{width:24px}
.reg__l{display:grid;gap:8px}
@media(min-width:1000px){.reg__l--zwei{grid-template-columns:1fr 1fr}}
.reg__z{display:grid;grid-template-columns:auto auto minmax(0,1fr) auto;align-items:center;gap:12px;padding:8px 10px 8px 8px;text-decoration:none;color:var(--tinte);transition:transform .5s var(--e2)}
.reg__z:hover{transform:translateY(-2px)}
.reg__z .reg__b{position:relative;display:block;width:clamp(56px,5vw,72px);aspect-ratio:1;border-radius:11px;overflow:hidden;background:var(--tief);box-shadow:0 0 0 3px #fff,0 0 0 4px rgba(11,42,76,.12)}
.reg__z .reg__b img{width:100%;height:100%;object-fit:cover}
.reg__nr{font-family:var(--mono);font-size:11px;letter-spacing:.14em;color:rgba(11,42,76,.72);min-width:2.6em}
.reg__k{font-family:var(--serif);font-weight:500;font-size:clamp(1.3rem,1.6vw,1.7rem);line-height:1;color:var(--nacht);white-space:nowrap;min-width:3.2em;letter-spacing:-.01em}
.reg__k.s3,.reg__k.s4{font-size:clamp(1.05rem,1.25vw,1.3rem)}
.reg__t{display:block;font-family:var(--serif);font-size:1.02rem;line-height:1.22}
.reg__t small{display:block;margin-top:3px;font-family:var(--sans);font-size:.82rem;line-height:1.35;color:rgba(11,42,76,.74)}
.reg__z .knauf{width:32px;height:32px}
.reg__z:hover .knauf{transform:translate(2px,-2px)}
.reg__z--k{grid-template-columns:auto auto auto minmax(0,1fr) auto}
@media(max-width:700px){.reg__z{gap:10px}.reg__z--k{grid-template-columns:auto auto minmax(0,1fr) auto}.reg__z--k .reg__nr{display:none}.reg__z--k .reg__b{width:46px}.reg__k{min-width:0;font-size:1.1rem}.reg__t{font-size:.98rem}.reg__t small{display:none}.reg__l--zwei .reg__t small{display:block}}
/* Bereiche: kompakter Kopf, weniger Luft, kein grosses Foto */
section.bereich.fl{padding-top:clamp(48px,5.6vw,84px)}
section.bereich.blatt{padding-bottom:calc(clamp(44px,5.2vw,76px) + var(--rund))}
.kkopf{display:grid;gap:clamp(14px,2.4vw,48px);align-items:end;margin-bottom:clamp(16px,2vw,28px)}
@media(min-width:1000px){.kkopf{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)}}
.kkopf .kap--z{margin-bottom:clamp(10px,1.2vw,18px)}
.kkopf .kap__z{width:clamp(44px,4.6vw,64px)}
.kkopf .kap--z~.zt{text-align:left;font-size:clamp(1.9rem,3.4vw,3.6rem);line-height:1.04}
.kkopf .zt .z>span{margin-inline:0}
.kkopf .lauf{margin:0;max-width:none;padding-bottom:.35em;font-size:clamp(1rem,1.1vw,1.12rem);line-height:1.6}
.pult{margin-bottom:clamp(12px,1.4vw,18px)}
.pult__sep{display:block;align-self:center;width:1px;height:34px;margin:0 4px;background:rgba(11,42,76,.2)}
.fl--navy .pult__sep,.fl--nacht .pult__sep{background:rgba(201,138,90,.4)}
.pult__reihe .pult__x b{letter-spacing:.06em;font-size:10.5px}
/* Blatt: Band flacher, Texte enger, Knopf dichter */
.pb__foto{min-height:clamp(160px,13vw,200px)}
.pb__inhalt{gap:8px;padding:clamp(18px,2vw,28px) clamp(20px,2.4vw,36px)}
.pb__band .pb__z,.fl--navy .pb__band .pb__z,.fl--nacht .pb__band .pb__z{font-size:clamp(34px,3.3vw,50px)}
.pb__band .pb__z.s3,.pb__band .pb__z.s4{font-size:clamp(28px,2.7vw,40px)}
.pb__band .pb__satz,.fl--navy .pb__band .pb__satz{font-size:clamp(1rem,1.25vw,1.22rem);line-height:1.34}
.pb__k{padding:clamp(18px,2.2vw,30px) clamp(14px,2vw,28px) clamp(8px,1.2vw,14px)}
.pb__k h3{font-size:clamp(1.35rem,1.9vw,1.9rem)}
.pb__kurz{margin-top:12px;font-size:clamp(1rem,1.1vw,1.1rem);line-height:1.6}
.pb__zwei{margin-top:clamp(14px,1.8vw,24px);gap:12px}
.pb__zwei .kuhle{padding:16px 18px 14px;font-size:.95rem;line-height:1.56}
.pb__nach{margin-top:14px;padding-top:12px}
.pb__nach p{font-size:.94rem;line-height:1.55}
.pb__ziele{margin-top:10px}
.pb__f{margin-top:12px}
.blatt-x .pb__text{padding:clamp(18px,2.2vw,30px) clamp(16px,2.2vw,32px) clamp(16px,2vw,26px)}
.blatt-x .pb__text p,.blatt-x .pb__text li{font-size:.98rem;line-height:1.6}
.uebergang{margin-top:clamp(24px,2.8vw,40px)}
/* Schluss: Was offen bleibt als helle Platte, zwei Spalten */
.schluss__offen{margin:clamp(22px,2.6vw,36px) auto 0;max-width:1100px;padding:clamp(18px,2.2vw,30px);text-align:left}
.schluss__offen .pb__ko--mitte{margin-bottom:8px}
.schluss__os{text-align:center;font-size:.95rem;line-height:1.55;color:rgba(11,42,76,.82);max-width:62ch;margin:0 auto}
.schluss__offen .luecken{margin-top:14px;gap:8px}
@media(min-width:900px){.schluss__offen .luecken{grid-template-columns:1fr 1fr}}
.schluss__offen .luecken li{background:var(--kuhle-h);box-shadow:var(--kuhle-h-s);color:rgba(11,42,76,.9);font-size:.92rem;padding:10px 14px 10px 36px}
.schluss__offen .luecken li::before{left:15px;top:16px}
.schluss__offen .luecken li small{color:var(--rot)}
.schluss .gruss-u{margin-top:clamp(22px,2.6vw,36px)}

/* ================= Fassung 7 (Robert 16.10.2026: «mit Bildern arbeiten wie beim Carlton, mit dem jetzigen Design»): Beweis rechts neben dem Text, Handy mit echter Aufnahme, roter Kreis, Rechner-Fenster, PDF-Streifen ================= */
.pb__k--bw{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(16px,2vw,32px);align-items:start}
@media(min-width:1000px){.pb__k--bw{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)}.pb__k--bw .pb__zwei{grid-template-columns:1fr}.pb__k--bw .pb__zwei--eins{max-width:none}}
.pb__links{min-width:0}
.pb__bew{display:flex;flex-wrap:wrap;justify-content:center;align-items:flex-start;gap:clamp(12px,1.4vw,20px);width:100%}
@media(min-width:1000px){.pb__bew{flex-wrap:nowrap;position:sticky;top:96px}}
.bw{margin:0;text-align:center;flex:0 1 auto;min-width:0}
.bw--tel{width:clamp(200px,62vw,280px)}
@media(min-width:1000px){.pb__bew--2 .bw--tel{width:min(48%,290px);flex:0 0 auto}.pb__bew--1 .bw--tel{width:min(70%,310px)}}
.bw--fen,.bw--dok{width:min(100%,520px)}

.bw--fen,.bw--dok{flex:1 1 0}.pb__bew--1 .bw--fen,.pb__bew--1 .bw--dok{flex:0 1 100%}
.bw figcaption{margin-top:10px;display:grid;gap:4px;justify-items:center}
.bw figcaption strong{font:400 1.02rem/1.25 var(--serif);color:var(--tinte)}
.bw figcaption span{font-size:.86rem;line-height:1.4;color:rgba(11,42,76,.8);max-width:30ch}
.fl--navy .bw figcaption strong,.fl--nacht .bw figcaption strong{color:#fff}
.fl--navy .bw figcaption span,.fl--nacht .bw figcaption span{color:rgba(255,255,255,.8)}
.bw figcaption .kn{margin-top:6px}
/* Handy: Rahmen aus Blender (Carlton), Bildschirm ausgespart, Aufnahme darunter */
.tel{position:relative;aspect-ratio:1400/2600;width:100%;margin:0 auto}
.tel__rahmen{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;-webkit-mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent),linear-gradient(0deg,transparent,#000 4%,#000 96%,transparent);-webkit-mask-composite:source-in;mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent),linear-gradient(0deg,transparent,#000 4%,#000 96%,transparent);mask-composite:intersect}
.tel__schirm{position:absolute;z-index:1;left:17.07%;top:11.62%;width:65.5%;height:76.69%;border-radius:12.6%/5.8%;overflow:hidden;background:#111;isolation:isolate}
.tel__schirm img{display:block;width:100%;height:100%;object-fit:cover}
.tel__insel{position:absolute;z-index:2;left:39.64%;top:12.88%;width:20.71%;height:2.9%;border-radius:999px;background:#050505}
.kreis{position:absolute;z-index:2;border:3px solid var(--rot);border-radius:50%;rotate:-2deg;box-shadow:0 0 0 1px rgba(255,255,255,.45);transform:scale(.6);opacity:0;transition:transform 1.2s var(--feder) .9s,opacity .5s var(--e2) .9s}
.kreis--eck{border-radius:12px;rotate:0deg}
.blatt-p.an.da .kreis,:root:not(.js) .kreis{transform:none;opacity:1}
/* Rechner-Fenster und Dokument */
.fenster{border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 18px 38px -18px rgba(11,42,76,.55),0 0 0 1px rgba(11,42,76,.14)}
.fenster__kopf{display:flex;align-items:center;gap:6px;height:28px;padding:0 12px;background:linear-gradient(#F1EFEA,#DDD6CA)}
.fenster__kopf i{width:9px;height:9px;border-radius:50%;background:#BBAE9C}
.fenster__kopf span{margin-left:8px;font-family:var(--mono);font-size:11px;letter-spacing:.02em;color:#4A3A2C;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fenster__b{position:relative}
.fenster__b img{display:block;width:100%;height:auto}
@media(max-width:700px){.bw figcaption span{max-width:none}}

/* ================= Fassung 7, mallorquinisch (Robert 16.10.2026: «diesen mallorquinischen Flair … dieses mallorquinische Lebensgefühl»): Sandstein am Tag, Windrose für Sa Clastra, Laufzeile mit den Worten des Hauses, Galatzó im Gruss ================= */
.kap__z--wind{width:clamp(40px,4vw,56px)!important;height:auto}
.b6__foto{position:relative;display:block;aspect-ratio:21/8;border-radius:clamp(14px,1.5vw,20px);overflow:hidden;margin-bottom:clamp(12px,1.4vw,18px);background:var(--tief)}
.b6__foto img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%}
.b6__foto .kerbe{--f:#FBFAF7;font-size:clamp(1rem,1.2vw,1.2rem);padding:8px 14px 5px 12px}
.laufzeile{position:relative;overflow:hidden;background:var(--nacht);color:var(--gold);padding:clamp(18px,2vw,26px) 0 calc(clamp(18px,2vw,26px) + var(--rund));margin-top:calc(var(--rund)*-1);border-radius:var(--rund) var(--rund) 0 0}
.lz__band{display:flex;width:max-content;animation:lzLauf 70s linear infinite}
.laufzeile.steht .lz__band{animation-play-state:paused}
.lz__satz{display:flex;align-items:center;gap:clamp(18px,2vw,30px);padding-right:clamp(18px,2vw,30px)}
.lz__satz span{font-family:var(--serif);font-size:clamp(1.3rem,2vw,2rem);line-height:1;white-space:nowrap;color:#F6E6D6}
.lz__z{width:clamp(18px,1.6vw,24px);height:auto;flex:none;fill:currentColor;opacity:.85}
@keyframes lzLauf{from{transform:translate3d(0,0,0)}to{transform:translate3d(-50%,0,0)}}
@media (prefers-reduced-motion:reduce){.lz__band{animation:none}}

@media(max-width:999px){.bw--fen,.bw--dok{flex:0 0 100%;width:100%}.pb__bew{margin-top:6px}}

@media(max-width:999px){.pb__bew--2{gap:10px}.pb__bew--2 .bw--tel{width:calc(50% - 5px);flex:0 0 calc(50% - 5px)}.pb__bew--2 .bw--tel figcaption strong{font-size:.92rem}.pb__bew--2 .bw--tel figcaption span{font-size:.8rem}.pb__bew--2 .bw--tel .kn{font-size:9.5px;padding-inline:10px}}

@media(max-width:999px){.pb__bew--2 .bw--tel .bw__l{display:none}}

/* ================= Hotel Monte-Moro, eigene Teile dieser Analyse (17.10.2026) ================= */
/* Auftakt im Massstab der Hauptseite (Master 1b Nr. 9): Haus in voller Farbe, Zeichen in Lärche, Name gross in Versalien, Ortszeile, ein ruhiger Satz, feine Zahlenzeile, Platte mit Knopf. Das Dunkel liegt im Bild selbst. */
.hero3{position:relative;min-height:100svh;display:flex;align-items:flex-end;padding:clamp(110px,14vh,170px) var(--rand) calc(clamp(30px,5vh,60px) + var(--rund));background:var(--nacht);color:#fff;overflow:clip}
.hero3__bild{position:absolute;inset:0;z-index:0;width:100%;height:100%;object-fit:cover;object-position:50% 40%}
.hero3__in{position:relative;z-index:1;width:100%;display:flex;flex-direction:column;align-items:center;text-align:center}
.hero3__z svg{width:clamp(110px,12vw,180px);height:auto;color:var(--gold);fill:currentColor;filter:drop-shadow(0 2px 6px rgba(3,10,16,.5))}
.hero3__ort{display:flex;align-items:center;gap:16px;margin-top:clamp(14px,1.8vw,24px);font-family:var(--mono);font-size:12.5px;letter-spacing:.32em;text-transform:uppercase;color:rgba(255,255,255,.95);text-shadow:0 1px 2px rgba(3,10,16,.95),0 2px 12px rgba(3,10,16,.7)}
.hero3__ort i{width:clamp(24px,3.4vw,56px);height:1px;background:currentColor;opacity:.7}
.hero3__ort--gold{color:#F6E6D6;letter-spacing:.4em}
.hero3__ort--gold i{background:var(--gold);opacity:1}
.hero3__t{margin:clamp(10px,1.4vw,20px) 0 0;font-family:var(--serif);font-weight:400;font-size:clamp(2.6rem,6.4vw,7.2rem);line-height:.98;letter-spacing:.03em;text-transform:uppercase;color:#fff;text-shadow:0 .03em .1em rgba(3,10,16,.55)}
.hero3__t span{white-space:nowrap}
@media(max-width:760px){.hero3__t span{display:block}}
.hero3__satz{max-width:46ch;margin:clamp(18px,2.2vw,30px) auto 0;font-size:clamp(1.06rem,1.3vw,1.3rem);line-height:1.6;color:rgba(255,255,255,.94);text-shadow:0 1px 3px rgba(3,10,16,.85)}
.hero3__p{margin-top:clamp(24px,3vw,40px);padding:12px 12px 12px clamp(18px,2vw,28px);display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:14px 28px}
.hero3__zahlen{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 22px;margin:0;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:rgba(11,42,76,.78)}
.hero3__zahlen b{font-family:var(--serif);font-weight:400;font-size:1.25rem;letter-spacing:0;color:var(--tinte);margin-right:4px}
.hero3+.fl{border-radius:var(--rund) var(--rund) 0 0;margin-top:calc(var(--rund)*-1);position:relative;z-index:2}
@media(max-width:600px){.hero3__ort{letter-spacing:.18em;font-size:11px;gap:10px}.hero3__ort--gold{letter-spacing:.22em}.hero3__p{border-radius:22px}}
/* Was das für Sie bedeutet: schmale Karten, Kontrast zum Grund (Master 1b Nr. 5 «was gehalten hat») */
.pb__ko--bed{margin-top:clamp(18px,2vw,26px);margin-bottom:10px}
.pb__ko--bed svg{width:26px}
.bed{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));margin-bottom:clamp(14px,1.6vw,20px)}
.bed__k{border-radius:16px;padding:14px 16px 15px;background:linear-gradient(180deg,#1E68AE,#115595 55%,#0C3F72);color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 14px 22px -16px rgba(11,42,76,.7)}
.bed__k p{margin:0;font-size:.95rem;line-height:1.55;color:rgba(255,255,255,.92)}
.bed__ko{display:flex;align-items:center;gap:10px;margin-bottom:8px!important;font-family:var(--mono);font-size:11.5px!important;letter-spacing:.16em;text-transform:uppercase;color:#F6E6D6!important}
.bed__ko i{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.14);flex:none}
.bed__ko svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.fl--navy .bed__k{background:linear-gradient(180deg,#FFFFFF,#F1EFEA 60%,#E3DCD0);color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 14px 22px -16px rgba(0,0,0,.6)}
.fl--navy .bed__k p{color:rgba(11,42,76,.92)}
.fl--navy .bed__ko{color:var(--messing)!important}
.fl--navy .bed__ko i{background:rgba(11,42,76,.08)}
.kuhle--tun{padding:16px 18px 15px;font-size:.98rem;line-height:1.6}
/* Kreise stehen sofort mit dem Bild (Master 1b Nr. 3), ohne Warten */
.kreis{opacity:1!important;transform:none!important;transition:none!important}
/* Wer hinter der heutigen Seite steht: ein ruhiger Teil */
.ag__raster{display:grid;gap:clamp(16px,2vw,26px)}
.ag__p{padding:clamp(20px,2.6vw,36px);display:grid;gap:clamp(18px,2.4vw,34px);align-items:start}
@media(min-width:1000px){.ag__p{grid-template-columns:minmax(0,1fr) auto}.ag__p .pb__bew--1 .bw--tel{width:260px}.ag__p--agb{grid-template-columns:minmax(0,1fr) minmax(0,.95fr)}}
.ag__p--agb .pb__bew{flex-direction:column}
.ag__p--agb .pb__bew .bw--dok{width:100%}
.ag__t p{font-size:1.02rem;line-height:1.66;color:rgba(11,42,76,.92);max-width:66ch}
.ag__t p+p{margin-top:.8em}
.ag__q{font-family:var(--mono);font-size:11.5px!important;letter-spacing:.06em;line-height:1.6!important;color:rgba(11,42,76,.66)!important;margin-top:1.2em!important}
.ag__l{display:grid;gap:8px;margin:14px 0 0;padding:0;list-style:none}
.ag__l li{display:grid;grid-template-columns:96px minmax(0,1fr);gap:12px;padding:10px 14px;border-radius:12px;background:var(--kuhle-h);box-shadow:var(--kuhle-h-s);font-size:.97rem;line-height:1.55;color:rgba(11,42,76,.92)}
.ag__l li b{font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--messing);padding-top:3px}
.ag__l--haken li{grid-template-columns:22px minmax(0,1fr)}
.ag__l--haken li::before{content:'';width:12px;height:7px;margin-top:7px;border-left:1.6px solid var(--messing);border-bottom:1.6px solid var(--messing);transform:rotate(-45deg)}
.ag__p--voll{margin-top:clamp(16px,2vw,26px)}
.ag__zwei{display:grid;gap:clamp(20px,3vw,44px)}
@media(min-width:1000px){.ag__zwei{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)}}
.ag__offen{margin-top:16px;padding:16px 18px}
.ag__offen p{font-size:.97rem;line-height:1.6;color:rgba(11,42,76,.9)}
.hum{display:grid;gap:8px}
.hum__z{display:grid;grid-template-columns:minmax(0,1fr) 26px minmax(0,1fr);gap:10px;align-items:center;padding:10px 12px;border-radius:14px;background:var(--kuhle-h);box-shadow:var(--kuhle-h-s)}
.hum__z p{margin:0;font-size:.94rem;line-height:1.5}
.hum__h{color:rgba(11,42,76,.72)}
.hum__m{color:var(--tinte)}
.hum__z i{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,#1E68AE,#0C3F72);color:#fff}
.hum__z i svg{width:11px;height:11px;stroke:currentColor;fill:none;stroke-width:1.5}
@media(max-width:620px){.hum__z{grid-template-columns:1fr}.hum__z i{transform:rotate(90deg)}.ag__l li{grid-template-columns:1fr;gap:4px}}
.pb__nr{letter-spacing:.12em}
.brief6__r h3{margin-top:clamp(18px,2vw,28px)}
.schluss .gruss-u small{color:#F6E6D6;text-shadow:0 1px 3px rgba(3,10,16,.9)}
@media(min-width:1000px){.ag__p--tech{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}}
.pb__bew--breit{width:100%}.pb__bew--breit .bw--dok{width:100%}
'''
