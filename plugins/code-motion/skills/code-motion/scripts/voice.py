"""Voiceover: script.json -> vo.wav + timings.json (line and word times the animation syncs to).

usage: python voice.py script.json <out_dir> [--provider auto|gemini|elevenlabs|edge|sapi] [--voice NAME] [--list]

script.json:
{
  "voice": {"provider": "auto", "gemini": "Charon", "edge": "en-US-AndrewNeural", "elevenlabs": "pNInz6obpgDQGcFmaJgB",
            "sapi": "Microsoft David Desktop", "rate": "+0%", "style": "Read like a calm, confident product-film narrator. Warm, natural, unhurried."},
  "lead_in": 0.5,            # silence before the first line (seconds)
  "gap": 0.35,               # default silence between lines
  "lines": [
    {"id": "hook", "text": "Your inbox is lying to you."},
    {"id": "problem", "text": "Three hundred unread. Two that matter.", "pause": 0.6}   # pause = silence AFTER this line
  ]
}

Male voices only: voices that are (or may be) female are refused (see references/content-policy.md).

Providers (auto picks the first available, falls back on failure):
  gemini      GEMINI_API_KEY or GOOGLE_API_KEY. Most natural; follows the "style" direction. Model: env CM_GEMINI_TTS_MODEL.
  elevenlabs  ELEVENLABS_API_KEY. Very natural; real per-character timestamps.
  edge        free Microsoft neural voices via the edge-tts package (online, no key). Real word timestamps.
  sapi        Windows offline voice. Robotic; last resort, no text leaves the machine.
gemini/elevenlabs/edge send the script text to that provider's cloud service.

Each line is synthesised separately, so line boundaries are exact and one bad line can be regenerated alone
(delete <out_dir>/lines/<id>.wav and run again: existing lines are reused when their text+voice is unchanged)."""
import argparse, asyncio, base64, hashlib, json, os, pathlib, shutil, subprocess, sys, time, urllib.request, urllib.error, wave
import numpy as np

SR = 48000
MALE = {
    'gemini': ['Charon (informative, default)', 'Orus (firm)', 'Iapetus (clear)', 'Algenib (gravelly)', 'Alnilam (firm)',
               'Schedar (even)', 'Sadaltager (knowledgeable)', 'Achird (friendly)', 'Umbriel (easy-going)', 'Fenrir (excitable)', 'Puck (upbeat)'],
    'edge': ['en-US-AndrewNeural (warm, default)', 'en-US-BrianNeural (casual)', 'en-US-GuyNeural (newscast)', 'en-US-ChristopherNeural (authoritative)',
             'en-US-EricNeural', 'en-US-DavisNeural', 'en-GB-RyanNeural (British)', 'en-AU-WilliamNeural (Australian)', 'en-IN-PrabhatNeural (Indian)'],
    'elevenlabs': ['pNInz6obpgDQGcFmaJgB (Adam, default)', 'ErXwobaYiN019PkySvjV (Antoni)', 'TxGEqnHWrfWFTfGW9XjX (Josh)', 'VR6AewLTigWG4xSOukaG (Arnold)'],
    'sapi': ['Microsoft David Desktop'],
}
GEMINI_MALE = {'Puck', 'Charon', 'Fenrir', 'Orus', 'Enceladus', 'Iapetus', 'Umbriel', 'Algieba', 'Algenib', 'Rasalgethi',
               'Alnilam', 'Schedar', 'Achird', 'Zubenelgenubi', 'Sadachbia', 'Sadaltager'}


class FemaleVoice(Exception):
    pass


