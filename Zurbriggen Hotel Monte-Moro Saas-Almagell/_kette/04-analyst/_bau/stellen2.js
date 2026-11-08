// Fassung 3 (Master 1b Nr. 15): je Stelle eine Aufnahme mit mehreren Ankern (Rechtecke mehrerer Textstellen), für «Was genau» mit Hinweislinien.
// node stellen2.js [id …] → stellen2/<id>.png + stellen2/anker.json {id: {url, anker:[{t,x,y,w,h}], W, H, f}}
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = __dirname + '/stellen2/';
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const L = JSON.parse(fs.readFileSync(__dirname + '/stellen2.json')); const nur = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const A = fs.existsSync(OUT + 'anker.json') ? JSON.parse(fs.readFileSync(OUT + 'anker.json')) : {};
  for (const [id, pfad, o] of L) {
    if (nur.length && !nur.includes(id)) continue;
    // «Lesbar oder raus» (Master 1b Nr. 15): die Vergrösserung zeigt dieselbe Stelle in 100 Prozent und schmal (270 px), damit die Schrift im Beweis mindestens Fliesstextgrösse hat
    const c = await b.newContext({ viewport: { width: 270, height: 900 }, deviceScaleFactor: 3, isMobile: false, hasTouch: true, userAgent: UA, locale: 'de-DE' });
    await c.addCookies([{ name: 'reDimCookieHint', value: '-1', domain: 'www.monte-moro.ch', path: '/' }]);
    const p = await c.newPage(); p.on('dialog', d => d.dismiss().catch(() => {}));
    try { await p.goto('https://www.monte-moro.ch' + pfad, { waitUntil: 'load', timeout: 90000 }); } catch (e) { console.log(id, e.message.split('\n')[0]); }
    await p.waitForTimeout(o.warte || 2500);
    // ragt etwas über 270 px hinaus (lange Überschrift), wird die Aufnahme so breit wie die Seite: kein Wort wird am Rand abgeschnitten
    let W = 270; const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    if (sw > 270) { W = Math.min(360, sw + 2); await p.setViewportSize({ width: W, height: 900 }); await p.waitForTimeout(1500); }
    await p.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    const finde = async () => p.evaluate((texte) => {
      const vv = window.visualViewport || { scale: 1, offsetLeft: 0, offsetTop: 0 };
      return texte.map(([txt, wahl]) => {
        const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, hits = [];
        while ((n = w.nextNode())) { const i = n.data.indexOf(txt); if (i < 0) continue; const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + txt.length); const q = r.getBoundingClientRect();
          if (q.width > 2 && q.height > 2 && getComputedStyle(n.parentElement).visibility !== 'hidden') hits.push({ zr: [...r.getClientRects()].filter(z => z.width > 1).map(z => [(z.left - vv.offsetLeft) * vv.scale, (z.top - vv.offsetTop) * vv.scale, z.width * vv.scale, z.height * vv.scale]), fs: parseFloat(getComputedStyle(n.parentElement).fontSize), t: txt, x: (q.left - vv.offsetLeft) * vv.scale, y: (q.top - vv.offsetTop) * vv.scale, w: q.width * vv.scale, h: q.height * vv.scale, top: q.top + scrollY }); }
        if (!hits.length) return { t: txt, fehlt: true };
        return wahl === 'letzt' ? hits[hits.length - 1] : hits[Math.min(wahl || 0, hits.length - 1)];
      });
    }, o.texte);
    let a = await finde();
    const erst = a.find(x => !x.fehlt);
    if (erst) { const sc = await p.evaluate(() => (window.visualViewport || { scale: 1 }).scale); await p.evaluate(([t, h]) => scrollTo(0, Math.max(0, t - h)), [erst.top, 900 / sc * (o.hoch ?? 0.3)]); await p.waitForTimeout(1500); a = await finde(); }
    // alle Textzeilen im Bild (oben, unten): der Ausschnitt endet nur zwischen zwei Zeilen
    const zeilen = await p.evaluate(() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) { if (!n.data.trim()) continue; const r = document.createRange(); r.selectNodeContents(n);
        for (const q of r.getClientRects()) if (q.bottom > -50 && q.top < innerHeight + 50 && q.width > 1 && q.height > 4) out.push([Math.round(q.top * 10) / 10, Math.round(q.bottom * 10) / 10]); }
      document.querySelectorAll('img,input,button,.btn,a.button').forEach(e => { const q = e.getBoundingClientRect(); if (q.bottom > -50 && q.top < innerHeight + 50 && q.height > 4) out.push([q.top, q.bottom]); });
      return out; });
    await p.screenshot({ path: OUT + id + '.png' });
    A[id] = { url: p.url().replace('?', ''), anker: a, W, H: 900, f: 3, zeilen }; console.log(id, JSON.stringify(a.map(x => x.fehlt ? 'FEHLT ' + x.t : [x.t.slice(0, 14), Math.round(x.x), Math.round(x.y), x.fs])));
    fs.writeFileSync(OUT + 'anker.json', JSON.stringify(A, null, 1)); await c.close();
  }
  await b.close();
})();
