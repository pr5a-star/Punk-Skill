"""Validate physical Codex installation copies. Requires Python 3 and PyYAML."""
from pathlib import Path
import hashlib
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('punk-cover', 'punk-avatar', 'punk-ip-video-cover')
errors = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def inventory(directory):
    check(directory.is_dir() and not directory.is_symlink(), f'Not a physical directory: {directory}')
    result = {}
    for file in directory.rglob('*'):
        check(not file.is_symlink(), f'Symlink in installation/source: {file}')
        if file.is_file():
            result[file.relative_to(directory)] = hashlib.sha256(file.read_bytes()).hexdigest()
    return result


for source, installed in [(ROOT / 'skills' / n, ROOT / '.agents/skills' / n) for n in NAMES] + [
    (ROOT / 'styles', ROOT / '.agents/styles')
]:
    expected, actual = inventory(source), inventory(installed)
    check(expected == actual, f'File set or SHA-256 mismatch: {source} -> {installed}')
    print(f'{installed.relative_to(ROOT)}: {len(actual)} files; exact SHA-256 copy={expected == actual}')

for name in NAMES:
    skill = ROOT / '.agents/skills' / name
    text = (skill / 'SKILL.md').read_text()
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    check(bool(match), f'{name}: missing YAML frontmatter')
    if match:
        data = yaml.safe_load(match[1])
        check(isinstance(data, dict), f'{name}: frontmatter must be a mapping')
        if isinstance(data, dict):
            check(data.get('name') == name and len(name) <= 64 and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)), f'{name}: invalid name')
            description = data.get('description')
            check(isinstance(description, str) and 0 < len(description.strip()) <= 1024, f'{name}: invalid description')
    agent = yaml.safe_load((skill / 'agents/openai.yaml').read_text())
    interface = agent.get('interface', {})
    for field in ('display_name', 'short_description', 'default_prompt'):
        check(isinstance(interface.get(field), str) and bool(interface[field].strip()), f'{name}: invalid interface.{field}')
    check(f'${name}' in interface.get('default_prompt', ''), f'{name}: missing invocation in default_prompt')
    check(any((skill / 'references').glob('*.md')), f'{name}: missing references')

# Markdown links are relative to the containing file. Inline resource paths in
# skill instructions are relative to the skill root; shared catalog paths retain
# their documented repository-library meaning, mirrored under .agents/.
for file in (ROOT / '.agents').rglob('*.md'):
    if file.name == 'README.md':
        continue
    text = file.read_text()
    for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', text):
        if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:|#', target):
            continue
        target = target.split('#')[0]
        check((file.parent / target).is_file(), f'Broken Markdown link: {file.relative_to(ROOT)} -> {target}')
    skill = next((ROOT / '.agents/skills' / n for n in NAMES if file.is_relative_to(ROOT / '.agents/skills' / n)), None)
    for target in re.findall(r'`([^`\n]+)`', text):
        if not re.match(r'^(?:\.\./\.\./styles/|references/|styles/)', target) or not target.endswith(('.md', '.yaml')):
            continue
        if '{' in target:
            # Template paths must resolve for every installed shared style.
            if target.startswith('../../styles/{style-id}/'):
                for style in (ROOT / '.agents/styles').iterdir():
                    check((skill / target.replace('{style-id}', style.name)).is_file(), f'Broken style template: {target} ({style.name})')
            continue
        base = skill if skill else file.parent
        if target.startswith('styles/') and skill and skill.name != 'punk-ip-video-cover':
            base = ROOT / '.agents'
        matches = list(base.glob(target)) if '*' in target else [base / target]
        check(bool(matches) and all(p.is_file() for p in matches), f'Broken resource: {file.relative_to(ROOT)} -> {target}')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {checks} integrity, format and resource-path checks (no image generation).')
