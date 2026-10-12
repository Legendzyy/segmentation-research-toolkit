> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../../docs/PROVENANCE.md)。

# ENG02 KD seed42 decision

K1/K2 completed their frozen 60-epoch schedules. Independent full254 evaluation and all checked checkpoint, recovery, prediction, AP, matched-GT and coverage hashes passed. AP is COCO mask AP on 254 images/1803 GT. Differences below are percentage points relative to A0.

| Variant | AP | ΔAP pp | AP50 | AP75 | ΔAP75 pp | AP90 | Small AP | Δsmall pp | All-GT coverage | Small coverage | P1 | P2 | P3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| A0 | 0.8409 | +0.000 | 0.9310 | 0.8878 | +0.000 | 0.7412 | 0.6103 | +0.000 | 1734/1803 | 110/132 | - | - | - |
| K1 | 0.8423 | +0.143 | 0.9313 | 0.8894 | +0.158 | 0.7474 | 0.6134 | +0.311 | 1734/1803 | 106/132 | False | False | False |
| K2 | 0.8380 | -0.293 | 0.9284 | 0.8899 | +0.203 | 0.7359 | 0.6080 | -0.233 | 1726/1803 | 105/132 | False | False | False |

P1 requires ΔAP ≥+0.30 pp. P2 requires Δsmall AP ≥+1.00 pp, ΔAP ≥−0.10 pp and ΔAP75 ≥−0.30 pp. P3 requires AP within ±0.10 pp and material isolated efficiency improvement; neither same-size native-n student has such a demonstrated improvement. Neither K1 nor K2 qualifies. K3 was conditional on a clearly positive K1/K2 and is omitted. The frozen stop node is **K2 — branch fails**; no seed128/2024 or MinneApple runs are authorized by this gate.

All-GT coverage counts greedy same-class box matches at IoU ≥0.5 and score ≥0.25, not COCO mask AP. Common-GT shape uses only identities matched by all three models:

| Group | Common GT | Model | Mask IoU | Boundary F | FP pixels | FN pixels | Area ratio | False-hole pixels | Components |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| all | 1712 | A0 | 0.9334 | 0.9254 | 209.4 | 148.0 | 1.0216 | 1.2 | 1.06 |
| all | 1712 | K1 | 0.9340 | 0.9265 | 220.0 | 135.6 | 1.0224 | 1.1 | 1.05 |
| all | 1712 | K2 | 0.9339 | 0.9257 | 210.5 | 141.4 | 1.0208 | 0.5 | 1.06 |
| small | 102 | A0 | 0.8687 | 0.9475 | 67.2 | 33.3 | 1.0465 | 0.0 | 1.00 |
| small | 102 | K1 | 0.8715 | 0.9520 | 67.1 | 32.2 | 1.0475 | 0.0 | 1.01 |
| small | 102 | K2 | 0.8730 | 0.9525 | 62.0 | 33.9 | 1.0378 | 0.0 | 1.01 |
| medium | 1205 | A0 | 0.9300 | 0.9231 | 185.8 | 102.0 | 1.0258 | 0.8 | 1.04 |
| medium | 1205 | K1 | 0.9304 | 0.9240 | 184.0 | 103.9 | 1.0250 | 0.7 | 1.04 |
| medium | 1205 | K2 | 0.9301 | 0.9230 | 182.4 | 104.8 | 1.0250 | 0.1 | 1.04 |
| large | 405 | A0 | 0.9599 | 0.9266 | 315.5 | 313.7 | 1.0026 | 2.8 | 1.11 |
| large | 405 | K1 | 0.9602 | 0.9274 | 365.7 | 255.9 | 1.0085 | 2.7 | 1.09 |
| large | 405 | K2 | 0.9602 | 0.9270 | 331.7 | 277.2 | 1.0040 | 2.1 | 1.12 |

Shared-GPU training/validation times are descriptive; isolated latency was not measured. Test remains sealed.
