"""Reactive sound design, synthesised in code (no samples, no licences): cues.json + vo.wav -> mix.wav

usage:
  python sfx.py mix  <cues.json> <mix.wav> [--vo vo.wav] [--dur SECONDS] [--sfx-db -8] [--duck-db 5] [--air]
  python sfx.py list                       # every sound with what it is for
  python sfx.py audition <out_dir>         # writes each sound as a wav + reel.wav to listen through

cues.json is written by render.js (from M.cue calls in the page): [{"t":1.25,"s":"pop","g":0.8,"pan":-0.3,"d":0.4,"pitch":1.1}, ...]
  t      seconds. For sounds with anchor 'end' (riser, suck) t is when the sound PEAKS/ends, so it lands on the hit.
  g      gain, linear (default 1). Keep most cues 0.4-0.9 so the impacts have headroom.
  pan    -1 left .. 1 right (default 0). Pan with the motion: things entering from the left start left.
  d      duration override for sustained sounds (whoosh, riser, pen, roll, paper).
  pitch  multiplier (default 1 with ±3% random humanising; pass "exact": true to disable the jitter).

Music: OFF by default (content policy). Only when the user asked for it:
  --music path/to/track.mp3   their own track (they own the rights); looped/trimmed, faded, ducked under the voice
  --music synth               generated soft ambient pad (no licence needed)
  --music-db -20              music level vs voice (default -20 dB; ducks a further 8 dB under speech)

Mixing: VO is the lead. SFX sit ~8 dB under it and duck a further ~5 dB while words are spoken, then come back
for the gaps. Final loudness (-14 LUFS) is set by mux.py, so levels here are relative."""
import json, sys, wave, hashlib, argparse, pathlib
import numpy as np

SR = 48000
TAU = 2 * np.pi


def T(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.002, d=0.1, curve=1.0):
    t = np.arange(n) / SR; at = np.clip(t / max(a, 1e-4), 0, 1)
    return at * np.exp(-np.maximum(t - a, 0) / max(d, 1e-4)) ** curve
def bell(n, peak=0.5, power=2.0):
    x = np.linspace(0, 1, n); return np.where(x < peak, (x / peak), ((1 - x) / (1 - peak))) ** power
def sweep(f0, f1, d, shape='exp'):
    n = int(d * SR); u = np.linspace(0, 1, n)
    f = f0 * (f1 / f0) ** u if shape == 'exp' else f0 + (f1 - f0) * u
    return np.sin(TAU * np.cumsum(f) / SR)
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    m = np.clip(np.minimum((f - lo * 0.7) / (lo * 0.3 + 1), (hi * 1.3 - f) / (hi * 0.3 + 1)), 0, 1)
    return np.fft.irfft(X * m, len(x))
def noise(n, rng): return rng.standard_normal(n)
def moving_band(d, centers, width, rng):
    """noise whose band centre follows `centers` (list of Hz over the duration): the whoosh core."""
    n = int(d * SR); seg = 2048; hop = seg // 2; out = np.zeros(n + seg); w = np.hanning(seg)
    k = 0
    while k * hop < n:
        u = k * hop / max(n - 1, 1); c = np.interp(u, np.linspace(0, 1, len(centers)), centers)
        out[k * hop:k * hop + seg] += band(noise(seg, rng), c / width, c * width) * w
        k += 1
    return out[:n]
def norm(x, peak=0.9): m = np.abs(x).max(); return x / m * peak if m > 0 else x
def bellsound(f, d, rng, partials=((1, 1, 1), (2.0, .5, .55), (2.76, .35, .4), (5.4, .15, .25))):
    t = T(d); x = sum(a * np.sin(TAU * f * r * t + rng.uniform(0, 6)) * np.exp(-t / (d * dk * 0.35)) for r, a, dk in partials)
    return x * np.clip(t / 0.003, 0, 1)


# ---------------- the library: name -> (fn(rng, d, p) , default d, anchor, what it is for) ----------------
def s_click(r, d, p): t = T(0.05); return norm(band(noise(len(t), r), 2000, 9000) * env(len(t), .0005, .004) + .6 * np.sin(TAU * 2300 * p * t) * env(len(t), .0005, .012) + .4 * np.sin(TAU * 900 * p * t) * env(len(t), .001, .02))
def s_tick(r, d, p): t = T(0.03); return norm(np.sin(TAU * 3200 * p * t) * env(len(t), .0003, .006) + .3 * band(noise(len(t), r), 4000, 12000) * env(len(t), .0002, .003), .6)
def s_hover(r, d, p): return s_tick(r, d, p * 0.8) * 0.4
def s_key(r, d, p):
    t = T(0.06); f = r.uniform(.85, 1.15) * p
    return norm(band(noise(len(t), r), 1500 * f, 6000 * f) * env(len(t), .0005, .012) + .5 * np.sin(TAU * 190 * f * t) * env(len(t), .001, .02), .55)
