# SPDX-License-Identifier: AGPL-3.0-or-later
"""Portable run scheduling around archived model/loss implementations."""
import copy
import json
import platform
from pathlib import Path
import time
import torch
import yaml
import ultralytics
from ultralytics import YOLO
from ultralytics.models.yolo.segment.train import SegmentationTrainer
from .data import load_prepared
from .io import fresh_directory, sha256, write_json
from .models import architecture, distiller
from .settings import UPSTREAM_COMMIT


class ResearchTrainer(SegmentationTrainer):
    plan = None

    def get_model(self, cfg=None, weights=None, verbose=True):
        student = super().get_model(cfg, weights, verbose)
        student.args = self.args
        model = distiller(self.plan['variant'], student, self.plan.get('teacher'))
        if hasattr(model, 'teacher_model'):
            if model.teacher_model.model[-1].nc != self.data['nc']:
                raise ValueError('Teacher class count differs from dataset. Train a native teacher on the same class mapping.')
            if model.teacher_model.names != student.names:
                raise ValueError('Teacher/student class names differ; do not transfer across unmatched class identities.')
        return model

    def validate(self):
        # All ports use the separately versioned COCO evaluator, including
        # doubled prototype grids unsupported by the historic validator.
        return self.metrics, 0.0

    def final_eval(self):
        return None

    def resume_training(self, ckpt):
        if self.resume:
            raise ValueError('Automatic resume is not supported; retain failed run and start a new output directory.')
        return super().resume_training(ckpt)

    def save_model(self):
        if self.batch_size != self.plan['batch']:
            raise RuntimeError('Trainer changed the requested batch; this run is not comparable.')
        for model in [self.model, self.ema.ema]:
            for value in model.state_dict().values():
                if value.is_floating_point() and (not torch.isfinite(value).all() or value.abs().max() > 65504):
                    raise RuntimeError('Nonfinite/fp16-overflow state; refusing silently sanitized checkpoint.')
        return super().save_model()


def run(plan, data, output):
    plan = dict(plan)
    required = {'variant','scale','epochs','batch','imgsz','seed','device','workers','weights','purpose'}
    if required - plan.keys():
        raise ValueError(f'Missing run fields: {sorted(required-plan.keys())}')
    if plan.keys() - required - {'teacher'}:
        raise ValueError(f'Unknown run fields: {sorted(plan.keys()-required-{"teacher"})}')
    if plan['purpose'] not in {'engineering_smoke', 'new_experiment'}:
        raise ValueError('purpose must be engineering_smoke or new_experiment; historical outcomes are immutable.')
    if plan['imgsz'] < 64 or plan['imgsz'] % 32 or plan['batch'] < 1 or plan['epochs'] < 1:
        raise ValueError('imgsz must be >=64 and divisible by 32; epochs/batch positive.')
    root, manifest, manifest_hash = load_prepared(data)
    if plan['variant'].startswith(('eng02:', 'eng03:', 'eng04:')):
        if not plan.get('teacher') or not Path(plan['teacher']).is_file():
            raise ValueError('A same-task teacher checkpoint is required via --teacher.')
        plan['teacher'] = str(Path(plan['teacher']).resolve())
    if plan['device'] != 'cpu' and ',' in str(plan['device']):
        raise ValueError('Single-device runner only; DDP has not been ported.')
    folder = fresh_directory(output)
    plan.update(dataset_manifest_sha256=manifest_hash, upstream_commit=UPSTREAM_COMMIT, checkpoint_policy='last_scheduled_epoch_EMA', evaluation='coco-mask-reference-grid-v1')
    if plan.get('teacher'):
        plan['teacher_sha256'] = sha256(plan['teacher'])
    write_json(folder/'run.json', plan)
    write_json(folder/'environment.json', dict(python=platform.python_version(), torch=torch.__version__, ultralytics=ultralytics.__version__, platform=platform.platform()))
    variant = plan['variant']
    model_config = architecture(variant, plan['scale'], len(manifest['names']))
    model_file = folder/f'yolo11{plan["scale"]}-research.yaml'
    model_file.write_text(yaml.safe_dump(model_config, sort_keys=False), encoding='utf-8')
    if variant in {'eng01:E4', 'eng01:E5'}:
        from .boundary import install_training_hooks
        install_training_hooks()
    torch.manual_seed(plan['seed'])
    torch.set_num_threads(2)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    wrapper = YOLO(str(model_file), task='segment')
    weights = plan['weights']
    if weights and weights != 'none':
        wrapper.load(weights)
        plan['initialization_sha256'] = sha256(wrapper.ckpt_path)
    else:
        plan['initialization_sha256'] = None
    plan['architecture_sha256'] = sha256(model_file)
    write_json(folder/'run.json', plan)
    ResearchTrainer.plan = plan
    if variant.startswith('eng04:'):
        multiplier = .25 if variant == 'eng04:X0' else 1.
        def schedule(trainer):
            trainer.model.kd_scale = multiplier * min(1., (trainer.epoch + 1)/3)
        wrapper.add_callback('on_train_epoch_start', schedule)
    started = time.perf_counter()
    try:
        wrapper.train(trainer=ResearchTrainer, data=str(Path(data).resolve()), epochs=plan['epochs'], batch=plan['batch'], imgsz=plan['imgsz'],
                      device=plan['device'], workers=plan['workers'], project=str(folder), name='train', exist_ok=False,
                      pretrained=bool(weights and weights != 'none'), optimizer='AdamW', seed=plan['seed'], deterministic=True,
                      patience=0, val=False, plots=False, save=True, save_period=-1, cache=False, amp=plan['device'] != 'cpu',
                      lr0=.001, lrf=.01, momentum=.937, weight_decay=.0005, warmup_epochs=3, warmup_momentum=.8,
                      warmup_bias_lr=0., close_mosaic=5, hsv_h=.015, hsv_s=.7, hsv_v=.4, degrees=0., translate=.1,
                      scale=.5, shear=0., perspective=0., flipud=0., fliplr=.5, mosaic=1., mixup=0., cutmix=0.,
                      copy_paste=0., overlap_mask=True, mask_ratio=4, nbs=32, cls_remap=True, verbose=False)
        last = folder/'train/weights/last.pt'
        ckpt = torch.load(last, map_location='cpu', weights_only=False)
        if ckpt['epoch'] + 1 != plan['epochs']:
            raise RuntimeError('Run did not reach the requested last epoch.')
        model = copy.deepcopy(ckpt['ema']).float()
        if hasattr(model, 'student_model'):
            model._remove_feature_hooks()
            model = model.student_model
        if hasattr(model.model[-1], 'strip_boundary_head'):
            model.model[-1].strip_boundary_head()
        model.criterion = None
        deploy = folder/'deploy.pt'
        torch.save(dict(model=model, ema=None, train_args=ckpt['train_args'], epoch=ckpt['epoch'], version=ultralytics.__version__), deploy)
        receipt = dict(status='PASS', role=plan['purpose'], variant=variant, seed=plan['seed'], epochs=plan['epochs'], dataset_manifest_sha256=manifest_hash,
                       checkpoint='deploy.pt', checkpoint_sha256=sha256(deploy), training_checkpoint_sha256=sha256(last),
                       elapsed_s=time.perf_counter()-started, test_access=False)
        write_json(folder/'completion.json', receipt)
        return receipt
    except Exception as exc:
        write_json(folder/'failure.json', dict(status='FAILED', error=repr(exc), elapsed_s=time.perf_counter()-started))
        raise
