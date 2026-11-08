/* Kurzer Rundgang durch die Besucherliste · Hotel Monte-Moro, Saas-Almagell (Stamm: die Besucherliste der Häuser; Karte und Schild im Kleid des Hauses, Lärche als Hauptknopf; Vorlage: assets/js/rundgang.js des ersten Hauses, Robert 16.10.2026: «einmal ganz kurz zeigen, hier kannst du das machen,
   da das, damit man weiss, wo man gelandet ist»). Ein Lichtkegel liegt auf dem echten Bedienelement, daneben eine Karte mit zwei, drei Sätzen.
   Kein Start von selbst: unten rechts erscheint ein Schild «Kurzer Rundgang» (fünf Sekunden, die Maus darauf hält es), dann zieht es sich zurück.
   Wieder aufrufen: «Kurzer Rundgang» im Rand oder ?rundgang (startet direkt). Automatische Prüfungen (navigator.webdriver) und eingebettete Ansichten sehen nichts. */
(function () {
  var Q = new URLSearchParams(location.search), ERZWINGEN = Q.has('rundgang');
  if (window.self !== window.top && !ERZWINGEN) return;
  var NAME = (window.WO && WO.name('besuche')) || 'Besuche', KLEIN = NAME.replace(/^(Die|Das|Der) /, function (m) { return m.toLowerCase(); });   /* Name nur aus dem Kleid des Hauses */
  var G = { name: NAME, schritte: [
    { ziel: ['#ansicht .wo-sb'], titel: 'Das ist <span style="white-space:nowrap">' + KLEIN + '</span>',   /* der Name bricht nie, kein Wort allein in der letzten Zeile (WebKit, Cloud-Prüfung 31.10.2026) */
      text: 'Wer Ihre Website besucht hat: woher die Gäste kommen, was sie interessiert und wer ein Zimmer buchen oder anfragen will.' },
    { ziel: ['#rand', '#kopf .wo-kopf__ber'], titel: 'Acht Ansichten',
      text: 'Besuche und Herkunft, Zeit und Verlauf, Seiten und «Zur Buchung», dazu «So wird gezählt». Ein Klick wechselt, der Zeitraum gilt überall.' },
    { ziel: ['#ansicht .zahlen'], titel: 'Bringt die Website Gäste?',
      text: 'Besuche, Verweildauer und der Weg zur Buchung. So sehen Sie, ob die neuen Preise, ein Beitrag auf Instagram oder ein Eintrag bei Schweiz Tourismus Gäste ins Haus bringt.' },
    { ziel: ['#ansicht .zwei'], titel: 'Woher Ihre Gäste kommen',
      text: 'Orte und Länder, und welche Seiten am längsten gelesen werden. Gut zu wissen für Beiträge, Angebote und die nächste Saison.' },
    { ziel: ['#ansicht .liste'], titel: 'Jeder Besuch einzeln',
      text: 'Wie sich ein Gast durch die Seiten bewegt hat. Ohne Namen, ohne Cookies.' }
  ] };
  var SCHLUESSEL = 'rundgang-montemoro-registre';
  function merk() { try { localStorage.setItem(SCHLUESSEL, '1'); } catch (e) { } }

  var CSS = '' +
    '.rdg-kegel{position:fixed;left:0;top:0;z-index:2147483000;border-radius:16px;pointer-events:none;' +
      'box-shadow:0 0 0 3px #C67144,0 0 0 9px rgba(198,113,68,.28),0 0 40px 10px rgba(198,113,68,.24),0 0 0 200vmax rgba(7,27,46,.74)}' +
    '.rdg-sperre{position:fixed;inset:0;z-index:2147482999}' +
    '.rdg-karte{position:fixed;left:0;top:0;z-index:2147483001;width:360px;max-width:calc(100vw - 32px);box-sizing:border-box;' +
      'padding:22px 24px 20px;border-radius:18px;color:#13263A;background:linear-gradient(180deg,#FFFFFF,#F5F2EE);' +
      'box-shadow:0 1px 0 #fff inset,0 0 0 1px rgba(154,79,43,.22),0 30px 60px -24px rgba(7,27,46,.6),0 10px 22px -12px rgba(7,27,46,.4);' +
      'font:15px/1.55 "Instrument Sans",Arial,system-ui,sans-serif;animation:rdg-auf .42s cubic-bezier(.2,.8,.2,1) both}' +
    '@keyframes rdg-auf{from{transform:translate3d(var(--rx,0),calc(var(--ry,0px) + 14px),0)}to{transform:translate3d(var(--rx,0),var(--ry,0),0)}}' +
    '.rdg-karte{transform:translate3d(var(--rx,0),var(--ry,0),0)}' +
    '.rdg-zier{display:flex;align-items:center;gap:10px;font:400 10px/1 "DM Mono",ui-monospace,Menlo,monospace;letter-spacing:.2em;text-transform:uppercase;color:#9A4F2B}' +
    '.rdg-zier i{flex:1;height:1px;background:linear-gradient(90deg,#B39867,rgba(179,152,103,0))}' +
    '.rdg-karte h3{margin:12px 0 6px;font:400 27px/1.14 "Fjalla One","Arial Narrow",Arial,sans-serif;color:#13263A;letter-spacing:0}' +
    '.rdg-karte p{margin:0;color:rgba(19,38,58,.78)}' +
    '.rdg-fuss{display:flex;align-items:center;gap:14px;margin-top:20px}' +
    '.rdg-karte .rdg-weg{display:flex;gap:5px;flex:1 1 auto;min-width:64px}.rdg-karte .rdg-weg b{display:block;height:3px;flex:1 1 0;min-width:6px;max-width:26px;border-radius:2px;background:rgba(19,38,58,.14)}.rdg-karte .rdg-weg b.da{background:#B39867}' +
    '.rdg-karte .rdg-zu{flex:none;margin:0;border:0;background:none;padding:6px 2px;font:400 10px/1 "DM Mono",ui-monospace,Menlo,monospace;letter-spacing:.14em;text-transform:uppercase;color:#9A4F2B;cursor:pointer}' +
    '.rdg-karte .rdg-zu:hover{color:#13263A}' +
    '.rdg-karte .rdg-los{flex:none;margin:0;display:inline-flex;align-items:center;gap:12px;height:42px;padding:0 6px 0 18px;border:0;border-radius:999px;cursor:pointer;' +
      'font:400 10px/1 "DM Mono",ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;color:#FFFFFF!important;' +
      'background:linear-gradient(180deg,#D3845A 0%,#C67144 46%,#AE5E34 100%);box-shadow:0 1px 0 rgba(255,255,255,.3) inset,0 10px 18px -10px rgba(198,113,68,.7)}' +
    '.rdg-karte .rdg-los i{display:grid;margin:0;place-items:center;width:30px;height:30px;border-radius:50%;background:linear-gradient(180deg,#FFFFFF,#EFE9E1);' +
      'box-shadow:0 1px 0 rgba(255,255,255,.6) inset,0 3px 6px -2px rgba(0,0,0,.45)}' +
    '.rdg-karte .rdg-los svg{width:14px;height:14px;fill:none;stroke:#0A2A4A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}' +
    '.rdg-karte .rdg-los:hover i{transform:translateX(2px)}.rdg-karte .rdg-los i{transition:transform .2s}' +
    '.rdg-los:focus-visible,.rdg-zu:focus-visible{outline:2px solid #C67144;outline-offset:3px}' +
    /* Werkzeug-Stile (La Carte vergrössert Knöpfe und Schrift) dürfen die Karte nicht verändern */
    '.rdg-karte,.rdg-karte *{box-sizing:border-box!important}' +
    '.rdg-karte p{font:15px/1.55 "Instrument Sans",Arial,system-ui,sans-serif!important;letter-spacing:0!important;text-transform:none!important}' +
    '.rdg-karte h3{font:400 27px/1.14 "Fjalla One","Arial Narrow",Arial,sans-serif!important;letter-spacing:0!important;text-transform:none!important}' +
    '.rdg-karte .rdg-fuss{flex-wrap:nowrap!important}' +
    '.rdg-karte .rdg-zu,.rdg-karte .rdg-los{font:400 10px/1 "DM Mono",ui-monospace,Menlo,monospace!important;letter-spacing:.14em!important;text-transform:uppercase!important;min-width:0!important;width:auto!important;outline:0;border:0!important;margin:0!important}' +
    '.rdg-karte .rdg-zu{height:auto!important;padding:6px 2px!important;background:none!important;box-shadow:none!important;color:#9A4F2B!important}' +
    '.rdg-karte .rdg-los{height:42px!important;padding:0 6px 0 18px!important;letter-spacing:.16em!important;border-radius:999px!important}' +
    '.rdg-karte .rdg-los i{width:30px!important;height:30px!important;flex:none!important}' +
    '@media (max-width:700px){.rdg-karte{left:16px!important;right:16px;top:auto!important;bottom:16px;width:auto;--rx:0!important;--ry:0!important}}' +
    '@media (prefers-reduced-motion:reduce){.rdg-karte{animation:none}}';
  var SCHILD_CSS = '' +
    '.rdg-schild{position:fixed;right:24px;bottom:24px;z-index:2147482990;display:flex;align-items:center;gap:14px;box-sizing:border-box;' +
      'padding:10px 10px 10px 18px;border-radius:999px;color:#13263A;background:linear-gradient(180deg,#FFFFFF,#F5F2EE);' +
      'box-shadow:0 1px 0 #fff inset,0 0 0 1px rgba(154,79,43,.28),0 18px 34px -16px rgba(7,27,46,.55),0 6px 14px -8px rgba(7,27,46,.35);' +
      'transform:translate3d(0,0,0);transition:transform .55s cubic-bezier(.2,.8,.2,1);animation:rdg-schild-auf .7s cubic-bezier(.2,.9,.25,1.15) both}' +
    '@keyframes rdg-schild-auf{from{transform:translate3d(0,calc(100% + 40px),0)}to{transform:translate3d(0,0,0)}}' +
    '.rdg-schild.weg{animation:none;transform:translate3d(0,calc(100% + 60px),0)}' +
    '.rdg-schild__t{display:flex;flex-direction:column;gap:4px;line-height:1}' +
    '.rdg-schild__t small{font:400 9px/1 "DM Mono",ui-monospace,Menlo,monospace!important;letter-spacing:.2em!important;text-transform:uppercase;color:#9A4F2B}' +
    '.rdg-schild__t b{font:400 18px/1 "Fjalla One","Arial Narrow",Arial,sans-serif!important;letter-spacing:0!important;color:#13263A}' +
    '.rdg-schild .rdg-los{flex:none;margin:0!important;display:inline-flex;align-items:center;gap:10px;height:38px!important;padding:0 5px 0 15px!important;border:0!important;border-radius:999px!important;cursor:pointer;' +
      'font:400 9.5px/1 "DM Mono",ui-monospace,Menlo,monospace!important;letter-spacing:.16em!important;text-transform:uppercase!important;color:#F5F2EE!important;' +
      'background:linear-gradient(180deg,#D3845A 0%,#C67144 46%,#AE5E34 100%)!important;box-shadow:0 1px 0 rgba(255,255,255,.3) inset,0 8px 16px -10px rgba(198,113,68,.7)!important}' +
    '.rdg-schild .rdg-los i{display:grid;place-items:center;width:28px!important;height:28px!important;border-radius:50%;background:linear-gradient(180deg,#FFFFFF,#EFE9E1);box-shadow:0 1px 0 rgba(255,255,255,.95) inset,0 -2px 0 rgba(0,0,0,.24) inset,0 2px 5px rgba(0,0,0,.2);transition:transform .2s}' +
    '.rdg-schild .rdg-los:hover i{transform:translateX(2px)}' +
    '.rdg-schild .rdg-los svg{width:13px;height:13px;fill:none;stroke:#0A2A4A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}' +
    '.rdg-schild__zu{flex:none;width:26px;height:26px;margin:0 2px 0 -4px!important;padding:0!important;border:0!important;border-radius:50%;background:none!important;box-shadow:none!important;cursor:pointer;color:#4A5D70;font:16px/1 system-ui!important}' +
    '.rdg-schild__zu:hover{color:#13263A}' +
    '.rdg-schild__zu{display:grid;place-items:center}.rdg-schild__zu svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}' +   /* kein «×» (Robert 30.10.2026): Zurück-Pfeil wie «Verwerfen» */
    '@media (max-width:700px){.rdg-schild{right:16px;left:auto}}' +
    '@media (prefers-reduced-motion:reduce){.rdg-schild{animation:none;transition:none}}';
  var PFEIL = '<i><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg></i>';
  var lauf = null;

  function sichtbar(sel) {
    var e; try { e = document.querySelector(sel); } catch (x) { return null; }
    if (!e) return null;
    var r = e.getBoundingClientRect();
    if (r.width > 4 && r.height > 4) return e;
    return window.WO && WO.randZiel ? WO.randZiel(e) : null;   /* Handy: Ziel im zugeklappten Rand, das Kleid klappt ihn auf (30.10.2026) */
  }
  function finde(liste) { for (var i = 0; i < liste.length; i++) { var e = sichtbar(liste[i]); if (e) return e; } return null; }
  function scroller() { var f = document.querySelector('#flaeche'); return f && getComputedStyle(f).overflowY === 'auto' ? f : null; }

  function starte() {
    var schritte = G.schritte; if (lauf) return;
    if (!finde(schritte[0].ziel)) return;
    if (!document.getElementById('rdg-css')) { var st = document.createElement('style'); st.id = 'rdg-css'; st.textContent = CSS; document.head.appendChild(st); }
    var sperre = document.createElement('div'); sperre.className = 'rdg-sperre';
    var kegel = document.createElement('div'); kegel.className = 'rdg-kegel';
    var karte = document.createElement('div'); karte.className = 'rdg-karte';
    karte.setAttribute('role', 'dialog'); karte.setAttribute('aria-modal', 'true'); karte.setAttribute('aria-label', 'Kurzer Rundgang ' + G.name);
    document.body.appendChild(sperre); document.body.appendChild(kegel); document.body.appendChild(karte);
    var nr = 0, ziel = null, gerueckt = false;
    lauf = { };

    function lege() {
      if (!ziel || !ziel.isConnected) ziel = finde(schritte[nr].ziel);
      if (!ziel) return;
      var r = ziel.getBoundingClientRect(), pad = 8, vw = innerWidth, vh = innerHeight;
      var x = Math.max(4, r.left - pad), y = Math.max(4, r.top - pad);
      var b = Math.min(vw - 8, r.right + pad) - x, h = Math.min(vh - 8, Math.min(Math.max(r.bottom, r.top + (schritte[nr].min || 0)), r.top + (schritte[nr].max || 1e5)) + pad) - y;
      if (vw <= 700) {   /* Handy (Oberchef 30.10.2026): die Karte überdeckt nie das Markierte; ein Ziel höher als das freie Feld wird bis über die Karte markiert */
        var kt = vh - (parseFloat(getComputedStyle(karte).bottom) || 16) - karte.offsetHeight - 18;
        if (y < kt && y + h > kt) {   /* der Rahmen endet an einer Zeilengrenze, nie mitten durch eine Zeile, einen Knopf oder einen Eintrag (Oberchef 30.10.2026) */
          var schnitt = kt, rs = [], alle = ziel.querySelectorAll('*'), rg = document.createRange(), tw = document.createTreeWalker(ziel, NodeFilter.SHOW_TEXT), tn;
          for (var j = 0; j < alle.length; j++) { var er = alle[j].getBoundingClientRect(); if (er.height > 0 && er.height < 100) rs.push(er); }
          while ((tn = tw.nextNode())) { if (!tn.nodeValue.trim()) continue; rg.selectNodeContents(tn); var cr = rg.getClientRects(); for (var q = 0; q < cr.length; q++) rs.push(cr[q]); }
          for (var d = 0; d < 12; d++) {
            var neu = schnitt;
            for (j = 0; j < rs.length; j++) if (rs[j].top < neu - 2 && rs[j].bottom > neu + 3) neu = rs[j].top - 3;
            if (neu === schnitt) break; schnitt = neu;
          }
          h = Math.max(40, schnitt - y);
        }
      }
      kegel.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
      kegel.style.width = Math.max(0, b) + 'px'; kegel.style.height = Math.max(0, h) + 'px';
      if (vw <= 700) return;
      karte.style.width = '';
      var kw = karte.offsetWidth, kh = karte.offsetHeight, abst = 22, kx, ky;
      if (x + b + abst + kw <= vw - 16) { kx = x + b + abst; ky = y; }
      else if (x - abst - kw >= 16) { kx = x - abst - kw; ky = y; }
      else if (y + h + abst + kh <= vh - 16) { kx = x; ky = y + h + abst; }
      else if (y - abst - kh >= 16) { kx = x; ky = y - abst - kh; }
      else if (x - abst - 16 >= 240) { karte.style.width = (x - abst - 16) + 'px'; kw = karte.offsetWidth; kh = karte.offsetHeight; kx = 16; ky = y; }   /* Tor 30.10.2026: grosses Ziel, die Karte steht links daneben über dem Rand, nie auf dem Gezeigten */
      else if (!gerueckt && h + abst + kh + 110 < vh) { gerueckt = true; (scroller() || window).scrollBy({ top: r.top - 96, behavior: 'instant' }); return lege(); }
      else { kx = vw - kw - 24; ky = vh - kh - 24; }
      kx = Math.min(Math.max(16, kx), vw - kw - 16); ky = Math.min(Math.max(16, ky), vh - kh - 16);
      karte.style.setProperty('--rx', kx + 'px'); karte.style.setProperty('--ry', ky + 'px');
    }

    function zeige(n, rueck) {
      while (n >= 0 && n < schritte.length && !finde(schritte[n].ziel)) n += rueck ? -1 : 1;   /* fehlt ein Ziel (Handy, leere Ansicht), weiter zum nächsten */
      if (n < 0 || n >= schritte.length) return ende();
      nr = n; gerueckt = false; var s = schritte[n], letzt = n === schritte.length - 1;
      ziel = finde(s.ziel);
      if (window.WO && WO.randZurueck) WO.randZurueck(ziel);   /* Schritt ausserhalb des Rands: der Rundgang klappt ihn wieder zu */
      var r = ziel.getBoundingClientRect();
      if (r.top < 70 || r.bottom > innerHeight - 20) ziel.scrollIntoView({ block: r.height > innerHeight * .7 ? 'start' : 'center', behavior: 'instant' });
      var weg = ''; for (var i = 0; i < schritte.length; i++) weg += '<b' + (i <= n ? ' class="da"' : '') + '></b>';
      karte.innerHTML = '<div class="rdg-zier"><span>' + G.name + ' · ' + (n + 1) + ' von ' + schritte.length + '</span><i></i></div>' +
        '<h3>' + s.titel + '</h3><p>' + s.text + '</p>' +
        '<div class="rdg-fuss"><div class="rdg-weg" aria-hidden="true">' + weg + '</div>' +
        (letzt ? '' : '<button type="button" class="rdg-zu">Überspringen</button>') +
        '<button type="button" class="rdg-los">' + (letzt ? 'Los geht’s' : 'Weiter') + PFEIL + '</button></div>';
      karte.style.animation = 'none'; void karte.offsetWidth; karte.style.animation = '';
      var handy = function () { if (window.WO && WO.rdgHandy) WO.rdgHandy(ziel, karte); };   /* Handy: Ziel ins freie Feld zwischen Kopf und Karte (30.10.2026) */
      handy(); lege(); setTimeout(function () { handy(); lege(); }, 450); setTimeout(lege, 1300);   /* nach den Auftritten: Zeilengrenze neu messen */
      var zu = karte.querySelector('.rdg-zu'); if (zu) zu.onclick = ende;
      var los = karte.querySelector('.rdg-los'); los.onclick = function () { letzt ? ende() : zeige(n + 1); };
      try { los.focus({ preventScroll: true }); } catch (e) { }
    }

    function taste(e) {
      if (e.key === 'Escape') { e.preventDefault(); ende(); }
      else if (e.key === 'ArrowRight' || e.key === 'Enter') { e.preventDefault(); nr < schritte.length - 1 ? zeige(nr + 1) : ende(); }
      else if (e.key === 'ArrowLeft' && nr > 0) { e.preventDefault(); zeige(nr - 1, true); }
    }
    var takt = 0; function neu() { if (!takt) takt = requestAnimationFrame(function () { takt = 0; lege(); }); }
    var zuletzt = '', wacht = setInterval(function () {   /* der Kegel folgt seinem Ziel, solange es sich bewegt oder wächst */
      if (!ziel) return; var r = ziel.getBoundingClientRect(), k = [r.left, r.top, r.width, r.height].map(Math.round).join();
      if (k !== zuletzt) { zuletzt = k; neu(); }
    }, 120);
    function ende() {
      if (window.WO && WO.randZurueck) WO.randZurueck(null);
      merk(); lauf = null;
      removeEventListener('resize', neu); removeEventListener('scroll', neu, true); document.removeEventListener('keydown', taste, true);
      clearInterval(wacht); sperre.remove(); kegel.remove(); karte.remove();
    }
    addEventListener('resize', neu); addEventListener('scroll', neu, true); document.addEventListener('keydown', taste, true);
    zeige(0);
  }

  /* Erst fliegt die Seite herein, dann erscheint das Schild: gewartet wird, bis keine endliche Animation mehr läuft (mindestens 2,5 s, höchstens 6 s), dann noch eine Pause. */
  function wenn_bereit(dann) {
    var t0 = Date.now();
    (function blick() {
      if (finde(G.schritte[0].ziel) && document.readyState === 'complete' && !document.documentElement.classList.contains('auftakt')) return nach_auftritt(dann);
      if (Date.now() - t0 < 12000) setTimeout(blick, 250);
    })();
  }
  function nach_auftritt(dann) {
    var t0 = performance.now(), ruhe = 0;
    (function blick() {
      var laeuft = (document.getAnimations ? document.getAnimations() : []).some(function (a) {
        try { return a.playState === 'running' && isFinite(a.effect.getComputedTiming().endTime); } catch (e) { return false; }
      });
      ruhe = laeuft ? 0 : ruhe + 1;
      var seit = performance.now() - t0;
      if ((ruhe >= 3 && seit > 2500) || seit > 6000) return setTimeout(dann, 700);
      setTimeout(blick, 200);
    })();
  }
  var angesetzt = false;
  function vielleicht() {
    if (lauf || angesetzt) return;
    if (navigator.webdriver && !ERZWINGEN) return;
    angesetzt = true;
    wenn_bereit(function () { ERZWINGEN ? starte() : schild(); });
  }

  function schild() {
    if (document.querySelector('.rdg-schild')) return;
    /* der Knopf «Zeigen» braucht die Knopf-Regeln aus CSS: ohne sie stand er ungestaltet da (Fund Doldenhorn 17.10.2026, steckt so in der Carlton-Vorlage) */
    if (!document.getElementById('rdg-css')) { var sk = document.createElement('style'); sk.id = 'rdg-css'; sk.textContent = CSS; document.head.appendChild(sk); }
    if (!document.getElementById('rdg-schild-css')) { var st = document.createElement('style'); st.id = 'rdg-schild-css'; st.textContent = SCHILD_CSS; document.head.appendChild(st); }
    var s = document.createElement('div'); s.className = 'rdg-schild'; s.setAttribute('role', 'status');
    s.innerHTML = '<span class="rdg-schild__t"><small>' + G.name + '</small><b>Kurzer Rundgang</b></span>' +
      '<button type="button" class="rdg-los">Zeigen' + PFEIL + '</button><button type="button" class="rdg-schild__zu" aria-label="Schliessen"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 9.67 2.67 6.33 6 3M2.67 6.33h7.33a3.33 3.33 0 0 1 0 6.67h-2"/></svg></button>';
    function platz() {   /* über die Leiste unten setzen, nie darauf */
      var l = document.querySelector('#leiste'), lr = l && l.getBoundingClientRect();
      if (!l || !lr || lr.height < 5) return;
      s.style.bottom = Math.max(24, innerHeight - lr.top + 14) + 'px';
    }
    document.body.appendChild(s); platz();
    var wache = setInterval(platz, 150);
    var uhr = 0, ueber = false;
    function weg() { clearTimeout(uhr); clearInterval(wache); s.classList.add('weg'); setTimeout(function () { s.remove(); }, 650); }
    function zaehle() { clearTimeout(uhr); uhr = setTimeout(function () { if (!ueber) weg(); }, 10000); }
    s.addEventListener('mouseenter', function () { ueber = true; clearTimeout(uhr); });
    s.addEventListener('mouseleave', function () { ueber = false; uhr = setTimeout(weg, 2000); });
    s.querySelector('.rdg-los').onclick = function () { weg(); starte(); };
    s.querySelector('.rdg-schild__zu').onclick = weg;
    zaehle();
  }

  /* «Kurzer Rundgang» als Weg im Rand, damit er sich jederzeit wieder öffnen lässt. */
  function weg_im_rand() {
    var wege = document.querySelector('#rand .wege');
    if (!wege || wege.querySelector('.rdg-wieder')) return;
    var a = document.createElement('a'); a.href = '#'; a.className = 'rdg-wieder'; a.textContent = 'Kurzer Rundgang';
    a.onclick = function (e) { e.preventDefault(); starte(); };
    var haus = wege.querySelector('.rand__haus');
    wege.insertBefore(a, haus);
  }
  function los() {
    vielleicht();
    new MutationObserver(weg_im_rand).observe(document.body, { childList: true, subtree: true });
    weg_im_rand();
  }
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', los) : los();
  window.rundgang = function () { starte(); };
})();
