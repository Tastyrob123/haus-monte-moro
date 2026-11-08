#!/usr/bin/env python3
"""Werkbank Monte-Moro, Kapitel I «Befund des aktuellen Auftritts online» (Werkbank Kern, 08.11.2026; Bauart der Befund-Bühne aus dem Stamm).

Die Funde kommen aus der Potentialanalyse des Hauses (_kette/04-analyst/potential.json, Stand 17.10.2026), nichts dazuerfunden: vorn die vier, die
am meisten ausmachen (Robert 20.10.2026: «nur so die krassesten 4 Sachen», das Wichtigste zuerst, in der Reihenfolge der Analyse), alle zwölf auf der
Seite befund/. Belegbilder sind die Aufnahmen der Analyse: die heutige Seite im Gerät (Blender), mit der Stelle markiert, dazu der Ausschnitt, von dem der
Satz spricht (Roberts Kriterium 30). Eine Bühne, ein Befund im Blick: Pfeile, Ziffern, Wischen, Tasten. Kein Vorwurf, keine Mutmassung, ohne mailto."""
import html, json, os
from PIL import Image

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
AN = os.path.join(PROJ, '_kette', '04-analyst')
LI = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
RE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
_P = json.load(open(os.path.join(AN, 'potential.json'), encoding='utf-8'))
VORN = 4
NAH = {'02': 1, '03': 1}   # welcher Ausschnitt den Satz am genausten zeigt (02: «kein Preis, kein Knopf», 03: das Buchungsfenster mit Grösse und Betten)
STAND = '17. Oktober 2026'


def befunde():
    aus = []
    for b in _P['befunde']:
        bw = b['beweis']
        nah = bw['was_genau'][NAH.get(b['nr'], 0)] if bw['was_genau'] else None
        aus.append(dict(nr=b['nr'], was=b['was'] + '.', wo=b['heute'], beispiel=b['beispiel'], gaeste=bw.get('fuer_gaeste', ''), haus=bw.get('fuer_das_haus', ''), tun=b['idee'],
                        ganz=os.path.join(AN, bw['geraet']), nah=os.path.join(AN, nah['bild']) if nah else None,
                        nah_t=' · '.join(nah['beschriftung']) if nah else '', stelle=bw.get('wo', '')))
    return aus


def bilder(webp):
    for b in befunde()[:VORN]:
        if os.path.exists(b['ganz']):
            webp(Image.open(b['ganz']).convert('RGBA'), f'bf-h-{b["nr"]}', 900 if Image.open(b['ganz']).width > Image.open(b['ganz']).height else 640, 84)
        if b['nah'] and os.path.exists(b['nah']):
            webp(Image.open(b['nah']).convert('RGB'), f'bf-n-{b["nr"]}', 1100, 84)


def _breit(p):
    im = Image.open(p)
    return im.width > im.height


STARK = [(x['was'] + '.', x['satz']) for x in _P['was_gut_ist']]


