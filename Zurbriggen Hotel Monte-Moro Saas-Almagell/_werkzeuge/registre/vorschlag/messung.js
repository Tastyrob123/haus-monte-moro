/* Die Besucherliste (Le Registre) · Hotel Monte-Moro, Saas-Almagell: Zählung auf der Website (Tasty Studios, 08.11.2026). Quelle dieser Datei; auf der
   Website liegt sie als assets/js/messung.js, auf jeder Seite vor </body> als <script src="assets/js/messung.js?v=…" defer></script>, nach anfrage.js.
   Den Einbau in bau.py (Fuss) macht der Bau der Website (Revier website/, erst auf Roberts Wort); hier nur die Quelle. Vorbild: messung.js der Besucherliste
   im Stamm der Häuser (nur kopiert), Ereignisse aus den Wegen der Website des Monte-Moro.

   Je Seite geht eine Zeile an /api/registre (lokal der Server der Besucherliste, online die Funktion api/registre.py, gleiche Adresse):
       r1 <seitenaufruf> <datei> <sprache> <geraet> <sekunden> <ereignisse|-> <herkunft|->
   einmal beim Öffnen (0 Sekunden), bei jedem gezählten Klick und beim Verlassen (Sekunden, in denen die Seite sichtbar war).
   Ohne Cookies und ohne Kennung im Gerät: «seitenaufruf» ist eine Zufallsfolge, die nur in dieser Variablen lebt und mit der Seite endet.
   Dass die Seiten eines Besuchs zusammenfinden, Land und Ort bestimmt der Server aus der Verbindung (registre.py); die Adresse speichert er nicht.
   «herkunft» ist nur der Name der Website, von der der Gast kam (zum Beispiel www.booking.com), nie die ganze Adresse.
   «sprache» ist die Sprache des Browsers (die Website gibt es auf Deutsch), sonst «xx».
   Nicht gezählt: automatische Browser (Prüfläufe), Seiten im Rahmen, die Werkzeuge und die Werkbank, Wahl- und Vorschauseiten
   und Geräte mit der Marke «montemoro-nicht-zaehlen» im localStorage (das Einzige, was je im Gerät steht).
   Das Fenster «Anfrage» (anfrage.js, dialog.anf) und der Chat (rezeption.js) bleiben unberührt: gezählt wird nur, dass etwas geöffnet oder abgeschickt
   wurde, nie ein Inhalt (kein Name, keine Telefonnummer, keine Frage).

   Ereignisse (Schlüssel wie in allen Häusern, Bedeutung beim Hotel Monte-Moro):
     fenster  Zimmer-Anfrage begonnen: Fenster «Anfrage» für ein Zimmer, das Familienzimmer, Haus Apollo, Haus Arizona oder eine Frage zu den Preisen geöffnet
     buchung  Zimmer angefragt: erst wenn dieses Fenster sein «Danke.» zeigt (.anf__danke sichtbar)
     booking  «Zimmer buchen» angeklickt (weiter zur Buchung bei seekda, monte-moro.ch/de/buchen.html)
     tisch    Tisch-Anfrage begonnen: Fenster «Tisch im Röstihüs» geöffnet (data-art="tisch")
     anfrage  Tisch im Röstihüs angefragt: erst wenn dieses Fenster sein «Danke.» zeigt
     anruf    Telefonnummer des Hauses angeklickt (+41 27 957 10 12)
     mail     E-Mail-Adresse des Hauses angeklickt (info@monte-moro.ch; die Website öffnet dafür das Fenster «Ihre Anfrage»)
     chat     Chat der Rezeption geöffnet (Knopf unten rechts, [data-chat-auf])
     route    weiter zur Familie Zurbriggen (Spa nebenan im Wellness & Spa Pirmin Zurbriggen, Familienband im Fuss jeder Seite) */
