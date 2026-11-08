// node _bau/mass.js <url> <css-selektor> [breite]: Lage und berechnete Stile der Treffer
const { chromium } = require('playwright');
(async () => {
  const [url, sel, br] = process.argv.slice(2);
  const b = await chromium.launch(), p = await (await b.newContext({ viewport: { width: +(br || 1440), height: +(process.argv[5] || 900) } })).newPage();
  await p.addInitScript(() => { try { localStorage.setItem('rundgang-montemoro-registre', '1'); } catch (e) {} });
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(2500);
  const r = await p.evaluate(s => [...document.querySelectorAll(s)].slice(0, 12).map(e => { const q = e.getBoundingClientRect(), c = getComputedStyle(e);
    return { t: (e.textContent || '').trim().slice(0, 30), y: Math.round(q.top), h: Math.round(q.height), x: Math.round(q.left), w: Math.round(q.width), pos: c.position, tr: c.transform, mt: c.marginTop, disp: c.display, op: c.opacity, anim: c.animationName }; }), sel);
  console.log(JSON.stringify(r, null, 1)); await b.close();
})();
