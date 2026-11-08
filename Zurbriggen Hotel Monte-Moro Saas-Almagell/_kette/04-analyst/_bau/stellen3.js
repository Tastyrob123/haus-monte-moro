// Fassung 4 (Robert 17.10.2026: «auf dem Telefon ist alles in zwei Zeilen und du hast vier Zeilen rausgemacht»): die Vergrösserung kommt aus derselben
// Ansicht wie das Gerät, iPhone 390 × 844 (am Rechner 1440 × 900), in vierfacher Dichte. Jede Zeile bricht genau wie auf dem Handy.
// node stellen3.js [id …] → stellen3/<id>.png + stellen3/anker.json {id: {url, anker:[{t,x,y,w,h,zr,fs}], zeilen:[[oben,unten,links,rechts]], W, H, f}}
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
const OUT = __dirname + '/stellen3/'; fs.mkdirSync(OUT, { recursive: true });
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const UA_DESK = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36';
const L = JSON.parse(fs.readFileSync(__dirname + '/stellen3.json')); const nur = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const A = fs.existsSync(OUT + 'anker.json') ? JSON.parse(fs.readFileSync(OUT + 'anker.json')) : {};
  for (const [id, pfad, o] of L) {
    if (nur.length && !nur.includes(id)) continue;
    const W = o.desk ? 1440 : 390, H = o.desk ? 900 : 844, f = o.desk ? 2 : 4;
    const c = await b.newContext(o.desk ? { viewport: { width: W, height: H }, deviceScaleFactor: f, locale: 'de-DE', userAgent: UA_DESK }
      : { viewport: { width: W, height: H }, deviceScaleFactor: f, isMobile: true, hasTouch: true, userAgent: UA, locale: 'de-DE' });
    await c.addCookies([{ name: 'reDimCookieHint', value: '-1', domain: 'www.monte-moro.ch', path: '/' }]);
    const p = await c.newPage(); p.on('dialog', d => d.dismiss().catch(() => {}));
    try { await p.goto('https://www.monte-moro.ch' + pfad, { waitUntil: 'load', timeout: 90000 }); } catch (e) { console.log(id, e.message.split('\n')[0]); }
    await p.waitForTimeout(o.warte || 2500);
    await p.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < h; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    const finde = async () => p.evaluate((texte) => {
      const vv = window.visualViewport || { scale: 1, offsetLeft: 0, offsetTop: 0 };
      return texte.map(([txt, wahl]) => {
        const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, hits = [];
        while ((n = w.nextNode())) { const i = n.data.indexOf(txt); if (i < 0) continue; const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + txt.length); const q = r.getBoundingClientRect();
          if (q.width > 2 && q.height > 2 && getComputedStyle(n.parentElement).visibility !== 'hidden') hits.push({ zr: [...r.getClientRects()].filter(z => z.width > 1).map(z => [(z.left - vv.offsetLeft) * vv.scale, (z.top - vv.offsetTop) * vv.scale, z.width * vv.scale, z.height * vv.scale]), fs: parseFloat(getComputedStyle(n.parentElement).fontSize) * vv.scale, t: txt, x: (q.left - vv.offsetLeft) * vv.scale, y: (q.top - vv.offsetTop) * vv.scale, w: q.width * vv.scale, h: q.height * vv.scale, top: q.top + scrollY }); }
        if (!hits.length) return { t: txt, fehlt: true };
        return wahl === 'letzt' ? hits[hits.length - 1] : hits[Math.min(wahl || 0, hits.length - 1)];
      });
    }, o.texte);
    let a = await finde();
    const erst = a.find(x => !x.fehlt);
    if (erst) { const sc = await p.evaluate(() => (window.visualViewport || { scale: 1 }).scale); await p.evaluate(([t, h]) => scrollTo(0, Math.max(0, t - h)), [erst.top, H / sc * (o.hoch ?? 0.3)]); await p.waitForTimeout(1500); a = await finde(); }
    // jede Textzeile und jedes Bild mit Lage in Bildschirmpunkten: der Ausschnitt nimmt ganze Zeilen und endet nur zwischen zwei Zeilen
    const zeilen = await p.evaluate(() => { const vv = window.visualViewport || { scale: 1, offsetLeft: 0, offsetTop: 0 }; const s = vv.scale, out = [];
      const add = q => { if (q.bottom > -50 && q.top < innerHeight + 50 && q.width > 1 && q.height > 4) out.push([(q.top - vv.offsetTop) * s, (q.bottom - vv.offsetTop) * s, (q.left - vv.offsetLeft) * s, (q.right - vv.offsetLeft) * s].map(v => Math.round(v * 10) / 10)); };
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) { if (!n.data.trim()) continue; const st = getComputedStyle(n.parentElement); if (st.visibility === 'hidden' || st.display === 'none') continue; const r = document.createRange(); r.selectNodeContents(n); for (const q of r.getClientRects()) add(q); }
      document.querySelectorAll('img,input,button,.btn,a.button').forEach(e => add(e.getBoundingClientRect()));
      return out; });
    // Wortkästen (für Ausschnitte, die schmaler sind als die Zeile: ein Wort am Rand fällt ganz weg, keins wird zerschnitten)
    const worte = await p.evaluate(() => { const vv = window.visualViewport || { scale: 1, offsetLeft: 0, offsetTop: 0 }; const s = vv.scale, out = [];
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) { const re = /\S+/g; let m; while ((m = re.exec(n.data))) { const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
        for (const q of r.getClientRects()) if (q.bottom > 0 && q.top < innerHeight && q.width > 0.5) out.push([(q.left - vv.offsetLeft) * s, (q.top - vv.offsetTop) * s, (q.right - vv.offsetLeft) * s, (q.bottom - vv.offsetTop) * s].map(v => Math.round(v * 10) / 10)); } }
      return out; });
    await p.screenshot({ path: OUT + id + '.png' });
    A[id] = { url: p.url().replace('?', ''), anker: a, W, H, f, zeilen, worte, desk: !!o.desk }; console.log(id, JSON.stringify(a.map(x => x.fehlt ? 'FEHLT ' + x.t : [x.t.slice(0, 14), Math.round(x.x), Math.round(x.y), Math.round(x.fs * 10) / 10])));
    fs.writeFileSync(OUT + 'anker.json', JSON.stringify(A, null, 1)); await c.close();
  }
  await b.close();
})();
