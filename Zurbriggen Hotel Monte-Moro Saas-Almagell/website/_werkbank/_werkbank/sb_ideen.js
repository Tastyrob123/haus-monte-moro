// Aufnahmen für die Werkbank des Hotel Monte-Moro (Werkbank Kern, 08.11.2026, Vorlage aus dem Stamm): Ideen (Rechner 1440 × 900) und Gäste-Funktionen (Rechner + Handy 390 × 844).
//   node _werkbank/sb_ideen.js [name …]  →  _werkbank/ansichten/Ideen/<name>.jpg, ansichten/Gaeste/<name>.jpg und <name>-h.jpg
// Jede Stelle: Seite, Anker (Abschnitt oben an den Rand), Verschiebung in px, optional ein Klick vor der Aufnahme. Nichts wird abgeschickt.
const path = require('path'), fs = require('fs');
let PW; try { PW = require('playwright'); } catch (e) { PW = require('/opt/node-tools/node_modules/playwright'); }
const { chromium } = PW;
const HIER = __dirname, B = 'http://127.0.0.1:' + (process.env.WB_PORT || 9388) + '/';
const IDEEN = [
  ['start', 'index.html', null, 0], ['zimmer', 'index.html', '#zimmer', 0], ['bon', 'index.html', '#inbegriffen', 0],
  ['saastal', 'index.html', '#saastal', 0], ['spa', 'index.html', '#spa', 0], ['roesti', 'index.html', '#roestihues', 0],
  ['kinder', 'index.html', '#kinder', 0], ['wein', 'index.html', '#wein', 0], ['schluss', 'index.html', '#morgen-wieder', 0],
  ['preise', 'preise.html', '#preisliste', 0], ['karte', 'roestihues.html', '#karte', 0], ['anreise', 'anreise.html', '#weg', 0],
];
const GAESTE = [   // name, Seite, Anker, Verschiebung, Klick (Selektor) oder null
  ['buchen', 'index.html', null, 0, null], ['zimmer', 'zimmer.html', '#hotelzimmer', 0, '[data-zimmer="standard"]'],
  ['anfrage', 'zimmer.html', '#hotelzimmer', 0, '[data-anfrage="Familienzimmer"]'], ['chat', 'index.html', '#zimmer', 0, '[data-chat-auf]'],
  ['inklusive', 'preise.html', '#bon', 0, null], ['anreise', 'anreise.html', '#zwei-wege', 0, null],
];
const nur = process.argv.slice(2);
async function stelle(p, seite, anker, dy, klick) {
  await p.goto(B + seite, { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
  await p.waitForTimeout(seite === 'index.html' ? 5200 : 2600);
  await p.evaluate(async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } });
  if (anker) await p.evaluate(([a, dy]) => { const e = document.querySelector(a); if (e) scrollTo(0, e.getBoundingClientRect().top + scrollY + dy); }, [anker, dy]);
  else await p.evaluate(() => scrollTo(0, 0));
  await p.waitForTimeout(2600);
  if (klick) { const k = await p.$(klick); if (k) { await k.click().catch(() => {}); await p.waitForTimeout(1600); } else console.log('  kein Ziel für Klick', klick); }
}
(async () => {
  for (const d of ['Ideen', 'Gaeste']) fs.mkdirSync(path.join(HIER, 'ansichten', d), { recursive: true });
  const b = await chromium.launch({ headless: true });
  const r = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }); const p = await r.newPage(); p.setDefaultTimeout(240000);
  for (const [n, s, a, dy] of IDEEN) { if (nur.length && !nur.includes(n)) continue; await stelle(p, s, a, dy); await p.screenshot({ path: path.join(HIER, 'ansichten/Ideen', n + '.jpg'), quality: 88 }); console.log('Idee', n); }
  for (const [n, s, a, dy, k] of GAESTE) { if (nur.length && !nur.includes(n)) continue; await stelle(p, s, a, dy, k); await p.screenshot({ path: path.join(HIER, 'ansichten/Gaeste', n + '.jpg'), quality: 88 }); console.log('Gast', n); }
  const h = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }); const q = await h.newPage(); q.setDefaultTimeout(240000);
  for (const [n, s, a, dy, k] of GAESTE) { if (nur.length && !nur.includes(n)) continue; await stelle(q, s, a, dy, k); await q.screenshot({ path: path.join(HIER, 'ansichten/Gaeste', n + '-h.jpg'), quality: 88 }); console.log('Gast Handy', n); }
  await b.close();
})();
