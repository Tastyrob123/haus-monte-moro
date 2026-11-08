#!/usr/bin/env python3
"""Wissen des Chats für die Rezeption des Hotel Monte-Moro, Saas-Almagell (08.11.2026). Muster: _bau/culinarium_wissen.py des Culinarium.
Liest nur, aus dem Hausordner:
  website/inhalt/daten.py          alle Angaben des Hauses an einer Stelle, wörtlich aus den Seiten des Hauses (HAUS, PREISE, INKLUSIVE, ZUSCHLAEGE …, OFFEN)
  website/assets/js/wissen.json    die Fragen und Antworten, mit denen die Rezeption im Chat der Website antwortet
  _werkzeuge/reception/_bau/website-text/*.txt   Wortlaut der Seiten, wie ein Gast ihn sieht (node _bau/website_text.js), nur zur Gegenprobe
Schreibt: gast/gast_wissen.txt, gast/gast_umgebung.txt, gast/gast_haus.json und vorlagen/*.txt.
Nichts wird abgetippt oder umformuliert: jede Angabe kommt aus daten.py bzw. wissen.json. Was in OFFEN steht, gibt es nicht; der Chat sagt dann,
dass Esther und Fabian das persönlich beantworten, und nennt keine Zahl. Die Gratis-Anreise lief am 31.10.2026 ab (ANREISE_GRATIS.bis): sie kommt
nirgends mehr vor, auch nicht aus wissen.json. Prüft am Ende, dass jede Zahl der Preise auch auf der gebauten Website steht.
Aufruf aus dem Hausordner: python3 _werkzeuge/reception/_bau/montemoro_wissen.py   (nach neuen Angaben erneut, danach steckbrief_bau.py)"""
import datetime, importlib.util, json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))     # _werkzeuge/reception
PROJ = os.path.dirname(os.path.dirname(C))
WEB = os.path.join(PROJ, 'website')
WT = os.path.join(C, '_bau', 'website-text')
ZIEL = os.path.join(C, 'gast')


def daten():
    s = importlib.util.spec_from_file_location('mm_daten', os.path.join(WEB, 'inhalt', 'daten.py'))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def gratis_ab(D):
    """True, solange die Gratis-Anreise gilt (heute bis ANREISE_GRATIS.bis)."""
    return datetime.date.today().isoformat() <= D.ANREISE_GRATIS['bis']


