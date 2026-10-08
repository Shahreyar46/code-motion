# Voiceover script + voice

## Writing for the ear (and for animation)

- **One line = one visual beat.** Each `lines[]` entry becomes one scene or one state change. 4-12 words per line.
- ~150 words/min for promos, ~140 for tutorials. A 30 s promo ≈ 65-75 words.
- Put the **key word last** in the line; that's where the hero visual lands and where the voice naturally stresses.
- Short sentences, contractions, second person ("you"). No jargon the viewer can't see on screen.
- Fragments are good in promos: "No timeline. No keyframes. No editor."
- Numbers: write them as spoken ("forty-eight thousand" or "48,000" both fine for edge/Gemini; avoid symbols like "%", write "percent").
- Product names: spell phonetically if TTS mangles them (`"Numtera"` → `"Num-terra"` in the VO text only; keep the visual correct).
- `pause` after a line = beat for a visual payoff (0.5-0.8 s). Default `gap` 0.35-0.45 s.
- Never invent claims. The script uses the same truth sources as the visuals.

## script.json

```json
{
  "voice": {"provider": "auto", "gemini": "Charon", "edge": "en-US-AndrewNeural", "rate": "-4%",
            "style": "Read like a calm, confident product-film narrator. Warm, natural, unhurried."},
  "lead_in": 0.6, "gap": 0.4,
  "lines": [
    {"id": "hook", "text": "Your orders page shouldn't take a coffee break.", "pause": 0.5},
    {"id": "meet", "text": "Meet YourPlugin."}
  ]
}
```
IDs are what the page anchors to (`M.line('meet').start`, `M.word('meet','YourPlugin')`), so keep them stable when editing text.

## Choosing the voice (male, natural)

| Provider | Needs | Voice suggestions | Notes |
|---|---|---|---|
| Gemini TTS | `GEMINI_API_KEY` | **Charon** (informative, default), Orus (firm), Iapetus (clear), Algenib (gravelly), Fenrir (excitable), Puck (upbeat). Some Gemini voices can sound light/higher; the pitch gate refuses them, so pick a deeper one | Most natural; obeys `style` direction. Word times are estimated (±0.15 s). Model via `CM_GEMINI_TTS_MODEL`. |
| ElevenLabs | `ELEVENLABS_API_KEY` | Adam `pNInz6obpgDQGcFmaJgB`, Josh, Antoni | Very natural, real timestamps, paid. |
| edge-tts | internet | **en-US-AndrewNeural** (warm, default), BrianNeural (casual), GuyNeural (news), ChristopherNeural (authoritative), en-GB-RyanNeural | Free, natural, real word timestamps. `rate` like `"-4%"`. |
| SAPI | Windows | Microsoft David | Offline, robotic; last resort. |

Energy by type: launch/promo = confident, slight smile, `rate -4%..+0%`; tutorial = friendly, slower `-8%`; AI/brand film = calm, intimate `-6%`.
Cloud providers receive the script text; say so if the content is confidential, and offer SAPI.

Premium voices use the **user's own** API key; the skill ships with none and works without one (edge-tts). To connect: get a Gemini API key from Google AI Studio (aistudio.google.com → Get API key) or an ElevenLabs key. Then either:
- Claude Code settings (`~/.claude/settings.json`, merge into any existing `env`), so every session has it:
  ```json
  { "env": { "GEMINI_API_KEY": "your-key", "CM_GEMINI_TTS_MODEL": "gemini-2.5-flash-preview-tts" } }
  ```
- or the OS: `setx GEMINI_API_KEY "..."` (Windows, new terminal) / `export GEMINI_API_KEY=...`.
Never paste keys into chat or into project files. A Gemini MCP connector does NOT give voice.py a key; it needs the env var. Check with `python scripts/voice.py --list` (first line should list `gemini`). If Google renames the TTS model, set `CM_GEMINI_TTS_MODEL` to the current one; on any Gemini error voice.py falls back to edge-tts and says why.

## After generating
Read the printed timeline. If a line is longer than its visual needs, shorten the words (don't speed the voice). Listen to `audio/vo.wav` for mispronunciations; fix by phonetic spelling and re-run (only changed lines regenerate).
