> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG03 development method specification — output KD v1

**Status (2026-09-27):** implemented and numerically audited, with independent
full254 efficacy now measured. D0 is the plain output-KD control; Q0 adds
task-specific selection. Neither is an established paper contribution. Source:
`src/output_kd_model.py`, frozen `configs/DEVELOPMENT_V1.json`.

## Inputs and deployment

The fixed teacher is ENG02's 60-epoch YOLO11s-seg A2 last checkpoint. The
student is native YOLO11n-seg initialized from the same n pretrained source
used by ENG02. Both consume the identical train image tensor **after** the
same random geometric and color augmentation. The data loader remains the
Ultralytics segment loader; GT identities, overlap masks, class IDs and boxes
come only from training annotations. There is no validation instance lookup,
teacher pseudo-label on unannotated regions or test access.

The teacher and all KD logic exist only while training. At inference the
wrapper returns its original student segmentation graph; `fuse()` drops the
teacher. The student prediction head and NMS protocol are unchanged. The
train-only numeric audit found deployment-fusion output agreement under
`atol=.003, rtol=.001` on one batch (largest leaf mean absolute difference
`6.5e-6`). This is a parity check, not a latency certification.

## Correspondence and supervision

The student native Task-Aligned Assigner (TAL) establishes positive dense
anchors and a **training GT index** per anchor. It is computed on detached
student outputs. The corresponding teacher anchor uses the same feature-map
location/stride; runtime assertions check score/box/coefficient shapes,
stride and `reg_max`. This dense anchor mapping is separate from both
models' post-NMS candidate IDs. The student native GT loss remains active.

For every positive anchor, the true-class independent sigmoid teacher logit
is converted to a probability. BCE-with-logits trains the student true-class
logit on that target. The teacher and student box distributions are decoded
to a common pixel coordinate system; Smooth L1 compares boxes after division
by input width/height. Each GT's positive anchors sum to one instance weight,
then instance weights average over GT with positives. This prevents a GT with
more positives from mechanically dominating the new class/box losses.

For mask supervision, one positive anchor per GT is selected deterministically
by minimum distance to the GT box center. Teacher and student each render
their own coefficient/prototype pair into a **common 160×160 augmented-image
grid**. Teacher sigmoid mask is the soft target; student logits receive BCE
inside the *GT box support*, not a teacher-predicted crop. Each eligible GT
contributes one BCE scalar; the sum is divided by the number of eligible GT.
The native overlap-mask ID mapping is `GT_index+1`; a missing or zero-area GT
mask is skipped with an explicit count. No prototype channels or coefficient
vectors are directly regressed across models.

For D0 all these GT-linked targets are active. For Q0, each task is selected
separately using **detached training-GT quality**:

- Classification: teacher true-class probability exceeds student probability
  by `0.03` and exceeds `0.20`.
- Localization: teacher box IoU to the assigned GT box exceeds student IoU
  by `0.02` and exceeds `0.50`.
- Mask: teacher mask IoU to the GT mask within the common GT box exceeds
  student mask IoU by `0.02` and exceeds `0.50`.

The mask quality is assessed at the same selected anchor and 160² grid used
for mask KD. Selection is binary and detached; the student cannot lower its
own quality to gain an easier weight through that path. These thresholds are
design choices frozen **before** D0/Q0 formal training, not estimated from
the val set. They are not calibrated probabilities. Teacher reliability and
teacher-relative advantage are both required for Q0, while D0 tests whether
selection is necessary at all.

The objective is

`L = L_native + 1.0 L_class_KD + 5.0 L_box_KD + 1.0 L_mask_KD`.

The native loss is returned unchanged in its original components. The KD
scalar is batch-scaled in the wrapper to match the training engine's loss
convention. Teacher targets, quality references and TAL assignment are
detached. Student class, decoded box, coefficient and prototype branches
remain differentiable. A train-only batch check found zero teacher KD
gradient, positive student KD gradient, native no-op difference exactly zero,
and zero KD on an empty-GT batch. Both short train-path smokes completed;
their one-epoch validation values are not model-selection evidence.

## Scope of mechanisms and failure modes

The first mechanism is GT-corresponded **output** targets across detection
and instance mask, including student positives whose final candidate score
may be low. It differs from ENG02 K1/K2 uniform neck-feature matching. The
second proposed mechanism is per-task teacher advantage selection. It may
help avoid pulling a task where the student is already better, but this has
not been demonstrated by AP or a direct ablation. D0 vs Q0 tests that claim.

This version does not supervise duplicate predictions, unmatched/background
candidate scores, or post-NMS ranking directly. Those stay under native GT
loss and default detector training. Consequently, even improved GT-linked
quality cannot be claimed to solve complete prediction behavior until the
independent full254 AP, low-score queue, FP/FN and coverage analyses support
it. Inference latency equivalence also requires separate measurement under
a declared GPU-sharing condition.

## Reproduction and checkpoint policy

The frozen seed42 pair runs D0 then Q0, 60 epochs each, input640/batch8,
AdamW and ENG02-family native augmentation, last scheduled epoch checkpoint.
The formal driver is `src/queue_development_v1.py`. It checks live E: free
space before each run; each epoch stores a full recovery state atomically and
exits only at that safe boundary if free space falls below 9 GiB. Automatic
resume is disabled because exact data-loader continuity has not been proved.
Any failed run remains preserved for audit. Both methods use the same
checkpoint rule and independent ENG03 full254 evaluator as historical A0/K1.
All shared-GPU time is descriptive and cannot be labelled isolated latency.

## Observed outcome and interpretation limit

The predeclared last-checkpoint full254 comparisons are in `RESULTS_MASTER.csv`.
Q0 and C0 lose overall AP to D0 in seed42; M0's seed42 small AP increase
reverses in seed128; R0 ranked-anchor and F0 output-plus-feature controls are
negative in their single seed. D0−N0 overall AP changes sign across the two
fully matched seeds128/2024 (−.1007/+.2284 pp). Consequently this is a
reproducible **implementation specification**, not a validated beneficial
method. The positive common-GT and fixed score-.25 coverage diagnostics do
not identify an AP mechanism. The original class/box/mask KD formula and
training semantics are unchanged; no validation-driven coefficient tuning or
checkpoint selection followed the negative results.
