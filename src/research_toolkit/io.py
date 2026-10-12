# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
import hashlib
import json
import os


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    os.replace(temporary, path)


def fresh_directory(path):
    path = Path(path).resolve()
    if path.exists():
        raise FileExistsError(f'Output already exists: {path}. Choose a new directory; partial runs are retained.')
    path.mkdir(parents=True)
    return path
