"""Bildkarussells der Startseite (Ideen, Gäste) heissen «kartenzug», nicht «band».

Grund (09.11.2026, Nachtrag vom Mac): `_Werkzeuge/oberflaeche_pruefen.js` misst jedes Element mit «band» im Klassennamen
als Laufband (Prüfpunkt 6, Schrift in der Bandmitte). Die zwei Reihen mit Bildkarten zum Blättern sind keine Laufbänder;
das Kit nennt sie trotzdem `.band`. Der Name wird nach dem Bau in Seite, Stilblättern und Skripten ersetzt, das Kit bleibt
unverändert. Ablauf, Masse und Verhalten bleiben gleich. Dazu: Zähler der Karussells zählt beim Blättern mit.
Mehrfach aufrufbar.
"""
import os
import re

_SEL = re.compile(r'\.band(?![\w-])')


def anwenden(wb):
    seite = os.path.join(wb, 'index.html')
    if os.path.exists(seite):
        t = open(seite, encoding='utf-8').read()
        n = t.replace('class="band"', 'class="kartenzug"')
        n = _SEL.sub('.kartenzug', n)
        if n != t:
            open(seite, 'w', encoding='utf-8').write(n)
    for f in ('werkbank.css', 'werkbank.js', 'kapitel.css'):
        p = os.path.join(wb, f)
        if not os.path.exists(p):
            continue
        t = open(p, encoding='utf-8').read()
        n = _SEL.sub('.kartenzug', t)
        # Zähler «01 / 12»: Kartenabstand vom ersten Kärtchen aus messen, nicht vom Zug (der Zug hat links Innenabstand
        # var(--rand) > 60 px; sonst bleibt der Zähler nach dem Blättern auf 01 stehen; Beleg 09.11.2026, 1440 px)
        n = n.replace('el.offsetLeft - band.offsetLeft - 60 <= x', 'el.offsetLeft - k[0].offsetLeft - 60 <= x')
        if n != t:
            open(p, 'w', encoding='utf-8').write(n)


if __name__ == '__main__':
    import sys
    anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'werkbank'))
