#!/usr/bin/env python3
"""Werkbank: Texte in den Foto-Fenstern (.wfen) und im Schluss (.schluss) gut lesbar (Robert 10.11.2026: «die Texte in den Fenstern noch besser
lesbar machen … die gehen so ein bisschen unter im Hintergrund … bei mehreren Häusern»). Hinter dem Text liegt ein weicher, runder Schatten auf dem
Foto (radialer Verlauf ohne Kante, kein Kasten), die Schrift selbst behält ihren feinen Schatten. Läuft am Ende von haus.nach_bau über alle Seiten der
Werkbank, wiederholbar.   python3 _werkbank/fenster_lesbar.py [<werkbank-root>]"""
import glob, os, re, sys

CSS = (".wfen__in::before{content:'';position:absolute;left:50%;top:50%;z-index:-1;width:min(1180px,100%);height:calc(100% + clamp(160px,22vw,320px));"
       "transform:translate(-50%,-50%);pointer-events:none;"
       "background:radial-gradient(closest-side,rgba(8,9,16,.66),rgba(8,9,16,.46) 55%,rgba(8,9,16,.18) 82%,rgba(8,9,16,0))}"
       ".schluss .in{position:relative;isolation:isolate}"
       ".schluss .in::before{content:'';position:absolute;left:50%;top:50%;z-index:-1;width:min(1240px,100%);height:calc(100% + clamp(120px,16vw,240px));"
       "transform:translate(-50%,-50%);pointer-events:none;"
       "background:radial-gradient(closest-side,rgba(8,9,16,.6),rgba(8,9,16,.4) 55%,rgba(8,9,16,.14) 82%,rgba(8,9,16,0))}")
BLOCK = '<style id="fenster-lesbar">' + CSS + '</style>'


def anwenden(root):
    n = 0
    for f in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
        rel = os.path.relpath(f, root)
        if rel.startswith(('_werkbank', '_sicherung', 'node_modules')) or '.vor-' in rel:
            continue
        s = open(f, encoding='utf-8').read()
        if ('class="wfen' not in s and 'class="schluss' not in s) or '</body>' not in s:
            continue
        s = re.sub(r'<style id="fenster-lesbar">.*?</style>', '', s, flags=re.S)
        i = s.rfind('</body>'); s = s[:i] + BLOCK + s[i:]
        open(f, 'w', encoding='utf-8').write(s); n += 1
    return n


if __name__ == '__main__':
    print('fenster-lesbar:', anwenden(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Seiten')
