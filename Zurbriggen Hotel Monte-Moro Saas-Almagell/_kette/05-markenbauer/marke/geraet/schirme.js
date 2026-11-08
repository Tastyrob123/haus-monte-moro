/* Bildschirminhalte für Laptop (1440 × 932, Mass aus laptop.json) und Handy (1406 × 3054, Mass der iPhone-Textur), je Farbwelt. Hotel Monte-Moro, 17.10.2026. */
const path=require('path'),os=require('os');module.paths.push(path.join(os.homedir(),'Aussen-Pruefung','node_modules'));
const pw=require('playwright');const M=path.resolve(__dirname,'..');const Z=path.join(__dirname,'schirm');
(async()=>{const b=await pw.chromium.launch({headless:true});
for(const w of ['a','b']){
  for(const [name,cw,ch,scale] of [['laptop',1440,932,1.25],['handy',430,934,1406/430]]){
    const ctx=await b.newContext({viewport:{width:cw,height:ch},deviceScaleFactor:scale,locale:'de-CH'});const page=await ctx.newPage();
    await page.goto('file://'+path.join(M,'probe.html')+'?welt='+w,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
    await page.evaluate(()=>{document.body.classList.add('aufnahme');document.querySelectorAll('section').forEach(s=>s.classList.add('da'))});
    await page.waitForTimeout(3000);
    await page.screenshot({path:path.join(Z,`${name}-${w}.png`),type:'png'});
    await ctx.close();console.log(name,w,'ok');
  }
}
await b.close();})().catch(e=>{console.error(String(e));process.exit(1)});
