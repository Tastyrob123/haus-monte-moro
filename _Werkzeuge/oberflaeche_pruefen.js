// oberflaeche_pruefen.js · Prüft eine Oberfläche (Zentrale, Werkbank, Werkzeug-Übersicht, Landingpage) auf die Punkte,
// die Robert an solchen Seiten immer wieder beanstandet hat. Läuft, bevor eine Seite zu Robert geht.
//   node ~/Desktop/Website-Projekte/_Werkzeuge/oberflaeche_pruefen.js <adresse> [--ausnahme "Punkt: Grund"]
// Ergebnis: letzte Zeile BESTANDEN oder DURCHGEFALLEN. Punkte (Robert 06.–08.11.2026, Zentrale der internen Werkzeuge):
//   1 Aufnahmen von Werkzeugen/Websites nur in Blender-Geräten (Laptop/Handy), nie als flaches Fenster
//   2 je Abschnitt eine Ansicht, nie zwei Bildschirme übereinander
//   3 kein leerer Abschnitt, kein Platzhalter, keine leere Tafel
//   4 grosse Zahlen nie lose auf dem Hintergrund, immer in einer Tafel
//   5 nicht dasselbe kleine Bild in jeder Zeile
//   6 Laufband: Schrift mittig im sichtbaren Band
//   7 keine Fehler, kein fehlendes Bild, nichts läuft über den Rand (1440 und 390)
const { chromium } = require('/Users/robertreff/Desktop/Website-Projekte/_Befund-Vorschlaege/node_modules/playwright');
const arg = process.argv.slice(2);
const adresse = arg.find(a => /^https?:/.test(a));
const ausnahmen = []; arg.forEach((a, i) => { if (a === '--ausnahme' && arg[i + 1]) ausnahmen.push(arg[i + 1]); });
if (!adresse) { console.log('Adresse fehlt.\nDURCHGEFALLEN'); process.exit(1); }

const SCHIRM_NAME = /(^|[\/_-])(schirm|screen|screenshot|aufnahme|shot|geraet|ansicht)[-_.\d]/i;   // nur Dateinamen, die mit dem Wort beginnen (Foto «bildschirm» zählt nicht)
const SCHIRM_KLASSE = /schirm|screen|fenster|window|browser|mockup/i;
const GERAET = /laptop|handy|phone|macbook|imac|ipad|geraet|device|monitor/i;

