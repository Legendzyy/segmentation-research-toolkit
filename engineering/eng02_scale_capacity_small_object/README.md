> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# ENG02 — native scale and capacity headroom screening

Stage `EXP-SIS-20260924-ENG02` is authorized by `USER_REQUEST_ENG02.md`. This is a new engineering phase; P1A–P1F and ENG01 remain read-only historical evidence.

Current phase: **complete at K2/STOP**. A0 reused the audited ENG01 E0 final checkpoint after exact independent evaluator parity. A1 (native n, 896, batch 8) and A2 (native s, 640, batch 8) completed under `configs/FROZEN_STAGE_A.json`. The preregistered Stage A result was `SCALE_HEADROOM=false`, `CAPACITY_HEADROOM=true`, hence `BRANCH_KD`. Both frozen K1/K2 KD variants finished 60 epochs and independent full254 evaluations with verified hashes. Neither met the seed42 continuation gate; K3, three-seed replication and MinneApple were not triggered. Read `ENG02_VERDICT.md`, `analysis/KD_SEED42_DECISION.md`, and `ARTIFACT_INDEX.json` for the final evidence. A2 is a capacity reference/teacher only; deployed KD students remained native n. Test data remain sealed. Shared-GPU observations are descriptive, not isolated latency results.

See `RESUME.md` and `EXECUTION_JOURNAL.md` for the latest durable position.
