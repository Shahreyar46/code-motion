# WooCommerce plugin promo reel, vertical 9:16 (55 s, 60 fps, 1 hard cut)

ArchiveMaster (Woo order archiver) as a meme-then-solution reel, ~3.5-5 s per idea.

## Arc
- 0-7 pain meme: fake wp-admin browser, caption "Me: opening the Orders page" → "Still loading..." → "Seriously?!" + "Page Unresponsive" dialog.
- 7-13 reaction-GIF card on dark.
- 13-17.4 dark "The real problem? Years of old orders." + 3D DB cylinder, counter 0→48,213, order chips falling in, red glow.
- HARD CUT 17.43 dark → light (relief beat).
- 17.4-21 logo + "Archive old orders. Speed up your store."
- 21-28 "One click. Old orders, archived." dashboard card, cursor clicks Archive Now, progress bar, donut recolours.
- 28-33 "Moved to separate archive storage" flow: live DB card → node → storage options.
- 33-38 "Still searchable. Exportable. Restorable." + 3 pill chips.
- 38-43 meme payoff "Me: opening it now" (same mock, now loads fast) + stat cards.
- 43-48 reaction GIF "Me seeing my Orders page now".
- 48-55 logo ring/particle burst, "Lighter database. Faster store.", CTA pill "Get it free on WordPress.org", URL, tiny disclaimer.
Dark/chaos = problem, light/lavender = solution, meme bookends.

## Layout (vertical)
Headline top third (y 8-20%), product mid, chips/CTA lower third, bottom ~12% empty (platform UI). Headlines 64-72 px, nothing under 22 px. On-screen text carries everything (sound-off).

## Typography
Inter-like grotesk 700-800, −0.02 em, sentence case. Line 2 = highlight: gradient purple `#6C4DF0` → cyan `#3AA8E8` on light, coral `#FF6B4A` → orange `#FF9A3C` on dark. Meme caption ~34 px bold in white rounded card (r~28) with emoji. Subtext 24-26 px grey. Word-by-word blur(8)→0 + 10 px rise, 0.12 s stagger, ~0.35 s per word; line 2 starts 0.5 s after line 1. Whole scene cross-blurs out while next headline blurs in (overlap, no gap). Hold 3-5 s.

## Look
Light `#F4F2FF` with violet `#B9A6FF` (top-left) and sky `#A8DCF5` (bottom-right) blurred blobs drifting. Dark `#0C0A16→#1A1030`, indigo glow top, red `#FF3B2F` glow pulsing behind the DB. Cards white r~24, shadow `0 20px 60px rgba(80,60,160,.18)`. Primary CTA dark navy `#14112B` pill with WordPress logo.

## Motion
Counter ramp ease-out-expo; chips drop into DB staggered; glow pulse 1.2 s period; cards scale 0.96→1 + fade + blur 0.5 s; macOS cursor on eased arcs, press scale, button states Archive Now → Archiving… spinner → green Archived; progress fill; donut recolour; flow diagram line draws, node travels, chips drop along it, live DB bar shrinks as count falls with red→green; end ring + particles resolve into logo. Camera static.

## Build with
`M.words('blur')`, gradient line 2, `M.vis` cross-blur, hard cut + `impact`, reusable browser mock with state, `M.count`, `M.stagger` chip drops + `pop`, `M.pulse` glow, cursor + morph button + `click`/`success`, `M.stroke` flow line, `M.burst` end, `M.orbs` background.
