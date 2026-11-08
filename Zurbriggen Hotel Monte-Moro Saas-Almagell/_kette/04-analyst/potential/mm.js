/* Potentialanalyse Hotel Monte-Moro, Fassung 2: mitlaufende Liste am Rand (nur Klassen), Sicherung für Auftritte. Nativer Scroll. */
(function () {
  'use strict';
  var d = document, $$ = function (s) { return [].slice.call(d.querySelectorAll(s)); };
  var links = $$('.mm-rand a'), arts = $$('.mm-p');
  if ('IntersectionObserver' in window && links.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) links.forEach(function (a) { a.classList.toggle('an', a.dataset.ziel === e.target.id); }); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    arts.forEach(function (a) { io.observe(a); });
  }
  function sicher() {
    var h = innerHeight * 1.05;
    $$('[data-a]:not(.da),.zt:not(.da),.wfen:not(.da)').forEach(function (el) { if (el.closest('details:not([open])')) return; if (el.getBoundingClientRect().top < h) el.classList.add('da'); });
  }
  var t = 0; addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(sicher, 260); }, { passive: true });
  addEventListener('load', function () { setTimeout(sicher, 1500); }); setTimeout(sicher, 3500);
  $$('.laufzeile').forEach(function (l) { if (!('IntersectionObserver' in window)) return; new IntersectionObserver(function (es) { l.classList.toggle('steht', !es[0].isIntersecting); }).observe(l); });
  $$('.wfen').forEach(function (f) {
    if (!('IntersectionObserver' in window)) { f.classList.add('da'); return; }
    f.classList.add('weg');
    new IntersectionObserver(function (es) { f.classList.toggle('weg', !es[0].isIntersecting); }).observe(f);
    new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { o.disconnect(); f.classList.add('da'); } }, { threshold: 0.35 }).observe(f);
  });
  /* Lichtkegel (Robert 17.10.2026, Master 1b Nr. 16): von der Stelle im Gerät zur Lupe. Gerechnet aus der Lage ohne Bewegung (offsetLeft/Top), neu bei Grössenänderung. */
  var NS = 'http://www.w3.org/2000/svg';
  function lage(el, root) { var x = 0, y = 0; while (el && el !== root) { x += el.offsetLeft; y += el.offsetTop; el = el.offsetParent; } return { x: x, y: y }; }
  function kegel(o) {
    var svg = o.querySelector('.mm-kegel'), img = o.querySelector('.mm-g img[data-mark]'), z = o.querySelector('.mm-z--lupe');
    if (!svg || !img || !z) return;
    var ziel = z.querySelector('.mm-z__b, .mm-tab__b'); if (!ziel || !img.offsetWidth) return;
    var m = img.dataset.mark.split(',').map(Number), p = lage(img, o), q = lage(ziel, o);
    var sx0 = p.x + img.offsetWidth * m[0] / 100, sy0 = p.y + img.offsetHeight * m[1] / 100;
    var sx1 = sx0 + img.offsetWidth * m[2] / 100, sy1 = sy0 + img.offsetHeight * m[3] / 100;
    var r = 14, cx0 = q.x, cy0 = q.y, cx1 = q.x + ziel.offsetWidth, cy1 = q.y + ziel.offsetHeight, pts, a, b;
    if (cx0 >= sx1 + 8) { pts = [[sx1, sy0], [cx0, cy0 + r], [cx0, cy1 - r], [sx1, sy1]]; a = [sx1, (sy0 + sy1) / 2]; b = [cx0, (cy0 + cy1) / 2]; }
    else if (cx1 <= sx0 - 8) { pts = [[sx0, sy0], [cx1, cy0 + r], [cx1, cy1 - r], [sx0, sy1]]; a = [sx0, (sy0 + sy1) / 2]; b = [cx1, (cy0 + cy1) / 2]; }
    else {   // untereinander: zur Oberkante der Lupe, rechts an der Beschriftung «Was genau» vorbei
      var l = o.querySelector('.mm-s--was > .mm-l'), lx = l ? lage(l, o).x + l.offsetWidth + 22 : cx0;
      var fx0 = Math.max(cx0 + r, Math.min(lx, cx1 - 60));
      pts = [[sx0, sy1], [fx0, cy0], [cx1 - r, cy0], [sx1, sy1]]; a = [(sx0 + sx1) / 2, sy1]; b = [(fx0 + cx1) / 2, cy0];
    }
    var W = o.offsetWidth, H = o.offsetHeight, id = 'kg' + (o.id || Math.random().toString(36).slice(2, 7));
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H); svg.setAttribute('width', W); svg.setAttribute('height', H);
    svg.innerHTML = '<defs><linearGradient id="' + id + '" gradientUnits="userSpaceOnUse" x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '">' +
      '<stop offset="0" class="mm-kegel__a"/><stop offset="1" class="mm-kegel__b"/></linearGradient></defs>' +
      '<polygon class="mm-kegel__f" fill="url(#' + id + ')" points="' + pts.map(function (v) { return v.join(','); }).join(' ') + '"/>' +
      '<line class="mm-kegel__l" x1="' + pts[0][0] + '" y1="' + pts[0][1] + '" x2="' + pts[1][0] + '" y2="' + pts[1][1] + '"/>' +
      '<line class="mm-kegel__l" x1="' + pts[3][0] + '" y1="' + pts[3][1] + '" x2="' + pts[2][0] + '" y2="' + pts[2][1] + '"/>' ;
  }
  // am Handy: breite Vergrösserungen als Band zum Wischen, es beginnt dort, wo die rote Stelle steht
  function band() { $$('.mm-z__b').forEach(function (b) { if (b.dataset.lage || b.scrollWidth <= b.clientWidth + 2) return; var m = b.querySelector('.mm-z__m--h'); b.dataset.lage = 1;
    if (m && m.offsetLeft + m.offsetWidth > b.clientWidth - 16) b.scrollLeft = Math.max(0, m.offsetLeft - 20); }); }
  addEventListener('load', band); setTimeout(band, 1200);
  var os = $$('.mm-p__o');
  os.forEach(function (o, i) { o.id = o.id || 'mo' + i; });
  function alle() { os.forEach(kegel); }
  if ('ResizeObserver' in window) { var ro = new ResizeObserver(function (es) { es.forEach(function (e) { kegel(e.target); }); }); os.forEach(function (o) { ro.observe(o); }); }
  addEventListener('load', alle); $$('.mm-p__o img').forEach(function (im) { if (!im.complete) im.addEventListener('load', function () { kegel(im.closest('.mm-p__o')); }); }); alle();
  if ('IntersectionObserver' in window) {
    var ko = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { kegel(e.target); e.target.classList.add('kegel'); ko.unobserve(e.target); } }); }, { threshold: 0.3 });
    os.forEach(function (o) { ko.observe(o); });
  } else os.forEach(function (o) { o.classList.add('kegel'); });
})();
