#!/usr/bin/env node
/* Aufnahmen des Markenbauer-Pakets, unsichtbar (Playwright, Regel 49): Probe A/B am Rechner und Handy, Logo richtig/falsch,
   Markenbuch-Kopf, Farbkarten. node aufnahmen.js  → bilder/*.jpg  (Playwright aus ~/Aussen-Pruefung/node_modules) */
const path = require('path'), os = require('os'), fs = require('fs');
module.paths.push(path.join(os.homedir(), 'Aussen-Pruefung', 'node_modules'));
const pw = require('playwright');
const H = __dirname, M = path.join(H, 'marke'), B = path.join(H, 'bilder');
const url = f => 'file://' + path.join(M, f);
(async () => {
  fs.mkdirSync(B, { recursive: true });
  const browser = await pw.chromium.launch({ headless: true });
  const bericht = [];
  async function seite(adresse, b, h, scale = 2) {
    const ctx = await browser.newContext({ viewport: { width: b, height: h }, deviceScaleFactor: scale, locale: 'de-DE' });
    const page = await ctx.newPage();
    const fehler = [];
    page.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); });
    page.on('pageerror', e => fehler.push(String(e)));
    await page.goto(adresse, { waitUntil: 'load', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    return { ctx, page, fehler };
  }
  async function durchscrollen(page) {
    const H = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += 500) { await page.evaluate(v => window.scrollTo(0, v), y); await page.waitForTimeout(90); }
    await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(400);
  }
  // Probe: Welt A und B, Rechner (ganze Seite) und Handy (ganze Seite)
  for (const w of ['a', 'b']) {
    for (const [name, b, h] of [['rechner', 1440, 900], ['handy', 390, 844]]) {
      const { ctx, page, fehler } = await seite(url('probe.html') + '?welt=' + w, b, h);
      await durchscrollen(page);
      await page.evaluate(() => { document.body.classList.add('aufnahme'); document.querySelectorAll('section').forEach(s => s.classList.add('da')); });
      await page.waitForTimeout(2900);
      const ziel = path.join(B, `probe-${w}-${name}.jpg`);
      await page.screenshot({ path: ziel, fullPage: true, type: 'jpeg', quality: 86 });
      const ueberlauf = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      const hoehe = await page.evaluate(() => document.documentElement.scrollHeight);
      bericht.push({ datei: path.relative(H, ziel), breite: b, hoehe, ueberlauf_px: ueberlauf, fehler });
      await ctx.close();
    }
  }
  // Logo richtig und falsch: die zwei Gruppen je als Bild
  {
    const { ctx, page, fehler } = await seite(url('logo-richtig-falsch/index.html'), 1440, 900);
    await page.waitForTimeout(600);
    const gruppen = await page.$$('ul.gr');
    for (const [i, name] of [[0, 'logo-richtig'], [1, 'logo-falsch']]) {
      const ziel = path.join(B, name + '.jpg');
      await gruppen[i].screenshot({ path: ziel, type: 'jpeg', quality: 86 });
      bericht.push({ datei: path.relative(H, ziel), fehler });
    }
    const ziel = path.join(B, 'logo-richtig-falsch.jpg');
    await page.screenshot({ path: ziel, fullPage: true, type: 'jpeg', quality: 84 });
    bericht.push({ datei: path.relative(H, ziel), fehler });
    await ctx.close();
  }
  // Farbkarten als Bild
  {
    const { ctx, page } = await seite(url('farben.svg'), 1400, 900);
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    await page.setViewportSize({ width: 1400, height: h });
    const ziel = path.join(B, 'farben.jpg');
    await page.screenshot({ path: ziel, type: 'jpeg', quality: 88 });
    bericht.push({ datei: path.relative(H, ziel) });
    await ctx.close();
  }
  // Tapete-Kacheln als WebP-Ersatz (PNG) für Grafikprogramme
  for (const t of ['tapete-hell', 'tapete-dunkel', 'tapete-dunkel-b']) {
    const { ctx, page } = await seite(url('zeichen/' + t + '.svg'), 560, 560, 1);
    await page.screenshot({ path: path.join(M, 'zeichen', t + '.png'), type: 'png' });
    await ctx.close();
  }
  // Markenbuch: Kopf und ganze Seite (Rechner), Kopf am Handy
  {
    const { ctx, page, fehler } = await seite(url('markenbuch.html'), 1440, 900);
    await durchscrollen(page);
    await page.evaluate(() => document.querySelectorAll('section').forEach(s => s.classList.add('da')));
    await page.waitForTimeout(2600);
    await page.screenshot({ path: path.join(B, 'markenbuch-kopf.jpg'), type: 'jpeg', quality: 86 });
    await page.screenshot({ path: path.join(B, 'markenbuch-rechner.jpg'), fullPage: true, type: 'jpeg', quality: 78 });
    const ueberlauf = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    bericht.push({ datei: 'bilder/markenbuch-rechner.jpg', ueberlauf_px: ueberlauf, fehler, hoehe: await page.evaluate(() => document.documentElement.scrollHeight) });
    await ctx.close();
    const m = await seite(url('markenbuch.html'), 390, 844);
    await durchscrollen(m.page);
    const u = await m.page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    await m.page.evaluate(() => window.scrollTo(0, 0)); await m.page.waitForTimeout(1800);
    await m.page.screenshot({ path: path.join(B, 'markenbuch-handy.jpg'), type: 'jpeg', quality: 86 });
    bericht.push({ datei: 'bilder/markenbuch-handy.jpg', ueberlauf_px: u, fehler: m.fehler });
    await m.ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(B, '_bericht.json'), JSON.stringify(bericht, null, 1));
  console.log(JSON.stringify(bericht, null, 1));
})().catch(e => { console.error(String(e)); process.exit(1); });
