# Pro techniques: how professional launch, demo and explainer videos are built

Distilled from frame-by-frame study of 7 professional videos (Numtera and LangEase SaaS launch ads, Teamble product demo, Google "Introducing Vids", Google "What's New in Search", Gemini Canvas intro, a WooCommerce plugin vertical reel) plus 280 Opus 5.5 code-made videos. Each technique ends with how to build it with this engine.

## Contents
1. The 12 rules every pro video followed
2. Story structures that worked
3. Typography
4. Transitions (how they avoid cuts)
5. Camera
6. Showing a product UI (demo technique)
7. Backgrounds and looks
8. Vertical / social specifics
9. Technique cookbook (code)

---

## 1. The 12 rules every pro video followed

1. **One idea on screen at a time**, 2-6 s each. Never two messages competing.
2. **Continuous motion beats cuts.** 0-27 hard cuts in ~90 s. Within a chapter, the hero element of scene N *becomes* the hero of scene N+1 (morph, zoom-through, shared shape). Hard cuts are reserved for chapter changes, usually with a dark↔light flip.
3. **Text is small and confident or huge and alone**: 28-56 px sentences, or one 110-300 px word alone. Never medium text walls.
4. **The key word is coloured** (accent or gradient), the rest stays neutral. One highlighted word per line.
5. **Words enter one by one with blur + small rise** (8 px blur → 0, 10-20 px rise, ~0.35-0.45 s each, 0.06-0.12 s stagger). Exits are faster (0.2-0.3 s) and blur out or fly through the camera.
6. **UI is redrawn, never a raw screenshot**: clean cards, 10-15 words of real text, skeleton bars for the rest, big type (×1.3 for legibility).
7. **Show the full UI once, tilted, for context; then crop-zoom into the one component that matters.**
8. **A cursor does one action per step**, on a curved path, small press scale, and the target reacts instantly.
9. **Every workflow is a 3-5 step morph chain**: button → loading → result → detail → check.
10. **Close each flow with a check / success beat**, then move on.
11. **Springs with small overshoot (≤4%)**, settle 0.5-0.9 s. 2.5D tilt planes settle flat.
12. **End card holds 3-6 s**: logo + one-line tagline + URL/CTA pill.

## 2. Story structures that worked

**SaaS launch ad (30-95 s)** — Numtera, LangEase:
hook (typed pain question, 0-8 s) → "Stop X" → big "Meet [logo]" → one-line positioning → 3-5 feature beats (UI) → contrast line ("They close tickets. We eliminate them.") → logo → typed CTA.

**Product demo (60-100 s)** — Teamble:
dark brand intro (logo, typed "Introducing …") → light kinetic headline promise → chapters, each: caption line → tilted UI → crop to component → cursor action → result morph → check. Chapters alternate dark/light. Before/after cards + score counter for proof. Logo + tagline.

**Tutorial / feature walkthrough** — Google Vids:
a first-person typed caption ("Let's choose a style") with the last word in blue → zoomed UI crop → one cursor action → result plays → next caption. Full editor shown once for orientation. Kinetic list of use cases at the end ("event recaps / project updates / milestones").

**Feature-update explainer** — Google Search:
each feature = prompt typed into a hero pill → UI demo → one huge kinetic word card as palette cleanser ("Search", "Visualize it", "& shop for you"). Section bridges: dot tunnel, push-through.

**AI product intro** — Gemini:
alternates short kinetic text beats (≈3 s, small type, keyword blue-violet) with tilted dark UI close-ups (3-6 s) carrying cursor and glow. Bookends with the same opening screen.

**Vertical plugin reel (55 s)** — meme hook (relatable pain, 0-7 s) → reaction beat → dark "The real problem?" + counter → HARD CUT to light → logo + promise → one-click demo → how it works flow → benefit chips → meme payoff (same mock, now fast) → logo burst + CTA pill + URL.

Pacing everywhere: **one idea per 2-6 s**; kinetic word cards 0.8-1.5 s.

## 3. Typography

