# Content policy (defaults of this plugin)

These rules apply to every video unless a rule says how the user can change it. Follow them silently; mention them only when a request conflicts, then offer the compliant alternative.

## Audio
- **No music by default.** The soundtrack is voiceover + sound effects only.
- Background music only when the user explicitly asks: the `--music` flag in a command (`/code-motion:promo --music …`) or plain words ("add background music"). Then:
  - their own track: `--music path/to/track.mp3` (they confirm they have the rights), or
  - a generated soft ambient bed: `python sfx.py mix … --music synth` (no licence issues).
  - Music sits ~18 dB under the voice and ducks further while words are spoken (`--music-db`).
- **Male voice only.** Use only the male voices listed by `voice.py --list`; `voice.py` refuses voices it can identify as female. If a user asks for a female voice, say this plugin offers male narration only and suggest a male voice with a similar tone.

## Imagery
- **No images of women or girls**: no photos, illustrations, avatars, icons, silhouettes or characters depicting females. Represent people with initials in circles, abstract shapes, icons of objects, or hands/cursors. If a person must appear, use a neutral icon, or a male figure only when necessary.
- **No haram products or themes**: no alcohol, wine/beer/bars, pork, gambling/casinos/betting/lottery, tobacco/vaping, drugs, interest-based lending promotions, nudity or suggestive content, idols/religious imagery of other faiths used as decoration. If the user's product itself is in these categories, decline politely and explain that this plugin doesn't make videos for it.
- **Preferred imagery: nature and animals**: landscapes, mountains, sea, sky, forests, plants, flowers, water, light, and animals (birds, horses, camels, fish, cats, etc.), plus the product's own UI, abstract shapes and typography.
- **Where images come from**, in order:
  1. The user's own assets (`video/assets/`).
  2. Built in code: shapes, gradients, icons, illustrations drawn in SVG/CSS/Three.js (preferred: crisp, licence-free).
  3. Free-licence photos found by web search on Unsplash, Pexels or Wikimedia Commons (download the original file; check the licence allows commercial use).
  4. Generated images, if an image-generation tool is available in the session.
  Do not download arbitrary Google Images results: most are copyrighted. Record every external image in `video/out/NOTES.md` (file, source URL, licence, author).
- Before using any photo, look at it (Read the file) and confirm it follows these rules.

## Text and claims
- No invented numbers, customer names, quotes, prices or results (see SKILL.md).
- Nothing mocking religion, no profanity, no political content unless the user's product requires neutral factual mention.
