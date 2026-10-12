# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check that training-only components do not alter deployment predictions."""
import json
from pathlib import Path
import torch
from .io import sha256


def flatten(value):
    if torch.is_tensor(value):
        return [value.detach().clone()]
    if isinstance(value,dict):
        return [tensor for key in sorted(value) for tensor in flatten(value[key])]
    if isinstance(value,(tuple,list)):
        return [tensor for item in value for tensor in flatten(item)]
    return []


def verify(run_dir):
    run_dir=Path(run_dir)
    plan=json.loads((run_dir/'run.json').read_text(encoding='utf-8'))
    receipt=json.loads((run_dir/'completion.json').read_text(encoding='utf-8'))
    if sha256(run_dir/'deploy.pt')!=receipt['checkpoint_sha256']:
        raise ValueError('Deployment checkpoint changed')
    torch.set_num_threads(2)
    training=torch.load(run_dir/'train/weights/last.pt',map_location='cpu',weights_only=False)['ema'].float().eval()
    deployed=torch.load(run_dir/'deploy.pt',map_location='cpu',weights_only=False)['model'].float().eval()
    if hasattr(deployed,'teacher_model') or hasattr(deployed.model[-1],'boundary_head'):
        raise AssertionError('Training-only components remain in deploy graph')
    generator=torch.Generator().manual_seed(123)
    image=torch.rand(1,3,plan['imgsz'],plan['imgsz'],generator=generator)
    with torch.no_grad():
        expected=flatten(training(image));actual=flatten(deployed(image))
    if len(expected)!=len(actual):
        raise AssertionError('Deployment output structure differs')
    for a,b in zip(expected,actual):
        torch.testing.assert_close(a,b,rtol=0,atol=0)
    return dict(status='PASS',tensors=len(actual),input_size=plan['imgsz'],scope='exact CPU forward parity: last-epoch EMA versus exported deployment graph')
