#!/usr/bin/env python3
"""Werkbank Hotel Monte-Moro, Kapitel «Ihre Karten, neu gesetzt»: alle Karten des Hauses als Blätter mit Angaben
(Robert 09.11.2026, 15:34, KORREKTUR-ROBERT.md 5: «nicht zwei dumme Dokumente in der Luft hängen, obwohl es eigentlich mehr sind»).
Die Karten sind die fünf Karten des Kartenbretts (_werkzeuge/carte/_daten/stand/*.json): Name, was drinsteht («unter»), Format und Stand
(«veroeffentlicht») kommen aus der Karte, die Seitenzahl aus dem gedruckten PDF. Nichts geschätzt.
Röstihüs-Karte und Wein/Apéro liegen schon als Unterlagen (unterlagen/pdf, Seite «Unterlagen» mit dem Vergleich zu heute); die übrigen druckt
das Kartenbrett (carte/drucke.js, Server 9383) nach werkbank/karten/<ziel>.pdf. Nur dieses Kapitel ändert sich; die Seite «Unterlagen» bleibt.
   python3 _werkbank/karten_faecher.py        → werkbank/karten/*.pdf, werkbank/karten/*.webp, _werkbank/karten_faecher.json
   wb_kapitel.py ruft einsetzen(html) für das Kapitel und hängt CSS an."""
import datetime, html, json, os, re, subprocess, sys
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
CARTE = os.path.join(PROJ, '_werkzeuge', 'carte')
STAND = os.path.join(CARTE, '_daten', 'stand')
PLAN = os.path.join(W, 'karten_faecher.json')
FOLGE = ['roestihues', 'wein-apero', 'preisliste', 'zuschlaege', 'spa']   # Röstihüs zuerst (gross), dann Haus
UNTERLAGE = {'roestihues', 'wein-apero'}                                  # mit Seite «Unterlagen» (Vergleich zu heute)
FORMATE = {(210, 297): 'A4', (148, 210): 'A5', (297, 420): 'A3', (105, 148): 'A6'}


def seiten(pdf):
    t = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    m = re.search(r'Pages:\s+(\d+)', t)
    return int(m.group(1)) if m else 0


