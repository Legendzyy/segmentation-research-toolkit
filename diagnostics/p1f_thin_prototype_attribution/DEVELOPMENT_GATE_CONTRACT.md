> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1F development gate contract

Frozen before any trained seed-42 factorial result. The comparison baseline is F00 seed42 at its final scheduled epoch. The scientific candidates are F10, F01 and F11; C-UP and C-COMP are attribution controls and cannot be selected as a method. No best checkpoint or intermediate validation result is used.

All six models are evaluated on the complete 254-image validation set with the frozen input-640, confidence 0.001, class-aware NMS 0.7 and max-detections 300 contract. Standard AP metrics use COCO evaluation. Deployment boundary and shape comparisons use the intersection of independently matched GT identities across all six variants. Deployment thin recall includes every frozen thin-applicable GT: an unmatched thin GT contributes all of its thin pixels as false negatives. Oracle comparisons use the intersection of thin GT identities with a valid final class-aware match in all six variants. This prevents a change in detector coverage from masquerading as a prototype-capacity improvement. Per-variant non-common summaries are retained as coverage diagnostics.

A candidate passes conditions 1–7 only when all are true:

1. mask AP is strictly greater than F00;
2. AP75 is strictly greater than F00;
3. small-object AP is strictly greater than F00;
4. all-thin pixel recall is strictly greater than F00;
5. mean common-GT boundary F is strictly greater than F00;
6. median common-thin GT-support oracle recall is strictly greater than F00;
7. common-thin material-failure fraction is strictly lower than F00 and median oracle interior recall is no more than 0.005 below F00.

If more than one candidate passes 1–7, select at most two by the preregistered lexicographic order: larger oracle-thin delta, then AP75 delta, then AP delta, with variant name as the deterministic final tie-break. This ranking is used only after the hard gates and cannot rescue a failing candidate.

Condition 8 requires the candidate to exceed C-UP on both common-thin oracle recall and AP75. Condition 9 requires either (a) exceeding C-COMP on both common-thin oracle recall and AP75, or (b) a clear mechanism separation in which the candidate improves oracle recall and lowers material failures versus F00 while C-COMP does neither. Condition 10 requires a separately run isolated, CUDA-synchronized end-to-end latency median no more than 10% above F00. Shared-GPU observations are descriptive and set condition 10 to `PENDING`, never `PASS`.

Three-seed extension is permitted only when one or two candidates pass every condition, including an isolated condition 10. If none passes, seed128/2024 training is forbidden. Basis-rank control remains forbidden until a source/spatial candidate succeeds over three seeds.
