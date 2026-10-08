# Engine API (`engine/motion.js`, global `M`)

## Fragment format

A fragment is one HTML file in `video/src/`. `build.py` inlines engine, fonts and VO timings into `video/dist/<name>.html`.

```html
<title>My film</title>
<style> /* your CSS; base.css already gives .a .fill .center .row .col .mono .anton .hand .serif .glass .rim .grad .skel .orbs .vignette */ </style>

<div class="fill" id="world"> …all markup that goes inside #stage… </div>
<div class="vignette"></div>

<script>
// 1) setup (runs once): split text, build lists, compute times from the VO, declare sound cues
// 2) M.video({W, H, T, bg, draw(t){…}})   — draw sets styles from t only
</script>
<script type="module"> /* optional Three.js: import * as THREE from 'three' */ </script>
```

Rules: everything visual comes from `t`; no CSS transitions/animations, timers, `Math.random`, `Date`; read nothing from the previous frame. Hidden things: `M.apply(el, M.vis(...))` (sets visibility) or `el.style.opacity`.

Build: `python build.py src/video.html dist/video.html --vo audio/timings.json --audio audio/vo.wav`. Without `--vo`, `M.VO` is empty: use literal times.

## Timing from the voice
| Call | Returns |
|---|---|
| `M.VO` | `{duration, lines:[{id,text,start,end,words:[{w,start,end}]}]}` |
| `M.line(id)` | the line (`.start`, `.end`) — throws if missing |
| `M.word(id, n \| 'text', 'start'\|'end')` | time a word is spoken (index from 0, negative from end, or text match) |
| `M.words$(id)` | all word start times of a line (feed to `M.words`) |

Typical: scene in = `M.line('x').start - 0.12`; hero lands on `M.word('x','key')`; `T = M.VO.duration + 1.5`.

## Runner
| Call | What |
|---|---|
| `M.video({W,H,T,bg,draw})` | sizes stage, sets `window.seek/DURATION`, preview player. `bg:null` = transparent (render to `.mov`) |
| `M.morph(cfg)` (= `M.scene`) | one-shape UI morph scene (`SH` states, `SEQ`, `layers`, `cursor`, `geom`, `extra`; see `templates/ui-morph.html`). Needs `<div id="world"><div id="shape">…</div></div><div id="cursor"></div>`. Fragments from the separate motion-broll skill (`data-slot` format) also build unchanged, if you have it |
| `M.AR` | `'9x16'`/`'1x1'`/`'16x9'`/`''` from `?ar=`; pass `--ar` to stills/render and lay out from it |
| `M.RENDER` | true while rendering |

Aspect ratios: decide `W,H` from `M.AR`; add a class to `#stage` (e.g. `vertical`) and restyle in CSS; or scale content blocks. Render each: `render.js page.html out/v-9x16.mp4 --ar 9x16`.

## Motion math
| Call | What |
|---|---|
| `M.sp(t,t0,[ω,ζ])` | one spring 0→1 started at t0. Presets: `M.MORPH [15,.84]`, `M.FAST [27,.86]`, `M.SLOW [12.5,.9]`, `M.SOFT [10,.95]`, `M.CAM [7.5,1]`, `M.POP [22,.62]` (visible overshoot), `M.INSTANT` |
| `M.track(v0,[[t,v,spring?],…])` | value with many targets (sum of springs). `M.ctrack('#hex',[[t,'#hex']])` for colour |
| `M.step(v0,[[t,v]])` | hard switch |
| `M.eo M.eo5 M.ei M.eio M.expo M.back` | easings on 0..1 (clamped) |
| `M.win(t,a,b)` / `M.map(x,a,b,c,d)` / `M.clamp` / `M.lerp` / `M.mix('#a','#b',u)` | helpers |
| `M.rand(seed)` → `()=>0..1`, `M.noise(x)` smooth −1..1, `M.shake(t,t0,amp,dur)` → `[dx,dy]` | deterministic randomness |

## Visibility & content
| Call | What |
|---|---|
| `M.vis(t,tin,tout,{din,lin,lout,blur})` | enter/exit with blur → `{o,blur,s,on}` |
| `M.apply(el,v,extraTransform)` | applies a vis (opacity, blur, scale) |
| `M.setText(el,s)` | cheap text update |
| `M.flyOut(t,t0,dur,{scale,blur})` | fly-through exit → `{s,blur,o}` |
| `M.focus(t,t0,dur)` | 1→0 blur factor (rack focus in) |
| `M.smear(p,'x'\|'y')` | `{tf,f}` stretch+blur for a fast move at progress p |

