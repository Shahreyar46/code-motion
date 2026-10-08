#!/usr/bin/env bash
# One-time setup of a video work folder. usage: bash setup.sh [./video] [--three]
# Creates the folder layout, checks node / python / ffmpeg, installs Playwright + Chromium (and Three.js with --three)
# into <folder>/node_modules, and the Python packages numpy + edge-tts.
set -e
DIR="./video"; THREE=0; for a in "$@"; do case "$a" in --three) THREE=1;; --*) ;; *) DIR="$a";; esac; done
mkdir -p "$DIR"/{src,dist,out,audio,assets,stills}
missing=()
command -v node >/dev/null || missing+=("node (https://nodejs.org)")
if ! command -v ffmpeg >/dev/null; then   # cloud/Linux machines: try to install it non-interactively
  if command -v apt-get >/dev/null; then (sudo -n apt-get install -y -qq ffmpeg || apt-get install -y -qq ffmpeg) >/dev/null 2>&1 || true
  elif command -v brew >/dev/null; then brew install ffmpeg >/dev/null 2>&1 || true; fi
fi
command -v ffmpeg >/dev/null || missing+=("ffmpeg (Windows: winget install Gyan.FFmpeg | macOS: brew install ffmpeg | Linux: sudo apt-get install ffmpeg)")
PY=""; for c in python3 python py; do command -v $c >/dev/null && $c -c "import sys; assert sys.version_info>=(3,8)" 2>/dev/null && { PY=$c; break; }; done
[ -z "$PY" ] && missing+=("python 3.8+")
if [ ${#missing[@]} -gt 0 ]; then echo "Missing: ${missing[*]}"; exit 1; fi
pipi(){ "$PY" -m pip install -q "$1" 2>/dev/null || "$PY" -m pip install --user -q "$1" 2>/dev/null || "$PY" -m pip install --user --break-system-packages -q "$1"; }
"$PY" -c "import numpy" 2>/dev/null || pipi numpy || { echo "Could not install numpy (try a venv: python -m venv .venv)"; exit 1; }
"$PY" -c "import edge_tts" 2>/dev/null || pipi edge-tts || echo "Note: edge-tts not installed; voice falls back to other providers."
cd "$DIR"
[ -f package.json ] || echo '{"private":true}' > package.json
[ -d node_modules/playwright ] || { npm install --silent --no-audit --no-fund playwright; npx playwright install chromium || npx playwright install --with-deps chromium; }
[ -f .gitignore ] || printf "node_modules/
dist/
stills/
audio/lines/
" > .gitignore
[ $THREE = 1 ] && { [ -d node_modules/three ] || npm install --silent --no-audit --no-fund three; }
echo "Ready: $(pwd)"
echo "  src/    fragments (video.html) + script.json      dist/   built pages"
echo "  audio/  vo.wav, timings.json, mix.wav             out/    renders + final.mp4"
echo "  stills/ contact sheets                            assets/ logos, screenshots, brand files"
