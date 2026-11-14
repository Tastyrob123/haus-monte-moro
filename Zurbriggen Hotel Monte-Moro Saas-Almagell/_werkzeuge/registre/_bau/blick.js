// Bildschirmfotos Besucher für das Auge: node _bau/blick.js <ausordner> [breite] [ansichten …]
// Je Ansicht ein ganzes Seitenbild, dazu Konsolenfehler und fehlende Dateien (404) als Liste.
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const aus = process.argv[2] || '/tmp/registre-blick', breite = +(process.argv[3] || 1440);
  const ansichten = process.argv.slice(4).length ? process.argv.slice(4) : ['start', 'besuche', 'herkunft', 'zeit', 'seiten', 'verlauf', 'buchung', 'zaehlung'];
  fs.mkdirSync(aus, { recursive: true });
  const b = await chromium.launch();
  const s = await b.newContext({ viewport: { width: breite, height: breite < 600 ? 844 : 900 }, deviceScaleFactor: 1 });
  await s.addInitScript(() => { try { localStorage.setItem('rundgang-montemoro-registre', '1'); } catch (e) {} });
  const p = await s.newPage(), fehler = [];
  p.on('console', m => { if (m.type() === 'error') fehler.push('konsole: ' + m.text()); });
  p.on('pageerror', e => fehler.push('seite: ' + e.message));
  p.on('response', r => { if (r.status() >= 400) fehler.push(r.status() + ' ' + r.url()); });
  for (const a of ansichten) {
    const url = a.startsWith('http') ? a : 'http://127.0.0.1:9386/_werkzeuge/registre/?gruss=tag#' + a;
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1800);
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    await p.waitForTimeout(2600);
    const name = a.startsWith('http') ? 'seite' : a;
    await p.screenshot({ path: path.join(aus, name + '-' + breite + '.png'), fullPage: true });
  }
  fs.writeFileSync(path.join(aus, 'fehler-' + breite + '.txt'), fehler.join('\n'));
  console.log('fertig', aus, fehler.length, 'Fehler'); fehler.slice(0, 20).forEach(f => console.log(f));
  await b.close();
})();