(function () {
  'use strict';
  var n = navigator, d = document, w = window;
  if (w.__registre || !n.sendBeacon || n.webdriver || w.self !== w.top) return;
  try { if (w.localStorage.getItem('montemoro-nicht-zaehlen') === '1') return; } catch (e) { /* privat: zählt normal */ }
  var teile = location.pathname.split('/'), datei = teile.pop() || 'index.html';
  if (/^(_werkzeuge|werkzeuge|werkbank|_werkbank|_varianten|maison|marke|reception|registre|imprimerie|_qa|_sicherung|_alt|_zuschnitt)$/.test(teile[1] || '')) return;   /* Werkzeuge und Werkbank zählen nie */
  if (!/^[a-z0-9-]{1,60}\.html$/.test(datei) || /wahl|^konzept|varianten|^vorschau|^404/.test(datei)) return;
  w.__registre = 1;
  var SPRACHEN = ' de en fr it nl es pt zh ja ko ar ';
  var sp = String(n.language || 'de').slice(0, 2).toLowerCase();
  if (SPRACHEN.indexOf(' ' + sp + ' ') < 0) sp = 'xx';
  var breit = function (px) { return !!(w.matchMedia && w.matchMedia('(max-width:' + px + 'px)').matches); };
  var geraet = breit(700) ? 'handy' : breit(1060) ? 'tablet' : 'rechner';
  var her = '-';
  try { var r = d.referrer ? new URL(d.referrer).hostname.toLowerCase() : ''; if (r && r !== location.hostname && /^[a-z0-9.-]{3,60}$/.test(r)) her = r; } catch (e) {}
  var TEL = /^tel:\+?(41279571012|0279571012)$/;
  var pv, war, liste, sichtbar, seit, gesendet;
  function neu() {
    pv = (Math.random().toString(36) + '000000').slice(2, 8);
    war = {}; liste = []; sichtbar = 0; gesendet = '';
    seit = d.visibilityState === 'hidden' ? 0 : Date.now();
    sende();
  }
  function sek() { return Math.min(1800, Math.round((sichtbar + (seit ? Date.now() - seit : 0)) / 1000)); }
  function sende() {
    var zeile = 'r1 ' + pv + ' ' + datei + ' ' + sp + ' ' + geraet + ' ' + sek() + ' ' + (liste.length ? liste.join(',') : '-') + ' ' + her;
    if (zeile === gesendet) return;
    gesendet = zeile;
    try { n.sendBeacon('/api/registre', zeile); } catch (e) {}   /* wartet auf keine Antwort */
  }
  function zaehle(was) {
    if (war[was]) return;
    war[was] = 1; liste.push(was);
    sende();
  }
  function weg() { if (seit) { sichtbar += Date.now() - seit; seit = 0; } sende(); }
  neu();
  d.addEventListener('visibilitychange', function () { if (d.visibilityState === 'hidden') weg(); else if (!seit) seit = Date.now(); });
  w.addEventListener('pagehide', weg);
  w.addEventListener('pageshow', function (e) { if (e.persisted) neu(); });   /* zurück aus dem Seitenspeicher des Browsers: neuer Aufruf */

  /* Gezählt ist erst, was die Website zeigt («Danke.»); nachgesehen wird kurz, höchstens 20 Sekunden. Bleibt es aus (Pflichtfeld leer), zählt nichts. */
  function danach(pruef, was) {
    var bis = Date.now() + 20000;
    (function schau() { if (pruef()) { zaehle(was); return; } if (Date.now() < bis) setTimeout(schau, 250); })();
  }
  var offen = '';   /* welches Fenster «Anfrage» gerade offen ist: 'zimmer', 'tisch' oder 'allgemein' (E-Mail-Adresse) */

  d.addEventListener('click', function (e) {
    var t = e.target; if (!t || !t.closest) return;
    if (t.closest('[data-chat-auf]')) { zaehle('chat'); return; }
    var anf = t.closest('[data-anfrage], a[href^="mailto:info@monte-moro.ch"]');
    if (anf) {
      var art = anf.getAttribute('data-art'), betreff = anf.getAttribute('data-anfrage') || 'Ihre Anfrage';
      if (art === 'tisch') { offen = 'tisch'; zaehle('tisch'); }
      else if (betreff === 'Ihre Anfrage') { offen = 'allgemein'; zaehle('mail'); }
      else { offen = 'zimmer'; zaehle('fenster'); }
      return;
    }
    if (t.closest('dialog.anf button[type=submit]')) {
      /* «Ihre Anfrage» (E-Mail-Adresse) ohne Zimmer oder Tisch zählt beim Abschicken nichts weiter; «Zimmer angefragt» nur, wenn ein Zimmer gemeint war */
      if (offen === 'zimmer' || offen === 'tisch') danach(function () { var x = d.querySelector('dialog.anf .anf__danke'); return !!(x && !x.hidden); }, offen === 'tisch' ? 'anfrage' : 'buchung');
      return;
    }
    var a = t.closest('a[href]'); if (!a) return;
    var h = (a.getAttribute('href') || '').replace(/\s/g, ''), host = (a.hostname || '').toLowerCase(), pfad = a.pathname || '';
    if (/^tel:/i.test(h)) { if (TEL.test(h)) zaehle('anruf'); }
    else if ((/(^|\.)monte-moro\.ch$/.test(host) && /\/buchen\.html$/.test(pfad)) || /(^|\.)seekda\.(com|net)$/.test(host)) zaehle('booking');
    else if (/(^|\.)wellnesshotel-zurbriggen\.ch$/.test(host) || a.closest('.familienband')) zaehle('route');
  }, true);
})();
