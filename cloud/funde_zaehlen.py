#!/usr/bin/env python3
"""Zählt Zustände und Funde je Ziel eines tor-schnell-Laufs. Aufruf: python3 cloud/funde_zaehlen.py <ordner> [--json]"""
import glob, json, os, sys
D = sys.argv[1]; aus = {}
for inv in sorted(glob.glob(os.path.join(D, '*', 'inventar.json'))):
    k = os.path.basename(os.path.dirname(inv)); j = json.load(open(inv, encoding='utf-8'))
    z = len(j.get('zustaende', [])); f = []; ne = len(j.get('nichtErreicht', []) or [])
    for st in j.get('zustaende', []):
        for x in st.get('funde', []) or []: f.append(('1440', st.get('id'), x))
    for s in sorted(glob.glob(os.path.join(os.path.dirname(inv), 'stich-*.json'))):
        b = os.path.basename(s)[6:-5]; sj = json.load(open(s, encoding='utf-8'))
        for st in sj.get('zustaende', []):
            for x in st.get('funde', []) or []: f.append((b, st.get('id'), x))
    aus[k] = {'zustaende': z, 'funde': len(f), 'nicht_erreicht': ne, 'liste': f[:40]}
if '--json' in sys.argv: print(json.dumps(aus, ensure_ascii=False, indent=1))
else:
    for k, v in aus.items(): print(f"{k:28s} {v['zustaende']:4d} Zustände  {v['funde']:4d} Funde  {v['nicht_erreicht']} nicht erreicht")
