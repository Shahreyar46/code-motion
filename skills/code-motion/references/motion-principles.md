# Motion Principles Reference (for t-pure HTML/JS motion graphics)

> Numbers combine published design-system specs (Material 3 and IBM Carbon easing/duration tokens, Apple HIG) with practitioner guidelines for motion design and editing. Treat durations, pacing curves and safe margins as strong defaults to adjust by eye on the contact sheets, not as laws.

Every frame = pure function of t. All rules below are expressed so they can be implemented as `f(t)` with engine `M`.
Settle formula: `settle ≈ 4/(zeta*omega)` s. Spring presets: MORPH [15,.84], FAST [27,.86], SLOW [12.5,.9], SOFT [10,.95], CAM [7.5,1], POP [22,.62].

## Table of contents
1. The 12 principles applied
2. Timing and easing standards
3. Choreography
4. Kinetic typography
5. Composition and framing
6. Editing theory for motion pieces
7. Color and light in motion
8. Sound-picture sync
9. Common amateur mistakes (25)
10. Senior review checklist

---

## 1. The 12 principles applied

| # | Principle | Rule | Numeric guideline | Implement |
|---|---|---|---|---|
| 1 | Squash and stretch | Convey speed/impact by deforming along motion axis, preserving area. | Stretch scaleX 1.0 to 1.08-1.25 at peak velocity, scaleY = 1/scaleX. Squash on impact 0.88-0.94 for 60-100ms. UI: max 6%; playful: up to 25%. | `M.smear(p)` for velocity stretch; spring POP for squash recovery. Derive stretch from `abs(dx/dt)`, not time. |
| 2 | Anticipation | Small counter-move before a big move. Telegraphs the action. | Wind-up = 8-15% of travel opposite direction, 80-150ms, then main move. Skip for tiny UI moves (<150ms). | `M.track(0,[[t0,-0.1,FAST],[t0+0.12,1,MORPH]])` |
| 3 | Staging | One clear idea per moment; viewer eye goes to the one thing. | Max 1 primary mover + 2 supporting. Dim non-focus to 35-50% opacity or blur 4-8px. | `M.focus`, `M.vis(...,{blur})` on background elements. |
| 4 | Straight-ahead / pose-to-pose | In code: define key poses (poses) and let springs/eases interpolate. | Keyposes every 0.4-1.2s; never more than 3 properties animated independently without a shared timing. | `M.track` per property with shared keyframe times. |
| 5 | Follow-through and overlapping action | Children/secondary parts lag the parent and settle later. | Lag 40-120ms per layer (typically 3-6 frames at 60fps). Overshoot of followers 1.5x leader. Settle 150-300ms after main stop. | Same spring, `t0 + i*0.06`. Lighter elements use lower omega (CAM/SOFT). |
| 6 | Slow in / slow out | Never linear for position/scale/opacity of objects (linear OK for rotation loops, progress bars, color cycles, scrolling tickers). | Entrances: decelerate (ease-out). Exits: accelerate (ease-in). Start/end velocity 0 only for A-to-B moves. | `M.eo` enter, `M.ei` exit, `M.eio` A-to-B, `M.expo` for dramatic. |
| 7 | Arcs | Natural motion is curved. Straight lines read mechanical. | Curve deviation 8-20% of path length for mid-range moves; use a perpendicular control offset. Cursor paths always arc. | `M.path` with a control point; never lerp x and y with the same easing for a travelling object, give y a slightly different spring (omega x0.85). |
| 8 | Secondary action | Add small supporting motion that does not compete. | Amplitude <= 20% of primary; starts after primary peak; duration <= primary. E.g. icon glow pulse 0.9-1.1 during a card entrance. | Add a second `M.track` offset 100-200ms later. |
| 9 | Timing | Duration communicates weight, size and importance. | See section 2. Rule: heavier/larger = longer and slower. 2 frames=snappy hit; 12 frames=normal; 24+=majestic (at 24fps scale). | Pick omega by size; settle=4/(zeta*omega). |
| 10 | Exaggeration | Push 20-30% beyond realistic for clarity, then taper. | Hero moments: overshoot 8-15%. Everything else: 0-5%. Only 1 exaggerated element per beat. | Spring POP for hero, MORPH/FAST for rest. |
| 11 | Solid drawing / depth | Give objects volume with consistent light, shadow, perspective. | Shadow offset follows one light (e.g. 0, +y). Blur radius grows with z-height (elevation 8px = blur 16-24px, 10-18% alpha). Perspective 800-1400px; tilt max 8-14deg for UI cards. | `M.tilt(rx,ry)`, `M.cam` with scale parallax. |
| 12 | Appeal | Clear silhouette, consistent corner radius, limited palette, rhythmic motion. | Radius family (e.g. 8/16/24); 1 accent + 1-2 neutrals; same easing family across a piece. | Constants block at top: RADII, COLORS, SPRING presets. |

Rule of consistency: pick 2 spring presets (one for enter, one for hero) and 1 exit ease for the whole video; deviate only on purpose.

Further reading:
https://www.interaction-design.org/literature/article/the-12-principles-of-animation
https://m3.material.io/styles/motion/overview/how-it-works
https://www.schoolofmotion.com/blog/12-principles-of-animation

