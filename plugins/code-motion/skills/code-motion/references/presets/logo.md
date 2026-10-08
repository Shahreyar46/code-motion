<!-- generated from commands/logo.md by tools/sync_presets.py; edit the command, not this file -->
Make a **logo reveal / intro / outro** with the code-motion skill. Load the skill and follow its workflow (skip the storyboard table; show 2 concept options in one line each instead). Skill folder: `this skill's folder`.

Request: the user's message (flags like --auto, --music, --unattended may appear in it)

## Preset for this type
- 3-6s, 16:9 (and 1:1 if asked), 60fps. Transparent version on request (`bg:null` → render to `.mov`).
- Use the **real logo**: trace/convert it to inline SVG (separate paths for mark and wordmark) so strokes can draw and parts can move. If only a PNG exists, ask for SVG; otherwise use the PNG as one element and animate around it.
- Pick one concept: (a) mark draws on with `M.stroke`, fills, wordmark mask-reveals per char; (b) letters `M.scramble` and assemble; (c) a shape/sparkle morphs into the mark (`M.track` on size/radius), then wordmark slides out from behind it; (d) zoom-through from a product UI element into the mark.
- Riser (0.8-1.2s) into `reveal` at the moment the mark completes; tagline fades in 0.6s later; hold ≥1.5s.
- Optional voice tag ("YourBrand. Tagline.") only if asked.
- Read `references/pro-techniques.md` sections 3-4 and `references/case-studies/gemini.md` (sparkle → logo).

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `the user's request` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `the user's request` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar
Logo proportions and colours exactly match the source file; final frame is clean (no motion blur residue, no particles over the mark).
