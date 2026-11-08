"""Töne und Schriften der Bar (Wild Side) auf die des Hotel Monte-Moro (kleid/montemoro.css, Markenbuch farben.json):
python3 _bau/farben.py <datei> …   ersetzt feste Werte, die nicht über --wo-* laufen (Rundgang-Karte, Schatten, Haarlinien)."""
import re, sys
TABELLE = [
    # Tinte der Bar → Tinte des Hauses #13263A; Nacht der Bar → Tiefnacht #071B2E; Gold → Messing #B39867; Gold tief → Lärche tief #9A4F2B; Rot → Lärche #C67144
    (r'rgba\(\s*28\s*,\s*21\s*,\s*19\s*,', 'rgba(19,38,58,'),
    (r'rgba\(\s*19\s*,\s*14\s*,\s*13\s*,', 'rgba(7,27,46,'),
    (r'rgba\(\s*216\s*,\s*178\s*,\s*100\s*,', 'rgba(179,152,103,'),
    (r'rgba\(\s*122\s*,\s*92\s*,\s*36\s*,', 'rgba(154,79,43,'),
    (r'rgba\(\s*240\s*,\s*50\s*,\s*63\s*,', 'rgba(198,113,68,'),
    (r'#7A5C24', '#9A4F2B'), (r'#D8B264', '#B39867'), (r'#E4C88A', '#C67144'), (r'#F1E2BE', '#F5F2EE'),
    (r'#1C1513', '#13263A'), (r'#130E0D', '#071B2E'), (r'#261E1A', '#0D3F6F'), (r'#F2E9DC', '#F5F2EE'), (r'#FFFBF5', '#FFFFFF'),
    (r'#F7F1E7', '#F5F2EE'), (r'#EFE6D8', '#EFE9E1'), (r'#8C7F72', '#4A5D70'), (r'#F0323F', '#C67144'), (r'#5E524A', '#4A5D70'),
    # Schriften: Prata → Fjalla One (Titel, eine Stärke); Hanken in Etiketten (500, Versalien) → DM Mono 400; Hanken im Lauf → Instrument Sans
    (r'400 (\d+(?:\.\d+)?px/[\d.]+) Prata,Georgia,serif', r'400 \1 "Fjalla One","Arial Narrow",Arial,sans-serif'),
    (r'500 (\d+(?:\.\d+)?px/1) Hanken,"Helvetica Neue",Arial,sans-serif', r'400 \1 "DM Mono",ui-monospace,Menlo,monospace'),
    (r'(\d+px/1\.55) Hanken,"Helvetica Neue",Arial,sans-serif', r'\1 "Instrument Sans",Arial,system-ui,sans-serif'),
]
for p in sys.argv[1:]:
    t = open(p, encoding='utf-8').read()
    n = 0
    for a, b in TABELLE:
        t, k = re.subn(a, b, t, flags=re.I)
        n += k
    open(p, 'w', encoding='utf-8').write(t)
    print(p, n, 'Stellen')
