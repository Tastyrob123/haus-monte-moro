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
//   9 kein Knopf, kein Text, keine Tafel wird vom nächsten Abschnitt verdeckt (runde Ecken legen sich darüber) oder vom eigenen Abschnitt abgeschnitten
//     (Robert 09.11.2026, Chalet Rustica: «Button komplett abgeschnitten … so grundlegende Themen, über die wir gar nicht erst reden müssen»)
//  10 keine Leerfläche unter der kürzeren von zwei Tafeln/Spalten nebeneinander: Inhalt verteilt sich über die Höhe, Spalten gleich hoch, letzte Rasterreihe voll
//     (Robert 09.11.2026, Besucher Schlössli: «Da ist so ein Leerbereich unten, den ich nicht haben will … Das kann doch nicht sein, dass sowas jetzt erst bei mir auffällt»)
//  11 Auftritte beim Scrollen: Was unterhalb des ersten Bildschirms steht, schwebt beim Hereinscrollen an seinen Platz (nur Seiten über 1,6 Bildschirme)
//     (Robert 09.11.2026, Markenbuch und Werkzeuge: «diese Animationen, dieses luxuriöse, edle, überall … Ich habe das Gefühl, das hast du jetzt teilweise überall rausgelöscht»)
//  12 Zurück-Pfeil aus dem Speicher des Browsers (Safari): Seiten mit Rücksprung stehen danach wieder an der alten Stelle, nicht ganz oben
//     (Robert 09.11.2026, Werkbank Schlössli: «… gehe auf die Zurücktaste und wo lande ich? Am Anfang der Werkbank»; Prüfung mit dem Prüf-Browser allein fand es nicht, weil er den Speicher nicht nutzt)
//  13 Raster und Bildflächen voll: kein Raster mit leerer Spalte in der letzten Reihe (drei Fotos in vier Spalten), keine Bildfläche aus frei gelegten Stücken, deren untere Hälfte leer bleibt
//     (Robert 09.11.2026, Werkbank Wellness & Spa: «warum fehlt da ein bild» · «warum sieht das so lächerlich leer aus»)
//  14 Text nie unter einem Nachbarn im selben Abschnitt: keine Zeile läuft hinter ein Blatt, eine Tafel oder ein Bild, das darübergelegt ist
//     (Robert 09.11.2026, Werkbank Schäfli, Zeile «Taverne zum Schäfli · Oberdorfstrasse 8» unter dem Briefblatt: «Da verschwindet der Text so hinter abgeschnitten, das ist kacke»)
//  15 Werkbank, Kapitel Unterlagen/Karten: alle Unterlagen des Hauses schweben als Blätter im Raum, nie nur zwei Blätter in leerer Fläche; die Blätter füllen ihre Fläche, nie Kacheln oder Beschreibungen (Robert 09.11.2026, 16:51)
//     (Robert 09.11.2026, Werkbank Wellness & Spa, «Ihre Karten, neu gesetzt»: «zwei Dokumente dort einfach nur erbärmlich leer … nicht zwei dumme Dokumente in der Luft hängen, obwohl es eigentlich mehr sind»)
//  16 Übersichten mit Häusern: Häuser einer Familie (gleiche Eigentümer, Liste familien.js) stehen zusammen in einem Block wie im Atelier, nie einzeln untereinander
//     (Robert 09.11.2026, Kunden «Alle Häuser»: «alles untereinander und man checkt halt nicht, was ist jetzt zusammen und was nicht»)
const { chromium } = require('/Users/robertreff/Desktop/Website-Projekte/_Befund-Vorschlaege/node_modules/playwright');
const arg = process.argv.slice(2);
const adresse = arg.find(a => /^https?:/.test(a));
const ausnahmen = []; arg.forEach((a, i) => { if (a === '--ausnahme' && arg[i + 1]) ausnahmen.push(arg[i + 1]); });
if (!adresse) { console.log('Adresse fehlt.\nDURCHGEFALLEN'); process.exit(1); }

