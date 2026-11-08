#!/usr/bin/env python3
"""Hotel Monte-Moro: sechs Mail-Vorlagen an Gäste, als Idee zum Entwurf (Werkbank Papier, 08.11.2026).
Bauart aus mails/_src/bau.py der Vorlage (Band mit «Ganze Mail»), Inhalt und Kleid des Hauses.

Die Fälle eines Hotels mit Restaurant: die Antwort auf eine Zimmeranfrage, das Angebot (Preise aus der Preisliste des Hauses gerechnet:
website/inhalt/daten.py PREISE, KINDER, ZUSCHLAEGE), die Bestätigung, «Vor Ihrer Anreise» (Zug und Postauto, Auto, Parkplatz aus ANREISE_*),
der Dank nach dem Aufenthalt und der Tisch im Röstihüs. Im Sie, Schweizer Schreibung. Absender «Hotel Monte-Moro», Gruss von Esther und
Fabian Zurbriggen. Fotos aus der Website (assets/img), unter 100 KB, mit Beschreibung aus bilder.py; Tabellen und feste Stile,
Titel in Fjalla One (Arial Narrow, wo ein Mailprogramm keine Schrift lädt), Lauf in Instrument Sans, kleine Zeilen in DM Mono.
Namen, Daten und Nummern der Gäste sind Beispielwerte und so beschriftet; Preise, Inklusive, Anreise und Kontakt sind die des Hauses.
Was das Haus nicht veröffentlicht (Öffnungszeiten des Röstihüs, Check-in-Zeit, Storno, Strasse), steht nicht darin. Gebaut, nie verschickt.

Aufruf:  python3 mails/_src/bau.py  → mails/NN-<fall>/index.html, mails/index.html, mails/img/;  danach WB_PORT=9388 node mails/_src/aufnahme.js"""
import html, json, os, re, glob, shutil, sys

HIER = os.path.dirname(os.path.abspath(__file__)); MAILS = os.path.dirname(HIER); ROOT = os.path.dirname(MAILS); WEB = os.path.dirname(ROOT)
from PIL import Image  # noqa: E402
sys.path.insert(0, os.path.join(WEB, 'inhalt'))
import daten as D  # noqa: E402  (nur gelesen)
from bilder import BILDER  # noqa: E402

TEL, MAIL_ADR, PLZ_ORT = D.HAUS['tel'], D.HAUS['mail'], D.HAUS['plz_ort']
ADRESSE = f'Hotel Monte-Moro · {PLZ_ORT}'
GRUSS = 'Esther und Fabian Zurbriggen'
BUCHEN = D.HAUS['buchen']
STAND = '08.11.2026'


def e(t):
    """escape; Zahl und Einheit bleiben zusammen"""
    return re.sub(r'(\d) (Uhr|%|Min\.|Nächte|Gäste)', '\\1&nbsp;\\2', html.escape(t)).replace('CHF ', 'CHF&nbsp;')


TIEF, NACHT, NACHT2, CREME, BLATT, TINTE, LEISE, MESSING, LAERCHE, LAERCHE_T, WAND = ('#071B2E', '#0A2A4A', '#0D3F6F', '#EFE9E1', '#F5F2EE', '#13263A', '#4A5D70',
                                                                                     '#B39867', '#C67144', '#9A4F2B', '#D6CCC1')
SERIF = "'Fjalla One','Arial Narrow',Arial,sans-serif"
SANS = "'Instrument Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'DM Mono',Menlo,Consolas,monospace"


def chf(x):
    return f'CHF {x:,.2f}'.replace(',', "'")


# ---------- das Angebot: aus der Preisliste gerechnet (Beispiel: zwei Erwachsene, ein Kind von 7 Jahren, Standardzimmer, Halbpension, 4 Nächte im Sommer)
NAECHTE = 4
P_HP = float([p for z, a, p in D.PREISE if z == 'Standardzimmer' and 'Halbpension' in a][0])
P_KIND = float(dict(D.KINDER)['7 Jahre'])
KT_E = float(dict(D.ZUSCHLAEGE)['Kurtaxe Erwachsene pro Tag (Sommer)'])
KT_K = float(dict(D.ZUSCHLAEGE)['Kurtaxe Kinder (6 - 16 Jahre) pro Tag (Sommer)'])
ZIMMER = 2 * P_HP * NAECHTE
KIND = P_KIND * NAECHTE
KURTAXE = (2 * KT_E + KT_K) * NAECHTE
SUMME = ZIMMER + KIND + KURTAXE
assert (P_HP, P_KIND, KT_E, KT_K) == (130.0, 70.0, 7.0, 3.5)
INKL = [i.replace(' - ', ' bis ').replace('Mo bis Sa', 'Montag bis Samstag') for i in D.INKLUSIVE]

