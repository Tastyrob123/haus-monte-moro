#!/usr/bin/env python3
"""Werkbank Monte-Moro, Blatt «Worum es geht» zwischen Brief und Inhalt (Werkbank Kern, 08.11.2026; Aufbau und Kleid wie das Blatt mit Rechner
im Stamm). Robert 1.11.2026: «Worum es geht» bleibt bei Hotels, weil Buchungen über die eigene Website Mehrwert bringen. Der Rechner zeigt, was bei
Ihnen bleibt, wenn ein Teil der Übernachtungen direkt statt über ein Portal gebucht wird. Belegt ist nur der Zimmerpreis (website/inhalt/daten.py,
PREISE: Budgetzimmer mit Frühstück, pro Person/Tag); Zahl der Übernachtungen, Provision und Anteil sind Annahmen, als solche beschriftet und überschreibbar.
Kein Agenturpreis, keine Zusage."""
import html, os, sys

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), 'inhalt'))
import daten as D  # noqa: E402

_PREIS = float(D.PREISE[0][2])   # 90.00
ANNAHMEN = [  # Schlüssel, Zeile, Wert, Einheit, Beschriftung
    ('naechte', 'Übernachtungen im Jahr, heute über ein Portal gebucht', 600, '', 'Annahme · je Person und Nacht'),
    ('preis', 'Preis je Person und Nacht', f'{_PREIS:.2f}', 'CHF', f'laut Ihrer Preisliste: {D.PREISE[0][0]}, {D.PREISE[0][1]}'),
    ('provision', 'Provision des Portals', 15, '%', 'Annahme · Ihr Vertrag mit dem Portal entscheidet'),
    ('anteil', 'Anteil, der künftig direkt bei Ihnen bucht', 25, '%', 'Annahme'),
]


def _chf(x):
    return f"{round(x):,}".replace(',', '’')


def blatt(k):
    v = {key: float(wert) for key, _z, wert, _e, _q in ANNAHMEN}
    direkt = v['naechte'] * v['anteil'] / 100
    umsatz = direkt * v['preis']
    bleibt = umsatz * v['provision'] / 100
    felder = ''.join(f'<div class="vt-feld"><div class="vt-feld__l"><span>{e(z)}</span><small>{e(q)}</small></div><label class="vt-feld__w"><input type="text" inputmode="decimal" value="{wert}" data-k="{key}" aria-label="{e(z)}">'
                     + (f'<em>{e(ein)}</em>' if ein else '') + '</label></div>' for key, z, wert, ein, q in ANNAHMEN)
    gruende = [('Gebucht wird bei Ihnen', 'Das Buchungsfenster sitzt schon heute auf Ihrer eigenen Seite. Neu wählt der Gast Anreise, Abreise und Gäste gleich im ersten Bild der Startseite.'),
               ('Was im Preis steckt, steht vorn', 'Postautos im ganzen Saastal, im Sommer die Bergbahnen, Frühstück, Racletteabend und Kidsclub: Das steht wie auf einem Bon, bevor jemand vergleicht.'),
               ('Das Zimmer, bevor man bucht', 'Jede Zimmerart öffnet sich mit allen Fotos, der Ausstattung und den Preisen. Wer sein Zimmer kennt, bucht lieber direkt.')]
    fotos = ['vt-g-1', 'vt-g-2', 'vt-g-3']
    gr = ''.join(f'<li>' + (f'<span class="vt-gb">{k["bild"](f, t)}</span>' if f in k['m'] else '') + f'<b>{e(t)}</b><span>{e(x)}</span></li>' for (t, x), f in zip(gruende, fotos))
    return f'''
<section class="fl fl--navy tapete blatt vt" id="worum">
  <div class="in">
    {k['kopf'](0, 'Worum es geht', ['Direkt gebucht,', 'bleibt mehr im Haus.'], 'Jede Nacht, die ein Gast direkt bei Ihnen bucht statt über ein Portal, spart die Provision. Die neue Seite soll das Buchen bei Ihnen so leicht machen wie dort. Dieses Blatt ist ein Rechenbeispiel; jede Annahme rechts können Sie durch Ihre eigene Zahl ersetzen.')}
    <div class="ag-blatt vt-r" data-a="hoch">
      <div class="vt-r__t">
        <p class="ag-r__n">Direkt statt über ein Portal</p>
        <h3>Ein Rechenbeispiel.</h3>
        <p class="vt-r__lead">Auf Grundlage dieser Annahmen: Buchen <b data-vt="direkt">{_chf(direkt)}</b> Übernachtungen im Jahr direkt bei Ihnen, sind das <b data-vt="umsatz">{_chf(umsatz)}</b> Franken, für die keine Provision anfällt. Bei Ihnen bleiben so <b data-vt="bleibt">{_chf(bleibt)}</b> Franken im Jahr.</p>
        <p class="ag-r__n vt-gr__k">Drei Wege zur Direktbuchung</p>
        <ul class="vt-gr">{gr}</ul>
        <p class="vt-gegen__satz">Wie viele Gäste direkt buchen, hängt nicht an der Seite allein: Saison, Preise im Portal, Bewertungen und Empfehlungen spielen mit. Eine Zusage ist das Rechenbeispiel nicht.</p>
      </div>
      <div class="vt-r__r">
        <p class="vt-r__k">Vier Zahlen, jede lässt sich überschreiben</p>
        {felder}
        <div class="vt-ergebnis">
          <div class="vt-erg"><b data-vt="direkt">{_chf(direkt)}</b><span>Nächte</span><small>direkt gebucht im Jahr</small></div>
          <div class="vt-erg"><b data-vt="umsatz">{_chf(umsatz)}</b><span>CHF</span><small>Umsatz ohne Provision</small></div>
          <div class="vt-erg vt-erg--gross"><b data-vt="bleibt">{_chf(bleibt)}</b><span>CHF</span><small>bleiben im Jahr bei Ihnen, als Rechenbeispiel</small></div>
        </div>
      </div>
    </div>
  </div>
</section>
{JS}'''


