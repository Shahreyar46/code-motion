# Gemini "Canvas" intro (60 s, 4K, no audio track, 1 hard cut)

## Arc
Pure black canvas. Alternates short kinetic text beats (~3 s, centred, small) with 3D-tilted dark UI close-ups (3-6 s) carrying cursor and glow.
- 0-1 "✦ Gemini" wordmark; sparkle scales into a big 4-point star (blue→violet).
- 2-5 dark UI "Hello, Teresa" (gradient text) in perspective; second panel slides in left (parallax, 2 planes), blue rim glow.
- 5-7 "Your AI assistant from Google" (AI in blue). 7-10 "Reimagined for better collaboration" letter-scramble assemble, "collaboration" ends large + blue.
- 11-15 "Introducing Canvas in Gemini" → Canvas pill (glowing rim) pushes in, prompt UI blurred behind.
- 16-19 "From the first draft" → prompt pill types a request + PDF attachment card; camera tilts/pans to a doc.
- 20-25 "To all the versions in between" → doc editing, vertical tool-rail pill, cursor clicks (Longer/Shorter/Suggest edits), suggestion card with ✦.
- 29-40 "Turn your concepts into code" → typed prompt in tilted input bar → code editor scroll → "And preview the final prototypes" Code|Preview toggle, Preview fills blue-violet, giant soft purple orb behind.
- 42-51 cycling keyword "docs / timelines / data / games / apps" over blurred app screens. Hard cut 51.7.
- 52-60 "All in one space" pill morphs into "Canvas" pill → bookend "Hello, Teresa" → "Try Canvas in Gemini today." + URL.

## Typography
Google Sans class, weight 400-500 only, never bold. Small and confident: beats 28-34 px at 1080p, keywords ~56 px. White `#F1F3F4`, 1-2 keywords blue-violet `#8AB4F8→#7B7FF2`. Entry blur-fade + slight rise, per-word stagger ~60 ms. Letter scramble ~0.8 s. Exit quick fade 0.2-0.3 s. Hold 1.5-2.5 s. Cycling words crossfade in place.

## Look
Black with violet bloom bottom-right (`#5B4BC4` @30%), cool blue haze top-left; only blue/violet hues. Star gradient `#4285F4→#7B6CF6→#A78BFA`. Neon rim: 2-3 px stroke blue `#4F7BFF` → violet `#9B7CF0` + outer halo 40-80 px. Panels `#1A1B1E`-`#202124`, radius ~28 px, pills fully round. Active toggle fill `linear-gradient(135deg,#7B7FF2,#4F86F7)`. Depth of field 6-12 px on non-focal layers. Cursor: white arrow, black outline, blue-violet offset shadow.

## Motion
Springs ζ≈0.8, settle 0.6-0.9 s. UI planes at rotateY −20…−30°, rotateX ~8°, drifting slowly; two depths for parallax. Typing 14-18 cps, blue caret, camera follows text end. Cursor curved ease-in-out path, press 0.9, target springs. Pill morph swaps width + label/icon. Camera: slow dolly-in + lateral pans, rack focus at the click, 8-12% push per beat. Never fades through white; shared constants (black, glow colour, tilt, pill) carry continuity.

## Build with
`.rim` panels, `M.tilt` + drift `ry=-24+3*sin(.5t)`, `M.scramble`, `M.cycle`, `M.typed`, `M.gradInit/gradText`, `M.focus` rack focus, `M.pulse` glow, `M.morph` pill. Sounds: pop on pill, click, shimmer, quiet riser into Preview, chime on end.
