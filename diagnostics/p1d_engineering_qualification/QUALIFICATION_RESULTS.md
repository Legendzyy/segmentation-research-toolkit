> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1D three-seed qualification

**Registered gate:** FAIL
**Decision boundary:** STOP; MinneApple open = false.

| variant | mean AP ΔM0 / Δfresh75 | mean AP75 ΔM0 / Δfresh75 | mean small ΔM0 / Δfresh75 | all-seed primary positive | gate |
|---|---:|---:|---:|---|---|
| B1 | +0.002691 / +0.002055 | -0.000403 / -0.004162 | -0.001930 / +0.003959 | False | False |
| M1 | +0.005253 / +0.004617 | +0.000658 / -0.003101 | +0.002602 / +0.008492 | True | False |
| M2 | +0.003038 / +0.002402 | +0.000773 / -0.002986 | -0.000916 / +0.004974 | False | False |
| M3 | +0.005162 / +0.004525 | +0.001797 / -0.001961 | +0.003930 / +0.009819 | False | False |

M2/M3 qualification requires every seed to improve AP, AP75 and small AP versus its paired M0, plus a positive three-seed mean against fresh75 on all three. The final scheduled checkpoints are used throughout; no best-checkpoint selection or result-based configuration change was made.
