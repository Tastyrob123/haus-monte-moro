"""Kleid Monte-Moro, zuletzt nach jedem Bau (haus.nach_bau): Schriftfamilien der Vorlagen heissen nach den Schriften der Website (Fjalla One,
Instrument Sans, DM Mono), Farbreste der Vorlagen werden zu den Tönen des Hauses, und die Leiste der Unterseiten (Kit «rahmen») trägt den breiten
Bergkamm in der Lärche, ohne am Handy überzulaufen. Wiederholbar, ändert nur Ausgaben des Kerns in werkbank/ und befund/. Werkbank Kern, 08.11.2026."""
import os
import re

TAUSCH = [
    ("'Prata'", "'Fjalla One'"), ('"Prata"', '"Fjalla One"'), ("'Fraunces'", "'Fjalla One'"), ('"Fraunces"', '"Fjalla One"'),
    ('font-family="Prata', 'font-family="Fjalla One'), ('font-family="Fraunces', 'font-family="Fjalla One'),
    ("'Hanken Etikett'", "'DM Mono'"), ("'Hanken Grotesk'", "'Instrument Sans'"), ('"Hanken Grotesk"', '"Instrument Sans"'),
    ('font-family="Hanken Grotesk', 'font-family="Instrument Sans'), ("'Urbanist'", "'Instrument Sans'"),
    ('Georgia,serif', "'Arial Narrow',sans-serif"),
]
FARBE = {'d8b264': 'c67144', 'f0323f': 'c67144', '130e0d': '0a2a4a', '1c1513': '082339', 'f2e9dc': 'f5f2ee', 'ef7649': 'c67144', '16141b': '0a2a4a', 'dcc68f': 'c67144'}

# Leiste der Unterseiten (Kit rahmen): Bergkamm breit statt quadratisch, in Lärche; am Handy ohne Seitennamen, nichts läuft über
LEISTE_CSS = ('<style id="mm-leiste">.insel__m svg{height:18px!important;width:auto!important;aspect-ratio:3483/696;color:#c67144!important;fill:currentColor}'
              '.insel__m span{color:#c67144}'
              '@media(max-width:600px){.insel__m span,.insel__m b{display:none!important}.insel{gap:10px!important}.insel .glanz{white-space:nowrap}}</style>')


def _farben(t):
    t = t.replace('rgba(216,178,100,', 'rgba(179,152,103,').replace('rgba(19,14,13,', 'rgba(10,42,74,').replace('rgba(239,118,73,', 'rgba(198,113,68,')
    return re.sub(r'#(' + '|'.join(FARBE) + r')\b', lambda m: '#' + FARBE[m.group(1).lower()], t, flags=re.I)


def anwenden(root):
    for ordner in ('werkbank', 'befund'):
        for dp, dn, fn in os.walk(os.path.join(root, ordner)):
            for f in fn:
                if not f.endswith(('.html', '.css', '.js', '.svg')):
                    continue
                p = os.path.join(dp, f)
                try:
                    t = open(p, encoding='utf-8').read()
                except UnicodeDecodeError:
                    continue
                n = t
                for a, b in TAUSCH:
                    n = n.replace(a, b)
                n = _farben(n)
                if f.endswith(('.js', '.css')):
                    n = n.replace('\u00df', 'ss')   # Schweizer Schreibung auch in Kommentaren der Kit-Dateien
                if f.endswith('.html'):
                    if not p.endswith(os.path.join('werkbank', 'index.html')):
                        n = n.replace(' loading="lazy"', '')   # kleine Seiten: Bilder sofort laden
                    n = n.replace('>Zur Werkbank<svg', '>Zur Übersicht<svg')
                    if '</head>' in n:
                        n = re.sub(r'<style id="mm-leiste">.*?</style>', '', n, flags=re.S).replace('</head>', LEISTE_CSS + '</head>', 1)
                if n != t:
                    open(p, 'w', encoding='utf-8').write(n)


if __name__ == '__main__':
    anwenden(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