def check_male(provider, voice):
    """This plugin narrates with male voices only. Raise FemaleVoice when a voice is (or may be) female."""
    if provider == 'gemini' and voice not in GEMINI_MALE:
        raise FemaleVoice(f'Gemini voice "{voice}" is not in the male voice list: {", ".join(sorted(GEMINI_MALE))}')
    if provider == 'edge':
        import edge_tts
        vs = asyncio.run(edge_tts.list_voices())
        g = next((v.get('Gender') for v in vs if v.get('ShortName') == voice), None)
        if g != 'Male':
            raise FemaleVoice(f'edge voice "{voice}" is not a male voice (gender: {g})')
    if provider == 'elevenlabs':
        key = os.environ.get('ELEVENLABS_API_KEY', '')
        req = urllib.request.Request(f'https://api.elevenlabs.io/v1/voices/{voice}', headers={'xi-api-key': key})
        with urllib.request.urlopen(req, timeout=30) as r:
            g = (json.loads(r.read()).get('labels') or {}).get('gender', '')
        if g.lower() != 'male':
            raise FemaleVoice(f'ElevenLabs voice "{voice}" is not labelled male (gender: {g or "unknown"})')


DEFAULTS = {'gemini': 'Charon', 'edge': 'en-US-AndrewNeural', 'elevenlabs': 'pNInz6obpgDQGcFmaJgB', 'sapi': 'Microsoft David Desktop'}


def ff_to_wav(src_args, dst):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *src_args, '-ac', '1', '-ar', str(SR), '-sample_fmt', 's16', str(dst)], check=True)


def read_wav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def write_wav(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(p), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())


def speech_bounds(x, thr_db=-42):
    """first/last sample above threshold (20ms RMS windows)."""
    n = int(0.02 * SR); m = len(x) // n
    if m == 0: return 0, len(x)
    rms = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1) + 1e-12)
    on = np.where(20 * np.log10(rms) > thr_db)[0]
    if not len(on): return 0, len(x)
    return on[0] * n, min(len(x), (on[-1] + 1) * n)


def estimate_words(text, x):
    """spread words over the voiced region by character weight (±0.15s). Used when a provider gives no timings."""
    a, b = speech_bounds(x); ws = text.split(); wt = np.array([len(w) + 1.5 for w in ws], float)
    edges = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
    return [{'w': w, 'start': (a + (b - a) * edges[i]) / SR, 'end': (a + (b - a) * edges[i + 1]) / SR} for i, w in enumerate(ws)]


def http_json(url, body, headers, tries=4):
    data = json.dumps(body).encode()
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', **headers})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors='ignore')[:300]
            if e.code in (429, 500, 503) and k < tries - 1:
                time.sleep(4 * (k + 1)); continue
            raise RuntimeError(f'HTTP {e.code}: {msg}')