def s_pop(r, d, p):
    x = sweep(260 * p, 820 * p, .07) * env(int(.07 * SR), .001, .03); c = s_click(r, d, p); x[:len(c)] += .25 * c; return norm(x)
def s_bubble(r, d, p): return norm(sweep(520 * p, 1500 * p, .05) * env(int(.05 * SR), .001, .018), .7)
def s_snap(r, d, p): t = T(0.04); return norm(band(noise(len(t), r), 3000, 12000) * env(len(t), .0003, .004) + .5 * np.sin(TAU * 1600 * p * t) * env(len(t), .0003, .008), .8)
def s_whoosh(r, d, p):
    d = d or .55; x = moving_band(d, [350 * p, 1300 * p, 2600 * p, 900 * p], 1.6, r); return norm(x * bell(len(x), .62, 1.6), .8)
def s_swish(r, d, p): d = d or .28; x = moving_band(d, [1400 * p, 5200 * p, 2500 * p], 1.5, r); return norm(x * bell(len(x), .45, 1.8), .7)
def s_swipe(r, d, p): d = d or .17; x = moving_band(d, [2500 * p, 6500 * p], 1.4, r); return norm(x * bell(len(x), .35, 1.5), .55)
def s_suck(r, d, p): return s_whoosh(r, d or .5, p)[::-1] * np.linspace(.3, 1, int((d or .5) * SR)) ** 2
def s_impact(r, d, p):
    d = d or 1.3; t = T(d)
    sub = np.sin(TAU * np.cumsum(38 * p + 50 * p * np.exp(-t / .08)) / SR) * env(len(t), .002, .55)
    body = np.sin(TAU * 140 * p * t) * env(len(t), .001, .12) * .5
    crack = band(noise(len(t), r), 80, 3500) * env(len(t), .0005, .05) * .9
    tail = band(noise(len(t), r), 200, 1200) * env(len(t), .01, .35) * .12
    return norm(np.tanh(1.6 * (sub + body + crack + tail)))
def s_thud(r, d, p):
    t = T(.45); return norm(np.tanh(1.4 * (np.sin(TAU * np.cumsum(55 * p + 45 * p * np.exp(-t / .05)) / SR) * env(len(t), .002, .14) + band(noise(len(t), r), 60, 1500) * env(len(t), .0005, .03) * .6)), .8)
def s_sub(r, d, p): d = d or 1.4; t = T(d); return norm(np.sin(TAU * np.cumsum(32 * p + 18 * p * np.exp(-t / .3)) / SR) * env(len(t), .012, .6), .9)
def s_riser(r, d, p):
    d = d or 1.6; n = int(d * SR); ramp = np.linspace(0, 1, n) ** 2.6
    x = moving_band(d, [300 * p, 1500 * p, 6000 * p], 1.5, r) * ramp + .35 * sweep(180 * p, 1100 * p, d) * ramp
    x[-int(.012 * SR):] *= np.linspace(1, 0, int(.012 * SR)); return norm(x, .75)
def s_chime(r, d, p): return norm(bellsound(1320 * p, d or 1.1, r), .55)
def s_ding(r, d, p):
    a = bellsound(880 * p, .7, r); b = bellsound(1320 * p, .9, r); o = np.zeros(int(.09 * SR) + len(b)); o[:len(a)] += a; o[int(.09 * SR):] += b; return norm(o, .55)
def s_success(r, d, p):
    o = np.zeros(int(1.1 * SR))
    for i, f in enumerate([660, 880, 1320]):
        b = bellsound(f * p, .8, r); k = int(i * .07 * SR); o[k:k + len(b)] += b[:len(o) - k]
    return norm(o, .55)
def s_error(r, d, p):
    t = T(.11); sq = lambda f: np.sign(np.sin(TAU * f * t)) * .4 + np.sin(TAU * f * t) * .6
    b = band(sq(220 * p), 100, 3000) * env(len(t), .002, .06); o = np.zeros(int(.26 * SR)); o[:len(b)] += b; o[int(.13 * SR):int(.13 * SR) + len(b)] += b; return norm(o, .6)
def s_shimmer(r, d, p):
    d = d or 1.1; t = T(d); x = np.zeros(len(t))
    for _ in range(14):
        f = r.uniform(3000, 9500) * p; x += np.sin(TAU * f * t + r.uniform(0, 6)) * (0.5 + 0.5 * np.sin(TAU * r.uniform(4, 9) * t + r.uniform(0, 6)))
    return norm(x * bell(len(t), .25, 1.4), .35)
