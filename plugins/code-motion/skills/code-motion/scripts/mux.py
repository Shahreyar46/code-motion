"""Put the mix under the rendered video and master loudness for social/web: -14 LUFS integrated, -1.5 dBTP.
usage: python mux.py <video.mp4> <mix.wav> <final.mp4> [--lufs -14]
Two-pass ffmpeg loudnorm (measure, then apply linearly) so dynamics are kept. Audio is cut/padded to the video length."""
import json, re, subprocess, sys, argparse

ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('mix'); ap.add_argument('out'); ap.add_argument('--lufs', type=float, default=-14)
a = ap.parse_args()
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', a.video], capture_output=True, text=True, check=True).stdout.strip())
base = f'I={a.lufs}:TP=-1.5:LRA=11'
m = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.mix, '-af', f'apad,atrim=0:{dur},loudnorm={base}:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
j = json.loads(re.findall(r'\{[^{}]*\}', m.stderr, re.S)[-1])
af = (f'apad,atrim=0:{dur},loudnorm={base}:measured_I={j["input_i"]}:measured_TP={j["input_tp"]}:measured_LRA={j["input_lra"]}'
      f':measured_thresh={j["input_thresh"]}:offset={j["target_offset"]}:linear=true,aresample=48000')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', a.video, '-i', a.mix, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-af', af, '-c:a', 'aac', '-b:a', '256k', '-t', f'{dur}', '-movflags', '+faststart', a.out], check=True)
chk = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.out, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
k = json.loads(re.findall(r'\{[^{}]*\}', chk.stderr, re.S)[-1])
print(f'final {a.out}: {dur:.2f}s, {k["input_i"]} LUFS, {k["input_tp"]} dBTP (input mix was {j["input_i"]} LUFS)')
