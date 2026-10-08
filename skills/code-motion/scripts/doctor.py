"""Environment check: can this machine/sandbox make code-motion videos? Prints PASS/FAIL per requirement and
tries to fix what it can (pip installs). Safe to run anywhere (local PC, Claude Code cloud, claude.ai sandbox).
usage: python doctor.py [--fix]"""
import importlib, os, shutil, subprocess, sys, tempfile, time

FIX = '--fix' in sys.argv
R = []


def check(name, ok, detail='', hint=''):
    R.append((name, ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  ({detail})' if detail else '') + ('' if ok or not hint else f'\n      fix: {hint}'))
    return ok


def run(cmd, timeout=60):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout); return p.returncode == 0, (p.stdout + p.stderr).strip()
    except Exception as e:
        return False, str(e)


def pip(pkg):
    for extra in ([], ['--user'], ['--user', '--break-system-packages']):
        ok, _ = run([sys.executable, '-m', 'pip', 'install', '-q', *extra, pkg], 300)
        if ok: return True
    return False


def has_mod(m):
    try: importlib.import_module(m); return True
    except Exception: return False


print(f'code-motion doctor  ·  python {sys.version.split()[0]}  ·  {sys.platform}\n')
check('python >= 3.8', sys.version_info >= (3, 8))

for mod, pkg in (('numpy', 'numpy'), ('edge_tts', 'edge-tts')):
    if not has_mod(mod) and FIX: pip(pkg)
    check(f'python package {pkg}', has_mod(mod), hint=f'pip install {pkg}')

ff = shutil.which('ffmpeg')
if not ff and FIX and pip('imageio-ffmpeg'):
    try:
        import imageio_ffmpeg; ff = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception: pass
check('ffmpeg', bool(ff), ff or '', 'install ffmpeg (winget install Gyan.FFmpeg / brew install ffmpeg / apt install ffmpeg) or pip install imageio-ffmpeg')

node = shutil.which('node')
ok, out = run(['node', '-v']) if node else (False, '')
check('node >= 18', ok and int(out.lstrip('v').split('.')[0]) >= 18 if ok else False, out, 'install Node.js 18+ (https://nodejs.org)')

# headless browser: the Node Playwright that setup.sh installs (./video/node_modules), else Python Playwright
browser_ok, why, engine = False, 'playwright not installed (run setup.sh)', None
def node_pw_dir():
    for d in (os.getcwd(), os.path.join(os.getcwd(), 'video'), os.path.dirname(os.getcwd())):
        if os.path.isdir(os.path.join(d, 'node_modules', 'playwright')): return os.path.join(d, 'node_modules')
def node_js(js, nm, timeout=180):
    try:
        p = subprocess.run(['node', '-e', js], capture_output=True, text=True, timeout=timeout, env={**os.environ, 'NODE_PATH': nm})
        return p.returncode == 0, (p.stdout + p.stderr).strip()
    except Exception as e:
        return False, str(e)
NODE_PROBE = "require('playwright').chromium.launch().then(async b=>{const p=await b.newPage();await p.setContent('<b>ok</b>');console.log(await p.innerText('b'));await b.close()}).catch(e=>{console.log('ERR '+e.message.split(String.fromCharCode(10))[0]);process.exit(1)})"
nm = node_pw_dir() if node else None
if nm:
    ok, out = node_js(NODE_PROBE, nm)
    if ok and out.endswith('ok'): browser_ok, why, engine = True, f'node playwright ({nm})', 'node'
    else: why = out[-160:]
if not browser_ok:
    if not has_mod('playwright') and FIX: pip('playwright')
    if has_mod('playwright'):
        if FIX: run([sys.executable, '-m', 'playwright', 'install', 'chromium'], 600)
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(); pg = b.new_page(); pg.set_content('<b id=x>ok</b>'); browser_ok = pg.inner_text('#x') == 'ok'; b.close()
            why, engine = 'python playwright', 'python'
        except Exception as e:
            why = str(e).splitlines()[0][:160]
check('headless chromium (renders frames)', browser_ok, why, 'run setup.sh, or: pip install playwright && python -m playwright install chromium (needs internet access to the Playwright CDN)')

# network: free voice + package downloads
net = {}
for host, url in (('edge-tts voice', 'https://speech.platform.bing.com'), ('npm registry', 'https://registry.npmjs.org'), ('pypi', 'https://pypi.org/simple/')):
    try:
        import urllib.request; urllib.request.urlopen(url, timeout=8); net[host] = True
    except Exception as e:
        net[host] = 'HTTP Error' in str(e) or '404' in str(e) or '403' in str(e)  # reachable even if it refuses the bare URL
    check(f'internet: {host}', net[host], hint='allow network access for this environment')

if has_mod('edge_tts') and net.get('edge-tts voice'):
    try:
        import asyncio, edge_tts
        async def go():
            a = b''
            async for c in edge_tts.Communicate('Test.', 'en-US-AndrewNeural').stream():
                if c['type'] == 'audio': a += c['data']
            return len(a)
        n = asyncio.run(go()); check('voice synthesis (edge-tts, male)', n > 1000, f'{n} bytes')
    except Exception as e:
        check('voice synthesis (edge-tts, male)', False, str(e)[:120], 'needs internet; or set GEMINI_API_KEY / ELEVENLABS_API_KEY')
check('premium voice key (optional)', True, 'GEMINI_API_KEY set' if os.environ.get('GEMINI_API_KEY') else ('ELEVENLABS_API_KEY set' if os.environ.get('ELEVENLABS_API_KEY') else 'none, free voice will be used'))

if browser_ok and ff:
    SPEED = "require('playwright').chromium.launch().then(async b=>{const p=await b.newPage({viewport:{width:1920,height:1080}});await p.setContent('<div style=width:1920px;height:1080px;background:#2B4BF0></div>');const t=Date.now();for(let i=0;i<10;i++)await p.screenshot({type:'jpeg',quality:90});console.log((10000/(Date.now()-t)).toFixed(2));await b.close()})"
    fps = None
    if engine == 'node':
        ok, out = node_js(SPEED, nm)
        try: fps = float(out.split()[-1])
        except Exception: pass
    else:
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080}); pg.set_content('<div style="width:1920px;height:1080px;background:#2B4BF0"></div>')
                t = time.time()
                for _ in range(10): pg.screenshot(type='jpeg', quality=90)
                fps = 10 / (time.time() - t); b.close()
        except Exception: pass
    w = max(1, min(4, (os.cpu_count() or 2) // 2))
    check('render speed', bool(fps), f'~{fps:.1f} test captures/s per worker, {w} workers -> 30s at 60fps final ~ {30*60*4/(fps/10)/w/60:.0f} min (real scenes ~10x heavier than the test)' if fps else 'could not measure')

need = ['python >= 3.8', 'python package numpy', 'ffmpeg', 'headless chromium (renders frames)']
ready = all(ok for n, ok in R if n in need)
print('\nRESULT:', 'READY to render videos here.' if ready else 'NOT READY: fix the FAIL lines above (run with --fix to try automatic fixes).')
if ready and not shutil.which('node'):
    print('note: node not found; render.js needs Node. Use the Python render fallback if provided, or install Node.')
