> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# EXP-SIS-20260922-P1F frozen protocol

This protocol is frozen before P1F replication outcomes. P1A=E, P1B=A+STOP, P1C=F/PIVOT, P1D=H/STOP/`COEFFICIENT-LINE-CLOSED`, and P1E=C/GO/`THIN-PROTOTYPE CAPACITY BOTTLENECK` remain immutable. P1A–P1E, raw data, and historical checkpoints are read-only. No test result is read.

## P1F-0 replication is a hard gate

Use the independently trained P1D `BASE60_s42`, `BASE60_s128`, and `BASE60_s2024` final scheduled checkpoints. Their initialization hash, training horizon, optimizer, image size, batch size, augmentation, and schedule agree; only the registered seed differs. Hashes are frozen in `config.json` and verified before inference.

R1 is the exact immutable P1E 64-image manifest. R2 is every one of the 254 validation images in the inherited dataset manifest. One full-validation inference pass per seed produces both R1 and R2; R1 is a strict key filter, so this does not create a second stochastic evaluation path.

For each final class-aware NMS output, match GT greedily one-to-one by same class and box IoU at least 0.50, exactly as P1E. Thin pixels are the inherited Zhang skeleton pixels whose Euclidean distance to GT background is at most two input pixels; a GT is thin-applicable with at least three such pixels. Native masks, GT-raster-box-support coefficient oracle masks, and predicted-box-support coefficient oracle masks inherit P1E's float64 standardized L-BFGS BCE contract (400 iterations, fixed tolerances). Interior is GT distance greater than four pixels. The material event is GT-support oracle thin failure at least 0.10.

Per seed and scope report selected thin count, all thin GT count, detection absence, native thin-recall median, GT-support oracle thin-recall median, predicted-support oracle thin-recall median, GT-support interior-recall median, boundary F, material count/fraction, and 5,000-replicate image-cluster bootstrap intervals. Missing detections remain missing and are never silently imputed as oracle outcomes.

A seed meets the inherited core gate when oracle thin-recall median is below 0.90, interior-recall median is at least 0.98, and material failure fraction is at least 0.20. `THIN_CAPACITY_REPLICATION=STRONG` requires at least two of three independent seeds to meet the gate on R1 or R2, with direction retained. If only seed42 meets it, the result is `SEED-SPECIFIC`; if R1 replicates but R2 does not, it is `SAMPLE-SPECIFIC`; otherwise P1F stops. Architecture code or training may begin only after a signed `artifacts/replication/gate.json` records `allow_factorial=true`.

## Conditional factorial

If and only if P1F-0 passes, source × lattice variants F00/F10/F01/F11, interpolation control C-UP, and compute control C-COMP are defined in `FACTORIAL_IMPLEMENTATION_CONTRACT.md` before implementation or training. The development seed is 42, horizon is 60, and all non-intervention training/evaluation settings inherit P1D. Three-seed extension is forbidden unless every one of the ten registered development gates passes. Basis-rank control is forbidden unless a spatial/source intervention succeeds on three seeds. Coarse-fine prototypes are outside P1F.

## Operational rules

The GPU is shared with `${OTHER_PROJECT_ROOT}`; P1F does not pause, terminate, or modify that project. Shared-GPU timing is labeled as such and cannot satisfy the isolated latency gate. Every command runs through `run_stage.py` or is captured equivalently with source/config hashes, stdout, stderr, and completion metadata. Interrupted image-level replication resumes only from immutable per-image records after checkpoint/config verification.
