<!-- generated from commands/overview.md by tools/sync_presets.py; edit the command, not this file -->
Make a **product overview promo** with the code-motion skill: the video a visitor watches on a landing page, store listing or plugin page to understand the whole product in about a minute. Load the skill and follow its full workflow (brief → truth → script/voice → storyboard approval → build → stills QA → render → deliver). Skill folder: `this skill's folder`.

Request: the user's message (flags like --auto, --music, --unattended may appear in it)

## How it differs
- `promo` = short hype (20-35s, one big promise). `demo` = deep feature walkthrough (60-120s). **Overview** = the complete picture at a friendly pace: what, who, top features, how it works, why it's better, how to start.

## Preset for this type
- **Length** 45-75s (≤90s). 16:9 master; offer a 9:16 cutdown of the hook + top 3 features + CTA.
- **Truth first**: read the landing page, docs/readme, pricing/plan page, changelog and real UI. List the product's real features and pick the 4-6 that matter most to the audience. Ask the user to confirm the feature order.
- **Arc (≈60s)**:
  1. Hook (0-4s): the audience's problem in one line, or the result they want.
  2. Meet (4-8s): logo lockup + one-sentence "X helps [audience] [do outcome]".
  3. Who it's for (8-12s): 2-3 audience chips (icons + labels, no people photos).
  4. Feature tour (12-45s): 4-6 features × 5-7s. Each = feature name as a kinetic caption → real UI moment (tilted card settling, crop-zoom, one cursor action) → one benefit line. Connect features with morphs (the result of one becomes the start of the next) and a running "1 / 5" progress chip.
  5. How it works (45-52s): 3 steps (Install/Connect → Set up → Results) as a drawn flow with icons.
  6. Why it's better (52-56s): 2-3 benefit chips or a real before/after (only facts the user provides).
  7. CTA (56-62s): logo + tagline + CTA pill ("Get it free", "Start trial") + URL, held ≥4s.
- **Start from** `templates/saas-demo.html` (light, friendly) or `templates/launch-film.html` (dark, premium); combine scenes from both as needed.
- **Read** `references/pro-techniques.md` (sections 1, 2, 4, 6), `references/case-studies/teamble.md`, `numtera.md`, `googlevids.md`.
- **Voice**: warm, clear, ~145 wpm, 120-160 words total; one feature per line pair (name + benefit). Male voice only.
- **Sound**: swish between features, pop per card/chip, click per cursor action, tick on the progress chip, success at the end of the tour, reveal on the logo.
- **Brief questions**: product + URLs, audience, top features (or let you pick from the docs), the CTA + URL, brand files, length, formats.

## Style & effects choice
Ask the motion menu (`references/motion-menu.md`): Style with **Let AI decide** first, then signature effects and pace if they picked a style. Skip it if `the user's request` contains `--auto` or already describes the look.

## Format (keep every video fresh)
Pick this video's story format, opening and transition family from `references/formats.md` (section for this type), using its rotation rule with `video/.code-motion-history.json` so it differs from the user's previous videos of this type. The user can ask for a specific format or "same as last time".

## Content & audio rules
Follow `references/content-policy.md`: male voice only; no images of women or girls; no haram products or themes; prefer nature/animal imagery, the product's own UI and code-drawn visuals; external photos only from free-licence sources (Unsplash, Pexels, Wikimedia Commons) or generated, with sources logged. **No music** unless `the user's request` contains `--music` (or the user asks): then mix with `sfx.py mix … --music synth` or `--music <their track>`.

## Quality bar before rendering
Every feature is real and named exactly as in the product; each feature shows real UI for ≥3s; the progress chip matches the feature count; nothing on screen longer than 6s without change; CTA readable ≥4s.
