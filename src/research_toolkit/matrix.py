# SPDX-License-Identifier: AGPL-3.0-or-later
"""Run a registered ablation matrix sequentially in isolated processes."""
import json
from pathlib import Path
import subprocess
import sys
from .io import fresh_directory, write_json
from .ablation import summarize


def run(config, data, output, teacher=None):
    plan = json.loads(Path(config).read_text(encoding='utf-8'))
    variants, seeds = plan['variants'], plan['seeds']
    from .models import VARIANTS
    if not variants or len(variants)!=len(set(variants)) or not set(variants)<=set(VARIANTS):
        raise ValueError('Invalid/duplicate variants')
    if not seeds or len(seeds)!=len(set(seeds)) or plan['baseline'] not in variants:
        raise ValueError('Require unique seeds and baseline in the matrix')
    if any(v.startswith(('eng02:','eng03:','eng04:')) for v in variants):
        teacher = teacher or plan['training'].get('teacher')
        if not teacher or not Path(teacher).is_file():
            raise ValueError('KD matrix requires an existing --teacher checkpoint before any job starts')
    folder=fresh_directory(output)
    data=str(Path(data).resolve())
    write_json(folder/'matrix.json',plan)
    records=[];metrics=[]
    for seed in seeds:
        for variant in variants:
            name=variant.replace(':','_')+f'_s{seed}'
            job=dict(plan['training'],variant=variant,seed=seed)
            if teacher and variant.startswith(('eng02:','eng03:','eng04:')):
                job['teacher']=str(Path(teacher).resolve())
            cfg=folder/(name+'.json');write_json(cfg,job)
            record=dict(variant=variant,seed=seed,status='RUNNING');records.append(record)
            write_json(folder/'queue.json',records)
            try:
                with (folder/(name+'.log')).open('w',encoding='utf-8') as log:
                    subprocess.run([sys.executable,'-m','research_toolkit','train','--config',str(cfg),'--data',data,'--output',str(folder/name)],stdout=log,stderr=subprocess.STDOUT,check=True)
                    subprocess.run([sys.executable,'-m','research_toolkit','evaluate','--run',str(folder/name),'--data',data,'--output',str(folder/(name+'_eval')),'--reference-size',str(plan['reference_size'])],stdout=log,stderr=subprocess.STDOUT,check=True)
                metrics.append(folder/(name+'_eval')/'metrics.json')
                record['status']='PASS'
            except Exception:
                record['status']='FAILED';write_json(folder/'queue.json',records);raise
            write_json(folder/'queue.json',records)
            print(f'Completed {name}',flush=True)
    return summarize(metrics,plan['baseline'],folder/'summary')