def bau():
    os.makedirs(os.path.join(ROOT, 'werkbank', 'karten'), exist_ok=True)
    
    plan = []
    for z in FOLGE:
        q = os.path.join(STAND, z + '.json')
        if not os.path.exists(q):
            print('Karte fehlt im Kartenbrett:', z); continue
        d = json.load(open(q, encoding='utf-8'))
        if z in UNTERLAGE:
            pdf = os.path.join(ROOT, 'unterlagen', 'pdf', z + '.pdf')
        else:
            pdf = os.path.join(ROOT, 'werkbank', 'karten', z + '.pdf')
            r = subprocess.run(['node', os.path.join(CARTE, 'drucke.js'), z, 'stand', pdf + '.neu.pdf'], capture_output=True, text=True, timeout=240)
            if r.returncode == 0 and os.path.exists(pdf + '.neu.pdf'):
                os.replace(pdf + '.neu.pdf', pdf)
            else:
                print('Kartenbrett nicht erreichbar, bleibt:', z, r.stderr[-200:])
        if not os.path.exists(pdf):
            print('kein PDF:', z); continue
        roh = os.path.join(W, 'roh', 'kf-' + z)
        os.makedirs(os.path.dirname(roh), exist_ok=True)
        subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '110', '-png', '-singlefile', pdf, roh], check=True)
        im = Image.open(roh + '.png').convert('RGB'); im.thumbnail((900, 1300))
        im.save(os.path.join(ROOT, 'werkbank', 'karten', z + '.webp'), 'WEBP', quality=86)
        fmt = tuple(d.get('format') or (210, 297))
        stand = (d.get('veroeffentlicht') or '')[:10]
        plan.append(dict(ziel=z, name=d.get('name', z), unter=d.get('unter', ''), seiten=seiten(pdf), format=FORMATE.get(fmt, f'{fmt[0]} × {fmt[1]} mm'),
                         stand=datetime.date.fromisoformat(stand).strftime('%d.%m.%Y') if stand else '', b=im.width, h=im.height,
                         href=(f'../unterlagen/index.html#{z}' if z in UNTERLAGE else f'karten/{z}.pdf')))
    json.dump(plan, open(PLAN, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Karten im Kapitel:', ', '.join(p['ziel'] for p in plan))


def einsetzen(t):
    """Fächer und Namenzug des Kapitels «Unterlagen» durch alle Karten des Hauses ersetzen (fehlt der Plan: unverändert)."""
    if not os.path.exists(PLAN):
        return t
    plan = json.load(open(PLAN, encoding='utf-8'))
    if len(plan) < 3:
        return t
    e = html.escape
    def blatt(i, p):
        ang = ' · '.join(x for x in (f"{p['seiten']} {'Seite' if p['seiten'] == 1 else 'Seiten'}" if p['seiten'] else '', p['format'], f"Stand {p['stand']}" if p['stand'] else '') if x)
        return (f'<a class="blattk kf__b kf__b--{i + 1}" style="--j:{i}" href="{e(p["href"])}" target="_blank" rel="noopener">'
                f'<span class="kf__s"><img src="karten/{p["ziel"]}.webp" width="{p["b"]}" height="{p["h"]}" alt="{e(p["name"])}" loading="lazy" decoding="async"><i class="kf__p" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg></i></span>'
                f'<span class="kf__t"><strong>{e(p["name"])}</strong><small>{e(ang)}</small><em>{e(p["unter"])}</em></span></a>')
    staende = sorted({p['stand'] for p in plan if p['stand']})
    try:
        import rh_werkzeuge as WK
        carte = [w for w in WK.WERKZEUGE if w[0] == 'carte'][0]
        knopf = f'<a class="kf__l" href="{e(carte[6])}" target="_blank" rel="noopener">{e(carte[1])} öffnen</a>' if carte[6] else ''
    except Exception:
        knopf = ''
    zahl = {3: 'Drei', 4: 'Vier', 5: 'Fünf', 6: 'Sechs'}.get(len(plan), str(len(plan)))
    info = (f'<div class="kf__i"><p class="kf__k">{zahl} Karten, ein Werkzeug</p><h3>Gesetzt im Kartenbrett.</h3>'
            f'<p>Gerichte, Weine und Preise pflegen Sie im Kartenbrett; daraus entstehen diese Blätter, druckfertig als PDF.</p>'
            + (f'<p class="kf__k">Stand {staende[-1]}</p>' if staende else '') + knopf + '</div>')
    neu = f'<div class="faecher faecher--{len(plan)} kf" data-a="auf">' + ''.join(blatt(i, p) for i, p in enumerate(plan)) + (info if len(plan) % 3 else '') + '</div>'
    t, n = re.subn(r'<div class="faecher faecher--\d+"[^>]*>.*?</a>\s*</div>', lambda m: neu, t, count=1, flags=re.S)
    if not n:
        return t
    # Titel und Satz des Kapitels in der Mehrzahl (nur hier; die Seite «Unterlagen» bleibt bei der Röstihüs-Karte)
    # Titel «Ihre Karten, neu gesetzt.» setzt haus.TITEL_NEU
    t = t.replace('Die Karte des Röstihüs, neu gesetzt neben den Seiten, wie sie heute auf dem Tisch liegen: die Röstis, die Cordon bleus, der Wein von Fabian und der Apéro.',
                  'Alle Karten des Hauses, neu gesetzt: die Röstis und Cordon bleus, der Wein von Fabian mit dem Apéro, die Preisliste, die Zuschläge und das Spa im Partnerhotel. '
                  'Die Karten des Röstihüs liegen in den Unterlagen neben den Seiten, wie sie heute auf dem Tisch liegen.', 1)
    namen = ''.join(f'<span>{e(p["name"])}</span>' for p in plan)
    t = re.sub(r'(<div class="namenzug"[^>]*><div>).*?(</div></div>)', lambda m: m.group(1) + namen * 5 + m.group(2), t, count=1, flags=re.S)
    return t


CSS = """
/* ---------- Kapitel Karten: alle Karten des Hauses mit Angaben (karten_faecher.py, Robert 09.11.2026) ---------- */
.faecher.kf{position:relative;aspect-ratio:auto;max-width:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-auto-rows:auto;gap:clamp(12px,1.2vw,18px);align-self:stretch}
.kf .blattk{position:relative;top:auto;left:auto;width:auto;display:flex;flex-direction:column;border-radius:14px;overflow:hidden;background:rgba(255,255,255,.05);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.1),0 30px 40px -28px rgba(0,0,0,.8);color:#f6f1e8;text-decoration:none;transform:translateY(60px)}
.kf.da .blattk,.da .kf .blattk{transform:none}
.kf.da .blattk:hover{transform:translateY(-6px)}
.kf .blattk .kf__s{display:block;position:relative;aspect-ratio:210/297;overflow:hidden;background:#f7f3ec}
.kf .blattk .kf__s img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0;display:block}
.kf .blattk .kf__t{position:static;background:none;text-transform:none;letter-spacing:0;font-family:inherit;justify-content:flex-start;display:flex;flex-direction:column;gap:3px;padding:12px 14px 14px}
.kf .kf__t strong{font-family:var(--serif);font-weight:400;font-size:clamp(1rem,1.15vw,1.25rem);line-height:1.15}
.kf .kf__t small{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}
.kf .kf__t em{font-style:normal;font-size:.86rem;line-height:1.35;color:rgba(246,241,232,.78)}
.kf .kf__t b{font-family:var(--mono);font-weight:400;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(246,241,232,.62);margin-top:4px}
.kf .blattk .kf__t{white-space:normal;overflow:visible}
.kf__i{display:flex;flex-direction:column;justify-content:center;gap:10px;padding:clamp(16px,1.6vw,24px);border-radius:14px;background:rgba(255,255,255,.04);box-shadow:inset 0 0 0 1px rgba(216,178,100,.28);color:#f6f1e8}
.kf__i h3{margin:0;font-family:var(--serif);font-weight:400;font-size:clamp(1.25rem,1.6vw,1.7rem);line-height:1.12;color:#f6f1e8}
.kf__i p{margin:0;font-size:.92rem;line-height:1.45;color:rgba(246,241,232,.8)}
.kf__i .kf__k{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.kf__i .kf__l{margin-top:4px;font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:#f6f1e8;text-decoration:none;border-bottom:1px solid var(--gold);align-self:flex-start;padding-bottom:3px}
.kf__i .kf__l:hover{color:var(--gold)}
@media(max-width:1199px){.faecher.kf{grid-template-columns:1fr 1fr}}
.kf .kf__p{position:absolute;right:10px;top:10px;width:30px;height:30px;border-radius:50%;background:var(--navy);display:grid;place-items:center;box-shadow:0 6px 12px -6px rgba(0,0,0,.6)}
.kf .kf__p svg{width:12px;height:12px;fill:none;stroke:#f6f1e8;stroke-width:1.6}
@media(prefers-reduced-motion:reduce){.kf .blattk{transform:none;transition:none}}
"""


if __name__ == '__main__':
    bau()