---

## 2. Timing and easing standards

### 2.1 Duration by element (UI scale, 1080p video can go 1.3-2x slower than live UI because viewers cannot interact)

| Element / distance | Live UI (ms) | Video (ms) | Notes |
|---|---|---|---|
| Micro (icon swap, toggle, ripple, color) | 100-150 | 150-250 | |
| Small (button, chip, tooltip, cursor click) | 150-250 | 250-400 | |
| Medium (card, list item, menu) | 200-300 | 350-600 | |
| Large (panel, modal, full-width card) | 250-400 | 500-800 | |
| Full-screen / scene transition | 300-500 | 600-1000 | |
| Camera move (push/pan) | n/a | 1200-3000 | Slow, CAM spring |
| Hero reveal (logo, title) | n/a | 800-1400 | |

Scale with distance: `dur ≈ 150ms + 0.25 ms per px` capped at 800ms (video). Travel < 40px: do not exceed 250ms.
Material 3 durations: short1-4 = 50/100/150/200ms; medium1-4 = 250/300/350/400ms; long1-4 = 450/500/550/600ms; extra-long1-4 = 700/800/900/1000ms.
Nothing in a product video should run > 1.4s for a single move except camera and ambient loops.

### 2.2 Enter vs exit asymmetry
- Exit = 60-75% of enter duration (e.g. enter 500ms, exit 300ms). Leaving elements must get out of the way.
- Enter: decelerate (arrives soft). Exit: accelerate (leaves fast). Never decelerate an exit.
- Exits: move less distance (24-40px) and fade; entrances travel 40-120px.
- Elements being replaced: outgoing finishes ~40% before incoming settles (overlap 30-50%, not sequential waiting).
- Fade: opacity enter completes in first 50-60% of the move duration; exit fade in last 50%.

### 2.3 Standard curves (cubic-bezier)

| Name | Source | Value | Use |
|---|---|---|---|
| Standard | Material 3 (legacy) | (0.2, 0, 0, 1) | on-screen A to B |
| Emphasized (legacy single) | M3 | (0.2, 0, 0, 1) | hero moves |
| Emphasized decelerate | M3 | (0.05, 0.7, 0.1, 1) | enter |
| Emphasized accelerate | M3 | (0.3, 0, 0.8, 0.15) | exit |
| Standard decelerate | M3 | (0, 0, 0, 1) | small enter |
| Standard accelerate | M3 | (0.3, 0, 1, 1) | small exit |
| Legacy Material standard | M2 | (0.4, 0, 0.2, 1) | fallback |
| Legacy decelerate | M2 | (0, 0, 0.2, 1) | enter |
| Legacy accelerate | M2 | (0.4, 0, 1, 1) | exit |
| Carbon productive standard | IBM | (0.2, 0, 0.38, 0.9) | small, functional |
| Carbon productive entrance | IBM | (0, 0, 0.38, 0.9) | |
| Carbon productive exit | IBM | (0.2, 0, 1, 0.9) | |
| Carbon expressive standard | IBM | (0.4, 0.14, 0.3, 1) | large, showy |
| Carbon expressive entrance | IBM | (0, 0, 0.3, 1) | |
| Carbon expressive exit | IBM | (0.4, 0.14, 1, 1) | |
| Apple-style ease-out | common | (0.25, 0.1, 0.25, 1) / (0.16, 1, 0.3, 1) expoOut | keynote smooth |
| easeOutBack | common | (0.34, 1.56, 0.64, 1) | ~10% overshoot, cartoony if overused |

Mapping to engine: `M.eo` (enter/decelerate), `M.ei` (exit/accelerate), `M.eio` (move A to B), `M.expo` (keynote glide, long deceleration, 0.8-1.4s), `M.back` (overshoot pop, use <= 2 per scene).
Carbon rule: productive (150-240ms-ish) for utility, expressive (400-700ms) for brand moments; video leans expressive.
Never use CSS default `ease` or `linear` for object motion.

### 2.4 When springs beat beziers
Use springs when: motion is interruptible or retargeted mid-flight (`M.track` handing off between targets), when a physical feel/overshoot is wanted, for camera, drag/release, pop-in, morphs. Use beziers/eases when: exact duration needed to land on a beat, opacity/color fades, wipes, masks, progress. In t-pure code both are deterministic; springs just need `t0`.
Opacity and color: ease only (springs overshoot clamp to [0,1] incorrectly). Clamp opacity.

### 2.5 Spring parameters (omega = natural frequency rad/s, zeta = damping ratio)
- omega 7-12: slow, heavy (camera, large panels). 12-18: medium, UI. 18-30: snappy, small elements.
- zeta 1.0: no overshoot (critically damped; CAM). 0.9-0.95: ~0-1% overshoot (SOFT/SLOW). 0.84-0.86: ~0.5-0.8% (barely visible, premium: MORPH/FAST). 0.7: ~4.6%. 0.62: ~8% (POP). 0.5: ~16%. 0.3: ~37% (cartoony, ringing).
- Overshoot % = `exp(-pi*zeta/sqrt(1-zeta^2))*100`.
- Premium feel: overshoot 0-5% for UI, 5-10% for one hero pop, never > 12% except playful brands. Cartoony: > 15% or visible ringing (more than 2 oscillations).
- Settle time = 4/(zeta*omega): omega 27/zeta .86 -> 0.17s; 15/.84 -> 0.32s; 12.5/.9 -> 0.36s; 10/.95 -> 0.42s; 7.5/1 -> 0.53s; 22/.62 -> 0.29s (with ringing).
  Note: perceived end ~ settle time; start of motion at t0 is felt immediately, so anchor sound cues at t0 (+0-2 frames).
