# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""Simple additive direct output KD plus the frozen K1 neck-feature MSE.

This is a training-only complementarity control, not a new mechanism claim.
Inference remains the original student graph.
"""
from __future__ import annotations

import torch
from torch import nn

from .output_kd import InstanceOutputDistiller


class CombinedOutputFeatureDistiller(InstanceOutputDistiller):
    NECK = (16, 19, 22)

    def __init__(self, teacher_checkpoint: str, student_model: nn.Module, *,
                 lambda_cls: float, lambda_box: float, lambda_mask: float,
                 lambda_fd: float, adapter_seed: int):
        assert lambda_fd > 0
        super().__init__(teacher_checkpoint, student_model, mode="direct",
                         lambda_cls=lambda_cls, lambda_box=lambda_box,
                         lambda_mask=lambda_mask)
        assert tuple(self.get_distill_layers(student_model)[:-1]) == self.NECK
        dims = [(self._student_feats[i].shape[1], self._teacher_feats[i].shape[1])
                for i in self.NECK]
        device = next(student_model.parameters()).device
        # Adapter initialization has its own stream; shared model and data RNG
        # are not perturbed by the extra training-only parameters.
        devices = [device.index if device.index is not None else torch.cuda.current_device()] \
            if device.type == "cuda" else []
        with torch.random.fork_rng(devices=devices):
            torch.manual_seed(adapter_seed)
            self.projector = nn.ModuleList(
                nn.Conv2d(source, target, kernel_size=1, bias=True)
                for source, target in dims
            ).to(device)
        self.feats_idx = list(self.NECK)
        self._register_feature_hooks()
        self.lambda_fd = float(lambda_fd)
        self.adapter_seed = int(adapter_seed)
        self._freeze_teacher()

    def loss(self, batch, preds=None):
        if not self.training:
            base, items = super().loss(batch, preds)
            zero = base.new_zeros(1)
            items["fd_loss"] = zero.squeeze().detach()
            return torch.cat((base, zero)), items
        self._teacher_feats.clear()
        self._student_feats.clear()
        base, items = super().loss(batch, preds)
        terms = []
        for layer, adapter in zip(self.NECK, self.projector):
            source = adapter(self._student_feats[layer]).float()
            target = self._teacher_feats[layer].float().detach()
            assert source.shape == target.shape, (layer, source.shape, target.shape)
            terms.append((source - target).square().mean(dim=1, keepdim=True).mean())
        fd = torch.stack(terms).mean()
        assert torch.isfinite(fd).all()
        items["fd_loss"] = (self.lambda_fd * fd).detach()
        return torch.cat((base, (self.lambda_fd * fd * batch["img"].shape[0]).reshape(1))), items
