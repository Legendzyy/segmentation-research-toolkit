> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# EXP-SIS-20260921-P1E final report

## P1E VERDICT

**C. THIN-PROTOTYPE CAPACITY BOTTLENECK**

## Required statuses

| Status | Result |
|---|---|
| `CANDIDATE_MASK_ALIGNMENT` | **MODERATE** |
| `MASK_SCORE_ALIGNMENT` | **PARTIAL** |
| `THIN_PROTOTYPE_CAPACITY` | **LOCALLY_LIMITED** |
| `GLOBAL_LOCAL_CONTROL` | **COUPLING-WEAK** |
| `SUPPORT_COUPLING` | **NO-EVIDENCE** |
| `FAULT_TAXONOMY` | **COMPLETE** |
| `NOVELTY_RISK` | **HIGH** |
| `RECOMMENDED_BRANCH` | **prototype** |
| `PUBLICATION_POTENTIAL` | **CONDITIONAL** |

Final decision: **GO**

## Scope and integrity

P1E used the preregistered P1D `BASE60_s42` checkpoint (SHA256 `ab8985871ae126ba0007a5ca19b1bbee416449655fd7c3464e6c62cbc59985b5`) on 64 deterministic validation images containing 453 GT. It read no test outcome, trained no model, and did not modify P1A–P1D. Candidate masks, prototype tensors, assignments, NMS identities, oracle coefficients, local-residual masks, commands and hashes are retained under `artifacts/`.

The registered global oracle used float64 standardized L-BFGS for at most 400 iterations. A sensitivity continuation of every one of the 61 selected thin instances for 1,200 additional iterations changed no thresholded thin-recall value (maximum numerical delta 1.11e-16); its median remained 0.875000. The completion manifest's `all_finite=false` is fully explained by non-applicable thin metrics on 311 selected non-thin instances; all applicable thin rows are finite.

## Frozen gate outcomes

| Diagnostic | Registered gate | Observation | Outcome |
|---|---|---|---|
| Candidate selection | ≥20% relevant GT with gap≥.03, or ≥30% in an n≥30 named subgroup | overall 11.21%; small 22.22%; thin 18.03%; close 11.29% | `MODERATE`, GO-A not met |
| Thin prototype | GT-support median<.90, interior median≥.98, material residual fraction≥.20 | thin recall 0.875000; interior 1.000000; material residual 52.46% | `LOCALLY_LIMITED`, GO-B met |
| Box/support | GT-support recovery with material GT-minus-predicted support loss | median thin gap 0.000000; median IoU gap 0.003551 | `NO-EVIDENCE` |
| Local control | median thin gain≥.05, repetition≥20%, no FP loss, random margin≥.03 | median gain 0.000000; random 0.000000; repetition 39.34% | `COUPLING-WEAK`, GO-C not met |

Image-cluster bootstrap sensitivity (5,000 replicates) gives GT-support thin-recall median CI [0.777778, 1.000000], material-failure fraction CI [0.409091, 0.636364], and interior-recall median CI [1.000000, 1.000000]. These intervals are sensitivity summaries, not new decision gates.

## Candidate lifecycle and alignment

SET-A stores class-consistent raw anchors with decoded box IoU≥.30; SET-B stores official TAL positives; SET-C applies the frozen .001 confidence floor; SET-D is the final class-aware NMS match at box IoU≥.50. The source audit demonstrates that training selection is driven by class score and CIoU-derived TAL alignment, inference filtering/ranking/NMS is detection-driven, and mask coefficients/prototypes are decoded after those decisions.

Of 446 relevant GT, the candidate mask-IoU gap has mean 0.014841, median 0.004033, and ≥.03 rate 11.21%. Privileged re-selection improves matched mean mask IoU by 0.014841, boundary F by 0.022802, thin recall by 0.330211, and the matched IoU≥.75 proxy by 0.040359; none is deployable AP. Cluster-median Spearman correlations are detection score↔mask IoU 0.301944, TAL↔mask IoU 0.668131, and box IoU↔mask IoU 0.891200.

## Prototype and local-control diagnosis

For 61 thin instances, the GT-support oracle reaches median thin recall 0.875000 while median interior recall is 1.000000; 32/61 retain at least .10 thin failure. The predicted-support median is 0.666667, but the median GT-minus-predicted support gap is 0.000000; support truncation therefore does not explain the registered population result. The stable high-budget continuation leaves this conclusion unchanged.

