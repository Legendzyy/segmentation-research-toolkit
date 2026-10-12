# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""Training-only neck feature distillation for the frozen ENG02 KD branch.

K1 and K2 share the same student, teacher, adapters, and native loss. K2 only
changes the spatial reduction weights of the feature MSE.
"""
from __future__ import annotations

import math
import torch
from torch import nn

from ultralytics.nn.distill_model import DistillationModel


class ENG02FeatureDistiller(DistillationModel):
    """YOLO11n-seg student with a frozen YOLO11s-seg teacher at neck P3/P4/P5."""

    NECK = (16, 19, 22)

    def __init__(self, teacher_checkpoint: str, student_model: nn.Module, *, mode: str, lambda_fd: float):
        assert mode in {"K1", "K2"}
        assert lambda_fd > 0
        # The upstream wrapper supplies hook-safe deepcopy/checkpoint semantics,
        # student-only inference, and native trainer/EMA integration.
        super().__init__(teacher_checkpoint, student_model)
        assert tuple(self.feats_idx[:-1]) == self.NECK
        student_dims = [self._student_feats[i].shape[1] for i in self.NECK]
        teacher_dims = [self._teacher_feats[i].shape[1] for i in self.NECK]
        self._remove_feature_hooks()
        self.feats_idx = list(self.NECK)
        self.projector = nn.ModuleList(
            nn.Conv2d(s, t, kernel_size=1, bias=True) for s, t in zip(student_dims, teacher_dims)
        ).to(next(student_model.parameters()).device)
        self._register_feature_hooks()
        self.mode = mode
        self.lambda_fd = float(lambda_fd)
        self.teacher_checkpoint = str(teacher_checkpoint)

    @staticmethod
    def _foreground_weights(batch: dict, height: int, width: int, dtype: torch.dtype) -> torch.Tensor:
        """Rasterize post-augmentation GT boxes and normalize weights to unit mean per image."""
        images = batch["img"]
        mask = torch.zeros((images.shape[0], 1, height, width), device=images.device, dtype=torch.bool)
        boxes = batch["bboxes"].float()
        indices = batch["batch_idx"].view(-1).long()
        assert len(boxes) == len(indices)
        for box, index in zip(boxes.detach().cpu().tolist(), indices.detach().cpu().tolist()):
            assert 0 <= int(index) < len(mask)
            cx, cy, bw, bh = box
            x0 = max(0, min(width - 1, int((cx - bw / 2) * width)))
            y0 = max(0, min(height - 1, int((cy - bh / 2) * height)))
            x1 = max(x0 + 1, min(width, math.ceil((cx + bw / 2) * width)))
            y1 = max(y0 + 1, min(height, math.ceil((cy + bh / 2) * height)))
            mask[index, :, y0:y1, x0:x1] = True
        weights = 1.0 + mask.to(dtype=dtype)  # foreground 2, background 1
        return weights / weights.mean(dim=(2, 3), keepdim=True)

    def loss(self, batch, preds=None):
        if not self.training:
            if preds is None:
                preds = self.student_model(batch["img"])
            native, items = self.student_model.loss(batch, preds)
            zero = native.new_zeros(1)
            items["fd_loss"] = zero.squeeze().detach()
            return torch.cat((native, zero)), items
        self._teacher_feats.clear()
        self._student_feats.clear()
        with torch.no_grad():
            self.teacher_model(batch["img"])
        predictions = self.student_model(batch["img"])
        native, items = self.student_model.loss(batch, predictions)
        terms = []
        for layer, adapter in zip(self.NECK, self.projector):
            source = adapter(self._student_feats[layer]).float()
            target = self._teacher_feats[layer].float().detach()
            assert source.shape == target.shape, (layer, source.shape, target.shape)
            squared = (source - target).square().mean(dim=1, keepdim=True)
            if self.mode == "K2":
                weights = self._foreground_weights(batch, squared.shape[-2], squared.shape[-1], squared.dtype)
                squared = squared * weights
            terms.append(squared.mean())
        fd = torch.stack(terms).mean()
        assert torch.isfinite(fd).all()
        items["fd_loss"] = (self.lambda_fd * fd).detach()
        return torch.cat((native, (self.lambda_fd * fd * batch["img"].shape[0]).reshape(1))), items
