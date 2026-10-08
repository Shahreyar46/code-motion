"""Build a video fragment into one self-contained HTML page (engine + fonts + VO timings inlined).

usage:
  python build.py <fragment.html> <out.html> [--vo timings.json] [--audio mix.wav]

Fragment format (see references/engine-api.md):
  <title>…</title> <style>…</style>
  <div id="…">markup that goes inside #stage</div>        (everything that is not <title>/<style>/<script>)
  <script>…M.video({...}) or M.morph({...})…</script>
  <script type="module">…</script>                       (optional, e.g. Three.js; `import * as THREE from 'three'`)

motion-broll fragments (data-slot="world|shape|over") are also accepted unchanged.

Fonts: Geist + Geist Mono always; Anton, Caveat, Instrument Serif are inlined only when the fragment names them.
Three.js: when the fragment imports 'three', an import map is written and three.module.min.js is copied next to
out.html (./three/) from ./node_modules/three (run setup first). Pages with modules must be served over http (engine/serve.js,
render.js and stills.js do this automatically)."""
import base64, json, re, sys, shutil, pathlib, argparse

E = pathlib.Path(__file__).resolve().parent
FONTS = {  # family -> (file, format, always)
    'Geist': ('Geist-Variable.woff2', 'woff2', True),
    'Geist Mono': ('GeistMono-Medium.woff2', 'woff2', True),
    'Anton': ('Anton-Regular.ttf', 'truetype', False),
    'Caveat': ('Caveat-Variable.ttf', 'truetype', False),
    'Instrument Serif': ('InstrumentSerif-Regular.ttf', 'truetype', False),
}
CLASS_HINT = {'Anton': 'anton', 'Caveat': 'hand', 'Instrument Serif': 'serif'}


def font_css(frag):
    out = []
    for fam, (f, fmt, always) in FONTS.items():
        used = always or fam in frag or re.search(r'class="[^"]*\b%s\b' % CLASS_HINT.get(fam, '#none#'), frag)
        if used:
            b = base64.b64encode((E / 'fonts' / f).read_bytes()).decode()
            out.append(f"@font-face{{font-family:'{fam}';src:url(data:font/{fmt};base64,{b}) format('{fmt}');font-weight:100 900;font-display:block}}")
    return '\n'.join(out)


def find_three(start):
    for d in [start, *start.parents, pathlib.Path.cwd(), *pathlib.Path.cwd().parents]:
        b = d / 'node_modules' / 'three' / 'build'
        for name in ('three.module.min.js', 'three.module.js'):
            if (b / name).exists():
                return b / name
    return None


def build(src, dst, vo=None, audio=None):
    src, dst = pathlib.Path(src), pathlib.Path(dst)
    frag = src.read_text(encoding='utf-8')
    m = re.search(r'<title>(.*?)</title>', frag, re.S)
    title = m.group(1).strip() if m else src.stem
    css = ''.join(re.findall(r'<style>(.*?)</style>', frag, re.S))
    scripts = re.findall(r'<script(\s[^>]*)?>(.*?)</script>', frag, re.S)
    classic = ''.join(body for attrs, body in scripts if 'module' not in (attrs or ''))
    modules = [body for attrs, body in scripts if 'module' in (attrs or '')]
    body = re.sub(r'<title>.*?</title>|<style>.*?</style>|<script(\s[^>]*)?>.*?</script>', '', frag, flags=re.S).strip()

    if 'data-slot="shape"' in frag:  # motion-broll fragment
        slot = lambda n: (re.search(rf'<div data-slot="{n}">(.*?)</div><!--/{n}-->', frag, re.S) or [None, ''])[1]
        body = f'<div id="world">{slot("world")}<div id="shape">{slot("shape")}</div>{slot("over")}</div><div id="cursor"></div>'

    pre = ''
    if vo:
        pre += 'window.VO=' + json.dumps(json.loads(pathlib.Path(vo).read_text(encoding='utf-8'))) + ';'
    if audio:
        dst.parent.mkdir(parents=True, exist_ok=True)
        a = pathlib.Path(audio)
        target = dst.parent / a.name
        if a.resolve() != target.resolve():
            shutil.copyfile(a, target)
        pre += f'window.AUDIO_SRC={json.dumps(a.name)};'

    head_extra = ''
    if any(re.search(r"from\s+['\"]three", mod) for mod in modules):
        three = find_three(src.parent)
        if not three:
            sys.exit('Fragment imports three but node_modules/three was not found. Run: npm install three  (in your work folder)')
        dst.parent.mkdir(parents=True, exist_ok=True)
        tdir = dst.parent / 'three'
        tdir.mkdir(exist_ok=True)
        for f in three.parent.glob('three.*js'):          # module + core (r160+ splits them); skip webgpu/tsl builds
            if 'webgpu' not in f.name and 'tsl' not in f.name and not f.name.endswith('.cjs'):
                shutil.copyfile(f, tdir / f.name)
        addons = three.parent.parent / 'examples' / 'jsm'
        imap = {'imports': {'three': './three/' + three.name}}
        if addons.exists() and re.search(r"three/addons/", ''.join(modules)):
            dst_add = dst.parent / 'three-addons'
            if not dst_add.exists():
                shutil.copytree(addons, dst_add)
            imap['imports']['three/addons/'] = './three-addons/'
        head_extra = f'<script type="importmap">{json.dumps(imap)}</script>'

    base = (E / 'base.css').read_text(encoding='utf-8')
    engine = (E / 'motion.js').read_text(encoding='utf-8')
    mods = ''.join(f'<script type="module">{mod}</script>' for mod in modules)
    html = (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>{head_extra}'
            f'<style>{font_css(frag)}\n{base}\n{css}</style></head><body>\n'
            f'<div id="wrap"><div id="stage">{body}</div></div>\n'
            f'<script>{pre}</script><script>{engine}</script><script>{classic}</script>{mods}</body></html>')
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding='utf-8')
    print('built', dst, f'({len(html)//1024} KB)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--vo'); ap.add_argument('--audio')
    a = ap.parse_args()
    build(a.src, a.dst, a.vo, a.audio)
