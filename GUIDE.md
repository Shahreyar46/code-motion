# Code Motion: User Guide

Everything you need to make professional videos with Claude Code: installation, every command, how a video gets made, how to get the best results, voice and sound, content rules, editing, and troubleshooting.

## Contents
1. What Code Motion does
2. Requirements
3. Install
4. First-time setup in a project
5. Commands (which one to use)
6. Your first video, step by step
7. What happens during a video (the workflow)
8. Choosing style, effects and pace
9. Fresh formats every time
10. Voice
11. Sound effects and music
12. Content rules
13. Tutorial / docs videos
14. Vertical videos (Reels, TikTok, Shorts)
15. Editing a video after it's made
16. Render times and quality
17. Getting the best results
18. Output files
19. Troubleshooting
20. FAQ

---

## 1. What Code Motion does

You describe a video; Claude writes it as code (HTML + JavaScript), renders every frame in a headless browser with real motion blur, records a natural male voiceover, places sound effects on every movement, and delivers an MP4. Because the whole video is code, any detail can be changed and re-rendered, and the same project can produce 16:9, 9:16 and 1:1 versions.

It was built from frame-by-frame studies of professional SaaS launch, demo, tutorial and product videos and 280 viral AI-made motion videos, so it follows their typography, transitions, camera moves and pacing.

## 2. Requirements

| Need | Why | Install |
|---|---|---|
| Claude Code | runs the plugin | https://claude.com/claude-code |
| Node.js 18+ | renders frames (Playwright) | https://nodejs.org |
| Python 3.8+ | voice, sound, mastering | https://python.org |
| ffmpeg | encodes video and audio | Windows `winget install Gyan.FFmpeg` · macOS `brew install ffmpeg` · Linux `sudo apt install ffmpeg` |
| Git Bash (Windows only) | runs the setup script | comes with Git for Windows |
| Internet | free voice (edge-tts), optional premium voices, optional photo search | |

Claude.ai chat is not supported: it can't install a browser and ffmpeg to render.

## 3. Install

In Claude Code:

```
/plugin marketplace add Shahreyar46/code-motion
/plugin install code-motion@code-motion
```

Restart Claude Code (or run `/reload-plugins`). Type `/code-motion:` to see the commands.

**Turn on auto-update (recommended):** `/plugin` → **Marketplaces** → **code-motion** → enable **auto-update**. New releases then install automatically when Claude Code starts. Manual alternative: `/plugin marketplace update code-motion`, then `/reload-plugins`. What changed: `CHANGELOG.md` / GitHub Releases.

## 4. First-time setup in a project

Open Claude Code in the project you want to make videos for (your app, plugin or website repo is ideal: Claude reads it for real copy, colours and logo), then run:

```
/code-motion:setup
```

This creates a `video/` folder and installs Playwright + Chromium, numpy and edge-tts into it (about 200 MB, once per project). For 3D scenes: `/code-motion:setup ./video --three`.

```
video/
├── src/      your video page(s) + script.json (the editable source)
├── audio/    voice (vo.wav), timings, final mix
├── assets/   your logo, screenshots, brand files ← put them here
├── stills/   contact sheets Claude reviews
├── dist/     built pages (preview these in a browser)
└── out/      final videos, captions, notes
```

## 5. Commands (which one to use)

| Command | Use it for | Length |
|---|---|---|
| `/code-motion:promo` | Launch video, ad, hype promo with one big promise | 15-35 s |
| `/code-motion:overview` | Product overview: what it is, who it's for, feature tour, how it works, CTA | 45-90 s |
| `/code-motion:demo` | Product demo with feature chapters and proof | 60-120 s |
| `/code-motion:tutorial` | Step-by-step tutorial / docs / how-to for one feature (+ captions, chapters, written guide) | 60-180 s |
| `/code-motion:explainer` | Explain a concept, or "what's new" feature updates | 45-90 s |
| `/code-motion:reel` | Vertical 9:16 reel/short for social | 20-40 s |
| `/code-motion:ui-loop` | Dribbble-style looping UI animation | 8-15 s |
| `/code-motion:logo` | Logo reveal, intro, outro | 3-8 s |
| `/code-motion:scene-3d` | 3D cinematic scene (Three.js) | 10-60 s |
| `/code-motion:video` | Anything else; picks the right type for you | |
| `/code-motion:setup` | First-time setup + voice check | |

**Flags** you can add to any video command:
- `--auto`: skip the style/effects questions and let Claude decide.
- `--music`: add background music (off by default; see section 11).

You can also ask in plain words ("make a tutorial video showing how to export reports in my plugin"); the skill triggers by itself.

## 6. Your first video, step by step

1. Put your logo (SVG is best), a few screenshots and your brand colours in `video/assets/`.
2. Run, for example:
   ```
   /code-motion:overview My plugin "OrderFlow" (repo is this folder, site https://orderflow.example). Audience: WooCommerce store owners. CTA: Get it free on WordPress.org
   ```
