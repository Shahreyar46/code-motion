---
name: code-motion
description: Create professional motion-graphics videos entirely in code (HTML/JS pure function of time, rendered frame-by-frame with Playwright + ffmpeg), with a natural male voiceover and reactive sound effects synced to every move. Covers product launch films, SaaS promos and ads, feature explainers, tutorials and product demos, kinetic-typography pieces, Dribbble-style UI motion, social reels (9:16), showreels, logo reveals and Three.js 3D scenes. Use this skill whenever the user wants to make, create, generate, render or edit any video, promo, trailer, launch video, explainer, tutorial video, demo video, ad, reel, short, intro/outro or animation for a product, app, plugin, website, feature or idea, even if they don't say "motion graphics" or "code". Also use it when they share reference videos and want "a video like this", or ask for voiceover/sound design on an animated video.
---

# code-motion

Make videos the way the best Opus-made videos are made: **every frame is code**. One HTML page draws frame `t` in a pure function `seek(t)`; Playwright screenshots it frame by frame (with subframes for real motion blur); ffmpeg encodes. A natural male voiceover drives the timing, and every visual hit gets a synthesised sound effect. No music.

Why this works for an agent: the page is deterministic, so you can look at any frame (`stills.js`), fix it, and re-render; every number is editable; every scene can be anchored to the exact word the narrator says.

`$SKILL` = this skill's folder: `${CLAUDE_SKILL_DIR}` (if that shows literally, use the base directory printed when the skill loaded). Work in a `video/` folder in the user's project (or where they say).

## What to read when

| Need | Read |
|---|---|
| Writing the page: helpers, fragment format, VO anchors, cues, 9:16 | `references/engine-api.md` (always, before the first fragment) |
| Picking the structure for this kind of video | `references/video-types.md` |
| Picking a look (palette, type, motion personality) | `references/styles.md` |
| Asking the user which style / effects / pace (or letting AI decide) | `references/motion-menu.md` |
| Choosing a fresh story format / opening / transitions (never repeat the last video) | `references/formats.md` |
| Voice, music, imagery and topic rules | `references/content-policy.md` |
| Typography, transitions, UI-demo and camera craft from pro videos (read for every video) | `references/pro-techniques.md` |
| Senior motion-design & editing rules: 12 principles, easing/timing numbers, choreography, kinetic-type reading speed, composition, cutting, colour, sync, 30 amateur mistakes, senior review checklist | `references/motion-principles.md` (read sections 2, 4, 9, 10 for every video) |
| Writing the narration + choosing a voice | `references/voice-script.md` |
| Placing sound effects like a sound engineer | `references/sound-design.md` |
| Proven prompt patterns from 280 viral Opus 5.5 videos | `references/prompt-patterns.md` |
| Dark product film to copy from (kinetic type, code card, slams, waveform, logo) | `templates/launch-film.html` + `.script.json` |
| Light glass SaaS demo/tutorial to copy from (typed caption, Meet, tilted dashboard, cursor, morph chain, crop-zoom, orbit, confetti) | `templates/saas-demo.html` + `.script.json` |
| Frame-by-frame breakdowns of pro reference videos | `references/case-studies/*.md` |
| 3D scene starter | `templates/three-scene.html` |
| One-shape UI morph loop to copy from (button → loader → check → toggle → card, cursor-driven) | `templates/ui-morph.html` |

## Content & audio rules (always)

Read `references/content-policy.md` once per video. In short: **male voice only**; **no music** unless the user asks (`--music`); **no images of women or girls**; **no haram products or themes**; prefer nature and animal imagery, the product's real UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, never random Google Images results; log every image source in `NOTES.md`.

## Type presets

Each video type has a preset with its structure, defaults, template, brief questions and quality bar. When installed as the code-motion plugin they live in `${CLAUDE_PLUGIN_ROOT}/commands/` (`promo.md`, `overview.md`, `tutorial.md`, `demo.md`, `explainer.md`, `reel.md`, `ui-loop.md`, `logo.md`, `scene-3d.md`); users can also call them directly as `/code-motion:<type>`. Identify the type and read its preset before the brief. Without the plugin, use `references/video-types.md`.

## Workflow

### 0. Setup (first run in a folder)

```bash
bash $SKILL/scripts/setup.sh ./video          # add --three for 3D
```
Checks node, python, ffmpeg; installs Playwright + Chromium (and Three.js) into `video/node_modules`, and `numpy` + `edge-tts`. Run node scripts with `NODE_PATH=./video/node_modules` (or from inside `video/`).

### 1. Brief (one round of questions, skip what's already known)