AUFENTHALT = [('Anreise', 'Samstag, 10. Juli 2027'), ('Abreise', 'Mittwoch, 14. Juli 2027'), ('Gäste', '2 Erwachsene, 1 Kind (7 Jahre)'), ('Zimmer', 'Standardzimmer, Halbpension (4-Gänge)')]
FAELLE = [
    dict(nr='01', wann='Gleich nach einer Zimmeranfrage', ordner='01-anfrage', name='Ihre Anfrage ist da', satz='Kommt gleich nach der Anfrage über die Website: was angefragt ist, und dass das Angebot persönlich folgt.',
         betreff='Ihre Anfrage im Hotel Monte-Moro', titel=('Ihre Anfrage', 'ist angekommen.'), foto='z-hell', bsp=True,
         text=['Grüezi Frau Meier', 'Vielen Dank für Ihre Anfrage. Wir freuen uns, dass Sie Ferien in Saas-Almagell planen.',
               'Wir schauen uns Ihre Daten an und melden uns persönlich mit einem Angebot. Bis dahin ist nichts fest, Sie müssen nichts tun.',
               f'Haben Sie noch eine Frage, rufen Sie uns an: {TEL}.'],
         karte=('Ihre Anfrage', AUFENTHALT),
         knopf=('Die Zimmer ansehen', 'zimmer.html'), dazu='Alle Zimmer haben Dusche oder Bad, WC, Haarfön, TV, Safe und Balkon.'),
    dict(nr='02', wann='Wenn das Angebot steht', ordner='02-angebot', name='Ihr Angebot', satz='Das Angebot zur Anfrage, gerechnet aus der Preisliste des Hauses: Zimmer mit Halbpension, Kind im Zimmer der Eltern, Kurtaxe.',
         betreff='Ihr Angebot für den Sommer im Monte-Moro', titel=('Ihre Ferien,', 'unser Angebot.'), foto='haus-sommer-g', bsp=True,
         text=['Grüezi Frau Meier', f'Gern machen wir Ihnen ein Angebot für {NAECHTE} Nächte im Juli: ein Standardzimmer mit Halbpension (4-Gänge), Ihre Tochter wohnt im Zimmer der Eltern.',
               'Im Preis steckt mehr, als man denkt: das Postauto im ganzen Saastal, im Sommer alle Bergbahnen ausser der Metro Alpin, das Frühstücksbuffet, der Racletteabend und der Kidsclub. Mehr erleben, weniger zahlen.',
               'Passt Ihnen das Angebot, buchen Sie direkt über unsere Website oder rufen Sie uns an.'],
         karte=('Ihr Angebot', AUFENTHALT[:2] + [
             ('Zimmer', f'2 × {NAECHTE} Nächte zu {chf(P_HP)}, {chf(ZIMMER)}'), ('Kind', f'{NAECHTE} Nächte zu {chf(P_KIND)}, inklusiv Halbpension, {chf(KIND)}'),
             ('Kurtaxe', f'Sommer, {chf(KURTAXE)}'), ('Zusammen', chf(SUMME))]),
         knopf=('Zimmer buchen', BUCHEN), dazu=D.EURO),
    dict(nr='03', wann='Nach der Buchung', ordner='03-bestaetigung', name='Ihre Buchung ist bestätigt', satz='Kommt nach der Buchung: die Daten des Aufenthalts und alles, was im Preis schon dabei ist.',
         betreff='Ihre Buchung im Hotel Monte-Moro ist bestätigt', titel=('Ihre Buchung', 'ist bestätigt.'), foto='empfang', bsp=True,
         text=['Grüezi Frau Meier', 'Ihre Buchung ist bestätigt. Wir freuen uns auf Sie und Ihre Familie.',
               'Alles schon dabei: Unten stehen Ihre Daten und was im Zimmerpreis inklusive ist. Kurz vor der Anreise schicken wir Ihnen noch den Weg zu uns.'],
         karte=('Ihr Aufenthalt', AUFENTHALT + [('Inklusive', ', '.join(i.split(':')[0] if ':' in i else i for i in ['Postauto', 'Bergbahnen (Sommer)', 'Frühstücksbuffet', 'Racletteabend', 'Kidsclub', 'Parkplatz']))]),
         knopf=('Was im Preis steckt', 'preise.html'), dazu='Die Buchungsnummer finden Sie in der Bestätigung des Buchungssystems.'),
    dict(nr='04', wann='Eine Woche vor der Anreise', ordner='04-anreise', name='Vor Ihrer Anreise', satz='Kommt vor der Anreise: der Weg mit Zug und Postauto oder mit dem Auto, so wie das Haus ihn beschreibt, und der Parkplatz.',
         betreff='Bald sind Sie bei uns in Saas-Almagell', titel=('Bald sind Sie', 'bei uns.'), foto='tal-dorf', bsp=True,
         text=['Grüezi Frau Meier', 'In einer Woche ist es so weit. Damit die Anreise leicht wird, hier der Weg ins Saastal.',
               D.ANREISE_ZUG.split(' Es bestehen')[0].replace('wo sie', 'wo Sie') + ' In Saas-Grund steigen Sie um, von der Busstation sind es drei Gehminuten bis zum Hotel.',
               'Mit dem Auto fahren Sie von Visp durchs Vispertal, bei der Verzweigung in Stalden Richtung Saastal; in Saas-Grund halten Sie sich bei der Abzweigung nach Saas-Fee links. ' + D.PARK + '.'],
         karte=('Der Weg', [('Mit Zug und Postauto', 'ab Visp ca. 45 Min.'), ('Mit dem Auto', 'ab Visp ca. 40 Min.'), ('Letztes Postauto', 'stündlich bis 20.10 Uhr ab Visp'),
                            ('Parkplatz', 'Hotelparkplatz, inklusive'), ('Ihre Anreise', 'Samstag, 10. Juli 2027')]),
         knopf=('Anreise ansehen', 'anreise.html'), dazu=f'Kommen Sie später an, rufen Sie uns kurz an: {TEL}.'),
    dict(nr='05', wann='Am Tag nach der Abreise', ordner='05-danke', name='Danke für Ihren Besuch', satz='Kommt am Tag nach der Abreise: ein Dank von Esther und Fabian und der Weg zurück ins Saastal.',
         betreff='Danke, dass Sie bei uns waren', titel=('Danke', 'für Ihren Besuch.'), foto='alpenrosen', bsp=True,
         text=['Grüezi Frau Meier', 'Schön, dass Sie bei uns im Monte-Moro waren. Wir hoffen, Sie haben das Saastal von seiner schönsten Seite erlebt.',
               'Und falls es einmal geregnet hat: Bei uns scheint fast immer die Sonne. Und morgen scheint die Sonne wieder.'],
         karte=('Bis zum nächsten Mal', [('Sommer', 'über 250 km Wanderwege'), ('Winter', 'Saas-Almagell 2400 m, Saas-Grund 3200 m, Saas-Fee 3500 m'),
                                         ('Im Preis', 'Postauto im ganzen Saastal'), ('Ab', 'CHF 90.00 pro Person und Tag mit Frühstück')]),
         knopf=('Wieder buchen', BUCHEN), dazu='Bezahlung in Euro möglich, Rückgeld in Franken.'),
    dict(nr='06', wann='Nach einer Tischreservierung', ordner='06-tisch', name='Ihr Tisch im Röstihüs', satz='Kommt nach der Reservierung eines Tischs im Röstihüs: Tag, Uhrzeit, Personen, und was auf der Karte steht.',
         betreff='Ihr Tisch im Röstihüs ist reserviert', titel=('Ihr Tisch', 'im Röstihüs.'), foto='roesti-tische', bsp=True,
         text=['Grüezi Herr Imboden', 'Ihr Tisch im Röstihüs ist reserviert. Wir freuen uns auf Sie.',
               'Elf Röstis stehen auf unserer Karte, dazu fünf Cordon bleus. Die Rösti Tschug Tschug wird mit Calvados flambiert, und zum Wein empfehlen wir den Hotelwein, den Fabian selbst kreiert hat.',
               f'Ändert sich etwas, rufen Sie uns an: {TEL}.'],
         karte=('Ihr Tisch', [('Tag', 'Freitag, 12. Februar 2027'), ('Uhrzeit', '19 Uhr'), ('Personen', '4'), ('Name', 'Imboden')]),
         knopf=('Die Karte ansehen', 'roestihues.html'), dazu=D.SONNE.replace('(bei uns scheint fast immer die Sonne) ', '').replace('Sonnenterasse', 'Sonnenterrasse')),
]
FUSSBILD = 'haus-winter-g'


