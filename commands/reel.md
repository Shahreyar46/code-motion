---
description: "Vertical social reel / short (9:16, 15-45s) for TikTok, Reels, Shorts, LinkedIn: hook in 2s, captions, CTA"
argument-hint: "[--music] [--auto to skip style questions] [product or topic, platform, hook idea]"
---
Make a **vertical social reel** with the code-motion skill. Load the skill and follow its full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver). Skill folder: `${CLAUDE_PLUGIN_ROOT}/skills/code-motion`.

Request: $ARGUMENTS

## Preset for this type
- **Format** 1080×1920 (`W=1080,H=1920`, or build 16:9 and lay out from `M.AR` with `--ar 9x16`), 60fps, 20-40s.
- **Safe zones**: headline in the top 20%, hero in the middle, chips/CTA in the lower third, **bottom 12% empty** (platform buttons), 60px side margins. Headlines ≥64px, nothing under 22px.
- **Arc**: relatable hook in the first 2s (meme-style caption, bold question or pain shown in UI) → problem (dark) → hard cut + impact → product promise (light) → one-click demo → 3 benefit chips → payoff that calls back to the hook → CTA pill + URL held ≥4s.
- **On-screen text carries the message** (most people watch muted): every VO line also appears as a caption; captions measured in the real font and fitted to the safe zone.
- **Start from** `templates/saas-demo.html` and re-lay out vertically.
- **Read** `references/case-studies/plugin-reel-vertical.md` and `references/pro-techniques.md` section 8.
- **Voice**: energetic, ~160 wpm, short lines.
- **Sound**: denser hits than 16:9 (pop/click/swish every 0.5-1s during the demo), impact at the dark→light cut, reveal at the CTA.
- **Brief questions**: platform(s), product/topic, the hook angle, CTA + URL, brand files.

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `$ARGUMENTS` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `$ARGUMENTS` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar before rendering
Check stills with `--ar 9x16`: nothing important in the bottom 12% or under 60px from the sides; hook readable in the first frame that has text; one idea per 3-5s.
