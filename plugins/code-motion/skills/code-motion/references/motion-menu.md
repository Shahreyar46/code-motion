# Motion menu: choices to offer the user

Used in the brief (SKILL.md step 1). Ask with AskUserQuestion; "Let AI decide" is always the first, recommended option. Skip the menu entirely when the user says "you decide", "auto", "just do it", passes `--auto`, or already described the look/motion.

## Question A: Style (single select, max 4 options)

Options = **Let AI decide (Recommended)** + the 3 styles that best fit this video type and brand (from `styles.md`). Give each a one-line description and, when useful, a tiny ASCII `preview` of a frame.

Good defaults per type:
| Type | Offer |
|---|---|
| promo / launch | Dark Product Film · Light Glass SaaS · Halftone/Acid Tech |
| tutorial / docs | Light Glass SaaS · Google Playful · Dark Product Film |
| demo | Dark ↔ Light Chapters · Light Glass SaaS · Dark Product Film |
| explainer | Paper & Marker · Editorial Serif · AI Neon Glow |
| reel (9:16) | Light Glass SaaS · Dark ↔ Light Chapters · Halftone/Acid Tech |
| ui-loop | One-Shape UI Motion (only option; skip question) |
| logo | AI Neon Glow · Dark Product Film · Editorial Serif |
| 3D | 3D Cinematic (skip question) |

If the user has a brand, say the style is applied in their colours/fonts.

## Question B: Signature effects (multi select, only if they picked a style)

Max 4 options; selecting none = AI picks. Group effects so each option is a recognisable "feel":

| Option label | Includes | Engine |
|---|---|---|
| Kinetic typography | word-by-word blur-rise, slams, rolling word slot, typewriter + caret, gradient key words, letter scramble | `M.words`, `M.cycle`, `M.typed`, `M.scramble`, `M.gradText` |
| 3D UI + camera | tilted UI planes settling flat, crop-zoom into features, push-ins, parallax, rack focus | `M.tilt`, `M.cam`, `M.focus` |
| Seamless morphs (no cuts) | one shape becomes the next (button → loader → ✓ → card), zoom-through, fly-through exits | `M.track`, `M.morph`, `M.flyOut`, `M.smear` |
| Glow & celebration | neon rim, gradient orbs, ripples, confetti, sparkle → logo | `.rim`, `M.orbs`, `M.ripple`, `M.burst` |

Other effects the user may type in ("Other"): hand-drawn notes + arrows (`M.stroke` + Caveat), counters/charts (`M.count`, `M.stroke`), cursor walkthrough (`M.path`), glitch/halftone, dark↔light chapter flips, 3D scene (Three.js), meme/caption cards (reels).

## Question C (only if relevant): Pace

`Calm & premium` (one idea per 4-6s, long holds) · `Punchy` (one idea per 2-3s, more hits) · `Let AI decide`. Ask only for promos/reels/explainers when the request doesn't imply it.

## After answers

Write the choices into the storyboard header ("Style: Light Glass SaaS · Effects: kinetic type, seamless morphs · Pace: punchy") so the user sees them before approving. Whatever was left to AI: choose from the type preset + `pro-techniques.md`, and state the choice in one line with the reason.
