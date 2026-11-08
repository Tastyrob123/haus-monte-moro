# Quelltext-Schirme für Befunde, die man auf dem Telefon nicht sieht: jede Zeile wörtlich aus dem Abruf der Seite am 17.10.2026 (roh/).
# python3 code.py → code.json (id → titel, zeilen, fuss), danach node code.js → stellen/<id>.png
import re, json, html, os
H = os.path.dirname(os.path.abspath(__file__)); R = H + '/roh/'
lies = lambda f: open(R + f, encoding='utf-8', errors='replace').read()
e = lambda s: html.escape(s, quote=False)
def z(s, kl=''): return f'<div class="z{(" " + kl) if kl else ""}">{s}</div>'
de = lies('de.html'); ak = lies('de_hotel_aktuelles.html.html')
S = {}
vp = re.search(r'<meta name="viewport"[^>]*>', de).group(0)
S['1.2c'] = dict(titel='Kopf jeder Seite · Abruf 17.10.2026', zeilen=''.join([z(e(vp), 'n'), z('<b>initial-scale=0.8</b> · die Seite öffnet sich auf 80 Prozent', 'g'), z('Üblich: initial-scale=1')]), fuss='Gleich auf Startseite, Zimmer, Preise und Restaurant, in Deutsch, Englisch und Französisch.')
cf = re.search(r'confirm\("[^"]*"\)', de).group(0)
S['1.3c'] = dict(titel='Der Knopf «Ablehnen» · Abruf 17.10.2026', zeilen=''.join([z(e('<a id="cookiehintsubmitno" onclick="return cookiehintsubmitnoc(this);" … class="btn">Ablehnen</a>')), z('function cookiehintsubmitnoc(obj) {'), z(e(cf), 'n'), z('«Akzeptieren»: ohne Rückfrage', 'g')]), fuss='Erweiterung redim cookiehint für Joomla, auf jeder Seite.')
ti = re.search(r'<title>[^<]*</title>', de).group(0); ds = re.search(r'<meta name="description"[^>]*>', de).group(0); ti2 = re.search(r'<title>[^<]*</title>', ak).group(0)
S['8.1c'] = dict(titel='Kopf der Startseite · Abruf 17.10.2026', zeilen=''.join([z(e(ti), 'n'), z(e(ds)), z('Seite «Aktuelles»:', 'g'), z(e(ti2), 'n')]), fuss='Titel und Beschreibung zeigt Google meist als Treffer an.')
mp = html.unescape(re.search(r'href="(https://www\.google\.ch/maps/dir/[^"]*)"', de).group(1))
S['8.2c'] = dict(titel='Knopf «Anfahrt berechnen» · Abruf 17.10.2026', zeilen=''.join([z(e(mp[:64]) + ' …'), z('Ziel: <b>Hotel Monte Moro, Talstrasse 129, 3905 Saas-Almagell</b>', 'n'), z('Fuss der Seite: CH-3905 Saas-Almagell (ohne Strasse)', 'g'), z('Google Maps, Eintrag des Hauses: Furusandstrasse 12', 'g')]), fuss='Google Maps abgelesen am 17.10.2026.')
kopf = [m.group(0) for m in re.finditer(r'<(?:title|meta)[^>]*>(?:[^<]*</title>)?', de)][:8]
S['8.3c'] = dict(titel='Kopf der Startseite · Abruf 17.10.2026', zeilen=''.join([z(e(k[:120]) + (' …' if len(k) > 120 else '')) for k in kopf] + [z('application/ld+json · <b>0</b> Treffer', 'n'), z('og:image · <b>0</b> Treffer', 'n')]), fuss='Keine Angaben nach schema.org: Name, Adresse, Sterne, Telefon, Restaurant.')
S['z.1c'] = dict(titel='Was die Seite über sich sagt · Abruf 17.10.2026', zeilen=''.join([z('templates/zerone/templateDetails.xml', 'g'), z('&lt;creationDate&gt;04.04.2019&lt;/creationDate&gt;'), z('&lt;author&gt;zerone&lt;/author&gt; · info@zerone.ch'), z('&lt;copyright&gt;Copyright (C) zerone computer gmbh&lt;/copyright&gt;', 'n'), z('&lt;license&gt;None&lt;/license&gt;', 'n'), z('Joomla, Fassung', 'g'), z('&lt;version&gt;<b>3.10.12</b>&lt;/version&gt; · vom Juli 2023', 'n')]), fuss='Joomla 3: Ende der Pflege im August 2023, bezahlte Verlängerung bis 17.02.2025, seither keine Sicherheits-Updates (joomshaper.com, abgerufen 17.10.2026).')
json.dump(S, open(H + '/code.json', 'w'), ensure_ascii=False, indent=1)
print(list(S))
