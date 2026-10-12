> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG01 final engineering report

**Stage:** `EXP-SIS-20260923-ENG01` — semantic detail fusion and train-only boundary assistance  
**Decision:** `STOP-CURRENT-DESIGN` at **K2** after the frozen Blueberry replication gate failed.  
**Evidence scope:** Blueberry development validation only; 254 images and 1,803 GT instances per evaluation. No test data were read. P1A–P1F, raw labels, and `${OTHER_PROJECT_ROOT}` were not modified.

## Decision and status

ENG01 completed its six frozen seed42 variants (E0–E5, 60 epochs each), evaluated all six on the full Blueberry validation split, then repeated the only seed42 borderline candidate (E4) at seeds128 and 2024 with paired E0 baselines. All final training/evaluation receipts and checkpoint/output hashes pass. The replication is descriptive evidence, not a powered significance test.

E4 was the seed42 leader, but its paired COCO mask AP gains did not replicate: the three-seed mean is **−0.1532 pp** (sample SD 0.4978 pp; range −0.7275 to +0.1539 pp), with 2/3 positive seeds. The frozen precision gate (+0.30 pp mean and at least 2/3 positive) fails; the modest gate (+0.10 to +0.30 pp mean, all three AP deltas positive and positive mean AP75) also fails. Small AP falls by more than 2 pp at both repeat seeds, triggering the registered quality-review flag. The result therefore stops at K2; MinneApple and more development revisions were not started.

| ENG01_STAGE | `EXP-SIS-20260923-ENG01` |
|---|---|
| DECISION | `STOP-CURRENT-DESIGN` |
| STOP_NODE | `K2` |
| HISTORICAL_P1F_STATUS | `STOP prototype-resolution development extension` — unchanged |
| PRIMARY_METHOD | No supported new method; retain native E0 as current reference |
| BEST_SIMPLE_OR_PRIOR_CONTROL | E0 native YOLO11n-seg; E2 is the closest attention adaptation control |
| BLUEBERRY_SEED42 | E4, +0.1141 pp AP vs E0; borderline allocation signal only |
| BLUEBERRY_REPLICATION | E4 mean −0.1532 pp; 2/3 positive; modest and precision gates fail |
| MINNEAPPLE_STATUS | Not run; Blueberry qualification failed |
| INDEPENDENT_MODULE_VALUE | E4 boundary auxiliary is not replicated; E3 semantic-gated detail is below E0 |
| COMBINATION_VALUE | E5 does not justify retaining both components; AP −0.0386 pp and small AP −2.5183 pp vs E0 at seed42 |
| EFFICIENCY_STATUS | Static parameters/FLOPs recorded; isolated latency not measured |
| LITERATURE_REVIEW_STATUS | 20 technical neighbors and 5 engineering-journal neighbors recorded from primary sources |
| QUARTILE_VERIFICATION_STATUS | JCR and CAS quartiles unverified; no Q2 claim |
| TRAINING_TASKS_USED | 8 unique completed formal jobs (six seed42 plus E4 seeds128/2024); one failed E2 first-step attempt is retained and charged |
| TRAINING_PROCESS_HOURS | 19.94 h logged across training attempts; below 72 h cap |
| TEST_ACCESS | NO |
| NEXT_HUMAN_DECISION | Whether to close this design line or authorize a separately frozen follow-up; no continuation is recommended from current evidence |

## Frozen full254 results

All AP entries are COCO mask AP@[.50:.95], absolute AP columns are fractions, and deltas are percentage points. Seed42 deltas compare each variant with E0 under the same evaluator. E4 repeat deltas compare each seed's E4 checkpoint with its paired E0 baseline.

