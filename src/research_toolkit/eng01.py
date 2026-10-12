# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""Preserve native YOLO11 semantics while adding one detail adapter and optional train-only head."""
from __future__ import annotations

import copy
import sys

import torch
from .settings import BOUNDARY_CONFIG as CONFIG
import torch.nn as nn
import torch.nn.functional as F
import yaml
from .third_party.mlca import MLCA
from ultralytics import YOLO
from ultralytics.nn.modules.block import Proto as NativeProto
from ultralytics.nn.modules.conv import Conv
from ultralytics.nn.modules.head import Detect, Segment as NativeSegment
import ultralytics.nn.modules as modules
import ultralytics.nn.modules.head as head_module
import ultralytics.nn.tasks as tasks

VARIANTS = ("E0", "E1", "E2", "E3", "E4", "E5")
DETAIL_VARIANTS = {"E1", "E2", "E3", "E5"}
BOUNDARY_VARIANTS = {"E4", "E5"}


class DetailAdapter(nn.Module):
    def __init__(self, input_channels: int, width: int):
        super().__init__()
        self.project = Conv(input_channels, width, 1)
        self.depthwise = nn.Sequential(
            nn.Conv2d(width, width, 3, padding=1, groups=width, bias=False),
            nn.BatchNorm2d(width), nn.SiLU(),
        )

    def forward(self, detail: torch.Tensor, target_shape: tuple[int, int]):
        value = self.project(detail)
        if value.shape[-2:] != target_shape:
            value = F.interpolate(value, size=target_shape, mode="bilinear", align_corners=False)
        return value, self.depthwise(value)


class ENGProto(NativeProto):
    def __init__(self, c1: int, c_: int, c2: int, detail_channels: int | None, variant: str):
        super().__init__(c1, c_, c2)
        self.variant = variant
        self.has_detail = variant in DETAIL_VARIANTS
        self.width = min(CONFIG["detail_width"], c_) if self.has_detail else 0
        if self.has_detail:
            self.adapter = DetailAdapter(int(detail_channels), self.width)
            self.output_project = nn.Conv2d(self.width, c_, 1, bias=True)
            nn.init.zeros_(self.output_project.weight)
            nn.init.zeros_(self.output_project.bias)
            if variant == "E2":
                self.mlca = MLCA(self.width)  # official defaults: local_size=5, gamma=2, b=1, weight=.5
                # Torch 2.1 fused AdamW requires the parameter and gradient
                # strides to agree. The official global Conv1d has a singleton
                # middle dimension; its backward gradient arrives as (k, 1, 1)
                # rather than the default (k, k, 1). Re-stride the same values
                # so the operation and initialization are unchanged.
                weight = self.mlca.conv.weight
                target_stride = (weight.shape[-1], 1, 1)
                if weight.stride() != target_stride:
                    with torch.no_grad():
                        storage = torch.empty_strided(weight.shape, target_stride,
                                                      dtype=weight.dtype, device=weight.device)
                        storage.copy_(weight)
                        weight.data = storage
            if variant in {"E3", "E5"}:
                self.semantic_project = nn.Conv2d(c_, self.width, 1, bias=True)
                self.gate = nn.Conv2d(2 * self.width, 1, 1, bias=True)

    def forward_with_feature(self, semantic: torch.Tensor, detail: torch.Tensor | None = None):
        u = self.cv2(self.upsample(self.cv1(semantic)))
        if self.has_detail:
            assert detail is not None
            value, adapted = self.adapter(detail, u.shape[-2:])
            if self.variant == "E2":
                adapted = self.mlca(adapted)
            if self.variant in {"E3", "E5"}:
                gating = torch.sigmoid(self.gate(torch.cat((self.semantic_project(u), value), 1)))
                adapted = gating * adapted
            u = u + self.output_project(adapted)
        return self.cv3(u), u

    def forward(self, semantic: torch.Tensor, detail: torch.Tensor | None = None):
        return self.forward_with_feature(semantic, detail)[0]


class BoundaryHead(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(channels, 16, 1, bias=False), nn.BatchNorm2d(16), nn.SiLU(),
            nn.Conv2d(16, 16, 3, padding=1, groups=16, bias=False), nn.BatchNorm2d(16), nn.SiLU(),
            nn.Conv2d(16, 1, 1, bias=True),
        )

    def forward(self, x):
        return self.layers(x)


class ENGSegment(NativeSegment):
    def __init__(self, nc=80, nm=32, npr=256, variant="E1", reg_max=16, end2end=False, ch=()):
        assert variant in VARIANTS[1:]
        detail_present = variant in DETAIL_VARIANTS
        assert len(ch) == (4 if detail_present else 3), (variant, ch)
        semantic_channels = ch[1] if detail_present else ch[0]
        detection_channels = ch[1:] if detail_present else ch
        super().__init__(nc, nm, npr, reg_max, end2end, detection_channels)
        self.variant = variant
        self.has_boundary = variant in BOUNDARY_VARIANTS
        self.proto = ENGProto(semantic_channels, self.npr, self.nm, ch[0] if detail_present else None, variant)
        if self.has_boundary:
            self.boundary_head = BoundaryHead(self.npr)

    def forward(self, x):
        detail = x[0] if self.variant in DETAIL_VARIANTS else None
        detector_features = x[1:] if detail is not None else x
        outputs = Detect.forward(self, detector_features)
        preds = outputs[1] if isinstance(outputs, tuple) else outputs
        prototype, u = self.proto.forward_with_feature(detector_features[0], detail)
        if "one2one" in preds:
            preds["one2many"]["proto"] = prototype
            preds["one2one"]["proto"] = prototype.detach()
            if self.training and self.has_boundary:
                preds["one2many"]["boundary_logit"] = self.boundary_head(u)
        else:
            preds["proto"] = prototype
            if self.training and self.has_boundary:
                preds["boundary_logit"] = self.boundary_head(u)
        if self.training:
            return preds
        return (outputs, prototype) if self.export else ((outputs[0], prototype), preds)

    def strip_boundary_head(self):
        if self.has_boundary:
            del self.boundary_head
            self.has_boundary = False