def kopiere_analyse():
    """Der ganze Befund als eigene Seite neben der Werkbank (befund/index.html), für Esther und Fabian Zurbriggen geschrieben: was heute stark ist,
    alle zwölf Funde mit Gerät und Ausschnitt, dazu die übrigen Beobachtungen. Quelle: Potentialanalyse (Station 04), nichts dazuerfunden."""
    import kern as K
    z = os.path.join(ROOT, 'befund'); os.makedirs(os.path.join(z, 'img'), exist_ok=True)
    for f in os.listdir(os.path.join(z, 'img')):
        os.remove(os.path.join(z, 'img', f))
    stark = ''.join(f'<li><b>{e(t)}</b><span>{e(s)}</span></li>' for t, s in STARK)
    funde = ''
    for b in befunde():
        bi = ''
        for art, q in (('h', b['ganz']), ('n', b['nah'])):
            if not q or not os.path.exists(q):
                continue
            im = Image.open(q); im = im.convert('RGBA' if art == 'h' else 'RGB'); im.thumbnail((1000, 1000) if art == 'h' and im.width > im.height else (900, 900))
            n = f'{art}-{b["nr"]}.webp'; im.save(os.path.join(z, 'img', n), 'WEBP', quality=84)
            kl = f'bfs-{art}' + (' bfs-h--breit' if art == 'h' and im.width > im.height else '')
            alt = f'Die heutige Seite im Gerät, Stelle zum Fund {b["nr"]}' if art == 'h' else f'Ausschnitt: {b["nah_t"]}'
            bi += f'<img src="img/{n}" width="{im.width}" height="{im.height}" alt="{e(alt)}" decoding="async" class="{kl}">'
        funde += (f'<article class="bfs-f"><div class="bfs-b">{bi}</div><div><p class="bfs-nr">{b["nr"]}</p><h2>{e(b["was"])}</h2><p class="bfs-wo"><b>Heute</b>{e(b["wo"])}</p>'
                  f'<p class="bfs-bsp">{e(b["beispiel"])}</p>'
                  f'<dl><dt>Für Ihre Gäste</dt><dd>{e(b["gaeste"])}</dd><dt>Für Sie</dt><dd>{e(b["haus"])}</dd><dt>Was wir tun würden</dt><dd>{e(b["tun"])}</dd></dl></div></article>')
    weitere = ''.join(f'<li><span>{e(x["was"])}</span></li>' for x in _P['weitere'])
    haupt = f'''<section class="fl fl--nacht tapete-leicht bfs"><div class="in">
  <p class="kap kap--z">Der Befund</p>
  <h1 class="t1 zt"><span class="z"><span>Wie das Monte-Moro</span></span><span class="z"><span><em>heute im Netz steht.</em></span></span></h1>
  <p class="bfs-lauf">Angesehen wurde monte-moro.ch am Rechner und am Telefon, dazu das Buchungsfenster, die Speisekarte und die Portale, Stand {STAND}.
  Hier steht zuerst, was schon stark ist, dann jeder Punkt, an dem ein Gast auf dem Weg zu Ihnen hängen bleibt, mit der Stelle im Gerät.</p>
</div></section>
<section class="fl fl--papier tapete-hell bfs"><div class="in"><h2 class="bfs-h">Was schon stark ist</h2><ul class="bfs-l bfs-l--3">{stark}</ul></div></section>
<section class="fl fl--nacht tapete-leicht bfs"><div class="in"><h2 class="bfs-h">Zwölf Punkte, das Wichtigste zuerst</h2>{funde}</div></section>
<section class="fl fl--papier tapete-hell bfs"><div class="in"><h2 class="bfs-h">Was sonst noch auffällt</h2><ul class="bfs-l">{weitere}</ul></div></section>'''
    css = ('<style>.bfs .in{max-width:1180px}.bfs-lauf{max-width:62ch;margin:18px auto 0;text-align:center;font-size:clamp(1.05rem,1.3vw,1.25rem);line-height:1.6;color:rgba(245,242,238,.86)}'
           '.bfs-h{font-family:var(--serif);font-weight:400;font-size:clamp(1.8rem,3vw,2.8rem);margin:0 0 clamp(24px,3vw,44px)}'
           '.bfs-l{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:clamp(18px,2vw,30px)}'
           '@media(min-width:900px){.bfs-l--3{grid-template-columns:repeat(3,minmax(0,1fr))}.bfs-l:not(.bfs-l--3){grid-template-columns:repeat(4,minmax(0,1fr))}}'
           '.bfs-l li{display:flex;flex-direction:column;gap:8px;padding-top:16px;border-top:1px solid rgba(19,38,58,.16)}.bfs-l b{font-family:var(--serif);font-weight:400;font-size:1.3rem}.bfs-l span{line-height:1.6}'
           '.bfs-f{display:grid;gap:clamp(24px,4vw,64px);align-items:center;padding:clamp(28px,4vw,56px) 0;border-top:1px solid rgba(245,242,238,.14)}'
           '@media(min-width:900px){.bfs-f{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}}'
           '.bfs-b{display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;min-width:0}.bfs-b img{max-width:100%;height:auto;min-width:0}'
           '.bfs-b img.bfs-h{width:min(280px,62%)}.bfs-b img.bfs-h--breit{width:min(520px,100%)}.bfs-b img.bfs-n{width:min(480px,100%);border-radius:10px;box-shadow:0 0 0 5px var(--papier),0 26px 30px -20px rgba(0,0,0,.7)}'
           '.bfs-f>div:last-child{padding:clamp(22px,2.6vw,40px);border-radius:clamp(18px,2vw,28px);background:rgba(7,27,46,.55);box-shadow:inset 0 0 0 1px rgba(179,152,103,.32)}'
           '.bfs-nr{margin:0;font-family:var(--serif);font-size:clamp(3rem,6vw,5.6rem);line-height:.9;color:var(--gold)}.bfs-f h2{font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2.2vw,2.1rem);line-height:1.2;margin:12px 0 0;text-wrap:balance}'
           '.bfs-wo{display:flex;gap:14px;margin:16px 0 0;line-height:1.55;color:rgba(245,242,238,.8)}.bfs-wo b{font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-top:3px}'
           '.bfs-bsp{margin:14px 0 0;line-height:1.6;color:rgba(245,242,238,.72)}'
           '.bfs-f dl{margin:18px 0 0}.bfs-f dt{margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}.bfs-f dd{margin:6px 0 0;line-height:1.6;color:rgba(245,242,238,.9)}</style>')
    s = K.rahmen('Der Befund', 'Wie das Hotel Monte-Moro heute im Netz steht, angesehen im Oktober 2026.', 'Befund', haupt,
                 'Ein Befund von Robert Reff, Tasty Studios, nach dem Stand vom 17. Oktober 2026. Aufnahmen von monte-moro.ch nur zur Anschauung.')
    s = s.replace('</head>', css + '</head>', 1)
    open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(s)


