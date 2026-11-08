/* festigkeit.js · Das Schaufenster des Hotel Monte-Moro (08.11.2026): kleine Nachbesserungen am Werkzeug des Stamms (website.js), ohne dessen Datei zu ändern.
   Aus der früheren Ansicht des Stamm-Rahmens übernommen (Abnahme-Tor 2, Messlauf 30.10.2026), Wortlaut auf das Hotel gestellt. Nach website.js laden. */
(function () {
  /* Kacheltitel und -unterschriften der Übersicht ohne einzelnes Wort in der letzten Zeile (Kriterium 7): die letzten zwei Wörter bleiben zusammen
     (Safari kennt den Umbruch «pretty» noch nicht) */
  function fest() {
    document.querySelectorAll(':is(.wo-ag__t, .wo-bk__t) > :is(b, span):not([data-fest]):not(:has(*)), .ws-eintrag__t > b:not([data-fest])').forEach(function (b) {
      b.setAttribute('data-fest', '');
      var t = b.textContent.trim(), i = t.lastIndexOf(' '), j = i > 0 ? t.lastIndexOf(' ', i - 1) : -1;
      if (j < 0) { if (i > 0 && b.parentNode.classList.contains('ws-eintrag__t')) b.textContent = t.replace(' ', ' '); return; }   /* Namen aus zwei Wörtern bleiben ganz */
      b.textContent = t.slice(0, j + 1) + t.slice(j + 1).replace(' ', ' ');
    });
  }
  /* Listen des Hauses: «Ändern» unter dem Namen als Zeichen der Kachel (CSS ::after), damit die letzte Textzeile der Name bleibt */
  function aendernZeichen() {
    document.querySelectorAll('.ws-eintrag__auf:not([data-text])').forEach(function (e) { var t = e.textContent.trim(); if (!t) return; e.setAttribute('data-text', t); e.textContent = ''; });
  }
  /* Fenster «Foto tauschen»: der Bildtitel steht ganz (das gemeinsame Werkzeug kürzt ihn auf 48 Zeichen mit «…»; der volle steht im title) */
  function ganz() {
    document.querySelectorAll('.ws-fwahl:not([data-ganz])').forEach(function (k) {
      k.setAttribute('data-ganz', '');
      var t = k.querySelector('.ws-fwahl__t'), voll = k.getAttribute('title');
      if (!t) return;
      var text = (voll && /…$/.test(t.textContent)) ? (/^Eigenes Foto · /.test(t.textContent) ? 'Eigenes Foto · ' : '') + voll : t.textContent;
      var i = text.lastIndexOf(' ');   /* die letzten zwei Wörter bleiben zusammen: nie ein Wort allein in der letzten Zeile (Kriterium 7) */
      t.textContent = '';
      if (i > 0) { var j = text.lastIndexOf(' ', i - 1), ende = document.createElement('span'); ende.style.whiteSpace = 'nowrap'; ende.textContent = text.slice(j + 1); t.append(text.slice(0, j + 1), ende); }
      else t.textContent = text;
    });
  }
  /* Kein «×» als Zählzeichen (Kriterium 24): «Link · 4× auf der Seite» heisst «4-mal auf der Seite», «Steht 9× …» heisst «Steht an 9 Stellen …» */
  function ohneX() {
    document.querySelectorAll('.ws-st small, .ws-ang__lage, .ws-hoch, .ws-hoch *').forEach(function (e) {
      if (e.children.length) return;
      var t = e.textContent; if (t.indexOf('×') < 0) return;
      e.textContent = t.replace(/(\d+)× auf der Seite/g, '$1-mal auf der Seite').replace(/Steht (\d+)×/g, 'Steht an $1 Stellen').replace(/(\d+)\s*×\s*(\d+)/g, '$1 auf $2').replace(/(\d+)×/g, '$1-mal');
    });
  }
  /* Knopf «Website ansehen» im Kopf: zwischen 901 und 1240 px nur der runde Knauf (bureau.css); sein Name bleibt für Vorlesegeräte als aria-label */
  function knaufName() {
    document.querySelectorAll('#ws-kopf a.wo-kn--gold:not([aria-label])').forEach(function (a) { var t = a.textContent.trim(); if (t) a.setAttribute('aria-label', t); });
  }
  /* Lange Werte in Feldern des Stamms (Bildbeschreibung, Google-Titel, Links): ein einzeiliges Feld versteckt den Anfang (Kriterium 2). Daneben
     steht ein Textfeld, das umbricht; das Feld des Stamms bleibt (verborgen) die Quelle: Eingaben gehen als «input» an es, Werte, die der Stamm setzt
     («Wie ursprünglich»), erscheinen im Textfeld. Zeilenumbrüche werden zu Leerzeichen, Enter fügt keinen ein. */
  var WERT = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
  function langfeld() {
    document.querySelectorAll('input#ws-alt:not([data-lang]), input[id^="ws-gt-t-"]:not([data-lang]), input[id^="ws-ang-"][type="url"]:not([data-lang]), input[id^="ws-ang-"][type="text"]:not([data-lang])').forEach(function (f) {
      f.setAttribute('data-lang', '');
      var t = document.createElement('textarea');
      t.className = 'ws-langfeld'; t.rows = 1; t.spellcheck = false; t.setAttribute('autocomplete', 'off');
      var lb = f.id && document.querySelector('label[for="' + CSS.escape(f.id) + '"]');
      if (lb) { if (!lb.id) lb.id = 'lb-' + f.id; t.setAttribute('aria-labelledby', lb.id); }
      t.value = f.value;
      var hoch = function () { t.style.height = 'auto'; t.style.height = t.scrollHeight + 'px'; };
      var spiegel = function () { t.disabled = f.disabled; t.setAttribute('aria-invalid', f.getAttribute('aria-invalid') || 'false'); };
      Object.defineProperty(f, 'value', { configurable: true, get: function () { return WERT.get.call(this); }, set: function (v) { WERT.set.call(this, v); if (t.value !== String(v)) { t.value = v; hoch(); } } });
      t.addEventListener('keydown', function (e) { if (e.key === 'Enter') e.preventDefault(); });
      t.addEventListener('input', function () { var v = t.value.replace(/\s*\n\s*/g, ' '); if (v !== t.value) t.value = v; WERT.set.call(f, v); f.dispatchEvent(new Event('input', { bubbles: true })); hoch(); });
      if (window.MutationObserver) new MutationObserver(spiegel).observe(f, { attributes: true, attributeFilter: ['disabled', 'aria-invalid'] });
      spiegel();
      f.style.display = 'none';
      f.after(t);
      requestAnimationFrame(hoch);
      if (document.activeElement === f) t.focus();
    });
  }
  /* Kacheln unter «Häufig gebraucht»: das Foto in der nächsten Stufe der Website (-m, 900 px, statt -s, 480 px), sonst stand es unscharf vergrössert */
  function scharf() {
    document.querySelectorAll('.ws-aufgaben > .wo-ag .wo-ag__b img:not([data-scharf]), .ws-bereiche > .wo-bk .wo-bk__b img:not([data-scharf])').forEach(function (i) {
      i.setAttribute('data-scharf', '');
      var alt = i.getAttribute('src') || '';
      if (!/-s\.webp/.test(alt)) return;
      i.addEventListener('error', function () { if (i.getAttribute('src') !== alt) i.setAttribute('src', alt); }, { once: true });
      i.setAttribute('src', alt.replace(/-s\.webp/, '-m.webp'));
    });
  }
  /* Wörter des Stamms, die es beim Hotel nicht gibt: Öffnungszeiten (die Website nennt keine, sie sind offen) und eine Strasse (offen). Das Hotel führt
     Telefon, E-Mail und Ort; Zeiten auf der Website sind Uhrzeiten (Kidsclub, Zug ab Visp). */
  var WORT = [[/^Preis oder Öffnungszeit$/, 'Preis oder Uhrzeit'], [/^Telefon oder Adresse$/, 'Telefon oder E-Mail'],
    [/^Telefon, E-Mail, Adresse, Öffnungstage und die wichtigsten Links\./, 'Telefon, E-Mail und Ort des Hotels.']];
  function woerter() {
    document.querySelectorAll('#ws-mitte b, #ws-mitte p, #ws-mitte span, #ws-mitte h2').forEach(function (e) {
      if (e.children.length) return;
      var t = e.textContent;
      WORT.forEach(function (w) { if (w[0].test(t)) e.textContent = t = t.replace(w[0], w[1]); });
    });
  }
  /* Fotos der Foto-Gruppen eines Bereichs sofort laden und malen (WebKit malte spät geladene Bilder unter einem offenen Fenster nicht) */
  function sofort() {
    document.querySelectorAll('.ws-fotos .ws-foto img:not([data-sofort])').forEach(function (i) { i.setAttribute('data-sofort', ''); i.loading = 'eager'; i.decoding = 'sync'; });
  }
  /* Preise der Website stehen als «90<i>.00</i>»: die Schicht des Stamms liest daraus «90 .00». In der Unterzeile einer Liste steht der Preis wie auf der Website */
  /* Die Zeile über dem Namen ist ein eigener Absatz (p statt span): Name und Zeile darüber sind zwei Blöcke, nicht ein Satz, der umbricht */
  function preise() {
    document.querySelectorAll('.ws-eintrag__t > span.ws-mono:not([data-preis])').forEach(function (e) {
      var p = document.createElement('p'); p.className = e.className; p.setAttribute('data-preis', '');
      p.textContent = e.children.length ? e.textContent : e.textContent.replace(/(\d) \.(\d)/g, '$1.$2');
      e.replaceWith(p);
    });
  }
  /* Werte nur aus Kleinbuchstaben («inkl.»): auf Versalhöhe zugeschnitten sassen sie gemessen 1 px zu tief (Kriterium 35); sie werden auf die x-Höhe zugeschnitten */
  function klein() {
    document.querySelectorAll('.ws-zl__wert:not([data-klein])').forEach(function (e) { e.setAttribute('data-klein', /^[a-zäöüß.,:;\s–-]+$/.test(e.textContent.trim()) ? 'ja' : 'nein'); });
  }
  /* Zum Kartenbrett führt der Weg im Kopf (Werkzeuge des Hauses); die Gruppe «Karten», die der Stamm in den Rand setzt, wäre ein zweiter Weg zum selben Ziel (Kriterium 15) */
  function einWeg() {
    document.querySelectorAll('#ws-rand .wo-rand__g').forEach(function (g) { if (g.querySelector('a.wo-re[href*="/_werkzeuge/carte/"]')) g.remove(); });
  }
  var plan = 0;
  function alles() { plan = 0; einWeg(); sofort(); klein(); woerter(); preise(); fest(); aendernZeichen(); ganz(); ohneX(); knaufName(); langfeld(); scharf(); }
  if (window.MutationObserver) new MutationObserver(function () { if (!plan) plan = requestAnimationFrame(alles); }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
})();
