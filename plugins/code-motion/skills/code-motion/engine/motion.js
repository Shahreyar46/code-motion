/* code-motion engine. Every frame is a pure function of time: seek(t) draws frame t.
   No CSS transitions, no timers, no state carried between frames. That is what makes
   frame-exact rendering, motion blur by subframes and re-renders after edits possible. */
(function(){
const M = window.M = {};
const qs = new URLSearchParams(location.search);
M.RENDER = qs.has('render');
M.AR = qs.get('ar') || '';                     // '16x9' | '9x16' | '1x1' | '' (fragment default)

/* ---------- math + easing ---------- */
const clamp = M.clamp = (x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const lerp = M.lerp = (a,b,u)=>a+(b-a)*u;
M.map = (x,a,b,c=0,d=1)=>lerp(c,d,clamp((x-a)/(b-a)));
const eo = M.eo = x=>{x=clamp(x);return 1-Math.pow(1-x,3)};          // ease out cubic
M.eo5 = x=>{x=clamp(x);return 1-Math.pow(1-x,5)};                     // ease out quint (snappy)
M.ei = x=>{x=clamp(x);return x*x*x};
const eio = M.eio = x=>{x=clamp(x);return x*x*x*(x*(6*x-15)+10)};    // smootherstep
M.expo = x=>{x=clamp(x);return x===1?1:1-Math.pow(2,-10*x)};
M.back = (x,s=1.4)=>{x=clamp(x)-1;return 1+x*x*((s+1)*x+s)};          // tiny overshoot, use sparingly
M.win = (t,a,b)=>clamp((t-a)/(b-a));                                  // linear 0..1 progress over [a,b]

/* ---------- closed-form springs ---------- */
// step response 0 -> 1 with zero initial velocity; tau = time since trigger
const S = M.S = (tau,w,z)=>{
  if(tau<=0) return 0;
  if(!isFinite(w)) return 1;
  if(z<1){const wd=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*tau)*(Math.cos(wd*tau)+z*w/wd*Math.sin(wd*tau));}
  if(z===1) return 1-Math.exp(-w*tau)*(1+w*tau);
  const r=w*Math.sqrt(z*z-1), a=w*z-r, b=w*z+r;               // over-damped
  return 1-(b*Math.exp(-a*tau)-a*Math.exp(-b*tau))/(b-a);
};
// presets [omega, zeta]. MORPH = default UI morph, FAST/SLOW = leading/trailing edges, CAM = camera
M.MORPH=[15,0.84]; M.FAST=[27,0.86]; M.SLOW=[12.5,0.9]; M.SOFT=[10,0.95]; M.CAM=[7.5,1]; M.POP=[22,0.62]; M.INSTANT=[Infinity,1];
M.sp = (t,t0,s=M.MORPH)=>S(t-t0,s[0],s[1]);                           // one spring 0->1 triggered at t0

// a value that changes target many times = the sum of one spring per change (still a pure function of t)
M.track = (v0,keys,def=M.MORPH,period=0)=>{
  let prev=v0; const ks=[];
  for(const k of keys){const d=k[1]-prev; prev=k[1]; const sp=k[2]||def; if(d!==0) ks.push([k[0],d,sp[0],sp[1]]);}
  const loop = period>0 && Math.abs(prev-v0)<1e-9;
  return t=>{let v=v0; for(const k of ks){v+=k[1]*S(t-k[0],k[2],k[3]); if(loop) v+=k[1]*(S(t+period-k[0],k[2],k[3])-1);} return v;};
};
const hex = M.hex = h=>{ if(/^#[0-9a-f]{3}$/i.test(h)) h='#'+[...h.slice(1)].map(c=>c+c).join(''); if(!/^#[0-9a-f]{6}$/i.test(h)) throw new Error('colour must be #rgb or #rrggbb: '+h); return [1,3,5].map(i=>parseInt(h.slice(i,i+2),16)); };
M.ctrack = (h0,keys,def=[20,1],period=0)=>{
  const c0=hex(h0); const tr=[0,1,2].map(i=>M.track(c0[i],keys.map(k=>[k[0],hex(k[1])[i],k[2]]),def,period));
  return t=>`rgb(${tr.map(f=>Math.round(clamp(f(t),0,255))).join(',')})`;
};
M.mix = (h1,h2,u)=>{const a=hex(h1),b=hex(h2);return `rgb(${a.map((v,i)=>Math.round(lerp(v,b[i],clamp(u)))).join(',')})`;};
M.step = (v0,keys)=>t=>{let v=v0; for(const k of keys) if(t>=k[0]) v=k[1]; return v;};

/* ---------- deterministic randomness ---------- */
M.rand = seed=>{let a=(seed*2654435761)>>>0;return ()=>{a=(a+0x6D2B79F5)>>>0;let x=Math.imul(a^a>>>15,1|a);x^=x+Math.imul(x^x>>>7,61|x);return((x^x>>>14)>>>0)/4294967296;};};
const h1 = n=>{const x=Math.sin(n*127.1)*43758.5453;return x-Math.floor(x);};
M.noise = x=>{const i=Math.floor(x),f=x-i,u=f*f*(3-2*f);return lerp(h1(i),h1(i+1),u)*2-1;};   // smooth -1..1
M.shake = (t,t0,amp=14,dur=0.35,freq=38)=>{const k=t-t0; if(k<0||k>dur) return [0,0]; const e=Math.pow(1-k/dur,2)*amp; return [M.noise(t*freq)*e, M.noise(t*freq+91.7)*e];};

/* ---------- visibility: enter/exit with blur (content swap) ---------- */
M.vis = (t,tin,tout,o={})=>{
  const din=o.din??0.0, lin=o.lin??0.32, lout=o.lout??0.18, bl=o.blur??12;
  const a = tin==null?1:eo((t-tin-din)/lin);
  const b = tout==null?0:eo((t-tout)/lout);
  return {o:a*(1-b), blur:(1-a)*bl+b*bl*0.8, s:(0.94+0.06*a)*(1-0.03*b), a, b, on:a*(1-b)>0.002};
};
M.apply = (el,v,extra='')=>{
  if(v.o<0.002){el.style.visibility='hidden';return false;}
  el.style.visibility=''; el.style.opacity=v.o.toFixed(4);
  el.style.filter=v.blur>0.05?`blur(${v.blur.toFixed(2)}px)`:'none';
  el.style.transform=`${extra} scale(${v.s.toFixed(4)})`;
  return true;
};
M.show = (el,on)=>{el.style.visibility=on?'':'hidden';};
M.setText = (el,s)=>{ if(el._t!==s){ el.textContent=s; el._t=s; } };
M.$ = id=>document.getElementById(id);
M.css = (el,o)=>{for(const k in o) el.style[k]=o[k];};

/* ---------- kinetic type ---------- */
// split an element's text into spans once at setup. mode 'words' | 'chars'. keeps spaces.
M.split = (el,mode='words')=>{
  const txt=el.textContent; el.textContent='';
  const parts = mode==='chars'?[...txt]:txt.split(/(\s+)/);
  const out=[];
  for(const p of parts){
    if(/^\s+$/.test(p)){el.appendChild(document.createTextNode(p));continue;}
    if(!p) continue;
    const s=document.createElement('span'); s.textContent=p; s.style.display='inline-block'; s.style.willChange='auto';
    el.appendChild(s); out.push(s);
  }
  return out;
};
// per-span entrance. times: number (start) + step, or array of absolute times (e.g. VO word times)
// style: 'rise' | 'drop' | 'blur' | 'scale' | 'slam' | 'mask'
M.words = (spans,t,times,o={})=>{
  const step=o.step??0.06, style=o.style||'rise', spg=o.spring||M.MORPH, dist=o.dist??0.6;
  spans.forEach((s,i)=>{
    const t0=Array.isArray(times)?times[Math.min(i,times.length-1)]:times+i*step;
    const p=S(t-t0,spg[0],spg[1]), q=clamp((t-t0)/0.18);
    const em=parseFloat(getComputedStyle(s).fontSize)||40;
    let tf='', op=q, bl=0;
    if(style==='rise'){tf=`translateY(${((1-p)*dist*em).toFixed(2)}px)`; bl=(1-q)*6;}
    else if(style==='drop'){tf=`translateY(${(-(1-p)*dist*em).toFixed(2)}px)`;}
    else if(style==='blur'){bl=(1-eo(q))*14; tf=`scale(${(1.08-0.08*p).toFixed(4)})`;}
    else if(style==='scale'){tf=`scale(${(0.6+0.4*p).toFixed(4)})`;}
    else if(style==='slam'){const k=S(t-t0,24,0.55); tf=`scale(${(2.2-1.2*k).toFixed(4)})`; op=clamp((t-t0)/0.05);}
    else if(style==='mask'){tf=`translateY(${((1-p)*1.05*em).toFixed(2)}px)`; op=t>=t0?1:0; s.parentElement.style.overflow='hidden';}
    s.style.transform=tf; s.style.opacity=op.toFixed(3); s.style.filter=bl>0.05?`blur(${bl.toFixed(2)}px)`:'none';
  });
};
// animated number: eased count from->to over [t0,t0+dur]. fmt: (n)=>string
M.count = (t,t0,dur,from,to,fmt=n=>Math.round(n).toLocaleString('en-US'))=>fmt(lerp(from,to,M.expo((t-t0)/dur)));
// typewriter: substring at cps characters/second, with deterministic caret
M.typed = (text,t,t0,cps=28)=>text.slice(0,Math.max(0,Math.floor((t-t0)*cps)));
M.caret = (t)=>((t*2)%2<1.25)?'|':' ';
// draw an SVG stroke on: path/line/circle element. lazily caches length
M.stroke = (el,t,t0,dur=0.6,ease=M.eio)=>{
  if(el._len==null){el._len=el.getTotalLength(); el.style.strokeDasharray=el._len;}
  el.style.strokeDashoffset=(el._len*(1-ease((t-t0)/dur))).toFixed(2);
};
// shrink font until el fits maxW (call once at setup, after fonts load)
M.fit = (el,maxW,min=10)=>{let fs=parseFloat(getComputedStyle(el).fontSize); while(el.scrollWidth>maxW&&fs>min){fs-=1;el.style.fontSize=fs+'px';} return fs;};

/* ---------- pro-video helpers (learned from Numtera, LangEase, Teamble, Gemini, Google Search refs) ---------- */
// n staggered spring values: chips, list rows, tiles
M.stagger = (n,t,t0,gap=0.08,s=M.MORPH)=>Array.from({length:n},(_,i)=>S(t-t0-i*gap,s[0],s[1]));
// fly-through exit: text/scene rushes past the camera. returns {s, blur, o}; apply as transform scale + filter
M.flyOut = (t,t0,dur=0.32,o={})=>{const e=M.ei(clamp((t-t0)/dur)); return {s:1+(o.scale??0.6)*e, blur:(o.blur??30)*e, o:1-e};};
// blur-in focus pull (rack focus): 1 -> 0 blur factor
M.focus = (t,t0,dur=0.5)=>1-eo((t-t0)/dur);
// directional smear for fast moves: returns CSS transform+filter for a move whose progress is p (0..1)
M.smear = (p,axis='x',k=0.35,blur=10)=>{const v=4*p*(1-p); return {tf:axis==='x'?`scaleX(${1+k*v})`:`scaleY(${1+k*v})`, f:`blur(${(blur*v).toFixed(2)}px)`};};
// gradient text that slowly sweeps. call once: M.gradInit(el,['#4285F4','#A78BFA']); per frame: M.gradText(el,t,speed)
M.gradInit = (el,stops,angle=90)=>{el.style.backgroundImage=`linear-gradient(${angle}deg,${[...stops,stops[0]].join(',')})`;el.style.backgroundSize='200% 100%';el.style.webkitBackgroundClip='text';el.style.backgroundClip='text';el.style.color='transparent';};
M.gradText = (el,t,speed=12)=>{el.style.backgroundPosition=`${(t*speed)%200}% 0`;};
// cycle words in one slot every `per` seconds with blur crossfade. returns {word, v} for the current word
M.cycle = (words,t,t0,per=0.7,fade=0.18)=>{const k=Math.max(0,t-t0), i=Math.min(words.length-1,Math.floor(k/per)), u=k-i*per;
  const last=i===words.length-1; const a=eo(u/fade), b=last?0:eo((u-per+fade)/fade); return {word:words[i], i, o:a*(1-b), blur:(1-a)*10+b*10, y:(1-a)*14-b*14};};
// letter scramble assemble: chars fly in from seeded random offsets with blur, snap into place. spans from M.split(el,'chars')
M.scramble = (spans,t,t0,dur=0.8,spread=220,seed=3)=>{const r=M.rand(seed);
  spans.forEach((s,i)=>{const dx=(r()-0.5)*2*spread, dy=(r()-0.5)*spread, rot=(r()-0.5)*60, d=r()*0.25;
    const p=S(t-t0-d,11,0.85), q=clamp((t-t0-d)/0.15);
    s.style.transform=`translate(${(dx*(1-p)).toFixed(1)}px,${(dy*(1-p)).toFixed(1)}px) rotate(${(rot*(1-p)).toFixed(1)}deg)`;
    s.style.opacity=q.toFixed(3); s.style.filter=p<0.98?`blur(${(8*(1-p)).toFixed(2)}px)`:'none';});};
// per-character width stretch / squash wave (Google "search" stretch)
M.stretch = (spans,t,t0,from=0.2,to=1,gap=0.04,s=M.MORPH)=>spans.forEach((e,i)=>{const p=S(t-t0-i*gap,s[0],s[1]); e.style.transform=`scaleX(${lerp(from,to,p).toFixed(4)})`; e.style.transformOrigin='0 50%';});
// ripple rings behind a pill/button: returns [{s,o}] per ring
M.ripple = (t,t0,n=3,gap=0.1,dur=0.9,maxS=1.8)=>Array.from({length:n},(_,i)=>{const u=clamp((t-t0-i*gap)/dur); return {s:1+(maxS-1)*eo(u), o:u>0&&u<1?(1-u)*(1-i/n)*0.6:0};});
// seeded confetti/particle burst, pure f(t): returns [{x,y,r,o,c}] relative to origin
M.burst = (t,t0,n=40,o={})=>{const r=M.rand(o.seed??11), cols=o.colors||['#4F7BFF','#6EC6F5','#FF7AB6','#FFD45E'], g=o.gravity??900, sp=o.speed??900, life=o.life??1.4;
  const k=t-t0; if(k<0||k>life) return [];
  return Array.from({length:n},(_,i)=>{const a=(o.angle??-Math.PI/2)+(r()-0.5)*(o.spread??Math.PI*1.6), v=sp*(0.35+0.65*r()), dr=Math.exp(-1.6*k);
    return {x:Math.cos(a)*v*(1-dr)/1.6, y:Math.sin(a)*v*(1-dr)/1.6+0.5*g*k*k*0.35, r:(r()*720-360)*k, o:1-M.ei(k/life), c:cols[i%cols.length], s:0.6+r()*0.8};});};
// ambient drifting blurred orbs background. call M.orbsInit(container,[{c:'#B9A6FF',x:.2,y:.2,r:700}]) once; M.orbs(t) per frame
M.orbsInit = (box,orbs)=>{box.innerHTML=''; return orbs.map((o,i)=>{const d=document.createElement('div'); d.style.cssText=`position:absolute;width:${o.r}px;height:${o.r}px;border-radius:50%;background:radial-gradient(circle,${o.c} 0%,transparent 70%);${o.blur?`filter:blur(${o.blur}px);`:''}opacity:${o.o??0.8}`; box.appendChild(d); return {...o,el:d,ph:i*1.7};});};
M.orbs = (list,t,W,H,amp=60,speed=0.25)=>list.forEach(o=>{const x=o.x*W-o.r/2+Math.sin(t*speed+o.ph)*amp, y=o.y*H-o.r/2+Math.cos(t*speed*0.8+o.ph)*amp; o.el.style.transform=`translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`;});
// breathing glow alpha
M.pulse = (t,period=2.4,lo=0.45,hi=0.75)=>lo+(hi-lo)*(0.5+0.5*Math.sin(2*Math.PI*t/period));
// scan line sweep progress (for "analysing" cards)
M.sweep = (t,t0,dur=1.2)=>clamp((t-t0)/dur);

// curved move from p0 to p1 with adjustable bend (perpendicular bow, px; negative bends the other way)
M.arc = (t,t0,dur,p0,p1,bend=120,ease=eio)=>{const e=ease((t-t0)/dur), dx=p1[0]-p0[0], dy=p1[1]-p0[1], L=Math.hypot(dx,dy)||1, b=bend*Math.sin(Math.PI*e);
  return {x:p0[0]+dx*e-dy/L*b, y:p0[1]+dy*e+dx/L*b, e};};
// horizontal-only (or vertical-only) motion blur via a per-element SVG filter. amt in px; axis 'x' | 'y'
M.xblur = (el,amt,axis='x')=>{
  if(!el._xb){ const id='cmxb'+Math.random().toString(36).slice(2,8); let defs=document.getElementById('cm-filters');
    if(!defs){ defs=document.createElementNS('http://www.w3.org/2000/svg','svg'); defs.id='cm-filters'; defs.setAttribute('width','0'); defs.setAttribute('height','0'); defs.style.position='absolute'; document.body.appendChild(defs); }
    defs.insertAdjacentHTML('beforeend',`<filter id="${id}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0 0"/></filter>`);
    el._xb=defs.querySelector('#'+id+' feGaussianBlur'); el._xbid=id; }
  const a=Math.max(0,amt); el._xb.setAttribute('stdDeviation',axis==='x'?`${a.toFixed(2)} 0`:`0 ${a.toFixed(2)}`);
  el.style.filter=a>0.05?`url(#${el._xbid})`:'none';
};
// white (or any colour) flash: opacity 0 -> 1 -> 0 over dur, peak at t0 + dur/2 (swap scenes at the peak)
M.flash = (t,t0,dur=0.18)=>{const u=(t-t0)/dur; return u<0||u>1?0:Math.sin(Math.PI*u);};
// fly N items along an SVG path (element or 'M..' string), staggered; for "file chips into a folder" moves.
// returns [{x,y,angle,p,s,o,landed}] in the path's coordinate space. o.dur per item, o.gap stagger, o.ease, o.land (overshoot scale on landing)
M.along = (path,n,t,t0,o={})=>{
  if(typeof path==='string'){ M._paths=M._paths||{}; if(!M._paths[path]){const p=document.createElementNS('http://www.w3.org/2000/svg','path'); p.setAttribute('d',path); M._paths[path]=p;} path=M._paths[path]; }
  const L=path._len??(path._len=path.getTotalLength()), dur=o.dur??0.65, gap=o.gap??0.08, ease=o.ease||eio;
  return Array.from({length:n},(_,i)=>{const a=t0+i*gap, p=ease((t-a)/dur), pt=path.getPointAtLength(L*p), pt2=path.getPointAtLength(Math.min(L,L*p+1));
    const land=S(t-a-dur,22,0.55); const s=t<a?0:(p<1?0.75+0.25*eo((t-a)/0.15):1+0.18*(1-land)*Math.sin(Math.PI*Math.min(1,(t-a-dur)/0.25)));
    return {x:pt.x, y:pt.y, angle:Math.atan2(pt2.y-pt.y,pt2.x-pt.x)*180/Math.PI, p, s, o:t<a?0:Math.min(1,(t-a)/0.08), landed:t>=a+dur, t:a};});
};

/* ---------- camera ---------- */
// 2D camera on a world element: x,y = world point at screen centre, s = zoom, r = degrees
M.cam = (el,W,H,x,y,s=1,r=0)=>{el.style.transformOrigin='0 0';el.style.transform=`translate(${W/2}px,${H/2}px) rotate(${r}deg) scale(${s}) translate(${-x}px,${-y}px)`;};
// 2.5D tilt for UI cards: rx,ry degrees
M.tilt = (rx,ry,z=0,persp=1800)=>`perspective(${persp}px) rotateX(${rx}deg) rotateY(${ry}deg) translateZ(${z}px)`;

/* ---------- cursor ---------- */
M.path = (CK)=>t=>{
  if(t<=CK[0][0]) return {x:CK[0][1],y:CK[0][2]};
  const L=CK[CK.length-1]; if(t>=L[0]) return {x:L[1],y:L[2]};
  let i=0; while(t>=CK[i+1][0]) i++;
  const [t0,x0,y0]=CK[i],[t1,x1,y1]=CK[i+1];
  const u=eio((t-t0)/(t1-t0)), dx=x1-x0, dy=y1-y0, arc=Math.sin(Math.PI*u)*0.06;
  return {x:x0+dx*u-dy*arc, y:y0+dy*u+dx*arc};
};
M.presses = (clicks=[],drags=[])=>{
  const k=[];
  for(const c of clicks){k.push([c-0.07,1,[45,1]],[c+0.035,0,[22,0.72]]);}
  for(const [a,b] of drags){k.push([a-0.04,1,[45,1]],[b,0,[22,0.72]]);}
  k.sort((a,b)=>a[0]-b[0]); return M.track(0,k);
};
M.CURSOR = '<svg viewBox="0 0 40 56" width="40"><path d="M3 3 L3 41 L12.5 32 L19 47 L25.5 44.2 L19.2 29.8 L32 29.8 Z" fill="#0B0B0B" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>';
M.crossTimes = (f,t0,t1,ths)=>ths.map(th=>{for(let t=t0;t<=t1;t+=0.001) if(f(t)>=th) return t; return Infinity;});

/* ---------- icons (24-grid stroke, Lucide-style, ISC) ---------- */
M.IC = {
 arrow:['M5 12h14','M13 5l7 7-7 7'], check:['M20 6 9 17l-5-5'], x:['M18 6 6 18','M6 6l12 12'], plus:['M5 12h14','M12 5v14'],
 folder:['M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z'],
 terminal:['m4 17 6-6-6-6','M12 19h8'], file:['M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z','M14 2v4a2 2 0 0 0 2 2h4','M8 13h8','M8 17h5'],
 pencil:['M21.17 6.81a1 1 0 0 0-3.99-3.99L3.84 16.17a2 2 0 0 0-.5.83l-1.32 4.35a.5.5 0 0 0 .62.62l4.35-1.32a2 2 0 0 0 .83-.5z','m15 5 4 4'],
 clock:['M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z','M12 6v6l4 2'],
 sparkle:['M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.14-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.14a.5.5 0 0 1 .96 0L14.06 8.5A2 2 0 0 0 15.5 9.94l6.14 1.58a.5.5 0 0 1 0 .96L15.5 14.06a2 2 0 0 0-1.44 1.44l-1.58 6.14a.5.5 0 0 1-.96 0z'],
 search:['M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z','m21 21-4.3-4.3'],
 bolt:['M13 2 3 14h9l-1 8 10-12h-9l1-8z'], shield:['M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z'],
 user:['M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2','M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z'], chart:['M3 3v18h18','m19 9-5 5-4-4-3 3'],
 mail:['M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z','m22 6-10 7L2 6'], bell:['M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9','M10.3 21a1.94 1.94 0 0 0 3.4 0'],
 lock:['M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2Z','M7 11V7a5 5 0 0 1 10 0v4'], globe:['M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z','M2 12h20','M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z'],
 moon:['M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z'], sun:['M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z','M12 2v2','M12 20v2','m4.93 4.93 1.41 1.41','m17.66 17.66 1.41 1.41','M2 12h2','M20 12h2','m6.34 17.66-1.41 1.41','m19.07 4.93-1.41 1.41'],
 play:['m6 3 14 9-14 9V3z'], heart:['M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z'],
 code:['m16 18 6-6-6-6','m8 6-6 6 6 6'], cart:['M8 22a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z','M19 22a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z','M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12'],
};
M.icon = (name,size,color,sw=2)=>`<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${(M.IC[name]||M.IC.sparkle).map(d=>`<path d="${d}"/>`).join('')}</svg>`;

/* ---------- voiceover timing (injected by build.py from timings.json) ---------- */
// VO = {duration, lines:[{id,text,start,end,words:[{w,start,end}]}]}
const VO = window.VO || {duration:0, lines:[]};
M.VO = VO;
M.line = id=>{const l=VO.lines.find(l=>l.id===id); if(!l) throw new Error('VO line not found: '+id); return l;};
// time a word is spoken. which = index (0-based) or the word text (first match, case/punct-insensitive)
M.word = (id,which=0,edge='start')=>{
  const l=M.line(id), ws=l.words||[];
  if(!ws.length) return l[edge];
  let w;
  if(typeof which==='number') w=ws[Math.max(0,Math.min(ws.length-1,which<0?ws.length+which:which))];
  else {const n=s=>s.toLowerCase().replace(/[^\p{L}\p{N}]/gu,''); w=ws.find(x=>n(x.w)===n(which))||ws.find(x=>n(x.w).startsWith(n(which)));}
  if(!w) throw new Error(`word "${which}" not in line ${id}`);
  return w[edge];
};
M.words$ = id=>(M.line(id).words||[]).map(w=>w.start);   // all word start times of a line

/* ---------- sound cues: declared once at setup, exported to the SFX mixer ---------- */
// M.cue(t, 'whoosh', {g:0.8, pan:-0.2, d:0.5}) ; names: see scripts/sfx.py --list
const CUES = window.CUES = [];
M.cue = (t,s,o={})=>{CUES.push({t:+t.toFixed(4),s,...o}); return t;};

/* ---------- video runner ---------- */
// M.video({W,H,T,bg,draw(t)}) -> sizes the stage, exposes window.seek / DURATION, preview player
M.video = (cfg)=>{
  const {W,H,T}=cfg; const stage=M.$('stage'), wrap=M.$('wrap');
  stage.style.width=W+'px'; stage.style.height=H+'px'; wrap.style.width=W+'px'; wrap.style.height=H+'px';
  stage.style.background=cfg.bg||'transparent';
  if(!cfg.bg) document.documentElement.classList.add('alpha');
  window.DURATION=T; window.STAGE={W,H};
  window.seek=t=>{cfg.draw(clamp(t,0,T));};
  M._preview(W,H,T);
  return window.seek;
};
// preview: loops in a normal browser; space = play/pause, arrows = step, click bar = scrub, ?t=4.2 = freeze
M._preview = (W,H,T)=>{
  document.body.classList.add(M.RENDER?'render':'preview');
  const ready = Promise.resolve(window.READY).then(()=>document.fonts.ready);
  ready.then(()=>window.seek(+(qs.get('t')||0)));
  if(M.RENDER) return;
  const wr=M.$('wrap');
  const fit=()=>{const k=Math.min(innerWidth/W,(innerHeight-46)/H);wr.style.transform=`translate(-50%,-50%) scale(${k})`;};
  fit(); addEventListener('resize',fit);
  const bar=document.createElement('div'); bar.id='pbar'; bar.innerHTML='<div id="pfill"></div><span id="ptime"></span>'; document.body.appendChild(bar);
  let audio=null; if(window.AUDIO_SRC){audio=new Audio(window.AUDIO_SRC);}
  let playing=!qs.has('t'), t=+(qs.get('t')||0), last=performance.now();
  const toggle=()=>{playing=!playing; if(audio){ if(playing){audio.currentTime=t;audio.play().catch(()=>{});} else audio.pause(); }};
  addEventListener('keydown',e=>{ if(e.code==='Space'){e.preventDefault();toggle();}
    if(e.code==='ArrowRight'){t=Math.min(T,t+(e.shiftKey?1:1/30));playing=false;audio&&audio.pause();}
    if(e.code==='ArrowLeft'){t=Math.max(0,t-(e.shiftKey?1:1/30));playing=false;audio&&audio.pause();} });
  bar.addEventListener('click',e=>{t=T*e.offsetX/bar.offsetWidth; if(audio) audio.currentTime=t;});
  document.addEventListener('click',e=>{ if(audio&&audio.paused&&playing&&e.target!==bar){audio.currentTime=t;audio.play().catch(()=>{});} });
  ready.then(()=>{const loop=now=>{
    if(playing){ if(audio&&!audio.paused) t=audio.currentTime; else t+= (now-last)/1000; if(t>T+0.6){t=0; if(audio){audio.currentTime=0;}} }
    last=now; window.seek(Math.min(t,T));
    M.$('pfill').style.width=(100*Math.min(t,T)/T)+'%'; M.$('ptime').textContent=`${Math.min(t,T).toFixed(2)}s / ${T.toFixed(2)}s  ·  space play/pause  ←/→ step${audio?'  ·  click page for sound':''}`;
    requestAnimationFrame(loop);}; requestAnimationFrame(loop);});
};

/* ---------- one-shape morph scene (Dribbble-style UI motion) ----------
 Needs markup: <div id="world"><div id="shape">…layers…</div></div><div id="cursor"></div>
 cfg = { W,H,T, bg, center:[x,y], SH:{name:{w,h,r,bg,cam}}, start, SEQ:[[t,name]],
         layers:[{el,tin,tout,anchor:'c'|'t'|'l',update(t,g)}], cursor:{keys,clicks,drags,size},
         shapePress:[t], intro, geom(t,g), extra(t,g) } */
M.morph = (cfg)=>{
  const $=M.$; const {W,H}=cfg; const [CX,CY]=cfg.center||[W/2,H/2];
  const world=$('world'), shape=$('shape'), cur=$('cursor');
  if(cur&&!cur.innerHTML) cur.innerHTML=M.CURSOR;
  const P0=cfg.SH[cfg.start], SEQ=cfg.SEQ, sp=cfg.spring||M.MORPH;
  const tr=k=>M.track(P0[k],SEQ.map(([t,n])=>[t,cfg.SH[n][k]]),sp);
  const shW=tr('w'), shH=tr('h'), shR=tr('r');
  const shBG=M.ctrack(P0.bg,SEQ.map(([t,n])=>[t,cfg.SH[n].bg]),[20,1]);
  const cam=M.track(P0.cam,SEQ.map(([t,n])=>[t,cfg.SH[n].cam]),cfg.camSpring||M.CAM);
  const press=M.track(0,(cfg.shapePress||[]).flatMap(c=>[[c-0.07,1,[45,1]],[c+0.035,0,[22,.72]]]));
  const intro=cfg.intro===undefined?0.02:cfg.intro;
  const cpath=cfg.cursor?M.path(cfg.cursor.keys):null, cpress=cfg.cursor?M.presses(cfg.cursor.clicks,cfg.cursor.drags):null;
  if(cur){ if(cfg.cursor) cur.style.width=(cfg.cursor.size||46)+'px'; else cur.style.display='none'; }
  const layers=(cfg.layers||[]).map(L=>({...L,node:$(L.el)}));
  return M.video({W,H,T:cfg.T,bg:cfg.bg,draw:(t)=>{
    let g={t, w:shW(t), h:shH(t), r:shR(t), bg:shBG(t), s:cam(t), cx:0, cy:0, fx:0, fy:0, sc:1-0.035*press(t), op:1};
    if(intro!=null){const a=S(t-intro,13,0.78); g.sc*=0.55+0.45*a; g.op=clamp((t-intro)/0.12);}
    g.cursor=cpath?cpath(t):null;
    if(cfg.geom) g=cfg.geom(t,g)||g;
    g.r=Math.min(g.r,g.h/2,g.w/2);
    world.style.transform=`translate(${(CX-g.s*g.fx).toFixed(3)}px,${(CY-g.s*g.fy).toFixed(3)}px) scale(${g.s.toFixed(5)})`;
    const st=shape.style;
    st.left=(g.cx-g.w/2).toFixed(3)+'px'; st.top=(g.cy-g.h/2).toFixed(3)+'px';
    st.width=g.w.toFixed(3)+'px'; st.height=g.h.toFixed(3)+'px'; st.borderRadius=g.r.toFixed(3)+'px';
    st.background=g.bg; st.transform=`scale(${g.sc.toFixed(5)})`; st.opacity=g.op.toFixed(4);
    for(const L of layers){
      const v=M.vis(t,L.tin,L.tout,{din:0.07,lin:0.26,lout:0.12,...(L.o||{})});
      if(M.apply(L.node,v)){
        const an=L.anchor||'c';
        L.node.style.left=(an==='l'?0:g.w/2).toFixed(3)+'px';
        L.node.style.top=(an==='t'?0:g.h/2).toFixed(3)+'px';
        if(L.update) L.update(t,g,v);
      }
    }
    if(cfg.extra) cfg.extra(t,g);
    if(cpath&&cur){
      const c=g.cursor, sx=CX+g.s*(c.x-g.fx), sy=CY+g.s*(c.y-g.fy);
      cur.style.transform=`translate(${(sx-3).toFixed(2)}px,${(sy-3).toFixed(2)}px) scale(${(1-0.13*cpress(t)).toFixed(4)})`;
    }
  }});
};
M.scene = M.morph;   // alias: motion-broll fragments run unchanged
})();
