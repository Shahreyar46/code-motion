---
description: "3D cinematic scene (10-60s) with Three.js: camera flythrough, scale journeys, hardware/science visuals, HTML text on top"
argument-hint: "[--music] [what the camera travels through, length, text beats]"
---
Make a **3D scene video** with the code-motion skill. Load the skill, read `references/engine-api.md` (Three.js section), and start from `templates/three-scene.html`. Skill folder: `${CLAUDE_PLUGIN_ROOT}/skills/code-motion`.

Request: $ARGUMENTS

## Preset for this type
- Requires setup with Three.js: `/code-motion:setup ./video --three`.
- Everything is a function of t: camera on a `CatmullRomCurve3` spline sampled with an eased u(t); object transforms from t; no physics state, clocks or `Math.random` (use `M.rand(seed)`). `preserveDrawingBuffer:true`, `renderer.render()` inside draw.
- Headless rendering uses CPU WebGL: keep particles ≤50k, low-poly meshes, canvas-texture glows instead of post-processing. Draft with `--sub 2`; final `--sub 4` only if time allows (tell the user the render estimate).
- Text/HUD in HTML over the canvas with the normal M helpers (kinetic words, labels, scale ruler, counters).
- Voice optional: anchor beats to VO words if there is narration.
- Sound: whoosh on camera accelerations, suck into arrivals, impact + shimmer on the hero reveal.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `$ARGUMENTS` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar
Stills every second: subject framed, no clipping through geometry, text readable over the scene (add a soft dark gradient behind HUD text if needed).
