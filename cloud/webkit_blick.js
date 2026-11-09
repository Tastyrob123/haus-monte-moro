// WebKit-Blick ohne Playwright-WebKit (Download in der Cloud gesperrt): WebKitWebDriver (Debian webkit2gtk-driver) unter xvfb-run.
// Je Adresse bei 1440 und 390: Seite laden, ganz durchscrollen, Fehler (window.onerror, früh eingehängt über eine Wiederholung nach dem Laden),
// waagrechter Überlauf, Bild des ersten Schirms. Aufruf: xvfb-run -a node cloud/webkit_blick.js <ausordner> <url> [url …]
const { spawn } = require('child_process'); const fs = require('fs'); const path = require('path');
const [aus, ...urls] = process.argv.slice(2); fs.mkdirSync(aus, { recursive: true });
const PORT = 4444 + Math.floor(Math.random() * 1000), B = `http://127.0.0.1:${PORT}`;
const wd = spawn('WebKitWebDriver', [`--port=${PORT}`], { stdio: 'ignore' });
const zz = ms => new Promise(r => setTimeout(r, ms));
async function c(m, p, body) { const r = await fetch(B + p, { method: m, headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined }); const j = await r.json(); if (j.value && j.value.error) throw new Error(j.value.error + ': ' + j.value.message); return j.value; }
(async () => {
  for (let i = 0; i < 50; i++) { try { await fetch(B + '/status'); break; } catch (e) { await zz(200); } }
  const s = await c('POST', '/session', { capabilities: { alwaysMatch: { browserName: 'MiniBrowser', 'webkitgtk:browserOptions': { binary: '/usr/lib/x86_64-linux-gnu/webkit2gtk-4.1/MiniBrowser', args: ['--automation'] } } } }).catch(async () => c('POST', '/session', { capabilities: {} }));
  const S = '/session/' + s.sessionId, ergebnis = [];
  for (const url of urls) for (const w of [1440, 390]) {
    // MiniBrowser wird nicht schmaler als ~447 px: schmale Breiten in einem iframe genau dieser Grösse (eigener Viewport, eigene Media Queries)
    const schmal = w < 600; let rahmen = null;
    await c('POST', S + '/frame', { id: null }).catch(() => {});
    await c('POST', S + '/window/rect', { width: schmal ? 900 : w, height: schmal ? 1000 : 900 });
    if (schmal) {
      // Rahmen auf derselben Herkunft wie die Seite (Server senden frame-ancestors 'self' / X-Frame-Options SAMEORIGIN)
      await c('POST', S + '/url', { url: new URL(url).origin + '/__webkit_rahmen_' + Date.now() });
      await c('POST', S + '/execute/sync', { script: `document.documentElement.innerHTML='<head></head><body></body>';document.body.style.margin='0';const f=document.createElement('iframe');f.id='r';f.style.cssText='border:0;width:${w}px;height:844px;display:block';f.src=arguments[0];document.body.appendChild(f);`, args: [url] });
      await zz(2500);
      rahmen = await c('POST', S + '/element', { using: 'css selector', value: '#r' });
      await c('POST', S + '/frame', { id: rahmen });
    } else { await c('POST', S + '/url', { url }); await zz(1500); }
    const r = await c('POST', S + '/execute/async', { script: `const fertig = arguments[arguments.length-1]; (async () => {
      const f = []; window.addEventListener('error', e => f.push(String(e.message)));
      for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 70)); }
      scrollTo(0, 0); await new Promise(r => setTimeout(r, 600));
      const sw = document.documentElement.scrollWidth, iw = document.documentElement.clientWidth;
      const breit = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); if (!r.width || r.right <= iw + 1) return false;
        for (let a = e.parentElement; a; a = a.parentElement) { const o = getComputedStyle(a); if (/hidden|clip|auto|scroll/.test(o.overflowX)) return false; } return getComputedStyle(e).position !== 'fixed'; }).slice(0, 3).map(e => e.tagName + '.' + String(e.className).slice(0, 40));
      fertig({ sw, iw, breit, f, titel: document.title, laenge: (document.body && document.body.innerText || '').trim().length, wo: location.href }); })();`, args: [] });
    if (schmal) await c('POST', S + '/frame', { id: null });
    const png = await c('GET', S + '/screenshot');
    const datei = path.join(aus, url.replace(/[^A-Za-z0-9]/g, '_').slice(-60) + '-' + w + '.png'); fs.writeFileSync(datei, Buffer.from(png, 'base64'));
    const leer = !r.titel || r.laenge < 40 || r.wo !== url && !r.wo.startsWith(url.split('#')[0]);
    if (leer) r.f.push('Seite nicht geladen oder leer (Titel «' + r.titel + '», ' + r.laenge + ' Zeichen, ' + r.wo + ')');
    const ok = r.sw <= r.iw + 1 && !r.breit.length && !r.f.length;
    ergebnis.push({ url, w, ok, ...r, bild: datei }); console.log((ok ? '✓ ' : '✗ ') + w + ' ' + url + (ok ? '' : ' ' + JSON.stringify({ sw: r.sw, iw: r.iw, breit: r.breit, f: r.f })));
  }
  fs.writeFileSync(path.join(aus, 'webkit.json'), JSON.stringify(ergebnis, null, 1));
  await c('DELETE', S); wd.kill(); console.log(ergebnis.every(e => e.ok) ? 'WEBKIT BESTANDEN' : 'WEBKIT DURCHGEFALLEN (' + ergebnis.filter(e => !e.ok).length + ')');
})().catch(e => { console.error(e); wd.kill(); process.exit(2); });
