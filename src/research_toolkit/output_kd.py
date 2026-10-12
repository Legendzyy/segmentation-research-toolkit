# SPDX-License-Identifier: AGPL-3.0-or-later
# Ported from completed research stages; see evidence/CODE_SOURCE_MAP.json.
"""Train-only GT-corresponded detector/mask output distillation.

`direct`: teacher targets on every student-TAL GT-positive anchor, with a
single representative mask anchor per GT. `rank_mask_selective` uses the
highest detached student class-score TAL-positive anchor for the mask only;
other modes use the geometric-center positive. `selective`: the same targets, but
each task is separately enabled only when the detached teacher GT quality
exceeds the student's. `mask_selective` and `det_selective` isolate those
two gates. Native GT supervision always remains active.
"""
from __future__ import annotations

import json
import torch
import torch.nn.functional as F
from torch import nn

from ultralytics.nn.distill_model import DistillationModel


def elementwise_iou(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    lt = torch.maximum(a[..., :2], b[..., :2])
    rb = torch.minimum(a[..., 2:], b[..., 2:])
    wh = (rb - lt).clamp_min(0)
    inter = wh[..., 0] * wh[..., 1]
    aa = (a[..., 2:] - a[..., :2]).clamp_min(0).prod(-1)
    bb = (b[..., 2:] - b[..., :2]).clamp_min(0).prod(-1)
    return inter / (aa + bb - inter).clamp_min(1e-6)


class InstanceOutputDistiller(DistillationModel):
    """Keep the pretrained YOLO11n inference graph; drop teacher at deployment."""

    def __init__(self, teacher_checkpoint: str, student_model: nn.Module, *, mode: str,
                 lambda_cls: float, lambda_box: float, lambda_mask: float):
        assert mode in {"direct", "selective", "mask_selective", "det_selective",
                        "rank_mask_selective"}
        super().__init__(teacher_checkpoint, student_model)
        self._remove_feature_hooks()
        self.feats_idx = []
        del self.projector  # feature KD is not part of this experiment
        self.mode = mode
        self.lambda_cls = float(lambda_cls)
        self.lambda_box = float(lambda_box)
        self.lambda_mask = float(lambda_mask)
        self.teacher_checkpoint = str(teacher_checkpoint)
        self.last_audit = {}
        self.collect_gt_audit = False
        self.last_audit_gt = []
        self.audit_calls = 0
        self._freeze_teacher()

    @staticmethod
    def _raw_teacher(output):
        assert isinstance(output, tuple) and len(output) == 2 and isinstance(output[1], dict)
        return output[1]

    def _corresponded_losses(self, batch: dict, student: dict, teacher: dict):
        criterion = self.student_model.criterion
        device = batch["img"].device
        bs = batch["img"].shape[0]
        for name in ("scores", "boxes", "mask_coefficient"):
            assert student[name].shape == teacher[name].shape, (name, student[name].shape, teacher[name].shape)
        assert torch.equal(self.teacher_model.model[-1].stride, self.student_model.model[-1].stride)
        assert self.teacher_model.model[-1].reg_max == self.student_model.model[-1].reg_max
        assert teacher["proto"].shape[0] == student["proto"].shape[0] == bs
        assert teacher["proto"].shape[1] == student["proto"].shape[1]
        assert criterion.overlap, "ENG03 overlap-mask training mapping is required"

        with torch.no_grad():
            detached = {key: val.detach() if isinstance(val, torch.Tensor) else val
                        for key, val in student.items()}
            fg, gt_index, target_box, anchor, stride = criterion.get_assigned_targets_and_loss(detached, batch)[0]
        zero = student["scores"].sum() * 0
        bi, ai = fg.nonzero(as_tuple=True)
        if not len(ai):
            self.last_audit = {"GT_with_positive": 0, "positive_anchors": 0}
            self.last_audit_gt = []
            return zero, zero, zero
        gi = gt_index[bi, ai].long()
        nanchors = student["scores"].shape[-1]
        assert fg.shape == (bs, nanchors)
        assert teacher["scores"].shape[-1] == nanchors
        # The native criterion's per-image GT ordering is shared with its
        # overlap-mask IDs; it is not a post-NMS candidate identity.
        img_hw = torch.tensor(student["feats"][0].shape[2:], device=device, dtype=student["scores"].dtype)
        img_hw = img_hw * criterion.stride[0]
        targets = torch.cat((batch["batch_idx"].view(-1, 1), batch["cls"].view(-1, 1), batch["bboxes"]), 1)
        packed = criterion.preprocess(targets.to(device), bs, img_hw[[1, 0, 1, 0]])
        labels = packed[..., 0].long()
        cls = labels[bi, gi]
        assert torch.all((cls >= 0) & (cls < student["scores"].shape[1]))

        slogit = student["scores"].permute(0, 2, 1)[bi, ai, cls].float()
        tlogit = teacher["scores"].permute(0, 2, 1)[bi, ai, cls].float().detach()
        tprob = tlogit.sigmoid()
        sprob = slogit.detach().sigmoid()
        with torch.no_grad():
            sb = criterion.bbox_decode(anchor, student["boxes"].permute(0, 2, 1).float().detach()) * stride
            tb = criterion.bbox_decode(anchor, teacher["boxes"].permute(0, 2, 1).float().detach()) * stride
            gt_box = target_box[bi, ai].float()
            siou = elementwise_iou(sb[bi, ai], gt_box)
            tiou = elementwise_iou(tb[bi, ai], gt_box)
        # Decode again WITH student gradient. Teacher remains detached.
        student_box = criterion.bbox_decode(anchor, student["boxes"].permute(0, 2, 1).float())[bi, ai] * stride[ai]
        teacher_box = tb[bi, ai]
        pair = bi * (packed.shape[1] + 1) + gi
        unique, inverse, counts = torch.unique(pair, return_inverse=True, return_counts=True)
        per_anchor = counts[inverse].float().reciprocal() / len(unique)
        if self.mode in {"selective", "det_selective"}:
            cls_gate = ((tprob > sprob + .03) & (tprob > .2)).float().detach()
            box_gate = ((tiou > siou + .02) & (tiou > .5)).float().detach()
        else:
            cls_gate = box_gate = torch.ones_like(per_anchor)
        cls_loss = (F.binary_cross_entropy_with_logits(slogit, tprob, reduction="none") * per_anchor * cls_gate).sum()
        scale = torch.tensor([img_hw[1], img_hw[0], img_hw[1], img_hw[0]], device=device)
        box_error = F.smooth_l1_loss(student_box / scale, teacher_box / scale,
                                     reduction="none", beta=.02).mean(-1)
        box_loss = (box_error * per_anchor * box_gate).sum()

        # One fixed geometrically selected positive anchor per training GT.
        # No high-confidence post-NMS intersection is required.
        mask_losses = []
        mask_selected = 0
        mask_total = 0
        gt_audit = []
        smask = student["mask_coefficient"].permute(0, 2, 1)
        tmask = teacher["mask_coefficient"].permute(0, 2, 1).detach()
        sp = student["proto"]
        tp = teacher["proto"].detach()
        masks = batch["masks"].to(device)
        mh, mw = masks.shape[-2:]
        if sp.shape[-2:] != (mh, mw):
            sp = F.interpolate(sp, (mh, mw), mode="bilinear", align_corners=False)
        if tp.shape[-2:] != (mh, mw):
            tp = F.interpolate(tp, (mh, mw), mode="bilinear", align_corners=False)
        yy = torch.arange(mh, device=device)[:, None]
        xx = torch.arange(mw, device=device)[None, :]
        anchor_px = anchor * stride
        for value in unique:
            positions = torch.where(pair == value)[0]
            first = positions[0]
            b, g = int(bi[first]), int(gi[first])
            gbox = target_box[b, ai[first]].float()
            center = (gbox[:2] + gbox[2:]) / 2
            dist = ((anchor_px[ai[positions]] - center).square()).sum(-1)
            if self.mode == "rank_mask_selective":
                cls_for_gt = labels[b, g]
                detached_score = student["scores"][b, cls_for_gt, ai[positions]].detach()
                a = int(ai[positions[detached_score.argmax()]])
            else:
                a = int(ai[positions[dist.argmin()]])
            truth = (masks[b] == g + 1)
            if not bool(truth.any()):
                continue
            roi = (xx >= gbox[0] * mw / img_hw[1]) & (xx < gbox[2] * mw / img_hw[1]) & \
                  (yy >= gbox[1] * mh / img_hw[0]) & (yy < gbox[3] * mh / img_hw[0])
            if not bool(roi.any()):
                continue
            sl = torch.einsum("c,chw->hw", smask[b, a].float(), sp[b].float())
            with torch.no_grad():
                tl = torch.einsum("c,chw->hw", tmask[b, a].float(), tp[b].float())
                tsp = tl.sigmoid()
                gt = truth & roi
                tbin = (tsp > .5) & roi
                sbin = (sl.detach().sigmoid() > .5) & roi
                ti = (tbin & gt).sum().float() / (tbin | gt).sum().clamp_min(1)
                si = (sbin & gt).sum().float() / (sbin | gt).sum().clamp_min(1)
                enabled = bool(self.mode in {"direct", "det_selective"} or
                               (ti > si + .02 and ti > .5))
            mask_total += 1
            if self.collect_gt_audit:
                positive_anchors = ai[positions]
                positive_scores = student["scores"][b, labels[b, g], positive_anchors].detach().sigmoid()
                gt_audit.append(dict(batch_index=b, gt_index=g, anchor_index=a,
                                     category_id=int(labels[b, g]),
                                     positive_anchor_indices=[int(v) for v in positive_anchors],
                                     top_score_positive_anchor=int(positive_anchors[positive_scores.argmax()]),
                                     center_anchor_class_score=float(student["scores"][b, labels[b, g], a].detach().sigmoid()),
                                     top_positive_class_score=float(positive_scores.max()),
                                     bbox_xyxy=[float(v) for v in gbox],
                                     mask_area_proxy_input640=int(truth.sum()) * 16,
                                     teacher_mask_iou=float(ti), student_mask_iou=float(si),
                                     mask_gate_enabled=enabled))
            if enabled:
                mask_selected += 1
                mask_losses.append(F.binary_cross_entropy_with_logits(sl[roi], tsp[roi]))
        mask_loss = torch.stack(mask_losses).sum() / max(mask_total, 1) if mask_losses else zero
        self.last_audit = dict(GT_with_positive=len(unique), positive_anchors=len(ai),
                               cls_gate_fraction=float(cls_gate.mean().detach()),
                               box_gate_fraction=float(box_gate.mean().detach()),
                               mask_GT_eligible=mask_total, mask_GT_selected=mask_selected,
                               native_mask_grid=[mh, mw])
        self.last_audit_gt = gt_audit
        return cls_loss, box_loss, mask_loss

    def loss(self, batch, preds=None):
        if not self.training:
            if preds is None:
                preds = self.student_model(batch["img"])
            native, items = self.student_model.loss(batch, preds)
            zero = native.new_zeros(1)
            items["coord_kd_loss"] = zero.squeeze().detach()
            return torch.cat((native, zero)), items
        with torch.no_grad():
            teacher = self._raw_teacher(self.teacher_model(batch["img"]))
        student = self.student_model(batch["img"])
        native, items = self.student_model.loss(batch, student)
        cls, box, mask = self._corresponded_losses(batch, student, teacher)
        kd = self.lambda_cls * cls + self.lambda_box * box + self.lambda_mask * mask
        assert torch.isfinite(kd).all()
        if self.audit_calls == 0:
            print("ENG03_FIRST_BATCH_AUDIT=" + json.dumps({
                **self.last_audit, "mode": self.mode,
                "native_components": [float(v.detach()) for v in native],
                "kd_cls": float(cls.detach()), "kd_box": float(box.detach()),
                "kd_mask": float(mask.detach()), "kd_weighted": float(kd.detach())
            }), flush=True)
        self.audit_calls += 1
        items["coord_kd_loss"] = kd.detach()
        return torch.cat((native, (kd * batch["img"].shape[0]).reshape(1))), items
