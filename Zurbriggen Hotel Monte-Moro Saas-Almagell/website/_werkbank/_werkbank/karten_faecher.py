#!/usr/bin/env python3
"""Werkbank Hotel Monte-Moro, Kapitel «Ihre Karte, neu gesetzt»: alle Karten des Hauses als Blätter im Fächer (ohne Angaben)
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


ETIKETT = {'roestihues': 'Röstihüs', 'wein-apero': 'Weinkarte', 'preisliste': 'Preisliste', 'zuschlaege': 'Zuschläge', 'spa': 'Spa'}


def einsetzen(t):
    """Nur mehr Blätter im Fächer (Robert 09.11.2026, 16:51: «einfach nur mehr Dokumente … im Raum schweben», keine Kacheln, keine Angaben):
    jedes Blatt wie im Kit mit seinem Etikett (Name, «ansehen»); Titel, Text und Knöpfe des Kapitels bleiben. Fehlt der Plan: unverändert."""
    if not os.path.exists(PLAN):
        return t
    plan = json.load(open(PLAN, encoding='utf-8'))
    if len(plan) < 3:
        return t
    e = html.escape
    def blatt(i, p):
        n = ETIKETT.get(p['ziel'], p['name'])
        return (f'<a class="blattk blattk--{i + 1}" style="--j:{i}" href="{e(p["href"])}" target="_blank" rel="noopener">'
                f'<img src="karten/{p["ziel"]}.webp" width="{p["b"]}" height="{p["h"]}" alt="Idee: {e(n)}" loading="lazy" decoding="async"><span>{e(n)}<b>ansehen</b></span></a>')
    neu = f'<div class="faecher faecher--{len(plan)}" data-a="auf">' + ''.join(blatt(i, p) for i, p in enumerate(plan)) + '</div>'
    t, n = re.subn(r'<div class="faecher faecher--\d+"[^>]*>.*?</a>\s*</div>', lambda m: neu, t, count=1, flags=re.S)
    if not n:
        return t
    namen = ''.join(f'<span>{e(p["name"])}</span>' for p in plan)
    t = re.sub(r'(<div class="namenzug"[^>]*><div>).*?(</div></div>)', lambda m: m.group(1) + namen * 5 + m.group(2), t, count=1, flags=re.S)
    return t


CSS = """
/* ---------- Kapitel Karten: fünf Blätter schweben im Fächer, zwei Reihen versetzt (karten_faecher.py, Robert 09.11.2026, 16:51) ---------- */
.faecher--5{aspect-ratio:1/.9}
.faecher--5 .blattk{width:28%}
.faecher--5 .blattk--1{left:4%;top:3%;z-index:1}.faecher--5 .blattk--2{left:36%;top:0;z-index:2}.faecher--5 .blattk--3{left:68%;top:4%;z-index:1}
.faecher--5 .blattk--4{left:20%;top:52%;z-index:3}.faecher--5 .blattk--5{left:52%;top:53%;z-index:3}
.da .faecher--5 .blattk--1,.faecher--5.da .blattk--1{transform:rotate(-7deg)}.da .faecher--5 .blattk--2,.faecher--5.da .blattk--2{transform:rotate(-1.5deg)}
.da .faecher--5 .blattk--3,.faecher--5.da .blattk--3{transform:rotate(6deg)}.da .faecher--5 .blattk--4,.faecher--5.da .blattk--4{transform:rotate(3.5deg)}
.da .faecher--5 .blattk--5,.faecher--5.da .blattk--5{transform:rotate(-4deg)}
.faecher--5.da .blattk--1:hover{transform:rotate(-7deg) translateY(-18px)}.faecher--5.da .blattk--2:hover{transform:rotate(-1.5deg) translateY(-18px)}
.faecher--5.da .blattk--3:hover{transform:rotate(6deg) translateY(-18px)}.faecher--5.da .blattk--4:hover{transform:rotate(3.5deg) translateY(-18px)}
.faecher--5.da .blattk--5:hover{transform:rotate(-4deg) translateY(-18px)}
.faecher--5 .blattk span{padding:9px 11px}
@media(max-width:700px){.faecher--5 .blattk span{flex-direction:column;gap:3px;font-size:9px;letter-spacing:.06em;padding:7px 8px}}
"""


if __name__ == '__main__':
    bau()
