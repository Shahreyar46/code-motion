---
description: "Dribbble-style one-shape UI motion loop (8-15s, seamless): one element morphs through UI states driven by a cursor"
argument-hint: "[--music] [UI states to show, colours, size 1:1 or 16:9]"
---
Make a **one-shape UI motion loop** with the code-motion skill. Load the skill, read `references/engine-api.md` (M.morph), and start from `templates/ui-morph.html`. Skill folder: `${CLAUDE_PLUGIN_ROOT}/skills/code-motion`.

Request: $ARGUMENTS

## Preset for this type
- 1080×1080 (or 1920×1080), 60fps, 8-15s, no voiceover by default (ask; a loop usually has only UI sounds).
- One shape never cuts: each state is the same element changing size, radius and colour; content swaps with a short blur (enter after the morph starts, leave before the next). 120 BPM grid: something happens every 0.5s. Cursor drives every change with real clicks and drags. Camera zooms so each state fills the frame. Last frame = first frame.
- 8-12 states, e.g. button → loader → check → toggle → tabs (edges on different springs so the indicator stretches) → chart drawing itself → search/command palette → toast → back to button. Use the user's states if given.
- Style 6 (One-Shape UI Motion): warm grey canvas, black/white components, one accent. Banned: bouncy easing, particles, glows, gradients on UI chrome, mismatched icon strokes, dead time.
- Sound: click per press, swipe per indicator move, snap per toggle, tick per state, success on check.
- Render `--fps 60 --sub 4`. With no VO: `python sfx.py mix out/x.cues.json audio/mix.wav --dur <T>`, then mux.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `$ARGUMENTS` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar
Stills at every state change: no text overlapping during swaps, cursor inside frame at every zoom, loop seam invisible (compare t=0 and t=T stills).
