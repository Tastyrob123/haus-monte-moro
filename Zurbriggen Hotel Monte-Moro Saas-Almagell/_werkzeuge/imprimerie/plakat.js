/* Die Hausdruckerei · Hotel Monte-Moro (08.11.2026, Form der Hausdruckerei des Stammhauses): zwei Ansichten.
   1. «Bergbilder» (#msMotive): Fotos des Saastals und des Hauses (motive.json, aus bau.py), jedes gleich als Aushang mit der Grat-Kante der Website;
      «Als Aushang öffnen» öffnet es im Editor.
   2. «Aushang anlegen» (#msAbend): Baukasten mit Live-Vorschau: Etikett, Titel, Satz und Zusatzzeile, ein Foto (Bergbild, Foto des Hauses oder eigenes),
      der Grund (Nacht, Papier oder Nachtblau); «Aushänge anlegen» setzt daraus Instagram, Story und A3 und dasselbe in den anderen Gründen.
   Gesetzt wird mit dem Aufbau «grat» (haeuser/montemoro/dokumente.js). Ohne KI, ohne Server: eigene Fotos bleiben wie «Meine Medien» im Browser. */
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const PFEIL = '<svg viewBox="0 0 24 24"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>';
  let MOTIVE = [];
  const bergbilder = () => MOTIVE.map(m => m.key).filter(k => DS.M.bildIndex && DS.M.bildIndex[k]);
  const TOENE = [['dunkel', 'Nacht', 'navy'], ['hell', 'Papier', 'weiss'], ['blau', 'Nachtblau', 'laden']];
  const FN = { insta: 'Instagram 4:5', story: 'Story 9:16', a3h: 'A3 zum Aushang' };

  /* Der Aushang als Drucksache; Texte sind eigene Ebenen (Etikett, Titel, Satz, Zusatzzeile), das Foto trägt oben die Grat-Kante */
  function aushangDoc(o) {
    const inhalt = { bild: o.bild || bergbilder()[0] || DS.M.ersatz, ueber: o.ueber || '', titel: o.titel || '', text: o.text || '', aktion: o.aktion || '' };
    return DS.dokument(DS.M, { name: o.name || o.titel || 'Aushang', format: o.format || 'insta', seiten: [{ vorlage: 'grat', ton: o.ton || 'dunkel', inhalt }] });
  }
  function fach(raster, n) {
    const w = raster.clientWidth || 900, breit = matchMedia('(min-width:700px)').matches;
    const sp = !breit ? 1 : n == 4 ? 2 : 3;
    return Math.round(Math.max(230, Math.min(400, (w - (sp - 1) * 26) / sp / 1.05)));
  }
  function karte(doc, titel, unter, knopf, groesse) {
    const k = document.createElement('div'); k.className = 'pk-karte pk-karte--eins';
    const box = groesse || 230, S = window.DSStudio;
    const b = document.createElement('div'); b.className = 'pk-blaetter pk-blaetter--eins';
    b.style.cssText = `height:${Math.round(box * 1.25 + 20)}px`;
    try { const v = S.miniBox(doc, 0, box * 1.25); v.classList.add('pk-vorn'); b.appendChild(v); } catch (e) { console.warn(e); }
    k.appendChild(b);
    k.insertAdjacentHTML('beforeend', `<div class="pk-text"><b>${esc(titel)}</b><small>${esc(unter)}</small></div>
      <button class="kn knopf--voll pk-los" type="button"><span>${esc(knopf)}</span><i>${PFEIL}</i></button>`);
    k.querySelector('.pk-los').addEventListener('click', () => { DSStudio.oeffne(doc); if (DSStart.offen()) DSStart.zu(); });
    return k;
  }

  /* ---------- 1 Bergbilder ---------- */
  function zeichneMotive() {
    const box = $('#pkMotive'); if (!box) return;
    $('#pkFilter').innerHTML = '';
    box.innerHTML = '';
    const L = MOTIVE.filter(m => DS.M.bildIndex && DS.M.bildIndex[m.key]);
    $('#pkMotivZahl').textContent = `${L.length} Bergbilder, jedes mit der Grat-Kante der Website`;
    L.forEach((m, i) => box.appendChild(karte(aushangDoc({ bild: m.key, ueber: (m.schlagworte || {}).thema === 'Haus' ? DS.M.voll : 'Saastal', titel: m.titel, text: '', ton: i % 3 === 2 ? 'hell' : 'dunkel', name: m.titel }),
      m.titel, (m.schlagworte || {}).thema || 'Saastal', 'Als Aushang öffnen')));
  }

  /* ---------- 2 Aushang anlegen: Baukasten mit Live-Vorschau ---------- */
  const SPEICHER = 'ds-montemoro-aushang';
  let BK = null, zeichnen = 0, quelle = 'berg', hausAlle = false;
  const lies = () => { try { return JSON.parse(localStorage.getItem(SPEICHER) || 'null'); } catch (e) { return null; } };
  const merke = () => { try { localStorage.setItem(SPEICHER, JSON.stringify(BK)); } catch (e) { } };
  function zustand() {
    if (BK) return BK;
    const alt = lies() || {};
    BK = { bild: alt.bild || null, ton: alt.ton || 'dunkel', format: alt.format || 'insta' };
    return BK;
  }
  function werte() {
    const v = id => (($('#' + id) || { value: '' }).value || '').trim();
    return { titel: v('pkThema') || 'Racletteabend im Stübli.', ueber: v('pkFreitag'), text: v('pkGast'), aktion: v('pkZusatz') };
  }
  function bauDoc(format, ton) {
    const s = zustand(), w = werte(), bild = s.bild && DS.M.bildIndex[s.bild] ? s.bild : bergbilder()[0];
    return aushangDoc(Object.assign({}, w, { bild, format: format || s.format, ton: ton || s.ton, name: w.titel.replace(/\.$/, '') }));
  }
  function vorschau() {
    clearTimeout(zeichnen);
    zeichnen = setTimeout(() => {
      const box = $('#bkBlatt'); if (!box || !window.DSStudio) return;
      const breit = matchMedia('(min-width:1100px)').matches, F = DS.FORMATE[zustand().format] || { b: 4, h: 5 };
      const bw = (box.clientWidth || 320) - 4, h = Math.min(breit ? Math.min(600, innerHeight - 200) : 520, Math.floor(bw * F.h / F.b));
      try { const v = DSStudio.miniBox(bauDoc(), 0, Math.max(200, h)); box.replaceChildren(v); } catch (e) { console.warn(e); }
      const w = werte(); $('#bkUnter').textContent = `${w.titel} · ${(TOENE.find(t => t[0] === zustand().ton) || [])[1] || ''} · ${(DS.FORMATE[zustand().format] || {}).name || ''}`;
      merke();
    }, 90);
  }
  async function hochladen(ev) {
    const d = ev.target.files && ev.target.files[0]; ev.target.value = ''; if (!d) return;
    const m = $('#bkMeldung');
    try {
      m.textContent = 'Das Foto wird gelesen …';
      const neu = await DS.eigene.hinzu(DS.M, [d], t => { m.textContent = t; });
      if (!neu.length) throw new Error('Das Foto liess sich nicht lesen.');
      zustand().bild = neu[0]; quelle = 'eigen';
      m.textContent = neu.fluechtig ? 'Fertig. Dieser Browser behält das Foto nur bis zum Schliessen.' : 'Fertig. Das Foto bleibt in diesem Browser.';
      zeichneFotos(); vorschau();
    } catch (e) { m.textContent = e.message || 'Das Foto liess sich nicht lesen.'; }
  }
  const NICHT = [DS.eigene ? DS.eigene.GRUPPE : 'Eigene Fotos'];
  const hausFotos = () => (DS.M.bilder || []).filter(b => !b.eigen && !b.ki && !NICHT.includes(b.gruppe)).map(b => b.key);
  function zeichneFotos() {
    const box = $('#bkFotos'); if (!box) return;
    document.querySelectorAll('[data-bkquelle]').forEach(x => { const an = x.dataset.bkquelle === quelle; x.classList.toggle('an', an); x.setAttribute('aria-pressed', an); });
    const s = zustand(), akt = s.bild && DS.M.bildIndex[s.bild] ? s.bild : bergbilder()[0];
    const knopf = k => { const b = DS.M.bildIndex[k] || {}, an = k === akt;
      return `<button type="button" class="bk-foto${an ? ' an' : ''}" data-bkbild="${esc(k)}" aria-pressed="${an}" aria-label="${esc(b.alt || k)}" title="${esc(b.alt || k)}"><img src="${esc(DS.bildUrl(DS.M, k, true))}" alt="" loading="lazy"></button>`; };
    let L = quelle === 'haus' ? hausFotos() : quelle === 'eigen' ? (DS.M.bilder || []).filter(b => b.eigen).map(b => b.key) : bergbilder();
    const voll = L.length, zeig = quelle === 'haus' && !hausAlle ? L.slice(0, 24) : L;
    box.innerHTML = zeig.map(knopf).join('') + (voll > zeig.length ? `<button type="button" class="ms-lnk bk-mehrfotos" id="bkMehrFotos"><span>Alle ${voll} Fotos zeigen</span>${PFEIL}</button>` : '')
      + (!voll ? '<p class="bk-satz">Noch keine eigenen Fotos in diesem Browser. Oben ein Foto hochladen.</p>' : '');
    box.querySelectorAll('[data-bkbild]').forEach(b => b.addEventListener('click', () => { s.bild = b.dataset.bkbild; zeichneFotos(); vorschau(); }));
    const mehr = $('#bkMehrFotos'); if (mehr) mehr.addEventListener('click', () => { hausAlle = true; zeichneFotos(); });
  }
  function zeichneGruende() {
    const box = $('#bkGruende'); if (!box) return;
    const s = zustand(), F = DS.M.farben || {};
    box.innerHTML = TOENE.map(([t, n, f]) => `<button type="button" class="bk-grund bk-grund--ton${t === s.ton ? ' an' : ''}" data-bkton="${t}" aria-pressed="${t === s.ton}" aria-label="${esc(n)}" style="--f:${esc(F[f] || '#0A2A4A')}"><i></i><span>${esc(n)}</span></button>`).join('');
    box.querySelectorAll('[data-bkton]').forEach(b => b.addEventListener('click', () => { s.ton = b.dataset.bkton; zeichneGruende(); vorschau(); }));
  }
  function formular() {
    if (!$('#pkForm')) return;
    zustand(); zeichneFotos(); zeichneGruende();
    document.querySelectorAll('[data-bkformat]').forEach(b => { const an = b.dataset.bkformat === zustand().format; b.classList.toggle('an', an); b.setAttribute('aria-pressed', an); });
    vorschau();
  }
  /* «Aushänge anlegen»: der gebaute Aushang in den drei Formaten, dazu derselbe auf den anderen Gründen; «Diesen bearbeiten» öffnet den Editor */
  function vorschlagen(ev) {
    if (ev) ev.preventDefault();
    const box = $('#pkVorschlaege');
    if ($('#pkThema').value.trim().length < 2) {
      $('#pkThema').setAttribute('aria-invalid', 'true'); $('#pkThema').focus();
      box.innerHTML = '<p class="pk-leer">Bitte zuerst einen Titel eintragen, zum Beispiel «Racletteabend im Stübli.»</p>'; return;
    }
    $('#pkThema').removeAttribute('aria-invalid');
    const s = zustand(), w = werte(), tn = t => (TOENE.find(x => x[0] === t) || [])[1] || '';
    const liste = ['insta', 'story', 'a3h'].map(f => ({ doc: bauDoc(f), t: FN[f], u: `${tn(s.ton)} · Ihr Aushang` }))
      .concat(TOENE.filter(t => t[0] !== s.ton).map(([t]) => ({ doc: bauDoc(null, t), t: 'Grund ' + tn(t), u: `${FN[s.format] || ''} · gleicher Text und dasselbe Foto` })));
    box.innerHTML = `<p class="pk-hinweis">${liste.length} Aushänge zu «${esc(w.titel)}»: in drei Formaten und auf den anderen Gründen. «Diesen bearbeiten» öffnet ihn im Editor.</p>`;
    box.dataset.n = liste.length; const gr = fach(box, liste.length);
    liste.forEach(x => box.appendChild(karte(x.doc, x.t, x.u, 'Diesen bearbeiten', gr)));
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function verdrahten() {
    $('#pkForm') && $('#pkForm').addEventListener('submit', vorschlagen);
    /* Robert 10.11.2026: aus dem Baukasten direkt im Editor weiter gestalten (Texte verschieben, Grössen, Foto), nicht an die festen Felder gebunden */
    const ed = $('#pkEditor'); if (ed) ed.addEventListener('click', () => {
      if ($('#pkThema').value.trim().length < 2) { $('#pkThema').setAttribute('aria-invalid', 'true'); $('#pkThema').focus(); return; }
      DSStudio.oeffne(bauDoc(zustand().format)); if (window.DSStart && DSStart.offen()) DSStart.zu();
    });
    ['pkThema', 'pkGast', 'pkZusatz', 'pkFreitag'].forEach(id => { const e = $('#' + id); if (e) e.addEventListener('input', () => { e.removeAttribute('aria-invalid'); vorschau(); }); });
    const d = $('#bkDatei'); if (d) d.addEventListener('change', hochladen);
    document.querySelectorAll('[data-bkformat]').forEach(b => b.addEventListener('click', () => { zustand().format = b.dataset.bkformat; document.querySelectorAll('[data-bkformat]').forEach(x => { x.classList.toggle('an', x === b); x.setAttribute('aria-pressed', x === b); }); vorschau(); }));
    document.querySelectorAll('[data-bkquelle]').forEach(b => b.addEventListener('click', () => { quelle = b.dataset.bkquelle; zeichneFotos(); }));
    addEventListener('resize', () => { if ($('#msAbend') && !$('#msAbend').hidden) vorschau(); });
  }

  function zeige(a) { if (a === 'motive') zeichneMotive(); if (a === 'abend') formular(); }
  async function los() {
    try { MOTIVE = await (await fetch(DS.M.basis + 'motive.json', { cache: 'no-cache' })).json(); } catch (e) { MOTIVE = []; }
    const z = $('#pkZahl'); if (z) z.textContent = bergbilder().length;
    verdrahten();
    if ($('#msAbend') && !$('#msAbend').hidden) formular();
  }
  window.DSPlakat = { zeige, aushangDoc, motive: () => MOTIVE };
  if (window.DS && DS.M && window.DSStudio) los(); else document.addEventListener('ds:bereit', los, { once: true });
})();