- Scale spring: start at 0.92-0.96 (not 0) for UI cards; start at 0.6-0.8 only for POP.
- Rotation springs: omega lower (x0.6) than position.

Further reading:
https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
https://carbondesignsystem.com/elements/motion/overview/
https://developer.apple.com/design/human-interface-guidelines/motion
https://developer.apple.com/videos/play/wwdc2023/10158/
https://easings.net

---

## 3. Choreography

### 3.1 Hierarchy of motion
- One primary move at a time. Primary = the thing that carries the story; viewer should be able to say what moved. Everything else: supporting at <= 50% of primary amplitude or static.
- Order of attention: (1) largest/fastest, (2) first to move, (3) highest contrast. Make them the same element.
- Do not start a new primary until the previous is 80-90% settled (within 5% of target), unless it is deliberate overlap (hand-off).
- Ambient motion (floating, shimmer) <= 3-6px, 4-8s period, linear-sine; stop or dim it during primary moves.

### 3.2 Stagger rules
- Gap: 40-80ms per item for small items (list rows, chips); 80-150ms for cards; 150-250ms for large panels or words in a hero line.
- Total stagger cascade cap: 400-600ms for UI, <= 900ms for hero. If n*gap exceeds cap, compress: `gap = cap/(n-1)`.
- More than 8 items: group in rows/clusters, stagger groups (100ms) and items within group (30ms).
- Direction: follow reading order (left-to-right, top-to-bottom) or radiate from focal point/click origin. Reverse for exits, with half the gap.
- Use ease-out gap curve (first gaps larger) for dramatic cascade: `t_i = t0 + cap*eo(i/(n-1))`.
- Implement: `M.stagger(n,t,t0,gap)`; words: `M.words(spans,t,times,{style,step})` with step 0.05-0.09s per word (per-letter 0.02-0.035s).

### 3.3 Leading and following
- Leader moves first and farthest; followers delayed 40-100ms with 80-90% of distance and slightly softer spring (omega x0.85).
- Container leads content: container expands first (0-250ms), content fades/slides in during last 60% (starting ~150-200ms) so text is not clipped.
- Shadow/glow follows 1-2 frames behind its object; reflection/highlight sweeps AFTER arrival (200-400ms).
- Cursor leads UI: cursor arrives, 100-160ms dwell, click squash (scale .92 for 80ms), then UI reacts 40-80ms after click frame.

### 3.4 Shared-element / container transform
- Source element morphs into destination: animate position, size, radius, color on one shared timeline (`M.sp` MORPH [15,.84]); duration 400-600ms video.
- Cross-fade content: outgoing content fades out in first 20-30% (0-100ms), incoming fades in from 30-100%. Never both at full opacity (ghosting).
- Interpolate in an arc (x uses eo, y uses slightly slower curve) for a 10-15% path curve.
- Keep the shared element on top (z-index) for entire transition; scrim behind it at 0 to 40-60% black.
- Border radius, shadow, and aspect change simultaneously; fixed text should not scale (swap font-size instead, or crossfade).
- `M.cam` zoom into the shared element is the best container transform for "enter the app" moments: scale 1 -> 2.5-4 over 700-1100ms with CAM spring, then cut/crossfade to next full-screen state.

### 3.5 Continuity of direction
- Screen-direction: in a sequence of transitions, forward progress moves left (content exits left, new enters from right) in LTR logic; do not alternate arbitrarily. Reverse = back/undo.
- Exit direction of scene N = entry direction of scene N+1 (carry momentum). If an object leaves right at velocity v, next enters from left? NO: keep it consistent: left-to-right flow throughout unless story reverses.
- Vertical for hierarchy (up = deeper/new, down = dismiss), horizontal for sequence, z (scale) for drill-in/out.
- Maintain one light direction and one camera direction per scene.
- Match velocity at cut: outgoing motion speed ~ incoming motion speed.

Further reading:
https://m3.material.io/styles/motion/transitions/transition-patterns
https://carbondesignsystem.com/elements/motion/choreography/
https://www.schoolofmotion.com/blog/animation-principles-ui

---

## 4. Kinetic typography

### 4.1 Reading speed and holds
- Comfortable on-screen reading: 3.0 words/sec (180 wpm) for fully read lines; 2.0-2.5 w/s for first-time dense; 4 w/s hard max for short punchy slides.
- Minimum hold (after fully visible): `hold = max(0.8s, 0.3s + words*0.33s)` ≈ words / 3 w/s. 1 word: 0.6-0.8s; 3 words: 1.2-1.5s; 6 words: 2.0-2.5s; 10 words: 3.3-4s; 15+ words: split.
- Total on-screen time = animate-in (0.3-0.6s) + hold + animate-out (0.2-0.35s). Do not count animate-in time as reading time unless the first word is readable within 150ms.
- Numbers/stats: 1.5-2.0s hold (viewer needs recognition + context). Logos: 1.0-1.5s.
- Voiceover pairing: text appears 100-300ms BEFORE the spoken word (eye leads ear), stays through the end of the phrase +300ms.
- Max words per screen: headline 3-7 words (hero 2-4); body line 8-12 words; never > 2 lines of body in a 16:9 promo.
- Reduce when audience watches muted/mobile: hold x1.25.