Use AskUserQuestion once. You need:
- **What it's for**: product/topic, audience, the one thing a viewer should remember, the call to action.
- **Type + length**: launch/promo (15-45s), explainer/feature update (45-120s), tutorial/demo (60-180s), social reel (15-45s, 9:16), UI motion loop (8-15s). Formats: 16:9, 9:16, 1:1.
- **Truth sources**: repo path, landing page URL, brand tokens/CSS, logo file, real screenshots, real numbers. Ask them to drop files in `video/assets/`.
- **Look & motion**: follow `references/motion-menu.md`: a Style question with **Let AI decide (Recommended)** first plus the 3 styles that fit this type, then (only if they chose a style) a multi-select of signature effects, and pace for promos/reels. Skip the menu when the user says "you decide"/"auto"/"just do it", passes `--auto`, or already described the look. Their brand colours/fonts always apply on top of the style.
- **Voice**: default natural male narrator; ask only if they care (accent, energy). Run `python $SKILL/scripts/voice.py --list` first: if it shows only `edge`/`sapi`, tell the user they can connect their own premium voice by adding `GEMINI_API_KEY` (or `ELEVENLABS_API_KEY`) to their Claude Code settings `env` (steps in `references/voice-script.md`), otherwise the free edge-tts voice is used. Never ask them to paste a key into chat. Mention that cloud TTS sends the script text to the provider.

### 2. Harvest the truth

