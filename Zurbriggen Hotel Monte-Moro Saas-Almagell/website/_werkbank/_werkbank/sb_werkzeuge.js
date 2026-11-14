// Bildschirme der sieben Werkzeuge für die Werkbank des Hotel Monte-Moro (Werkbank Kern, 08.11.2026, Vorlage aus dem Stamm). Adresse aus _werkbank/werkzeuge.json (Lieferung der Werkzeug-Chats)
// (_kette/11-werkbank/werkzeuge/<teil>/stand.json, nur «liegt vor» oder «bestätigt»).   node _werkbank/sb_werkzeuge.js [schlüssel …] [--alle]
//   → ansichten/Werkzeuge/<schlüssel>.jpg (Rechner 1440 × 900, doppelte Dichte), <schlüssel>-2.jpg (eine Bildschirmhöhe weiter), ansichten/Werkzeuge-Handy/<schlüssel>.jpg (390 × 844)
// Nur ansehen: nichts wird gespeichert, nichts abgeschickt. --alle nimmt auch Werkzeuge, die noch «läuft» melden (Probebild, nie für die Meldung).
const path = require('path'), fs = require('fs');
let PW; try { PW = require('playwright'); } catch (e) { PW = require(require('path').join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright')); }
const { chromium } = PW;
const HIER = __dirname, PROJEKT = path.join(HIER, '..', '..', '..');   // _werkbank liegt in website/_werkbank
const TEIL = { maison: 'zentrale', bureau: 'website', carte: 'karten', reception: 'gaeste', livre: 'marke', registre: 'besuche', imprimerie: 'druck' };
// die zweite Aufnahme zeigt eine eigene Ansicht, wo das Werkzeug eine hat (sonst eine Bildschirmhöhe weiter)
const ZWEITE = {};
const AUFNAHME = { registre: '?gruss=tag' };   // Rechner 1440 × 932 = Bildschirm des Laptops (geraete/laptop.json); bei 900 schnitt rh_werkzeuge links und rechts je 24 px ab (Tresen-Kacheln am Rand, 30.10.)
// zweite Ansicht aus der Lieferung des Werkzeugs (das Werkzeug scrollt in einer Fläche, eine Bildschirmhöhe weiter zeigte dasselbe)
const ZWEITE_BILD = {};
const DRITTE_BILD = {};
const arg = process.argv.slice(2), alle = arg.includes('--alle'), nur = arg.filter(a => !a.startsWith('--'));
(async () => {
  for (const d of ['Werkzeuge', 'Werkzeuge-Handy']) fs.mkdirSync(path.join(HIER, 'ansichten', d), { recursive: true });
  const b = await chromium.launch({ headless: true });
  for (const [k, t] of Object.entries(TEIL)) {
    if (nur.length && !nur.includes(k)) continue;
    const p0 = path.join(PROJEKT, '_kette/11-werkbank/werkzeuge', t, 'stand.json');
    const st = fs.existsSync(p0) ? JSON.parse(fs.readFileSync(p0, 'utf8')) : {};
    // Robert 20.10.2026 «Da fehlt ein Tool»: alle sieben stehen immer in der Werkbank; ohne gemeldete Adresse der Stand vom Prüfserver des Werkzeug-Chats (nur ansehen)
    const WJ = path.join(HIER, 'werkzeuge.json'), PRUEF = fs.existsSync(WJ) ? JSON.parse(fs.readFileSync(WJ, 'utf8')) : {};
    if (PRUEF[k]) { st.adresse = PRUEF[k]; st.zustand = 'liegt vor'; }
    if (!st.adresse || (!alle && !['liegt vor', 'bestätigt'].includes(st.zustand))) { console.log('wartet', k, st.zustand || ''); continue; }
    for (const [art, vp, dsf] of [['Werkzeuge', { width: 1440, height: 932 }, 2], ['Werkzeuge-Handy', { width: 390, height: 844 }, 2]]) {
      const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: dsf, ...(vp.width < 700 ? { isMobile: true, hasTouch: true } : {}) });
      const p = await ctx.newPage(); await p.clock.install({ time: new Date('2026-11-08T10:30:00') });   // eine Uhrzeit für alle Werkzeuge: gleicher Gruss überall
      await p.addInitScript(() => { try { localStorage.setItem('ws-livre-willkommen', '1'); for (const h of ['montemoro']) { localStorage.setItem('ds-' + h + '-willkommen', '1'); localStorage.setItem('ds-' + h + '-rundgang', '1'); for (const w of ['maison', 'bureau', 'carte', 'reception', 'livre', 'registre', 'imprimerie']) localStorage.setItem('rundgang-' + h + '-' + w, '1'); } if (!localStorage.getItem('lc-wer')) { localStorage.setItem('lc-wer', 'Team Monte-Moro'); localStorage.setItem('lc-rolle', 'direktion'); } } catch (e) {} });
      try {
        await p.goto(st.adresse + (AUFNAHME[k] || ''), { waitUntil: 'load', timeout: 30000 }); await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(3500);
        await p.screenshot({ path: path.join(HIER, 'ansichten', art, k + '.jpg'), quality: 88 });
        if (art === 'Werkzeuge') {
          if (ZWEITE_BILD[k] && fs.existsSync(ZWEITE_BILD[k])) { await p.goto('file://' + ZWEITE_BILD[k]); await p.setViewportSize({ width: 1440, height: 900 }); await p.waitForTimeout(500); }
          else if (ZWEITE[k]) { await p.goto(st.adresse.replace(/\/?$/, '/') + ZWEITE[k], { waitUntil: 'load', timeout: 30000 }); await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(3500); }
          else { await p.evaluate(() => { scrollTo(0, innerHeight * .9); const f = [...document.querySelectorAll('*')].filter(x => x.scrollHeight > x.clientHeight + 200 && /auto|scroll/.test(getComputedStyle(x).overflowY) && x.clientHeight > 300).sort((a, b) => b.clientHeight - a.clientHeight)[0]; if (f) f.scrollTop = f.clientHeight * .85; }); await p.waitForTimeout(3500); }   // Werkzeuge mit eigener Scrollfläche (Plakatwerkstatt) rollen innen   // Tresen 30.10.: Zoom und Zählen erst nach 3 s fertig
          await p.screenshot({ path: path.join(HIER, 'ansichten', art, k + '-2.jpg'), quality: 88 });
          if (DRITTE_BILD[k] && fs.existsSync(DRITTE_BILD[k])) { await p.goto('file://' + DRITTE_BILD[k]); await p.waitForTimeout(500); await p.screenshot({ path: path.join(HIER, 'ansichten', art, k + '-3.jpg'), quality: 88 }); }
        }
        console.log('aufgenommen', k, art, st.adresse);
      } catch (e) { console.log('fehlgeschlagen', k, art, String(e).slice(0, 120)); }
      await ctx.close();
    }
  }
  await b.close();
})();