| Variant | Seed42 AP | Δ AP vs E0 (pp) | Δ AP75 (pp) | Δ small AP (pp) | Δ common-match boundary F (pp) |
|---|---:|---:|---:|---:|---:|
| E0 native | 0.840904 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| E1 simple residual detail | 0.837123 | −0.3781 | −0.4860 | −1.8933 | +0.0809 |
| E2 MLCA adaptation | 0.840370 | −0.0534 | +0.1586 | +0.5663 | −0.0603 |
| E3 semantic-gated detail (SPDF implementation) | 0.840001 | −0.0903 | −0.1789 | −0.0461 | −0.0557 |
| E4 E0 + train-only BAPL boundary loss | **0.842044** | **+0.1141** | **+0.1884** | **+0.9759** | **+0.1134** |
| E5 E3 + BAPL | 0.840517 | −0.0386 | +0.4435 | −2.5183 | +0.0877 |

| E4 paired seed | E0 AP | E4 AP | Δ AP (pp) | Δ AP50 (pp) | Δ AP75 (pp) | Δ AP90 (pp) | Δ small AP (pp) | Δ medium AP (pp) | Δ large AP (pp) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 42 | 0.840904 | 0.842044 | +0.1141 | −0.0044 | +0.1884 | +0.0598 | +0.9759 | −0.0954 | −0.2345 |
| 128 | 0.840163 | 0.841702 | +0.1539 | +0.3994 | +0.1114 | +0.1223 | −2.2738 | +0.2319 | +0.2768 |
| 2024 | 0.842095 | 0.834820 | −0.7275 | −0.3488 | −0.6420 | −1.0405 | −2.0124 | −0.3281 | −0.6080 |
| **Mean** | — | — | **−0.1532** | +0.0154 | −0.1141 | −0.2861 | −1.1035 | −0.0639 | −0.1886 |

Paired AP delta sample SD is 0.4978 pp, with range −0.7275 to +0.1539 pp. This three-seed spread is reported descriptively; it is not a confidence interval or significance test. Only the mean AP50 delta is slightly positive; AP, AP75, AP90, small, medium, and large mean deltas are negative.

![Seed-paired E4 minus E0 AP, AP75, and small-AP deltas](results/figures/REPLICATION_E4_E0.png)

## Required interpretation

1. **Best observed configuration:** E4 at seed42, +0.1141 pp AP versus E0. This small one-seed difference does not establish an improvement; its three-seed mean is negative.
2. **E4 against controls at seed42:** +0.1141 pp vs E0, +0.4922 pp vs E1, +0.1674 pp vs E2, and +0.2044 pp vs E3. These are single-seed comparisons. E1 and E2 themselves do not beat E0 on AP.
3. **Independent SPDF value:** E3 is −0.0903 pp versus E0 and is not a positive independent contribution in this run. E4's seed42 edge cannot be attributed to semantic-detail fusion.
4. **Combination:** E5 is −0.0386 pp vs E0, +0.0517 pp vs E3, and −0.1527 pp vs E4. Although E5 edges E3 on seed42 AP, both remain below E0 and E5 has the small-AP risk; it does not justify keeping both modules. Its seed42 small AP is −2.5183 pp versus E0 and its quality review was completed before replication.
5. **Repeat behavior:** E4 is positive at seeds42/128 but negative at 2024. Mean −0.1532 pp, sample SD 0.4978 pp, range 0.8814 pp. The frozen precision and modest-signal gates both fail. No additional seed is authorized by this result.
6. **MinneApple:** not evaluated because the Blueberry replication qualification failed. No method or split was changed on that dataset; no MinneApple result exists.
7. **Deployment cost:** E4's train graph has 2,844,247 parameters; removing its 1,249-parameter auxiliary head leaves 2,842,998, equal to E0. Static forward compute is 9.7866752 GFLOPs at 640 for both E0 and deployed E4 (THOP convention; 2×MAC). A graph-parity check passed. Batch-8 smoke allocation was 1.654 GB peak allocated / 1.883 GB reserved on a shared GPU. No isolated latency, end-to-end throughput, or deployment peak-memory measurement was made. Do not infer speedup or zero overhead from parameter equality.
8. **Unsuccessful designs:** E1 simple detail fusion, E2 MLCA, and E3 gated detail did not improve seed42 AP over E0; E5 did not show useful combination value and incurred a small-AP risk. E2's first formal attempt failed at the fused AdamW first step due to a stride incompatibility; the failure was preserved, a value-preserving stride fix was verified, and the fixed E2 then completed from epoch 0 under the frozen recipe. No R-A or R-B revision trigger was met.
9. **Most informative literature controls:** BlendMask (semantic/detail basis blending), BMask R-CNN (boundary supervision and mask interaction), and RefineMask (fine-grained feature refinement). ASF-YOLO is the closest journal fusion system; MLCA is the exact official E2 module; YOLOv8-seg-CP is a relevant industrial package. These results differ in dataset, backbone, metric label, training, and sometimes whole-system changes; they are not directly comparable to ENG01 COCO AP@[.50:.95]. The apple journal row reports fixed-threshold Mask mAP50 and an internal delta discrepancy. All journal CAS/JCR quartiles remain unverified.
10. **What ENG01 changed:** implemented and tested a residual detail adapter/gated fusion family and a train-only boundary auxiliary on the pinned native YOLO11n-seg prototype path. E2 uses the official MLCA adaptation. No new backbone, detector, coefficient mapping, or inference-time boundary refinement was added. E4 removes its boundary head at deployment with graph parity.
11. **Evidence sufficiency:** sufficient to stop this frozen design line at K2, not sufficient to claim a paper-ready gain. An external decision is only needed if the user wants to authorize a new, independently frozen research phase; no additional ENG01 run is planned.

