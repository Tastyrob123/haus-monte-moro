module.paths.push(require('path').join(require('os').homedir(), 'Aussen-Pruefung', 'node_modules'));
const { chromium } = require('playwright'); const fs = require('fs');
const S = JSON.parse(fs.readFileSync(__dirname + '/code_breit.json'));
const css = `body{margin:0;background:#0b2a4c;color:#ece6d6;font:15px/1.5 'SF Mono',Menlo,monospace;padding:26px 26px 22px;box-sizing:border-box}
h1{font:500 12px 'Helvetica Neue',sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#e2b48c;margin:0 0 16px}
.z{padding:7px 10px;border-radius:6px;margin:0 0 7px;background:rgba(255,255,255,.06)}
.n{background:rgba(190,60,40,.22);color:#ffd9cf}.n b{color:#ff9d8a}.g{color:#e2b48c}.g b{color:#fff}b{font-weight:600}
small{display:block;margin-top:14px;font:12.5px/1.5 'Helvetica Neue',sans-serif;color:#a9bfd6}`;
(async () => {
  const b = await chromium.launch(); const c = await b.newContext({ viewport: { width: 760, height: 300 }, deviceScaleFactor: 2 });
  for (const [id, s] of Object.entries(S)) { const p = await c.newPage(); await p.setContent(`<style>${css}</style><h1>${s.titel}</h1>${s.zeilen}<small>${s.fuss}</small>`); await p.screenshot({ path: __dirname + '/stellen/' + id + '.png', fullPage: true }); await p.close(); console.log(id); }
  await b.close();
})();
