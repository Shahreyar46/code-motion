# Prompt patterns from 280 viral Opus 5.5 videos

What the best creators told the model, distilled. Use these as your own internal brief when the user's request is short.

## Process patterns that made the difference
- **Read the real source first**: landing page, repo, CSS tokens, logo (trace to SVG), current screenshots. "Do not invent functionality that does not exist." Prefer newest source over stale artifacts.
- **Write a style bible + component kit first** when making many animations, so all look like the same show.
- **Render one still per beat into a contact sheet before any video**, fix cramped/clipped/off-grid, then render. "I didn't review it by watching renders, it tiled 20 stills into one contact sheet."
- **Self-critique loop**: render a frame, critique it like a VFX supervisor / design director, fix, repeat. P0 issues always fixed; others only if worth it. Back up before each round, roll back what can't be fixed.
- **Notes like a creative director**: "make it less like a PowerPoint", "go all out, like a showreel for your résumé". Push past the first cut.
- **Multiple cuts from one codebase**: 30 s / 15 s / 6 s and 16:9 / 9:16 as different scene lists; captions measured in the real font and shrunk to fit the safe zone.
- **Sync everything to a grid**: beats (120 BPM) or, here, the voice's word times. Sound placed at measured peaks.

## Craft rules creators wrote into prompts
- "Every style is computed from time inside seek(t): no CSS transitions, no timers, no state carried between frames."
- "Springs are closed-form step responses. A value that changes target many times is the sum of one spring per change."
- "Content enters after its container starts morphing and leaves before the next morph so text never overlaps."
- "Never fade black directly into the accent colour. Move an accent element between states instead."
- "Tab indicators stretch: each edge on a different spring."
- "Zoom the camera so every state fills the frame."
- "Set every from-state at t=0 (seek-safe); never cover an exit. One primary move per transition; no generic push/slide/rotate-swing."
- "Real easing, squash/stretch, stagger, overlap, onion skin, smear, follow-through."
- "Kinetic typography word by word, spring easing, smooth camera pushes and pans, depth and glow, elements that build in on the beat instead of just appearing."
- "Keep each scene on screen long enough to read."
- "One soft sound effect for every element that appears and silence otherwise."
- "End on a memorable animated logo reveal with the tagline and URL."
- "Render with 4-6 subframes per frame blended for motion blur, H.264 yuv420p, export all aspect ratios."
- "Master −14 LUFS, −2 dBTP, re-measured after AAC encode."
- Banned lists: "bouncy easing, particle bursts, glows, gradients on UI chrome, mismatched icon strokes, dead time, anything that looks like a template"; "no chrome (scrubber, timecode, fps, headers)"; "no animator jargon on screen"; "no invented results: no %, multipliers, customer names or figures".

## Reusable master brief (fill the braces)
> Act as a senior motion designer and build a {LENGTH}-second {TYPE} for {PRODUCT} entirely in code. First read {SOURCES} to pull the real story, copy, colours, font and logo (trace the logo to SVG). Write it as one story ({ARC}) in {N} scenes, one short line each, narrated by a natural male voice. Animate like a premium product film: kinetic typography word by word on the spoken words, spring easing with tiny overshoot, 2.5D tilted UI that settles flat, crop-zooms into the feature being used, a cursor that does one real action per step, morphs instead of cuts, one highlighted key word per line. One soft sound effect for every element that lands, a whoosh per camera move, silence otherwise, riser into the logo reveal. Keep each scene long enough to read. Render a contact sheet first, fix anything that overlaps, clips, feels rushed or looks like a template, then render at 60 fps with motion blur and master to −14 LUFS.