## Coverage, shape, efficiency, and integrity

All four new detailed evaluations passed the same 254-image/1,803-GT receipt checks, used the same GT hash, and recorded `test_used=false`; their checkpoint, predictions, AP, matched-GT, and coverage hashes are in each `completion.json`. Mean common matched GT counts for E0/E4 pairs were 1,718 (seed42), 1,715 (seed128), and 1,719 (seed2024). The all-GT coverage table includes missed GTs in its denominator and separately reports common-match shape metrics. Overall paired coverage changes are −0.277, +0.111, and +0.166 pp. Thin-applicable coverage changes are 0.000, +0.366, and +1.099 pp. This does not explain away the two repeated small-AP drops; AP and coverage measure different behavior.

Efficiency evidence is limited to static architecture counts and a shared-device allocation smoke. The E4 deploy graph equals E0 by parameter count and THOP operations; graph output parity is verified after removing the auxiliary head. There is no isolated latency result, so the registered latency route is unmeasured and cannot qualify an efficiency-priority gate.

The technical-neighbor table contains 20 primary-source entries; the engineering-journal table contains five. Each records metric ambiguity/limitations where the source did not permit reliable extraction. JCR/CAS quartiles are explicitly unverified. The first E2 failure and the earlier seed42 summary serialization failure are retained as engineering history; neither changed the frozen metric or scientific gate.

Resource accounting: 8 unique completed formal training jobs (E0–E5 at seed42 and E4 at seeds128/2024), plus one failed first-step E2 attempt charged to the total. Logged training process time is 19.94 h, below the 72 h cap; newly added assets remain well below 40 GB. Disk free at finalization was about 23.1 GiB. The two reused E0 seed128/2024 checkpoints were hash-audited compatible and reevaluated with the ENG01 evaluator. Evaluation and smoke GPU use were shared and are not isolated timing evidence.

## K2 closeout

The frozen repeat shows that E4's seed42 borderline AP advantage is not stable across the registered seeds, and small-object AP incurs repeated losses beyond the numeric quality-review line. The correct action under the prewritten rule is **K2 / STOP current design**. Do not open MinneApple, run more seeds, invoke R-A/R-B, or retrofit a positive paper claim. The separate `PAPER_MAINLINE_BLUEPRINT.md` records the narrow baseline-first position and the evidence needed before any new phase; it does not authorize additional experiments.

Primary artifacts and hashes are indexed in `artifact_index.json`. Detailed receipts, source/config pins, logs, and checkpoints remain in their run folders; the index deliberately avoids hashing the entire historical project tree.
