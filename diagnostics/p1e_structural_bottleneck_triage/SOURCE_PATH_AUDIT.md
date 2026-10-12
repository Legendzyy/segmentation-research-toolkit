> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# YOLO11 candidate lifecycle source audit

Pinned source commit `b454f423600f99d41730bd75a7a26b491187de36`. Snapshot hashes are in `artifacts/audit/source_anchors.json`.

## Training selection

`v8SegmentationLoss.get_assigned_targets_and_loss` decodes detached boxes/scores and invokes `TaskAlignedAssigner`; `get_pos_mask` restricts anchor centers to GT boxes, ranks top-k by `score^alpha × CIoU^beta`, and `select_highest_overlaps` resolves multi-GT collisions into `fg_mask` and `target_gt_idx`. Mask IoU, prototype logits and mask coefficients do not enter that assignment metric.

## Inference selection

`non_max_suppression` filters by maximum class confidence, chooses the best class, sorts/limits candidates and applies class-aware box NMS. With `return_idxs=True`, P1E retains the raw 8,400-point source anchor of every survivor. Mask quality does not enter filtering, ranking or NMS.

## Mask branch

`Segment.forward` emits coefficients/prototypes alongside detection predictions. `process_mask` linearly combines coefficients and prototypes, upsamples, thresholds and crops to the predicted box only after detection-driven candidate selection. P1E verified raw coefficient identity against NMS `return_idxs` for every sampled image.

## Exact anchors

- `TaskAlignedAssigner.forward`: `${RUNTIME_ROOT}\.venvs\lednet-p0\lib\site-packages\torch\utils\_contextlib.py:63`; SHA256 `fc396504fd6d6428580f8041944c7418e55fc19e5651f6a0373b152b29bb948c`
- `TaskAlignedAssigner.get_pos_mask`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\tal.py:177`; SHA256 `ef13b44812260227ab0f0bb299471cd830484315d7603df22ff1847fb04d9b5d`
- `TaskAlignedAssigner.get_box_metrics`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\tal.py:203`; SHA256 `ef13b44812260227ab0f0bb299471cd830484315d7603df22ff1847fb04d9b5d`
- `TaskAlignedAssigner.select_highest_overlaps`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\tal.py:343`; SHA256 `ef13b44812260227ab0f0bb299471cd830484315d7603df22ff1847fb04d9b5d`
- `non_max_suppression`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\nms.py:13`; SHA256 `7283e91c5881491c8f1519011244e4aa62eaa070877b950092105a391f3837a4`
- `process_mask`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\ops.py:513`; SHA256 `ae25ae5332497169e357f2152eaf1edca03d4412594a72fd0086b06aedc03f28`
- `crop_mask`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\ops.py:490`; SHA256 `ae25ae5332497169e357f2152eaf1edca03d4412594a72fd0086b06aedc03f28`
- `v8DetectionLoss.get_assigned_targets_and_loss`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\loss.py:403`; SHA256 `b481b5134a787adac8766d3d799598b42ab88eea1264349759240bf1fe2e4237`
- `v8SegmentationLoss.single_mask_loss`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\utils\loss.py:563`; SHA256 `b481b5134a787adac8766d3d799598b42ab88eea1264349759240bf1fe2e4237`
- `Segment.forward`: `${RESEARCH_ROOT}\diagnostics\p1b_publishability_triage\upstream\ultralytics\nn\modules\head.py:337`; SHA256 `e05c5d596533f2758c82ab27b18b5b789f86a8436c7a0e6e9bb2247dd0d61854`