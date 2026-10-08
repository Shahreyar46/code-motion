<!-- generated from commands/tutorial.md by tools/sync_presets.py; edit the command, not this file -->
Make a **tutorial / docs video** with the code-motion skill. Load the skill and follow its full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver). Skill folder: `this skill's folder`.

Request: the user's message (flags like --auto, --music, --unattended may appear in it)

## Preset for this type
- **Length** 60-150s; one task per video (split long docs into a series and say so). 16:9, 1920×1080.
- **Truth first**: read the docs page / README / settings screens. Every step, label, menu name and button text must match the real product exactly. If you can open the product (browser/screenshots), capture the real UI and rebuild it in HTML. If a step is unclear, ask; never guess UI.
- **Structure**: title card ("How to …", 3s) → what you'll get (result shown first, 5s) → full UI shown once for orientation (tilted, dimmed) → steps. Each step = step chip "1/5" + first-person caption ("Let's connect your account", last word highlighted) → crop-zoom to the exact control → one cursor action (click/type/drag) with `click`/`key` sounds → result state → 0.5s pause → next step. End with recap list (cycling words or checklist) + where to learn more (docs URL).
- **Start from** `templates/saas-demo.html` (tilted dashboard, cursor, morph chain, crop-zoom). Light Glass or Google Playful style unless their brand says otherwise.
- **Read** `references/pro-techniques.md` section 6 and `references/case-studies/googlevids.md` (the tutorial pattern) + `teamble.md`.
- **Voice**: friendly, slower (~140 wpm, `rate` -6% to -8%), instructional: say exactly what to click and where ("Open Settings, then Integrations"). One step per VO line, `pause` 0.5-0.7s after each action line.
- **Sound**: hover + click per cursor action, keys while typing, tick per step chip, success on each completed step. Quiet otherwise.
- **Brief questions**: which task, product/version, docs URL or repo, the exact steps if not documented, viewer level (beginner/advanced), brand files.

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `the user's request` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `the user's request` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Docs deliverables (in addition to the video)
- Name VO line ids `step1`, `step2`, … so chapters are automatic.
- `python scripts/captions.py video/audio/timings.json video/out` → `captions.srt` / `captions.vtt` (upload with the video) and `chapters.txt` (YouTube description).
- `video/out/steps.md`: the same tutorial as a written user guide, ready for a docs page: title, what you'll achieve, prerequisites, numbered steps with the exact UI labels in **bold**, the expected result after each step, and the video timestamp for each step. Same wording as the narration.

## Quality bar before rendering
Every on-screen label matches the real UI; the cursor is on the control at the click frame; zoom makes UI text ≥28px on screen; each step's result is visible ≥1s before the next step; captions don't cover the control being used.
