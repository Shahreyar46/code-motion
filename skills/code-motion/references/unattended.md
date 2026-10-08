# Unattended mode (scheduled / cloud runs)

Use when the request contains `--unattended`, or when running as a scheduled task / routine where nobody can answer. Never call AskUserQuestion and never wait for approval in this mode.

## Inputs (in the user's project)
- `video/brief.md`: the standing brief, written once with the user (or by `/code-motion:setup --schedule`): product, audience, URLs/repo paths, CTA + URL, brand (colours, fonts, logo path), voice (provider/voice/rate), default formats (16:9, 9:16), allowed video types, things to always/never say.
- `video/queue.md`: what to make next, one item per line, checkboxes:
  ```
  - [ ] promo: new "bulk export" feature (see docs/export.md)
  - [ ] tutorial: how to connect Stripe
  - [ ] reel: 3 tips for faster checkout
  ```
  Take the **first unchecked item**. If the queue is empty, make the next video type in rotation from the brief (promo → overview → reel → tutorial…) about the product's most recent change (read `CHANGELOG`/git log).
- `video/.code-motion-history.json`: used by the format rotation so every scheduled video differs.

## Steps
1. Run `python $SKILL/scripts/doctor.py --fix`. If it isn't READY, run `bash $SKILL/scripts/setup.sh ./video` (cloud machines are fresh each run). If still not ready, write the doctor output to `video/out/FAILED-<date>.md`, commit it, and stop.
2. Read brief + queue item + the type preset. Choose style/effects/format yourself (`--auto` behaviour); pick a different format from recent history.
3. Write the script and voice it; write the storyboard into `video/out/<date>-<slug>/NOTES.md` instead of asking for approval.
4. Build → stills → run the senior review checklist (`motion-principles.md` §10) and fix, at least 2 rounds, stricter than usual since nobody reviews before publishing.
5. Render final (60fps; use `--sub 2` if the video is longer than 60 s to keep the run under ~30 min), mix (no music unless the brief says so), mux, captions.
6. Deliver into `video/out/<date>-<slug>/`: `final.mp4` (+ `final-9x16.mp4` if the brief asks), `captions.srt`, `chapters.txt`, `NOTES.md`, contact sheet.
7. Tick the queue item (`- [x] … → video/out/<date>-<slug>/final.mp4`), append history.
8. **Save the result where the user can get it** (cloud machines are deleted after the run):
   - commit `video/out/<date>-<slug>/` + queue + history on a branch `videos/<date>-<slug>` and push it (keep `video/node_modules/` out of git; MP4s are usually 3-15 MB, fine for git; if larger than 50 MB, render at `--crf 20`).
   - and/or open a pull request titled "New video: <title>" when `gh` is available, so the user gets a notification with the video.
9. End with a short summary: title, length, format/style, file path/branch, anything that needs the user's attention.

## Never in unattended mode
Invent facts, numbers, testimonials or UI; use music unless the brief allows it; break the content policy; publish anywhere except the user's own repo.
