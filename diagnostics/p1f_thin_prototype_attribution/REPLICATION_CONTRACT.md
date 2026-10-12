> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# P1F-0 replication contract

- Models: P1D clean BASE60 seeds 42, 128, 2024; final scheduled `last.pt`; no checkpoint selection.
- R1: exact byte-identical P1E `sample_manifest.json` (64 validation images).
- R2: all 254 inherited validation images, fixed dataset order.
- Image grid: 640×640, deterministic letterbox, no augmentation.
- Inference: confidence 0.001, IoU 0.7, max detections 300, two classes.
- Matching: same-class greedy one-to-one match, box IoU ≥0.50.
- Thin: inherited Zhang skeleton and GT distance ≤2 px, at least 3 pixels.
- Native mask: selected coefficient with its predicted-box support.
- Oracles: the frozen P1E 32-coefficient float64 standardized L-BFGS problem on GT-raster-box or predicted-box support.
- Interior: GT distance >4 px. Material failure: `1 - oracle_thin_recall ≥ 0.10`.
- Uncertainty: 5,000 image-cluster bootstrap resamples; intervals are sensitivity summaries, not new gates.
- Core gate: oracle thin median <0.90, interior median ≥0.98, material fraction ≥0.20.
- Hard stop: fewer than two independent seeds retain the signal under the registered interpretation; no model training on failure.
