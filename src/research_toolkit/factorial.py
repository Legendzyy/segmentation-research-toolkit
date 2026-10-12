# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""P1F frozen source × lattice model definitions and builders."""
import torch
import copy, yaml
import torch.nn as nn
import torch.nn.functional as F

from ultralytics import YOLO
from ultralytics.nn.modules.conv import Conv
from ultralytics.nn.modules.head import Detect, Segment as NativeSegment
import ultralytics.nn.modules as modules
import ultralytics.nn.modules.head as head_module
import ultralytics.nn.tasks as tasks

NATIVE_SEGMENT = NativeSegment
VARIANTS = ("F00", "F10", "F01", "F11", "CUP", "CCOMP")
SOURCE_LAYER = {"F00": 16, "F10": 2, "F01": 16, "F11": 2, "CUP": 16, "CCOMP": 16}
NPR_YAML = {"F00": 256, "F10": 256, "F01": 256, "F11": 256, "CUP": 256, "CCOMP": 544}


class FactorialProto(nn.Module):
    """Native Proto topology with fixed source resampling and a frozen variant role."""
    def __init__(self, c1, c_, c2, variant):
        super().__init__(); assert variant in VARIANTS
        self.variant = variant
        self.cv1 = Conv(c1, c_, k=3)
        self.upsample = nn.ConvTranspose2d(c_, c_, 2, 2, 0)
        self.cv2 = Conv(c_, c_, k=3)
        self.cv3 = Conv(c_, c2)

    def forward(self, x):
        if self.variant == "F10":
            x = F.interpolate(x, scale_factor=0.5, mode="bilinear", align_corners=False, recompute_scale_factor=False)
        elif self.variant == "F01":
            x = F.interpolate(x, scale_factor=2.0, mode="bilinear", align_corners=False, recompute_scale_factor=False)
        x = self.cv3(self.cv2(self.upsample(self.cv1(x))))
        if self.variant == "CUP":
            x = F.interpolate(x, scale_factor=2.0, mode="bilinear", align_corners=False, recompute_scale_factor=False)
        return x


class FactorialSegment(NativeSegment):
    """Use one frozen source tensor for Proto and native P3/P4/P5 for all detection paths."""
    def __init__(self, nc=80, nm=32, npr=256, variant="F00", reg_max=16, end2end=False, ch=()):
        assert variant in VARIANTS and len(ch) == 4
        source_ch, detect_ch = ch[0], ch[1:]
        super().__init__(nc, nm, npr, reg_max, end2end, detect_ch)
        self.variant = variant
        self.source_ch = source_ch
        self.proto = FactorialProto(source_ch, self.npr, self.nm, variant)

    def forward(self, x):
        source, detect_features = x[0], x[1:]
        outputs = Detect.forward(self, detect_features)
        preds = outputs[1] if isinstance(outputs, tuple) else outputs
        proto = self.proto(source)
        if isinstance(preds, dict):
            if "one2one" in preds:
                preds["one2many"]["proto"] = proto
                preds["one2one"]["proto"] = proto.detach()
            else:
                preds["proto"] = proto
        if self.training:
            return preds
        return (outputs, proto) if self.export else ((outputs[0], proto), preds)

