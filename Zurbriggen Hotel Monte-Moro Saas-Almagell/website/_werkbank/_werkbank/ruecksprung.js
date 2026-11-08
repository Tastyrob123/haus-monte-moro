/* Rücksprung auf die alte Höhe (Robert 1.11.2026: «wenn ich in etwas reingehe … und dann im Browser zurückgehe, will ich nicht immer ganz oben landen»).
   Jede Seite merkt sich ihre Höhe in sessionStorage (Schlüssel «rs:<Pfad>») beim Scrollen, beim Klick auf einen Link und bei pagehide.
   Kommt man mit Zurück/Vor wieder (Navigation «back_forward» ohne bfcache), springt die Seite nach dem Aufbau dorthin, ohne Auftakt-Bewegung.
   Aus dem bfcache (pageshow persisted) stellt der Browser die Höhe selbst wieder her. Keine unload-Handler, bfcache bleibt möglich.
   Eingesetzt von _werkbank/ruecksprung.py als <script id="ruecksprung"> vor </body> jeder Seite der Werkbank. */
(function () {
  var K = 'rs:' + location.pathname, d = document.documentElement;
  function merk() { try { var y = String(Math.round(window.scrollY || 0)); sessionStorage.setItem(K, y); if (document.getElementById('rh-zurueck')) sessionStorage.setItem('wb-y', y); } catch (e) {} }
  var t = 0;
  addEventListener('scroll', function () { clearTimeout(t); t = setTimeout(merk, 150); }, { passive: true });
  addEventListener('pagehide', merk);
  document.addEventListener('click', function (ev) { if (ev.target.closest && ev.target.closest('a[href]')) merk(); }, true);
  var nav = null; try { nav = performance.getEntriesByType('navigation')[0]; } catch (e) {}
  if (!nav || nav.type !== 'back_forward') return;
  if (document.getElementById('rh-zurueck')) return;   /* die Startseite stellt die Höhe selbst her (rh-zurueck liest «wb-y», das hier laufend mitgeschrieben wird) */
  var y = null; try { y = sessionStorage.getItem(K); } catch (e) {}
  if (y === null || !/^\d+$/.test(y) || +y < 40) return;
  y = +y;
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  var st = document.createElement('style');
  st.textContent = 'html.rs-sofort,html.rs-sofort *{transition:none!important;animation-duration:0s!important;animation-delay:0s!important;scroll-behavior:auto!important}';
  document.head.appendChild(st); d.classList.add('rs-sofort');
  var weg = false;
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (k) { addEventListener(k, function () { weg = true; }, { once: true, passive: true }); });
  function oben() { var g = y + innerHeight * 1.2; [].forEach.call(document.querySelectorAll('[data-a],.zt,.roll,img.ld'), function (e) { var r = e.getBoundingClientRect(); if (r.top + scrollY < g) e.classList.add('da'); }); }
  function geh() { if (!weg) { window.scrollTo(0, y); oben(); } }
  function los() {
    geh(); requestAnimationFrame(function () { geh(); requestAnimationFrame(function () { d.classList.remove('rs-sofort'); }); });
    var n = 0, iv = setInterval(function () { n++; if (Math.abs(scrollY - y) > 40) geh(); if (n >= 12 || weg) clearInterval(iv); }, 150);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
  addEventListener('load', function () { if (Math.abs(scrollY - y) > 40) geh(); });
})();
