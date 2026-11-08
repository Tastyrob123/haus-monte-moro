#!/usr/bin/env python3
"""Feste Druckschnitte für das Hotel Monte-Moro (Werkbank Papier, 08.11.2026; Bauart wie druckschrift.py der Vorlage):
Fjalla One (eine Stärke), Instrument Sans 400/500/600 und DM Mono 400 aus den Webschriften der Website (website/assets/fonts/*.woff2).
Variable Schriften schreibt Chromium als «Type 3» in die PDF, mit festen TrueType-Schnitten bleibt die Schrift scharf.
   python3 _werkbank/druckschrift.py → _werkbank/fonts/*.ttf  (alte Schnitte anderer Häuser werden entfernt)
Im Satz heissen die Familien wie die Schrift: 'Fjalla One', 'Instrument Sans', 'DM Mono' (umstellen() ersetzt Reste aus dem Kit)."""
import os
import re
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

W = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(os.path.dirname(os.path.dirname(W)), 'assets', 'fonts')
Z = os.path.join(W, 'fonts')
SCHNITTE = [('FjallaOne-400.woff2', 'FjallaOne-Regular', 'Fjalla One Druck', 'Regular', 400),
            ('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-Regular', 'Instrument Sans Druck', 'Regular', 400),
            ('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-Medium', 'Instrument Sans Druck', 'Medium', 500),
            ('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-SemiBold', 'Instrument Sans Druck', 'SemiBold', 600),
            ('DMMono-normal-400.woff2', 'DMMono-Regular', 'DM Mono Druck', 'Regular', 400)]
DATEIEN = {s[1] + '.ttf' for s in SCHNITTE}
# @font-face für den Satz (Pfad relativ zu _werkbank/satz/)
FACES = ("@font-face{font-family:'Fjalla One';font-style:normal;font-weight:100 900;src:url('../fonts/FjallaOne-Regular.ttf') format('truetype')}\n"
         "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:400;src:url('../fonts/InstrumentSans-Regular.ttf') format('truetype')}\n"
         "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:500;src:url('../fonts/InstrumentSans-Medium.ttf') format('truetype')}\n"
         "@font-face{font-family:'Instrument Sans';font-style:normal;font-weight:600 900;src:url('../fonts/InstrumentSans-SemiBold.ttf') format('truetype')}\n"
         "@font-face{font-family:'DM Mono';font-style:normal;font-weight:100 900;src:url('../fonts/DMMono-Regular.ttf') format('truetype')}\n")


def umstellen(css):
    """Satz-CSS des Kits: Titelschriften anderer Häuser → Fjalla One, Lauf-/Etikettschriften anderer Häuser → Instrument Sans."""
    css = re.sub(r"(Prata|Fraunces|LibreBaskerville)-[A-Za-z]+\.ttf", 'FjallaOne-Regular.ttf', css)
    css = re.sub(r"(HankenGrotesk|Urbanist)-(Regular)\.ttf", 'InstrumentSans-Regular.ttf', css)
    css = re.sub(r"(HankenGrotesk|Urbanist)-(Medium)\.ttf", 'InstrumentSans-Medium.ttf', css)
    css = re.sub(r"(HankenGrotesk|Urbanist)-(SemiBold|Bold)\.ttf", 'InstrumentSans-SemiBold.ttf', css)
    for alt in ("'Prata'", "'Fraunces'", "'Baskerville CE'"):
        css = css.replace(alt, "'Fjalla One'")
    for alt in ("'Hanken Grotesk'", "'Urbanist'"):
        css = css.replace(alt, "'Instrument Sans'")
    return css


def bau():
    os.makedirs(Z, exist_ok=True)
    for f in os.listdir(Z):   # Schnitte anderer Häuser weg
        if f.endswith('.ttf') and f not in DATEIEN:
            os.remove(os.path.join(Z, f))
    for quelle, ziel, fam, stil, g in SCHNITTE:
        f = TTFont(os.path.join(Q, quelle))
        if 'fvar' in f:
            f = instancer.instantiateVariableFont(f, {'wght': g}, inplace=False)
        for rec in f['name'].names:
            if rec.nameID in (1, 16): rec.string = fam
            if rec.nameID in (2, 17): rec.string = stil
            if rec.nameID == 4: rec.string = f'{fam} {stil}'
            if rec.nameID == 6: rec.string = f'{fam.replace(" ", "")}-{stil}'
        f['OS/2'].usWeightClass = g
        f.flavor = None
        f.save(os.path.join(Z, ziel + '.ttf'))
        print(ziel + '.ttf', 'fest')


if __name__ == '__main__':
    bau()