Read the real product before inventing anything: repo README/landing copy, CSS tokens (colours, radius, font), logo (trace to inline SVG so it stays sharp and can animate), real UI (recreate it in HTML from screenshots/source; don't paste blurry PNGs when a crisp rebuild is feasible).
**Never invent numbers, customer names, quotes, prices or results.** Use relative bars, skeleton lines or labels from the source, and list anything illustrative in the delivery notes.

### 3. Script → voice

Write `video/src/script.json` (format and rules in `references/voice-script.md`): one line = one visual beat, short sentences, ~150 words/min, the key word of each line near its end. Then:

```bash
python $SKILL/scripts/voice.py video/src/script.json video/audio
```
→ `vo.wav` + `timings.json` (line start/end and per-word times). Provider: Gemini TTS if `GEMINI_API_KEY` (most natural), ElevenLabs if `ELEVENLABS_API_KEY`, else edge-tts `en-US-AndrewNeural` (free, natural, real word timings), else Windows SAPI. `--list` shows voices. Lines are cached; edit one line and re-run, only that line regenerates. Read the printed timeline: if a line runs long, shorten the text rather than speeding the voice.

### 4. Storyboard, approved before code

First pick the **format, opening and transition family** with the rotation rule in `references/formats.md` (reads/writes `video/.code-motion-history.json`), so repeat users get a different video each time. Header line: `Format · Style · Opening · Transitions · Effects · Pace`.

Show a table, one row per VO line:

| # | Line (VO) | Time | Scene / visual | Motion (on which word) | Sound |

Rules: one idea per scene; something changes every 0.4-1.2s of speech; the hero visual lands ON the key word; leave the logo/end card on screen ≥1.5s after the last word. Pick transitions from `references/pro-techniques.md` (continuous morphs and match-moves beat hard cuts). Wait for approval or edits.

### 5. Build the page

Copy the closest template into `video/src/video.html` and rewrite it (dark film → `launch-film`, light SaaS/demo/tutorial → `saas-demo`, UI loop → `ui-morph`, 3D → `three-scene`) (`references/engine-api.md`). Anchor everything to the voice: `M.word('hook','code')`, `M.line('cta').start`. Declare sounds next to the motion that causes them with `M.cue(t, 'whoosh', {...})`.

```bash
python $SKILL/engine/build.py video/src/video.html video/dist/video.html --vo video/audio/timings.json --audio video/audio/vo.wav
```
Preview with sound: `node $SKILL/engine/server.js video/dist` → open the printed URL + `/video.html` (space play/pause, arrows step, `?t=4.2` freezes a frame). Give the user this link when they want to watch before rendering.

### 6. Look at stills, fix, look again (the step that makes it good)

```bash
node $SKILL/engine/stills.js video/dist/video.html video/stills/sheet.png --every 1      # whole cut
node $SKILL/engine/stills.js video/dist/video.html video/stills/hits.png --cues           # 0.25s after every sound cue
node $SKILL/engine/stills.js video/dist/video.html video/stills/s3.png 8.2 8.5 8.9 --keep # specific frames, full-size copies
```
Read every sheet yourself and run the senior review checklist in `references/motion-principles.md` §10. Check: text clipped/overlapping/too small (body ≥28px at 1080p, headlines 80-160px), content cramped or off-centre, dead frames (nothing moving for >1.5s while VO talks), a visual landing before or long after its word, inconsistent radii/strokes/fonts, anything that looks like a template. Fix and re-sheet at least twice. Also check the page printed no `PAGE ERRORS`.

### 7. Render, sound, master

```bash
# draft (fast): 30fps, 2 subframes
NODE_PATH=video/node_modules node $SKILL/engine/render.js video/dist/video.html video/out/draft.mp4 --fps 30 --sub 2
# final: 60fps, 4-subframe motion blur (≈4 frames/s/worker; a 30s film ≈ 15-25 min)
NODE_PATH=video/node_modules node $SKILL/engine/render.js video/dist/video.html video/out/video.mp4 --fps 60 --sub 4 --workers 4
python $SKILL/scripts/sfx.py mix video/out/video.cues.json video/audio/mix.wav --vo video/audio/vo.wav   # add --music synth|<file> ONLY if the user asked for music
python $SKILL/scripts/mux.py video/out/video.mp4 video/audio/mix.wav video/out/final.mp4
```
Render speed: plain scenes ≈4-9 frames/s with 4 workers; `backdrop-filter`, large `filter:blur()` layers and WebGL are much slower (≈1 frame/s). Add `--jpeg` for ~2x faster capture, use `--sub 2` for long videos, and prefer pre-blurred radial gradients over `filter:blur` on big orbs. `render.js` writes `<out>.cues.json` from the page's `M.cue` calls. `mux.py` masters to -14 LUFS / -1.5 dBTP. Run long renders in the background. For 9:16 / 1:1 pass `--ar 9x16` to stills and render (the page must lay itself out from `M.AR`, see engine-api).
After the draft: extract a few frames around transitions (`ffmpeg -ss T -i final.mp4 -vf fps=15,scale=480:-2,tile=4x2 -frames:v 1 burst.jpg`) and look at the motion, not just the stills.

### 8. Deliver

Also run `python $SKILL/scripts/captions.py video/audio/timings.json video/out` → `captions.srt`, `captions.vtt`, `chapters.txt` (always useful for YouTube/docs), and append this video to `video/.code-motion-history.json`.

In `video/out/`: `final.mp4` (+ other aspect ratios), `draft.mp4`, contact sheet, and a short `NOTES.md`: duration, scenes with timings, voice/provider used, what is illustrative, how to edit (change `script.json` → voice.py → build → render). The source (`src/`, `script.json`) is the editable master; say so.

## Defaults when the user has no brand

- 1920×1080, 60fps final; dark canvas `#0d0e12`, ink `#F3F1EC`, muted `#8b8f98`, one accent (`#FF5A1F`); Geist for UI/headlines, Geist Mono for code, Anton for slams, Caveat for handwriting, Instrument Serif for editorial. Only Geist/Geist Mono/Anton/Caveat/Instrument Serif are bundled (inlined at build); anything else needs a local font file in `assets/` and an `@font-face` in the fragment.
- Springs with at most a small overshoot; content enters after its container starts moving and leaves before the next move; subtle camera push inside every scene; vignette.
- **Banned**: bouncy cartoon easing, rainbow gradients on UI, mixed icon stroke weights, stock-template "slide in from left" on everything, walls of text, dead air, fake metrics, a watermark/progress bar nobody asked for.

## Gotchas

- Everything visual must derive from `t`. No `setTimeout`, CSS `transition`/`animation`, `Math.random()` (use `M.rand(seed)`), `Date.now()`, or state that depends on the previous frame; otherwise renders flicker and subframes smear wrongly.
- `will-change`/`filter` on a camera-scaled parent makes text blurry; scale the world, not each text node.
- Set a font-size on anything `M.words` animates (it reads it for distance). Call `M.split` once at setup, never inside `draw`.
- `M.word(id, 'text')` throws if the word isn't in that line; that's on purpose: it means the script changed. Re-run voice.py and rebuild after any script edit.
- Three.js pages need `preserveDrawingBuffer:true` and `renderer.render()` inside `seek`; set `window.READY` to a promise if textures/models load async.
- WebGL in headless Chromium runs on SwiftShader (CPU): keep 3D scenes modest or render at `--sub 2`.
- If stills/render say "page never called M.video", the page has a JS error: the message lists it; or open the preview and check the browser console.
- Elements that change width (button → check) must grow/shrink around a fixed centre (`left = x0 + (w0 - w)/2`), or they visibly jump when the state flips; effects anchored to them (rings, glows) must use that same centre.
- `stills.js` prints `Fontconfig error` on Windows from ffmpeg's drawtext; harmless.