def _alt(key):
    return BILDER[key][1] if key in BILDER else 'Hotel Monte-Moro'


def _bild(key):
    for a in ('l', 'x', 'm'):
        p = os.path.join(WEB, 'assets', 'img', f'{key}-{a}.webp')
        if os.path.exists(p):
            return p
    raise FileNotFoundError(key)


def bilder():
    """Fotos 1000 px im Format 16:9, unter 100 KB. Alte Bilder im Ordner, die keine Mail mehr braucht, fallen weg."""
    ziel = os.path.join(MAILS, 'img'); os.makedirs(ziel, exist_ok=True)
    brauch = {'marke.png'}
    for f in FAELLE + [dict(foto=FUSSBILD)]:
        key = f['foto']; z = os.path.join(ziel, key + '.jpg'); brauch.add(key + '.jpg')
        im = Image.open(_bild(key)).convert('RGB'); w, h = im.size
        nh = round(w * 9 / 16)
        if nh < h:
            y = round((h - nh) * .5); im = im.crop((0, y, w, y + nh))
        elif nh > h:
            nw = round(h * 16 / 9); x = round((w - nw) * {'alpenrosen': .7}.get(key, .5)); im = im.crop((x, 0, x + nw, h))
        for br, qu in ((1000, 80), (1000, 72), (1000, 64), (900, 66), (820, 64), (760, 62)):
            k = im.resize((br, round(im.height * br / im.width)), Image.LANCZOS) if br < im.width else im
            k.save(z, quality=qu, optimize=True, progressive=True)
            if os.path.getsize(z) < 100_000:
                break
    for p in os.listdir(ziel):
        if p not in brauch:
            os.remove(os.path.join(ziel, p))


