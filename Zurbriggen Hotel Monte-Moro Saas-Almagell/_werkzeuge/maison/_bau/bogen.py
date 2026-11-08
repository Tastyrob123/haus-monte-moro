#!/usr/bin/env python3
"""Kontaktbogen von Fotos der Website (zum Auswählen, mm-maison): python3 bogen.py <ausgabe.png> schluessel1 schluessel2 …"""
import os, sys
from PIL import Image, ImageDraw
WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'website', 'assets', 'img')
aus, keys = sys.argv[1], sys.argv[2:]
b, h = 300, 260
bogen = Image.new('RGB', (b * 5, h * ((len(keys) + 4) // 5)), 'white')
d = ImageDraw.Draw(bogen)
for i, k in enumerate(keys):
    im = Image.open(os.path.join(WEB, k + '-s.webp')).convert('RGB')
    im.thumbnail((b - 10, h - 30))
    x, y = (i % 5) * b, (i // 5) * h
    bogen.paste(im, (x + 5, y + 5))
    d.text((x + 5, y + h - 22), f'{k} {im.size}', fill='black')
bogen.save(aus)
