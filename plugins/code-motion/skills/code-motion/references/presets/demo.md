<!-- generated from commands/demo.md by tools/sync_presets.py; edit the command, not this file -->
Make a **product demo video** with the code-motion skill. Load the skill and follow its full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver). Skill folder: `this skill's folder`.

Request: the user's message (flags like --auto, --music, --unattended may appear in it)

## Preset for this type
- **Length** 60-100s, 16:9 (+ optional 9:16 30s cutdown).
- **Arc**: dark brand intro (logo + typed "Introducing …") → light promise headline → 3-5 feature chapters → proof (before/after cards, real counters) → logo + tagline + CTA. Alternate dark/light per chapter, hard cut + `impact` at each flip.
- **Each chapter**: caption line → whole UI once, tilted → camera crops into the one component → cursor action → result as a morph chain (button → loading → result → detail → ✓). Show only one component at a time, text 1.3× real size.
- **Start from** `templates/saas-demo.html`; Dark ↔ Light Chapters or Light Glass style.
- **Read** `references/pro-techniques.md` (all) and `references/case-studies/teamble.md` + `numtera.md`.
- **Voice**: confident and clear, ~145 wpm. One feature per chapter, benefit first then how.
- **Sound**: whoosh at chapter flips, pops for cards, clicks, shimmer on AI/loading, success on ✓, reveal on logo.
- **Brief questions**: product + access to real UI (URL, screenshots, repo), the 3-5 features in priority order, audience, real proof points they can share, CTA, brand files.

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `the user's request` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `the user's request` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar before rendering
Every feature shown is real and working in the product; no fake metrics; each chapter ends on a clear result; chapters are 10-20s, not longer.