- **Family**: geometric/neo-grotesk sans (Inter, Satoshi, Google Sans, Geist). Weights 400-500 for sentences, 600-800 for heroes. Tracking −0.02 to −0.035 em on big type. Sentence case. Bundled here: Geist (use it), Anton (condensed slams), Instrument Serif (editorial contrast), Caveat (hand notes), Geist Mono (code/labels).
- **Sizes at 1080p**: hero word 110-300 px; headline 64-110 px; sentence 44-56 px; UI text 28-36 px; labels ≥18 px (≥22 px for 9:16).
- **Highlight treatments**: accent-coloured key word; gradient key word (`#3B82F6→#60C5F0`, `#ff3d8b→#b24dff`, `#4285F4→#A78BFA`); selection-box highlight (blue box, white text); brackets `{learning}` / `[Reusable knowledge]` that collapse on exit; inline pill inside the sentence that morphs ("9x better" → "2x → 3x → 4x").
- **Entrances**: word blur-rise (default); typewriter + caret for prompts and hooks (14-18 cps, 20 for streaming text; last 2-3 chars tinted/blurred); char rise for hero words (0.05 s stagger); letter scramble that assembles (≈0.8 s); rolling word slot ("Meet your [designer/editor/storyteller]"); mask reveal; slam with slight rotation (−15°) + shake for emphasis.
- **Exits**: blur-fade 0.2-0.3 s; **fly-through** (scale 1→1.6 + blur 30 px in 0.3 s, ease-in); horizontal smear.
- **Holds**: 0.8-1.5 s for word cards, 1.5-3 s for sentences, ≥3 s end card.
- **Layout**: centred, one line ≤45 chars; two-line headline where line 2 is the highlight and starts 0.5 s after line 1.

## 4. Transitions (how they avoid cuts)

| Transition | What happens | Build |
|---|---|---|
| **Morph chain** | One shape changes size/radius/colour: folder → panel → phone → ribbon → progress bar → circle → check → tile → card | `M.morph` states, or one div with `M.track` on w/h/r/bg |
| **Zoom-through** | Camera pushes ~6-8× into a screen/element; the next scene is inside it | `M.cam` scale track + crossfade next scene at ~70% of the push + `whoosh`/`suck` |
| **Fly-through exit** | Text rushes past camera while next scene focuses in | `M.flyOut` + `M.focus` |
| **Cross-blur** | Outgoing blurs+fades, incoming un-blurs, 0.3-0.5 s overlap | `M.vis` with overlapping tin/tout |
| **Blob wipe** | Giant gradient ellipses sweep across, swap at midpoint | big blurred divs translated by `M.eio`, swap at 0.5 |
| **Smear** | Fast-moving element stretches + blurs along motion | `M.smear(p)` |
| **Shared constants** | Same background, glow colour, tilt and pill shape persist across scenes | design system, not code |
| **Hard cut + flip** | Chapter change: dark problem → light solution, with impact | cut on a word + `impact` cue |
| **Bridge** | Dot tunnel / hyperspace between sections | Three.js points or CSS dots scaled by z |

## 5. Camera

All 2.5D: UI planes tilted `rotateX 8-50°, rotateY −20…−30°` that drift slowly (`ry = −24 + 3·sin(0.5t)`) and settle flat on spring (ω≈8, ζ≈0.8); slow push-in 3-12% per beat; **crop-zoom** 2-4× onto the control being used, then back out with defocus; two planes at different depths for parallax; **rack focus**: non-focal layers blur 6-12 px, focus shifts on the click.

## 6. Showing a product UI (demo technique)

1. Rebuild UI in HTML as simplified cards (real labels, skeleton lines for filler, real brand radius/colour). Make text 1.3× larger than the real app.
2. Context shot: whole dashboard once, tilted and dimmed. Then crop into one strip that fills the frame.
3. Cursor: curved path (`M.path`), slight undershoot, press scale 0.85-0.9 for 0.12 s, `click` cue; target reacts the same frame (highlight, grow, state change).
4. Flow = morph chain: "Help me craft feedback" button → "Generating…" pill with shimmer → typed result → score card → detail panel → ✓.
5. Proof: before/after stacked cards with score badges; counters (`M.count`) with colour lerp at thresholds; progress bars bound to counters.
6. AI actions: dark console card, typed/streamed text, scan line (`M.sweep`).
7. People/integrations: avatar circles orbiting a centre node (`angle = a0 + 0.4t`); chat/response cards stagger in from edges at different sizes/depths, some blurred.
8. Flow diagrams: line draws (`M.stroke`), node travels along it, destination cards pop.
9. Callouts: hand-written note (Caveat) + drawn arrow (`M.stroke`) pointing at the thing.

## 7. Backgrounds and looks

- **Light airy**: `#F4F2FF`/`#F6F6FD`/`#FAFBFE` with 2-3 big blurred pastel orbs (violet `#B9A6FF`, sky `#A8DCF5`, pink) drifting slowly → `M.orbsInit` + `M.orbs`.
- **Dark premium**: `#0a0714`-`#0d0e12`, one coloured bloom (violet/indigo/red) in a corner, vignette.
- **Rising gradient**: white → sky `#6EC1FF` → azure `#1E90FF` → royal `#1B3FE0` from bottom edge (Numtera).
- **Glass cards**: white 70-80% + backdrop blur + 1 px white border + soft blue shadow, radius 16-28 → `.glass`.
- **Neon rim (AI)**: dark surface + 2 px gradient border blue→violet + outer halo → `.rim` (`--rim1`, `--rim2`, `--glow`).
- **Gradient text**: `.grad` + `M.gradInit` + `M.gradText` sweep.
- Dark ↔ light alternation marks chapters (problem vs solution).

