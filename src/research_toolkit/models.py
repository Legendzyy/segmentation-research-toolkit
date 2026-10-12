# SPDX-License-Identifier: AGPL-3.0-or-later
"""Portable builders for the original method classes."""
import copy
from pathlib import Path
import yaml
import ultralytics
from ultralytics.nn.modules.head import Segment as NativeSegment
from . import eng01, factorial

VARIANTS = ['native'] + ['eng01:' + v for v in eng01.VARIANTS] + ['p1f:' + v for v in factorial.VARIANTS] + ['eng02:K1', 'eng02:K2'] + ['eng03:' + v for v in ['D0', 'Q0', 'M0', 'C0', 'R0', 'F0']] + ['eng04:' + v for v in ['X0', 'I0', 'I1', 'J0']]


def register(variant):
    import ultralytics.nn.modules as modules
    import ultralytics.nn.modules.head as head
    import ultralytics.nn.tasks as tasks
    if variant not in VARIANTS:
        raise ValueError(f'Unknown variant: {variant}')
    cls = NativeSegment
    if variant.startswith('eng01:') and variant != 'eng01:E0':
        cls = eng01.ENGSegment
    elif variant.startswith('p1f:'):
        cls = factorial.FactorialSegment
    tasks.Segment = modules.Segment = head.Segment = cls


def architecture(variant, scale, nc):
    if scale not in {'n', 's'}:
        raise ValueError('Only YOLO11 n/s are ported and checked.')
    if variant != 'native' and scale != 'n':
        raise ValueError('Historical method ports use the n student; use native+s for the teacher.')
    register(variant)
    base = Path(ultralytics.__file__).parent / 'cfg/models/11/yolo11-seg.yaml'
    model = yaml.safe_load(base.read_text(encoding='utf-8'))
    model = copy.deepcopy(model)
    model.update(nc=nc, scale=scale)
    model['head'][-1] = [[16, 19, 22], 1, 'Segment', ['nc', 32, 256]]
    if variant.startswith('eng01:') and variant != 'eng01:E0':
        tag = variant.split(':')[1]
        sources = [2, 16, 19, 22] if tag in eng01.DETAIL_VARIANTS else [16, 19, 22]
        model['head'][-1] = [sources, 1, 'Segment', ['nc', 32, 256, tag]]
    elif variant.startswith('p1f:'):
        tag = variant.split(':')[1]
        model['head'][-1] = [[factorial.SOURCE_LAYER[tag], 16, 19, 22], 1, 'Segment', ['nc', 32, factorial.NPR_YAML[tag], tag]]
    return model


def distiller(variant, student, teacher):
    if variant.startswith('eng02:'):
        from .feature_kd import ENG02FeatureDistiller
        return ENG02FeatureDistiller(teacher, student, mode=variant.split(':')[1], lambda_fd=1.)
    if variant.startswith('eng03:'):
        tag = variant.split(':')[1]
        if tag == 'F0':
            from .combined_kd import CombinedOutputFeatureDistiller
            return CombinedOutputFeatureDistiller(teacher, student, lambda_cls=1., lambda_box=5., lambda_mask=1., lambda_fd=1., adapter_seed=102024)
        from .output_kd import InstanceOutputDistiller
        mode = {'D0':'direct', 'Q0':'selective', 'M0':'mask_selective', 'C0':'det_selective', 'R0':'rank_mask_selective'}[tag]
        return InstanceOutputDistiller(teacher, student, mode=mode, lambda_cls=1., lambda_box=5., lambda_mask=1.)
    if variant.startswith('eng04:'):
        from .transfer import TransferModel
        return TransferModel(teacher, student, variant.split(':')[1])
    return student
