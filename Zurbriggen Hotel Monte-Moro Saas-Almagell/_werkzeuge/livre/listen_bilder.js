/* Das Markenbuch · Hotel Monte-Moro · Bilder für die Listen «Schriften» und «Farben» (Robert 20.10.2026: «in allen Tools Bilder dazu»): je Schrift ein Ausschnitt
   der Website, so wie sie dort steht (nur lesen, unsichtbar, ein Browser, «weniger Bewegung», damit nichts mitten im Auftritt steht); dazu ein Ausschnitt
   eines hellen Abschnitts in Papier (Gruppe «Schrift»).
   Aufruf aus bau.py: node listen_bilder.js <zielordner> <adresse der seite> …  → listen/<name>.png (danach in bau.py zu WebP) */
const path = require('path');
const { chromium } = require('playwright');
const [, , ZIEL, ...SEITEN] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  // je Wunsch: erstes Element im Wähler, sichtbar, rein in dieser Schrift, 10 bis 120 Zeichen (Fliesstext ab 60)
  const WUNSCH = [['schrift-t', 'Fjalla One', 'h2, h1, h3'], ['schrift-e', 'DM Mono', '.ueber'], ['schrift-s', 'Instrument Sans', 'p'], ['schrift-z', 'DM Mono', 'td, dd, li, span, b, small']];
  const offen = async SEITE => {
    await p.goto(SEITE, { waitUntil: 'load' });
    await p.evaluate(async () => { document.documentElement.classList.add('ruhig'); document.querySelectorAll('.kopf').forEach(k => { k.style.visibility = 'hidden'; }); document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; }); await document.fonts.ready; });
    for (let y = 0; y < 40000; y += 700) { const h = await p.evaluate(y => { scrollTo(0, y); return document.body.scrollHeight; }, y); await p.waitForTimeout(30); if (y > h) break; }
  };
  for (const [name, schrift, wahl] of WUNSCH) {
    let box = null;
    for (const SEITE of SEITEN) {
      await offen(SEITE);
      const ziel = await p.evaluate(([schrift, wahl, name]) => {
        document.querySelectorAll('[data-livre-probe]').forEach(x => x.removeAttribute('data-livre-probe'));
        const el = [...document.querySelectorAll(wahl)].find(e => {
          const s = getComputedStyle(e), t = (e.textContent || '').trim().replace(/\s+/g, ' '), r = e.getBoundingClientRect();
          if (!schrift) return r.width > 900 && r.height > 300 && s.display !== 'none';
          const rein = [...e.querySelectorAll('*')].every(k => getComputedStyle(k).fontFamily === s.fontFamily);
          const zahl = name !== 'schrift-z' || (/\d/.test(t) && /CHF|\d:\d\d|Uhr|\d\.\d\d/.test(t));
          return rein && zahl && (name !== 'schrift-s' || t.length >= 100) && (name !== 'schrift-e' || r.width < 520) && s.fontFamily.includes(schrift) && t.length >= 10 && t.length <= (name === 'schrift-s' ? 400 : 120) && r.width > 140 && r.height > 10 && r.height < 300
            && s.visibility !== 'hidden' && +s.opacity > .9 && !e.closest('nav,header,footer,.kopf,.menue,[aria-hidden="true"]');
        });
        if (!el) return null;
        el.setAttribute('data-livre-probe', '1'); return true;
      }, [schrift, wahl, name]);
      if (!ziel) continue;
      const loc = p.locator('[data-livre-probe]').first();
      await loc.evaluate(e => e.scrollIntoView({ block: 'center' })); await p.waitForTimeout(900);
      const r = await loc.boundingBox();
      box = schrift ? { x: Math.max(0, r.x - 28), y: Math.max(0, r.y - 14), width: Math.min(r.width + 56, 1440 - Math.max(0, r.x - 28)), height: Math.min(r.height + 28, 900) }
        : { x: 0, y: Math.max(0, r.y), width: 1440, height: Math.min(r.height, 640, 900 - Math.max(0, r.y)), x: Math.max(0, r.x), width: Math.min(r.width, 1440) };
      break;
    }
    if (!box) { console.log('nicht gefunden', name); continue; }
    await p.screenshot({ path: path.join(ZIEL, name + '.png'), clip: box });
    console.log('ok', name);
  }
  await b.close();
})();
