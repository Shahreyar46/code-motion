# Sound design (no music by default): think like a sound engineer

Music is added only when the user asks (`--music synth` for a generated ambient bed, or `--music their-track.mp3`), mixed ~20 dB under the voice and ducked under speech. Everything below is about effects.

The voice is the lead instrument. Sound effects make motion feel physical; silence between them is part of the design. `scripts/sfx.py` synthesises every sound (no samples, no licences), humanises each instance (±3% pitch, ±1.2 dB), pans, glues the bus and ducks it under the voice.

## Rules

1. **Every visible cause gets a sound; nothing else does.** A card lands → pop. A camera move → whoosh sized to the move (`d` = move duration). Typing → keys. No sound for things that only fade.
2. **Sync to the visual hit, not the start.** Pops/thuds at the frame the element lands (≈ spring t0 + 0.05 s). Whooshes start ~0.1-0.2 s before the movement peaks. `riser`/`suck` use `t` = the hit (they're anchored at their end).
3. **Hierarchy by gain**: impact/reveal 0.8-1.0 · whoosh/thud 0.5-0.7 · pop/click 0.4-0.6 · tick/key/hover 0.15-0.35. Most cues should be quiet; impacts need headroom.
4. **Pan with motion**: enters from left → `pan:-0.4`; cursor on right side → `pan:0.3`. Keep VO-critical moments near centre.
5. **Don't stack on the voice's key word** with anything louder than a pop; the mixer ducks SFX ~5 dB under speech, but avoid impacts mid-sentence unless it's the punchline word.
6. **Density**: 2-5 cues per second during busy UI moments, 0-1 during calm explanation. Long typing: one `key` every 2 characters, gain 0.2.
7. **Leave air**: after an impact, ~0.5 s of nothing. Before the logo: riser (0.9-1.6 s) → `reveal`.
8. **Repeat sounds are fine** (that's a sound palette); the humaniser varies them.

## Mapping (motion → sound)

| Motion | Sound | Notes |
|---|---|---|
| Scene transition / camera push / fly-through | `whoosh` (`d` = duration) | alternate pan ±0.3 |
| Quick text slide / wipe | `swish` | |
| Tab indicator / card shift / list scroll | `swipe` | |
| Zoom-in collapse to a point | `suck` (t = arrival) | |
| Card / element lands | `pop` | small things: `bubble` |
| Cursor press | `click` | arrive on target: `hover` (very soft) |
| Toggle / snap into slot | `snap` | |
| Typing | `key` per 2 chars | |
| Row/list item appears, step tick | `tick` | |
| Counter running | `roll` (`d` = count duration) | |
| Title slam / big cut word | `impact` or `thud` | `shake` visually at the same t |
| Low weight under reveal | `sub` | |
| Build tension | `riser` (t = hit) | pair with `impact` |
| Success / check / done | `success` | |
| Notification / toast | `ding` | |
| Error / rejected | `error` | |
| AI magic / sparkle / glint | `shimmer` | |
| Highlight / tagline | `chime` | |
| Glitch transition | `glitch` | |
| Marker / handwriting draws | `pen` (`d` = draw time) | |
| Paper / sticky note / cutout | `paper`, `stamp` | |
| Screenshot / capture | `shutter` | |
| Logo / end card | `reveal` (+ `riser` into it) | |

## Workflow

```js
// in the page, next to the motion:
M.cue(tLand, 'pop', {g:0.5, pan:-0.3});
M.cue(tMove, 'whoosh', {g:0.6, d:0.6});
M.cue(tHit, 'riser', {g:0.35, d:1.2}); M.cue(tHit, 'impact', {g:0.8});
```
`render.js` exports them to `<out>.cues.json`; `sfx.py mix` builds `mix.wav`. Audition the palette: `python sfx.py audition out/sfx` → `reel.wav`. Mix knobs: `--sfx-db` (default −8: overall SFX level vs voice), `--duck-db` (default 5), `--air` (faint room tone so gaps don't sound dead; use for slow explainers).
Check after mux: `final.mp4` should read about −14 LUFS; if SFX feel loud relative to the voice, lower `--sfx-db` to −11, not individual cues.