def mail(f, basis, img='../img/'):
    """basis: Adresse der Website, relativ aus dem Ordner der Mail (Vorschau) oder voll (Versand)."""
    zeilen = ''.join(f'<tr><td style="padding:11px 12px 11px 0;border-top:1px solid rgba(179,152,103,.32);font:400 11px/1.35 {MONO};letter-spacing:.14em;text-transform:uppercase;color:{MESSING};width:36%;vertical-align:top">{e(k)}</td>'
                     f'<td style="padding:11px 0;border-top:1px solid rgba(179,152,103,.32);font:400 16px/1.4 {SANS};color:{CREME}">{e(v)}</td></tr>' for k, v in f['karte'][1])
    absaetze = f'<p style="margin:0 0 14px;font:400 21px/1.3 {SERIF};color:{TINTE}">{e(f["text"][0])}</p>' + ''.join(
        f'<p style="margin:0 0 14px;font:400 16px/1.62 {SANS};color:{TINTE}">{e(t)}</p>' for t in f['text'][1:])
    href = f['knopf'][1] if f['knopf'][1].startswith('http') else basis + f['knopf'][1]
    if f.get('plakat'):
        foto = f'<img src="{img}{f["foto"]}.jpg" width="300" alt="{e("Plakat des DJ-Abends: " + _alt(f["foto"]))}" style="display:block;border:0;width:300px;max-width:70%;height:auto;margin:0 auto;border-radius:14px;box-shadow:0 18px 30px -18px rgba(7,27,46,.55)">'
    else:
        foto = f'<img src="{img}{f["foto"]}.jpg" width="544" alt="{e(f.get("alt") or _alt(f["foto"]))}" style="display:block;border:0;width:100%;height:auto;border-radius:16px">'
    etikett = f['karte'][0] + (' · Beispielwerte' if f['bsp'] else '')
    knauf = f'<span style="display:inline-block;width:22px;height:22px;margin-left:14px;border-radius:50%;background:{CREME};vertical-align:middle;font:400 13px/22px {SANS};color:{LAERCHE_T};text-align:center">↗</span>'
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{e(f['betreff'])} · Hotel Monte-Moro</title>
<style>@font-face{{font-family:'Fjalla One';font-weight:400;font-display:swap;src:url('../../assets/fonts/FjallaOne-400.woff2') format('woff2')}}@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}}@font-face{{font-family:'DM Mono';font-weight:400;font-display:swap;src:url('../../assets/fonts/DMMono-normal-400.woff2') format('woff2')}}</style></head>
<body style="margin:0;padding:0;background:{CREME}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{CREME}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{BLATT};border-radius:18px;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(179,152,103,.45)">
  <tr><td align="center" style="background:{TIEF};padding:34px 30px 32px;border-bottom:1px solid rgba(179,152,103,.55)">
    <img src="{img}marke.png" width="190" alt="Hotel Monte-Moro, Saas-Almagell" style="display:block;border:0;width:190px;height:auto;margin:0 auto">
    <h1 style="margin:26px 0 0;font:400 clamp(28px,7.4vw,38px)/1.16 {SERIF};color:{CREME}">{e(f['titel'][0]).replace(' ', '&nbsp;')}<br><span style="color:{LAERCHE}">{e(f['titel'][1]).replace(' ', '&nbsp;')}</span></h1>
  </td></tr>
  <tr><td style="padding:34px clamp(22px,6vw,40px) 8px">{absaetze}</td></tr>
  <tr><td style="padding:6px 28px 6px">{foto}</td></tr>
  <tr><td style="padding:12px 28px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{NACHT};border-radius:14px;box-shadow:inset 0 0 0 1px rgba(179,152,103,.55)">
    <tr><td style="padding:22px 24px 12px"><div style="font:400 10.5px/1.3 {MONO};letter-spacing:.2em;text-transform:uppercase;color:{MESSING};padding-bottom:12px">{e(etikett)}</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{zeilen}</table></td></tr></table></td></tr>
  <tr><td align="center" style="padding:26px 30px 8px"><a href="{href}" style="display:inline-block;padding:9px 9px 9px 24px;border-radius:14px;background:{LAERCHE};font:400 12px/22px {MONO};letter-spacing:.16em;text-transform:uppercase;color:#FFFFFF;text-decoration:none">{e(f['knopf'][0])}{knauf}</a></td></tr>
  <tr><td style="padding:14px 36px 30px"><p style="margin:0;font:400 15px/1.6 {SANS};color:{LEISE};text-align:center">{e(f['dazu'])}</p>
    <img src="{img}{FUSSBILD}.jpg" width="520" alt="{e(_alt(FUSSBILD))}" style="display:block;border:0;width:100%;max-width:520px;height:auto;margin:26px auto 0;border-radius:16px">
    <p style="margin:18px 0 0;font:400 19px/1.4 {SERIF};color:{TINTE};text-align:center">Herzliche Grüsse aus Saas-Almagell<br>{fest(GRUSS)}</p></td></tr>
  <tr><td align="center" style="background:{TIEF};padding:26px 30px;border-top:1px solid rgba(179,152,103,.55)"><div style="font:400 13px/1.7 {SANS};color:{WAND}">{e(ADRESSE)}<br>Tel. {e(TEL)} · {e(MAIL_ADR)}</div></td></tr>
