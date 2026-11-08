/* kleid/montemoro.js · Hauswerte für oberflaeche.js (Hotel Monte-Moro mit Restaurant Röstihüs, Saas-Almagell; Gastgeber Esther und Fabian Zurbriggen; Oberchef 08.11.2026).
   Im <head> VOR allen Stilen laden (ohne defer). Rahmen «Die Bühne»: Kopf dunkel wie die Nacht über dem Saastal (#0A2A4A, Markenbuch Farbwelt A), Raum hell wie das Papier (#F5F2EE).
   Liegt unter _werkzeuge/oberflaeche/ und wird von den Werkzeug-Servern unter /assets/oberflaeche/ ausgeliefert (einziger Schreiber: Hotelbüro bzw. Oberchef).
   Fotos und Schriften kommen aus der Website (/assets/img/<schlüssel>-<s|m|l|x>.webp = 480/900/1440/2200 px, /assets/fonts/), Zeichen und Wortmarke aus dem Markenbuch (_kette/05-markenbauer/marke/zeichen/). */
window.WO_HAUS = { kurz: 'montemoro', name: 'Monte-Moro', voll: 'Hotel Monte-Moro', ort: 'Saas-Almagell', bar: 'Hotel Monte-Moro', welt: 'hotel', rahmen: 'buehne', anrede: 'sie',   /* das Haus siezt (Website) */
  /* Aussenfoto des Startbilds: das Haus im Sommer mit den Balkonen aus Lärche (Bildregister der Website, Schlüssel «haus-sommer») */
  foto: '/assets/img/haus-sommer-m.webp', fotoKlein: '/assets/img/haus-sommer-s.webp', fotoFarbe: '#5381BD',
  fotoStufen: [480, 900, 1440], fotoStufenNamen: { 480: 's', 900: 'm', 1440: 'l', 2200: 'x' }, fotoAlt: 'Das Hotel Monte-Moro im Sommer, mit den Balkonen aus Lärche',
  /* Zeichen: der Bergkamm aus dem Logo des Hauses (Markenbuch, bergkamm-*.svg, nachgezogen), Wortmarke: das ganze Logo «Monte Moro Saas-Almagell» (wortmarke-*.svg) */
  zeichen: '/assets/oberflaeche/kleid/montemoro-zeichen.svg', zeichenMass: 5.004, wortmarke: '/assets/oberflaeche/kleid/montemoro-marke.svg#wm', wortmarkeMass: 2.444,   /* Breite : Höhe (Bergkamm viewBox 3483 × 696, Logo 3483 × 1425); oberflaeche.js setzt zeichenMass als aspect-ratio */
  /* Namen der sieben Werkzeuge: die EINE Stelle (Oberchef 08.11.2026, Welt des Hotels; Dateien, Schlüssel und Adressen bleiben: maison, bureau, carte …) */
  namen: { zentrale: 'Das Hotelbüro', website: 'Das Schaufenster', karten: 'Das Kartenbrett', gaeste: 'Die Rezeption', marke: 'Das Markenbuch', besuche: 'Die Besucherliste', druck: 'Die Hausdruckerei' },
  saetze: { zentrale: 'Hier beginnt alles: ein Blick auf alle Werkzeuge und ihren Stand.',
    website: 'Die Website selbst pflegen: Texte, Fotos, Zimmer, Preise, Hinweise.',
    karten: 'Die Karte des Röstihüs und die Preislisten des Hotels schreiben, daraus entstehen Karte und PDF.',
    gaeste: 'Fragen der Gäste zu Zimmern, Preisen, Anreise und Röstihüs, mit Antwortentwurf.',
    marke: 'Logo, Bergkamm, Fotos, Farben und Schriften des Hauses an einem Ort.',
    besuche: 'Wer die Website besucht: woher, wann, welche Seiten, wer buchen oder anfragen will.',
    druck: 'Aushänge, Karten, Briefe und Beiträge in der Sprache des Hauses entwerfen.' },
  wege: { zentrale: '/_werkzeuge/maison/', website: '/_werkzeuge/bureau/', karten: '/_werkzeuge/carte/', gaeste: '/_werkzeuge/reception/', marke: '/_werkzeuge/livre/', besuche: '/_werkzeuge/registre/', druck: '/_werkzeuge/imprimerie/' },
  /* Prüfserver je Werkzeug (cloud/haus.json); Wege zwischen Werkzeugen immer 127.0.0.1, nie localhost (Fehlerbuch 10a) */
  ports: { zentrale: 9381, website: 9382, karten: 9383, gaeste: 9384, marke: 9385, besuche: 9386, druck: 9387, werkbank: 9388, website_lokal: 8947 } };