def abschnitt(k, kopfk):
    M, bild = k['m'], k['bild']
    B = befunde()[:VORN]
    platten = ''
    for i, b in enumerate(B):
        breit = os.path.exists(b['ganz']) and _breit(b['ganz'])
        handy = (f'<div class="sbf-handy{" sbf-handy--breit" if breit else ""}">{bild("bf-h-" + b["nr"], "Die heutige Seite im Gerät, Stelle zum Befund " + b["nr"], lazy=i > 1)}</div>' if 'bf-h-' + b['nr'] in M else '')
        nah = (f'<figure class="sbf-nah{" sbf-nah--breit" if breit else ""}">{bild("bf-n-" + b["nr"], "Ausschnitt: " + b["nah_t"], lazy=i > 1)}</figure>' if 'bf-n-' + b['nr'] in M else '')
        sinn = ''.join(f'<div class="sbf-sinn__z"><dt>{e(t)}</dt><dd>{e(x)}</dd></div>' for t, x in (('Für Ihre Gäste', b['gaeste']), ('Für Sie', b['haus']), ('Was wir tun würden', b['tun'])) if x)
        platten += (f'<article class="sbf-p{" an" if i == 0 else ""}" data-i="{i}" aria-label="Befund {b["nr"]}">'
                    f'<div class="sbf-bild">{handy}{nah}</div>'
                    f'<div class="sbf-text"><p class="sbf-nr">{b["nr"]}</p><h3>{e(b["was"])}</h3><p class="sbf-wo"><b>Heute</b>{e(b["wo"])}</p><dl class="sbf-sinn">{sinn}</dl></div></article>')
    ziffern = ''.join(f'<button type="button" class="sbf-z" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">{b["nr"]}</button>' for i, b in enumerate(B))
    return f'''
<section class="fl fl--nacht tapete-leicht blatt sbf" id="k1">
  <div class="in">
    {kopfk('k1', ['Viel zu bieten,', 'wenig zu sehen.'], f'Angesehen wurde monte-moro.ch am Rechner und am Telefon, Stand {STAND}. Von den zwölf Punkten der Analyse stehen hier die vier, die am meisten ausmachen, jeder mit der Stelle im Gerät. Die übrigen stehen im ganzen Befund.')}
    <div class="sbf-b" tabindex="0" aria-roledescription="Karussell" aria-label="Die Befunde">
      <div class="sbf-platten">{platten}</div>
      <div class="sbf-fuss"><button type="button" class="wf__pf" data-f="-1" aria-label="Voriger Befund">{LI}</button><div class="sbf-ziffern">{ziffern}</div><button type="button" class="wf__pf" data-f="1" aria-label="Nächster Befund">{RE}</button></div>
    </div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(28px,3vw,48px)">{k['kn']('Den ganzen Befund ansehen', '../befund/index.html')}</div>
  </div>
</section>
<script>(function(){{var s=document.querySelector('.sbf-b');if(!s)return;var P=[].slice.call(s.querySelectorAll('.sbf-p')),Z=[].slice.call(s.querySelectorAll('.sbf-z')),ist=0,n=P.length;
function zeig(k){{ist=(k%n+n)%n;P.forEach(function(p,i){{p.classList.toggle('an',i===ist);if(i===ist||i===(ist+1)%n)[].forEach.call(p.querySelectorAll('img[loading=lazy]'),function(x){{x.loading='eager'}})}});Z.forEach(function(z,i){{z.setAttribute('aria-pressed',i===ist?'true':'false')}})}}
[].forEach.call(s.querySelectorAll('[data-f]'),function(b){{b.addEventListener('click',function(){{zeig(ist+(+b.getAttribute('data-f')))}})}});
Z.forEach(function(z,i){{z.addEventListener('click',function(){{zeig(i)}})}});
s.addEventListener('keydown',function(ev){{if(ev.key==='ArrowRight')zeig(ist+1);else if(ev.key==='ArrowLeft')zeig(ist-1)}});
var x0=null;s.addEventListener('touchstart',function(ev){{x0=ev.touches[0].clientX}},{{passive:true}});s.addEventListener('touchend',function(ev){{if(x0===null)return;var d=ev.changedTouches[0].clientX-x0;x0=null;if(Math.abs(d)>50)zeig(ist+(d<0?1:-1))}},{{passive:true}})}})();</script>'''


