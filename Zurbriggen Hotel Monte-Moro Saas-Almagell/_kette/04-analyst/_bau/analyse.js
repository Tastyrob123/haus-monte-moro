/* Potentialanalyse Hotel Monte-Moro (Aufbau aus der Analyse des Castell Son Claret): Pult je Bereich (Pfeile, Zeichen, Zähler, Tastatur, Wischen), «Genauer nachlesen», Fenster. Nur Klassen setzen, nativer Scroll. */
(function () {
  'use strict';
  var doc = document, ruhig = matchMedia('(prefers-reduced-motion:reduce)').matches;
  var $ = function (s, e) { return (e || doc).querySelector(s); }, $$ = function (s, e) { return [].slice.call((e || doc).querySelectorAll(s)); };
  function odo(o) {
    var m = doc.createElement('span'); m.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap'; o.appendChild(m);
    $$('.od', o).forEach(function (s) { m.textContent = s.dataset.d; s.style.setProperty('--b', (m.getBoundingClientRect().width + 1).toFixed(1) + 'px'); });
    o.removeChild(m);
    o.classList.add('da');
    $$('.od', o).forEach(function (s) { s.style.transform = 'translateY(' + (-10 * +s.dataset.d) + '%)'; });
  }
  function blaetter(sek) { return $$('.blatt-p', sek); }
  function zeig(b, scrollen) {
    var sek = b.closest('section'), alle = blaetter(sek), i = alle.indexOf(b);
    alle.forEach(function (x) { x.classList.toggle('an', x === b); if (x !== b) x.classList.remove('da'); });
    $$('.pult button[data-ziel]', sek).forEach(function (w) { w.setAttribute('aria-pressed', w.dataset.ziel === b.id ? 'true' : 'false'); });
    var reihe = $('.pult__reihe', sek), kn = $('.pult button[aria-pressed="true"]', sek);
    if (reihe && kn) reihe.scrollTo({ left: kn.offsetLeft - reihe.clientWidth / 2 + kn.offsetWidth / 2, behavior: ruhig ? 'auto' : 'smooth' });
    var nr = $('[data-pult-nr]', sek), wort = $('[data-pult-wort]', sek), pts = alle.filter(function (x) { return !x.classList.contains('blatt-x'); });
    if (nr) nr.textContent = b.classList.contains('blatt-x') ? 'Dazu' : (pts.indexOf(b) + 1) + ' von ' + pts.length;
    if (wort && kn) wort.textContent = kn.getAttribute('aria-label');
    var zur = $('[data-zur]', sek), vor = $('[data-vor]', sek);
    if (zur) zur.disabled = i <= 0;
    if (vor) vor.disabled = i >= alle.length - 1;
    /* Beweisbilder dieses und des nächsten Blatts sofort holen, damit beim Blättern nichts leer steht */
    [b, alle[i + 1]].forEach(function (x) { if (x) $$('img[loading="lazy"]', x).forEach(function (im) { im.loading = 'eager'; }); });
    requestAnimationFrame(function () { b.classList.add('da'); $$('.odo', b).forEach(odo); });
    setTimeout(function () { $$('.odo', b).forEach(function (o) { if (!$('.od', o) || $('.od', o).style.transform) return; odo(o); }); }, 400);
    if (scrollen) {
      var ziel = $('.pult', sek) || b, top = ziel.getBoundingClientRect().top;
      if (top < 70 || top > innerHeight * 0.5) scrollTo({ top: scrollY + top - 96, behavior: ruhig ? 'auto' : 'smooth' });
    }
  }
  function schritt(sek, r) {
    var alle = blaetter(sek), i = alle.findIndex(function (x) { return x.classList.contains('an'); }), z = alle[i + r];
    if (z) zeig(z, false);
    else if (r > 0) { var n = sek.nextElementSibling; while (n && !n.querySelector('.pult')) n = n.nextElementSibling; if (n) { zeig(blaetter(n)[0], true); } }
    else { var v = sek.previousElementSibling; while (v && !v.querySelector('.pult')) v = v.previousElementSibling; if (v) { var bv = blaetter(v); zeig(bv[bv.length - 1], true); } }
  }
  $$('section').forEach(function (sek) { var a = blaetter(sek); if (a.length) { a[0].classList.add('da'); var zur = $('[data-zur]', sek); if (zur) zur.disabled = true; if (a.length === 1) { var vor = $('[data-vor]', sek); if (vor) vor.disabled = true; } } });
  doc.addEventListener('click', function (ev) {
    var w = ev.target.closest('.pult button[data-ziel]');
    if (w) { var b = doc.getElementById(w.dataset.ziel); if (b) zeig(b, false); return; }
    var zr = ev.target.closest('[data-zur]'); if (zr) { schritt(zr.closest('section'), -1); return; }
    var vr = ev.target.closest('[data-vor]'); if (vr) { schritt(vr.closest('section'), 1); return; }
    var n = ev.target.closest('[data-weiter]');
    if (n) { schritt(n.closest('section'), 1); return; }
    var g = ev.target.closest('[data-genau]');
    if (g) { var d = doc.getElementById(g.dataset.genau); if (d && d.showModal) { d.showModal(); d.scrollTop = 0; } return; }
    var z = ev.target.closest('[data-zu]');
    if (z) { var dd = z.closest('dialog'); if (dd) dd.close(); return; }
    var o = ev.target.closest('[data-oeffne]');
    if (o) { var bb = doc.getElementById(o.dataset.oeffne); if (bb) { ev.preventDefault(); zeig(bb, true); history.replaceState(null, '', '#' + bb.id); } return; }
    var dlg = ev.target.closest('dialog.genau');
    if (dlg && ev.target === dlg) dlg.close();
  });
  /* Pfeiltasten blättern im Bereich, der gerade im Bild ist (kein offenes Fenster, kein Eingabefeld) */
  doc.addEventListener('keydown', function (ev) {
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return;
    if (doc.querySelector('dialog[open]') || /INPUT|TEXTAREA|SELECT/.test(doc.activeElement.tagName)) return;
    var best = null, bd = 1e9, mitte = innerHeight / 2;
    $$('.pult').forEach(function (p) { var r = p.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return; var d = Math.abs((r.top + r.bottom) / 2 - mitte); if (d < bd) { bd = d; best = p; } });
    if (!best) return;
    ev.preventDefault(); schritt(best.closest('section'), ev.key === 'ArrowRight' ? 1 : -1);
  });
  /* Wischen auf dem Blatt und dem Pult */
  $$('.blaetter, .pult').forEach(function (el) {
    var x0 = null, y0 = null;
    el.addEventListener('pointerdown', function (e) { if (e.pointerType === 'mouse' && el.classList.contains('blaetter')) return; x0 = e.clientX; y0 = e.clientY; }, { passive: true });
    el.addEventListener('pointerup', function (e) { if (x0 === null) return; var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null; if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.4) schritt(el.closest('section'), dx < 0 ? 1 : -1); }, { passive: true });
  });
  /* Buchstaben steigen einzeln aus ihrer Zeile (wie im Markenbuch des Carlton), Wörter bleiben ganz */
  if (!ruhig) $$('.zt').forEach(function (t) {
    var k = 0; t.setAttribute('aria-label', $$('.z', t).map(function (z) { return z.textContent.trim(); }).join(' '));
    $$('.z>span', t).forEach(function (zeile) {
      (function geh(el) {
        [].slice.call(el.childNodes).forEach(function (n) {
          if (n.nodeType === 1) { geh(n); return; }
          if (n.nodeType !== 3) return;
          var f = doc.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) { f.appendChild(doc.createTextNode(' ')); return; }
            var wo = doc.createElement('span'); wo.className = 'wo'; wo.setAttribute('aria-hidden', 'true');
            w.split('').forEach(function (c) { var b = doc.createElement('span'); b.className = 'bu'; b.style.setProperty('--k', k++); b.textContent = c; wo.appendChild(b); });
            f.appendChild(wo);
          });
          el.replaceChild(f, n);
        });
      })(zeile);
    });
    t.classList.add('bst');
  });
  /* Bilder vorziehen: anderthalb Bildschirme voraus von «lazy» auf «eager», damit nichts wartet (Safari lädt lazy spät) */
  var holen = function (im) { if (im.getAttribute('loading') === 'lazy') { im.loading = 'eager'; if (im.decode) im.decode().catch(function () {}); } };
  if ('IntersectionObserver' in window) {
    var vor = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { vor.unobserve(e.target); holen(e.target); } }); }, { rootMargin: '150% 0px 150% 0px' });
    $$('img[loading="lazy"]').forEach(function (im) { vor.observe(im); });
  } else $$('img').forEach(holen);
  /* Sicherung: was im Bild oder schon darüber ist, steht da, auch wenn ein Beobachter nicht meldet (Safari, schneller Sprung) */
  function sicher() {
    var h = innerHeight * 1.05;
    $$('[data-a]:not(.da),.zt:not(.da),.wfen:not(.da),.odo:not(.da)').forEach(function (el) {
      if (el.closest('dialog') || el.closest('.blatt-p:not(.an)')) return;
      var r = el.getBoundingClientRect(); if (r.top < h) { if (el.classList.contains('odo')) odo(el); else el.classList.add('da'); }
    });
    $$('.blatt-p.an:not(.da)').forEach(function (b) { if (b.getBoundingClientRect().top < h) b.classList.add('da'); });
  }
  var st = 0; addEventListener('scroll', function () { clearTimeout(st); st = setTimeout(sicher, 260); }, { passive: true });
  addEventListener('load', function () { setTimeout(sicher, 1600); }); setTimeout(sicher, 3500);
  function marke() { var h = location.hash.replace('#', ''), b = h && doc.getElementById(h); if (b && b.classList.contains('blatt-p')) zeig(b, true); }
  marke(); addEventListener('hashchange', marke);
  $$('.laufzeile').forEach(function (l) {
    if (!('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) { l.classList.toggle('steht', !es[0].isIntersecting); }).observe(l);
  });
  $$('.wfen').forEach(function (f) {
    if (!('IntersectionObserver' in window)) { f.classList.add('da'); return; }
    f.classList.add('weg');
    new IntersectionObserver(function (es) { f.classList.toggle('weg', !es[0].isIntersecting); }).observe(f);
    new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { o.disconnect(); f.classList.add('da'); } }, { threshold: 0.35 }).observe(f);
  });
})();
