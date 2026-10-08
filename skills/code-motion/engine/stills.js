// Contact sheet of stills, the cheap way to review a whole cut before rendering video.
// usage: node stills.js <page.html> <sheet.png> [t1 t2 ...] [--every 1.0] [--cues] [--ar 9x16] [--cols 4] [--width 640]
//  no times given -> one still every second.  --cues -> one still 0.25s after every sound cue (the "hits").
// Also writes each frame as <sheet>-NN.png when --keep is passed (to inspect one at full size).
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const os=require('os');const {execFileSync}=require('child_process');
const {openPage}=require('./server');
const args=process.argv.slice(2); const html=args[0], out=args[1];
const opt=k=>{const i=args.indexOf('--'+k);return i>0?args[i+1]:undefined;}; const has=k=>args.includes('--'+k);
const flagged=new Set(); ['every','ar','cols','width'].forEach(k=>{const i=args.indexOf('--'+k); if(i>0){flagged.add(i);flagged.add(i+1);}});
let times=args.slice(2).filter((a,i)=>!flagged.has(i+2)&&!a.startsWith('--')).map(Number).filter(x=>!isNaN(x));
(async()=>{
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const P=await openPage(b,html,{ar:opt('ar')||''}); const {page,info}=P;
  if(has('cues')) times=[...new Set(info.cues.map(c=>+(c.t+0.25).toFixed(2)))].filter(t=>t<=info.T).sort((a,b)=>a-b);
  if(!times.length){const ev=+(opt('every')||1); for(let t=0.5;t<info.T;t+=ev) times.push(+t.toFixed(2)); times.push(+(info.T-0.05).toFixed(2));}
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'cm-st-'));
  if(info.alpha) await page.evaluate(()=>{document.documentElement.style.background='#000';document.body.style.background='#000';});
  for(let i=0;i<times.length;i++){
    await page.evaluate(t=>window.seek(t),times[i]);
    const f=path.join(dir,`${String(i).padStart(3,'0')}.png`);
    await page.screenshot({path:f});
    if(has('keep')) fs.copyFileSync(f,out.replace(/\.png$/i,'')+`-${String(i).padStart(2,'0')}.png`);
  }
  await b.close(); P.close();
  const cols=Math.min(+(opt('cols')||4),times.length), rows=Math.ceil(times.length/cols), w=+(opt('width')||(info.H>info.W?360:640));
  // label each tile with its time
  const lab=times.map((t,i)=>`[${i}:v]scale=${w}:-1,drawtext=text='${t.toFixed(2)}s':x=8:y=8:fontsize=${Math.round(w/24)}:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=4[v${i}]`);
  const inputs=times.flatMap((_,i)=>['-i',path.join(dir,`${String(i).padStart(3,'0')}.png`)]);
  const pad=cols*rows-times.length; const tiles=times.map((_,i)=>`[v${i}]`).join('');
  const filt=lab.join(';')+';'+(pad?`${tiles}concat=n=${times.length}:v=1:a=0,tpad=stop_mode=add:stop=${pad}:color=white[s];[s]`:`${tiles}concat=n=${times.length}:v=1:a=0[s];[s]`)+`tile=${cols}x${rows}:padding=4:color=white`;
  try{ execFileSync('ffmpeg',['-loglevel','error','-y',...inputs,'-filter_complex',filt,'-frames:v','1',out]); }
  catch(e){ execFileSync('ffmpeg',['-loglevel','error','-y','-i',path.join(dir,'%03d.png'),'-vf',`scale=${w}:-1,tile=${cols}x${rows}:padding=4:color=white`,'-frames:v','1',out]); }
  fs.rmSync(dir,{recursive:true,force:true});
  console.log(`sheet ${out}: ${times.length} stills at ${times.join(', ')}`+(P.errs.length?`\nPAGE ERRORS: ${[...new Set(P.errs)].slice(0,5).join(' | ')}`:''));
})().catch(e=>{console.error(e);process.exit(1);});
