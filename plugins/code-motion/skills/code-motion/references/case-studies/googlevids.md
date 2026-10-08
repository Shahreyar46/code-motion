# Google Vids intro: reverse-engineering notes (87s, 1080p)

## Overview
Arc: 0-5 "Meet your [New pill] designer/editor/storyteller" rolling word slot, cursor hits New (~4s) -> menu -> Google Vids. 5-9 prompt pill types "Help me create a sales training video". 10-15 app icons float, cursor drags a Slides file chip into the prompt; "Creating..." blue pill. 15-18 outline tilted in 3D then flattens (UI plane). 18-24 "Let's choose a style" -> style picker -> template cards. 26-35 "Let's write my script" -> mic button -> Script panel, text streams in blue. 36-46 "Now, let's give it a voice" -> gradient blobs wipe -> voice list, cursor selects Voice 2 (zoomed), waveform bars. 47-53 comments panel (collab). 54-60 stock media search "Landscape", image grid, drag into timeline. 60-64 editor timeline. 64-75 record: red button, 3-2-1 countdown blurred, presenter in frame. 75-80 Play button (concentric glow ring). 80-83 kinetic words ("AI powered / for work / event recaps / vendor outreach / how-to tutorials / project updates / company milestones") on white then blue gradient. 83 "coming soon". 84-87 Workspace icons -> "Google Workspace" wordmark.
Pacing: ~1 beat per 4-6s; hard cuts (cuts.txt) only at ~13.5, 25.6, 30.5, 39.5, 42.5, 46.5, 47.7, 50.4, 60.2, 64.2, 65-69 (countdown 1/s), 71.8, 73.6, 75, 82.6. Between cuts: continuous morph.
Tutorial pattern: one big typed caption (the "step title") -> cut/morph to UI crop of that step -> cursor does the single action -> result state; next step title. Step titles are first-person ("Let's choose a style", "Now, let's give it a voice"), last word in blue.

## Typography
Google Sans / Product Sans style geometric sans, regular weight (400), tracking slightly tight. Hero captions ~110-140px (e.g. "Now, let's give it a voice" ~100px, ~60% width); UI-label text 28-36px; tiny UI 10-14px. Color #3C4043 body, key word in gradient blue #4285F4 -> #4F6BFF -> #8AB4F8 (per-glyph gradient left-to-right, "voice" goes violet-blue to light-blue). Typed with caret: thin 4px dark caret #444, caret stays after last char; text scrolls left (clipped at the frame edge, reads "e it a voice|") as it overflows. Word slot ("designer/editor/storyteller") swaps by blur-fade + vertical slide ~0.35s, hold ~0.8s. Kinetic end words: blur+fade in (~0.4s), hold ~1s, exit with blur and horizontal motion-blur smear ("how-to tutorials" shows streaky horizontal blur); white text on blue gradient after bg flip at 80.8s. Final words shrink to small "coming soon" ~36px.

## Color & look
Bg near-white #FAFBFE with large soft blurred pastel blobs (sky #A8D8FF, lavender #C9B8F5, pink #E8B4F0). Blue accent #3B6CF5 / #4A6CF7 for "Creating..." pill and primary buttons (#1A5BD6). Pills: radius = full, glassy #E8EEF8 fill, 1px light-blue rim highlight on top edge, soft shadow 0 8px 24px rgba(60,90,160,.18). UI cards radius 24-32px, white, same shadow. Playful geometry: circles, rounded rectangles, capsule, star, blob ellipses with blue-violet-pink linear gradients (pill bars at 38-40s). Presenter slide template: teal #0F5D4F, yellow #F5D90A, pink #E8A0B8. Waveform: white vertical rounded bars on blue gradient #3B82F6->#8AB4F8.