const SCHIRM_NAME = /(^|[\/_-])(schirm|screen|screenshot|aufnahme|shot|geraet|ansicht)[-_.\d]/i;   // nur Dateinamen, die mit dem Wort beginnen (Foto «bildschirm» zählt nicht)
const SCHIRM_KLASSE = /schirm|screen|fenster|window|browser|mockup/i;
const GERAET = /laptop|handy|phone|macbook|imac|ipad|geraet|device|monitor/i;

function innerHeightGrenze() { return 450; }   // 12: eine halbe Fensterhöhe Spielraum (der Rücksprung richtet sich am Inhaltsstück aus, nicht an der Pixelzahl)

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
  // 11 Zustand vor dem Scrollen: Blöcke unterhalb des ersten Bildschirms, die noch nicht an ihrem Platz stehen
  await p.evaluate(() => { const H = innerHeight, st = e => { const s = getComputedStyle(e); return [s.opacity, s.transform, s.translate, s.scale, s.clipPath].join('|'); };
    window.__vor = [...document.querySelectorAll('body *')].filter(e => { const q = e.getBoundingClientRect(); return q.top > H * 1.15 && q.height > 30 && q.width > 60; }).map(e => [e, st(e)]); }).catch(() => {});
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
    document.querySelectorAll('[class*="--platz"],[class*="--leer"],[class*="platzhalter"],[data-leer]').forEach(e => { if (sicht(e) && !e.closest('form')) out.push('3 Platzhalter statt Inhalt in ' + abschnitt(e) + '.'); });
    document.querySelectorAll('section').forEach(s => {
      if (!sicht(s) || s.getBoundingClientRect().height < 250) return;
      const t = (s.innerText || '').replace(/\s+/g, ' ').trim();
      if (t.length < 60 && !s.querySelector('img,video,canvas,svg image,iframe')) out.push('3 Abschnitt fast leer: ' + name(s) + '.');
    });
    document.querySelectorAll('[class*="tafel"],[class*="karte"],[class*="card"]').forEach(k => {
      if (!sicht(k) || k.getBoundingClientRect().height < 120 || k.querySelector('img')) return;
      const kopie = k.cloneNode(true); kopie.querySelectorAll('button,a').forEach(x => x.remove());
      if (kopie.textContent.replace(/\s+/g, '').length < 15 && k.querySelectorAll('button,a').length <= 1) out.push('3 Leere Tafel in ' + abschnitt(k) + ' (nur ein Knopf, kein Inhalt).');
    });
    // 4 grosse Zahlen lose auf dem Hintergrund
    const hatFlaeche = e => { const s = getComputedStyle(e); const bg = s.backgroundColor; return (bg && bg !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(bg)) || s.backgroundImage !== 'none' || s.boxShadow !== 'none' || parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderLeftWidth) > 0; };
    const gemeldet = new Set();
    document.querySelectorAll('b,strong,span,div,p,em').forEach(e => {
      if (!sicht(e) || e.children.length > 1) return;
      const t = e.textContent.trim(); if (!/^[\d'’.,]+%?$/.test(t)) return;
      if (parseFloat(getComputedStyle(e).fontSize) < 28) return;
      // Zahl als Wort in einem ganzen Satz (Titel in Wort-Spans zerlegt, z. B. «40 Weltcupsiege») ist keine lose Kennzahl
      const satz = e.closest('h1,h2,h3,h4,h5,h6,p,blockquote,li'); if (satz && satz !== e && (satz.textContent.match(/[A-Za-zÀ-ÿ]{3,}/g) || []).length >= 3) return;
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
      if (/auto|scroll/.test(getComputedStyle(bd).overflowX)) return;   // Bildband zum Wischen (seitlich scrollbar) ist kein Laufband (09.11.2026, Seiler-Zimmer «Weitere Einblicke»)
      const t = bd.querySelector('li button, li, span'); if (!t) return;
      const r = bd.getBoundingClientRect(); let unten = r.bottom;
      const n = bd.nextElementSibling; if (n) { const rn = n.getBoundingClientRect(); if (rn.top < unten && rn.top > r.top) unten = rn.top; }
      const rt = t.getBoundingClientRect(), mitte = (r.top + unten) / 2, tm = (rt.top + rt.bottom) / 2;
      if (Math.abs(mitte - tm) > 3) out.push('6 Laufband: Schrift sitzt ' + Math.round(tm - mitte) + ' px neben der Mitte des sichtbaren Bands (' + name(bd) + ').');
    });
    // 14 Text unter einem späteren Nachbarn desselben Abschnitts (Blatt, Tafel, Bild mit Grund, über negativen Rand oder Lage darübergelegt)
    {
      const deckend = el => { const c = getComputedStyle(el); const m = c.backgroundColor.match(/[\d.]+/g) || []; return el.tagName === 'FIGURE' || el.tagName === 'IMG' || c.backgroundImage !== 'none' || (m.length >= 3 && (m.length < 4 || +m[3] > 0.5)); };
      const g14 = new Set();
      document.querySelectorAll('main > section, body > section').forEach(S => {
        if (!sicht(S)) return;
        const huelle = S.querySelector(':scope > .in') || S;
        const kinder = [...huelle.children].filter(k => sicht(k) && !/fixed|sticky/.test(getComputedStyle(k).position));
        kinder.forEach((B, i) => {
          const texte = [B, ...B.querySelectorAll('p, b, small, span, h1, h2, h3, h4, li, a')].filter(t => sicht(t) && [...t.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
          texte.forEach(t => {
            const r = t.getBoundingClientRect(); if (r.width < 4 || r.height < 4) return;
            for (const F of kinder.slice(i + 1)) {
              if (!deckend(F)) continue;
              const f = F.getBoundingClientRect(), w = Math.min(r.right, f.right) - Math.max(r.left, f.left), h = Math.min(r.bottom, f.bottom) - Math.max(r.top, f.top);
              if (w > 4 && h > r.height * 0.5) { const k = name(t) + name(F); if (!g14.has(k)) { g14.add(k); out.push('14 Text unter ' + name(F) + ' verschwunden: ' + name(t) + ' «' + (t.textContent || '').trim().slice(0, 30) + '» in ' + name(S) + '. Zeile an eine freie Stelle setzen.'); } break; }
            }
          });
        });
      });
    }
    // 9 Inhalt vom nächsten Abschnitt verdeckt oder vom eigenen Abschnitt abgeschnitten (Bilder dürfen unter die runde Ecke laufen, Knöpfe und Text nie)
    {
      const secs = [...document.querySelectorAll('main > section, main > div, body > footer')].filter(sicht);
      const INH = 'a, button, h1, h2, h3, h4, p, li, dt, dd, .knopf, .blatt, .tafel-holz, label, input, select, textarea';
      const gemeldet = new Set();
      secs.forEach((S, i) => {
        const N = secs[i + 1], rs = S.getBoundingClientRect(), cs = getComputedStyle(S);
        const schneidet = /clip|hidden/.test(cs.overflow + cs.overflowY);
        S.querySelectorAll(INH).forEach(e => {
          if (!sicht(e) || e.closest('figure')) return;
          const r0 = e.getBoundingClientRect(), r = { top: r0.top, bottom: r0.bottom, right: r0.right };
          // nur der sichtbare Teil zählt: Vorfahren mit overflow clip/hidden innerhalb des Abschnitts schneiden ab (z. B. geschlossene Akkordeon-Streifen)
          for (let a = e.parentElement; a && a !== S; a = a.parentElement) { const ca = getComputedStyle(a); if (/clip|hidden/.test(ca.overflow + ca.overflowY)) { const ra = a.getBoundingClientRect(); r.bottom = Math.min(r.bottom, ra.bottom); r.top = Math.max(r.top, ra.top); } }
          if (r.bottom - r.top <= 2) return;
          if (N && getComputedStyle(N).position !== 'fixed') {
            const rn = N.getBoundingClientRect();
            if (r.bottom > rn.top + 1 && r.top < rn.top - 2 && +getComputedStyle(N).zIndex >= 0) { const k = '9v' + name(e); if (!gemeldet.has(k)) { gemeldet.add(k); out.push('9 Vom nächsten Abschnitt verdeckt (' + Math.round(r.bottom - rn.top) + ' px): ' + name(e) + ' «' + (e.textContent || '').trim().slice(0, 30) + '» in ' + name(S) + '. Abstand unten vergrössern.'); } }
          }
          if (schneidet && (r.bottom > rs.bottom + 1 || r.right > rs.right + 1)) { const k = '9a' + name(e); if (!gemeldet.has(k)) { gemeldet.add(k); out.push('9 Vom eigenen Abschnitt abgeschnitten: ' + name(e) + ' «' + (e.textContent || '').trim().slice(0, 30) + '» in ' + name(S) + '.'); } }
        });
      });
    }
    // 10 Leerfläche: Tafeln/Spalten nebeneinander, deren Inhalt deutlich vor der Reihe endet (mitlaufende Spalten zählen nicht, Bilder und Bildflächen zählen als Inhalt)
    {
      const inhaltUnten = k => { let u = -1e9; const tw = document.createTreeWalker(k, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
        for (let n = tw.nextNode(); n; n = tw.nextNode()) {
          if (n.nodeType === 3) { if (!n.textContent.trim() || !sicht(n.parentElement)) continue; const rg = document.createRange(); rg.selectNodeContents(n); const r = rg.getBoundingClientRect(); if (r.height) u = Math.max(u, r.bottom); }
          else if (sicht(n) && (/^(IMG|SVG|CANVAS|VIDEO|INPUT|BUTTON|SELECT|TEXTAREA|PICTURE|IFRAME)$/i.test(n.tagName) || getComputedStyle(n).backgroundImage !== 'none' || !/rgba\([^)]*,\s*0\)$|transparent/.test(getComputedStyle(n).backgroundColor))) u = Math.max(u, n.getBoundingClientRect().bottom);
        } return u; };
      const gemeldet = new Set();
      document.querySelectorAll('body *').forEach(el => {
        const s = getComputedStyle(el); if (!/grid|flex/.test(s.display) || !sicht(el) || el.closest('footer,nav,header')) return;
        const kids = [...el.children].filter(sicht); if (kids.length < 2) return;
        const reihen = {}; kids.forEach(k => { const t = Math.round(k.getBoundingClientRect().top / 4); (reihen[t] = reihen[t] || []).push(k); });
        Object.values(reihen).forEach(r => {
          if (r.length < 2) return;
          const oben = Math.min(...r.map(k => k.getBoundingClientRect().top)), unten = Math.max(...r.map(k => k.getBoundingClientRect().bottom)), hoch = unten - oben;
          if (hoch < 200) return;
          r.forEach(k => {
            if (k.getBoundingClientRect().width < 80 || [k, ...k.querySelectorAll('*')].some(x => getComputedStyle(x).position === 'sticky')) return;   // Symbole neben Text und mitlaufende Spalten zählen nicht
            const rk = k.getBoundingClientRect(); if (kids.some(x => x !== k && x.getBoundingClientRect().top >= rk.bottom - 2 && x.getBoundingClientRect().top < unten && x.getBoundingClientRect().left < rk.right && x.getBoundingClientRect().right > rk.left)) return;   // darunter steht schon die nächste Kachel (Raster mit grossen Kacheln über zwei Reihen)
            const iu = inhaltUnten(k); if (iu < -1e8) return;
            const leer = unten - iu - (parseFloat(getComputedStyle(k).paddingBottom) || 0);
            if (leer > 100 && leer > hoch * 0.18) { const key = abschnitt(k) + name(el); if (!gemeldet.has(key)) { gemeldet.add(key); out.push('10 Leerfläche ' + Math.round(leer) + ' px unter ' + name(k) + ' in ' + abschnitt(k) + ' (Nachbar ist höher). Inhalt über die Höhe verteilen oder Spalten angleichen.'); } }
          });
        });
      });
    }
    // 13 Raster mit leerer Spalte in der letzten Reihe; Bildfläche aus frei gelegten Stücken, die unten leer bleibt
    {
      document.querySelectorAll('body *').forEach(el => {
        const s = getComputedStyle(el); if (!sicht(el) || el.closest('footer,nav,header')) return;
        if (s.display === 'grid') {
          const spalten = s.gridTemplateColumns.split(' ').filter(Boolean).length;
          const kids = [...el.children].filter(sicht);
          if (spalten >= 2 && kids.length >= 2 && kids.every(k => getComputedStyle(k).gridColumnStart === 'auto' && getComputedStyle(k).gridColumnEnd === 'auto' && (/^(IMG|PICTURE)$/.test(k.tagName) || k.querySelector('img,picture,canvas,video')))) {   // nur Bildkarten (Textlisten in zwei Spalten zählen nicht)
            const breiten = kids.map(k => k.getBoundingClientRect().width), b0 = Math.max(...breiten);
            const rest = kids.length % spalten, frei = rest ? (spalten - rest) * b0 : 0;
            if (rest && b0 > 120 && breiten.every(b => b > b0 * 0.9) && frei > 200) out.push('13 Raster nicht voll: ' + kids.length + ' Stücke in ' + spalten + ' Spalten, ' + (spalten - rest) + ' Spalte(n) leer in ' + name(el) + ' (' + abschnitt(el) + '). Spaltenzahl an die Stückzahl anpassen oder füllen.');
          }
        }
        if (s.position === 'relative' || s.position === 'absolute') {
          const kids = [...el.children].filter(sicht);
          if (kids.length >= 2 && kids.every(k => getComputedStyle(k).position === 'absolute' && k.querySelector('img,svg,canvas')) && el.offsetHeight > 150 && el.offsetWidth > 150) {
            const unten = Math.max(...kids.map(k => k.offsetTop + k.offsetHeight));
            if (unten < el.offsetHeight * 0.72) out.push('13 Bildfläche unten leer: die Stücke in ' + name(el) + ' (' + abschnitt(el) + ') enden bei ' + Math.round(unten / el.offsetHeight * 100) + ' % der Höhe. Zweite Reihe legen oder die Stücke über die Fläche verteilen.');
          }
        }
      });
    }
    // 15 Kapitel Unterlagen/Karten: so viele Blätter wie Unterlagen (Namenzug), mindestens drei, und die Blätter decken ihre Fläche
    document.querySelectorAll('#unterlagen').forEach(sec => {
      const f = sec.querySelector('.faecher'); if (!f || !sicht(f)) return;
      const bl = [...f.querySelectorAll('.blattk')].filter(sicht);
      const namen = new Set([...sec.querySelectorAll('.namenzug span')].map(x => x.textContent.trim()).filter(Boolean));
      if (namen.size > bl.length) out.push('15 Kapitel Karten zeigt ' + bl.length + ' Blätter, das Haus hat ' + namen.size + ' Unterlagen (' + [...namen].join(', ') + '). Alle Unterlagen als Blätter auslegen.');
      else if (bl.length && bl.length < 3) out.push('15 Kapitel Karten: nur ' + bl.length + ' Blätter in der Fläche. Weitere Blätter des Hauses im Raum schweben lassen, nie zwei Blätter in der Luft; keine Kacheln oder Beschreibungen dazu.');
      const text = [...f.querySelectorAll('p,dl,dd,h3,h4,strong,small')].filter(sicht);   // Robert 16:51: nur Blätter, nie Kacheln oder Beschreibungen
      if (text.length || sec.querySelector('.karten__zahl')) out.push('15 Kapitel Karten trägt Kacheln oder Beschreibungen zu den Blättern (' + (text[0] ? text[0].textContent.trim().slice(0, 40) : 'Zahlenreihe') + ' …). Nur die Blätter im Raum schweben lassen, Text und Knöpfe wie vorher.');
      const k = f.closest('.karten') || sec, kr = k.getBoundingClientRect(), fr = f.getBoundingClientRect();
      if (bl.length && innerWidth >= 900 && kr.height > 300) {   // nur nebeneinander (Text links, Blätter rechts); am Handy steht alles untereinander
        const oben = Math.min(...bl.map(b => b.getBoundingClientRect().top)), unten = Math.max(...bl.map(b => b.getBoundingClientRect().bottom));
        const flaeche = bl.reduce((a, b) => { const r = b.getBoundingClientRect(); return a + r.width * r.height; }, 0), spalte = fr.width * kr.height;
        if ((unten - oben) < kr.height * 0.6 || flaeche / spalte < 0.35) out.push('15 Kapitel Karten wirkt leer: die Blätter füllen ' + Math.round((unten - oben) / kr.height * 100) + ' % der Höhe neben dem Text und decken ' + Math.round(flaeche / spalte * 100) + ' % ihrer Spalte. Mehr Blätter oder grössere Blätter im Raum, keine Kacheln oder Beschreibungen.');
      }
    });
    // 16 Häuser einer Familie stehen zusammen in einem Block (nur Seiten, die familien.js laden und Häuser als [data-kl-haus] zeigen)
    (window.TASTY_FAMILIEN || []).forEach(f => {
      const da = f.ids.map(id => document.querySelector('[data-kl-haus="' + id + '"]')).filter(Boolean);
      if (da.length < 2) return;
      const bl = new Set(da.map(e => e.closest('[data-kl-familie]')));
      if (bl.size > 1 || bl.has(null)) out.push('16 Häuser von «' + f.t[0].replace(/\.$/, '') + '» stehen nicht zusammen in einem Block: oben die gemeinsame Startseite, darunter die Häuser, wie im Atelier.');
    });
    // 11 Auftritte beim Scrollen
    if (document.documentElement.scrollHeight > innerHeight * 1.6 && window.__vor && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const st = e => { const s = getComputedStyle(e); return [s.opacity, s.transform, s.translate, s.scale, s.clipPath].join('|'); };
      const kamen = window.__vor.filter(([e, v]) => e.isConnected && st(e) !== v).length;
      if (!kamen) out.push('11 Nichts schwebt beim Scrollen herein: unterhalb des ersten Bildschirms steht alles still. Auftritte wie in den abgenommenen Häusern einbauen.');
    }
    // 17 Keine Schrift unter 12,4 px (Robert 09.11.2026, Werkbank Sroka: «solchen kleinen Schriften, die da irgendwo mittig hängen. Mit denen keiner was anfangen kann»)
    { const klein = {};
      document.querySelectorAll('body *').forEach(e => {
        if (e.closest('svg,[aria-hidden="true"],iframe,.ins-sc,.schau')) return;
        if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
        const cs = getComputedStyle(e), q = e.getBoundingClientRect();
        if (q.width < 2 || q.height < 2 || cs.visibility === 'hidden' || +cs.opacity === 0) return;
        const fs = parseFloat(cs.fontSize);
        if (fs < 12.4) { const k = (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : e.tagName.toLowerCase()); klein[k] = klein[k] || [fs, e.textContent.trim().slice(0, 30)]; }
      });
      const ks = Object.entries(klein);
      if (ks.length) out.push('17 Schrift unter 12,4 px: ' + ks.slice(0, 8).map(([k, [fs, tx]]) => k + ' ' + fs.toFixed(1) + ' px «' + tx + '»').join(' · ') + (ks.length > 8 ? ' · und ' + (ks.length - 8) + ' weitere' : '') + '. Auf mindestens 13 px anheben.'); }
    // 18 Kein Leerraum über 380 px zwischen zwei Inhalten (Robert 09.11.2026, Werkbank Sroka: «Was ist es da für ein erbärmlicher Leerraum mit Kapitel 5»); Fenster zählen nicht (auch .bruch, so heissen die Fenster im Seiler au Lac, und .durchblick im roots)
    { const ys = [];
      document.querySelectorAll('h1,h2,h3,h4,p,li,img,svg,a,button,figure,video,canvas,dt,dd,small,b,span,label,input,textarea,select').forEach(e => {
        if (e.closest('[aria-hidden="true"]') && !e.matches('img')) return;
        if (e.closest('.wfen,.standbild,.fenster,[class*="fenster"],.bruch,.durchblick,body > header,body > nav,body > footer,.insel,.leiste')) return;
        const q = e.getBoundingClientRect(), cs = getComputedStyle(e);
        if (q.width < 4 || q.height < 4 || cs.visibility === 'hidden' || +cs.opacity === 0 || cs.position === 'fixed') return;
        if (!e.matches('img,svg,video,canvas,input,textarea,select') && !e.textContent.trim()) return;
        ys.push([q.top + scrollY, q.bottom + scrollY, e]);
      });
      ys.sort((x, y) => x[0] - y[0]);
      const fen = [...document.querySelectorAll('.wfen,.standbild,.fenster,[class*="fenster"],.bruch,.durchblick')].map(f => { const r = f.getBoundingClientRect(); return [r.top + scrollY, r.bottom + scrollY]; });
      let ende = ys.length ? ys[0][1] : 0;
      for (const [a, c, e] of ys) {
        const luecke = a - ende;
        if (luecke > 380 && !fen.some(([f0, f1]) => f0 < a && f1 > ende)) { const s = e.closest('section[id]'); out.push('18 Leerraum von ' + Math.round(luecke) + ' px vor «' + (e.textContent.trim().slice(0, 30) || e.tagName.toLowerCase()) + '»' + (s ? ' (#' + s.id + ')' : '') + '. Abstand verkleinern oder die Fläche füllen.'); break; }
        ende = Math.max(ende, c);
      } }
    // 8 Werkbank, Kapitel Werkzeuge: jedes Werkzeug hat seine Adresse und einen Knopf zum Öffnen (Robert 08.11.2026: «Bei den Werkzeugen fehlen die Buttons … dummer Fehler»)
    document.querySelectorAll('.ins-t[data-i]').forEach(t => {
      const n = t.getAttribute('aria-label') || t.dataset.i;
      if (!t.dataset.url) out.push('8 Werkzeug ohne Adresse in der Werkbank: ' + n + ' (Klick auf den Bildschirm öffnet nichts). Server starten und neu bauen.');
      if (!t.querySelector('.kn-reihe a[href]')) out.push('8 Werkzeug ohne Knopf «öffnen»: ' + n + '.');
    });
    return out;
  }, { SN: SCHIRM_NAME.source, SK: SCHIRM_KLASSE.source, GE: GERAET.source });
  // 8 Jede Werkzeug-Adresse der Werkbank antwortet (sonst öffnet der Knopf eine tote Seite)
  const wege = await p.evaluate(() => [...new Set([...document.querySelectorAll('.ins-t[data-url]')].map(t => t.dataset.url).filter(Boolean))]).catch(() => []);
  for (const w of wege) { const r = await p.request.get(new URL(w, p.url()).href, { timeout: 8000 }).catch(() => null); if (!r || r.status() >= 400) befund.push('8 Werkzeug antwortet nicht: ' + w); }
  // 12 Zurück aus dem Speicher (bfcache): Weggehen, Seite steht oben, pageshow mit persisted muss die alte Stelle wieder herstellen
  if (breite === 1440) {
    const r12 = await p.evaluate(async () => {
      if (!document.getElementById('ruecksprung') || document.documentElement.scrollHeight < innerHeight * 3) return null;
      scrollTo(0, Math.round(document.documentElement.scrollHeight * .5)); await new Promise(r => setTimeout(r, 500));
      const y0 = scrollY; dispatchEvent(new PageTransitionEvent('pagehide', { persisted: true }));
      scrollTo(0, 0); await new Promise(r => setTimeout(r, 80)); dispatchEvent(new PageTransitionEvent('pageshow', { persisted: true }));
      await new Promise(r => setTimeout(r, 2800)); return [y0, scrollY];
    }).catch(() => null);
    if (r12 && Math.abs(r12[1] - r12[0]) > innerHeightGrenze(r12[0])) befund.push('12 Zurück-Pfeil aus dem Speicher landet bei ' + Math.round(r12[1]) + ' px statt bei ' + Math.round(r12[0]) + ' px (Safari). Rücksprung aus _Werkbank-Kit/ruecksprung.js neu einsetzen.');
  }
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
