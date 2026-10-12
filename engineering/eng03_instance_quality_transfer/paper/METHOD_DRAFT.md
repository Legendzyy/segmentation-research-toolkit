> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# Method draft — implemented development version

We study supervised teacher–student transfer for a native YOLO11n instance
segmenter with a fixed YOLO11s teacher. Both models see the same augmented
image. The student's own ground-truth segmentation loss remains active; the
teacher supplies additional task targets only at student-TAL positive dense
anchors. Thus the correspondence key is the **training GT identity and anchor
location**, rather than the rank or index of a post-NMS prediction. Teacher
and student use different prototype bases and coefficient vectors, so our
loss compares rendered instance masks instead of their latent coordinates.

Let `P(i)` be the student positive anchors assigned to GT `i`, `q_t(i,a)`
the teacher true-class sigmoid response, and `b_t(i,a)` the decoded teacher
box at the same dense anchor. We use BCE-with-logits on the student true-class
logit and Smooth L1 on width/height-normalized decoded boxes. Each GT has
unit total class/box weight over its positive anchors before the GT mean.
For the mask term, a deterministic anchor nearest the GT box center is chosen
from `P(i)`. We render teacher and student masks on the native 160×160 mask
grid, and take soft-target BCE on pixels inside the GT box. Mask loss is
averaged by eligible GT count. This keeps the support independent of a
teacher-only box crop that might omit student errors.

The plain control D0 applies all three targets to every eligible training GT.
The selective variant Q0 tests task-dependent teacher quality. Detached
train-GT comparisons enable class KD only when teacher probability exceeds
student probability by 0.03 and exceeds 0.20; box KD only when teacher box
IoU exceeds student by 0.02 and exceeds 0.50; and mask KD only when teacher
mask IoU exceeds student by 0.02 and exceeds 0.50. These comparisons do not
backpropagate. Q0 can therefore differ by task for one instance. Both
variants use `L_native + L_cls + 5 L_box + L_mask`, the same student
initialization, 60 epochs and last-epoch selection.

The teacher is eval-only and no-grad. The student head receives KD gradient
through its logits, decoded boxes, coefficients and prototypes. With all KD
coefficients zero, the native loss vector was identical on the tested batch;
teacher KD gradient was zero; a blank-GT batch produced zero KD. One actual
augmented train target overlay and deployment fusion parity were checked.
These checks establish a functioning implementation path, not an effect on
full-image AP or a causal explanation of earlier K1/K2 results.

The deployed model is the original student segmentation model; no teacher,
selection network or inference adapter is retained. The current method does
not supervise unmatched candidate ranking directly, so any statement that it
addresses that observed failure mode will require independent full254 AP and
candidate-queue evidence. Full implementation details and exact thresholds
are in `METHOD_SPEC.md` and the frozen development configuration.


## Outcome note (2026-09-27)

The implementation and training-only gradient path above are retained as an exact record. Independent full254 now shows Q0 lower than D0 in seed42; M0's small-AP direction reverses by seed128; ranked-anchor R0 and additive F0 are negative in seed2024. D0's paired native overall AP delta changes from −.1007 pp in seed128 to +.2284 pp in seed2024. Accordingly this is a reproducible development method description, **not** a validated paper contribution. No final claim of instance-level quality transfer, superior AP, novelty or cross-dataset performance follows. See `paper/RESULTS_DRAFT.md` and `FINAL_RESEARCH_REPORT.md`.
