"""Create and verify a portable SHA256 inventory of explicitly allowed text files."""

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path, PurePosixPath


SCHEMA = "research-text-manifest-v1"
EXCLUDED_DIRS = frozenset({
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules",
    "work", "outputs", "data", "datasets", "weights", "checkpoints",
    "predictions", "artifacts", "runs", "upstream", ".idea", ".vscode",
})
EXTENSIONS = frozenset({".md", ".json", ".csv", ".py", ".yml", ".yaml", ".toml", ".txt"})
NAMES = frozenset({"LICENSE", ".gitignore", ".gitattributes"})
MAX_BYTES = 2 * 1024 * 1024


def inventory(root, exclude=None):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Root must be a directory")
    exclude = None if exclude is None else Path(exclude).resolve()
    entries = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        for name in dirs:
            path = Path(base) / name
            if path.is_symlink() or os.path.islink(path) or path.resolve().parent != Path(base).resolve():
                raise ValueError("Linked directories are not supported")
        for name in sorted(files):
            path = Path(base) / name
            if path.name.startswith(".env"):
                continue
            if path.suffix.lower() not in EXTENSIONS and name not in NAMES:
                continue
            if path.is_symlink():
                raise ValueError("Linked files are not supported")
            if path.resolve() == exclude:
                continue
            raw = path.read_bytes()
            if len(raw) > MAX_BYTES:
                raise ValueError("Allowed text file exceeds the 2 MiB limit")
            raw.decode("utf-8-sig")
            key = path.relative_to(root).as_posix()
            entries[key] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return dict(sorted(entries.items()))


def create(root, destination):
    destination = Path(destination)
    if destination.exists():
        raise ValueError("Refusing to overwrite an existing manifest")
    entries = inventory(root, exclude=destination)
    result = {"schema": SCHEMA, "scope": "allowed_text_only_not_all_research_assets", "files": entries}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    return result


def verify(root, manifest):
    manifest = Path(manifest)
    expected = json.loads(manifest.read_text(encoding="utf-8"))
    if expected.get("schema") != SCHEMA or not isinstance(expected.get("files"), dict):
        raise ValueError("Unsupported manifest schema")
    entries = expected["files"]
    for key, record in entries.items():
        path = PurePosixPath(key)
        if (not key or path.is_absolute() or ".." in path.parts or "\\" in key
                or ":" in key or path.as_posix() != key):
            raise ValueError("Manifest paths must be normalized relative paths")
        if not isinstance(record, dict) or set(record) != {"bytes", "sha256"}:
            raise ValueError("Invalid file record")
        if (type(record["bytes"]) is not int or record["bytes"] < 0
                or not isinstance(record["sha256"], str) or len(record["sha256"]) != 64
                or any(c not in "0123456789abcdef" for c in record["sha256"])):
            raise ValueError("Invalid byte count or SHA256")
    actual = inventory(root, exclude=manifest)
    missing = sorted(set(entries) - set(actual))
    added = sorted(set(actual) - set(entries))
    changed = sorted(k for k in set(entries) & set(actual) if entries[k] != actual[k])
    return {"status": "PASS" if not (missing or added or changed) else "FAIL",
            "missing": missing, "added": added, "changed": changed,
            "scope": "allowed_text_only_not_all_research_assets"}


def refresh(root, manifest):
    """Explicitly accept a changed inventory, keeping the previous bytes locally.

    This is not a secrecy review or a scientific approval. Never call from CI.
    """
    root = Path(root).resolve(strict=True)
    manifest = Path(manifest)
    if manifest.is_symlink():
        raise ValueError("Linked manifest files are not supported")
    difference = verify(root, manifest)
    if difference["status"] == "PASS":
        return {"status": "UNCHANGED", "difference": difference}
    original = manifest.read_bytes()
    old_hash = hashlib.sha256(original).hexdigest()
    result = {"schema": SCHEMA, "scope": "allowed_text_only_not_all_research_assets",
              "files": inventory(root, exclude=manifest)}
    backup_dir = root / "work" / "manifest_history"
    # Do not redirect the local backup through a link or junction.
    if backup_dir.resolve() != backup_dir:
        raise ValueError("Manifest backup directory must not be linked")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{old_hash}.json"
    if backup.exists():
        if backup.read_bytes() != original:
            raise ValueError("Existing backup content does not match its hash")
    else:
        with backup.open("xb") as handle:
            handle.write(original)
    fd, temporary_name = tempfile.mkstemp(prefix=".manifest-", suffix=".tmp", dir=manifest.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
        os.replace(temporary, manifest)
    finally:
        temporary.unlink(missing_ok=True)
    return {"status": "REFRESHED", "previous_sha256": old_hash,
            "backup": backup.relative_to(root).as_posix(), "difference": difference}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("create", "verify", "refresh"))
    parser.add_argument("root", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        result = {"create": create, "verify": verify, "refresh": refresh}[args.operation](args.root, args.manifest)
    except (OSError, ValueError, UnicodeError) as error:
        parser.exit(2, f"Manifest error: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.operation == "verify" and result["status"] != "PASS":
        parser.exit(1)


if __name__ == "__main__":
    main()
