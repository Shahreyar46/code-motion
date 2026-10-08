---
description: "Explainer video (30-120s): a concept, feature update or \"what's new\", built from diagrams, kinetic type and simple visuals"
argument-hint: "[--music] [--auto to skip style questions] [topic or feature, source material URL/file]"
---
Make an **explainer video** with the code-motion skill. Load the skill and follow its full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver). Skill folder: `${CLAUDE_PLUGIN_ROOT}/skills/code-motion`.

Request: $ARGUMENTS

## Preset for this type
- **Length** 45-90s, 16:9.
- **Two modes**, pick from the request:
  - *Concept explainer*: one idea per beat; diagrams build (lines draw with `M.stroke`, nodes pop with `M.stagger`), hand-written labels (Caveat), analogies as simple shapes, a huge kinetic word as a palette cleanser between ideas. Paper & Marker or Editorial Serif style.
  - *Feature update / what's new*: each feature = action typed into a hero pill → UI demo → giant kinetic word card. Bridges: zoom-through or blob wipe. Google Playful or AI Neon Glow style.
- **Start from** `templates/launch-film.html` (kinetic type, strike-through, waveform-style data visuals) and borrow from `saas-demo.html` for UI.
- **Read** `references/pro-techniques.md`, `references/case-studies/search.md` + `gemini.md`, `references/prompt-patterns.md`.
- **Voice**: calm, curious, ~145 wpm; one claim per line; numbers only from the source.
- **Sound**: pen for drawing lines, pop for nodes, swish for word cards, chime on the "aha" moment. Use `--air` in the mix for slow explainers.
- **Brief questions**: the topic and the single takeaway, audience level, source material (docs, article, data), any numbers to show, style preference.

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `$ARGUMENTS` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `$ARGUMENTS` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar before rendering
A viewer with sound off still follows it from on-screen text; every diagram label is readable (≥28px); no fact appears that isn't in the source; no beat longer than 6s without visual change.
