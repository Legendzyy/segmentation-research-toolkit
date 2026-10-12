> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# Stage A horizon bridge — interim result

Single legacy seed20260919; each schedule started independently from the same COCO initialization. These are not three independently trained seeds. Values below are percentage points on the fixed full254-val input640 COCO evaluator.

| Fixed final model | AP | AP75 | Small AP | AP90 |
|---|---:|---:|---:|---:|
| BASE30 | 83.9685 | 89.1635 | 59.8191 | 73.3865 |
| BASE45 | 84.0802 | 89.2409 | 61.0741 | 74.4415 |
| BASE60 | 83.8542 | 89.0603 | 60.2616 | 74.4999 |

Registered horizon status: **INCONCLUSIVE**. Extend100: **False**.

BASE60 minus BASE45: AP -0.2260 pp, AP75 -0.1805 pp, AP_small_input640 -0.8126 pp.

The bridge does not show sustained improvement warranting100epochs. The larger small-AP decline prevents a PLATEAU/NEAR-PLATEAU label under the registered absolute-difference rule. This is not evidence that BASE60 is conclusively converged, nor that BASE45 should be selected as a new tuned horizon.

BASE60 versus BASE30 is mixed: AP -0.1144 pp, AP75 -0.1031 pp, AP_small_input640 +0.4424 pp. The claim that the earlier gains are wholly explained by a weak30-epoch model is not established by this single-seed bridge.

Continue the preregistered independent60-epoch reference and fresh75-epoch controls at42/128/2024, then the fixed specialization comparisons. No MinneApple launch or publication decision is licensed by this intermediate result.

All21scheduled BASE45/60 evaluation completion records, checkpoint hashes and full prediction hashes passed. The learning-curve plot includes intermediate snapshots only to diagnose trajectories; final-only selection is unchanged. Intermediate checkpoints within a60-epoch schedule are not independent BASE45 experiments.

Figure: artifacts/figures/stage_a_learning_curves.png. Machine-readable curve metrics: artifacts/analysis/stage_a_curve_metrics.csv. Training times were observed under shared-GPU execution with ICASSP; they are not isolated resource measurements.
