"""Check that every file a skill or agent points to exists inside its own plugin,
the way a plugin install sees it (only plugins/<name>/ is copied).

Usage: python3 -I scripts/check-refs.py <dir containing the plugin folders>
"""
import os, re, sys, json

root = sys.argv[1]
problems, checked = [], 0
# Paths that live in the user's working folder or on their computer, not in the plugin.
USER_SIDE = ('profile/', 'tracker/', 'posts/', '~/', 'APPLICATIONS_ROOT', 'RESUME_SOURCE')
# Names of files the skills create in the user's profile/ or output folders, or wording that isn't a path.
EXPECTED = {'.md', 'prep-brief.md', 'humanizer-patterns.md', 'calibration-posts.md', 'interviewer-styles/'}

for plugin in sorted(os.listdir(root)):
    pdir = os.path.join(root, plugin)
    manifest = json.load(open(os.path.join(pdir, '.claude-plugin', 'plugin.json')))
    assert manifest['name'] == plugin, f'{plugin}: manifest name mismatch'
    for dirpath, _, files in os.walk(pdir):
        for f in files:
            if not f.endswith('.md'):
                continue
            path = os.path.join(dirpath, f)
            text = open(path).read()
            rel = os.path.relpath(path, root)
            # Frontmatter check for skills and agents
            if f == 'SKILL.md' or os.path.basename(dirpath) == 'agents':
                m = re.match(r'---\n(.*?)\n---\n', text, re.S)
                if not m or 'name:' not in m.group(1) or 'description:' not in m.group(1):
                    problems.append(f'{rel}: missing frontmatter name/description')
                else:
                    name = re.search(r'name:\s*"?([\w-]+)"?', m.group(1)).group(1)
                    expected = os.path.basename(dirpath) if f == 'SKILL.md' else f[:-3]
                    if name != expected:
                        problems.append(f'{rel}: name "{name}" != folder/file "{expected}"')
            # Backtick tokens that look like files/folders inside the plugin
            if '/evals/' in path:
                continue
            for tok in re.findall(r'`([^`\s]+)`', text):
                tok = tok.rstrip('.,')
                if tok.startswith(USER_SIDE) or '{' in tok or '<' in tok:
                    continue
                if not (tok.endswith('.md') or tok.endswith('/')):
                    continue
                if tok in ('SKILL.md', 'README.md', 'CREDITS.md') or tok in EXPECTED:
                    continue
                checked += 1
                cands = [os.path.normpath(os.path.join(dirpath, tok))]
                # skill-folder-relative paths used from within subfolders (templates/README.md etc.)
                skill_dir = dirpath
                while skill_dir != pdir and not os.path.exists(os.path.join(skill_dir, 'SKILL.md')):
                    skill_dir = os.path.dirname(skill_dir)
                cands.append(os.path.normpath(os.path.join(skill_dir, tok)))
                if not any(os.path.exists(c) for c in cands):
                    problems.append(f'{rel}: reference `{tok}` not found inside plugin "{plugin}"')

print(f'checked {checked} in-plugin references')
print('\n'.join(problems) if problems else 'all references resolve')
sys.exit(1 if problems else 0)
