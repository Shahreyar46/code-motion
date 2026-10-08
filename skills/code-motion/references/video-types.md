# Video types: structure, length, beats

Times are for the VO; adjust to the script. Every type: hook in the first 2 s, one idea per beat, end card ≥1.5 s after the last word (3-6 s for ads).

## Launch film / promo (15-45 s, 16:9 + 9:16)
1. Hook (0-3 s): bold question or pain, kinetic type. "What if…", "Your X is lying to you."
2. Problem (3-8 s): 2-3 short slams or a relatable broken UI.
3. Meet (8-11 s): big "Meet" → logo lockup. Riser → impact.
4. What it does (11-25 s): 3 feature beats, each = one UI moment + one line. Morph chain between them.
5. Contrast / proof (25-30 s): "They X. We Y." or before/after counter (real numbers only).
6. End card: logo + tagline + URL/CTA pill. `reveal` cue.

## Product overview promo (45-90 s)
What it is → who it's for → 4-6 feature tour with a progress chip → how it works in 3 steps → why better → CTA. Full preset: `commands/overview.md` in the plugin.

## Product demo (60-120 s)
Brand intro (dark) → promise headline (light) → 3-5 chapters (caption → tilted UI → crop-zoom → cursor action → result morph → ✓) → proof (before/after, counters) → logo + CTA. Alternate dark/light per chapter; hard cut + impact at flips.

## Tutorial / how-to (60-180 s)
Each step: step number chip + first-person caption ("Let's connect your account") → zoomed UI crop → one cursor action → result → short pause. Show the full UI once at the start for orientation. Keep VO instructional and slower (~140 wpm). End with recap list (cycling words) + CTA. Use real UI labels exactly; spell out where to click.

## Feature explainer / "what's new" (45-100 s)
Each feature: prompt/action typed into the hero element → UI demo → one huge kinetic word card as palette cleanser. Bridges between sections: zoom-through, dot tunnel, blob wipe.

## Concept explainer (30-120 s)
Paper & marker or dark diagram style. One concept per beat: diagram builds (lines draw, nodes pop), labels hand-written, analogies as simple shapes. Numbers only from the source.

## Social reel (15-45 s, 9:16)
Meme/relatable hook in 2 s → problem → hard cut → product promise → one-click demo → benefit chips → payoff callback → CTA (≥4 s). Safe zones: top 20% headline, bottom 12% empty. On-screen text must carry the message without sound.

## UI motion loop (8-15 s, 1:1 or 16:9)
One shape, never cuts, 120 BPM grid (0.5 s per beat), cursor drives every state, last frame = first frame. `M.morph`. Sounds: click per press, swipe per indicator move, tick per state.

## Showreel / brand reel (20-40 s)
"Show what an incredible motion designer you are, like a showreel for a résumé, go all out": fast variety, every 1.5-2 s a new technique, kinetic type, counters, 3D tilt, glow, logo finale.

## Logo reveal / intro / outro (3-8 s)
Riser into impact; mark draws on (stroke) or assembles (scramble/morph); wordmark mask reveal per char; tagline fades in; shimmer.

## 3D scene (10-60 s)
Three.js: camera on a spline, scale journeys (desk → atom, Earth → universe), HUD ruler/labels in HTML on top. `templates/three-scene.html`.
