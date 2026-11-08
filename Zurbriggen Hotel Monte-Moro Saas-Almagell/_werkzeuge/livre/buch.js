/* Die Hausregeln · Hotel Monte-Moro, Saas-Almagell (aus dem Stamm der Werkzeuge, dort buch/marke.js): «Als PDF sichern» öffnet das
   Druckfenster (je Kapitel eine A4-Seite quer, buch.css @media print); ein Klick auf eine Farbe kopiert ihren Wert.
   Bewegung wie im Stamm und im Kleid (oberflaeche/bewegung.js, Kriterium 37): Titel steigen Zeile für Zeile (Wörter je Zeile gestaffelt),
   Karten, Kacheln und Farbkarten schweben gestaffelt aus der Tiefe herauf, ihre Fotos zoomen von 1,12 auf 1, das Fenster-Foto zoomt beim Auftauchen.
   Nur translate und scale (nie opacity): alles ist ab dem ersten Bild deckend da, was unter dem Rand liegt, wartet dort nur leicht verschoben; vor
   dem Druck steht alles im Endzustand. «Weniger Bewegung» oder kein IntersectionObserver: nichts bewegt sich, alles steht. */
'use strict';
(function () {
  const alle = () => Promise.all([...document.images].map(i => { i.loading = 'eager'; return i.complete ? 0 : new Promise(r => { i.addEventListener('load', r, { once: true }); i.addEventListener('error', r, { once: true }); }); }));
  const b = document.getElementById('bu-pdf');
  const fertig = () => document.querySelectorAll('[data-r],[data-t],[data-z]').forEach(el => el.classList.add('da', 'steht'));
  if (b) b.addEventListener('click', () => { fertig(); alle().then(() => window.print()); });
  addEventListener('beforeprint', () => { fertig(); [...document.images].forEach(i => { i.loading = 'eager'; }); });
  addEventListener('load', () => setTimeout(alle, 1200));
  /* Farbe kopieren */
  const melde = t => { const m = document.getElementById('meldung'); if (!m) return; m.textContent = t; m.classList.add('an'); clearTimeout(melde.u); melde.u = setTimeout(() => m.classList.remove('an'), 1800); };
  document.querySelectorAll('[data-hex]').forEach(k => k.addEventListener('click', () => {
    const w = k.dataset.hex, ok = () => { k.classList.add('kopiert'); setTimeout(() => k.classList.remove('kopiert'), 1400); melde('Kopiert · ' + w); };
    if (navigator.clipboard && isSecureContext) navigator.clipboard.writeText(w).then(ok, ok); else ok();
  }));
  document.querySelectorAll('[data-hex][role="button"]').forEach(k => k.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); k.click(); } }));

  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;

  /* Titel in Wörter teilen, je Wort die Zeile als --z (wie WO_ZEILEN im Kleid); ändert sich dabei der Umbruch, bleibt der Titel unberührt */
  const zeilen = el => {
    const h0 = el.offsetHeight, roh = el.innerHTML, tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), ts = [];
    let t; while ((t = tw.nextNode())) if (/\S/.test(t.data)) ts.push(t);
    ts.forEach(t => {
      const f = document.createDocumentFragment();
      t.data.split(/([ \t\n\r]+)/).forEach(s => {   /* festes Leerzeichen bleibt im Wort: die letzten zwei Wörter brechen nie auseinander */
        if (!s) return;
        if (/^[ \t\n\r]+$/.test(s)) { f.appendChild(document.createTextNode(s)); return; }
        const w = document.createElement('span'); w.className = 'w'; w.textContent = s; f.appendChild(w);
      });
      t.parentNode.replaceChild(f, t);
    });
    if (Math.abs(el.offsetHeight - h0) > 2) { el.innerHTML = roh; el.removeAttribute('data-t'); el.setAttribute('data-r', ''); return; }
    let z = -1, oben = -1e9;
    el.querySelectorAll('.w').forEach(w => { const o = w.offsetTop; if (o > oben + 4) { z++; oben = o; } w.style.setProperty('--z', z); });
  };
  document.querySelectorAll('[data-t]').forEach(zeilen);

  document.documentElement.classList.add('bewegt');
  const io = new IntersectionObserver(es => {
    let k = 0;
    es.forEach(x => {
      if (!x.isIntersecting) return;
      io.unobserve(x.target);
      x.target.style.setProperty('--i', Math.min(k++, 5));
      x.target.classList.add('da');
    });
  }, { rootMargin: '0px 0px -4% 0px' });
  document.querySelectorAll('[data-r],[data-t],[data-z]').forEach(el => io.observe(el));
})();
