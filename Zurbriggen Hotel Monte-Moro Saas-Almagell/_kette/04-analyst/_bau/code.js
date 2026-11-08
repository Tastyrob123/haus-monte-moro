module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
const S = JSON.parse(fs.readFileSync(__dirname + '/code.json'));
const css = `body{margin:0;background:#0b2a4c;color:#ece6d6;font:14.5px/1.5 'SF Mono',Menlo,monospace;padding:64px 20px 30px;min-height:844px;box-sizing:border-box}
h1{font:500 12px 'Helvetica Neue',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#e2b48c;margin:0 0 20px}
.z{padding:7px 10px;border-radius:6px;margin:0 0 8px;background:rgba(255,255,255,.06);word-break:break-all;overflow-wrap:anywhere}
.n{background:rgba(190,60,40,.22);color:#ffd9cf}.n b{color:#ff9d8a}.g{color:#e2b48c}.g b{color:#fff}b{font-weight:600}
small{display:block;margin-top:18px;font:12px/1.5 'Helvetica Neue',sans-serif;color:#a9bfd6}`;
(async () => {
  const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  for (const [id, s] of Object.entries(S)) { const p = await c.newPage(); await p.setContent(`<style>${css}</style><h1>${s.titel}</h1>${s.zeilen}<small>${s.fuss}</small>`); await p.screenshot({ path: __dirname + '/stellen/' + id + '.png' }); await p.close(); console.log(id); }
  await b.close();
})();