3. Answer the short questions (product facts, then the style menu, or pick **Let AI decide**).
4. Approve or edit the **script** (each line becomes one moment in the video).
5. Approve or edit the **storyboard** table: line, time, visual, motion, sound.
6. Claude builds the video, reviews contact sheets of stills, fixes problems, renders a draft, then the final.
7. Watch `video/out/final.mp4`. Ask for changes ("slower at the start", "make the logo bigger"); Claude edits and re-renders.

## 7. What happens during a video (the workflow)

1. **Brief**: one round of questions. Anything you already said is skipped.
2. **Truth**: Claude reads your real product (repo, website, docs, brand files). It never invents numbers, customers, quotes or features.
3. **Script and voice**: narration is written line by line, then voiced. Every word gets a timestamp, so animation lands exactly on spoken words.
4. **Storyboard**: shown for your approval before any animation code.
5. **Build**: the video page is written from templates and the engine.
6. **Quality check**: contact sheets of stills at every second and every sound hit; Claude looks for clipped or overlapping text, small type, dead moments and late visuals, and fixes them (at least two rounds).
7. **Render**: draft (fast) then final (60 fps, motion blur).
8. **Sound and master**: effects mixed under the voice; loudness mastered to −14 LUFS (YouTube/social standard).
9. **Deliver**: MP4, captions, chapters, notes, editable source.

Preview any time before rendering: Claude can start a local preview server and give you a link; press space to play/pause, arrows to step.

## 8. Choosing style, effects and pace

Unless you pass `--auto`, Claude asks:

1. **Style**: *Let AI decide (recommended)* or one of three styles suited to the video type, for example:
   - Dark Product Film (premium, Apple/Stripe-like)
   - Light Glass SaaS (friendly, airy, glass cards)
   - Dark ↔ Light Chapters (problem/solution)
   - AI Neon Glow (gradients, glowing edges)
   - Google Playful (rounded, colourful)
   - Paper & Marker (hand-drawn explainer)
   - Halftone / Acid Tech (loud, bold)
   - Editorial Serif (elegant, brand stories)
   - One-Shape UI Motion (Dribbble loops)
   - 3D Cinematic
2. **Signature effects** (any): kinetic typography · 3D UI and camera · seamless morphs (no cuts) · glow and celebration · or type your own (hand-drawn arrows, counters, glitch…).
3. **Pace** (promos, reels, explainers): calm and premium · punchy · let AI decide.

Your brand colours and fonts are always applied on top of the style.

## 9. Fresh formats every time

Videos of the same type don't repeat. Each type has several story formats; a promo might be *Problem → Meet → Proof*, a *One-object journey* with no cuts, a *Countdown*, a *Before/After split*, a *Question chain*, a *Manifesto* or a *Zoom journey*. Claude keeps a small history (`video/.code-motion-history.json`) and picks a different format, opening and transition style from your last videos. Say "same format as last time" when you want a consistent series.

## 10. Voice

- Male narration only, natural and warm by default.
- **Free (default)**: Microsoft neural voices through edge-tts, e.g. *Andrew* (warm), *Brian* (casual), *Guy* (newscast), *Christopher* (authoritative), *Ryan* (British). Internet required.
- **Premium (bring your own key)**: Gemini TTS (most natural, follows direction like "calm, confident") or ElevenLabs. Add your key to Claude Code settings and restart:
  ```json
  // ~/.claude/settings.json  (merge into your existing "env")
  { "env": { "GEMINI_API_KEY": "your-key" } }
  ```
  Get a Gemini key at aistudio.google.com → *Get API key*. Never paste keys into the chat.
- **Offline**: the Windows built-in male voice (robotic; last resort).
- Ask for a different voice or energy: "use a British voice", "more energetic", "slower".
- Mispronounced name? Claude spells it phonetically in the narration only; the on-screen text stays correct.
- Cloud voice providers receive the narration text.

## 11. Sound effects and music

- **Sound effects**: 27 effects generated in code, so no licences are involved: whoosh, swish, pop, click, keys, tick, impact, riser, chime, success, ding, shimmer, glitch, pen, and more. Every movement that causes a sound gets one, timed to the frame, panned with the motion and kept under the voice.
- **Music is off by default.** To add it:
  - `--music` in the command (e.g. `/code-motion:promo --music …`) → a soft generated ambient bed, or
  - give your own track: "use video/assets/track.mp3 as background music" (you must own the rights).
  Music sits about 20 dB under the voice and dips further while words are spoken.

## 12. Content rules

Code Motion follows these rules on every video:
- Male voice only.
- No images of women or girls (photos, illustrations, avatars or icons). People are shown as initials, icons or abstract shapes.
- No haram products or themes: alcohol, pork, gambling, tobacco/vaping, drugs, interest-based lending promotion, nudity or suggestive content. Videos for such products are declined.
- Imagery favours **nature and animals** (landscapes, sky, sea, forests, plants, birds, horses…), your product's real UI and visuals drawn in code.
- External photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated images. Random Google Images results are not used because most are copyrighted. Every external image is listed in `NOTES.md` with source and licence.
- No invented numbers, customers, testimonials or prices.

