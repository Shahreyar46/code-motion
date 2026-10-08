<!-- generated from commands/video.md by tools/sync_presets.py; edit the command, not this file -->
Make a video with the code-motion skill. Skill folder: `this skill's folder`.

Request: the user's message (flags like --auto, --music, --unattended may appear in it)

0. If the request contains `--unattended` (or this is a scheduled run with nobody to answer): follow `references/unattended.md`. Take the topic and type from `video/queue.md` (first unchecked item) and the brief from `video/brief.md`, then continue below without asking any questions.

1. Classify the request into one type and read that type's preset file (all in `references/presets/`) before anything else:
   promo/launch/ad → `references/presets/promo.md` · product overview (what it is + feature tour) → `references/presets/overview.md` · tutorial/docs/how-to → `references/presets/tutorial.md` · product demo/walkthrough → `references/presets/demo.md` · concept/feature-update explainer → `references/presets/explainer.md` · vertical social reel/short → `references/presets/reel.md` · UI animation loop → `references/presets/ui-loop.md` · logo reveal/intro/outro → `references/presets/logo.md` · 3D scene → `references/presets/scene-3d.md`.
   If it's ambiguous, ask once which type, offering the two most likely.
2. Follow that preset together with the skill's full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver).
3. If the user shared reference videos, analyse them first: contact sheets (1 frame/s) + 8-frame bursts at transitions, then write a short breakdown (typography, motion, transitions, pacing, colours) in the format of `references/case-studies/*.md` and follow it.

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `the user's request` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.
