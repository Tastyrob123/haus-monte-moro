// _bau/blick.js · schneller Blick auf eine Seite (Kontrollpanel, mm-maison): Bildschirmbild, Konsolenfehler, fehlgeschlagene Anfragen.
// node blick.js <adresse> <ausgabe.png> [breite=1440] [hoehe=932] [ganz=0] [klick-selektor]
const { chromium } = require('playwright');
(async () => {
  const [url, aus, b = '1440', h = '932', ganz = '0', klick] = process.argv.slice(2);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +b, height: +h }, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  const fehler = [];
  page.on('console', m => { if (m.type() === 'error') fehler.push('konsole: ' + m.text()); });
  page.on('pageerror', e => fehler.push('seite: ' + e.message));
  page.on('response', r => { if (r.status() >= 400) fehler.push(r.status() + ' ' + r.url()); });
  page.on('requestfailed', r => fehler.push('fehlgeschlagen ' + r.url()));
  await page.goto(url, { waitUntil: 'networkidle' });
  if (klick) { await page.click(klick); await page.waitForTimeout(600); }
  await page.waitForTimeout(800);
  const breiter = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  await page.screenshot({ path: aus, fullPage: ganz === '1' });
  console.log(JSON.stringify({ fehler, ueberlauf: breiter }, null, 1));
  await browser.close();
})();