def bilder(webp, haus):
    for n, key, lage in (('vt-g-1', 'z-sessel', (.5, .5)), ('vt-g-2', 'fr-tisch', (.5, .5)), ('vt-g-3', 'z-hell', (.5, .5))):
        webp(haus(key), n, 520, 80, 3 / 2, lage)


JS = '''<script id="vt-rechner">
(function(){var S=document.getElementById('worum');if(!S)return;
var nf=new Intl.NumberFormat('de-CH',{maximumFractionDigits:0});
function w(el){var t=String(el.value).replace(/[\\u2019'\\u202f\\u00a0 ]/g,'').replace(/,/g,'.');var v=parseFloat(t);return isFinite(v)&&v>=0?v:null}
function setze(k,t){[].forEach.call(S.querySelectorAll('[data-vt="'+k+'"]'),function(x){x.textContent=t})}
function rechne(){var v={};[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){var x=w(i);i.classList.toggle('falsch',x===null);v[i.getAttribute('data-k')]=x===null?0:x});
var direkt=v.naechte*v.anteil/100,umsatz=direkt*v.preis,bleibt=umsatz*v.provision/100;
setze('direkt',nf.format(direkt));setze('umsatz',nf.format(umsatz));setze('bleibt',nf.format(bleibt))}
[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){i.addEventListener('input',rechne)});rechne()})();
</script>'''


CSS = '''
/* Blatt des Rechenbeispiels (Bauart des Blatts aus dem Stamm) */
.ag-blatt{position:relative;padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:linear-gradient(rgba(245,242,238,.95),rgba(245,242,238,.95)),var(--weiss) url(../werkbank/eigen/tapete-hell.svg) 50% 0/240px auto;color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 50px 70px -46px rgba(7,27,46,.95)}
.ag-blatt::before,.ag-blatt::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(179,152,103,.55);border-radius:clamp(14px,1.6vw,24px);inset:clamp(10px,1.1vw,16px)}
.ag-blatt::after{inset:clamp(15px,1.5vw,22px);border-color:rgba(179,152,103,.25);border-radius:clamp(11px,1.3vw,19px)}
.ag-r__n{margin:0 0 12px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--taupe)}
.vt-r{color:var(--tinte)}
.vt-r__lead b{color:var(--rot)!important}
.vt-gegen__satz{color:rgba(19,38,58,.82)!important;border-top-color:rgba(179,152,103,.5)!important}
.vt-gr li{display:grid;grid-template-columns:clamp(92px,9vw,128px) 1fr;column-gap:16px;align-items:start}
.vt-gr li>.vt-gb{grid-row:1/span 2;display:block;border-radius:12px;overflow:hidden;aspect-ratio:3/2}.vt-gr li>.vt-gb img{display:block;width:100%;height:100%;object-fit:cover}
.vt-gr li>b,.vt-gr li>span:not(.vt-gb){grid-column:2}
@media(max-width:560px){.vt-gr li{grid-template-columns:72px minmax(0,1fr);align-items:center;row-gap:8px}.vt-gr li>.vt-gb{grid-row:1}.vt-gr li>span:not(.vt-gb){grid-column:1/-1}}   /* Robert 10.11.2026: am Handy Bild über dem Text, keine schmale Spalte */
'''