### 4.2 Line length and layout
- 16:9: headline line 12-28 chars (<= 40 max); body 35-55 chars. 9:16: headline 8-16 chars per line; body 20-32 chars.
- Max 3 lines for headlines; balance lines (no single-word orphan on last line unless intentional).
- Line height: display 0.95-1.1; headline 1.1-1.2; body 1.3-1.5. Letter-spacing: display -1% to -3%; ALL CAPS +4% to +10%; small text +0 to +2%.
- Alignment: left-aligned for multiline (center only for 1-2 lines/hero).

### 4.3 Size hierarchy
- Ratio 1.5-2.5x between levels: hero 96-160px, headline 64-96px, subhead 36-48px, body 28-36px, caption >= 24px at 1080p. Minimum text anywhere: 24px at 1080p (2.2% of height); 9:16 1080x1920: >= 36px.
- Max 3 sizes and 2 weights per scene (e.g. 700/500). One font family, 2 at most.
- Hero word can be 2-3x its neighbors for emphasis; keep baseline aligned.
- Weight contrast beats size contrast for subtlety: 300 vs 800.

### 4.4 Emphasis techniques
- Scale pop 1.0 -> 1.08-1.15 -> 1.0 (POP, 300ms).
- Color switch to accent for 1-2 key words only (<= 15% of words on screen).
- Weight/underline sweep: stroke draws left to right 300-450ms (expo).
- Highlight bar behind word (mask wipe 250ms, 20-35% opacity accent).
- Hold-in-motion: dim everything else to 40% while emphasizing one word.
- Slam: scale 1.6 -> 1 with 4-8px shake 3 frames, plus impact cue (`M.shake`, `M.cue(t,'impact')`).
- Blur-to-sharp: blur 12px -> 0 in 300-450ms (use sparingly, expensive; legibility gone until sharp).

### 4.5 Per letter vs word vs line
| Unit | Use when | Timing | `M.words` style |
|---|---|---|---|
| Per letter | Hero word <= 12 chars, logo/wordmark, mono "typing" | 20-35ms/letter, total <= 600ms | none; build with per-char spans + `M.stagger` |
| Per word | Headlines of 3-10 words, voice-synced | 50-100ms/word (or sync to VO word timings) | 'rise' (default), 'blur', 'scale', 'slam', 'mask' |
| Per line | Body/subhead, 2+ lines | 80-150ms/line | 'drop'/'mask' per line |
| Whole block | Paragraph, legal, UI copy | one fade 250-400ms | `M.vis` |
- Per-letter on sentences = unreadable and slow; ban beyond ~14 characters.
- Style mapping: 'rise' = 24-40px translate up + fade (default, premium); 'drop' = from above (impact, announcement); 'blur' = soft focus (calm/ethereal); 'scale' = 0.85 -> 1 (confident); 'slam' = 1.5 -> 1 with shake (loud); 'mask' = slide up from clipped line (editorial/cinematic, best for headlines).
- Stay consistent: one style per piece plus one accent style for the hero.

### 4.6 Legibility during motion
- Text must be fully readable (opacity 1, blur 0, scale ~1) for its entire hold; anything moving behind text is slower than 40px/s or dimmed.
- Do not move text faster than 1/3 screen width per second while reading is expected. Camera moves while text is up: max scale delta 6%/s.
- No motion blur on text > 4px; no rotation > 3deg on body copy.
- Contrast ratio >= 4.5:1 (body), >= 3:1 (large display >= 48px); over imagery use 40-60% scrim or text shadow (0 2px 24px rgba(0,0,0,.35)).
- Text should not cross or sit on busy edges; place in negative space.

### 4.7 Safe areas
| Format | Action-safe | Title-safe | Social UI (9:16) |
|---|---|---|---|
| 16:9 (1920x1080) | 93% (inset 3.5%: 67px x, 38px y) | 90% (inset 5%: 96px x, 54px y) | n/a |
| 9:16 (1080x1920) | 93% | 90% | Extra: bottom 20-25% (~380-480px) captions/UI, top 10-14% (~190-270px), right 12% (~130px) for like/share rail. Keep key text in center ~ 60% vertical band (y 14% to 75%). |
| 1:1 (1080x1080) | 93% | 90% | |
| 4:5 (1080x1350) | 93% | 90% | bottom 15% overlay risk |
- Hero logos/headlines inside title-safe. Backgrounds and bleed go to edge + 5% overscan margin. Moving-in elements may start outside, but must rest inside.

Further reading:
https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
https://www.schoolofmotion.com/blog/kinetic-typography
https://help.netflix.com/en/node/14664
https://www.ebu.ch/files/live/sites/ebu/files/Publications/EBU-Tech%203276
https://www.nngroup.com/articles/legibility-readability-comprehension/

