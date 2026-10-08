# Numtera launch video, reverse-engineered notes (95s, 1080p30, 10 hard cuts)

## Overview
- 0-8s HOOK/PROBLEM: white bg, typed text "The same issue, Different channels", "Same investigation... again?" over faint ghost UI cards. Typewriter with caret, "Different" gets blue selection highlight then deleted.
- 8-10s "Stop Managing tickets" (blur-in, gradient-text), 10-13s "Meet Numtera" huge then shrinks with logo.
- 13-23s SOLUTION: "The AI-powered self-learning support OS", UI app tilted in 3D, glass blur wipes.
- 23-29s dark terminal-like cards (Connected to infrastructure, Scanning memory, Verified source).
- 29-39s "Agent Approves it as {learning}" -> blue progress pill -> expands to ticket card with scan line.
- 40-47s dark blue: "it turns the solution into [Reusable knowledge]" brackets collapse.
- 45-50s dashboard cursor, "Auto-resolved" italic extended font, blur-out.
- 50-54s "And / when you know the outcome / You can define the response".
- 55-1:16 workflow builder: menu card, 3D tilt page, form zoom (typing "Manufacturing: Production Status"), steps stack, Save click.
- 1:17-1:26 payoff: "The system gets smarter, forever." "They close tickets" -> "We Eliminate them" -> logo.
- 1:27-1:33 CTA on black/blue: typed "The self-learning support OS", "Start a free trial now!", www.Numtera.com. Fade to black 1:33-1:35.
- Pace: ~14 ideas/95s, ~5-7s each; text beats 1.5-3s hold.

## Typography
- Neo-grotesk / geometric sans (Inter/Satoshi-like), weight 500 body, 700 for "Meet". Extended italic wide grotesk for "Auto-resolved" (one-off).
- Hero word "Meet" ~300px bold tight tracking (-0.03em); subtitle lines ~44-56px medium; labels ~16-20px; mono for "learning..." (~40px).
- Sentence case. One line, short (<45 chars), centered at y~50%.
- Entrances: typewriter + caret (hook, CTA); per-word blur-in with scale (Stop Managing); chars rise with blur (Meet); fade/scale-out with heavy blur (Auto-resolved, "They close tickets" zooms past camera, 1.5x blur out).
- Highlights: key word in accent blue (#1F3FFF on light, #2E9BFF on dark), selection-box highlight (#2F6BFF bg, white text), brackets {learning} / [Reusable knowledge] in blue, brackets collapse to [] on exit.
- Text color: #0A0A0F on light, #FFFFFF on dark.

## Color & look
- Palette: white #FFFFFF, sky #6EC1FF, azure #1E90FF, royal #1B3FE0, navy #04153A, black.
- Backgrounds: soft radial/vertical gradients white->sky->royal at bottom edge, large blurred glow blobs, dark scenes navy radial with black vignette. No grain visible.
- UI glass cards: white 70% alpha, backdrop blur, radius 16-24px, soft large shadow (0 30px 80px rgba(20,60,200,.2)), 1px white border.
- Light-sweep diagonal shafts across screens (~21s).

## Motion vocabulary
- Typewriter w/ caret + selection highlight delete (~18cps).
- Blur-in per word 0.4s ease-out, 8px blur->0, slight scale 0.96->1.
- Blur+scale-out exit: scale 1->1.6, blur 0->30px, 0.3s (text flies through camera).
- UI page enters in 3D: rotateX ~45deg/rotateZ skew, drifts and settles flat ~1.2s, then keeps slowly dollying.
- Pill (blue progress bar) slides in from right with motion-blur streak, bar fills; morphs into ticket card.
- Scan line (cyan glow) sweeps down card.
- Cursor glides to target with eased curve, click triggers state change.
- Menu items stagger in 0.1s apart; step cards stack with numbered badges.
- Zoom-into-input cropped (x3) to show typing, blur on defocus then zoom out.

## Transitions
- Mostly continuous (blur/scale handoffs, UI kept moving through text beats); 10 hard cuts mostly at light<->dark/background swaps (8, 10, 29, 39.6, 44.6, 47.4, 60, 78, 83, 86.5). Blur-through-white and zoom-through used between text and UI.

## Camera
- 2.5D perspective tilt on UI, slow push-in, defocus blur on exit, crop-zoom on form fields. No parallax layers except ghost cards at hook.

## UI showcase
- Full app screen as floating glass slab in tilted perspective, cropped zoom on feature, cursor + click, dim ghosting, no device frame, no callout boxes; uses stylized dark "console" cards for AI actions.

## Sound (inferred)
- mean -11.8 dB, peak 0 dB: loud mastered track; likely music bed with riser into "Meet", typing ticks, UI clicks/whoosh at blur transitions, probably no VO (text-driven).

## TOP 10
1. Typewriter hook: M.typed(text,t,t0,18) + caret blink, selection highlight pill on word then delete.
2. Blur-word entrance: M.words(spans,t,times,{style:'blur'}) 0.4s.
3. Fly-through exit: M.vis with scale up 1.6 + blur 30px, 0.3s.
4. Hero word chars rise: M.split(el,'chars') + 'rise' with blur, stagger 0.05s, then shrink to inline logo lockup via M.track.
5. 3D tilt UI settle: M.tilt(rx 50->0, ry) + M.cam push-in, spring omega 8 zeta .8.
6. Pill morph: M.morph progress pill -> ticket card -> scan line (M.stroke/linear sweep).
7. Cursor-driven UI: M.track cursor path + M.cue click, state flip.
8. Crop-zoom to form with M.cam(el,W,H,x,y,3) typing M.typed.
9. Bracket text accent: {word} -> brackets collapse via M.sp, blue color word.
10. Gradient bg shift light->dark via hard cut with M.cue 'whoosh'/'riser'; CTA typed on black.
New helper suggestion: M.sweep(t,t0,dur,y0,y1) returns y for scan line; M.blurOut(t,t0) -> {scale:1+0.6*e, blur:30*e, opacity:1-e}, e=easeIn(clamp((t-t0)/0.3)).