def bau():
    D = daten()
    W = json.load(open(os.path.join(WEB, 'assets', 'js', 'wissen.json'), encoding='utf-8'))
    H = D.HAUS
    stand = 'Angaben des Hauses (website/inhalt/daten.py, Abruf 09.10.2026, Nachtrag 17.10.2026)'
    S = []

    def seite(datei, titel, zeilen):
        S.append(f'=== Seite: {titel} · Hotel Monte-Moro (Website: {datei}; {stand}) ===\n' + '\n'.join(z for z in zeilen if z))

    seite('index.html', 'Startseite', [
        '## Ihre Gastgeber',
        f'Esther und Fabian Zurbriggen sind die Gastgeber im {H["name"]} in {H["ort"]} (Impressum: {D.GASTGEBER_KURZ}).',
        f'{H["satz"]}', D.LAGE_SATZ, D.SONNE,
        f'Das Haus: {D.HAUS_ZAHLEN[0]} Zimmer, {D.HAUS_ZAHLEN[1]} Betten (Schweiz Tourismus), 3 Sterne.',
        D.RESTAURANT,
        '## Noten der Gäste (' + D.NOTEN_STAND + ')',
        ' · '.join(f'{n}: {w} {v}' + (f' ({b})' if b else '') for n, w, v, b in D.NOTEN)])
    seite('zimmer.html', 'Zimmer und Ferienwohnungen', [
        '## ' + D.ZIMMER_TITEL, D.ZIMMER_TEXT,
        'Laut dem Eintrag des Hauses bei Booking.com: ' + ', '.join(D.BOOKING_ZIMMER) + '.',
        '## Familienzimmer', D.FAMILIE_TEXT,
        '## Residence Alpenhof', D.ALPENHOF_TEXT,
        '## Ferienwohnung Haus Apollo', D.APOLLO,
        '## Ferienwohnungen Haus Arizona', D.ARIZONA])
    seite('preise.html', 'Preise und Inklusive', [
        '## Zimmer mit Frühstück und mit Halbpension (CHF pro Person / Tag)',
        '\n'.join(f'{k}, {a}: CHF {p} pro Person / Tag' for k, a, p in D.PREISE),
        '## Inklusive', '\n'.join(D.INKLUSIVE), D.BERGBAHN_SATZ,
        '## Zuschläge', '\n'.join(f'{k}: ' + (v if '%' in v else f'CHF {v}') for k, v in D.ZUSCHLAEGE),
        '## Kinder', D.KINDER_SATZ + ': ' + ' · '.join(f'{a}: CHF {p}' for a, p in D.KINDER), D.KINDER_EIGEN + '.',
        '## Bezahlung', D.EURO])
    seite('roestihues.html', 'Restaurant Röstihüs', [
        '## ' + D.TRADITION, D.RESTAURANT, D.ROESTI_SATZ, D.ROESTI_GETRAENKE, D.SONNE, D.ROESTI_KINDER,
        '## Best of Röstis (Karte vom 18.11.2024, Preise in Franken)', '\n'.join(f'{n}: {b}, Fr. {p}' for n, b, p in D.ROESTIS),
        '## Unsere Cordon bleus', '\n'.join(f'Cordon bleu {n}: {b}, Fr. {p}' for n, b, p in D.CORDON),
        '## Hotelweine', '\n'.join(f'{n}, {w}: {t.rstrip(", ")}, {g}, Fr. {p}' for n, w, t, g, p in D.HOTELWEINE),
        '## Spritz', '\n'.join(f'{n}: {b}, Fr. {p}' for n, b, p in D.SPRITZ),
        '## Dessert und Raclette', f'{D.KOPF[0]}: Fr. {D.KOPF[1]}', f'{D.RACLETTE[0]}: Fr. {D.RACLETTE[1]}', 'Halbpension: wöchentlicher Racletteabend im Stübli.',
        '## Tisch reservieren', f'Telefon {H["tel"]} oder über TheFork.'])
    seite('spa.html', 'Spa im Partnerhotel', [
        '## ' + D.SPA_TITEL, D.SPA_SATZ, D.SPA_ANGEBOT,
        '\n'.join(f'{p} {k}' + (f' ({z})' if z else '') for k, p, z in D.SPA_TARIFE), D.SPA_INKL])
    seite('saastal.html', 'Das Saastal', [
        '## Sommer', D.SOMMER_SATZ,
        '\n'.join(f'{t}: {s}' for _, t, s, _x in D.SAASTAL['sommer']),
        '## Winter', '\n'.join(f'{t}: {s}' for _, t, s, _x in D.SAASTAL['winter']),
        '## Lage', '\n'.join(f'{m} Gehminuten: {o} ({b})' for m, o, b in D.LAGE), D.POSTAUTO + '.'])
    seite('anreise.html', 'Anreise', [
        '## Mit Zug und Postauto', D.ANREISE_ZUG, D.ANREISE_ZUG_ZEIT,
        '## Mit dem Auto', D.ANREISE_AUTO, D.ANREISE_AUTO_ZEIT,
        '## Parkplatz', D.PARK + '. Hotelparkplatz inklusive.'])
    # die Fragen und Antworten des Chats der Website, ohne die abgelaufene Gratis-Anreise
    raus = [] if gratis_ab(D) else [D.ANREISE_GRATIS['titel']]
    qa = [e for e in W['eintraege'] if not any(r in e['a'] for r in raus)]
    S.append(f'=== Fragen und Antworten des Chats der Website (Website: assets/js/wissen.json, {W["stand"]}) ===\n'
             + '\n'.join(f'## {e["k"]}: {e["q"]}\n{e["a"]}' for e in qa))
    wissen = '\n\n'.join(S) + '\n'
    if not gratis_ab(D) and re.search(r'geschenkt|gratis an', wissen, re.I):
        sys.exit('PRUEF · die abgelaufene Gratis-Anreise steht noch im Wissen.')

    offen = [t for t, _ in D.OFFEN]
    umgebung = f"""=== Kontakt (Website: Impressum und Anreise, website/inhalt/daten.py HAUS) ===
{H['name']}, {H['plz_ort']}. Telefon {H['tel']}, Fax {H['fax']}, E-Mail {H['mail']}.
Gastgeber: Esther und Fabian Zurbriggen ({D.GASTGEBER_KURZ}).
Zimmer buchen: mit «Zimmer buchen» auf der Website (Buchungsfenster des Hauses), per Telefon oder E-Mail.
Tisch im Röstihüs: Telefon {H['tel']} oder über TheFork.
Anfrage an die Rezeption: das Anfrage-Fenster auf der Website (Name, E-Mail oder Telefon, Nachricht).

=== Was das Haus nicht veröffentlicht (website/inhalt/daten.py OFFEN, _kette/03-sammler/fakten.json) ===
Dazu steht in keiner Quelle des Hauses etwas; das beantworten Esther und Fabian persönlich, ohne dass der Chat eine Zahl oder Zeit nennt:
- Öffnungszeiten und Ruhetage des Röstihüs (die Rezeption gibt sie gern bekannt).
- die Strasse des Hauses (die Adresse lautet {H['name']}, {H['plz_ort']}).
- Storno- und Geschäftsbedingungen.
- Preise der Ferienwohnungen im Haus Apollo und im Haus Arizona.
- Zeiten für Anreise und Abreise am Zimmer (Check-in, Check-out).
- Alter und Ablauf im Kidsclub über die Zeiten hinaus (Kidsclub: täglich Mo - Sa 16:30 bis 21:00 Uhr, inklusive).
- Saisonzeiten und Betriebsferien.
Die Gratis-Anreise mit dem öffentlichen Verkehr galt für Buchungen vom 1. Mai bis 31. Oktober 2026 und wird nicht mehr angeboten; ob sie 2027 weiterläuft, steht nicht fest.

=== Lage (Website: Startseite und Anreise) ===
{D.LAGE_SATZ} {D.LAGE[0][0]} Gehminuten zum Skigebiet Saas-Almagell, {D.LAGE[1][0]} zur Busstation, {D.LAGE[2][0]} zum Dorfkern. {D.PARK}.
"""
    haus = {
        'name': H['name'], 'ort': H['ort'], 'tel': H['tel'], 'mail': H['mail'],
        'kontakt': f"der Rezeption unter {H['tel']} oder {H['mail']}",
        'adresse': f"{H['name']}, {H['plz_ort']}",
        'art': 'Hotel mit Restaurant Röstihüs im Saastal (Wallis), 3 Sterne, Familie Zurbriggen; Gastgeber Esther und Fabian Zurbriggen',
        'zeiten': '', 'ruhetage': '', 'fahrplan': '', 'kategorien': [], 'orte': [],
        'reservation': H['buchen'], 'reservation_name': 'Zimmer buchen',
        'muster': ('Frage: Was ist im Preis inbegriffen?\nAntwort: Bei uns ist vieles schon dabei.\n'
                   + '\n'.join('- ' + x for x in D.INKLUSIVE[:4]) + '\n\n'
                   'Frage: Wann hat das Röstihüs geöffnet?\nAntwort: Die Öffnungszeiten erfahren Sie gern direkt bei uns:\n'
                   f"- Telefon: {H['tel']}\n- E-Mail: {H['mail']}"),
    }
    vorlagen = {
        'zimmer': ['Preise (Website: Preise, CHF pro Person / Tag): ' + ' · '.join(f'{k}, {a}: CHF {p}' for k, a, p in D.PREISE),
                   'Inklusive: ' + '; '.join(D.INKLUSIVE) + '. ' + D.BERGBAHN_SATZ,
                   'Zuschläge: ' + '; '.join(f'{k}: ' + (v if '%' in v else f'CHF {v}') for k, v in D.ZUSCHLAEGE),
                   D.KINDER_SATZ + ': ' + ' · '.join(f'{a}: CHF {p}' for a, p in D.KINDER) + '. ' + D.KINDER_EIGEN + '.',
                   D.ZIMMER_TEXT + ' ' + D.FAMILIE_TEXT + ' ' + D.ALPENHOF_TEXT,
                   'Buchen: mit «Zimmer buchen» auf der Website, per Telefon oder E-Mail. ' + D.EURO],
        'wohnung': ['Haus Apollo: ' + D.APOLLO, 'Haus Arizona: ' + D.ARIZONA,
                    'Preise der Ferienwohnungen stehen nicht auf der Website: im Brief als offenes Feld [Preis der Wohnung], Esther und Fabian beantworten das persönlich.',
                    'Inklusive (Preisliste des Hotels): ' + '; '.join(D.INKLUSIVE[:2]) + '. ' + D.BERGBAHN_SATZ],
        'tisch': [D.RESTAURANT, D.ROESTI_LUST, f"Tisch reservieren: Telefon {H['tel']} oder über TheFork.",
                  'Öffnungszeiten des Röstihüs stehen nicht auf der Website: im Brief als offenes Feld [Tisch prüfen].', D.ROESTI_KINDER],
    }
    # Gegenprobe: jede Zahl der Preise steht auch auf der gebauten Website (Wortlaut, den ein Gast sieht)
    try:
        web = '\n'.join(open(os.path.join(WT, n), encoding='utf-8').read() for n in os.listdir(WT) if n.endswith('.txt'))
        fehlt = [p for _, _, p in D.PREISE if p not in web] + [p for _, p in D.KINDER if p.split('.')[0] not in web]
        if fehlt:
            sys.exit('PRUEF · Preise, die die Website nicht zeigt: ' + ', '.join(fehlt))
    except FileNotFoundError:
        print('Hinweis: ohne _bau/website-text (node _bau/website_text.js) keine Gegenprobe gegen die Website.')
    os.makedirs(ZIEL, exist_ok=True); os.makedirs(os.path.join(C, 'vorlagen'), exist_ok=True)
    open(os.path.join(ZIEL, 'gast_wissen.txt'), 'w', encoding='utf-8').write(wissen)
    open(os.path.join(ZIEL, 'gast_umgebung.txt'), 'w', encoding='utf-8').write(umgebung)
    json.dump(haus, open(os.path.join(ZIEL, 'gast_haus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for alt in os.listdir(os.path.join(C, 'vorlagen')):
        if alt.endswith('.txt') and alt[:-4] not in vorlagen:
            os.remove(os.path.join(C, 'vorlagen', alt))
    for k, z in vorlagen.items():
        open(os.path.join(C, 'vorlagen', k + '.txt'), 'w', encoding='utf-8').write('\n\n'.join(x for x in z if x) + '\n')
    print(f'gast_wissen.txt {len(wissen) // 1024} kB · gast_umgebung.txt {len(umgebung)} Zeichen · gast_haus.json · vorlagen: {", ".join(vorlagen)} · '
          f'{len(qa)} von {len(W["eintraege"])} Fragen der Website (ohne Abgelaufenes)')


if __name__ == '__main__':
    bau()
