> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG01 — semantic detail fusion and train-only boundary assistance

Stage ID: `EXP-SIS-20260923-ENG01`. **Final status: K2 / STOP-CURRENT-DESIGN.**

This stage tested six frozen YOLO11n-seg variants on Blueberry and repeated the sole seed42 borderline candidate against paired baselines. E4's seed42 AP delta was +0.1141 pp, but the three-seed mean was −0.1532 pp (2/3 positive); the registered repeat gates failed and small AP declined by >2 pp at both repeat seeds. MinneApple was not opened. No test data were read.

All six seed42 runs and the E4 seed128/2024 repeats completed with passing training receipts. Their full254 evaluations and all-GT/paired summaries are hash-pinned under `results/`. Current status and evidence are in `RESUME.md`, `FINAL_ENGINEERING_REPORT.md`, `PAPER_MAINLINE_BLUEPRINT.md`, and `artifact_index.json`.

The deployed E4 graph removes the auxiliary boundary head and has the same static parameter/FLOP counts as E0; graph parity passed. Isolated latency was not measured. All GPU timing context was shared/non-isolated. The literature register contains 20 technical neighbors and five engineering-journal neighbors; CAS/JCR quartiles remain unverified.

No further ENG01 runs are planned. Any continuation requires a separately authorized and frozen phase; historical P1A–P1F and `${OTHER_PROJECT_ROOT}` remain untouched.
