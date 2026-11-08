// Vorschaubilder der Zeichen für den Ordner «Material» (Werkbank Papier, 08.11.2026): jede SVG aus dem Markenbuch als PNG,
// auf ihren Inhalt zugeschnitten, mit Grund (helle Zeichen auf Nacht). Die Werkbank kennt sonst nur QuickLook (macOS) dafür.
//   node _werkbank/zeichen_bild.js   → _werkbank/roh/zeichen/<name>.png
const path = require('path'), fs = require('fs');
let pw; try { pw = require('playwright'); } catch (_) { pw = require('/Users/robertreff/Aussen-Pruefung/node_modules/playwright'); }
const HIER = __dirname, Q = path.join(HIER, '..', '..', '..', '_kette', '05-markenbauer', 'marke', 'zeichen'), Z = path.join(HIER, 'roh', 'zeichen');
const DATEIEN = [['wortmarke-blau', '#F5F2EE'], ['wortmarke-papier', '#0A2A4A'], ['wortmarke-nacht', '#F5F2EE'], ['bergkamm-laerche', '#F5F2EE'], ['bergkamm-blau', '#F5F2EE']];
(async () => {
  fs.mkdirSync(Z, { recursive: true });
  const b = await pw.chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 400 }, deviceScaleFactor: 1 });
  for (const [n, grund] of DATEIEN) {
    const svg = fs.readFileSync(path.join(Q, n + '.svg'), 'utf8').replace(/<\?xml[^>]*>/, '');
    await p.setContent(`<body style="margin:0;background:${grund}"><div id="z" style="display:inline-block;padding:40px;background:${grund}"><div style="width:420px">${svg.replace('<svg ', '<svg style="display:block;width:100%;height:auto" ')}</div></div></body>`);
    await (await p.$('#z')).screenshot({ path: path.join(Z, n + '.png') });
  }
  await b.close();
  console.log('Zeichen-Bilder', DATEIEN.length);
})();
