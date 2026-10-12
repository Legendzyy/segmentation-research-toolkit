> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1B AP translation diagnosis (P1C read-only replay)

These are completed diagnostics of immutable P1B predictions. They are not the P1C training verdict, not new trained variants, and not a selected inference gate. All22 native/probe AP values replay exactly; AP90 is added using the same COCO tensor.

## Regression to the mean is not a supported population description

All21 members improve the mean IoU of native>=.9 pairs (range 0.001484 to 0.002440). None meets the preregistered pattern of positive low-quality mean change and negative high-quality mean change. Individual damaging corrections exist, including large losses; this does not make the group mean negative. P0 also has positive means in the>=.95 bin across all three seeds. The full evaluator adds a further check: 19/21 probes improve AP90, even though18/21 reduce AP75. Negative correlation with native quality alone is constrained by the IoU ceiling and is insufficient evidence of regression.

## Fixed-pair and full-AP denominators differ

For P0/42, fixed diagnostic NetCross(.75)=+7 (15 up,8 down), while full class-aware COCO TP net=-8 (19 up,27 down). The fixed diagnostic set has1728 high-confidence pairs; all7374 frozen candidates participate in the full evaluator. Full AP uses class-aware score-ranked matching, all1803 GT, and area-specific ignore rules. The fixed small matched set has108 instances, compared with132 small GT in the full evaluator.

| area | diagnostic | confidence_band | candidates | tp_up | tp_down | net_tp | active_FP_delta |
|---|---|---|---|---|---|---|---|
| all | False | <.25 | 5364 | 4 | 18 | -14 | -37 |
| all | False | >=.25 | 282 | 0 | 1 | -1 | 1 |
| all | True | >=.25 | 1728 | 15 | 8 | 7 | -7 |
| small | False | <.25 | 5364 | 1 | 5 | -4 | 585 |
| small | False | >=.25 | 282 | 0 | 0 | 0 | 7 |
| small | True | >=.25 | 1728 | 1 | 1 | 0 | 3 |

At AP75, the fixed cohort retains net+7 full-evaluator TPs; the confidence<.25 cohort contributes net-14, and unmatched high-confidence candidates contribute-1. Small-area active false positives rise by585 in the low-confidence cohort. TP counts and their arithmetic do not reconstruct AP because ranking and precision interpolation matter.

## Mask bias and area-range eligibility

Every member shrinks most fixed masks: 78.47%–85.82% of pairs. Mean predicted-area/GT-area change is -0.020318 to -0.014342. P0/42 reduces FP by35.64pixels while increasing FN by26.25pixels per matched instance. Precision rises and recall falls. This supports SHRINK; it does not by itself establish smoothing, systematic hole filling, or removal of isolated thin structures.

A separate skeleton audit gives more specific shape evidence for P0 across all three seeds. Among2000 GT skeleton pixels with distance-to-background<=2input pixels, native misses755; P0 misses880/922/911 (seeds42/128/2024). For small instances the corresponding count rises from53 to65 out of197 pixels in every seed. Thus coverage of raster-defined narrow structures decreases consistently. Skeleton quantization spurs prevent interpreting every such pixel as a semantic thin appendage. Normalized perimeter and component count both increase across seeds, so broad SMOOTH is not supported. There are269 true GT hole pixels overall and only2 in the small subset; filled true-hole pixels decrease by2–4, while false holes inside GT foreground increase. Total predicted-hole area alone would obscure these distinctions. Per-instance evidence and definitions are retained in artifacts/analysis/p1b/topology.

COCO segmentation evaluation obtains detection area from each predicted mask. An unmatched prediction that shrinks into the small-area interval can become an eligible false positive there. This is standard evaluator behavior; scores and boxes need not change. It is a real metric consequence, not permission to alter official AP reporting.

## Bounded counterfactual attribution

Two standard-COCO hybrids apply the already-trained correction only to confidence>=.25 or only to confidence<.25 candidates. Threshold.25 is inherited from the original diagnostic protocol, not chosen from a sweep. A third, explicitly NONSTANDARD diagnostic keeps full P0 masks but substitutes native predicted area only for COCO unmatched-detection area eligibility. No weights are fitted, no GT-driven gate is deployed, and the nonstandard result never replaces reported AP.

| seed | mode | delta_AP75_pp | delta_smallAP_pp |
|---|---|---|---|
| 42 | full P0 (official) | -0.132665 | -1.139281 |
| 42 | correction_conf_ge025_only | 0.403842 | -0.458431 |
| 42 | correction_conf_lt025_only | -0.534561 | -0.678945 |
| 42 | full_correction_native_area_ignore_rule | -0.132665 | 0.161494 |
| 128 | full P0 (official) | 0.120496 | -2.020206 |
| 128 | correction_conf_ge025_only | 0.472670 | -1.440510 |
| 128 | correction_conf_lt025_only | -0.385199 | -0.596525 |
| 128 | full_correction_native_area_ignore_rule | 0.120496 | -0.724270 |
| 2024 | full P0 (official) | -0.009926 | -1.161595 |
| 2024 | correction_conf_ge025_only | 0.456792 | -0.751142 |
| 2024 | correction_conf_lt025_only | -0.324465 | -0.418972 |
| 2024 | full_correction_native_area_ignore_rule | -0.009926 | 0.316532 |

Three-seed mean official small-AP change is -1.4404 percentage points; under the nonstandard frozen-area eligibility ablation it is -0.0821 points. The difference is 1.3583 points. This isolates a substantial area-eligibility contribution for these fixed predictions; it does not prove all small-object mask changes are beneficial or that the training origin of shrinkage has been identified.

High-confidence-only correction improves AP75 in every P0 seed, but small AP still falls in every seed. Thus a confidence split explains part of the translation failure without satisfying the deployment gate. P1B trained its probes on selected matched instances, whereas deployment applies them to all surviving candidates; behavior on excluded low-confidence candidates must be measured rather than inferred from the matched subset.

## Limits

These are paired, validation-only counterfactuals on one fixed clean YOLO11 baseline, not independent training replications of a new method. The21 probes are correlated controls, not21 independent datasets. Area ranges are defined at input640 as in P1B. Boundary-band recall is distinct from the supplementary raster-skeleton audit. P1C formal head/resolution/native-support/capacity results remain the deciding evidence.

Fixed-rule illustrative cases（原资产，本次未收录：`artifacts/analysis/p1b/P0_42_cases.png`）
