> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# Train-mask gate and deployment-anchor diagnostic

2026-09-26, train-only pre-revision audit. Fixed tensors from 24 augmented,
non-mosaic training images were reused identically for the final M0_s42 and
M0_s128 students. The set deliberately includes 12 images containing a
small-mask proxy; it is an enriched mechanism probe, not a population
estimate. GT area is overlap-mask 160×160 pixel count multiplied by 16,
which is not official COCO area. Teacher and student used no optimizer step.
Optional per-GT instrumentation had bitwise-equal losses on the first batch.

| Student | Small eligible GT | Small gate selected | Same-class score≥.25 NMS matched | Center TAL anchor = NMS anchor | Top-score TAL anchor = NMS anchor | NMS anchor within TAL positives |
|---|---:|---:|---:|---:|---:|---:|
| M0_s42 | 25 | 14 | 21 | 4 | 10 | 21 |
| M0_s128 | 25 | 16 | 24 | 4 | 12 | 24 |

Across all 154 eligible GT on these images, center versus NMS anchor
agreement was 30/150 for seed42 and 34/153 for seed128, while top-score
positive versus NMS was 102/150 and 101/153. All NMS-matched candidates in
this sample were within the same GT's TAL-positive set. Mask gate selection
was not absent for small GT (14/25 and 16/25), so a simple "no small mask
supervision" explanation for validation instability is unsupported. The
center-anchor supervision often targets a different positive than the
deployed candidate. Top-score selection improves this alignment proxy, but
still misses roughly half the matched small candidates.

The NMS comparison uses a separate eval-mode forward on the same train
image, with a score-.25/class-aware/box-IoU≥.5 greedy GT assignment. Train
mode BN and augmentation differ from formal validation inference; exact
deployed candidate identity is not an observable training-time GT label.
Neither anchor agreement nor gate frequency proves an AP mechanism. The
preliminary 16-image smoke was unpaired across randomized augmentation and
is explicitly retained only as failed audit evidence (see
`TRAIN_MASK_GATE_AUDIT_SMOKE_LIMITATION.md`). The paired V1/V2 outputs retain
both valid observations; V2 adds TAL-positive membership and top-score
anchor comparisons.

**Bounded next design:** R0 changes only the representative mask-KD anchor
within each student-TAL-positive GT from geometric center to highest
detached student class score. It keeps the M0 teacher, student initialization,
direct classification/box KD, detached quality gate, mask BCE, weights,
60-epoch optimizer/schedule, input640/ratio4, batch8, last checkpoint and
evaluator. The intended path is greater overlap between supervised and
deployed mask coefficients, not a guaranteed small-AP gain. A numeric
train-only parity/gradient audit must pass before one formal seed2024 run;
D0_s2024 is an already completed same-seed direct-output comparator. Seed2024
is chosen to avoid an extra baseline run and is recorded before any R0
validation result. If R0 lacks an overall or coherent subgroup/cost signal,
do not add seeds to rescue it. No change to M0's recorded STOP decision.
