# Google "What's New in Search" (97s) reverse-engineering notes

## Overview
0-3s black->light grey (#F1F1F1 soft vignette). 3.8-5.5 colored pill bars (blue glow->flat blue, red, green) = vertical rounded bar becomes text caret. 5.5-8 "This is AI Search|" typed w/ blue-tinted newest chars. 8 3D tilted search pill (rainbow edge glow) with Google wordmark. 9-15 kinetic headlines ("Search reimagine|", "help me find a...", "for the agentic|") typed into 3D-tilted pill; arrow button zoom 14s. 15 giant "Search" slam. 16-22 "Visualize it" (letters extrude to 3D blue, slider scrubs) then AI Mode box typing (Camille). 23-32 dark section: wireframe glass panels, code, "CODE" dot sphere, green radial tunnel (hyperspace) = generative UI. 33-45 AI Mode workout/meal-plan UI, tilted 3D panels flying through, purple (#E9E3FA) UI. 45-47 "Look for it" kinetic text. 47-57 "keep me updated" prompt, phone lockscreen notif (agent). 57-60 "& shop for you" rotated words, cart icon. 60-70 shopping cart UI, add to cart, price drop, Buy now. 71 "You can search | understand" on black w/ red/blue letters; 72-75 rapid cuts (flurry of photo flashes at 0.1-0.3s: plane window, cowboy, birds) "do anything"; 76-79 "all you have to do is / ask"; 79-97 Google G logo hold (long outro; this is a YouTube end-screen pad, NOT a technique to copy: hold end cards 3-6 s per pro-techniques rule 12).
Pacing: 3-6s per beat, hard cut list: 15.3, 27.5, 31.6, 32.9, 45.8, 53.3, 71.4, then burst 73-76 (0.1-0.3s). Chapters are NOT numbered; each feature = prompt typed -> UI demo, joined by big kinetic word cards.

## Typography
Google Sans (geometric humanist, Product Sans lineage), weight 500-700 for headlines, 400 for UI. Headline ~110-130px for words, giant "Search" ~280px bold; UI prompts ~28-32px. Black #111 on light. Tight tracking -2%. Text typed with caret (blue #4285F4 caret, newest 2-3 chars blue-tinted w/ blur), ~14 cps. Word-mode cards swap with ~0.3s fade/blur; hold 0.8-1.2s. Variable-width letter morph: "search" widens/stretches letter by letter (font width axis animated per char, 70.8s). "Visualize it" letters extrude 3D blue starting with V,i,s progressing left->right while slider scrubs. Rotated word entry ("& shop" at -15deg, "you" slams/rotates in with motion blur).

## Color & look
Light bg #F2F2F2 radial gradient; Google blue #4285F4, red #EA4335, yellow #FBBC04, green #34A853 appear as bars/rainbow edge glows on pill (blue top-left, red bottom, green/yellow right). UI cards white, radii 24-40px, large soft shadows; AI Mode panels lavender #E8E0F7/#6A4FD6. Dark chapter #000 with neon RGB edges.

## Motion vocabulary
- Bar-to-caret: pill 14x90px w/ glow, glow decays 0.3s, becomes 3px caret.
- Typing: char reveal 12-16cps, blur-in last chars, caret blink.
- 3D tilt pill: rotateY/X ~15-25deg, perspective ~1200, drifts slowly (camera dolly) with rainbow glow edge.
- Slam text: scale 1.15->1, 0.25s ease-out, motion blur.
- Panels flying: cards at various z fly past camera w/ heavy depth blur; push-in zoom then crossfade into next UI.
- Hyperspace tunnel of dots at 32s as bridge transition.
- Rapid cut flurry 73-76s (0.1s cuts).

## Transitions
Mostly continuous: camera push through screens (zoom into UI, next UI emerges blurred then focuses), word cards as palette cleanser; 2-3 hard cuts to black for section break; blur-through crossfades.

## Camera
Virtual 3D camera with perspective; slow dolly + roll, UI panels tilted; depth-of-field blur on non-focal elements.

## UI/phone demo
Flat vector phone (rounded 48px, status bar 9:30/12:30), lockscreen notification slides in; UI cards rise with blur; cursor (hand pointer) drags slider; blue circular send button pressed; scroll content blurred during camera move; zoom to details (price $138.98, Add to cart pill).

## Sound (inferred)
Mean -17 dB, peak -0.5. Warm VO + light synth/pluck music, soft UI ticks on typing, whooshes on camera moves, riser into hyperspace, final resolve chord on G logo.

## TOP 10
1. Bar->caret: M.sp on width/glow; implement as pill div morph (w 14->3) with box-shadow blur from M.sp.
2. Typed prompt with blue-tinted blurred tail: M.typed + last-3-chars span with filter blur and color #4285F4.
3. 3D tilted rainbow pill: M.tilt(rx,ry) + M.cam, border via conic-gradient mask + blur glow layer.
4. Word card swaps: M.words style 'blur'/'rise', hold 1s, M.vis exit blur.
5. Slam/rotated words: M.words 'slam' with rot -15deg, M.shake tiny.
6. Variable-width letters: NEW helper M.stretch(el,t,t0,dur,wFrom,wTo): per-char font-stretch / scaleX with stagger 0.04s per char.
7. 3D extruded text: Three.js TextGeometry blue (#2F5BE0) w/ stagger per char, slider M.track driven.
8. Push-through camera: M.cam scale 1->6 centered on UI element + blur ramp, crossfade next scene at 70% (M.cue 'whoosh').
9. Phone/UI mockups rising with blur, notification slide, send button press (M.sp scale 0.92) + M.cue click.
10. Hyperspace dot tunnel transition: Three.js points w/ z velocity ramp, M.cue riser; plus rapid 0.1s flash cuts and the G logo drawing on via M.stroke with 4 colour arcs (hold it 3-6 s, not 18 s).
