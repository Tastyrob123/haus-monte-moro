/* Bilder für die Anleitung (anleitung.html): ein Bildschirmfoto je Kapitel aus dem echten Werkzeug, Beispielwerte, 1512×900 → 1200 px breit.
   node anleitung_bilder.js [basis]   (Server Besucher muss laufen, eigener Port 9386; headless Chromium, JPEG über Pillow) */
const path = require('path'), fs = require('fs');
let PW; try { PW = require('playwright'); } catch (e) { PW = require(path.join(process.env.HOME, 'Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright')); }
const A = process.argv[2] || 'http://127.0.0.1:9386/_werkzeuge/registre/';
const AUS = path.join(__dirname, 'anleitung');
const K = [
  ['k01', 'start', 0, null], ['k02', 'start', 520, null], ['k03', 'besuche', 540, null], ['k04', 'besuche', 540, async p => { await p.click('[data-filter="buchung"]'); await p.waitForTimeout(500); }],
  ['k05', 'herkunft', 400, null], ['k06', 'zeit', 470, null], ['k07', 'seiten', 470, null], ['k08', 'verlauf', 470, null], ['k09', 'buchung', 470, null],
  ['k10', 'zaehlung', 0, null]];   /* das Gasterntal hatte hier noch den Knopf «Dieses Gerät nicht mitzählen», der seit 18.10.2026 entfernt ist */
(async () => {
  const b = await PW.chromium.launch(); fs.mkdirSync(AUS, { recursive: true });
  for (const [id, v, y, vor] of K) {
    const c = await b.newContext({ viewport: { width: 1512, height: 900 }, deviceScaleFactor: 1 }); await c.addInitScript(() => { try { localStorage.setItem('rundgang-montemoro-registre', '1'); } catch (e) {} }); const p = await c.newPage();
    await p.goto(A + '?gruss=tag#' + v); await p.waitForFunction(() => window.BG_REGISTRE === 1 && document.documentElement.classList.contains('auftakt-da')); await p.waitForTimeout(3800);
    if (y) { await p.evaluate(y => window.scrollTo(0, y), y); await p.waitForTimeout(3600); }
    if (vor) await vor(p);
    /* Balken und Säulen, die erst halb im Bild stehen, zeigen im Foto schon ihren Wert (sonst leere Spuren am unteren Rand) */
    await p.evaluate(() => document.querySelectorAll('[data-r]').forEach(x => x.classList.add('rg-da', 'rg-los'))); await p.waitForTimeout(1800);
    await p.screenshot({ path: path.join(AUS, id + '.png') });
    await c.close();
  }
  await b.close();
  // PNG → JPEG 1200 px
  const { execSync } = require('child_process');
  for (const [id] of K) { const png = path.join(AUS, id + '.png'), jpg = path.join(AUS, id + '.jpg');
    execSync(`python3 -c "import sys;from PIL import Image;i=Image.open(sys.argv[1]).convert('RGB');i.resize((1200,round(i.height*1200/i.width)),Image.LANCZOS).save(sys.argv[2],quality=82)" "${png}" "${jpg}"`); fs.unlinkSync(png); }
  console.log('Bilder:', fs.readdirSync(AUS).join(' '));
})();
