#!/usr/bin/env python3
"""Karten & Preislisten · Hotel Monte-Moro, Saas-Almagell: feste Schnitte für den PDF-Satz (08.11.2026, Muster des Stamms).
Chromium bettet variable Schriften im PDF als «Type 3» ein; die Apple-Vorschau zeigt sie dann weich (Fehlerbuch 10a, 21.10.2026). Darum setzt der
Satz feste Schnitte (TrueType je Stärke, Lizenz SIL OFL wie das Original). Quelle: die Schriften der Website (website/assets/fonts/, woff2):
  · Fjalla One 400 (Titel, eine Stärke)
  · Instrument Sans 400 und 500 (Lauf; die Datei der Website ist variabel 400–600 → fest)
  · DM Mono 400 (Etiketten, Preise)
Geprüft wird, dass jedes Zeichen der Karten in jedem Schnitt steht (sonst fiele der Druck still auf eine Ersatzschrift).

    python3 _werkzeuge/carte/fonts_statisch.py
"""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
Q = os.path.join(HAUS, 'website', 'assets', 'fonts')
F = os.path.join(HIER, 'fonts')
FEST = [('FjallaOne-400.woff2', 'FjallaOne-400'), ('DMMono-normal-400.woff2', 'DMMono-400')]
VARIABEL = [('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-400', 400), ('InstrumentSans-normal-400_600.woff2', 'InstrumentSans-500', 500)]


def zeichen_der_karten():
    qd = os.path.join(HIER, '_daten', 'quelle')
    s = set()
    for f in os.listdir(qd):
        if f.endswith('.json'):
            s |= set(open(os.path.join(qd, f), encoding='utf-8').read())
    return {c for c in s if ord(c) > 32 and c not in '{}[]"\\'}


if __name__ == '__main__':
    os.makedirs(F, exist_ok=True)
    for f in os.listdir(F):
        if f.endswith('.ttf'):
            os.remove(os.path.join(F, f))
    for quelle, name in FEST:
        t = TTFont(os.path.join(Q, quelle))
        t.flavor = None
        t.save(os.path.join(F, name + '.ttf'))
        print(name)
    for quelle, name, w in VARIABEL:
        t = TTFont(os.path.join(Q, quelle))
        s = instancer.instantiateVariableFont(t, {'wght': w}, updateFontNames=False)
        s.flavor = None
        s.save(os.path.join(F, name + '.ttf'))
        print(name)
    fehlt = {}
    zz = zeichen_der_karten()
    for f in sorted(os.listdir(F)):
        cmap = TTFont(os.path.join(F, f)).getBestCmap()
        x = sorted(c for c in zz if ord(c) not in cmap)
        if x:
            fehlt[f] = ''.join(x)
    print('Zeichen der Karten in jedem Schnitt:', 'ja' if not fehlt else json.dumps(fehlt, ensure_ascii=False))
    if fehlt and 'FjallaOne-400.ttf' not in fehlt and 'InstrumentSans-400.ttf' not in fehlt:
        sys.exit(0)
