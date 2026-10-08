---
description: "One-time setup for code-motion in this project (Playwright, Chromium, numpy, edge-tts, optional Three.js) and a voice check"
argument-hint: "[folder, default ./video] [--three]"
---
Set up code-motion video tooling for this project.

1. Run: `bash "${CLAUDE_PLUGIN_ROOT}/skills/code-motion/scripts/setup.sh" $ARGUMENTS`
   (Windows: run it through Git Bash. If node, python or ffmpeg is missing, tell the user the exact install command for their OS from the script's message and stop.)
2. Run: `python "${CLAUDE_PLUGIN_ROOT}/skills/code-motion/scripts/voice.py" --list` and report which voice providers are available.
   - Only `edge`/`sapi` available: say the free natural voice (edge-tts) will be used, and that they can connect their own premium voice by adding `GEMINI_API_KEY` or `ELEVENLABS_API_KEY` to the `env` block of their Claude Code settings (`~/.claude/settings.json`), then restarting. Never ask them to paste a key into the chat.
3. Finish with the folder layout and the commands they can use next: `/code-motion:promo`, `/code-motion:overview`, `/code-motion:tutorial`, `/code-motion:demo`, `/code-motion:explainer`, `/code-motion:reel`, `/code-motion:ui-loop`, `/code-motion:logo`, `/code-motion:scene-3d`, or `/code-motion:video` for anything else.
