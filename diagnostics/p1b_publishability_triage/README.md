> **原生研究记录**：保留当时的方法、数值与判断；只适配路径和链接。历史命令及未收录依赖不能直接运行，草案/计划不等于已执行结果。见 [发布说明](../../docs/PROVENANCE.md)。

# EXP-SIS-20260919-P1B

Stable native oracle, clean cross-model scope, held-out coefficient probes, and publication-value triage. **Completed. P1B verdict A — CROSS-MODEL LEARNABLE COEFFICIENT GAP; publication decision STOP for the current H/P coefficient-calibration mainline.** P1A permanently remains E and is unchanged.

Read the Chinese [final report](FINAL_REPORT.md) and [complete result tables](RESULT_TABLES.md). The stable gap repeats in all three clean models, and all probe/control variants learn small held-out matched-IoU gains on clean YOLO11. H/P specificity and the joint full-AP/AP75/small/boundary gate fail. This is a completed negative publication triage, not an unfinished training run; verdict A does not mean publication MAINLINE-A passed.

## Read first

- [Frozen protocol](PROTOCOL.md) and configuration（原资产，本次未收录：`config.json`）.
- [Numerical contract and historical closure](NUMERIC_CONTRACT.md).
- [Architecture-specific source audit](MODEL_AUDIT.md).
- [30-work novelty matrix and five method-level nearest neighbors](NOVELTY_MATRIX.md).
- [Execution journal and implementation exceptions](EXECUTION_JOURNAL.md).
- [Metric, held-out split, control and resource measurement scope](MEASUREMENT_NOTES.md).

## Evidence layout

| Location | Contents |
|---|---|
| `artifacts/input_freeze.json`, manifests | P1A readback, source/dataset hashes, fixed pilot and train/val view |
| `artifacts/runs/`, `run_registry.jsonl` | Exact CLI, config, source hashes/snapshots, Git diff, stdout/stderr, timing and exit code |
| `artifacts/baselines/` | Clean final-epoch weights and native training logs |
| `artifacts/failed_baselines/` | Preserved failed launch output; never used as baselines |
| `artifacts/extracted/` | Fixed pilot native tensors, matching coverage, actual architecture shapes |
| `artifacts/cache/` | Frozen image-specific prototypes and predicted-box descriptors; no val-fitted probes |
| `artifacts/oracle/` | Unconstrained and fixed positive-lambda paths, native quality and precision audits |
| `artifacts/probes/` | Train-only descriptor bank, 21 independent tiny probes, full training history |
| `artifacts/failed_probes/` | Preserved nondeterministic-backward attempt, excluded from scientific evaluation |
| `artifacts/evaluation/` | Full val detector output RLE masks, COCO-style input-grid AP, matched diagnostics |
| `artifacts/analysis/` | Image-cluster geometric controls, common-GT scope, source contrasts and plots |
| `artifacts/interim_analysis/` | Explicitly labeled earlier snapshots; not the final three-model comparison |
| `artifacts/contracts/` | Implementation/launch checks and isolated test fixtures; not scientific checkpoints |
| `artifacts/literature/` | Primary-source retrieval logs and machine-readable novelty matrix |
| `artifacts/benchmark/` | Isolated batch-1 latency, FPS, parameters, FLOP accounting and VRAM |
| `runtime/`, `data/`, `weights/`, `upstream/` | Local-only runtime/cache/input view and pinned official source; ignored by Git |

## Execution

Run from this directory with the read-only P1A interpreter:

```powershell
& '../p1a_coef_refit/.venv/Scripts/python.exe' -B -u run_stage.py pipeline.py
```

The pipeline skips only stages with an explicit completion record. Do not run a second pipeline copy while the existing one is active. A failed partial training directory must be preserved under `artifacts/failed_baselines` before restarting; no automatic checkpoint selection or best-val tuning is permitted. The probe launcher additionally holds a process lock: an independently launched clean-YOLO11 probe may overlap the independent YOLO26 diagnostic phase if memory permits. A later pipeline caller waits for that owner and never optimizes a second copy. Partial probe checkpoints require inspection and preservation, rather than silent overwrite.

Postprocessing is complete: `analyze_probes.py`, isolated `benchmark.py`, `qualitative.py`, `summarize_results.py`, and `integrity_audit.py` ran through `run_stage.py`; figures were inspected. Integrity and online-output parity passed. Independent CPU integrity checks and fixed qualitative generation ran after probe fitting while full evaluation was active; latency ran after all research GPU jobs ended. Final source/documents are committed before `artifact_index.py` hashes the delivery. Scientific interpretation follows the frozen gates and retained failures. The cache is exact original BGR data in P1B; never overwrite or delete original datasets to reclaim it.

Re-running the pipeline is unnecessary for this completed experiment. It only skips explicitly completed stages and may regenerate analysis; preserve this delivery and its index before intentionally creating a new experiment.
