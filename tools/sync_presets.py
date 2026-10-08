"""Copy the plugin's command presets into the skill (references/presets/) so an uploaded skill
(claude.ai Skills, no plugin) gets the same per-type guidance. Run by release.sh before every release."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent / 'plugins' / 'code-motion'
dst = root / 'skills' / 'code-motion' / 'references' / 'presets'
dst.mkdir(parents=True, exist_ok=True)
for f in sorted((root / 'commands').glob('*.md')):
    s = f.read_text(encoding='utf-8')
    s = re.sub(r'^---\n.*?\n---\n', '', s, count=1, flags=re.S)
    s = s.replace('${CLAUDE_PLUGIN_ROOT}/skills/code-motion/', '').replace('${CLAUDE_PLUGIN_ROOT}/skills/code-motion', "this skill's folder")
    s = s.replace('${CLAUDE_PLUGIN_ROOT}/commands/', 'references/presets/').replace('`commands/', '`references/presets/')
    s = s.replace('Request: $ARGUMENTS', "Request: the user's message (flags like --auto, --music, --unattended may appear in it)").replace('$ARGUMENTS', "the user's request")
    (dst / f.name).write_text(f'<!-- generated from commands/{f.name} by tools/sync_presets.py; edit the command, not this file -->\n' + s, encoding='utf-8')
print('synced', len(list(dst.glob('*.md'))), 'presets ->', dst)
