# SPDX-License-Identifier: AGPL-3.0-or-later
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Native segmentation research: portable training, evaluation and ablation')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('variants')
    p = sub.add_parser('fetch-smoke'); p.add_argument('--output', required=True)
    p = sub.add_parser('prepare-yolo')
    for name in ['train-images','train-labels','val-images','val-labels','output']:
        p.add_argument('--'+name, required=True)
    p.add_argument('--names', nargs='+', required=True)
    p = sub.add_parser('train')
    p.add_argument('--config', required=True); p.add_argument('--data', required=True); p.add_argument('--output', required=True)
    for field, kind in [('variant',str),('scale',str),('epochs',int),('batch',int),('imgsz',int),('seed',int),('device',str),('workers',int),('weights',str),('teacher',str)]:
        p.add_argument('--'+field, type=kind)
    p = sub.add_parser('evaluate'); p.add_argument('--run',required=True); p.add_argument('--data',required=True); p.add_argument('--output',required=True); p.add_argument('--reference-size',type=int,default=640)
    p = sub.add_parser('replay'); p.add_argument('--evaluation',required=True)
    p = sub.add_parser('check-deploy'); p.add_argument('--run',required=True)
    p = sub.add_parser('summarize'); p.add_argument('--metrics',nargs='+',required=True); p.add_argument('--baseline',required=True); p.add_argument('--output',required=True)
    p = sub.add_parser('matrix'); p.add_argument('--config',required=True); p.add_argument('--data',required=True); p.add_argument('--output',required=True); p.add_argument('--teacher')
    args = parser.parse_args()
    os.environ.setdefault('YOLO_CONFIG_DIR',str(Path('work/runtime/yolo').resolve()))
    os.environ['YOLO_AUTOINSTALL']='false'
    os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
    from ultralytics import settings
    settings.update({k:False for k in ['sync','wandb','mlflow','clearml','comet','neptune','hub','dvc','tensorboard'] if k in settings})
    if args.command == 'variants':
        from .models import VARIANTS
        result = {'variants':VARIANTS}
    elif args.command == 'fetch-smoke':
        from .data import fetch_smoke
        result = {'data':str(fetch_smoke(args.output))}
    elif args.command == 'prepare-yolo':
        from .data import prepare
        result = {'data':str(prepare(args.train_images,args.train_labels,args.val_images,args.val_labels,args.names,args.output))}
    elif args.command == 'train':
        from .train import run
        plan = json.loads(Path(args.config).read_text(encoding='utf-8'))
        for key in ['variant','scale','epochs','batch','imgsz','seed','device','workers','weights','teacher']:
            value = getattr(args,key)
            if value is not None:
                plan[key] = value
        result = run(plan,args.data,args.output)
    elif args.command == 'evaluate':
        from .evaluate import run
        result = run(args.run,args.data,args.output,args.reference_size)
    elif args.command == 'replay':
        from .evaluate import replay
        result = replay(args.evaluation)
    elif args.command == 'check-deploy':
        from .deployment import verify
        result = verify(args.run)
    elif args.command == 'matrix':
        from .matrix import run
        result = run(args.config,args.data,args.output,args.teacher)
    else:
        from .ablation import summarize
        result = summarize(args.metrics,args.baseline,args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
