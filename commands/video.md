---
description: "Make any video with code-motion; it picks the right type (promo, tutorial, demo, explainer, reel, UI loop, logo, 3D) from your request"
argument-hint: "[--music] [describe the video you want]"
---
Make a video with the code-motion skill. Skill folder: `${CLAUDE_PLUGIN_ROOT}/skills/code-motion`.

Request: $ARGUMENTS

1. Classify the request into one type and read that type's preset file (all in `${CLAUDE_PLUGIN_ROOT}/commands/`) before anything else:
   promo/launch/ad → `${CLAUDE_PLUGIN_ROOT}/commands/promo.md` · product overview (what it is + feature tour) → `commands/overview.md` · tutorial/docs/how-to → `commands/tutorial.md` · product demo/walkthrough → `commands/demo.md` · concept/feature-update explainer → `commands/explainer.md` · vertical social reel/short → `commands/reel.md` · UI animation loop → `commands/ui-loop.md` · logo reveal/intro/outro → `commands/logo.md` · 3D scene → `commands/scene-3d.md`.
   If it's ambiguous, ask once which type, offering the two most likely.
2. Follow that preset together with the skill's full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver).
3. If the user shared reference videos, analyse them first: contact sheets (1 frame/s) + 8-frame bursts at transitions, then write a short breakdown (typography, motion, transitions, pacing, colours) in the format of `references/case-studies/*.md` and follow it.

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `$ARGUMENTS` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.