---

## 5. Composition and framing

- Rule of thirds: place focal point at a third intersection (x=33.3%/66.7%, y=33.3%/66.7%) for imagery; text/hero UI may be dead-center for symmetry/impact. In 9:16, focal point at upper-third line y~35%.
- Visual weight: large + saturated + high contrast + isolated + top-left/centre = heavy. Balance a heavy left element with lighter, smaller on right (weight ratio ~ 60/40). Asymmetry reads dynamic; symmetry reads formal/stable.
- Negative space: 40-60% of the frame empty in hero shots; never fill > 70%. Padding between groups >= 2x padding within groups. Margin from frame >= 8% (title-safe 10%).
- Focal point: exactly one per shot. Test: squint (blur 20px) - one blob should dominate. Give it 3 of: largest, brightest, most saturated, only mover, sharpest.
- Frame composition percentages: hero object 25-45% of frame height; secondary UI 15-25%; background elements <= 10% each; text block <= 30% of area. Product mockup full-bleed zoom: 70-90% of frame.
- Shot scale ladder: wide (UI full, 100%), medium (panel, 50-60%), close (detail, 25-30% of source visible). Alternate scale between consecutive shots by >= 1.5x so cuts read.
- Lead room: object moving right gets 60% empty space on the right; text next to motion goes ahead of the motion.
- Align to a grid: 12-col, 8px base; consistent baseline.

### Camera moves (`M.cam(world,W,H,x,y,scale,rot)`)
| Move | Numbers | Meaning |
|---|---|---|
| Push in (scale up) | 1.0 -> 1.08-1.2 slow over 2-5s; 1.0 -> 2-4 for drill-in over 0.8-1.2s | Focus, intimacy, importance, tension |
| Pull out | 1.5 -> 1.0, 1.2-2s | Reveal context, resolution, "big picture" |
| Pan | 8-25% of frame width over 1.2-3s, ease-in-out CAM | Discovery, relation between items |
| Dolly / tracking (parallax on x with z-layers) | layer speed ratios 1 : 0.6 : 0.3 (fg:mid:bg) | Spatial depth, travel |
| Tilt/roll | rot 1-3deg drift; 5-15deg for stylized; never > 3deg on static UI w/ text | Instability, energy |
| Orbit (3D) | 15-30deg over 2-4s | Product showcase |
| Rack focus | blur bg 0 -> 8px while fg sharp, 400-700ms (`M.focus`) | Shift of attention |
| Handheld shake | 1-3px, 6-12Hz noise, only during impact (`M.shake`) 150-300ms | Impact, energy |
- Camera always eases (CAM [7.5,1], no overshoot). Never ping-pong push/pull within one scene.
- Never camera-move and heavily animate the same elements simultaneously; one moves, other holds (camera is the primary).
- Constant slow drift (push-in 3-5% over scene) on "static" holds prevents dead frames (keeps life; amplitude <= 5%).

### Depth cues
- Overlap (occlusion), size, vertical position, blur (atmospheric 2-6px per layer back), shadow, parallax (see ratios), perspective/tilt via `M.tilt`, desaturation + lower contrast for distance.
- Elevation levels: z0 flat, z1 shadow 0 2px 8px @12%, z2 0 8px 24px @16%, z3 0 24px 64px @22%.

Further reading:
https://www.schoolofmotion.com/blog/composition-in-motion-design
https://www.studiobinder.com/blog/rule-of-thirds-photography-composition/
https://www.studiobinder.com/blog/camera-movements-ultimate-guide/
https://m3.material.io/foundations/layout/understanding-layout/overview

---

## 6. Editing theory for motion pieces

### 6.1 Murch's rule of six (priority and weight)
1. Emotion 51%: does the cut feel right emotionally? Beats all else.
2. Story 23%: does it advance the narrative/message?
3. Rhythm 10%: does it fall at an interesting, "right" moment?
4. Eye trace 7%: does it respect where the viewer looks (focal point continuity)?
5. 2D plane of screen 5%: respects the 180/screen direction.
6. 3D space of action 4%: spatial continuity.
Use: sacrifice 5-6 first (e.g. break direction) before rhythm/emotion. Place next shot's focal point at the same screen position as the previous (eye trace) for invisible cuts, or deliberately 25-40% away for a "jump".

### 6.2 Cutting techniques
- Cut on action: cut during motion (at ~60% through a move, peak velocity) so movement masks the edit. Outgoing move 60% done, incoming move starts at 40% of its path.
- Match cut: same shape/position/scale/color across cut (circle icon becomes sun, dashboard card becomes next screen). Align object center within 3% of frame and scale within 10%.
- Hard cut beats transition when: pace is fast (shots < 1.5s), content is a new idea/topic (not continuation), beat/impact hit, after a hold (to punch), or between unrelated items. Use dissolve/morph/zoom-through only when relating two states (A becomes B) or for time/space passage. Wipe/fancy transitions: 0-1 per piece.
- Transition durations: hard cut 0f; quick dissolve 150-250ms (4-6f); cross-zoom 400-700ms; morph 500-900ms. Anything > 1s feels slow in promos.
- J-cut: audio of shot B starts 0.25-0.5s before picture; L-cut: audio of A continues 0.25-0.5s over B. VO/music usually lead picture: new VO line starts under the last 6-12 frames of the previous scene; whoosh begins 3-8 frames before cut (see 8).
- Cut after the thing is read/understood, not when it finished animating: text hold complete + 4-8 frames, then cut.
- Avoid cut to near-same frame (jump cut with < 15% change in framing/position): either match cut or change scale >= 1.5x.
- Breathing frame: 6-12 frames of "settled" before outgoing action begins on important statements.

