# Code Motion: AI video studio for Claude Code

Make professional motion-graphics videos by asking Claude: product promos, launch films, tutorial and docs videos, product demos, explainers, vertical reels, UI animation loops, logo reveals and 3D scenes. Every frame is code (HTML/JS), rendered frame by frame with real motion blur. A natural voiceover drives the timing, and synthesised sound effects land on every move. No video editor, no stock assets, no music licences.

## Install

Pick **one** way. All need [Claude Code](https://claude.com/claude-code).

**A. Inside Claude Code** (type in the chat box):
```
/plugin marketplace add Shahreyar46/code-motion
/plugin install code-motion@code-motion
```

**B. From a terminal (CLI):**
```
claude plugin marketplace add Shahreyar46/code-motion
claude plugin install code-motion@code-motion
```

Then restart Claude Code (or run `/reload-plugins`) and type `/code-motion:` to see the commands.

### Turn on auto-update (recommended)
Auto-update is **off by default** for every marketplace that isn't Anthropic's own; plugin authors can't change that, so each user switches it on once:
- **In Claude Code:** `/plugin` → **Marketplaces** tab → **code-motion** → **Enable auto-update**.
- **Or in settings** (`~/.claude/settings.json`, merge with what's there). This also registers the marketplace, so then just run the install command:
  ```json
  {
    "extraKnownMarketplaces": {
      "code-motion": {
        "source": { "source": "github", "repo": "Shahreyar46/code-motion" },
        "autoUpdate": true
      }
    }
  }
  ```
With auto-update on, Claude Code checks for new releases in the background a few minutes into a session; the new version loads on the next start (or `/reload-plugins`).
Manual update any time: `/plugin marketplace update code-motion` (CLI: `claude plugin marketplace update code-motion`).
Note: `DISABLE_AUTOUPDATER=1` or `DISABLE_UPDATES=1` in your environment also stops plugin updates unless you set `FORCE_AUTOUPDATE_PLUGINS=1`.

### Uninstall
`/plugin uninstall code-motion@code-motion` (CLI: `claude plugin uninstall code-motion@code-motion`).

## First-time setup in a project

In the project where you want to make videos:

```
/code-motion:setup
```

This installs Playwright + Chromium, numpy and edge-tts into a `video/` folder and checks your voice options. Add `--three` for 3D scenes: `/code-motion:setup ./video --three`.

**Requirements:** Claude Code, Node.js 18+, Python 3.8+, ffmpeg on PATH. Windows users run the setup through Git Bash (included with Git for Windows).
- ffmpeg: `winget install Gyan.FFmpeg` (Windows), `brew install ffmpeg` (macOS), `sudo apt install ffmpeg` (Debian/Ubuntu).

## Make a video

| Command | For |
|---|---|
| `/code-motion:promo` | Product promo, launch film, ad (15-45s) |
| `/code-motion:overview` | Product overview: what it is, feature tour, how it works, CTA (45-90s) |
| `/code-motion:tutorial` | Step-by-step tutorial / docs video for a feature, plus captions, chapters and a written guide (60-180s) |
| `/code-motion:demo` | Product demo with feature chapters (60-120s) |
| `/code-motion:explainer` | Concept explainer or "what's new" (30-120s) |
| `/code-motion:reel` | Vertical reel/short for TikTok, Reels, Shorts (9:16) |
| `/code-motion:ui-loop` | Dribbble-style one-shape UI animation loop |
| `/code-motion:logo` | Logo reveal, intro, outro |
| `/code-motion:scene-3d` | 3D cinematic scene (Three.js) |
| `/code-motion:video` | Anything else; it picks the type for you |

Flags: `--auto` skips the style questions (AI decides) · `--music` adds background music (off by default).

Example: `/code-motion:promo 30s launch video for my app, landing page https://example.com, logo in ./assets/logo.svg`

Claude asks a few questions, reads your real product (repo, site, brand colours, logo), writes the narration, shows a storyboard for approval, builds the animation, checks contact sheets of stills and fixes problems, then renders. You get `video/out/final.mp4` plus the editable source.

You can also just ask in plain words ("make a tutorial video showing how to connect Stripe in my plugin"); the skill triggers on its own.

**Full documentation: [GUIDE.md](GUIDE.md)**: workflow, styles, formats, voice, sound, content rules, tutorials, editing, troubleshooting.

## Content rules
Male voice only · no music unless you ask (`--music`) · no images of women or girls · no haram products or themes · nature and animal imagery, your real UI and code-drawn visuals · free-licence or generated images only, with sources logged · no invented numbers or testimonials.

## Voice (bring your own key, optional)

Works out of the box with the free, natural edge-tts voice (needs internet). For the most natural voice, connect your own key by adding it to `~/.claude/settings.json` and restarting Claude Code:

```json
{ "env": { "GEMINI_API_KEY": "your-key" } }
```

or `ELEVENLABS_API_KEY`. Male voices only. Offline fallback on Windows: the built-in male system voice. Cloud voice providers receive the narration text. Keys are read from your environment only; never paste them into chat.

## Updating

See **Turn on auto-update** above. What changed: [CHANGELOG.md](CHANGELOG.md) / GitHub Releases.

## Tips for the best results
- Use a strong model with high effort (e.g. Opus on high or max).
- Put your real logo (SVG best), screenshots and brand colours in `video/assets/`, and point Claude at your repo or landing page.
- Share a reference video ("like this") and Claude will break it down and match its style.
- Review the draft render and give notes ("slower here", "less like a slideshow"); quality improves each round.
- Render time: roughly 5-10 minutes for a 30s video at 60fps with motion blur.

## What's inside
- `skills/code-motion/`: the skill: engine (`motion.js`, build, render, stills, preview server), scripts (voice, sound effects, mastering), references (pro techniques, styles, video types, sound design, voice, prompt patterns, case studies) and templates.
- `commands/`: the type presets above.

Licence: MIT. Bundled fonts: SIL OFL 1.1. See `skills/code-motion/THIRD_PARTY.md`.

## For maintainers: releasing
```
./release.sh 1.1.0 "Added X; fixed Y"
```
Bumps the version in `.claude-plugin/plugin.json`, adds a CHANGELOG entry, validates, commits, tags `v1.1.0` and pushes. The GitHub Action checks the tag matches the version and publishes the Release. Pushing to `main` without a new version does **not** update users: Claude Code updates by version number.
