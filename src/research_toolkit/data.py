# SPDX-License-Identifier: AGPL-3.0-or-later
"""Explicit YOLO-polygon train/val preparation; never discovers test data."""
from pathlib import Path
import json
import shutil
import urllib.request
import zipfile
import numpy as np
import yaml
from PIL import Image
from .io import fresh_directory, sha256, write_json

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}


def polygons(path, nc):
    result = []
    for lineno, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        values = np.asarray([float(v) for v in line.split()], dtype=np.float64)
        if len(values) < 7 or len(values) % 2 != 1 or not np.isfinite(values).all():
            raise ValueError(f'{path}:{lineno}: expected class + >=3 polygon points')
        cls = int(values[0])
        if values[0] != cls or not 0 <= cls < nc or np.any(values[1:] < 0) or np.any(values[1:] > 1):
            raise ValueError(f'{path}:{lineno}: invalid class or normalized coordinate; no silent clipping')
        xy = values[1:].reshape(-1, 2)
        if len(np.unique(xy, axis=0)) < 3:
            raise ValueError(f'{path}:{lineno}: degenerate polygon')
        result.append((cls, xy))
    return result


def prepare(train_images, train_labels, val_images, val_labels, names, output):
    if not names or len(names) != len(set(names)):
        raise ValueError('Class names must be a nonempty unique ordered list.')
    rows = []
    seen = {}
    sources = []
    for split, images, labels in [('train', train_images, train_labels), ('val', val_images, val_labels)]:
        images, labels = Path(images).resolve(), Path(labels).resolve()
        paths = sorted(p for p in images.rglob('*') if p.suffix.lower() in IMAGE_EXTENSIONS)
        if not paths:
            raise ValueError(f'No images in explicit {split} path: {images}')
        stems = set()
        for path in paths:
            relative = path.relative_to(images)
            stem = relative.with_suffix('').as_posix()
            if stem in stems:
                raise ValueError(f'Ambiguous image stem: {relative}')
            stems.add(stem)
            label = labels / relative.with_suffix('.txt')
            if not label.is_file():
                raise ValueError(f'Missing label: {label}; backgrounds require an explicit empty file.')
            objects = polygons(label, len(names))
            with Image.open(path) as image:
                width, height = image.size
                image.verify()
            digest = sha256(path)
            if digest in seen:
                raise ValueError(f'Duplicate image content: {path} and {seen[digest]}')
            seen[digest] = str(path)
            rows.append(dict(split=split, image=f'images/{split}/{relative.as_posix()}', label=f'labels/{split}/{relative.with_suffix(".txt").as_posix()}', image_sha256=digest, label_sha256=sha256(label), width=width, height=height, instances=len(objects)))
            sources.append((path, label))
    target = fresh_directory(output)
    for row, (image, label) in zip(rows, sources):
        for src, key in [(image, 'image'), (label, 'label')]:
            dest = target/row[key]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
    manifest = {'schema':1, 'role':'new_development_dataset', 'names':names, 'test_access':False, 'samples':rows}
    write_json(target/'manifest.json', manifest)
    (target/'data.yaml').write_text(yaml.safe_dump(dict(path=target.as_posix(), train='images/train', val='images/val', names=names), allow_unicode=True), encoding='utf-8')
    return target/'data.yaml'


def load_prepared(data_yaml, verify=True):
    data_yaml = Path(data_yaml).resolve()
    data = yaml.safe_load(data_yaml.read_text(encoding='utf-8'))
    root = Path(data['path'])
    if not root.is_absolute():
        root = data_yaml.parent/root
    root = root.resolve()
    manifest_path = root/'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if data.get('train') != 'images/train' or data.get('val') != 'images/val' or data['names'] != manifest['names'] or 'test' in data:
        raise ValueError('Use the data.yaml created by prepare-yolo; split/names must match manifest.')
    if verify:
        for row in manifest['samples']:
            for key in ['image', 'label']:
                path = (root/row[key]).resolve()
                if not path.is_relative_to(root) or sha256(path) != row[key+'_sha256']:
                    raise ValueError(f'Dataset file changed/outside root: {row[key]}')
    return root, manifest, sha256(manifest_path)


def fetch_smoke(output):
    target = fresh_directory(output)
    url = 'https://github.com/ultralytics/assets/releases/download/v0.0.0/coco8-seg.zip'
    archive = target/'coco8-seg.zip'
    urllib.request.urlretrieve(url, archive)
    with zipfile.ZipFile(archive) as handle:
        for member in handle.infolist():
            destination = (target/member.filename).resolve()
            if not destination.is_relative_to(target):
                raise ValueError('Archive member escapes destination')
        handle.extractall(target)
    import ultralytics
    description = yaml.safe_load((Path(ultralytics.__file__).parent/'cfg/datasets/coco8-seg.yaml').read_text(encoding='utf-8'))
    names = description['names']
    if isinstance(names, dict):
        names = [names[i] for i in range(len(names))]
    base = target/'coco8-seg'
    prepared = prepare(base/'images/train', base/'labels/train', base/'images/val', base/'labels/val', names, target/'prepared')
    write_json(target/'download.json', dict(url=url, sha256=sha256(archive), role='engineering_smoke_only'))
    return prepared
