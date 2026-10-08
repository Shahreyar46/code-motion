---
description: "Product promo / launch film / ad (15-45s) with voiceover and sound design, rendered from code"
argument-hint: "[--music] [--auto to skip style questions] [product, URL or repo path, length, anything to include]"
---
Make a **promo / launch video** with the code-motion skill. Load the skill and follow its full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver). Skill folder: `${CLAUDE_PLUGIN_ROOT}/skills/code-motion`.

Request: $ARGUMENTS

## Preset for this type
- **Length** 20-35s (ads 15s; ask if unclear). Formats: 16:9 master + 9:16 cut if they post on social.
- **Arc** (adapt beats to the VO): hook question or pain (0-3s) → 2-3 short problem slams → riser into big "Meet" → logo lockup → one-line positioning → 3 feature beats, each one real UI moment + one line, joined by morphs not cuts → contrast/proof line (real numbers only) → end card with logo, tagline, URL/CTA pill held 3-5s.
- **Start from** `templates/launch-film.html` (dark premium) or `templates/saas-demo.html` (light glass). Pick the style from `references/styles.md` that matches their brand; offer 2 options if they have no brand.
- **Read** `references/pro-techniques.md` sections 1-4 and 6, and `references/case-studies/numtera.md` + `langease.md`.
- **Voice**: confident, slight smile, ~150 wpm, 55-85 words total. Key word last in each line.
- **Sound**: whoosh per transition, pop per card, click per cursor press, riser + impact into "Meet", reveal on the logo.
- **Brief questions** (one round, skip what's known): product + URL/repo, the one thing viewers must remember, audience, CTA text + URL, brand files (logo, colours, screenshots) in `video/assets/`, length/formats.

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `$ARGUMENTS` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `$ARGUMENTS` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar before rendering
Hero visual lands on its key word; one idea on screen at a time; no invented stats or logos; every feature beat shows the real product (rebuilt UI, not blurry screenshots); end card readable for ≥3s; contact sheet checked twice.
