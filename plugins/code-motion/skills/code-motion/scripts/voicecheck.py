"""Male-voice gate: estimate the speaking pitch of a voiceover and refuse female-sounding audio.

usage: python voicecheck.py <audio file> [--max-hz 165]
exit 0 = male range (prints median F0), exit 3 = female/too high (do NOT use this audio), exit 2 = no speech found.

Works on any source: TTS output, an uploaded/recorded file, or old "takes" from a kit. voice.py, sfx.py mix and
mux.py call it automatically, so a female voice can't reach a final video even if it bypassed voice.py.
Adult male speech typically has a median F0 of ~85-155 Hz, adult female ~165-255 Hz."""
import sys, subprocess, tempfile, pathlib, wave
import numpy as np

SR = 16000


def load(path):
    p = pathlib.Path(path)
    with tempfile.TemporaryDirectory() as td:
        w = pathlib.Path(td) / 'v.wav'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', str(p), '-ac', '1', '-ar', str(SR), '-sample_fmt', 's16', str(w)], check=True)
        with wave.open(str(w)) as f:
            return np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768


def median_f0(x, fmin=65, fmax=400):
    n, hop = int(0.04 * SR), int(0.01 * SR)
    lo, hi = int(SR / fmax), int(SR / fmin)
    rms_all = np.sqrt(np.mean(x ** 2)) + 1e-9
    f0s = []
    for i in range(0, len(x) - n, hop):
        fr = x[i:i + n] * np.hanning(n)
        if np.sqrt(np.mean(fr ** 2)) < 0.5 * rms_all: continue          # skip silence/unvoiced
        fr = fr - fr.mean()
        ac = np.fft.irfft(np.abs(np.fft.rfft(fr, 2 * n)) ** 2)[:n]
        if ac[0] <= 0: continue
        ac /= ac[0]
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] < 0.45: continue                                          # not clearly periodic
        # prefer the lowest strong peak (avoid picking the first harmonic as F0's double)
        if k * 2 < hi and ac[min(k * 2, n - 1)] > 0.9 * ac[k]: k *= 2
        f0s.append(SR / k)
    return (float(np.median(f0s)), len(f0s)) if len(f0s) >= 10 else (None, len(f0s))


def check(path, max_hz=165.0):
    f0, n = median_f0(load(path))
    if f0 is None: return 2, f0, n
    return (0 if f0 < max_hz else 3), f0, n


if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    mx = float(sys.argv[sys.argv.index('--max-hz') + 1]) if '--max-hz' in sys.argv else 165.0
    code, f0, n = check(sys.argv[1], mx)
    if code == 0: print(f'MALE OK: median pitch {f0:.0f} Hz ({n} voiced frames)')
    elif code == 3: print(f'REFUSED: median pitch {f0:.0f} Hz sounds female (limit {mx:.0f} Hz). This plugin uses male narration only; regenerate with a male voice.')
    else: print('NO SPEECH FOUND: could not measure pitch.')
    sys.exit(code)