### 6.3 Pacing curves (shot length)
Target average shot length (ASL): 2-4s corporate/explainer; 1.2-2.5s hype/launch; 0.5-1.2s montage/climax; 4-8s calm/premium.
| Piece | Structure |
|---|---|
| 30s | Hook 0-3s (1 striking shot, text <= 5 words) ; setup 3-10s (ASL 3s) ; build 10-22s (ASL 2s, accelerating to 1.2) ; payoff/climax 22-27s (0.8-1.5s shots, then hero hold) ; end card 27-30s (hold 2.5-3s logo + CTA) |
| 60s | Hook 0-5s ; problem 5-15s (ASL 3-4s) ; solution intro 15-25s ; feature run 25-48s (ASL 3s alternating wide/close, 3-4 features, ~6-8s each, speed up toward last) ; proof/stat 48-54s ; CTA 54-60s (hold 3-4s) |
- Shape: slow-fast-slow with a ramp (e.g. ASL 3.5 -> 2.5 -> 1.5 -> hold). Final shot is the longest (2-4s) so the CTA is readable.
- Alternate density: one complex scene, one simple/breathing scene. Never > 3 consecutive high-density scenes.
- First 1.5s must contain motion + a legible hook (retention). No logo-only opening > 1s.
- Information density budget per scene: 1 idea, <= 7 words headline + 1 visual.

### 6.4 Rhythm and beat sync
- Choose tempo (BPM): beat period = 60/BPM s. 90-110 BPM calm, 120-128 upbeat promo (beat = 0.47-0.5s), 140+ hype. Bars: 4 beats; scene changes on bar lines (every 2s at 120 BPM), within-scene accents on beats, micro-moves on half-beats (0.25s).
- Snap key keyframe starts (t0) to the beat grid; snap the visual hit (not the start of the spring) to the beat: `t0 = beat - 0.04` (hit/impact feels at peak velocity, ~2-3 frames after start for FAST).
- Stagger gaps align to subdivisions: gap = beat/4 (125ms at 120BPM) or beat/8.
- Do not sync everything; accent only downbeats (1 and 3) and the key moments; leave off-beat for ambience.
- No music: use VO word timing as rhythm grid.

Further reading:
https://en.wikipedia.org/wiki/In_the_Blink_of_an_Eye_(book)
https://www.studiobinder.com/blog/what-is-a-match-cut-in-film/
https://www.studiobinder.com/blog/what-is-a-j-cut-and-l-cut/
https://www.schoolofmotion.com/blog/motion-design-pacing
https://www.premiumbeat.com/blog/the-rule-of-six-walter-murch/

---

## 7. Color and light in motion

- Contrast for legibility: text vs background >= 4.5:1 (body) / 3:1 (>= 48px). Compute in code and clamp; gradients: test the worst stop. During cross-fade the contrast dips (mid-fade ~ 50% alpha) - keep text out of crossfading zones.
- Luminance hierarchy: focal element 1.5-2x luminance contrast vs neighbors. Use luminance (not hue) to guide eye.
- Palette: 60% neutral, 30% secondary/surface, 10% accent. Max 1 accent hue + 1 tint. Accent used only on: current focus, CTA, key number. If accent appears on > 15% of pixels, it stops being accent.
- Saturation: UI/brand accents 65-90% saturation; backgrounds 0-20%; avoid pure #000 / #fff: use #0B0D12-#14161C and #F6F7F9 (reduces halation/banding).
- Dark scenes: bg L* 5-12, surfaces +4-8 L* per elevation, text 92-96% white (not 100%), shadows replaced by borders (1px @ 8-12% white) and subtle glow. Light scenes: bg L* 96-99, shadows on, text #111-#1A1A1A.
- Dark -> light transitions are strong beats: use for "problem -> solution" or "before -> after"; do it with a circular reveal/mask (expo, 600-900ms) from the focal point, or hard cut on beat. Do not flip theme more than twice per 30s.
- Glow/bloom restraint: max 1 glow source per focal element; blur radius 24-80px at 15-35% opacity; additive only on darks; glow intensity pulses +-10-15%, never flicker. Never bloom text (halo kills legibility); if used: 2-4px, <= 20%.
- Gradients: 2-3 stops, hue shift <= 40deg, subtle (delta L* <= 20); animate gradient angle/offset slowly (<= 15deg/s), avoid banding by adding noise/grain 2-4% at 8-bit output.
- Color as transition device: flood a brand color (full-bleed wipe or circle mask expanding 500-800ms) to cover a cut; next scene's bg = that color. Match accent of outgoing last frame to bg of incoming first frame.
- Color temp and mood: warm (accents hue 15-45deg) = human/energetic; cool (200-260deg) = tech/calm; use warm accent against cool bg for complementary pop.
- Color in animation: interpolate in OKLCH/OKLab (not RGB; avoids muddy middle), clamp chroma. Animate color with eases only (300-500ms).
- Grain/vignette: grain 2-4%, vignette 10-20% darken at edges; adds filmic depth; constant (not animated intensity).
- Consistency: light direction constant (top-left or top); one temperature per scene.

