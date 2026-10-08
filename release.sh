#!/usr/bin/env bash
# Release a new version of the code-motion plugin.
# usage: ./release.sh 1.1.0 "Short summary of what changed"
#
# Bumps plugins/code-motion/.claude-plugin/plugin.json, prepends CHANGELOG.md, validates the plugin,
# commits, tags vX.Y.Z and pushes main + tag. The GitHub Action then publishes a Release.
# Users with auto-update on get the new version the next time Claude Code starts;
# others run: /plugin marketplace update code-motion
set -euo pipefail
cd "$(dirname "$0")"

VER="${1:-}"; NOTES="${2:-}"
[[ "$VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "usage: ./release.sh X.Y.Z \"what changed\""; exit 1; }
[ -n "$NOTES" ] || { echo "Give release notes as the second argument."; exit 1; }
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || { echo "Switch to main first."; exit 1; }
python tools/sync_presets.py >/dev/null 2>&1 || python3 tools/sync_presets.py >/dev/null
[ -z "$(git status --porcelain)" ] || { echo "Uncommitted changes (or presets out of sync after tools/sync_presets.py): commit them first."; exit 1; }
git rev-parse "v$VER" >/dev/null 2>&1 && { echo "Tag v$VER already exists."; exit 1; }

PY=""; for c in python3 python py; do command -v $c >/dev/null && $c -c "import sys" 2>/dev/null && { PY=$c; break; }; done
[ -n "$PY" ] || { echo "python is required"; exit 1; }

OLD=$("$PY" - <<EOF
import json; print(json.load(open('plugins/code-motion/.claude-plugin/plugin.json'))['version'])
EOF
)
"$PY" - "$VER" "$NOTES" <<'EOF'
import json, sys, datetime, pathlib
ver, notes = sys.argv[1], sys.argv[2]
p = pathlib.Path('plugins/code-motion/.claude-plugin/plugin.json'); d = json.loads(p.read_text(encoding='utf-8'))
old = tuple(map(int, d['version'].split('.'))); new = tuple(map(int, ver.split('.')))
if new <= old: sys.exit(f'new version {ver} must be greater than {d["version"]}')
d['version'] = ver; p.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
c = pathlib.Path('CHANGELOG.md'); txt = c.read_text(encoding='utf-8') if c.exists() else '# Changelog\n'
head, _, rest = txt.partition('\n')
entry = f'\n## v{ver} ({datetime.date.today().isoformat()})\n' + ''.join(f'- {n.strip()}\n' for n in notes.split(';') if n.strip())
c.write_text(head + '\n' + entry + rest, encoding='utf-8')
EOF

if command -v claude >/dev/null; then
  claude plugin validate ./ >/dev/null && claude plugin validate ./plugins/code-motion >/dev/null && claude plugin validate ./plugins/code-motion/commands >/dev/null && claude plugin validate ./plugins/code-motion/skills >/dev/null \
    || { echo "Validation failed; reverting."; git checkout -- plugins/code-motion/.claude-plugin/plugin.json CHANGELOG.md; exit 1; }
fi

git add plugins/code-motion/.claude-plugin/plugin.json CHANGELOG.md
git commit -q -m "release: v$VER"
git tag -a "v$VER" -m "v$VER: $NOTES"
git push -q origin main
git push -q origin "v$VER"
echo "Released v$VER (was v$OLD). GitHub Action will publish the Release."
