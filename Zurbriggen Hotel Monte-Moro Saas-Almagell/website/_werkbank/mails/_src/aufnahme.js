// Mails des Hotels Monte-Moro (Vorlage des Werkbank-Kits, Werkbank Papier 08.11.2026): die Wortmarke als PNG für die Mails (Mailprogramme zeigen kein SVG)
// und der obere Teil jeder Mail als Bild für die Werkbank, doppelte Dichte.
// node mails/_src/aufnahme.js   (Server 9388 läuft; vorher python3 mails/_src/bau.py)  → mails/img/marke.png, _werkbank/ansichten/Mails/NN.jpg
const path = require('path'), fs = require('fs');
let pw; try { pw = require('playwright'); } catch (_) { pw = require('/opt/node-tools/node_modules/playwright'); }
const { chromium } = pw;
const ROOT = path.join(__dirname, '..', '..'), B = 'http://127.0.0.1:' + (process.env.WB_PORT || 9388) + '/';
const liste = JSON.parse(fs.readFileSync(path.join(__dirname, 'werkbank.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ headless: true });
  try {
    const z = await b.newPage({ viewport: { width: 600, height: 800 }, deviceScaleFactor: 1 });
    // das ganze Logo «Monte Moro / Saas-Almagell» in Papier für den Kopf in der Nacht des Hauses; 570 px breit für 190 px in der Mail (dreifache Dichte)
    const wm = fs.readFileSync(path.join(ROOT, '..', '..', '_werkzeuge/oberflaeche/kleid/montemoro-marke.svg'), 'utf8').replace(/<\?xml[^>]*>/, '');
    await z.setContent('<body style="margin:0;background:transparent"><div style="display:none">' + wm + '</div><div id="w" style="width:570px;color:#F5F2EE"><svg viewBox="0 0 3483 1425" fill="currentColor" style="display:block;width:570px;height:auto"><use href="#wm"/></svg></div></body>');
    fs.mkdirSync(path.join(ROOT, 'mails/img'), { recursive: true });
    await (await z.$('#w')).screenshot({ path: path.join(ROOT, 'mails/img/marke.png'), omitBackground: true });
    await z.close();
    const ziel = path.join(ROOT, '_werkbank/ansichten/Mails'); fs.mkdirSync(ziel, { recursive: true });
    for (const f of fs.readdirSync(ziel)) if (/^\d\d\.jpg$/.test(f) && !liste.some(([nr]) => nr + '.jpg' === f)) fs.unlinkSync(path.join(ziel, f));
    for (const [nr, ordner] of liste) {
      const p = await b.newPage({ viewport: { width: 640, height: 900 }, deviceScaleFactor: 2 });
      await p.goto(B + 'mails/' + ordner + '/index.html', { waitUntil: 'load', timeout: 60000 }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
      await p.screenshot({ path: path.join(ziel, nr + '.jpg'), quality: 88, clip: { x: 0, y: 0, width: 640, height: 940 }, fullPage: true });
      console.log('Mail', nr, ordner); await p.close();
    }
  } finally { await b.close(); }
})();