Further reading:
https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
https://m3.material.io/styles/color/system/overview
https://bottosson.github.io/posts/oklab/
https://www.schoolofmotion.com/blog/color-theory-motion-design

---

## 8. Sound-picture sync (`M.cue(t,'whoosh'|'pop'|'impact'|...)`)

- Frame accuracy: at 30fps one frame = 33ms; at 60fps = 16.7ms. Audio leading picture by up to ~ -40ms (audio early) is tolerable; audio late > +40ms feels wrong... sync to the frame where the visual hits (contact/arrival peak velocity/click), not where the spring starts.
- Perception: visual-first by <= 80ms is acceptable for large moves; SFX are best aligned on the visual impact frame or 1 frame earlier (1-2 frames, 16-35ms early often feels tighter).
- Anticipatory whoosh: starts 100-250ms BEFORE the move's arrival; peak (tail energy) lands at arrival; for fast move (200ms) whoosh length 250-400ms, begins at t0 - 50ms. For camera pushes: riser 0.6-1.5s ending at the cut.
- Pop/click: triggered at the frame the element reaches 90-100% scale/arrival; <= 120ms duration; low volume (-18 dB below VO).
- Impact/hit: sub + transient at the exact slam frame, add 150-400ms tail; follow with 0.2-0.5s of lowered music (duck) or silence-gap for emphasis.
- Whoosh for every move = noise. Cue the primary mover only, max ~1 cue per 0.35s; group staggered items into 1 cue (not n cues) or use a single rising cascade of soft ticks (60-100% velocity variation, pitch +1-2 semitones per item, max 5).
- Vary: 3+ variants per cue type and +-6% pitch/+-2 dB to avoid machine-gun repetition.
- Levels (relative, LUFS-ish): VO 0 dB reference; music -14 to -18 dB under VO (duck -6 to -10 dB under speech with 80-150ms attack, 300-500ms release); SFX peaks -12 to -6 dB relative VO, hero impact up to 0 dB. Overall loudness -14 LUFS (online), true peak <= -1 dBTP.
- Silence: leave 150-400ms of near silence (music ducked to -inf or filtered) right before the hero reveal/ title drop ("pre-drop breath"), and 300-800ms after the final line before end card. Quiet is a cue as strong as a hit.
- Text sync: typing ticks at letter rate only for <= 12 chars; otherwise 1 soft tick per word at most.
- Transitions: whoosh begins 3-8 frames before cut, hit on cut frame. Hard cut on beat; place VO phrase starts 2-6 frames after the beat.
- Music: structure scenes to bars; stinger/final hit at scene end; fade tail 1-2s after logo.
- VO leads sync: show a UI action 100-300ms before narration names it.

Further reading:
https://www.itu.int/rec/R-REC-BR.1343
https://tech.ebu.ch/docs/r/r128.pdf
https://www.premiumbeat.com/blog/sound-design-for-motion-graphics/
https://www.schoolofmotion.com/blog/sound-design-for-motion-designers

---

## 9. Common amateur mistakes and senior fixes (25)

1. Linear or default `ease` motion -> use directional eases (eo in, ei out) or springs.
2. Everything moves at once -> one primary, others static or at 50% amplitude, stagger 40-150ms.
3. Everything bounces -> overshoot only on one hero per beat; others zeta >= 0.84.
4. Same duration for all elements -> scale 150-800ms by size/distance.
5. Entrance and exit mirror each other -> exit 60-75% duration, accelerate, shorter travel.
6. Starting from scale 0 -> start 0.92-0.96 for UI, 0.6-0.8 for pop; combine with opacity.
7. Text too small/too fast -> >= 24px (1080p), hold >= words/3 s.
8. Too many words per screen -> <= 7-word headline, one idea/scene.
9. Per-letter animation on sentences -> per word/line; per-letter only <= 12 chars.
10. Unreadable text over moving/busy backgrounds -> scrim, slow bg, 4.5:1 contrast.
11. Text outside safe area / under platform UI -> title-safe 90%, 9:16 bottom 25% free.
12. Dead static frames -> slow drift (push 3-5%) or ambient 3-6px; but not during text reading emphasis.
13. Overlapping moves with no hierarchy -> sequence them; viewer must name what moved.
14. Straight-line cursor/object paths -> arcs 8-20% deviation, dwell 100-160ms before click.
15. Cursor clicks with no reaction -> squash .92 80ms, ripple, UI response 40-80ms later, `M.cue pop`.
16. Cross-dissolving everything -> hard cuts on beat; transitions only for state relationship.
17. Fancy transition on every scene -> max 1-2 per piece, otherwise consistent cut style.
18. Constant pace -> slow-fast-slow, last shot longest (2-4s).
19. Cutting before reading finished -> cut after hold +4-8 frames.
20. Ignoring frame-accuracy of SFX -> cue at the impact frame; whoosh leads by 100-250ms.
21. SFX on every item -> one cue per beat; cluster staggers into one.
22. No silence -> duck/stop music 150-400ms before the hero.
23. Pure #000/#fff and neon glow everywhere -> #0B0D12-style neutrals, one glow, 15-35%.
24. Too many colors -> 60/30/10; one accent for focus only.
25. Mixed easing/radius/shadow languages -> constants block; one light direction; consistent radius family.
26. Camera and elements both animating heavily -> camera primary or elements primary, not both.
27. Ending abruptly -> final hero hold 2.5-4s, ambient motion only, then fade/stinger.
28. Sound/animation beginning exactly at beat -> start slightly before so the hit lands on beat.
29. Frame-dropped looks (non-deterministic randomness) -> seed all noise by t; no Math.random() in frame function.
30. Motion blur/smear on everything -> `M.smear` only for velocity > 1.5 screen widths/s.

