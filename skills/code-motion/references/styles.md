# Styles

Pick one per video; the user's brand overrides colours and fonts but keep the motion personality. Each style: when to use, palette, type, motion, signature moves, sounds.

## 1. Dark Product Film (default)
Premium SaaS/dev tools; "Apple keynote × Stripe".
- Palette: bg `#0d0e12`, ink `#F3F1EC`, muted `#8b8f98`, card `#15171c`, line `#24262d`, one accent (`#FF5A1F` or brand).
- Type: Geist 600-700 headlines (−0.035em), Geist Mono for code/labels.
- Motion: word rise, cards rise with 2.5D tilt settling flat, slow camera push per scene, cross-blur transitions, vignette.
- Signature: real UI rebuilt in dark cards, counters, logo reveal with stroke draw.
- Sound: whoosh per transition, pop per card, key ticks, reveal at end.
- Template: `templates/launch-film.html`.

## 2. Light Glass SaaS
Friendly B2B launch/demo (Numtera, LangEase, Teamble light chapters).
- Palette: bg `#F6F6FD`/`#FAFBFE`, text `#0A0A0F`/`#1a1a2e`, secondary `#6B6F80`, primary `#2B4BF0`/`#1F3FFF`, sky `#6EC6F5`; pastel orbs `#B9A6FF`, `#A8DCF5`, `#FFB8DA`.
- Type: Geist 500 sentences 44-56 px, 700 heroes; key word gradient blue→cyan.
- Motion: blur-rise words, `.glass` cards, morph chains, tilted dashboard → crop-zoom, hand/arrow cursor, confetti on success, drifting orbs.
- Signature: one element morphs through the whole film (folder → panel → bar → check → card → logo).
- Sound: soft whoosh per morph, click, pop, success, shimmer, riser into logo.

## 3. Dark ↔ Light Chapters
Product demos with a problem/solution arc (Teamble, plugin reel).
- Dark `#0a0714` + magenta/violet orb (`#ff4fa0`, `#8a3ffc`) for problems/brand moments; light `#f6f0fb` + lilac/pink mesh for solutions.
- Keyword gradient `#ff3d8b → #b24dff`. Hard cut + impact on each flip.

## 4. AI Neon Glow
AI features, assistants, "magic" (Gemini).
- Palette: black `#000`-`#050508`, surface `#1A1B1E`, text `#F1F3F4`, keyword `#8AB4F8`; gradient `#4285F4 → #7B6CF6 → #A78BFA`; corner bloom `#5B4BC4` @30%.
- Type: Geist 400-500 only, small (28-34 px beats, keywords 56 px).
- Motion: `.rim` panels tilted −24° drifting, typed prompts with blue caret, letter scramble, cycling keywords, rack focus, sparkle star that morphs into logo.
- Sound: shimmer, soft pops, clicks, quiet riser, chime.

## 5. Google Playful
Consumer features, tutorials (Google Vids/Search).
- Palette: `#F1F1F1`/`#FAFBFE`, text `#111`/`#3C4043`, Google blue `#4285F4`, red `#EA4335`, yellow `#FBBC04`, green `#34A853`.
- Type: Geist 500-700, word cards 110-130 px, giant hero word ~280 px.
- Motion: typed captions with blue last word, rounded pills with rainbow edge glow, word cards as palette cleansers, blob wipes, phone mockup (48 px radius) with notifications, per-letter stretch.
- Sound: ticks on typing, whoosh, ding, bright chime on logo.

## 6. One-Shape UI Motion (Dribbble)
Loops, UI showcase, B-roll.
- Light warm grey `#E9E7E2`, black & white components, one accent. Geist.
- One shape never cuts: morphs size/radius/colour; content swaps with blur; cursor drives every change; camera zooms so each state fills frame; last frame = first frame.
- Build with `M.morph` (`templates/ui-morph.html`). Banned: bounce, particles, glows, gradients on UI chrome.

## 7. Paper & Marker Kinetic
Explainers, thought-leadership, podcasts (ik-builds, Voxyz).
- Paper `#F4F1EA` with subtle grain, ink `#111`, two marker accents (e.g. `#E8513A`, `#2E7DD7`); hard light/dark switches.
- Type: Anton for huge kinetic type, Caveat handwriting drawn via stroke, Geist for small labels.
- Motion: marker notes draw on (`M.stroke`), squash/stretch, overlap, follow-through, onion skin; a new idea every 1.5-2 s; ball/object with real physics leading the eye.
- Sound: pen scribbles, pops, whooshes, thud on big type.

## 8. Halftone / Acid Tech
Loud launches, dev/AI tools (LongCat).
- Black + one acid colour (`#2BE36B`) + white. Halftone dot patterns (CSS radial-gradient background-size 8px), pixel blocks, tunnels.
- Type: Geist 800 condensed-ish huge numbers ("1.6T", "1,000,000"), mono captions.
- Motion: hard switches, glitch transitions, counters, rings/tunnels, a mascot/eyes anchor that blinks on beat.
- Sound: glitch, impact, ticks, sub.

## 9. Editorial Serif
Brand stories, founders, premium/finance.
- Off-white `#F5F3EE` or deep `#0F1412`, ink, one muted accent (gold `#C9A45C`).
- Type: Instrument Serif headlines 120-200 px with Geist small caps labels.
- Motion: slow mask reveals, long holds, gentle camera drift, thin rule lines drawing.
- Sound: minimal: soft swish, chime, sub on logo.

## 10. 3D Cinematic
Hardware, science, "zoom through scales" (Three.js).
- Dark scene, physically-inspired lighting, depth of field feel, particles.
- Camera flythrough on a spline; scale ruler HUD; text minimal.
- Template: `templates/three-scene.html`. Keep geometry light (SwiftShader render).
