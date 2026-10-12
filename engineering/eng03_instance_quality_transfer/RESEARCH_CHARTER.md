> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Research charter (development version, 2026-09-25)

## Question

Can a stronger YOLO11s teacher's instance-level advantage be transferred to
the complete prediction queue of a native YOLO11n student by organizing
classification/localization and mask supervision around the same training GT,
instead of uniformly matching neck features?

## Observations used to choose the first design

1. ENG02 A2 is +0.685410 AP points and +3.584187 small-AP points above A0
   under the same full254 evaluator, while feature KD K1 is only +0.143272
   overall and K2 is −0.293475. The teacher advantage is not a transferable
   ceiling. Source: ENG02 `ENG02_VERDICT.md`.
2. On saved full254 predictions, the independent same-class box diagnostic at
   score≥0.25 finds 21 A2-only and 24 A0-only GT, with 1,698 common GT. For
   20/21 A2-only GT, A0 has an IoU≥0.5 same-class candidate below score .25;
   median A0 score is .089449 versus median A2 matched score .541745. Thus
   at this operating point a low score, rather than complete candidate
   absence, often explains the match difference. This is **not** an AP
   decomposition. Source: `analysis/DESIGN_EVIDENCE.json`.
3. On the 1,698 common GT, teacher box-IoU and historical matched-mask-IoU
   advantages point in opposite directions for 37.63%. K1/K2 change the
   historical common-GT mask IoU mean by only +.000447/+ .000378 relative
   to A0, while K2 loses same-class matches. This motivates separating task
   reliability and keeping complete prediction behavior in view; it does
   not establish that feature KD failed for this reason. Source: the same
   ENG03 table plus ENG02 independent AP.

## Testable design

First implement a **GT-corresponded, task-separated output KD** baseline on
the same augmented train views: aligned dense anchors for class and box,
and rendered teacher/student masks for GT-linked positives in a common
spatial grid. Keep native GT loss. Then test whether detached task-specific
teacher advantage on train GT can limit harmful transfer, instead of using
one foreground weight for every task. Teacher/student original output
channels (prototype and coefficients) will never be directly regressed.

This is a development hypothesis, not yet a demonstrated contribution.
The two proposed mechanisms are (A) task/output correspondence for all
training GT, including low-score student positives, and (B) task-specific
teacher reliability/advantage selection. Native A0, K1, a plain A-only
output KD, B-only/combined contrasts and a nearest mature method must be
compared fairly before a paper claim. If the simpler direct output KD wins,
retain the simpler method.

## Falsifiers and revision limits

- If the positive-anchor path gives no meaningful gradients to the student,
  or teacher mask targets are geometrically misaligned, fix implementation
  before interpreting an AP result.
- If task-specific gating fails to improve over plain output KD, remove it;
  do not rename a simple multi-loss system as a new mechanism.
- If common matched quality improves while full AP or low-score coverage
  weakens, inspect candidate ranking and all-GT behavior before a revision.
- If teacher task advantage on train GT does not predict a useful pattern,
  permit one evidence-backed pivot to training objective/sampling organization
  within the same complete-prediction question.

Validation instances are used only for descriptive development. Their
quality labels will not be imported into training or deployment.