</table>
</td></tr></table>
</body></html>
'''


def eingebettet(f):
    """Die Mail steht direkt in der Seite (Robert 18.10.2026: kein eingebettetes Fenster). Dieselbe Mail wie im Ordner, nur die Bildwege von hier aus."""
    t = mail(f, '../', img='img/')
    t = t[t.index('<body'):]; t = t[t.index('>') + 1:t.rindex('</body>')]
    return t


def fest(t):
    """die letzten zwei Wörter fest verbunden (kein Wort allein in der letzten Zeile)"""
    t = t.replace('Monte-Moro', 'Monte\u2011Moro')   # kein Umbruch im Namen des Hauses
    a, _, b = t.rpartition(' ')
    return e(a) + '&nbsp;' + e(b) if a else e(t)


ZAHLWORT = {5: 'Fünf', 6: 'Sechs', 7: 'Sieben', 10: 'Zehn', 11: 'Elf', 12: 'Zwölf'}


def uebersicht():
    # Robert 18.10.2026 (Website-Master Punkt 15): Mails nebeneinander im Band, obere Hälfte mit weichem Auslauf, «Ganze Mail» auf und zu,
    # Nummer, Titel, Absender und Wann darüber; Pfeile am Laptop, am Handy eine nach der anderen
    pf = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{d}"/></svg>'
    n = ZAHLWORT.get(len(FAELLE), str(len(FAELLE)))
    karten = ''.join(f'''<article class="mb hr" style="--i:{min(i, 4)}">
  <header class="mb-ueber"><span class="mb-nr">{f['nr']}</span><span class="mb-ueber__t"><b>{fest(f['name'])}</b><small><span>Von</span> Hotel&nbsp;Monte&#8209;Moro</small><small><span>Wann</span> {fest(f['wann'])}</small><small><span>Betreff</span> {fest(f['betreff'])}</small></span></header>
  <div class="mb-blatt"><div class="mb-in">{eingebettet(f)}</div></div>
  <p class="mb-ganz"><button type="button" class="mb-kn" aria-expanded="false"><span class="a">Ganze Mail</span><span class="z">Weniger zeigen</span><i>{pf('M4 6l4 4 4-4')}</i></button></p>
