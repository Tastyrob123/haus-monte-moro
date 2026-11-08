/* Die Hausdruckerei · Hotel Monte-Moro: die fertigen Drucksachen des Hauses als PDF (3 mm Beschnitt, Schriften eingebettet) und Vorschaubild,
   gesetzt mit dem Werkzeug selbst (DS.dokument, DS.pdf, DS.png) aus dem Katalog des Hauses (katalog.js). Dazu Druckprüfung und Stilprüfung je Stück.
   Aufruf (Server :9387 läuft):  NODE_PATH=$(npm root -g) node _bau/drucksachen.js   → haeuser/montemoro/drucksachen/ + LISTE.md */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ZIEL = path.join(__dirname, '..', 'haeuser', 'montemoro', 'drucksachen');
const STUECKE = [   // [Datei, Abteilung, Vorlage, was, Format (sonst das der Vorlage)]
  ['roestihues-best-of-roestis', 'roestihues', 'Best of Röstis', 'Röstihüs-Karte A4, Vorder- und Rückseite: die elf Röstis als Blatt auf Nacht'],
  ['roestihues-cordon-bleus', 'roestihues', 'Unsere Cordon bleus', 'Röstihüs-Karte DL hoch: die fünf Cordon bleus'],
  ['roestihues-auszug', 'roestihues', 'Röstihüs · Auszug der Karte', 'Karte am Tisch DL hoch: Auszug der Röstihüs-Karte'],
  ['roestihues-wein-von-fabian', 'roestihues', 'Wein von Fabian', 'Weinkarte DL hoch: die zwei Hotelweine, von Fabian selber kreiert'],
  ['roestihues-apero-dessert', 'roestihues', 'Zum Apéro und zum Dessert', 'Karte A6: Spritz und Monte-Moro-Kopf'],
  ['tischaufsteller-tradition', 'roestihues', 'Es lebe die Tradition', 'Tischaufsteller A6 im Röstihüs'],
  ['tischkarte-hotelwein', 'zimmer', 'Tischkarte · Cuvee Special', 'Tischkarte A7 quer zum Hotelwein'],
  ['tischkarte-hotelwein-eichenfass', 'zimmer', 'Tischkarte · Cuvee Special Eichenfass', 'Tischkarte A7 quer zum Hotelwein aus dem Eichenfass'],
  ['aushang-inklusive', 'inklusive', 'Inklusive', 'Aushang A4 «Inklusive»: Postauto, Bergbahnen im Sommer, Frühstück, Racletteabend, Kidsclub, Parkplatz'],
  ['plakat-inklusive-a3', 'inklusive', 'Aushang Inklusive', 'Plakat A3 mit Grat-Kante: Mehr erleben, weniger zahlen'],
  ['preisliste-zimmer', 'inklusive', 'Preisliste Zimmer', 'Preisliste A4: Zimmer mit Frühstück oder Halbpension'],
  ['preisliste-zuschlaege', 'inklusive', 'Zuschläge', 'Preisliste A5: Kurtaxe, Zuschläge, Hund'],
  ['preisliste-kinder', 'inklusive', 'Kinderpreise', 'Preisliste A5: Kinder im Zimmer der Eltern'],
  ['aushang-racletteabend', 'abende', 'Racletteabend im Stübli', 'Aushang A4 mit Grat-Kante: Racletteabend im Stübli'],
  ['aushang-kidsclub', 'abende', 'Kidsclub', 'Aushang A4: Kidsclub Mo–Sa 16:30–21:00 Uhr'],
  ['programm-woche', 'abende', 'Die Woche im Monte-Moro', 'Programm A5: was jede Woche dabei ist'],
  ['willkommensbrief', 'zimmer', 'Willkommensbrief im Zimmer', 'Brief A4 im Zimmer, mit dem Gruss von Esther und Fabian'],
  ['briefpapier-a4', 'zimmer', 'Briefpapier A4', 'Briefpapier A4 mit Wortmarke und Absender'],
  ['hinweis-spa', 'zimmer', 'Das Spa nebenan', 'Hinweiskarte A6: Spa im Partnerhotel mit Tarifen'],
  ['hinweis-euro', 'zimmer', 'Auch in Euro', 'Hinweiskarte A6: Bezahlung in Euro'],
  ['anreise-postauto', 'saastal', 'Anreise mit dem Postauto', 'Aushang A4: Anreise mit Zug und Postauto ab Visp'],
  ['anreise-zug-postauto', 'saastal', 'Mit Zug und Postauto', 'Programm A5: Visp, Stalden, Saas-Grund, Saas-Almagell'],
  ['anreise-auto', 'saastal', 'Mit dem Auto', 'Aushang A5: Anreise mit dem Auto'],
  ['plakat-wanderparadies-a3', 'saastal', 'Wanderparadies', 'Plakat A3 mit Grat-Kante: Sommer im Saastal'],
  ['ansichtskarte-sommer', 'saastal', 'Ansichtskarte Sommer', 'Ansichtskarte A6 quer, Rückseite für Grüsse'],
  ['gutschein-aufenthalt', 'haus', 'Gutschein für einen Aufenthalt', 'Gutschein DL quer, Vorder- und Rückseite'],
  ['gutschein-roestihues', 'haus', 'Gutschein Röstihüs', 'Gutschein DL quer mit Foto, Vorder- und Rückseite'],
  ['flyer-haus', 'haus', 'Flyer des Hauses', 'Flyer A6, vorne Foto, hinten Kontakt'],
  ['instagram-elf-roestis', 'roestihues', 'Elf Röstis', 'Instagram-Beitrag hoch 4:5'],
  ['instagram-bergbahnen', 'inklusive', 'Bergbahnen und Postautos', 'Instagram-Beitrag hoch 4:5 mit Grat-Kante'],
  ['instagram-lift-quadrat', 'saastal', 'Zwei Minuten bis zum Lift', 'Instagram-Beitrag quadratisch 1:1 mit Grat-Kante', 'ig11'],
  ['instagram-gastgeber', 'haus', 'Ihre Gastgeber', 'Instagram-Beitrag hoch 4:5'],
  ['story-spa', 'saastal', 'Das Spa nebenan · Story', 'Instagram-Story 9:16'],
  ['story-kidsclub', 'abende', 'Spielburg vor dem Haus', 'Instagram-Story 9:16'],
];
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const fehler = []; p.on('pageerror', e => fehler.push(e.message));
  await p.addInitScript(() => { try { localStorage.setItem('ds-montemoro-willkommen', '1'); } catch (e) {} });
  await p.goto('http://127.0.0.1:9387/_werkzeuge/imprimerie/', { waitUntil: 'load' });
  await p.waitForFunction(() => window.DS && DS.M && window.DSStudio && DS.pdf, null, { timeout: 30000 });
  await p.waitForTimeout(1500);
  const zeilen = [];
  for (const [k, abt, n, was, fmt] of STUECKE) {
    const r = await p.evaluate(async ({ abt, n, fmt }) => {
      const x = window.DSKATALOG.ABTEILUNGEN.find(a => a.k === abt).vorlagen.find(v => v.n === n);
      if (!x) return { fehlt: true };
      const seiten = [{ vorlage: x.vorlage, ton: x.ton, inhalt: x.inhalt, stil: x.stil }];
      if (x.rueck) seiten.push({ vorlage: x.rueck.vorlage, ton: x.ton, inhalt: x.rueck.inhalt });
      const doc = DS.dokument(DS.M, { name: 'Hotel Monte-Moro · ' + n, format: fmt || x.format, seiten });
      const pr = (DS.pruefe(DS.M, doc) || []).concat(DS.stilPruefe(DS.M, doc) || []).filter(h => h.stufe === 'rot').map(h => h.text);
      const { bytes } = await DS.pdf(DS.M, doc, { marken: false });
      const b64 = u => { let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); };
      const bilder = [];
      for (let i = 0; i < seiten.length; i++) { const bl = await DS.png(DS.M, doc, i, 1200), bm = await createImageBitmap(bl), cv = document.createElement('canvas'); cv.width = bm.width; cv.height = bm.height; const g = cv.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, cv.width, cv.height); g.drawImage(bm, 0, 0); const jp = await new Promise(ok => cv.toBlob(ok, 'image/jpeg', .86)); bilder.push(b64(new Uint8Array(await jp.arrayBuffer()))); }
      return { pdf: b64(bytes), bilder, rot: pr, format: DS.FORMATE[fmt || x.format].name, seiten: seiten.length };
    }, { abt, n, fmt });
    if (r.fehlt) { console.log('FEHLT', n); continue; }
    fs.writeFileSync(path.join(ZIEL, k + '.pdf'), Buffer.from(r.pdf, 'base64'));
    r.bilder.forEach((bi, i) => fs.writeFileSync(path.join(ZIEL, k + (i ? '-' + (i + 1) : '') + '.jpg'), Buffer.from(bi, 'base64')));
    zeilen.push({ k, abt, n, was, format: r.format, seiten: r.seiten, rot: r.rot });
    console.log(k, r.format, r.seiten, 'Seite(n)', r.rot.length ? 'ROT: ' + r.rot.join(' | ') : 'ohne roten Befund');
  }
  zeilen.forEach(x => { x.pdf = x.k + '.pdf'; x.vorschau = Array.from({ length: x.seiten }, (_, i) => x.k + (i ? '-' + (i + 1) : '') + '.jpg'); });
  fs.writeFileSync(path.join(ZIEL, 'liste.json'), JSON.stringify(zeilen, null, 1));
  const ABT = { roestihues: 'Röstihüs', inklusive: 'Preise & Inklusive', abende: 'Racletteabend & Kidsclub', zimmer: 'Im Zimmer', saastal: 'Saastal & Anreise', haus: 'Das Haus & Geschenke' };
  const md = ['---', 'tags: [projekt, website]', 'status: aktiv', '---', '', '# Drucksachen · Hotel Monte-Moro, Saas-Almagell', '',
    'Gesetzt mit der Hausdruckerei (`_werkzeuge/imprimerie/`, Aufruf `NODE_PATH=$(npm root -g) node _bau/drucksachen.js`), Inhalte nur aus `website/inhalt/daten.py` und den Seiten der Website (`bau_vorlagen.py`).',
    'PDF mit 3 mm Beschnitt und eingebetteten Schriften der Website (Fjalla One, Instrument Sans, DM Mono als TrueType), Vorschaubild 1200 px breit (JPG). Druck- und Stilprüfung je Stück: ' + (zeilen.every(x => !x.rot.length) ? 'ohne roten Befund.' : 'siehe liste.json.'), '',
    '| Datei | Drucksache | Abteilung | Was | Format | Seiten | Vorschau |', '|---|---|---|---|---|---|---|',
    ...zeilen.map(x => `| \`${x.pdf}\` | ${x.n} | ${ABT[x.abt] || x.abt} | ${x.was} | ${x.format} | ${x.seiten} | ${x.vorschau.map(v => '\`' + v + '\`').join(', ')} |`), '',
    'Nicht auf den Drucksachen, weil das Haus es nicht veröffentlicht: Öffnungszeiten des Röstihüs, Strasse des Hauses, Storno- und Geschäftsbedingungen, Fotos vom Kidsclub. Die Gratis-Anreise mit dem öffentlichen Verkehr galt bis 31.10.2026 und steht nirgends mehr.'];
  fs.writeFileSync(path.join(ZIEL, 'LISTE.md'), md.join('\n') + '\n');
  if (fehler.length) console.log('Seitenfehler:', fehler.join('\n'));
  await b.close();
})();
