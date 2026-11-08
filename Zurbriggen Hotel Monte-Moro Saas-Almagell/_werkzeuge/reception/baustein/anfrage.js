/* Baustein für die Website des Hotel Monte-Moro → Eingang der Rezeption (08.11.2026). Auf der Website NICHT eingebaut (Revier Website, ANLEITUNG.md daneben).
   Die Website hat schon ein Anfrage-Fenster (assets/js/anfrage.js, POST /api/anfragen) und die Rezeption im Chat (assets/js/rezeption.js, Antworten aus
   assets/js/wissen.json). Beide Skripte bleiben unverändert; dieser Baustein hängt sich im Fang-Durchlauf am Dokument davor:
   - «Anfrage senden» im Anfrage-Fenster: die Angaben gehen zusätzlich an die Rezeption (Standard /api/anfragen auf dem Server der Rezeption), auch dort,
     wo anfrage.js nichts ablegt (alle Server ausser der Vorschau 8947). Auf der Vorschau 8947 legt anfrage.js selbst ab; die Rezeption holt es dort ab.
   - Jede Frage an die Rezeption im Chat geht an /api/frage und steht danach in der Rezeption unter «Das wurde gefragt» (die Antwort rechnet der Server
     gleich wie der Chat der Website; Mail-Adressen und Nummern deckt er ab). Ohne Verbindung merkt der Gast nichts: der Chat antwortet wie bisher.
   Nie mailto, nie ein Mailprogramm, nichts an Dritte. Weg anpassbar mit data-api am Skript. */
(function () {
  'use strict';
  var S = document.currentScript, API = (S && S.getAttribute('data-api')) || '/api/anfragen', FRAGE = (S && S.getAttribute('data-frage')) || '/api/frage';
  function schick(weg, daten) {
    try { return fetch(weg, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(daten), keepalive: true }).catch(function () {}); } catch (e) { return null; }
  }
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (f && f.matches && f.matches('form.anf__form')) {
      if (location.port === '8947') return;   // die Vorschau der Website legt selbst ab (website/_dienste/anfragen.jsonl)
      var name = (f.name && f.name.value || '').trim(), kontakt = (f.kontakt && f.kontakt.value || '').trim();
      if (!name || !kontakt || (f.website && f.website.value)) return;   // anfrage.js zeigt dem Gast den Hinweis selbst
      var titel = document.getElementById('anf-titel'), tisch = f.tag && !f.tag.closest('label').hidden;
      schick(API, { haus: 'Hotel Monte-Moro', betreff: titel ? titel.textContent : 'Ihre Anfrage', art: tisch ? 'tisch' : '', tag: f.tag ? f.tag.value : '', zeit: f.zeit ? f.zeit.value : '',
        personen: tisch && f.personen ? f.personen.value : '', nachricht: f.nachricht ? f.nachricht.value : '', name: name, kontakt: kontakt, seite: location.pathname, zeitpunkt: new Date().toISOString() });
    } else if (f && f.matches && f.matches('[data-chat-form]')) {
      var feld = f.querySelector('[data-chat-feld]'), q = feld ? feld.value.trim() : '';
      if (q) schick(FRAGE, { frage: q.slice(0, 600), sprache: (document.documentElement.lang || 'de').slice(0, 2) });
    }
  }, true);
  document.addEventListener('click', function (e) {   // Vorschläge im Chat (Knöpfe unter der Antwort) sind auch Fragen
    var b = e.target.closest && e.target.closest('[data-chat-vorschlag] button');
    if (b) schick(FRAGE, { frage: b.textContent.trim().slice(0, 600), sprache: 'de' });
  }, true);
})();
