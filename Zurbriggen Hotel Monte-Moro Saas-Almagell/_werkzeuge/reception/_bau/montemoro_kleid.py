#!/usr/bin/env python3
"""Kleid der Rezeption für das Hotel Monte-Moro (08.11.2026): rechnet die Farben und Schriften der Kopie aus Wild Side (Eckschild der Bar: Nacht in Braun,
Gold, Creme, Rot) in die Farbwelt des Hauses um (Markenbuch _kette/05-markenbauer/marke/farben.json, wie kleid/montemoro.css, website/assets/css/montemoro.css):
  dunkle warme Töne (Helligkeit unter 0,2)                → Nacht #0A2A4A / Tiefnacht #071B2E / Tinte #13263A (Farbton 210°), Helligkeit bleibt
  dunkle warme Töne (0,2 bis 0,45, wenig Farbe)            → Grau #4A5D70 (Farbton 210°, leise Schrift)
  Gold tief (Farbton 30–55°, Sättigung ab 0,3, bis 0,45)  → Lärche tief #9A4F2B (Betonung auf Hell)
  Gold (0,45 bis 0,72)                                    → Messing #B39867 (nur feine Linien, Knauf, Etikett)
  Gold hell (über 0,72)                                   → Messing hell / Papier (Farbton 34–39°)
  Warmweiss und Creme (wenig Farbe, hell)                 → Papier #F5F2EE / Fassade #E7E1DC / Creme #EFE9E1
  Rot der Bar (#F0323F, Farbton um 356°)                  → Lärche #C67144 (Hauptknopf, Akzent)
Rot der Warnungen (#a8321a, Farbton 5–15°), Grün und Blau bleiben; die Werte der Farbwelt des Hauses selbst bleiben unberührt.
Schriften: Prata → Fjalla One (Titel, eine Stärke), Hanken → Instrument Sans (Lauf), die Etiketten- und Versalienschrift → DM Mono; Dateien wie in
website/assets/fonts/ (FjallaOne-400, InstrumentSans-normal-400_600, DMMono-normal-400).
Einmal angewendet am 08.11.2026 auf die Kopie aus Wild Side; erneut nur auf frische Kopien (sonst wird doppelt umgerechnet).
Aufruf: python3 _werkzeuge/reception/_bau/montemoro_kleid.py [dateien …]"""
import colorsys, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATEIEN = ['studio/studio.css', 'studio/hell.css', 'studio/schweben.css', 'reception.css', 'montemoro-reception.css', 'gastgeber.css', 'brief-pdf.css',
           'brief-pdf.js', 'reception.js', 'studio/rundgang.js', 'studio/zur-werkbank.js', 'studio/auswahl.js', 'pruefung.html', 'anleitung.html',
           'index.html', 'brief-pdf.html', 'studio/anleitung.js', 'pruefung.js']
HAUS = {'0a2a4a', '0d3f6f', '071b2e', '115595', 'c67144', '9a4f2b', 'b39867', 'f5f2ee', 'e7e1dc', 'efe9e1', 'd6ccc1', '13263a', '4a5d70', 'e3d5b8', 'cdb88f', 'ffffff', '000000'}


def neu_rgb(r, g, b):
    if '%02x%02x%02x' % (r, g, b) in HAUS:
        return None
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hg = h * 360
    warm = hg <= 55 or hg >= 335
    if s < 0.03 or not warm:
        return None
    if (hg >= 335 or hg <= 5) and s > 0.6:                       # Rot der Bar → Lärche
        h2, s2, l = 21 / 360, 0.53, min(max(l, 0.38), 0.56)
    elif 5 < hg <= 15 and s > 0.6 and l < 0.5:                   # Rot der Warnungen bleibt
        return None
    elif l < 0.2:                                                # Nacht
        h2, s2 = 210 / 360, 0.68 if s > 0.06 else 0.5
    elif l < 0.45 and s < 0.3:                                   # leise Schrift → Grau
        h2, s2, l = 210 / 360, 0.2, min(l + 0.06, 0.45)
    elif 28 <= hg <= 55 and s >= 0.3:
        if l <= 0.45:
            h2, s2 = 20 / 360, 0.56                              # Gold tief → Lärche tief
        elif l <= 0.72:
            h2, s2 = 39 / 360, 0.32                              # Gold → Messing
        elif l > 0.88:
            h2, s2 = 33 / 360, min(s, 0.3)                       # fast weiss → Papier
        else:
            h2, s2 = 38 / 360, 0.38                              # Gold hell → Messing hell
    elif l > 0.7:                                                # Warmweiss, Creme → Papier, Fassade
        h2, s2 = 30 / 360, min(s * 0.8 + 0.05, 0.28)
    elif l < 0.32:
        h2, s2 = 210 / 360, 0.45
    else:
        h2, s2 = 210 / 360, 0.15                                 # warme Mitteltöne → kühles Grau
    r2, g2, b2 = colorsys.hls_to_rgb(h2, l, s2)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def hexe(m):
    t = m.group(1)
    if len(t) == 3:
        t = ''.join(c * 2 for c in t)
    x = neu_rgb(int(t[0:2], 16), int(t[2:4], 16), int(t[4:6], 16))
    return m.group(0) if x is None else '#%02x%02x%02x' % x


