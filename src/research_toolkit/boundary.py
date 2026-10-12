# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""Augmentation-aligned, per-instance boundary targets and the train-only objective."""
from __future__ import annotations

import cv2
import numpy as np
import torch
import torch.nn.functional as F

from .settings import BOUNDARY_CONFIG as CONFIG
from ultralytics.data.augment import Format
from ultralytics.data.dataset import YOLODataset
from ultralytics.data.utils import polygon2mask
from ultralytics.nn.tasks import SegmentationModel
from ultralytics.utils.loss import v8SegmentationLoss


def instance_boundary_target(segments, shape: tuple[int, int], valid: np.ndarray | None):
    """Compute the union only after taking each augmented instance boundary."""
    height, width = shape
    boundary = np.zeros((height, width), np.uint8)
    kernel = np.ones((5, 5), dtype=np.uint8)  # radius two input pixels
    for segment in segments:
        mask = polygon2mask((height, width), [segment.reshape(-1)], color=1, downsample_ratio=1)
        if not mask.any():
            continue
        expanded = cv2.dilate(mask, kernel, iterations=1)
        eroded = cv2.erode(mask, kernel, iterations=1)
        boundary |= expanded - eroded
    if valid is None:
        valid = np.ones((height, width), np.uint8)
    else:
        assert valid.shape == (height, width), (valid.shape, shape)
        valid = (valid > 0).astype(np.uint8)
    boundary *= valid
    target = torch.from_numpy(boundary[None, None].astype(np.float32))
    validity = torch.from_numpy(valid[None, None].astype(np.float32))
    target = F.max_pool2d(target, 4, 4)[0, 0]
    # Only fully valid input cells contribute; this excludes letterbox/affine padding.
    validity = -F.max_pool2d(-validity, 4, 4)[0, 0]
    return target, validity


class BoundaryFormat(Format):
    def apply_instances(self, labels, params=None):
        h, w = params["h"], params["w"]
        segments = params["instances"].segments if params["instances"] is not None else []
        valid = labels.pop("semantic_mask", None)
        target, validity = instance_boundary_target(segments, (h, w), valid)
        labels = super().apply_instances(labels, params)
        labels["boundary_target"] = target
        labels["boundary_valid"] = validity
        return labels


class BoundaryDataset(YOLODataset):
    format_class = BoundaryFormat

    def get_image_and_label(self, index):
        labels = super().get_image_and_label(index)
        labels["semantic_mask"] = np.ones(labels["img"].shape[:2], np.uint8)
        return labels

    @staticmethod
    def collate_fn(samples):
        targets = torch.stack([item.pop("boundary_target") for item in samples], 0)
        valid = torch.stack([item.pop("boundary_valid") for item in samples], 0)
        result = YOLODataset.collate_fn(samples)
        result["boundary_target"] = targets
        result["boundary_valid"] = valid
        return result


def balanced_boundary_loss(logits, target, valid):
    assert logits.shape[:2] == (target.shape[0], 1)
    assert logits.shape[-2:] == target.shape[-2:] == valid.shape[-2:]
    per_pixel = F.binary_cross_entropy_with_logits(logits[:, 0].float(), target.float(), reduction="none")
    per_image = []
    for i in range(logits.shape[0]):
        pos = (target[i] > 0.5) & (valid[i] > 0.5)
        neg = (target[i] <= 0.5) & (valid[i] > 0.5)
        parts = []
        if pos.any():
            parts.append(per_pixel[i][pos].mean())
        if neg.any():
            parts.append(per_pixel[i][neg].mean())
        per_image.append(sum(parts) / len(parts) if parts else logits[i].sum() * 0)
    return torch.stack(per_image).mean()


class ENGSegmentationLoss(v8SegmentationLoss):
    def loss(self, preds, batch):
        native, metrics = super().loss(preds, batch)
        if "boundary_logit" not in preds:
            if torch.is_grad_enabled():
                raise RuntimeError("Boundary variant lost its train-only logits")
            # The deploy graph omits the auxiliary head during validation.
            # Official segmentation metrics still use exactly the native loss.
            metrics = dict(metrics)
            metrics["boundary_loss"] = native.new_zeros(()).detach()
            return native, metrics
        aux = balanced_boundary_loss(
            preds["boundary_logit"], batch["boundary_target"], batch["boundary_valid"]
        )
        weighted = float(CONFIG["boundary"]["weight"]) * aux
        # Official loss is a per-batch vector. Adding one batch-scaled element
        # makes the trainer's .sum() apply exactly one batch factor.
        total = torch.cat((native, weighted.reshape(1) * batch["img"].shape[0]))
        metrics = dict(metrics)
        metrics["boundary_loss"] = weighted.detach()
        return total, metrics


_NATIVE_INIT_CRITERION = SegmentationModel.init_criterion


def install_training_hooks():
    """Only call for E4/E5 in the current process, before trainer construction."""
    import ultralytics.data.build as build

    build.YOLODataset = BoundaryDataset

    def criterion_for_variant(model):
        return ENGSegmentationLoss(model)

    SegmentationModel.init_criterion = criterion_for_variant
