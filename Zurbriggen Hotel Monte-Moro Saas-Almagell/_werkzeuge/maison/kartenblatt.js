#!/usr/bin/env node
/* Das gesetzte Blatt einer Karte aus dem Kartenbrett als Bild (für die Stücke im Saal des Hotelbüros, wenn es noch keine PDF gibt).
   node _werkzeuge/maison/kartenblatt.js <ziel> <aus.png>   — öffnet das Kartenbrett auf #<ziel>, nur GET, und nimmt das Blatt der Vorschau auf. */
const pw = require('playwright');
(async () => {
  const [ziel, aus] = process.argv.slice(2);
  const b = await pw.chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 1600 }, deviceScaleFactor: 2.6, locale: 'de-DE', reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await p.route('**/*', r => ['GET', 'HEAD'].includes(r.request().method()) ? r.continue() : r.abort());
  await p.goto(`http://127.0.0.1:9383/_werkzeuge/carte/#${ziel}`, { waitUntil: 'load', timeout: 60000 });
  await p.waitForTimeout(3500);
  await p.addStyleTag({ content: '.wo-leiste,#meldung,.rdg-schild,#zur-werkbank{display:none!important}' });   /* nichts Schwebendes über dem Blatt */
  const fr = p.frames().find(f => /satz\/blatt\.html/.test(f.url()));
  if (!fr) throw new Error('kein Blatt');
  await fr.evaluate(() => document.fonts && document.fonts.ready);
  const el = await fr.$('section.blatt');
  if (!el) throw new Error('kein section.blatt');
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(600);
  await el.screenshot({ path: aus });
  await b.close();
})().catch(e => { console.error(String(e)); process.exit(1); });
