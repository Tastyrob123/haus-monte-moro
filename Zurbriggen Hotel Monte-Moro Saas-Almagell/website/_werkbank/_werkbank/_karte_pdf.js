
const path = require('path');
let PW; try { PW = require('playwright'); } catch (e) { PW = require('/opt/node-tools/node_modules/playwright'); }
const { chromium } = PW;
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('http://127.0.0.1:9388/werkbank/karte.html', { waitUntil: 'load' }); await p.evaluate(() => document.fonts && document.fonts.ready);
  // feste TrueType-Schnitte für den Druck (variable Schriften landen sonst als «Type 3» in der PDF, Apple-Vorschau zeichnet sie weich)
  await p.addStyleTag({ content: "@font-face{font-family:'TDruck';src:url(/_werkbank/fonts/FjallaOne-Regular.ttf)}" +
    "@font-face{font-family:'IDruck';font-weight:400;src:url(/_werkbank/fonts/InstrumentSans-Regular.ttf)}@font-face{font-family:'IDruck';font-weight:500;src:url(/_werkbank/fonts/InstrumentSans-Medium.ttf)}@font-face{font-family:'IDruck';font-weight:600 900;src:url(/_werkbank/fonts/InstrumentSans-SemiBold.ttf)}" +
    "@font-face{font-family:'MDruck';src:url(/_werkbank/fonts/DMMono-Regular.ttf)}:root{--serif:'TDruck','Arial Narrow',sans-serif!important;--sans:'IDruck',Arial,sans-serif!important;--mono:'MDruck',monospace!important}" +
    "body,body *{font-family:'IDruck',Arial,sans-serif}h1,h2,h3,h4,.mn-titel,[class*=mn-] b{font-family:'TDruck','Arial Narrow',sans-serif}.mn-haus,.mn-gang,.mn-gang span,.mn-ende span{font-family:'MDruck',monospace}" });
  await p.evaluate(() => document.fonts && document.fonts.ready); await p.waitForTimeout(800);
  await p.pdf({ path: process.argv[2], format: 'A4', printBackground: true, preferCSSPageSize: true }); await b.close(); console.log('PDF', process.argv[2]); })();
