> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG02 VERDICT — B. MODEL-CAPACITY HEADROOM / K2 STOP

**Decision:** `SCALE_HEADROOM=false`, `CAPACITY_HEADROOM=true`, `SELECTED_BRANCH=KD`, `SEED42_SIGNAL=false`, and final stop node **K2 — branch fails**. The native s model showed a real capacity signal, but the frozen n-student KD branch did not convert it into a qualifying accuracy or efficiency signal. **STOP** the ENG02 accuracy-improvement line at this node. Do not start K3, extra Blueberry seeds or MinneApple.

## Evidence and protocol

A0 is an independently re-evaluated, exact-parity reuse of ENG01 E0. A1, A2, K1 and K2 each completed their frozen seed42 60-epoch schedule. The two KD variants started from the pinned native n weights and used the frozen A2 teacher and `lambda_fd=1.0`; K2 added only normalized 2:1 foreground/background feature weights. Final scheduled checkpoint policy was honored. Training and independent full254 evaluator receipts, checkpoint/recovery hashes and per-image prediction/matched-GT files passed audit. The dataset contains 254 validation images and 1,803 GT instances. No test split was read. Historical projects and ICASSP were not modified.

| Model | Purpose | Mask AP | ΔAP vs A0, pp | AP75 | AP90 | Small AP | Δsmall, pp | All-GT coverage | Small coverage |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 native n@640 | reference | 0.840904 | 0 | 0.887850 | 0.741207 | 0.610283 | 0 | 1734/1803 | 110/132 |
| A1 native n@896 | scale screen | 0.843235 | +0.233144 | 0.889891 | 0.760030 | 0.625044 | +1.476087 | 1734/1803 | 115/132 |
| A2 native s@640 | capacity screen and teacher | 0.847758 | +0.685410 | 0.891607 | 0.766430 | 0.646125 | +3.584187 | 1733/1803 | 112/132 |
| K1 vanilla feature KD | deploy native n@640 | 0.842336 | +0.143272 | 0.889433 | 0.747375 | 0.613395 | +0.311128 | 1734/1803 | 106/132 |
| K2 foreground-weighted KD | deploy native n@640 | 0.837969 | −0.293475 | 0.889883 | 0.735942 | 0.607955 | −0.232873 | 1726/1803 | 105/132 |

The preregistered A1 routes required +0.30 pp overall AP or +1.50 pp small AP under the guardrails; A1 narrowly missed both. A2 passed the capacity route. KD continuation required P1 (+0.30 pp overall), P2 (+1.00 pp small with overall/AP75 floors), or P3 (AP within ±0.10 pp plus material isolated efficiency improvement). Neither K1 nor K2 passes. K1's +0.143 pp is an exploratory positive estimate, not a qualifying result. K2 is negative on overall and small AP. Neither meets the numeric severe-damage cutoffs; the branch still fails for insufficient benefit. Because the deployed network is identical in size to A0 and isolated latency was not measured, P3 cannot rescue either variant.

All-GT coverage uses the frozen greedy same-class box match at IoU ≥0.5 and score ≥0.25, distinct from COCO mask AP. On **1,712 common GT** matched by A0/K1/K2, mask IoU is 0.9334/0.9340/0.9339 and boundary F is 0.9254/0.9265/0.9257. For the **102 common small GT**, mask IoU is 0.8687/0.8715/0.8730. These matched-instance means show minor contour effects on survivors; they do not offset the decline in all-GT small coverage from 110 to 106/105. K2 all-GT coverage also falls by eight instances. The per-group FP/FN, area ratio, holes and components are in [`analysis/KD_SEED42_DECISION.md`](analysis/KD_SEED42_DECISION.md); the different denominators are explicit there.

The larger teacher's gain establishes **capacity headroom**, not a promise that raw feature alignment transfers it. Foreground weighting in K2 did not improve the outcome; plausible alternatives include mismatch between native segmentation supervision and feature MSE, teacher–student representational gaps, or insufficient small-object localization information. Those are hypotheses, not demonstrated causes. No validation-driven loss weight, checkpoint, architecture or endpoint was changed to pursue them. The result does not refute localization, output, scale-aware or mask-specific KD methods in the literature.

## Required final status

| Field | Status |
|---|---|
| `ENG02 VERDICT` | **B. MODEL-CAPACITY HEADROOM** (the capacity screen succeeded; the selected KD development branch failed) |
| `SCALE_HEADROOM` | `NO` under frozen A1 gate |
| `CAPACITY_HEADROOM` | `YES`, A2 +0.685 pp overall and +3.584 pp small |
| `SMALL_OBJECT_HEADROOM` | `YES_FROM_A2_ONLY`; A1 and K1/K2 do not pass their relevant gates |
| `SELECTED_BRANCH` | `KD`, selected before formal KD results |
| `SEED42_SIGNAL` | `NO_QUALIFYING_CANDIDATE` |
| `THREE_SEED_STATUS` | `NOT_STARTED_GATE_FAILED` |
| `MINNEAPPLE_STATUS` | `NOT_STARTED_GATE_FAILED`; external raw data remain unopened in ENG02 |
| `EFFICIENCY_STATUS` | `DESCRIPTIVE_SHARED_GPU_ONLY`; same deployed n model for KD, isolated latency unmeasured |
| `LITERATURE_POSITION` | 10 primary KD works and five engineering-journal comparators reviewed; K1/K2 mechanisms are established/adapted, no novelty claim |
| `PUBLICATION_POTENTIAL` | Insufficient for the proposed cross-dataset engineering paper; negative controlled screen is reportable internally |
| `GO/PIVOT/STOP` | **STOP** current ENG02 branch at K2; any different KD objective or architecture requires a new frozen question and budget |

The optional A0@896 inference-only scale probe was not run before A1 and cannot be reconstructed as a preregistered screening result after seeing A1; it does not affect the completed formal comparison. No K3, 128/2024 replication, MinneApple or conditional K5 paper blueprint/method draft was triggered. The final plot is [`analysis/ENG02_AP_COMPARISON.png`](analysis/ENG02_AP_COMPARISON.png), full numeric decision is `analysis/KD_SEED42_DECISION.json`（原资产，本次未收录：`analysis/KD_SEED42_DECISION.json`）, efficiency conditions are in [`efficiency/ENG02_EFFICIENCY.md`](efficiency/ENG02_EFFICIENCY.md), and literature evidence with unverifiable fields marked explicitly is in [`literature/KD_TARGETED_REVIEW.md`](literature/KD_TARGETED_REVIEW.md).
