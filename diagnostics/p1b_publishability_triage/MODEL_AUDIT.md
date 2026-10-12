> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Clean model source contract

Repository: https://github.com/ultralytics/ultralytics . All three use commit `b454f423600f99d41730bd75a7a26b491187de36`, version 8.4.155. Exact source excerpts and anchors are in `artifacts/source_anchors.md`. Runtime tensor shapes and final checkpoint hashes are independently recorded under `artifacts/extracted/<model>/`.

| Property | YOLOv8n-seg | YOLO11n-seg | YOLO26n-seg |
|---|---|---|---|
| Mask head | Segment | Segment | Segment26 |
| Prototype input | finest P3 neck map | finest P3 neck map | P3 plus refined, upsampled P4/P5 |
| Prototype generator | Proto | Proto | Proto26 feature fusion then Proto |
| Coefficient inputs | separate convolutions on P3/P4/P5 | separate convolutions on P3/P4/P5 | one-to-many and copied one-to-one branches on P3/P4/P5 |
| Coefficient dimensions | 32 | 32 | 32 |
| Coefficient nonlinearity | final linear 1×1 conv; no tanh/L2 normalization | same | same; inference takes one-to-one branch |
| Prototype grid at 640 | expected 160×160; verify runtime | expected 160×160; verify runtime | expected 160×160; verify runtime |
| Mask equation | a·P | a·P | a·P |
| Native path used here | float32 assembly, bilinear logit resize, predicted-box crop, strict >0 | same | same after end-to-end candidate selection |
| Assignment/detection | one-to-many, class-aware NMS | one-to-many, class-aware NMS | official E2E one-to-many/one-to-one training, one-to-one postprocess |
| Mask training | native v8SegmentationLoss; GT-cropped BCE with box-area normalization | same loss family | same instance loss family plus Proto26 semantic supervision; E2E branches |
| Other differences | v8 backbone/neck; legacy head settings | v11 backbone/neck/head settings | reg_max=1; Proto26 semantic branch in training |

The generations share a linear assembly operation, not an identical coefficient predictor, prototype generator, assignment rule, or complete objective. No source patch makes those differences artificially equal. The 30-epoch recipe standardizes data, image size, optimizer, augmentation family, batch/nominal accumulation, seed and stopping; it does not prove equal convergence.

Baseline training uses the official mask-ratio-4 target and overlap-mask conventions. P1B's oracle and residual probes instead receive the frozen full 640-grid polygon raster and a predicted-support BCE objective. Therefore a base-only P0 gain can reflect objective/resolution recalibration as well as predictor capacity; it does **not** establish missing prototype context. H/P source claims require contrasts against P0 under the same probe objective, plus shuffling controls. This objective distinction is retained explicitly, rather than attributed to a new architecture mechanism.

## Anchors

**Pinned-version selection detail:** `Detect.__init__(end2end=True)` constructs both heads, but `Detect.end2end` checks `_end2end`, which defaults false. `cfg/default.yaml` line 61 defines `nms=None` as external NMS and `nms=False` as the NMS-free head. Consequently the P1B YOLO26 protocol explicitly passes `nms=False` to its validator and sets `head.end2end=True` before raw extraction. YOLO8/11 explicitly use false. E2ELoss selection depends on the existence of the one-to-one head, so this inference flag does not remove either training branch. The first architecture smoke test exposed this before any clean extraction; its failure is retained and the corrected runtime schema is independently checked.

- [Segment and Segment26](https://github.com/ultralytics/ultralytics/blob/b454f423600f99d41730bd75a7a26b491187de36/ultralytics/nn/modules/head.py#L285): `cv4`, `forward_head`, `_inference`, one-to-one prototype detachment.
- [Prototype implementations](https://github.com/ultralytics/ultralytics/blob/b454f423600f99d41730bd75a7a26b491187de36/ultralytics/nn/modules/block.py): `Proto`, `Proto26`.
- [Native mask processing](https://github.com/ultralytics/ultralytics/blob/b454f423600f99d41730bd75a7a26b491187de36/ultralytics/utils/ops.py): `process_mask`, `crop_mask`; retina path excluded.
- [Loss implementations](https://github.com/ultralytics/ultralytics/blob/b454f423600f99d41730bd75a7a26b491187de36/ultralytics/utils/loss.py): `v8SegmentationLoss`, `single_mask_loss`, semantic branch and `E2ELoss`.

Class IDs remain the dataset's original 0/1 labels. Official COCO checkpoints are initialization only; every comparison uses architecture-specific train-split fine-tuning and the final fixed-epoch checkpoint. Historical YOLO11 is kept separately and never substitutes for clean cross-model evidence.