# ---------------- providers: each returns (wav_path, words|None) ----------------
def tts_gemini(text, voice, style, out):
    key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not key: raise RuntimeError('no GEMINI_API_KEY')
    model = os.environ.get('CM_GEMINI_TTS_MODEL', 'gemini-2.5-flash-preview-tts')
    prompt = f'{style}\n\n{text}' if style else text
    body = {'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['AUDIO'],
                                 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voice}}}}}
    r = http_json(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', body, {'x-goog-api-key': key})
    part = r['candidates'][0]['content']['parts'][0]['inlineData']
    raw = out.with_suffix('.pcm'); raw.write_bytes(base64.b64decode(part['data']))
    rate = 24000
    if 'rate=' in part.get('mimeType', ''): rate = int(part['mimeType'].split('rate=')[1].split(';')[0])
    ff_to_wav(['-f', 's16le', '-ar', str(rate), '-ac', '1', '-i', str(raw)], out); raw.unlink()
    return out, None


def tts_elevenlabs(text, voice, style, out):
    key = os.environ.get('ELEVENLABS_API_KEY')
    if not key: raise RuntimeError('no ELEVENLABS_API_KEY')
    body = {'text': text, 'model_id': os.environ.get('CM_ELEVEN_MODEL', 'eleven_multilingual_v2'),
            'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.15, 'use_speaker_boost': True}}
    r = http_json(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128', body, {'xi-api-key': key})
    mp3 = out.with_suffix('.mp3'); mp3.write_bytes(base64.b64decode(r['audio_base64']))
    ff_to_wav(['-i', str(mp3)], out); mp3.unlink()
    al = r.get('alignment') or {}
    ch, st, en = al.get('characters', []), al.get('character_start_times_seconds', []), al.get('character_end_times_seconds', [])
    words, cur = [], None
    for c, s, e in zip(ch, st, en):
        if c.isspace():
            if cur: words.append(cur); cur = None
            continue
        if cur is None: cur = {'w': c, 'start': s, 'end': e}
        else: cur['w'] += c; cur['end'] = e
    if cur: words.append(cur)
    return out, words or None


def tts_edge(text, voice, style, out, rate='+0%'):
    import edge_tts
    async def go():
        comm = edge_tts.Communicate(text, voice, rate=rate, boundary='WordBoundary')
        audio, words = bytearray(), []
        async for ch in comm.stream():
            if ch['type'] == 'audio': audio += ch['data']
            elif ch['type'] == 'WordBoundary':
                s = ch['offset'] / 1e7; words.append({'w': ch['text'], 'start': s, 'end': s + ch['duration'] / 1e7})
        return bytes(audio), words
    audio, words = asyncio.run(go())
    if not audio: raise RuntimeError('edge-tts returned no audio')
    mp3 = out.with_suffix('.mp3'); mp3.write_bytes(audio); ff_to_wav(['-i', str(mp3)], out); mp3.unlink()
    return out, words or None


def tts_sapi(text, voice, style, out):
    if os.name != 'nt': raise RuntimeError('sapi is Windows only')
    tmp = out.with_suffix('.sapi.wav'); txt = out.with_suffix('.txt'); txt.write_text(text, encoding='utf-8')
    ps = ("Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"try {{ $s.SelectVoice('{voice}') }} catch {{ $s.SelectVoiceByHints('Male') }}; "
          "if ($s.Voice.Gender -ne 'Male') { $s.SelectVoiceByHints('Male') }; if ($s.Voice.Gender -ne 'Male') { exit 3 }; "
          f"$s.Rate=0; $s.SetOutputToWaveFile('{tmp}'); "
          f"$s.Speak([IO.File]::ReadAllText('{txt}')); $s.Dispose()")
    r = subprocess.run(['powershell', '-NoProfile', '-Command', ps])
    if r.returncode == 3: raise FemaleVoice('no male Windows voice installed')
    r.check_returncode()
    ff_to_wav(['-i', str(tmp)], out); tmp.unlink(); txt.unlink()
    return out, None


PROVIDERS = {'gemini': tts_gemini, 'elevenlabs': tts_elevenlabs, 'edge': tts_edge, 'sapi': tts_sapi}


def available():
    order = []
    if os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY'): order.append('gemini')
    if os.environ.get('ELEVENLABS_API_KEY'): order.append('elevenlabs')
    try:
        import edge_tts  # noqa
        order.append('edge')
    except ImportError: pass
    if os.name == 'nt': order.append('sapi')
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('script', nargs='?'); ap.add_argument('out', nargs='?')
    ap.add_argument('--provider'); ap.add_argument('--voice'); ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list or not a.script:
        print('available here:', ', '.join(available()) or 'none (pip install edge-tts)')
        for p, vs in MALE.items(): print(f'\n{p} male voices:\n  ' + '\n  '.join(vs))
        return
    S = json.loads(pathlib.Path(a.script).read_text(encoding='utf-8'))
    V = S.get('voice', {}); out = pathlib.Path(a.out); (out / 'lines').mkdir(parents=True, exist_ok=True)
    want = a.provider or V.get('provider', 'auto')
    chain = available() if want == 'auto' else [want] + [p for p in available() if p != want]
    style = V.get('style', 'Read like a calm, confident product-film narrator. Warm, natural, unhurried, with clear emphasis on key words.')
    lead, gap = float(S.get('lead_in', 0.5)), float(S.get('gap', 0.35))
    cache_f = out / 'lines' / 'cache.json'
    cache = json.loads(cache_f.read_text()) if cache_f.exists() else {}
    used, timeline, chunks, t = set(), [], [np.zeros(int(lead * SR), np.float32)], lead
    for ln in S['lines']:
        lid, text = ln['id'], ln['text'].strip()
        wav = out / 'lines' / f'{lid}.wav'
        words = None
        for p in chain:
            voice = a.voice if (a.voice and p == chain[0]) else V.get(p, DEFAULTS[p])
            sig = hashlib.sha1(f'{p}|{voice}|{style}|{V.get("rate","")}|{text}'.encode()).hexdigest()
            if wav.exists() and cache.get(lid, {}).get('sig') == sig:
                words = cache[lid].get('words'); used.add(p); break
            try:
                if p != 'sapi': check_male(p, voice)
                kw = {'rate': V.get('rate', '+0%')} if p == 'edge' else {}
                _, words = PROVIDERS[p](text, voice, style, wav, **kw)
                cache[lid] = {'sig': sig, 'words': words, 'provider': p, 'voice': voice}; used.add(p)
                print(f'  {lid}: {p}/{voice}')
                break
            except FemaleVoice as e:
                sys.exit(f'Refused: {e}. This plugin uses male narration only; pick a voice from: python voice.py --list')
            except Exception as e:
                print(f'  {lid}: {p} failed ({str(e)[:160]}), trying next', file=sys.stderr)
        else:
            sys.exit(f'all providers failed for line {lid}')
        x = read_wav(wav)
        # trim provider padding to ~60ms each side so pacing is controlled by lead/gap/pause, not by the TTS engine
        a0, b0 = speech_bounds(x); a0 = max(0, a0 - int(0.06 * SR)); b0 = min(len(x), b0 + int(0.09 * SR))
        if words is None: words = estimate_words(text, x)
        x = x[a0:b0]; off = a0 / SR
        fade = int(0.008 * SR); x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
        ws = [{'w': w['w'], 'start': round(t + max(0, w['start'] - off), 3), 'end': round(t + max(0, w['end'] - off), 3)} for w in words]
        dur = len(x) / SR
        timeline.append({'id': lid, 'text': text, 'start': round(t, 3), 'end': round(t + dur, 3), 'words': ws})
        chunks.append(x); t += dur
        pause = float(ln.get('pause', gap)); chunks.append(np.zeros(int(pause * SR), np.float32)); t += pause
    cache_f.write_text(json.dumps(cache, indent=1))
    vo = np.concatenate(chunks)
    peak = np.abs(vo).max() or 1; vo = vo / peak * 0.89  # -1 dBFS peak; final loudness is set at mux
    write_wav(out / 'vo.wav', vo)
    # male-voice gate on the real audio (catches female-sounding voices whatever their name or source)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import voicecheck
    code, f0, _ = voicecheck.check(out / 'vo.wav')
    if code == 3:
        (out / 'vo.wav').rename(out / 'vo.REFUSED-female.wav')
        sys.exit(f'REFUSED: the narration sounds female (median pitch {f0:.0f} Hz). Male voice only: pick another male voice (python voice.py --list) and run again.')
    if f0: print(f'voice check: male, median pitch {f0:.0f} Hz')
    T = {'duration': round(len(vo) / SR, 3), 'providers': sorted(used), 'lines': timeline}
    (out / 'timings.json').write_text(json.dumps(T, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'vo.wav {T["duration"]}s, {len(timeline)} lines via {", ".join(sorted(used))} -> {out / "timings.json"}')
    for l in timeline: print(f'  {l["start"]:6.2f}-{l["end"]:6.2f}  {l["id"]}: {l["text"][:70]}')


if __name__ == '__main__':
    main()
