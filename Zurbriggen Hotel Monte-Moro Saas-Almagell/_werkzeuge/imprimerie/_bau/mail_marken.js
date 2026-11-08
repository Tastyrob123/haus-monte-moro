/* Kopf, Fuss und Trenner der Mails als PNG (kein Mailprogramm zeigt SVG zuverlässig): die echte Wortmarke «Monte Moro / Saas-Almagell» in Papier
   auf der Nacht der Mail, Trenner als Messinglinie.   NODE_PATH=$(npm root -g) node _bau/mail_marken.js */
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const Z = path.join(__dirname, '..', 'haeuser', 'montemoro', 'mail');
const svg = fs.readFileSync(path.join(__dirname, '..', '..', 'oberflaeche', 'kleid', 'montemoro-marke.svg'), 'utf8').replace(/<symbol id="wm" viewBox="[^"]*">/, '').replace('</symbol>', '');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
  const shot = async (html, w, h, f) => { await p.setViewportSize({ width: w, height: h }); await p.setContent(`<style>html,body{margin:0;background:transparent}</style>${html}`); await p.screenshot({ path: path.join(Z, f), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }); };
  const logo = (w) => svg.replace('<svg ', `<svg fill="#F5F2EE" style="width:${w}px;height:auto;display:block;color:#F5F2EE" `);
  await shot(`<div style="width:200px;height:82px;display:grid;place-items:center">${logo(200)}</div>`, 200, 82, '_kopf.png');
  await shot(`<div style="width:120px;height:49px">${logo(120)}</div>`, 120, 49, '_fuss.png');
  await shot(`<div style="width:190px;height:30px;position:relative"><i style="position:absolute;left:20px;right:20px;top:14.5px;height:1px;background:#B39867"></i></div>`, 190, 30, '_trenner.png');
  await b.close();
})();