</article>''' for i, f in enumerate(FAELLE))
    return f'''<!doctype html>
<html lang="de-CH"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{n} Mails · Hotel Monte-Moro</title>
<style>
@font-face{{font-family:'Fjalla One';font-weight:400;font-display:swap;src:url('../assets/fonts/FjallaOne-400.woff2') format('woff2')}}
@font-face{{font-family:'Instrument Sans';font-weight:400 600;font-display:swap;src:url('../assets/fonts/InstrumentSans-normal-400_600.woff2') format('woff2')}}
@font-face{{font-family:'DM Mono';font-weight:400;font-display:swap;src:url('../assets/fonts/DMMono-normal-400.woff2') format('woff2')}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{TIEF};color:{CREME};font:400 17px/1.6 'Instrument Sans','Helvetica Neue',Arial,system-ui,sans-serif;--rand:clamp(20px,4.6vw,76px)}}
header.kopf{{padding:clamp(56px,8vw,120px) var(--rand) clamp(30px,4vw,60px);text-align:center}}
header.kopf .marke{{display:block;width:clamp(150px,14vw,220px);height:auto;margin:0 auto;color:{BLATT};fill:currentColor}}
h1{{margin:clamp(18px,2vw,28px) auto 0;max-width:22ch;font:400 clamp(2.2rem,5vw,4.6rem)/1.06 'Fjalla One','Arial Narrow',sans-serif;text-wrap:balance}}h1 em{{font-style:normal;color:{LAERCHE}}}
header.kopf p{{max-width:60ch;margin:clamp(18px,2.1vw,32px) auto 0;color:rgba(245,242,238,.86)}}
main{{padding:0 0 clamp(60px,8vw,120px)}}
.band{{display:flex;gap:clamp(20px,2.4vw,40px);align-items:flex-start;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:var(--rand);padding:4px var(--rand) 34px;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
.band::-webkit-scrollbar{{display:none}}
.band:focus-visible{{outline:2px solid {LAERCHE};outline-offset:-2px}}
.mb{{flex:0 0 clamp(300px,34vw,520px);scroll-snap-align:start}}
.mb:last-child{{margin-inline-end:var(--rand)}}
.mb-ueber{{display:flex;gap:16px;align-items:flex-start;margin:0 4px 18px}}
.mb-nr{{font:400 2.3rem/.95 'Fjalla One','Arial Narrow',sans-serif;color:{CREME};font-variant-numeric:tabular-nums}}
.mb-ueber__t{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.mb-ueber__t b{{font:400 1.3rem/1.2 'Fjalla One','Arial Narrow',sans-serif}}
.mb-ueber__t small{{text-wrap:balance;font-size:.86rem;line-height:1.4;color:rgba(245,242,238,.76)}}
.mb-ueber__t small span{{display:inline-block;min-width:6.2em;font:400 10px/1.4 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:{MESSING}}}
.mb-blatt{{position:relative;height:640px;border-radius:18px;overflow:hidden;background:{CREME};box-shadow:0 0 0 1px rgba(179,152,103,.45),0 40px 50px -30px rgba(0,0,0,.9);-webkit-mask-image:linear-gradient(#000 68%,transparent);mask-image:linear-gradient(#000 68%,transparent)}}
.mb.auf .mb-blatt{{-webkit-mask-image:none;mask-image:none}}
.mb-in{{position:relative}}.mb-in table{{max-width:100%}}
.mb-ganz{{position:relative;margin:18px 0 0;text-align:center}}
.mb.auf .mb-ganz{{margin-top:22px}}
.mb-kn{{display:inline-flex;align-items:center;gap:14px;padding:7px 7px 7px 20px;border:0;border-radius:14px;cursor:pointer;font:400 11.5px/1 'DM Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:{CREME};
  background:linear-gradient(180deg,{NACHT2} 0%,{NACHT} 52%,{TIEF} 100%);box-shadow:inset 0 0 0 1px rgba(179,152,103,.6),inset 0 1px 0 rgba(255,255,255,.12),0 16px 30px -16px rgba(0,0,0,.75)}}
.mb-kn i{{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;color:#FFFFFF;background:linear-gradient(180deg,#E09A72,{LAERCHE} 55%,{LAERCHE_T});box-shadow:inset 0 1px 0 rgba(255,255,255,.55)}}
.mb-kn svg{{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}
.mb-kn .z,.mb.auf .mb-kn .a{{display:none}}.mb.auf .mb-kn .z{{display:inline}}.mb.auf .mb-kn svg{{transform:rotate(180deg)}}
.mb-kn:focus-visible{{outline:2px solid {CREME};outline-offset:3px}}
.pfeile{{display:flex;justify-content:center;gap:14px;margin-top:4px}}
.pf{{width:52px;height:52px;border:0;border-radius:50%;cursor:pointer;display:grid;place-items:center;color:#FFFFFF;background:linear-gradient(180deg,#E09A72,{LAERCHE} 55%,{LAERCHE_T});box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 12px 20px -10px rgba(0,0,0,.7)}}
.pf svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.pf:disabled{{opacity:.35;cursor:default}}
footer{{padding:26px var(--rand) 40px;text-align:center;font-size:.92rem;color:rgba(245,242,238,.64);border-top:1px solid rgba(179,152,103,.25)}}
footer a{{color:{CREME}}}
/* Hereinkommen wie auf den anderen Werkbank-Seiten: heben, nur transform und opacity, bei reduced-motion sofort da */
html.js .hr{{opacity:0;transform:translate3d(0,34px,0) scale(.985)}}
html.js .hr.da{{opacity:1;transform:none;transition:opacity .9s cubic-bezier(.2,.7,.2,1) calc(var(--i,0) * 110ms),transform 1.2s cubic-bezier(.16,1,.3,1) calc(var(--i,0) * 110ms)}}
@media (prefers-reduced-motion:reduce){{html.js .hr{{opacity:1;transform:none;transition:none}}}}
@media (max-width:760px){{.mb{{flex-basis:calc(100vw - 2 * var(--rand))}}.pfeile{{display:none}}}}
@media (hover:none){{.pfeile{{display:none}}}}
.mb-kn>span{{top:0!important;left:0!important;text-box:trim-both cap alphabetic}}.pf svg{{transform:none!important}}   /* Versalien mittig in Chromium und WebKit (wie knopf_mitte.css) */
</style></head>
<body>
<script>if (!matchMedia('(prefers-reduced-motion:reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<header class="kopf"><svg class="marke hr" style="--i:0" viewBox="0 0 3483 1425" role="img" aria-label="Hotel Monte-Moro, Saas-Almagell"><use href="/assets/oberflaeche/kleid/montemoro-marke.svg#wm"/></svg><h1 class="hr" style="--i:1">{n} Mails,<br><em>im Ton des&nbsp;Hauses.</em></h1>
<p class="hr" style="--i:2">Was ein Gast nach seiner Anfrage, nach der Buchung, vor der Anreise und nach dem Aufenthalt von Ihnen bekommt, kommt im Kleid der neuen Seite. {n} Fälle als Idee, von der Zimmeranfrage bis zum Tisch im Röstihüs. Namen, Daten und Nummern der Gäste sind Beispielwerte; Preise, Inklusive, Anreise und Kontakt sind die Ihres Hauses.</p></header>
<main><div class="band" id="mband" tabindex="0" aria-label="Die {n.lower()} Mails, zum Blättern">{karten}</div>
<div class="pfeile hr" style="--i:2"><button type="button" class="pf" data-r="-1" aria-label="Vorige Mail">{pf('M10.5 3 5.5 8l5 5')}</button><button type="button" class="pf" data-r="1" aria-label="Nächste Mail">{pf('m5.5 3 5 5-5 5')}</button></div></main>
<footer class="hr">Entwurf von Robert Reff, Tasty Studios. Stand {STAND}. <a href="../werkbank/index.html#papier">Zurück zu «Alles auf einen Blick»</a></footer>
<script>
(function () {{
  /* Hereinkommen: Kopf, Band und Fuss heben sich, sobald sie ins Bild kommen; die Mails im Band kommen zusammen mit dem Band */
  if (document.documentElement.classList.contains('js')) {{
    var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (!e.isIntersecting) return; io.unobserve(e.target);
      (e.target.id === 'mband' ? [].slice.call(e.target.querySelectorAll('.hr')) : [e.target]).forEach(function (x) {{ x.classList.add('da'); }}); }}); }}, {{ rootMargin: '0px 0px -8% 0px', threshold: 0 }});
    [].forEach.call(document.querySelectorAll('header.kopf .hr,.pfeile,footer'), function (x) {{ io.observe(x); }}); io.observe(document.getElementById('mband'));
  }}
}})();
(function () {{
  /* die Mail steht in der Seite; zu sieht man den oberen Teil, auf die ganze Mail, sofort */
  var ms = [].slice.call(document.querySelectorAll('.mb'));
  function lage(m) {{ var bl = m.querySelector('.mb-blatt'), i = bl.querySelector('.mb-in'); bl.style.height = (m.classList.contains('auf') ? i.scrollHeight : Math.min(640, i.scrollHeight)) + 'px'; }}
  ms.forEach(function (m) {{
    var k = m.querySelector('.mb-kn');
    [].forEach.call(m.querySelectorAll('img'), function (im) {{ if (!im.complete) im.addEventListener('load', function () {{ lage(m); }}, {{ once: true }}); }});
    lage(m);
    k.addEventListener('click', function () {{ var auf = m.classList.toggle('auf'); k.setAttribute('aria-expanded', auf); lage(m); if (!auf) m.scrollIntoView({{ block: 'nearest' }}); }});
  }});
  var rt = 0; addEventListener('resize', function () {{ clearTimeout(rt); rt = setTimeout(function () {{ ms.forEach(lage); kl(); }}, 120); }});
  /* Pfeile am Laptop blättern das Band um eine Mail */
  var b = document.getElementById('mband'), p = document.querySelectorAll('.pf');
  function schritt() {{ return ms[0].getBoundingClientRect().width + parseFloat(getComputedStyle(b).columnGap || 0); }}
  function kl() {{ p[0].disabled = b.scrollLeft < 4; p[1].disabled = b.scrollLeft > b.scrollWidth - b.clientWidth - 4; }}
  [].forEach.call(p, function (x) {{ x.addEventListener('click', function () {{ b.scrollBy({{ left: +x.dataset.r * schritt(), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }}); }}); }});
  b.addEventListener('scroll', kl, {{ passive: true }}); kl();
}})();
</script>
</body></html>
'''


def main():
    bilder()
    neu = {f['ordner'] for f in FAELLE}
    for p in glob.glob(os.path.join(MAILS, '[0-9][0-9]-*')):   # alte Ordner anderer Häuser fallen weg
        if os.path.basename(p) not in neu and os.path.isdir(p):
            shutil.rmtree(p)
    for f in FAELLE:
        z = os.path.join(MAILS, f['ordner']); os.makedirs(z, exist_ok=True)
        open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(mail(f, '../../'))
    open(os.path.join(MAILS, 'index.html'), 'w', encoding='utf-8').write(uebersicht())
    import sys
    sys.path.insert(0, os.path.join(ROOT, '_werkbank'))
    import papier_nach   # Knopfschrift mittig in Chromium und WebKit (knopf_mitte.css/.js des Papier-Teils, 31.10.2026)
    papier_nach.knopf_mitte(os.path.join(MAILS, 'index.html'))
    json.dump([[f['nr'], f['ordner'], f['name'], f['satz']] for f in FAELLE], open(os.path.join(HIER, 'werkbank.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(FAELLE), 'Mails gebaut:', ', '.join(f['ordner'] for f in FAELLE), '| Angebot', chf(SUMME))


if __name__ == '__main__':
    main()
