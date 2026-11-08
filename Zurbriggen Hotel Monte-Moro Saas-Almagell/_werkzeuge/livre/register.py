#!/usr/bin/env python3
"""Das Markenbuch · Hotel Monte-Moro: liest das Bildregister der Website (BILDER in website/inhalt/bilder.py), ohne die Datei auszuführen.
Je Schlüssel (Quelle relativ zu _quelle/, Beschreibung); Masse und die wirklich gebaute Quelle stehen in website/assets/img/_masse.json."""
import ast, os

HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJEKT, 'website')


def lesen():
    """{schlüssel: (quelle, beschreibung)} wie BILDER in website/inhalt/bilder.py."""
    baum = ast.parse(open(os.path.join(WEB, 'inhalt', 'bilder.py'), encoding='utf-8').read())
    for n in baum.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'BILDER':
            return ast.literal_eval(n.value)
    raise SystemExit('BILDER fehlt in website/inhalt/bilder.py, erst klären')


if __name__ == '__main__':
    print(len(lesen()), 'Einträge')
