#!/usr/bin/env python3
"""Werkbank Monte-Moro: «Heute und neu». Als «heute» dient die Aufnahme der heutigen Startseite von monte-moro.ch durch den Analysten
(_kette/04-analyst/_bau/stellen/d8.1.png, 1440 × 900, 17.10.2026), als «neu» die Aufnahme der neuen Seite (ansichten/Rechner, ansicht_lang.js).
Nichts wird online abgerufen.   python3 _werkbank/sb_heute.py  → ansichten/Vorher/<slug>-alt.jpg und <slug>-neu.jpg (gelesen von H.VORHER im Kit-Bau)"""
import os
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(W)))
SP = os.path.join(PROJ, '_kette', '04-analyst', '_bau', 'stellen')
Z = os.path.join(W, 'ansichten', 'Vorher')
PAARE = [('startseite', 'd8.1.png', 'Rechner/Startseite.jpg')]


def bau():
    os.makedirs(Z, exist_ok=True)
    os.makedirs(os.path.join(W, 'ansichten', 'Heute'), exist_ok=True)   # der Kit zeigt den Vergleich nur, wenn es «heute» gibt
    for slug, alt, neu in PAARE:
        a, n = os.path.join(SP, alt), os.path.join(W, 'ansichten', neu)
        if not (os.path.exists(a) and os.path.exists(n)):
            print('fehlt', slug); continue
        im = Image.open(n).convert('RGB')
        if im.width < 2880:   # beide Hälften gleich gross, sonst springt der Schieber
            im = im.resize((2880, round(im.height * 2880 / im.width)), Image.LANCZOS)
        im.save(os.path.join(Z, slug + '-neu.jpg'), quality=90)
        al = Image.open(a).convert('RGB').resize((im.width, im.height), Image.LANCZOS)
        al.save(os.path.join(Z, slug + '-alt.jpg'), quality=90)
        if slug == 'startseite':
            al.save(os.path.join(W, 'ansichten', 'Heute', 'Startseite.jpg'), quality=90)
        print('Vorher', slug)


if __name__ == '__main__':
    bau()
