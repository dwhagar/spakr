const { chromium } = require('playwright');
const fs=require('fs'); const axeSrc=fs.readFileSync(require.resolve('axe-core/axe.min.js'),'utf8');
const VPS=[['phone-small',320,568,2,1],['phone',390,844,3,1],['fold-cover',280,653,3,1],['fold-open',884,1104,2.5,1],['tablet',820,1180,2,1],['laptop',1366,768,1,1],['desktop',1920,1080,1,1],['tv-1080',1920,1080,1,1,'tv'],['tv-4k-raw',3840,2160,1,1,'tv']];
(async()=>{
 const b=await chromium.launch(); const out=[]; const viol=[];
 for(const [name,w,h,dsf,_,mode] of VPS) for(const scheme of ['light','dark']) for(const page of ['web-prototype/index.html','web-prototype/editor.html']){
  const ctx=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:dsf,colorScheme:scheme,hasTouch:dsf>1&&!mode,isMobile:dsf>1&&!mode});
  const p=await ctx.newPage();
  p.on('console',m=>{if(/Content Security|Refused/i.test(m.text()))viol.push(name+' '+m.text())});
  p.on('pageerror',e=>viol.push('err '+e.message));
  await p.goto((process.env.BASE||'http://127.0.0.1:8801/')+page); 
  if(mode==='tv') await p.click('[data-toggle-tv]');
  await p.waitForTimeout(150);
  const m=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,fs:getComputedStyle(document.body).fontSize,minTap:Math.min(...[...document.querySelectorAll('a,button,input,textarea')].filter(e=>e.offsetParent&&!e.classList.contains('skip')&&!e.closest('p,.crumbs,li.card,.infobox,.hint')).map(e=>Math.min(e.getBoundingClientRect().width,e.getBoundingClientRect().height))).toFixed(0)}));
  await p.evaluate(axeSrc); const ax=await p.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length)));
  out.push(`${name} ${scheme} ${page.split('/')[1]} overflow=${m.sw>m.cw} font=${m.fs} minTarget=${m.minTap} axe=[${ax}]`);
  if(page.endsWith('index.html')&&(scheme==='light'||name==='desktop'||name==='phone')) await p.screenshot({path:`shot-${name}-${scheme}.png`,fullPage:false});
  await ctx.close();
 }
 console.log(out.join('\n')); console.log('CSP/errors:',viol.length?viol.join('\n'):'none'); await b.close();
})();
