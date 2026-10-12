> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Native numerical closure — historical reference and clean scope

This establishes a new P1B contract. P1A permanently remains **E — DIAGNOSTIC NOT YET VALID**.

Three different statements must not be conflated:

1. **Optimization convergence:** a small gradient and agreement between solvers establish a solution to the specified BCE objective. They do not establish equivalence between two floating-point implementations.
2. **Linear-span representability:** in real arithmetic, linear interpolation commutes with a linear combination. A target may be well approximated by some vector in that span. Separability can also make unregularized logistic coefficients diverge while the loss approaches an infimum; a finite solver output is not a finite-complexity bound.
3. **Native finite-precision realization:** native inference first forms `float32 a @ P`, then bilinearly upsamples logits, crops by the continuous predicted box, and thresholds at zero. A float64 preinterpolated design matrix performs operations in a different order and precision. Cancellation between large channel contributions can flip near-zero pixels even after optimization has converged.

The 44 high-norm support cases were replayed. The largest raw coefficient norm was 52,534,508.6. Large norm alone is not proof of ill-conditioning: it also depends on prototype scaling and separability. All 505 historical normalized local designs have full numerical rank at the recorded relative 1e-8 cutoff.

## The original blocker

`val/00260 / GT 8` is **unmatched** and therefore a privileged GT-support diagnostic, not a deployed candidate improvement.

| lambda | Native IoU | Ideal-design IoU | Raw norm | Standardized norm | Maximum logit difference |
|---|---:|---:|---:|---:|---:|
| 0, diagnostic only | 0.996396 | 0.994595 | 11725.947 | 5466.760 | 0.002527 |
| 1e-6 | 0.996396 | 0.996396 | 169.165 | 78.658 | 0.000047 |
| 1e-5 | 0.994595 | 0.994595 | 77.633 | 36.754 | 0.000016 |
| **1e-4, frozen primary** | **0.989209** | **0.989209** | **34.563** | **16.252** | **0.000007** |
| 1e-3 | 0.975089 | 0.975089 | 13.644 | 6.668 | 0.000003 |
| 1e-2 | 0.947735 | 0.947735 | 5.299 | 2.697 | 0.000001 |

The unconstrained discrepancy is one binary pixel; its standardized gradient is already 8.66e-9. Convergence therefore does not fix the implementation disagreement. At the frozen primary lambda the discrepancy disappears, with a modest quality cost. No lambda was selected for this instance.

## Stable family

For each support, let `s_j = RMS(X_j)` and `b_j = a_j s_j`. Minimize mean BCE plus `lambda ||b||² / 2`. This is diagonal scale calibration, not whitening: correlated columns remain correlated. The solver uses the ideal design for stable optimization, but **every quality value is rerendered through the native float32 order** and checked against upstream `process_mask`.

All 2,525 positive-lambda historical fits pass the specified gradient/logit/IoU tolerances. All 505 primary fits have identical native and ideal binary IoU; the largest primary logit difference is 1.525e-5 and largest gradient is 9.77e-8. Twenty-four alternate-start support fits agree in objective within 7.96e-13.

For the 250 matched instances under predicted support, the mean native IoU gain is 0.036520 without regularization and **0.030866 at the primary lambda**. Across the positive grid it decreases from 0.035742 to 0.019693 as standardized complexity falls. Thus this checkpoint retains a meaningful stable utilization gap, but the unconstrained and finite-complexity diagnostics are not numerically identical conclusions. Neither BCE solution is a certified maximum-IoU ceiling.

The conditioning measurements remain coordinate-dependent: diagonal channel scaling is normalized, while support, interpolation and general channel mixing change the singular spectrum. All comparisons use the same convention; raw norms are never treated as cross-model evidence.

Evidence: `artifacts/oracle/historical/closure.json`, `regularization_path.csv`, `unconstrained_high_norm_replay.json`, `normalized_spectra.json`, and `alternate_init_audit.json`. Source path: `artifacts/source_anchors.md`. The numerical statements above concern historical tensors only; clean model closure is recorded independently.

## Completed clean-model closure

All three clean models completed their fixed 30 epochs. The same primary lambda and numerical tolerances were applied without selecting by their outcomes.

| Model | Primary fits | Primary failures | Maximum gradient | Maximum native/ideal IoU difference | Maximum logit difference |
|---|---:|---:|---:|---:|---:|
| Clean YOLO11n-seg | 503 | 0 | 7.815e-8 | 0 | 1.548e-5 |
| Clean YOLOv8n-seg | 505 | 0 | 9.569e-8 | 0 | 1.165e-5 |
| Clean YOLO26n-seg | 495 | 0 | 2.084e-7 | 0 | 1.291e-5 |

Including the historical reference, all 2,008 primary fits pass. All 10,040 positive-lambda sensitivity fits also pass the frozen tolerances. They are not all bitwise binary-equivalent: YOLOv8 has a maximum native/ideal IoU difference of 0.00012801 at a nonprimary lambda, below the 0.001 tolerance. The maximum positive-path logit difference across all four sources is 6.1271e-5. Primary quality remains native float32 throughout.

The three-model intersection contains 240 GT instances. On exactly those instances, primary native IoU gains are 0.0299142 (YOLO11), 0.0288091 (YOLOv8), and 0.0315454 (YOLO26). Own-set coverages are 248/255, 250/255, and 240/255 respectively. Thus the existence of a stable utilization gap repeats in all three tested clean checkpoints, conditional on this dataset, recipe and pilot; it is not a theorem about every prototype decoder.

The geometric mechanism is narrower. Predicted-support small-object control is SUPPORTED for clean YOLO11 and YOLOv8 but WEAK for YOLO26; GT-support control is WEAK for all three. In YOLO26, the controlled log-area coefficient for headroom gain is +0.01359 with interval [-0.05349, +0.07188], and for perimeter-error gain is -0.18330 with interval [-0.41840, +0.00612]. Raw small-object IoU gains alone do not establish a common scale mechanism.

The optional conditioning intervention is not activated. Predicted-support pooled log-condition associations are negative in all three clean models, while the YOLO11 val, YOLOv8 train and YOLO26 val intervals each cross zero. GT-support associations are weaker. These findings neither establish stable split-wise evidence nor support the proposed chain from ill-conditioning to larger utilization gap to a useful normalization intervention.

Evidence: per-model `artifacts/oracle/*/closure.json`, final `artifacts/analysis/cross_model_scope.json`, `geometry_regressions.json`, and `conditioning_associations.json`. Learnability and publication decisions require the separate held-out probes and are not issued by this numerical contract.
