/* pruefung-haus.js · Prüfseite des Stamms im Rahmen des Hotel Monte-Moro (08.11.2026): Name des Werkzeugs aus der einen Stelle (WO_HAUS.namen),
   «Zum Werkzeug» führt in dieses Werkzeug, nicht in den Stamm. Das Lexikon des Stamms bleibt unverändert und deckt jedes Stichwort des Werkzeugs. */
(function () {
  var z = document.getElementById('wsp-zurueck'); if (z) z.href = '/_werkzeuge/bureau/';
  var n = window.WO_HAUS && WO_HAUS.namen && WO_HAUS.namen.website;
  /* welt.js des Stamms füllt [data-werkzeug] erst nach dem Laden mit seinem Weltnamen («Le Bureau»): der Name des Hauses wird danach noch einmal gesetzt */
  function setze() { if (n) { document.querySelectorAll('[data-werkzeug]').forEach(function (e) { if (e.textContent !== n) e.textContent = n; }); document.title = 'Prüfung · ' + n + ' · ' + WO_HAUS.name; } }
  setze(); document.addEventListener('DOMContentLoaded', setze); window.addEventListener('load', function () { setze(); setTimeout(setze, 200); });
})();
