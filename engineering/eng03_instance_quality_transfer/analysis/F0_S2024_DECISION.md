> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# F0 additive control: independent full254 decision

2026-09-27, Blueberry development val, 254 images / 1803 GT, input640. F0 completed the frozen 60-epoch seed2024 run. Its scheduled last checkpoint passed independent evaluation. The descriptive paired table and per-instance evidence are `F0_S2024_PAIRED_EVALUATION.json` and `f0_s2024_instance_evidence.csv`; training and evaluation receipts remain in `runs/F0_s2024` and `analysis/evaluation/F0_s2024`.

| Mask endpoint | N0 native | K1 feature MSE | D0 output KD | F0 additive |
|---|---:|---:|---:|---:|
| AP | .842095 | .842411 | .844379 | .840628 |
| AP75 | .893193 | .892507 | .895112 | .890732 |
| AP90 | .743623 | .743782 | .745004 | .743983 |
| Small AP | .628707 | .596647 | .622610 | .626585 |

F0−D0 is −0.3751 pp overall AP, −0.4381 pp AP75, −0.1021 pp AP90, and +0.3976 pp small AP. Fixed score-.25 same-class coverage is 1725 versus D0's 1731 GT. Among 1708 aligned common GT, mean mask IoU changes −.000446 and boundary F −.000224. These fixed-threshold and conditional comparisons do not decompose AP or establish a cause. F0 also trails the same-seed native and K1 controls in overall AP. Shared-GPU times are non-isolated process times, not latency.

**Decision: STOP F0 seed expansion.** The simple additive feature term has no coherent complete-prediction gain in this one seed. This negative result does not prove every representation-plus-output approach fails, but it removes the present basis for spending another seed on this exact recipe. F0 is not a paper finalist or a novel mechanism claim.

The remaining small positive D0−N0 AP advantage was observed in only one fully matched seed. A bounded next test is a **native N0 seed128** run using the exact same 60-epoch control recipe except seed; D0_s128 is already complete and independently evaluated. The seed128 comparison is a resource gate, not a significance test. Recorded before seeing N0_s128: consider a K1_s128 matched strong-control run only if D0−N0 has overall AP ≥+0.10 pp, at least one of AP75/AP90 positive, and small AP no worse than −1.0 pp. Otherwise stop this branch's seed expansion, analyze the failure, and prepare the negative-evidence PAUSE-B deliverable. Any subsequent K1 run needs its own frozen plan and resource check; this document does not launch it. Mature-neighbor adaptation and MinneApple development remain unperformed. No test access.