## 8. Vertical / social specifics (9:16)

Headline in top 20%, hero mid, chips/CTA lower third, **bottom 12% empty** (platform UI). Headlines ≥64 px, nothing under 22 px. On-screen text carries the message (sound-off viewing) even with VO. Hook in first 2 s (meme/relatable pain/bold question). One idea per 3-5 s. End card ≥4 s with CTA pill + URL.

## 9. Technique cookbook (code)

```js
// word blur-rise with gradient key word
const sp = M.split(M.$('h'));                     // <div id="h">Turn books into <span class="grad" id="kw">audio</span></div> → split after gradInit
M.words(sp, t, M.words$('hook'), {style:'blur'}); // times = real VO word times

// fly-through exit at tOut
const f = M.flyOut(t, tOut); el.style.transform = `scale(${f.s})`; el.style.filter = `blur(${f.blur}px)`; el.style.opacity = f.o;

// tilt-in UI plane that settles flat + push
const k = M.sp(t, t0, [8, 0.8]);
panel.style.transform = M.tilt(50*(1-k), -24*(1-k)) + ` scale(${0.9+0.1*k + 0.03*M.eio((t-t0)/4)})`;

// crop-zoom into a component (world coords) and back
const zs = M.track(1, [[tZoom, 2.6, M.CAM], [tBack, 1, M.CAM]]), zx = M.track(960, [[tZoom, 1320, M.CAM], [tBack, 960, M.CAM]]);
M.cam(world, W, H, zx(t), 540, zs(t));

// cursor: curved path + press, click cue at tc
const cur = M.path([[t0, 1500, 900], [tc-0.05, 820, 610]]), pr = M.presses([tc]); M.cue(tc, 'click');
const c = cur(t); cursor.style.transform = `translate(${c.x}px,${c.y}px) scale(${1-0.13*pr(t)})`;

// morph chain on one element: button → loading pill → check circle
const w = M.track(360, [[t1, 220], [t2, 96]]), r = M.track(18, [[t1, 40], [t2, 48]]), bg = M.ctrack('#1A5BD6', [[t2, '#22C55E']]);

// rolling word slot
const cy = M.cycle(['designer','editor','storyteller'], t, t0, 0.8);
M.setText(slot, cy.word); slot.style.opacity = cy.o; slot.style.filter = `blur(${cy.blur}px)`; slot.style.translate = `0 ${cy.y}px`;

// counter + bar + colour threshold
M.setText(num, M.count(t, t0, 1.2, 10, 92)); bar.style.width = (92*M.expo((t-t0)/1.2))+'%';

// ripple rings behind a pill, check pop, confetti
M.ripple(t, t0).forEach((g,i)=>{ rings[i].style.transform=`scale(${g.s})`; rings[i].style.opacity=g.o; });
M.burst(t, t0, 40).forEach((p,i)=>{ const e=dots[i]; e.style.transform=`translate(${p.x}px,${p.y}px) rotate(${p.r}deg) scale(${p.s})`; e.style.opacity=p.o; e.style.background=p.c; });

// files flying from a form into a folder along a drawn connector (submission → storage), with landing ticks
const ps = M.along(M.$('route'), 6, t, tSend, {dur:0.7, gap:0.18});                 // <path id="route" d="M560 540 C 820 260, 1120 260, 1360 520"/>
ps.forEach((p,i)=>{ chips[i].style.transform=`translate(${p.x}px,${p.y}px) rotate(${p.landed?0:p.angle*0.15}deg) scale(${p.s})`; M.xblur(chips[i], p.landed?0:10*Math.sin(Math.PI*p.p)); });
M.setText(count, String(ps.filter(p=>p.landed).length));                           // setup: M.cue(tSend+i*0.18,'swish') and M.cue(tSend+i*0.18+0.7,'tick')

// white-flash scene swap
flash.style.opacity = M.flash(t, tCut-0.09, 0.18);  sceneA.style.visibility = t < tCut ? '' : 'hidden';

// ambient orbs
const orbs = M.orbsInit(M.$('bg'), [{c:'#B9A6FF',x:.15,y:.2,r:900},{c:'#A8DCF5',x:.85,y:.85,r:1000}]);  // setup
M.orbs(orbs, t, W, H);                                                                                   // draw
```
