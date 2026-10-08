"""Subtitles + chapters from the voiceover timings (no speech recognition needed: the script is the source).

usage: python captions.py audio/timings.json out/ [--max-chars 42] [--chapters chapters.json]
writes: out/captions.srt, out/captions.vtt, out/chapters.txt (YouTube format)

chapters.json (optional): [{"title": "Intro", "line": "hook"}, {"title": "Step 1: Connect", "line": "step1"}]
Without it, every line whose id starts with "step" (or "ch") becomes a chapter, plus "Intro" at 0:00.
Long lines are split into cues of <= max-chars using the real word times, so captions stay readable."""
import json, sys, argparse, pathlib


def ts(t, sep=','):
    ms = int(round(max(0, t) * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}'


def cues(lines, maxc):
    out = []
    for l in lines:
        ws = l.get('words') or [{'w': l['text'], 'start': l['start'], 'end': l['end']}]
        toks = l['text'].split()
        if len(toks) == len(ws):                      # TTS word events drop punctuation: restore it from the script text
            ws = [{**w, 'w': tk} for w, tk in zip(ws, toks)]
        cur, a = [], None
        for w in ws:
            if cur and len(' '.join(x['w'] for x in cur + [w])) > maxc:
                out.append((a, cur[-1]['end'], ' '.join(x['w'] for x in cur))); cur = []
            if not cur: a = w['start']
            cur.append(w)
        if cur: out.append((a, max(cur[-1]['end'], l['end']), ' '.join(x['w'] for x in cur)))
    # hold each cue until the next starts (max +0.6s) so text doesn't flash
    res = []
    for i, (a, b, s) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else b + 0.6
        res.append((a, min(max(b, a + 0.8), nxt - 0.02, b + 0.6) if nxt > a else b, s))
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('timings'); ap.add_argument('out')
    ap.add_argument('--max-chars', type=int, default=42); ap.add_argument('--chapters')
    a = ap.parse_args()
    T = json.loads(pathlib.Path(a.timings).read_text(encoding='utf-8')); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    C = cues(T['lines'], a.max_chars)
    srt = '\n'.join(f'{i}\n{ts(x)} --> {ts(y)}\n{s}\n' for i, (x, y, s) in enumerate(C, 1))
    vtt = 'WEBVTT\n\n' + '\n'.join(f'{ts(x, ".")} --> {ts(y, ".")}\n{s}\n' for x, y, s in C)
    (out / 'captions.srt').write_text(srt, encoding='utf-8'); (out / 'captions.vtt').write_text(vtt, encoding='utf-8')
    byid = {l['id']: l for l in T['lines']}
    if a.chapters:
        ch = [(byid[c['line']]['start'], c['title']) for c in json.loads(pathlib.Path(a.chapters).read_text(encoding='utf-8'))]
    else:
        ch = [(l['start'], l['text'].rstrip('.')[:60]) for l in T['lines'] if l['id'].lower().startswith(('step', 'ch'))]
    ch = sorted(ch); ch = ([(0, 'Intro')] if not ch or ch[0][0] > 0.5 else []) + ch
    ch[0] = (0, ch[0][1])
    mmss = lambda t: f'{int(t // 60)}:{int(t % 60):02d}'
    (out / 'chapters.txt').write_text('\n'.join(f'{mmss(t)} {n}' for t, n in ch) + '\n', encoding='utf-8')
    print(f'{len(C)} caption cues, {len(ch)} chapters -> {out}/captions.srt, captions.vtt, chapters.txt')


if __name__ == '__main__':
    main()