def rgba(m):
    x = neu_rgb(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return m.group(0) if x is None else f'{m.group(1)}({x[0]},{x[1]},{x[2]}{m.group(5)}'


FACE = {'Fjalla One': "@font-face{font-family:'Fjalla One';font-style:normal;font-weight:400;font-display:swap;src:url('%sassets/fonts/FjallaOne-400.woff2') format('woff2')}",
        'Instrument Sans': "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url('%sassets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}",
        'DM Mono': "@font-face{font-family:'DM Mono';font-style:normal;font-weight:400;font-display:swap;src:url('%sassets/fonts/DMMono-normal-400.woff2') format('woff2')}"}


def schriften(s):
    # @font-face der Kopie (Prata, zweimal Hanken) durch die drei Schriften des Hauses ersetzen, mit demselben Weg zur Website
    m = re.search(r"@font-face\{font-family:'Prata';[^}]*url\('((?:\.\./)*)assets/schrift/prata-latin\.woff2'\)[^}]*\}", s)
    if m:
        weg = m.group(1)
        s = re.sub(r"@font-face\{font-family:'(?:Prata|Hanken)';[^}]*\}\n?", '', s)
        s = s[:m.start()] + '\n'.join(FACE[k] % weg for k in ('Fjalla One', 'Instrument Sans', 'DM Mono')) + '\n' + s[m.start():]
    s = re.sub(r"@font-face\{font-family:'Hanken';[^}]*\}\n?", '', s)
    s = s.replace("--caps:'Prata',Georgia,'Times New Roman',serif", "--caps:'DM Mono',ui-monospace,Menlo,monospace")
    s = s.replace("--mono:'Hanken',ui-monospace,Menlo,monospace", "--mono:'DM Mono',ui-monospace,Menlo,monospace")
    s = s.replace("'Prata',Georgia,'Times New Roman',serif", "'Fjalla One','Arial Narrow',Arial,sans-serif").replace("'Prata',Georgia,serif", "'Fjalla One','Arial Narrow',Arial,sans-serif")
    s = s.replace("Prata,Georgia,serif", "'Fjalla One','Arial Narrow',Arial,sans-serif")
    s = s.replace("'Prata'", "'Fjalla One'").replace('"Prata"', '"Fjalla One"')
    s = s.replace("'Hanken'", "'Instrument Sans'").replace('"Hanken"', '"Instrument Sans"')
    s = s.replace('assets/schrift/prata-latin.woff2', 'assets/fonts/FjallaOne-400.woff2').replace('assets/schrift/hanken-latin.woff2', 'assets/fonts/InstrumentSans-normal-400_600.woff2')
    return s


def um(s):
    s = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F\w])', hexe, s)
    s = re.sub(r'(rgba?)\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(\s*[,)])', rgba, s)
    s = re.sub(r'%23([0-9a-fA-F]{6})', lambda m: '%23' + hexe(re.match(r'#(\w+)', '#' + m.group(1)))[1:], s)   # Farben in eingebetteten SVG
    return schriften(s)


if __name__ == '__main__':
    for d in sys.argv[1:] or DATEIEN:
        p = os.path.join(C, d)
        alt = open(p, encoding='utf-8').read()
        neu = um(alt)
        open(p, 'w', encoding='utf-8').write(neu)
        print(d, 'geändert' if neu != alt else 'gleich')