CSS = '''
/* ---------- Kapitel I «Befund» (sb_befund.py): ein Befund im Blick, die heutige Seite im Gerät, daneben der Ausschnitt ---------- */
.sbf-b{outline:0;margin-top:clamp(16px,2vw,32px)}
.sbf-platten{display:grid}
.sbf-p{grid-area:1/1;display:grid;gap:clamp(26px,4vw,72px);align-items:center;opacity:0;visibility:hidden;transition:opacity .25s linear,visibility 0s .25s;min-width:0}
.sbf-p.an{opacity:1;visibility:visible;transition:opacity .45s linear .1s,visibility 0s}
@media(min-width:960px){.sbf-p{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.sbf-bild{position:relative;display:flex;align-items:center;justify-content:center;min-height:clamp(320px,40vw,620px);min-width:0}
.sbf-handy{width:clamp(200px,19vw,290px);filter:drop-shadow(0 34px 34px rgba(0,0,0,.5))}
.sbf-handy--breit{width:min(100%,560px);align-self:flex-start;margin-top:4%}
.sbf-handy img{display:block;width:100%;height:auto}
.sbf-nah{position:absolute;right:0;bottom:4%;width:clamp(200px,24vw,360px);margin:0;border-radius:12px;overflow:hidden;
  box-shadow:0 0 0 6px var(--weiss),0 0 0 7px rgba(179,152,103,.6),0 34px 44px -24px rgba(0,0,0,.85)}
.sbf-nah--breit{right:4%;bottom:0;width:clamp(220px,26vw,400px)}
.sbf-handy+.sbf-nah{right:0}
.sbf-nah img{display:block;width:100%;height:auto}
.sbf-p.an .sbf-handy{animation:sbfHoch 1.1s cubic-bezier(.16,1,.3,1) both}.sbf-p.an .sbf-nah{animation:sbfHoch 1.3s cubic-bezier(.16,1,.3,1) .12s both}
@keyframes sbfHoch{from{translate:0 60px}to{translate:0 0}}
.sbf-nr{margin:0;font-family:var(--serif);font-size:clamp(3.6rem,7vw,7rem);line-height:.9;letter-spacing:.02em;color:var(--gold)}
.sbf-text{min-width:0;padding:clamp(22px,2.6vw,40px);border-radius:clamp(18px,2vw,28px);background:rgba(7,27,46,.55);box-shadow:inset 0 0 0 1px rgba(179,152,103,.32),0 30px 40px -30px rgba(0,0,0,.6)}   /* Ziffer und Text in einer Tafel (Oberflächen-Prüfung Punkt 4) */
.sbf-text h3{margin:clamp(12px,1.4vw,20px) 0 0;font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2.1vw,2.2rem);line-height:1.2;color:var(--weiss);text-wrap:balance}
.sbf-wo{display:flex;gap:14px;margin:clamp(14px,1.6vw,22px) 0 0;font-size:clamp(.96rem,1.04vw,1.06rem);line-height:1.55;color:rgba(245,242,238,.8)}
.sbf-wo b{flex:none;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-top:3px}
.sbf-sinn{margin:clamp(18px,2vw,28px) 0 0;border-top:1px solid rgba(179,152,103,.35)}
.sbf-sinn__z{padding:12px 0;border-bottom:1px solid rgba(179,152,103,.22)}
.sbf-sinn dt{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.sbf-sinn dd{margin:6px 0 0;font-size:clamp(1rem,1.08vw,1.1rem);line-height:1.6;color:rgba(245,242,238,.9)}
.sbf-fuss{display:flex;align-items:center;justify-content:center;gap:clamp(12px,2vw,28px);margin-top:clamp(26px,3vw,44px)}
.sbf-ziffern{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;max-width:640px}
.sbf-z{min-width:40px;padding:7px 9px;border-radius:999px;font-family:var(--mono);font-size:.78rem;color:rgba(245,242,238,.66);box-shadow:inset 0 0 0 1px rgba(179,152,103,.4);transition:color .4s,background .4s}
.sbf-z[aria-pressed="true"]{color:var(--tinte);background:var(--gold)}
@media(max-width:700px){.sbf-bild{min-height:0;padding:10px 0 40px}.sbf-handy{width:52vw}.sbf-handy--breit{width:100%;margin-top:0}.sbf-nah{width:60vw;bottom:0}.sbf-nah--breit{width:66vw;right:0;bottom:-6%}.sbf-ziffern{display:none}}
@media(prefers-reduced-motion:reduce){.sbf-p,.sbf-p.an .sbf-handy,.sbf-p.an .sbf-nah{transition:none;animation:none}}
'''