async function pruefe(b, breite) {
  const p = await b.newPage({ viewport: { width: breite, height: 900 } });
  const fehler = [];
  p.on('pageerror', e => fehler.push('Skriptfehler: ' + e.message.split('\n')[0]));
  p.on('console', m => { if (m.type() === 'error') fehler.push('Fehler in der Seite: ' + m.text().slice(0, 140)); });
  p.on('response', r => { if (r.status() >= 400 && /\.(webp|png|jpe?g|svg|gif|avif|css|js|woff2?)(\?|$)/i.test(r.url())) fehler.push('Datei fehlt (' + r.status() + '): ' + r.url()); });
  await p.addInitScript(() => { try { for (const k of Object.keys(localStorage)) if (/rundgang/i.test(k)) localStorage.setItem(k, '1'); } catch (e) {} });
  await p.goto(adresse, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => fehler.push('Seite lädt nicht: ' + e.message.split('\n')[0]));
  await p.waitForTimeout(800);
  for (const t of ['Überspringen', 'Schliessen']) await p.getByText(t, { exact: true }).first().click({ timeout: 800 }).catch(() => {});
  await p.keyboard.press('Escape');
  // alles einmal durchscrollen, damit Bilder laden und Auftritte fertig sind
  await p.evaluate(async () => {
    document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
    const H = document.documentElement.scrollHeight;
    for (let y = 0; y < H; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
    scrollTo(0, 0);
  });
  await p.waitForTimeout(2500);
  const befund = await p.evaluate(({ SN, SK, GE }) => {
    const SCHIRM_NAME = new RegExp(SN, 'i'), SCHIRM_KLASSE = new RegExp(SK, 'i'), GERAET = new RegExp(GE, 'i');
    const out = [], name = el => (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : el.tagName.toLowerCase());
    const abschnitt = el => { const s = el.closest('section,[id]'); return s ? name(s) : name(el); };
    const sicht = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el); return r.width > 2 && r.height > 2 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
    const abs = el => { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
    if (document.documentElement.scrollWidth > innerWidth + 1) out.push('7 Die Seite läuft seitlich über den Rand.');
    document.querySelectorAll('img').forEach(i => { if (i.complete && i.naturalWidth === 0 && sicht(i)) out.push('7 Bild lädt nicht: ' + (i.getAttribute('src') || '').slice(0, 90)); });
    // 1 + 2 Bildschirm-Aufnahmen
    const schirme = [...document.querySelectorAll('img')].filter(i => sicht(i) && i.naturalWidth >= 900 && !GERAET.test(i.src) && (SCHIRM_NAME.test(i.src) || [...Array(4)].reduce((e) => e && e.parentElement, i) && (() => { let e = i.parentElement; for (let k = 0; k < 4 && e; k++, e = e.parentElement) if (SCHIRM_KLASSE.test(e.className || '')) return true; return false; })()));
    schirme.forEach(i => {
      let e = i.parentElement, imGeraet = /geraet/i.test(i.src) && false;
      for (let k = 0; k < 4 && e && !imGeraet; k++, e = e.parentElement) if ([...e.querySelectorAll('img')].some(x => x !== i && GERAET.test(x.src))) imGeraet = true;
      if (!imGeraet) out.push('1 Flaches Bildschirmbild ohne Gerät in ' + abschnitt(i) + ' (' + i.src.split('/').pop() + '). In einen Blender-Laptop oder ein Blender-Handy setzen.');
    });
    for (let a = 0; a < schirme.length; a++) for (let c = a + 1; c < schirme.length; c++) {
      const r1 = abs(schirme[a].closest('figure') || schirme[a]), r2 = abs(schirme[c].closest('figure') || schirme[c]);
      const ix = Math.max(0, Math.min(r1.x + r1.w, r2.x + r2.w) - Math.max(r1.x, r2.x)), iy = Math.max(0, Math.min(r1.y + r1.h, r2.y + r2.h) - Math.max(r1.y, r2.y));
      if (ix * iy > 0.04 * Math.min(r1.w * r1.h, r2.w * r2.h)) out.push('2 Zwei Bildschirme liegen übereinander in ' + abschnitt(schirme[a]) + '. Eine Ansicht je Abschnitt.');
    }
    // 3 leere Abschnitte, Platzhalter, leere Tafeln
    document.querySelectorAll('[class*="--platz"],[class*="--leer"],[class*="platzhalter"],[data-leer]').forEach(e => { if (sicht(e)) out.push('3 Platzhalter statt Inhalt in ' + abschnitt(e) + '.'); });
    document.querySelectorAll('section').forEach(s => {
      if (!sicht(s) || s.getBoundingClientRect().height < 250) return;
      const t = (s.innerText || '').replace(/\s+/g, ' ').trim();
      if (t.length < 60 && !s.querySelector('img,video,canvas,svg image')) out.push('3 Abschnitt fast leer: ' + name(s) + '.');
    });
    document.querySelectorAll('[class*="tafel"],[class*="karte"],[class*="card"]').forEach(k => {
      if (!sicht(k) || k.getBoundingClientRect().height < 120 || k.querySelector('img')) return;
      const kopie = k.cloneNode(true); kopie.querySelectorAll('button,a').forEach(x => x.remove());
      if (kopie.textContent.replace(/\s+/g, '').length < 15) out.push('3 Leere Tafel in ' + abschnitt(k) + ' (nur ein Knopf, kein Inhalt).');
    });
    // 4 grosse Zahlen lose auf dem Hintergrund
    const hatFlaeche = e => { const s = getComputedStyle(e); const bg = s.backgroundColor; return (bg && bg !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(bg)) || s.backgroundImage !== 'none' || s.boxShadow !== 'none' || parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderLeftWidth) > 0; };
    const gemeldet = new Set();
    document.querySelectorAll('b,strong,span,div,p,em').forEach(e => {
      if (!sicht(e) || e.children.length > 1) return;
      const t = e.textContent.trim(); if (!/^[\d'’.,]+%?$/.test(t)) return;
      if (parseFloat(getComputedStyle(e).fontSize) < 28) return;
      let a = e.parentElement, lose = true;
      while (a && a !== document.body) {
        if (a.matches('section,main,header,footer,body')) break;
        if (hatFlaeche(a)) { lose = false; break; }
        a = a.parentElement;
      }
      const s = abschnitt(e);
      if (lose && !gemeldet.has(s)) { gemeldet.add(s); out.push('4 Grosse Zahl steht lose auf dem Hintergrund in ' + s + ' («' + t + '»). In die Tafel holen.'); }
    });
    // 5 dasselbe kleine Bild in vielen Zeilen
    const klein = {}; document.querySelectorAll('img').forEach(i => { const r = i.getBoundingClientRect(); if (sicht(i) && r.width < 140 && r.width > 20) (klein[i.src] = klein[i.src] || []).push(i); });
    Object.entries(klein).forEach(([src, l]) => { if (l.length >= 4 && !/zeichen|logo|icon|avatar|portr/i.test(src) && !GERAET.test(src)) out.push('5 Dasselbe Bild steht ' + l.length + '-mal in ' + abschnitt(l[0]) + ' (' + src.split('/').pop() + '). Durch etwas ersetzen, das die Zeile unterscheidet.'); });
    // 6 Laufband mittig
    document.querySelectorAll('[class*="band"],[class*="laufband"],[class*="marquee"],[class*="ticker"],[data-laufband]').forEach(bd => {
      if (!sicht(bd) || getComputedStyle(bd).overflow.indexOf('hidden') < 0) return;
      const t = bd.querySelector('li button, li, span'); if (!t) return;
      const r = bd.getBoundingClientRect(); let unten = r.bottom;
      // Ein Laufband ist ein Schriftstreifen. Bildbänder zum Blättern (Karten mit Fotos, höher als 160 px) sind keins (Beleg 08.11.2026, Werkbank Monte-Moro:
      // die Ziffer «01» auf dem ersten Bild im Ideen- und Gästeband wurde gegen die Bandmitte gemessen). [data-laufband] wird immer gemessen.
      if (!bd.hasAttribute('data-laufband') && r.height > 160 && bd.querySelector('img,picture,video')) return;
      const n = bd.nextElementSibling; if (n) { const rn = n.getBoundingClientRect(); if (rn.top < unten && rn.top > r.top) unten = rn.top; }
      const rt = t.getBoundingClientRect(), mitte = (r.top + unten) / 2, tm = (rt.top + rt.bottom) / 2;
      if (Math.abs(mitte - tm) > 3) out.push('6 Laufband: Schrift sitzt ' + Math.round(tm - mitte) + ' px neben der Mitte des sichtbaren Bands (' + name(bd) + ').');
    });
    return out;
  }, { SN: SCHIRM_NAME.source, SK: SCHIRM_KLASSE.source, GE: GERAET.source });
  await p.close();
  return [...new Set(fehler.map(f => '7 ' + f).concat(befund))].map(x => breite + ' px · ' + x);
}

(async () => {
  const b = await chromium.launch();
  let alle = [];
  for (const w of [1440, 390]) alle = alle.concat(await pruefe(b, w));
  await b.close();
  const offen = alle.filter(x => !ausnahmen.some(a => x.includes(a.split(':')[0].trim())));
  console.log('Geprüft: ' + adresse);
  if (offen.length) console.log(offen.map(x => '✗ ' + x).join('\n'));
  if (ausnahmen.length) console.log('Ausnahmen: ' + ausnahmen.join(' | '));
  console.log(offen.length ? 'DURCHGEFALLEN (' + offen.length + ')' : 'BESTANDEN');
  process.exit(offen.length ? 1 : 0);
})();