Further reading:
https://www.schoolofmotion.com/blog/common-motion-design-mistakes
https://m3.material.io/styles/motion/overview/specs
https://www.nngroup.com/articles/animation-purpose-ux/

---

## 10. Senior review checklist (run on contact sheets before render)

Contact sheet protocol: render every 0.25s (4 per second) for the whole piece, plus every frame (or 33ms) around each hit/transition, plus the last frame of every hold.

A. Hook and structure
- [ ] First frame (t=0) has meaningful content; hook readable by 1.5s.
- [ ] Scene count vs duration: ASL matches target curve (section 6.3); final shot longest.
- [ ] Each scene has exactly one idea and one focal point (squint test).
- [ ] Story order: problem -> solution -> proof -> CTA.

B. Per-frame legibility
- [ ] Every text hold frame: opacity 1, blur 0, contrast >= 4.5:1 (3:1 for >= 48px), size >= 24px (1080p).
- [ ] Text within title-safe (90%); 9:16: bottom 25%, top 12%, right 12% free of key content.
- [ ] Hold time >= max(0.8s, words/3 s) measured from fully-visible frame to exit start.
- [ ] No text in the middle of cross-fade or overlapping other text.
- [ ] No more than 3 sizes, 2 weights, 1 accent per scene.

C. Motion quality
- [ ] No linear moves on objects; enter = decelerate, exit = accelerate, exit duration <= 75% of enter.
- [ ] Overshoot <= 5% for UI; one hero pop <= 10%; no ringing > 2 oscillations.
- [ ] Only one primary mover at a time in every sampled frame; others dim/static.
- [ ] Stagger gaps within 40-150ms and cascade total <= 600ms (hero <= 900ms).
- [ ] Moves have arcs, followers lag 40-120ms, settle phases visible (not frozen suddenly).
- [ ] Durations scale with size/distance (table 2.1); nothing >1.4s except camera/ambient.
- [ ] Shared elements stay continuous; no pop-in/out; no ghosting from double opacity.
- [ ] Direction continuity: exit direction -> next entry direction consistent.

D. Composition
- [ ] Focal point on thirds or deliberate center; negative space >= 40% on hero frames.
- [ ] Nothing clipped at frame edge unintentionally; element spacing on 8px grid.
- [ ] Depth cues consistent: one light direction, elevations, parallax ratios 1:.6:.3.
- [ ] Camera move eased (CAM), single, not fighting element animation; no unmotivated roll > 3deg.

E. Color and light
- [ ] Palette 60/30/10 holds; accent < 15% of pixels; no pure black/white.
- [ ] Glow single-source, 15-35%, none on body text.
- [ ] Theme flips <= 2 per 30s and motivated; color transitions interpolated in OKLCH.

F. Edit and rhythm
- [ ] Cuts happen after read + 4-8 frames; cut on action or match cut; no near-duplicate jump cuts.
- [ ] Hard cuts on beat; transitions used only for relation/time/space; <= 2 distinct transition types.
- [ ] Beat grid: key hits on downbeats; scene boundaries on bar lines.
- [ ] No more than 3 consecutive high-density scenes; breathing frames present.

G. Sound
- [ ] Each audible cue lands within +-1 frame of the visual hit (whoosh leads 100-250ms).
- [ ] Cue density <= 1 per 0.35s; staggers share one cue; variants/pitch jitter used.
- [ ] Music ducked under VO (-6 to -10 dB) and silence gaps before hero/after last line.
- [ ] Loudness around -14 LUFS, peaks <= -1 dBTP; end tail 1-2s.

H. Technical determinism
- [ ] Frame function is pure in t (no Math.random, Date.now, unseeded noise); scrubbing back/forward gives identical frames.
- [ ] First/last frame of each scene correct when rendered in isolation; no dependence on previous frame.
- [ ] Fonts loaded before render; no layout shift between frames; all springs clamped for t < t0 (value=0) and finite for large t.
- [ ] Any failing item -> fix, re-render contact sheet of the affected span only, re-run checklist for that span.

Further reading:
https://www.schoolofmotion.com/blog/motion-design-critique
https://www.nngroup.com/articles/animation-duration/
https://developer.apple.com/design/human-interface-guidelines/motion