## Type
| Call | What |
|---|---|
| `M.split(el,'words'\|'chars')` | once at setup → spans (keeps inner text only; wrap gradient words in their own element and split it separately) |
| `M.words(spans,t,times,{style,step,spring,dist})` | entrance per span. `times` = start number (+`step`) or array (VO word times). Styles: `rise` `drop` `blur` `scale` `slam` `mask` |
| `M.scramble(spans,t,t0,dur,spread,seed)` | letters fly in from random offsets and assemble |
| `M.stretch(spans,t,t0,from,to,gap)` | per-char width stretch wave |
| `M.cycle(words,t,t0,per)` | rolling word slot → `{word,o,blur,y}` |
| `M.typed(text,t,t0,cps)` + `M.caret(t)` | typewriter |
| `M.count(t,t0,dur,from,to,fmt)` | counting number string |
| `M.gradInit(el,[stops])` + `M.gradText(el,t,speed)` | gradient text with sweep |
| `M.fit(el,maxW)` | shrink font to fit (setup) |

## Shapes, effects, camera
| Call | What |
|---|---|
| `M.stroke(pathEl,t,t0,dur)` | draw an SVG stroke on |
| `M.stagger(n,t,t0,gap,spring)` | array of n spring values |
| `M.ripple(t,t0,n,gap,dur,maxS)` | rings `[{s,o}]` |
| `M.burst(t,t0,n,{colors,speed,gravity,life,seed})` | confetti particles `[{x,y,r,o,c,s}]` |
| `M.orbsInit(box,[{c,x,y,r,blur,o}])` + `M.orbs(list,t,W,H)` | drifting blurred background orbs |
| `M.pulse(t,period,lo,hi)` | breathing value for glows |
| `M.sweep(t,t0,dur)` | 0..1 scan-line progress |
| `M.along(path,n,t,t0,{dur,gap,ease})` | fly n items along an SVG path (element or `'M…'` string), staggered → `[{x,y,angle,p,s,o,landed,t}]` with a small landing overshoot in `s`. Use for files/orders/chips flying from a form into a folder, database → storage, etc. |
| `M.arc(t,t0,dur,p0,p1,bend)` | curved A→B move with adjustable bend (px, sign flips the side) → `{x,y,e}` |
| `M.xblur(el,amt,'x'\|'y')` | directional motion blur (SVG filter) for fast horizontal/vertical moves; `M.smear` blurs both axes |
| `M.flash(t,t0,dur)` | 0→1→0 flash opacity (white-flash transition; swap scenes at the peak `t0+dur/2`) |
| `M.cam(worldEl,W,H,x,y,scale,rotDeg)` | 2D camera: world point (x,y) at screen centre |
| `M.tilt(rx,ry,z,persp)` | CSS 2.5D transform string |
| `M.path([[t,x,y],…])` | eased point path with human arc (cursor, flying objects) |
| `M.presses(clicks,drags)` | 0..1 press amount for cursor scale |
| `M.CURSOR` | arrow cursor SVG markup |
| `M.icon(name,size,color,stroke)` | Lucide-style icons: arrow check x plus folder terminal file pencil clock sparkle search bolt shield user chart mail bell lock globe moon sun play heart code cart |

## Sound cues
`M.cue(t, name, {g, pan, d, pitch, exact})` at setup (not in draw). Names: `python scripts/sfx.py list`. Exported by `render.js` to `<out>.cues.json`; `stills.js --cues` shows the frames right after each cue.

## Three.js
```html
<script type="module">
import * as THREE from 'three';
const r = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
r.setSize(1920,1080); M.$('gl').appendChild(r.domElement);
const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(40, 16/9, 0.1, 100);
// …build scene once…
M.video({W:1920,H:1080,T:10,bg:'#05060a',draw:t=>{ /* move objects/camera from t */ r.render(scene,cam); }});
</script>
```
Setup with `--three`; build copies `three.module.min.js` (and `three/addons/` if imported) next to the page; preview through `server.js`. See `templates/three-scene.html`.

## Tools
| Command | What |
|---|---|
| `node engine/server.js dist [port]` | preview server (modules, audio) |
| `node engine/stills.js page out.png [times…] [--every s] [--cues] [--ar] [--keep]` | contact sheet with time labels |
| `node engine/render.js page out.mp4 [--fps 60] [--sub 4] [--workers 4] [--ar] [--from --to] [--crf 16]` | frames → video (+ cues.json) |
| `python scripts/voice.py script.json audio/ [--provider] [--voice] [--list]` | VO + timings |
| `python scripts/sfx.py mix cues.json mix.wav --vo vo.wav` / `list` / `audition dir` | sound |
| `python scripts/mux.py video.mp4 mix.wav final.mp4` | mux + −14 LUFS master |
