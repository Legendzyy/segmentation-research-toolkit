# SPDX-License-Identifier: AGPL-3.0-or-later
"""Explicit paired summaries; incompatible comparisons fail rather than pool."""
import csv
import json
from pathlib import Path
from .io import fresh_directory, write_json


def summarize(paths, baseline, output):
    records = [json.loads(Path(p).read_text(encoding='utf-8')) for p in paths]
    by_key = {}
    for record in records:
        key = record['variant'], record['seed']
        if key in by_key:
            raise ValueError(f'Duplicate variant/seed: {key}')
        by_key[key] = record
    rows = []
    for r in records:
        if r['variant'] == baseline:
            continue
        b = by_key.get((baseline, r['seed']))
        if b is None:
            raise ValueError(f'Missing paired baseline for seed {r["seed"]}')
        for key in ['dataset_manifest_sha256', 'protocol', 'role']:
            if r[key] != b[key]:
                raise ValueError(f'Incompatible {key}; use a separate system/scale comparison.')
        for key in ['scale', 'epochs', 'batch', 'imgsz', 'weights', 'initialization_sha256']:
            if r['run_config'][key] != b['run_config'][key]:
                raise ValueError(f'Incompatible training setting: {key}')
        if r['run_config'].get('teacher_sha256') and b['run_config'].get('teacher_sha256') and r['run_config']['teacher_sha256'] != b['run_config']['teacher_sha256']:
            raise ValueError('Different teacher identities in paired KD comparison')
        for metric in ['AP','AP50','AP75','AP90','AP_small','AP_medium','AP_large']:
            candidate, reference = r['metrics'][metric], b['metrics'][metric]
            rows.append(dict(variant=r['variant'], baseline=baseline, seed=r['seed'], metric=metric, candidate=candidate, reference=reference,
                             delta_pp=None if candidate is None or reference is None else 100*(candidate-reference), role=r['role']))
    if not rows:
        raise ValueError('No candidate/baseline pairs')
    folder = fresh_directory(output)
    with (folder/'paired.csv').open('w',newline='',encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    write_json(folder/'summary.json',dict(pairs=rows, inference='descriptive paired differences; no significance or causal claim inferred'))
    return {'status':'PASS','rows':len(rows),'output':str(folder/'paired.csv')}
