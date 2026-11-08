// Hotel Monte-Moro, Potentialanalyse: je Punkt die echte Stelle von monte-moro.ch, aufgenommen wie ein Gast sie sieht (Werkzeugkette Castell _bau7).
// Chromium im iPhone-Modus (390 × 844, doppelte Dichte, iPhone-Kennung).
// «desk»: 1440 × 900 am Rechner.   node stellen.js [id …]  → stellen/<id>.png + stellen/lage.json (Rechteck der Stelle für den roten Kreis)
module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = __dirname + '/stellen/'; fs.mkdirSync(OUT, { recursive: true });
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const UA_DESK = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36';   // ohne echte Kennung antwortet der Server mit 400
async function weg(p) {   // «Alle ablehnen» per DOM anklicken (der Textverweis liegt am Rand und wird von Playwright als verdeckt gemeldet)
  const ok = await p.evaluate(() => { const re = /^\s*(Ablehnen|Decline|Refuser|Rejeter)\s*$/i;
    const el = [...document.querySelectorAll('a, button, span, div, p')].find(e => re.test(e.textContent) && e.getBoundingClientRect().height > 0);
    if (!el) return false; (el.closest('a, button') || el).click(); return true; });
  if (ok) await p.waitForTimeout(900); return ok;
}
const B = 'https://www.monte-moro.ch';
const L = JSON.parse(fs.readFileSync(__dirname + '/stellen.json'));
const nur = process.argv.slice(2);
const ABLEHNEN = /^\s*(Alle ablehnen|Rechazar todo|Reject all|Tout refuser|Ablehnen|Rechazar|Decline|Refuser)\s*$/i;
async function finde(p, txts, nth, letzt) {
  for (const txt of [].concat(txts)) {
    const r = await p.evaluate(([txt, nth, letzt]) => {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, k = 0, hits = [];
      while ((n = w.nextNode())) {
        const i = n.data.toLowerCase().indexOf(txt.toLowerCase()); if (i < 0) continue;
        const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, Math.min(n.data.length, i + txt.length));
        const q = rg.getBoundingClientRect(); const st = getComputedStyle(n.parentElement);
        const vv = window.visualViewport || { scale: 1, offsetLeft: 0, offsetTop: 0 }; if (q.width > 2 && q.height > 2 && st.visibility !== 'hidden' && st.opacity !== '0') hits.push({ top: q.top + scrollY, x: (q.left - vv.offsetLeft) * vv.scale, w: q.width * vv.scale, h: q.height * vv.scale, y: (q.top - vv.offsetTop) * vv.scale, cx: q.left + q.width / 2, cy: q.top + q.height / 2, el: null });
      }
      if (!hits.length) return null;
      return letzt ? hits[hits.length - 1] : hits[Math.min(nth || 0, hits.length - 1)];
    }, [txt, nth || 0, !!letzt]);
    if (r) return { ...r, txt };
  }
  return null;
}
async function scrollZu(p, txt, nth, letzt, hoch, H) {
  await p.evaluate(([txt, nth, letzt, hoch, H]) => {
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, hits = [];
    while ((n = w.nextNode())) { const i = n.data.toLowerCase().indexOf(txt.toLowerCase()); if (i < 0) continue; const e = n.parentElement; const q = e.getBoundingClientRect(); if (q.width > 2 && getComputedStyle(e).visibility !== 'hidden') hits.push(e); }
    const e = letzt ? hits[hits.length - 1] : hits[Math.min(nth || 0, hits.length - 1)]; if (!e) return;
    const r = e.getBoundingClientRect(); const sc = (window.visualViewport || { scale: 1 }).scale; scrollTo(0, Math.max(0, scrollY + r.top - H / sc * hoch));
  }, [txt, nth || 0, !!letzt, hoch ?? 0.42, H]);
}
(async () => {
  const b = await chromium.launch();
  const lage = fs.existsSync(OUT + 'lage.json') ? JSON.parse(fs.readFileSync(OUT + 'lage.json')) : {};
  for (const [id, pfad, o] of L) {
    if (nur.length && !nur.includes(id)) continue;
    const W = o.desk ? 1440 : 390, H = o.desk ? 900 : 844;
    const c = await b.newContext(o.desk ? { viewport: { width: W, height: H }, deviceScaleFactor: 1, locale: 'de-DE', userAgent: UA_DESK }
      : { viewport: { width: W, height: H }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: UA, locale: 'de-DE' });
    if (!o.banner) await c.addCookies([{ name: 'reDimCookieHint', value: '-1', domain: 'www.monte-moro.ch', path: '/' }]);
    let p = await c.newPage(); let box = null; p.on('dialog', d => d.dismiss().catch(() => {}));
    const url = /^https?:/.test(pfad) ? pfad : B + pfad;
    try {
      try { await p.goto(url, { waitUntil: 'load', timeout: 90000 }); } catch (e) { console.log(id, 'laden:', e.message.split('\n')[0]); }
      await p.waitForTimeout(2500);
      // einmal durchscrollen, damit nachgeladene Bilder stehen und der Cookie-Hinweis erscheint (er kommt erst bei der ersten Bewegung)
      await p.evaluate(async () => { const h = document.body.scrollHeight; for (let y = 0; y < Math.min(h, 9000); y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 70)); } scrollTo(0, 0); });
      await p.waitForTimeout(1500);
      if (!o.banner) { await weg(p); }
      else { await p.evaluate(() => scrollTo(0, 260)); await p.waitForTimeout(2500); }
      if (o.warte) await p.waitForTimeout(o.warte);
      if (!o.banner) await weg(p);
      if (o.menu) { await p.getByText(o.menu, { exact: true }).first().click({ timeout: 5000 }); await p.waitForTimeout(1800); }
      if (o.ende) { await p.evaluate(() => scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(1500); }
      if (o.y) { await p.evaluate(y => scrollTo(0, y), o.y); await p.waitForTimeout(1200); }
      if (o.tapHref) {
        const href = await p.evaluate(t => { const a = [...document.querySelectorAll('a')].find(a => a.textContent.toLowerCase().includes(t.toLowerCase())); return a ? a.href : null; }, o.tapHref);
        console.log(id, 'href', href);
        if (href) { try { await p.goto(href, { waitUntil: 'load', timeout: 30000 }); } catch (e) { console.log(id, 'ziel:', e.message.split('\n')[0]); } await p.waitForTimeout(o.warte || 2000); }
      }
      if (o.tap) {
        const pop = c.waitForEvent('page', { timeout: 8000 }).catch(() => null);
        const r = await finde(p, o.tap, o.nth, o.letzt);
        if (r) { await p.mouse.click(r.cx, r.cy); } else { await p.getByText(o.tap).last().click({ timeout: 5000 }).catch(e => console.log(id, 'tap:', e.message.split('\n')[0])); }
        const np = await pop; if (np) { p = np; try { await p.waitForLoadState('load', { timeout: 30000 }); } catch (e) {} }
        await p.waitForTimeout(o.warte || 3000);
        if (o.banner) { }   // zweiter Cookie-Hinweis ist Gegenstand des Punktes
      }
      for (let versuch = 0; versuch < 2; versuch++) {   // ein spät erscheinender Cookie-Hinweis wird weggeklickt, dann die Stelle neu gesucht
      box = null;
      if (o.text) {
        let r = await finde(p, o.text, o.nth, o.letzt);
        if (r) {
          await scrollZu(p, r.txt, o.nth, o.letzt, o.hoch, H); await p.waitForTimeout(1500);
          if (!o.banner) await weg(p);
          await scrollZu(p, r.txt, o.nth, o.letzt, o.hoch, H); await p.waitForTimeout(1200);   // zweimal: nachgeladene Bilder verschieben die Seite
          const r2 = await finde(p, r.txt, o.nth, o.letzt);
          if (r2) box = { x: r2.x, y: r2.y, w: r2.w, h: r2.h };
        } else console.log(id, 'NICHT GEFUNDEN', JSON.stringify(o.text));
      } else if (o.sel) {
        const el = p.locator(o.sel).nth(o.nth || 0);
        if (await el.count()) {
          await el.scrollIntoViewIfNeeded(); const r0 = await el.boundingBox();
          if (o.hoch !== undefined && r0) await p.evaluate(d => scrollBy(0, d), r0.y - H * o.hoch);
          await p.waitForTimeout(1200); const r = await el.boundingBox(); if (r) box = { x: r.x, y: r.y, w: r.width, h: r.height };
        } else console.log(id, 'NICHT GEFUNDEN', o.sel);
      }
      if (o.banner || !(await weg(p))) break;
      }
      if (o.kein) box = null;
      if (o.box) box = o.box;
    } catch (e) { console.log(id, 'FEHLER', e.message.split('\n')[0]); }
    await p.screenshot({ path: OUT + id + '.png', timeout: 60000 }).catch(e => console.log(id, 'KEIN BILD', e.message.split('\n')[0]));
    lage[id] = { pfad, box, url: p.url(), desk: !!o.desk, W, H }; console.log(id, JSON.stringify(box), p.url().slice(0, 90));
    fs.writeFileSync(OUT + 'lage.json', JSON.stringify(lage, null, 1));
    await c.close();
  }
  await b.close();
})();