def s_glitch(r, d, p):
    d = d or .22; n = int(d * SR); x = np.zeros(n); k = 0
    while k < n:
        L = int(r.uniform(.006, .02) * SR); f = r.uniform(90, 2200) * p; t = np.arange(min(L, n - k)) / SR
        blk = np.sign(np.sin(TAU * f * t)) if r.random() < .5 else np.round(noise(len(t), r) * 3) / 3
        x[k:k + len(t)] = blk * (r.random() < .8) * r.uniform(.3, 1); k += L
    return norm(band(x, 80, 9000), .55)
def s_pen(r, d, p):
    d = d or .6; t = T(d); rate = r.uniform(9, 14); am = np.abs(np.sin(TAU * rate * t + .3 * np.sin(TAU * 2.3 * t))) ** 1.5
    return norm(band(noise(len(t), r), 2500 * p, 7000 * p) * am * bell(len(t), .1, .5), .35)
def s_paper(r, d, p): d = d or .35; t = T(d); am = np.clip(noise(len(t) // 400 + 2, r), 0, None); am = np.interp(np.arange(len(t)), np.arange(len(am)) * 400, am); return norm(band(noise(len(t), r), 900, 8000) * am * bell(len(t), .3, 1), .4)
def s_stamp(r, d, p): a = s_thud(r, d, p * 1.3); b = s_paper(r, .2, p); o = np.zeros(max(len(a), len(b))); o[:len(a)] += a; o[:len(b)] += .5 * b; return norm(o, .85)
def s_shutter(r, d, p):
    c = s_click(r, d, p * .7); o = np.zeros(int(.12 * SR) + len(c)); o[:len(c)] += c; o[int(.07 * SR):int(.07 * SR) + len(c)] += .8 * s_click(r, d, p * .9); return norm(o + .3 * np.pad(s_swipe(r, .1, p), (0, max(0, len(o) - int(.1 * SR))))[:len(o)], .7)
def s_roll(r, d, p):
    """counter ticking: fast ticks that slow down, for numbers counting up. d = how long the count runs."""
    d = d or 1.0; o = np.zeros(int((d + .05) * SR)); tk = 0.0
    while tk < d:
        u = tk / d; tick = s_tick(r, 0, p * (1 + .25 * u)) * (1 - .6 * u); k = int(tk * SR); o[k:k + len(tick)] += tick[:len(o) - k]; tk += .028 + .09 * u ** 2
    return norm(o, .45)
def s_reveal(r, d, p):
    a = s_sub(r, 1.4, p); b = s_shimmer(r, 1.3, p); c = s_chime(r, 1.2, p * .5)
    o = np.zeros(max(map(len, (a, b, c)))); o[:len(a)] += a; o[:len(b)] += .6 * b; o[:len(c)] += .5 * c; return norm(o, .9)

LIB = {
    'click': (s_click, 0, 'start', 'cursor press, button tap'),
    'tick': (s_tick, 0, 'start', 'tiny UI step: list row lands, step in a sequence, caret'),
    'hover': (s_hover, 0, 'start', 'very soft tick: cursor arrives on a target'),
    'key': (s_key, 0, 'start', 'one keystroke; put one per typed character (or every 2nd) with pitch variety'),
    'pop': (s_pop, 0, 'start', 'element appears / card lands / badge pops'),
    'bubble': (s_bubble, 0, 'start', 'small light appear: chip, tag, dot, notification count'),
    'snap': (s_snap, 0, 'start', 'toggle flips, item snaps into slot, crop/cut'),
    'whoosh': (s_whoosh, .55, 'start', 'camera move / big element flies across. d = move duration'),
    'swish': (s_swish, .28, 'start', 'quick transition, wipe, text slides in'),
    'swipe': (s_swipe, .17, 'start', 'small slide: tab indicator, card shift, list scroll'),
    'suck': (s_suck, .5, 'end', 'reverse whoosh INTO a hit: collapse, zoom-in to a point (t = moment of arrival)'),
    'impact': (s_impact, 1.3, 'start', 'big hit: title slam, scene cut on a key word, logo lands'),
    'thud': (s_thud, .45, 'start', 'medium weight: heavy card drops, word lands hard'),
    'sub': (s_sub, 1.4, 'start', 'low boom under a reveal (felt more than heard)'),
    'riser': (s_riser, 1.6, 'end', 'tension build INTO a hit (t = the hit); pair with impact at the same t'),
    'chime': (s_chime, 1.1, 'start', 'bright highlight, sparkle moment, tagline'),
    'ding': (s_ding, 0, 'start', 'notification / toast / message received'),
    'success': (s_success, 0, 'start', 'check mark, task done, payment success'),
    'error': (s_error, 0, 'start', 'wrong / rejected / problem state'),
    'shimmer': (s_shimmer, 1.1, 'start', 'glint across a logo/card, magic/AI moment'),
    'glitch': (s_glitch, .22, 'start', 'digital glitch transition, RGB split, data corrupt'),
    'pen': (s_pen, .6, 'start', 'marker/handwriting drawing on (d = draw duration)'),
    'paper': (s_paper, .35, 'start', 'paper/cutout/sticky note moves'),
    'stamp': (s_stamp, 0, 'start', 'stamp/label slapped on'),
    'shutter': (s_shutter, 0, 'start', 'screenshot / capture / camera'),
    'roll': (s_roll, 1.0, 'start', 'number counting up (d = count duration)'),
    'reveal': (s_reveal, 0, 'start', 'logo reveal / end card (sub + shimmer + low chime)'),
}


def render_cue(c, idx):
    name = c['s']
    if name not in LIB: raise SystemExit(f'unknown sound "{name}". run: python sfx.py list')
    fn, dd, anchor, _ = LIB[name]
    seed = int(hashlib.md5(f'{idx}|{name}|{c["t"]}'.encode()).hexdigest()[:8], 16); r = np.random.default_rng(seed)
    p = float(c.get('pitch', 1)) * (1 if c.get('exact') else r.uniform(.97, 1.03))
    g = float(c.get('g', 1)) * (1 if c.get('exact') else 10 ** (r.uniform(-1.2, 1.2) / 20))
    x = fn(r, float(c.get('d', dd) or dd), p) * g
    start = c['t'] - (len(x) / SR if anchor == 'end' else 0)
    pan = float(np.clip(c.get('pan', 0), -1, 1)); a = (pan + 1) * np.pi / 4
    return start, np.stack([x * np.cos(a), x * np.sin(a)], 1) * np.sqrt(2)


def read_wav(p):
    with wave.open(str(p)) as w:
        ch, sr = w.getnchannels(), w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    x = x.reshape(-1, ch)
    if sr != SR: raise SystemExit(f'{p}: expected {SR} Hz')
    return x if ch == 2 else np.repeat(x, 2, 1)


def write_wav(p, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1: x = np.stack([x, x], 1)
    with wave.open(str(p), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())


def vo_envelope(vo):
    m = np.abs(vo).mean(1); n = int(.03 * SR); k = len(m) // n
    rms = np.sqrt((m[:k * n].reshape(k, n) ** 2).mean(1)); on = (rms > 0.02).astype(float)
    # attack 30ms, release 250ms smoothing on the block grid
    out = np.zeros_like(on); v = 0
    for i, o in enumerate(on):
        v = v + (o - v) * (1 if o > v else 0.12); out[i] = v
    return np.repeat(out, n)


def synth_pad(n, seed=5):
    """soft ambient chord bed: I-vi-IV-V voicings, slow swells, gentle shimmer. Quiet by design."""
    r = np.random.default_rng(seed); t = np.arange(n) / SR; out = np.zeros(n)
    chords = [[261.6, 329.6, 392.0, 493.9], [220.0, 261.6, 329.6, 392.0], [174.6, 220.0, 261.6, 329.6], [196.0, 246.9, 293.7, 392.0]]
    seg = 4.0; k = 0
    while k * seg < n / SR:
        a, b = int(k * seg * SR), min(n, int((k + 1) * seg * SR + 1.5 * SR)); tt = t[a:b] - k * seg
        env = np.clip(tt / 1.2, 0, 1) * np.clip((seg + 1.5 - tt) / 1.5, 0, 1)
        for f in chords[k % 4]:
            for det in (-0.6, 0.6):
                ph = r.uniform(0, 6)
                out[a:b] += env * (np.sin(TAU * (f + det) * tt + ph) + 0.25 * np.sin(TAU * 2 * (f + det) * tt + ph)) * 0.12
        out[a:b] += env * np.sin(TAU * chords[k % 4][0] / 2 * tt) * 0.18
        k += 1
    return norm(out * (0.85 + 0.15 * np.sin(TAU * 0.13 * t)), 0.8)


def load_music(spec, n, tmpdir):
    if spec == 'synth':
        x = synth_pad(n); return np.stack([x, x], 1)
    import subprocess
    w = pathlib.Path(tmpdir) / 'music48k.wav'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', spec, '-ac', '2', '-ar', str(SR), '-sample_fmt', 's16', str(w)], check=True)
    m = read_wav(w)
    if len(m) < n: m = np.concatenate([m] * (n // max(1, len(m)) + 1))
    return m[:n]


def cmd_mix(a):
    if a.cues and not pathlib.Path(a.cues).exists(): raise SystemExit(f'cues file not found: {a.cues} (render.js writes <out>.cues.json)')
    cues = json.loads(pathlib.Path(a.cues).read_text(encoding='utf-8')) if a.cues else []
    if a.vo:   # male-voice gate: applies to ANY narration file, including pre-recorded takes
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import voicecheck
        code, f0, _ = voicecheck.check(a.vo)
        if code == 3: raise SystemExit(f'REFUSED: {a.vo} sounds female (median pitch {f0:.0f} Hz). This plugin uses male narration only; regenerate the voice with a male voice.')
    vo = read_wav(a.vo) if a.vo else np.zeros((0, 2), np.float32)
    rendered = [render_cue(c, i) for i, c in enumerate(sorted(cues, key=lambda c: c['t']))]
    end = max([len(vo) / SR, a.dur or 0] + [s + len(x) / SR for s, x in rendered]) + 0.3
    if a.dur: end = a.dur
    n = int(end * SR); bus = np.zeros((n, 2), np.float32)
    for s, x in rendered:
        k = int(round(s * SR));
        if k < 0: x = x[-k:]; k = 0
        m = min(len(x), n - k)
        if m > 0: bus[k:k + m] += x[:m]
    bus = np.tanh(bus * 1.1) / 1.1                                       # gentle bus glue, catches stacked hits
    bus *= 10 ** (a.sfx_db / 20)
    if len(vo):
        e = vo_envelope(vo); duck = np.ones(n); duck[:len(e)] = 10 ** (-a.duck_db * e[:n] / 20); bus *= duck[:, None]
    mix = bus.copy(); mix[:min(n, len(vo))] += vo[:n]
    if a.music:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            mu = load_music(a.music, n, td)
        mu = mu / (np.abs(mu).max() or 1)
        fi, fo = int(1.0 * SR), int(min(2.5, end / 3) * SR)
        g = np.ones(n); g[:fi] = np.linspace(0, 1, fi); g[-fo:] = np.minimum(g[-fo:], np.linspace(1, 0, fo))
        if len(vo):
            e = vo_envelope(vo); dk = np.ones(n); dk[:len(e)] = 10 ** (-8 * e[:n] / 20); g *= dk
        mix += mu * (g * 10 ** (a.music_db / 20))[:, None]
    if a.air:                                                            # faint room tone so silence never sounds "digital"
        r = np.random.default_rng(7); x = band(r.standard_normal(n), 80, 6000); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[1:] /= np.sqrt(f[1:] / 80); X[0] = 0   # pink-ish via FFT (fast)
        mix += norm(np.fft.irfft(X, n), 1)[:, None] * 10 ** (-56 / 20)
    pk = np.abs(mix).max()
    if pk > .98: mix *= .98 / pk
    write_wav(a.out, mix)
    print(f'mix {a.out}: {end:.2f}s, {len(cues)} cues, sfx {a.sfx_db} dB, duck {a.duck_db} dB' + (f', music {a.music} at {a.music_db} dB' if a.music else ', no music'))


def cmd_audition(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True); reel = []
    for i, (k, v) in enumerate(LIB.items()):
        s, x = render_cue({'t': 2, 's': k, 'exact': True}, i); write_wav(out / f'{k}.wav', x); reel += [x, np.zeros((int(.45 * SR), 2))]
    write_wav(out / 'reel.wav', np.concatenate(reel)); print('wrote', len(LIB), 'sounds + reel.wav to', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd')
    m = sp.add_parser('mix'); m.add_argument('cues'); m.add_argument('out'); m.add_argument('--vo'); m.add_argument('--dur', type=float)
    m.add_argument('--sfx-db', type=float, default=-8); m.add_argument('--duck-db', type=float, default=5); m.add_argument('--air', action='store_true')
    m.add_argument('--music', help='OFF by default. path to your own track, or synth'); m.add_argument('--music-db', type=float, default=-20)
    sp.add_parser('list'); au = sp.add_parser('audition'); au.add_argument('out')
    a = ap.parse_args()
    if a.cmd == 'mix': cmd_mix(a)
    elif a.cmd == 'audition': cmd_audition(a.out)
    else:
        for k, v in LIB.items(): print(f'{k:9s} {v[3]}' + ('   [t = end]' if v[2] == 'end' else ''))
