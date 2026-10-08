# Teamble SaaS product demo (98 s, 25 fps, 10 hard cuts)

## Arc
- 0-7 dark brand intro: logo, typed "Introduces teamble ai" in a rounded pill, blurred orb.
- 7-17 light kinetic headline "Give your team superpowers / Help them unlock their potential with [9x better] Feedback".
- 15-22 prompt card "Good morning Mike, you have a 1-on-1 with Taylor", cursor clicks Prepare, card tilts into 3D, UI reveals.
- 22-38 "Even a simple observation" → dark button "Help me craft feedback" → Generating → typed text → "AI feedback score" card → tilted panel with metric rows.
- 39-48 "go from just managing to truly coaching": before/after cards, score 4 → 10 → 92/100.
- 48-67 dark "Unlock actionable insights": full dashboard (tilted) → crop/zoom to insights strip → themes card → Share pill → avatars → check.
- 67-85 light "uncovers hidden trends": orbiting avatars around "Onboarding Survey", floating response cards.
- 85-95 dark heatmap → benchmark pill → AI insights → "Create report" → check.
- 95-98 logo + tagline.
Hard cuts at 7.0, 15, 17.2, 22.4, 26.1, 48.2, 57.4, 64.2, 67.9, 76.1. One idea per 3-6 s; chapters alternate dark/light.

## Typography
Geometric grotesk (Inter/Satoshi-like), Medium/Semibold. Headlines 56-110 px, tracking −0.02 em; subheads 28-36 px. Phrases of 3-6 words swap in place, centred; blur+rise or mask entrance, blur-fade exit, hold 1-1.5 s. Key words pink→violet gradient `#ff3d8b→#b24dff`; rest white on dark / `#1a1a2e` on light. Typed text with caret. Inline pill morphs inside the sentence ("9x better", "2x→3x→4x better" with growing concentric rings).

## Look
Dark `#0a0714` + magenta/violet blurred orb (`#ff4fa0`, `#8a3ffc`) drifting; light `#f6f0fb` + lilac/pink mesh (`#d9a8ff`, `#ff9ccf`, hint `#9ec5ff`). White glass cards, radius 20-28 px. Gradient pill buttons.

## Motion
Spring pop for cards (~4% overshoot, 0.5 s); concentric ring ripples (stagger 0.08 s); 3D tilt-in of UI plane (rotateX ~50° → flat over 1.5 s); slow orb drift; counters; orbit rings with avatars; checkmark circle closes each flow. Hard cuts on a beat with the incoming element already moving; within chapters one shape morphs (Share pill → avatar pill → check).

## Product-demo lesson
UI is never a screenshot: clean cards, 10-15 words, skeleton lines. One component on screen at a time, cropped huge. Full dashboard appears once, tilted and dimmed, then camera pushes into one strip. Purple hand-pointer cursor glides on a curve, slightly undershoots, clicks with tiny press; target reacts instantly. Each workflow is a 3-5 morph chain: button → loading → typed text → score card → detail. Chat/response cards stagger in from edges at different sizes/depths. People/integrations as avatars orbiting a node. Before/after as two stacked cards with score badges.

## Build with
`M.morph`/`M.track` morph chains, `M.words('blur')` + gradient spans, `M.typed`, `M.ripple`, `M.tilt` (50→0), `M.cam` crop-zoom, `M.path` cursor + `M.presses`, `M.orbs`, `M.count` with colour lerp, orbit `angle=a0+0.4t`. Sounds: whoosh on cuts, pops on cards, clicks, success on checks.
