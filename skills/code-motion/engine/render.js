// Render a built page frame by frame to video, with motion blur from subframes.
// usage: node render.js <page.html> <out.mp4|out.mov> [--fps 60] [--sub 4] [--workers 4] [--ar 9x16] [--from 0 --to T] [--crf 16]
//  --sub N   : N subframes per frame across a 180° shutter, averaged (1 = no blur, fast draft; 4 = final)
//  --workers : parallel browser pages, each renders a contiguous frame range, joined losslessly at the end
//  --jpeg   : capture JPEG q95 instead of PNG (≈2x faster capture, imperceptible loss after H.264; not for alpha)
//  .mov out  : ProRes 4444 with alpha (for bg:null pages); .mp4: H.264 yuv420p
// Also writes <out>.cues.json (the page's sound cues) for scripts/sfx.py.
const {chromium}=require('playwright');const {spawn,execFileSync}=require('child_process');const path=require('path');const fs=require('fs');const os=require('os');
const {openPage}=require('./server');
const args=process.argv.slice(2); const html=args[0], out=args[1];
const opt=k=>{const i=args.indexOf('--'+k);return i>0?args[i+1]:undefined;};
if(!html||!out){console.log('usage: node render.js page.html out.mp4 [--fps 60] [--sub 4] [--workers 4] [--ar 9x16]');process.exit(1);}
const JPEG=args.includes('--jpeg'); const FPS=+(opt('fps')||60), K=Math.max(1,+(opt('sub')||4)), WORKERS=Math.max(1,+(opt('workers')||Math.min(4,Math.max(1,os.cpus().length>>1)))), AR=opt('ar')||'', CRF=opt('crf')||'16';
(async()=>{
  const t0=Date.now();
  const browser=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const probe=await openPage(browser,html,{ar:AR}); const info=probe.info; await probe.page.close(); probe.close();
  const from=+(opt('from')||0), to=Math.min(+(opt('to')||info.T),info.T);
  const N=Math.round((to-from)*FPS); if(N<=0) throw new Error('nothing to render');
  fs.writeFileSync(out.replace(/\.(mp4|mov)$/i,'')+'.cues.json',JSON.stringify(info.cues.filter(c=>c.t>=from&&c.t<=to).map(c=>({...c,t:+(c.t-from).toFixed(4)})),null,1));
  const alpha=info.alpha&&/\.mov$/i.test(out);
  const enc=alpha?['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-vendor','apl0']:['-c:v','libx264','-crf',CRF,'-preset','medium','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709'];
  const sub=1/(FPS*2*K); // subframes span half a frame (180° shutter), centred on the frame time
  const csc=alpha?'':',scale=out_color_matrix=bt709:out_range=tv';   // convert + tag as BT.709 so HD players show true colours
  const vf=K>1?[`format=gbrap,tmix=frames=${K}:weights='${Array(K).fill(1).join(' ')}',select='eq(mod(n\\,${K})\\,${K-1})',setpts=N/(${FPS})/TB${csc}`]:(csc?[csc.slice(1)]:[]);
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'cm-render-'));
  const per=Math.ceil(N/WORKERS); const segs=[]; let done=0; const errs=[];
  const work=async w=>{
    const a=w*per, b=Math.min(N,a+per); if(a>=b) return;
    const seg=path.join(tmp,`seg${String(w).padStart(2,'0')}${alpha?'.mov':'.mp4'}`); segs[w]=seg;
    const P=await openPage(browser,html,{ar:AR}); P.page.on('pageerror',e=>errs.push(e.message));
    const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate',String(FPS*K),'-c:v',(JPEG&&!alpha)?'mjpeg':'png','-i','-',...(vf.length?['-vf',vf[0]]:[]),'-r',String(FPS),...enc,seg]);
    ff.stderr.on('data',d=>process.stderr.write(d));
    for(let f=a;f<b;f++){ for(let k=0;k<K;k++){
        const t=Math.max(0,from+f/FPS+(K>1?(k-(K-1)/2)*sub:0));
        await P.page.evaluate(t=>window.seek(t),t);
        const buf=(JPEG&&!alpha)?await P.page.screenshot({type:'jpeg',quality:95}):await P.page.screenshot({type:'png',omitBackground:alpha});
        if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); }
      done++; if(done%Math.max(1,Math.round(FPS))===0) process.stdout.write(`\r  ${done}/${N} frames  ${((Date.now()-t0)/1000).toFixed(0)}s `);
    }
    ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await P.page.close(); P.close();
  };
  await Promise.all(Array.from({length:WORKERS},(_,w)=>work(w)));
  await browser.close();
  const list=path.join(tmp,'list.txt'); fs.writeFileSync(list,segs.filter(Boolean).map(s=>`file '${s.replace(/\\/g,'/')}'`).join('\n'));
  execFileSync('ffmpeg',['-loglevel','error','-y','-f','concat','-safe','0','-i',list,'-c','copy',...(alpha?[]:['-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-movflags','+faststart']),out]);
  fs.rmSync(tmp,{recursive:true,force:true});
  console.log(`\nrendered ${out}  ${N} frames @${FPS}fps x${K} sub, ${info.W}x${info.H}, ${((Date.now()-t0)/1000).toFixed(1)}s${errs.length?'  PAGE ERRORS: '+[...new Set(errs)].slice(0,3).join(' | '):''}`);
})().catch(e=>{console.error(e);process.exit(1);});
