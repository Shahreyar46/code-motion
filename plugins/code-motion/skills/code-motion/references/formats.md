# Formats: so no two videos look the same

A video = **type** (promo, tutorial…) × **format** (the storytelling device) × **style** (look) × **opening** (first 3 s) × **transition family**. The type preset fixes the goals and length; the format decides how the story is told. Rotate formats so a user who makes many videos of one type gets fresh ones.

## Rotation rule
1. Read `video/.code-motion-history.json` (create it if missing). It holds past videos: `[{"date","type","format","style","opening","transitions","title"}]`.
2. Pick the format that best fits this product/request **and** differs from the last 2 videos of the same type. Also change at least one of style / opening / transition family from the previous one.
3. If the user asks for "same as last time" or a series look, keep the format and style (consistency wins for a series).
4. Put the choice in the storyboard header: "Format: Before/After split · Style: … · Opening: … · Transitions: …". In the motion menu, AI decides the format by default; if the user picked a style themselves, still pick the format with this rule.
5. After delivery, append the entry to the history file.

## Formats per type

**Promo / launch (20-35 s)**
- *Problem → Meet → Proof*: pain slams, big "Meet", three feature hits, logo. (classic; Numtera)
- *One-object journey*: one shape travels and morphs through the whole film (folder → panel → bar → check → logo), no cuts. (LangEase)
- *Countdown / list*: "3 things X does" with huge numerals 3-2-1, each a feature.
- *Before / After split*: screen splits; left the old way (grey, slow), right with the product (colour, fast), merging at the end.
- *Question chain*: a sequence of typed questions the viewer recognises, each answered by a UI flash.
- *Manifesto*: kinetic-typography only, bold statements on the beat, product revealed last.
- *Zoom journey*: continuous zoom from a wide world (desk, city, map) into the product UI and finally into the logo.

**Product overview (45-75 s)**
- *Guided tour*: progress chip 1/5, feature by feature. (default)
- *Hub & spokes*: product icon in the centre; each feature orbits in, expands, returns to the hub.
- *Day in the life*: morning → noon → evening, the product helping at each moment (no people shown; use objects, time-of-day skies and nature).
- *Problem map*: 4-6 pain cards on a board; each gets solved and flipped to a feature card.
- *Build-up dashboard*: start from an empty canvas; each feature adds its panel until the full product is assembled.

**Tutorial / docs (60-150 s)**
- *Classic steps*: step chip + caption + crop-zoom + cursor action. (default; Google Vids)
- *Checklist*: a checklist on the side ticks off as each step completes on the main UI.
- *Result first, then rewind*: show the finished result, "here's how", rewind effect to step 1.
- *Split guide*: left = written step list (the docs), right = UI performing it; the active step highlights.
- *Problem → fix*: start from the common error/question users hit, then the steps that solve it.

**Product demo (60-120 s)**
- *Dark/light chapters* (Teamble) · *Single workflow end-to-end* (one real task from start to finish) · *Persona-free scenario* ("A new order arrives…" told through UI events) · *Feature matrix* (grid of features, camera dives into each cell).

**Explainer (45-90 s)**
- *Diagram build* · *Analogy* (concept explained through a nature/animal/object analogy, e.g. bees and a hive for a distributed system) · *Myth vs fact* · *Zoom through scales* · *Timeline* (then → now → next).

**Reel 9:16 (20-40 s)**
- *Meme hook → payoff* (plugin reel) · *POV caption* ("POV: your orders page loads instantly") · *Speed run* (task done in 10s with a timer) · *3 tips* · *Before/after swipe*.

**Logo** — draw-on · scramble · morph-from-shape · zoom-through · particles-assemble (nature: leaves/birds forming the mark).

## Openings (first 3 s), rotate them
Typed question · bold one-word slam · relatable broken UI · counter running up · zoom out from a detail · nature establishing shot (sky/sea/forest) that turns into the product world · sound-led hit on black · the finished result first.

## Transition families, pick one per video and stay consistent
Morph chain · zoom-through · cross-blur · blob/gradient wipe · whip-pan with smear · match-cut on shape/colour · hard cuts on beats with dark/light flips.
