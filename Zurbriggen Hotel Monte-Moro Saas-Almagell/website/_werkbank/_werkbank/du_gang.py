#!/usr/bin/env python3
"""Werkbank Monte-Moro: Sie-Form und Schweizer Schreibung (Werkbank Kern, 08.11.2026). Kit und Stamm sprechen im Sie und schreiben «ss»; die Werkbank
spricht Esther und Fabian Zurbriggen im Sie an. Läuft als letzter Text-Schritt nach jedem Bau über die gebauten Seiten des Kerns (nur Text, nie Adressen,
Skripte oder Bilder): ß wird ss, ein paar Wendungen der Vorlage, die fürs Hotel nicht stimmen, werden ersetzt. Der Suchlauf am Ende meldet, was danach
noch nach Du/Ihr-Form, ß oder fremdem Haus klingt. Mehrfach anwendbar.   python3 _werkbank/du_gang.py"""
import glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
KERN = ('werkbank', 'befund')   # nur die Seiten des Kerns (die Papier-Seiten macht Werkbank Papier)
ERSATZ = [   # (alt, neu) ganze Wendungen des Kits, die fürs Haus nicht stimmen
    ('ß', 'ss'),
    ('Adresse, Telefon, Reservation, Karte und Öffnungszeiten werden beim Freigeben', 'Adresse, Telefon, Zimmer, Preise und die Karte des Röstihüs werden beim Freigeben'),
]


def seiten():
    for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        r = os.path.relpath(p, ROOT)
        if r.split(os.sep)[0] in KERN:
            yield p


def text_teile(t, f):
    """Wendet f nur auf Text zwischen Tags an (nicht in <script>, <style>, Attributen)."""
    teile = re.split(r'(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', t, flags=re.S)
    return ''.join(x if (x.startswith('<')) else f(x) for x in teile)


def attribute(t):
    """Dieselben Wendungen in alt, aria-label, title und content."""
    return re.sub(r'((?:alt|aria-label|title|content)=")([^"]*)(")', lambda m: m.group(1) + umformen(m.group(2)) + m.group(3), t)


def umformen(s):
    for a, n in ERSATZ:
        s = s.replace(a, n)
    return s


def anwenden():
    n = 0
    for p in seiten():
        a = open(p, encoding='utf-8').read()
        b = attribute(text_teile(a, umformen))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


FREMD = r'wild ?side|culinarium|rudi\b|momo|derya|linden|hannover|haasemann|prata|hanken|fraunces|urbanist|\bDJ\b|session|cocktail|negroni|Beau-Rivage|Schäfli|Schlössli|Theke|Eckschild|Plakatwerkstatt|Pairing'


def suchlauf():
    """Was danach noch nach Du/Ihr, ß oder fremdem Haus klingt (Text und Attribute), zur Prüfung."""
    import html as _h
    aus = set()
    for p in seiten():
        t = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', '', open(p, encoding='utf-8').read(), flags=re.S)
        t = re.sub(r'(?:alt|aria-label|title|content)="([^"]*)"', lambda m: '>' + m.group(1) + '<', t)
        for z in _h.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n'):
            if re.search(r'ß|\b(euch|eure[mnrs]?|euer|ihr habt|ihr könnt|dein[em]?|du)\b|' + FREMD, z, re.I):
                aus.add((os.path.relpath(p, ROOT), z.strip()[:200]))
    return sorted(aus)


if __name__ == '__main__':
    print('Schweizer Schreibung:', anwenden(), 'Seiten')
    for x in suchlauf():
        print(*x, sep=' | ')