## Motion vocabulary
- Rolling word slot: out blur+up, in blur+from-below, ~0.35s, ease-out cubic / spring zeta .8.
- Pill scale-in from 0.8 with spring (omega ~14, zeta .7), overshoot ~4%.
- Typing: ~14 cps for prompts, caret solid; ~20 cps for script, text streamed in blue.
- "Creating..." pill: loops sparkle (4-point star rotating/scale pulsing ~1.2s), pill leans in 3D slightly (rotateY ~8deg) and enlarges 1.0->1.15.
- Panels tilt in 3D: card enters at rotateX ~25deg, rotateZ -8deg, flattens in 0.8s ease-out (15s).
- Cursor: black hand-pointer with white outline ~40-60px, path = curved arc, eased in-out ~0.8s, press = scale .85 for 0.12s; cursor enters from bottom-right/bottom.
- Buttons press: depress + click ripple; menu items slide in from right.
- Concentric ring pulse on Play (3 rings expanding, 1s loop, opacity to 0).
- Gradient blobs: big ellipses sweep across screen as transition (38-40s), 0.8s, ease-in-out; shapes morph (circle to capsule).
- Selection: check circle (blue #1A5BD6, white check) pops with spring; row highlight light gray.
- Countdown numbers 3-2-1 in translucent circle w/ progress wedge over blurred video, 1s each, hard cut each.

## Transitions
Mostly morph/continuity: pill -> menu, prompt pill -> blue "Creating" pill (same shape, recolor), blobs wipe, typed text pushes out. Hard cuts only between chapters (white card <-> UI). Background flips white->blue via radial blur blob expanding at 80.5s. Wipes by shape: giant ellipses sweeping horizontal.

## Camera
UI is shown as cropped zoom (2-4x) on the active control, never full app, until 61s (full editor timeline for orientation). Zoom-to-feature via scale + translate in one spring; slight 3D perspective tilt on first reveal. Static otherwise; cursor does the "camera" work.

## UI demo technique
Cursor-led: cursor travels to target, hover state highlights, click, result animates. One action per shot. Inputs enlarged to caption scale. Side toolbars (icons right edge) show tool context. Callouts: colored name flags with cursors (Kai, Evelyn) for collab; comment cards stack and fade top/bottom (vertical list with mask fade). Focus dimming: neighbors reduced opacity (comment cards 40%), selected row elevated. Blur of background during record countdown.

## Sound/VO (inferred)
mean -19.9 dB, peak 0 dB. Likely upbeat light electronic/piano music bed, VO narrating steps in sync with the text, UI clicks/soft pops on cursor press, whoosh on blob wipes, shimmer on "Creating", ping on select.

## TOP 10 TECHNIQUES
1. Rolling word slot: implement as M.vis per word with 'blur' style inside fixed-width inline box; M.track for width tween.
2. Typed caption + caret + overflow scroll: M.typed(text,t,t0,cps) with caret div, wrap in overflow-hidden, translateX = -(max(0,textW-boxW)); color last span gradient via background-clip:text.
3. Cursor-driven single action: M.track(cursorXY,[[t,target]]) spring path with curve offset; click = M.sp pulse scale .85; fire M.cue('click').
4. Morph pill: M.morph one rounded rect changing width/radius/color through states (New -> prompt -> Creating).
5. 3D tilt-flatten UI plane: M.tilt(rx,ry) driven by (1-M.sp) from 25deg to 0 plus M.cam scale 0.9->1.
6. Zoom-to-feature crop: M.cam(el,W,H,x,y,scale,rot) with scale 2-4 target the control; spring omega 10 zeta .9.
7. Blob wipe transition: giant gradient ellipses translate across 0.8s; swap scene at midpoint; M.cue whoosh.
8. Kinetic end words: M.words style 'blur' enter, exit with blur plus horizontal motion-blur (filter blur(0 -> 12px) via SVG feGaussianBlur stdDeviation x only); bg flip white to blue.
9. List fade-mask stack (comments): cards translateY, opacity by distance from focus; mask-image linear-gradient top/bottom.
10. Selected row check + concentric ring pulse: M.sp for check scale; rings = 3 elements with scale 1->1.4, opacity .6->0, stagger .25s, loop.
New helper: M.arc(t,t0,dur,p0,p1,bend) -> position = lerp(p0,p1,e)+perp*bend*sin(pi*e), e=easeInOutCubic((t-t0)/dur).
New helper: M.xblur(el,amt) -> filter url(#xb) with feGaussianBlur stdDeviation="amt 0".