/* Lokal (Prüfserver je Werkzeug) zeigen die Wege zu den ANDEREN Werkzeugen auf deren eigenen Server unter 127.0.0.1, nie auf den eigenen Port
   (Fund im Stamm 28.10.2026: der Knopf zur Zentrale öffnete /_werkzeuge/maison/ auf 9384 ohne Stand-Wege; Fehlerbuch 10a). Online bleiben sie relativ.
   Wer selbst schon absolute Wege setzt: nur Wege umschreiben, die noch mit «/» beginnen (WO_HAUS.wegeLokal = true zeigt, dass es hier geschah). */
(function () {
  if (!/^(127\.0\.0\.1|localhost)$/.test(location.hostname)) return;
  Object.keys(WO_HAUS.wege).forEach(function (k) {
    var p = WO_HAUS.ports[k], w = WO_HAUS.wege[k];
    if (p && String(p) !== location.port && w.charAt(0) === '/') WO_HAUS.wege[k] = 'http://127.0.0.1:' + p + w;
  });
  WO_HAUS.wegeLokal = true;
})();
document.documentElement.setAttribute('data-wo-haus', WO_HAUS.kurz);
document.documentElement.setAttribute('data-wo-rahmen', WO_HAUS.rahmen);
try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
/* Bewegung der Werkzeuge (29.10.2026): bewegung.js neben oberflaeche.js, async und mit wenig Vorrang nachgeladen, damit es nie vor dem ersten Knopf steht */
(function () {
  var me = document.currentScript, s = document.createElement('script');
  s.src = (me && me.src ? new URL('../bewegung.js', me.src).href : '/assets/oberflaeche/bewegung.js') + '?v=3';   /* Fassung hochzählen, wenn bewegung.js sich ändert */
  s.async = true; s.setAttribute('fetchpriority', 'low'); document.head.appendChild(s);
})();
/* Titel fliegen zeilenweise hoch (Kriterium 37, 30.10.2026). WO_ZEILEN(el) setzt jedes Wort eines Titels in <span class="wo-w"> und schreibt die Zeile als --z daran;
   die Wörter einer Zeile steigen zusammen, Zeile für Zeile gestaffelt. Ändert sich dabei der Umbruch (Silbentrennung, sehr lange Wörter), bleibt der Titel unberührt.
   Hier im Kleid (ohne defer), damit der Titel des Startbilds schon vor dem ersten Bild geteilt ist; bewegung.js nutzt dieselbe Funktion für die Zwischentitel. */
window.WO_ZEILEN = function (el) {
  if (!el || el.hasAttribute('data-wo-zl')) return !!(el && el.classList.contains('wo-zl'));
  var h0 = el.offsetHeight; if (!h0) return false;   /* verborgen: später, wenn er zu sehen ist */
  el.setAttribute('data-wo-zl', '');
  var w0 = Math.max(el.scrollWidth, el.clientWidth), roh = el.innerHTML, tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), t, ts = [];
  while ((t = tw.nextNode())) if (/\S/.test(t.data) && !t.parentNode.closest('svg')) ts.push(t);
  if (!ts.length) return false;
  ts.forEach(function (t) {
    var f = document.createDocumentFragment();
    t.data.split(/(\s+)/).forEach(function (s) {
      if (!s) return;
      if (/^\s+$/.test(s)) { f.appendChild(document.createTextNode(s)); return; }
      var w = document.createElement('span'); w.className = 'wo-w'; w.textContent = s; f.appendChild(w);
    });
    t.parentNode.replaceChild(f, t);
  });
  if (el.offsetHeight !== h0 || el.scrollWidth > w0 + 1) { el.innerHTML = roh; return false; }
  var z = -1, oben = -1e9, halb = parseFloat(getComputedStyle(el).fontSize) * 0.5;
  el.querySelectorAll('.wo-w').forEach(function (w) { var y = w.getBoundingClientRect().top; if (y > oben + halb) { z++; oben = y; } if (z) w.style.setProperty('--z', z); });
  el.classList.add('wo-zl');
  return true;
};
/* Der Titel des Startbilds: geteilt, sobald er im Dokument steht (vor dem ersten Bild, der Auftritt beginnt erst nach 0,18 s) */
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('MutationObserver' in window)) return;
  var plan = 0;
  function teile() {
    plan = 0;
    document.querySelectorAll('.wo-sb__h:not([data-wo-zl])').forEach(function (h) {
      if (document.documentElement.classList.contains('still')) return;
      var a = h.getAnimations ? h.getAnimations() : [];
      if (a.some(function (x) { return (x.currentTime || 0) > 120; })) { h.setAttribute('data-wo-zl', ''); return; }   /* läuft schon: bleibt ein Block, nie zurückspringen */
      WO_ZEILEN(h);
    });
  }
  new MutationObserver(function () { if (!plan && document.querySelector('.wo-sb__h:not([data-wo-zl])')) { plan = 1; Promise.resolve().then(teile); } })
    .observe(document.documentElement, { childList: true, subtree: true });
})();