The width-4 privileged local correction yields median thin gain 0.000000; the equal-controllable-pixel random median is 0.000000. Although 39.34% of thin cases individually gain ≥.05 without FP loss, the registered median and random-margin conditions fail. This is heterogeneous headroom, not a qualified global-local bottleneck.

## Interaction of bottlenecks

1. Candidate gap and GT-support global-oracle IoU gain have Spearman ρ=0.721318 across 446 relevant GT, so these ceilings overlap rather than define independent populations.
2. Among 37 thin instances with candidate gap<.01 or unavailable, 13 show local gain≥.05. The median/random gates still reject local control as the main branch.
3. Prototype failure is a thin-subgroup result: 32/61 thin instances retain material failure. The mutually exclusive precedence moves many such cases into earlier E/A/C labels; the 4 TYPE-D headline count must not be read as the prevalence of the continuous prototype signal.

## Mutually exclusive fault taxonomy

| Type | GT | Fraction |
|---|---:|---:|
| `UNRESOLVED` | 191 | 42.16% |
| `TYPE-B_COEFFICIENT_UTILIZATION` | 152 | 33.55% |
| `TYPE-E_BOX_SUPPORT` | 50 | 11.04% |
| `TYPE-A_SELECTION` | 35 | 7.73% |
| `TYPE-C_LOCAL_CONTROL` | 14 | 3.09% |
| `TYPE-F_DETECTION_ABSENCE` | 7 | 1.55% |
| `TYPE-D_PROTOTYPE` | 4 | 0.88% |

`UNRESOLVED` is the largest headline bin (191/453). Among resolved bins, `TYPE-B_COEFFICIENT_UTILIZATION` is largest (152/453, 33.55%); that is historical decoder/coefficient-utilization evidence and does not reopen the coefficient line.

## Twelve required answers

1. **Does a better mask candidate already exist?** Yes for a minority; the ≥.03 rate is 11.21%, below GO-A.
2. **Do score/TAL mis-rank mask quality?** Partially. Detection-score correlation is 0.301944; TAL is 0.668131. The registered ranking bottleneck gate is not met.
3. **Is the gap stronger for small/thin/close cases?** Small and thin rise to 22.22%/18.03%; neither reaches the frozen 30% subgroup gate. Close cases are 11.29% and dominate the sample, so they do not isolate a stronger effect.
4. **Can coefficient refitting recover thin structures?** Only incompletely: GT-support median thin recall is 0.875000.
5. **Is there a thin-specific prototype ceiling?** Yes under the frozen gate: `LOCALLY_LIMITED`; interior is perfect at the median while 52.46% retain material thin failure.
6. **Does predicted-box support truncate key structure?** It does in individual cases, but the population verdict is `NO-EVIDENCE` because both registered median gaps are small.
7. **Does global coefficient correction inherently create an FP/thin trade-off?** The frontier is heterogeneous; evidence is `COUPLING-WEAK`.
8. **Can local boundary correction remove the trade-off?** It helps a minority but has zero median advantage and no qualified random-control margin.
9. **What failure source dominates?** Overall, 42.16% remain unresolved. Among resolved categories, decoder/coefficient utilization is largest at 33.55%; the only new gate-qualified actionable signal is thin-prototype capacity.
10. **Which instance category is most common?** `UNRESOLVED`, 191/453 (42.16%).
11. **What are the most dangerous nearest works?** maIoU/GmaIoU and mask-aware matching for assignment; Mask Scoring R-CNN for ranking; PatchDCT for compact-vector coupling; PointRend, Boundary Patch Refinement, SharpContour and Mask Transfiner for local refinement. `NOVELTY_RISK=HIGH`.
12. **Is another method round justified?** **GO**, only for one minimal P1F prototype-resolution branch. No model is trained in P1E.

## Novelty and limits

The 34-work primary/official matrix blocks broad novelty claims about mask-aware assignment, score-quality alignment, spatial coefficients, high-resolution refinement, boundary residuals and thin preservation. The P1E contribution is the frozen diagnosis. The sample is one model seed and 64 development images; nearly every thin instance is also close-neighbor, and the bootstrap upper bound for median thin recall reaches 1.0. P1F must therefore be a strict falsification experiment, not an assumption that publication value is established.

## Decision

**GO** — generate one P1F blueprint for the thin-prototype branch only. Keep P1A–P1D verdicts unchanged and keep the coefficient line closed.
