<!-- generated from commands/setup.md by tools/sync_presets.py; edit the command, not this file -->
Set up code-motion video tooling for this project. Arguments: the user's request

1. Run: `bash "scripts/setup.sh" <folder> [--three]` (pass the folder/`--three` from the arguments; not `--schedule`).
   (Windows: run it through Git Bash. If node, python or ffmpeg is still missing, tell the user the exact install command for their OS from the script's message and stop.)
2. Run: `python "scripts/doctor.py"` and report the result (READY / what failed, render-time estimate).
3. Voice: if no premium key is set, say the free natural male voice (edge-tts) will be used and that they can connect their own Gemini or ElevenLabs key by adding `GEMINI_API_KEY` / `ELEVENLABS_API_KEY` to the `env` block of `~/.claude/settings.json` (on Claude Code on the web: the environment's variables/secrets settings). Never ask them to paste a key into the chat.
4. **Make the plugin load everywhere for this project** (Desktop app, VS Code, Claude Code on the web, teammates): offer to add this to the project's `.claude/settings.json` (merge with existing content, don't overwrite):
   ```json
   {
     "extraKnownMarketplaces": {
       "code-motion": { "source": { "source": "github", "repo": "Shahreyar46/code-motion" } }
     },
     "enabledPlugins": { "code-motion@code-motion": true }
   }
   ```
   Then commit `.claude/settings.json` and `video/.gitignore` (never `video/node_modules`).

## If `--schedule` is in the arguments (scheduled / machine-off videos)
5. Ask (one AskUserQuestion round, plus free text where needed) and write **`video/brief.md`**: product name + one-liner, audience, URLs / repo paths / docs to read, CTA + URL, brand (colours, fonts, logo path in `video/assets/`), voice + energy, formats (16:9 and/or 9:16), which video types the schedule may make, always/never-say rules, music yes/no (default no).
6. Write **`video/queue.md`** with 3-5 suggested upcoming videos (from the product's features/changelog) as `- [ ] type: topic` lines; let the user edit them.
7. Commit and push `video/brief.md`, `video/queue.md`, `.claude/settings.json`.
8. Tell the user how to schedule (their machine can be off):
   - **Claude Code on the web** (claude.ai/code → this repo's project) → **Scheduled** → new schedule → this repo/environment → prompt `/code-motion:video --unattended` → time (e.g. every Monday 09:00).
   - or in any Claude Code session: "schedule `/code-motion:video --unattended` every Monday at 9am for this repo" (routines, where available).
   - Each run takes the next queue item, makes a different-format video, and pushes it on a `videos/<date>-<slug>` branch (plus a PR when possible). Add items to `video/queue.md` any time.
9. Offer a **test run now**: `/code-motion:video --unattended` on the first queue item, so they see one result before trusting the schedule.

Finish with the commands they can use next: `/code-motion:promo`, `/code-motion:overview`, `/code-motion:tutorial`, `/code-motion:demo`, `/code-motion:explainer`, `/code-motion:reel`, `/code-motion:ui-loop`, `/code-motion:logo`, `/code-motion:scene-3d`, or `/code-motion:video` for anything else.
