"""Verify the selected native archive; this does not execute research code."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def verify():
    errors = []
    index = json.loads((ROOT / 'evidence/NATIVE_SOURCE_MAP.json').read_text(encoding='utf-8'))
    names = [entry['published'] for entry in index['files']]
    if len(names) != len(set(names)):
        errors.append('duplicate published paths')
    if len(names) != 127:
        errors.append(f'expected 127 selected native files, found {len(names)}')
    selected = set(names)
    code_index = ROOT / 'evidence/CODE_SOURCE_MAP.json'
    if code_index.is_file():
        for entry in json.loads(code_index.read_text(encoding='utf-8'))['files']:
            path = ROOT / entry['published']
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry['published_sha256']:
                errors.append(f'ported source hash mismatch: {entry["published"]}')
    counts = {}
    csv_rows = {}
    for entry in index['files']:
        name = entry['published']
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT) or not path.is_file():
            errors.append(f'missing or out-of-root file: {name}')
            continue
        if entry['source'] != name:
            errors.append(f'native layout changed: {name}')
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['published_sha256']:
            errors.append(f'hash mismatch: {name}')
        counts[path.suffix] = counts.get(path.suffix, 0) + 1
        try:
            if path.suffix == '.json':
                json.loads(data)
            elif path.suffix == '.csv':
                with path.open(encoding='utf-8', newline='') as handle:
                    rows = list(csv.reader(handle))
                if not rows or len(set(rows[0])) != len(rows[0]):
                    errors.append(f'invalid/duplicate CSV header: {name}')
                elif any(len(row) != len(rows[0]) for row in rows[1:]):
                    errors.append(f'inconsistent CSV columns: {name}')
                csv_rows[name] = len(rows) - 1
            elif path.suffix == '.png':
                if not data.startswith(b'\x89PNG\r\n\x1a\n'):
                    errors.append(f'invalid PNG signature: {name}')
                if entry['source_sha256'] != entry['published_sha256']:
                    errors.append(f'original figure altered: {name}')
            else:
                data.decode('utf-8')
        except (UnicodeError, ValueError, csv.Error) as exc:
            errors.append(f'{name}: {exc}')
    if counts != {'.md': 95, '.json': 17, '.csv': 10, '.png': 5}:
        errors.append(f'unexpected native file mix: {counts}')

    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(part in {'.git', '__pycache__', '.venv', 'work', 'build', 'dist'} or part.endswith('.egg-info') for part in relative.parts):
            continue
        if not path.is_file():
            continue
        name = relative.as_posix()
        if relative.parts[0] in {'engineering', 'diagnostics'} and len(relative.parts) > 2 and name not in selected:
            errors.append(f'unlisted stage asset: {name}')
        if path.suffix.lower() in {'.pt', '.pth', '.ckpt', '.npy', '.npz', '.pkl', '.zip', '.jpg', '.jpeg', '.pem', '.key'}:
            errors.append(f'excluded asset type: {name}')
        if path.suffix != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        # Ignore code examples, validate local Markdown link destinations.
        text = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^\n)]*)\)', text):
            target = target.strip().strip('<>')
            if re.match(r'^(https?://|mailto:|#)', target):
                continue
            target = unquote(target.split('#')[0])
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(ROOT) or not resolved.exists():
                errors.append(f'broken local link: {name} -> {target}')

    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(names)} native files, hashes, formats, local links and excluded asset types')
    print('CSV data rows: ' + json.dumps(csv_rows, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(verify())