## 13. Tutorial / docs videos

`/code-motion:tutorial` makes a step-by-step guide for one feature:
- Title → result shown first → the full screen once for orientation → each step: step chip (1/5), caption, zoom to the exact control, one cursor action, result → recap and docs link.
- Every label matches your real UI exactly; Claude asks if a step is unclear.
- Narration is slower and instructional ("Open **Settings**, then **Integrations**").
- Extra deliverables in `video/out/`:
  - `captions.srt` / `captions.vtt`: subtitles from the exact script.
  - `chapters.txt`: timestamps to paste into a YouTube description.
  - `steps.md`: the same tutorial as a written docs page with numbered steps and timestamps.
- Long features are split into a short series (one task per video).

## 14. Vertical videos (Reels, TikTok, Shorts)

`/code-motion:reel` builds 1080×1920 with safe zones (nothing important in the bottom 12% where the app buttons sit), big captions for muted viewing, a hook in the first 2 seconds and a CTA held for 4+ seconds. Any other video can also get a vertical version: ask for "a 9:16 version too".

## 15. Editing a video after it's made

Just ask in the same project:
- Text or narration: "change the tagline to …" (re-voices only the changed lines).
- Timing: "hold the logo longer", "slower in the middle".
- Look: "make it lighter", "bigger headline", "use our green #1FA463".
- Format: "make a 15-second cut", "make a square version".

The editable master is `video/src/` + `video/src/script.json`. Developers can edit the HTML directly; every frame is `seek(t)`.

## 16. Render times and quality

- Draft (30 fps, light blur): about 1-2 minutes for 20 s.
- Final (60 fps, 4-sample motion blur): about 4-8 minutes for 20-30 s on a typical laptop; heavy blur/glass effects and 3D take longer.
- Output: H.264 MP4, BT.709 colour, AAC 256 kbps, −14 LUFS.

## 17. Getting the best results

- Use a strong model with high effort (e.g. Opus on high or max).
- Run Claude Code inside your product's repo, or give the website/docs URL: real copy and real UI beat generic visuals.
- Provide an SVG logo and brand colours.
- Share a reference video ("make it like this one"): Claude breaks it down frame by frame and matches the style.
- Approve the script carefully; the script drives every visual.
- Review the draft and give concrete notes. Two rounds of notes usually gets a polished result.
- Keep one idea per line in the script; short lines make better motion.

## 18. Output files

| File | What |
|---|---|
| `video/out/final.mp4` | the video |
| `video/out/draft.mp4` | quick draft render |
| `video/out/captions.srt`, `.vtt` | subtitles |
| `video/out/chapters.txt` | YouTube chapters |
| `video/out/steps.md` | written guide (tutorials) |
| `video/out/NOTES.md` | scenes and timings, voice used, image sources, what is illustrative |
| `video/stills/*.png` | contact sheets used for quality checks |
| `video/src/` | the editable source |

## 19. Troubleshooting

| Problem | Fix |
|---|---|
| `Missing: ffmpeg` / `node` / `python` during setup | install it (section 2), reopen the terminal, run `/code-motion:setup` again |
| Windows: `bash` not found | install Git for Windows; run Claude Code from Git Bash or make sure `bash` is on PATH |
| `Python was not found` (Windows Store alias) | install Python from python.org, or disable the alias in *Settings → Apps → App execution aliases* |
| Voice uses edge instead of Gemini | key not visible: check `env` in `~/.claude/settings.json`, restart Claude Code, run `/code-motion:setup` to re-check |
| `Refused: … not a male voice` | choose a male voice (`python voice.py --list`) |
| `page never called M.video` | the video page has a JavaScript error; the message names it. Ask Claude to fix it |
| Render very slow | normal for glass/blur/3D; ask for `--sub 2` drafts, or fewer blur layers |
| Text looks blurry | ask Claude to remove `will-change`/blur filters from scaled parents |
| Audio too quiet/loud vs effects | "make effects quieter" (Claude lowers `--sfx-db`) |
| Plugin commands missing | `/reload-plugins`, or `/plugin` → check *code-motion* is enabled |

## 20. FAQ

**Does it need a GPU?** No. It renders with the CPU in a headless browser.

**Can I use my own screenshots?** Yes: put them in `video/assets/`. For crisp results Claude often rebuilds the UI in HTML from them.

**Can it make videos in other languages?** Yes for on-screen text; for voice, pick a male voice in that language (edge-tts has many; Gemini handles many languages).

**Can I use the videos commercially?** Yes. Fonts are open licence, sound effects are generated, and external images come only from free-licence sources (check `NOTES.md`).

**Is my data sent anywhere?** Only the narration text to the voice provider you use, and web searches if Claude looks for photos. Rendering is local.
