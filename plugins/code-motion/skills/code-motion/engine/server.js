// Tiny static server so pages with ES modules / audio / textures load like on the web (file:// blocks modules).
// CLI preview: node serve.js <dir> [port]   -> open http://localhost:<port>/<page>.html
const http=require('http'),fs=require('fs'),path=require('path');
const TYPES={'.html':'text/html; charset=utf-8','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.json':'application/json',
 '.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.svg':'image/svg+xml','.gif':'image/gif',
 '.woff2':'font/woff2','.ttf':'font/ttf','.wav':'audio/wav','.mp3':'audio/mpeg','.m4a':'audio/mp4','.mp4':'video/mp4','.glb':'model/gltf-binary','.hdr':'application/octet-stream'};
function serve(root,port=0){
  root=path.resolve(root);
  const srv=http.createServer((req,res)=>{
    let rel; try{rel=decodeURIComponent(req.url.split('?')[0]);}catch(e){res.writeHead(400);return res.end();}
    if(rel.includes('\0')){res.writeHead(400);return res.end();}
    const p=path.join(root,rel);
    if(p!==root&&!p.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
    fs.readFile(p,(e,b)=>{ if(e){res.writeHead(404);return res.end('404');}
      res.writeHead(200,{'Content-Type':TYPES[path.extname(p).toLowerCase()]||'application/octet-stream','Cache-Control':'no-store'}); res.end(b);});
  });
  return new Promise(r=>srv.listen(port,'127.0.0.1',()=>r({port:srv.address().port,close:()=>srv.close(),url:f=>`http://127.0.0.1:${srv.address().port}/${encodeURIComponent(path.basename(f))}`})));
}
// open a built page in render mode and wait for fonts + window.READY
async function openPage(browser,html,{ar='',W=1920,H=1080}={}){
  const s=await serve(path.dirname(path.resolve(html)));
  const page=await browser.newPage({viewport:{width:W,height:H}});
  const errs=[]; page.on('pageerror',e=>errs.push(e.message)); page.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
  await page.goto(s.url(html)+'?render'+(ar?'&ar='+ar:''),{waitUntil:'load'});
  try{ await page.waitForFunction(()=>typeof window.seek==='function'&&window.DURATION>0,null,{timeout:30000}); }
  catch(e){ s.close(); throw new Error('page never called M.video (seek missing). Page errors: '+(errs.join(' | ')||'none, check the console in a browser preview')); }
  await page.evaluate(async()=>{await Promise.resolve(window.READY);await document.fonts.ready;});
  const info=await page.evaluate(()=>({T:window.DURATION,W:window.STAGE?window.STAGE.W:document.getElementById('stage').offsetWidth,H:window.STAGE?window.STAGE.H:document.getElementById('stage').offsetHeight,alpha:document.documentElement.classList.contains('alpha'),cues:window.CUES||[]}));
  await page.setViewportSize({width:info.W,height:info.H});
  return {page,info,errs,close:()=>{s.close();}};
}
module.exports={serve,openPage};
if(require.main===module){serve(process.argv[2]||'.',+(process.argv[3]||5173)).then(s=>console.log(`serving ${path.resolve(process.argv[2]||'.')} at http://127.0.0.1:${s.port}/  (Ctrl+C to stop)`));}
